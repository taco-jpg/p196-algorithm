// wincd.h -- r9u: a second, coarser window family that keeps only the carry bits c and the d bits of w consecutive slots (no r digits),
// so that much longer windows fit in memory (2^(2w) bits per phase: w = 16 -> 512 MB).
// Abstract step: the per-slot rule of FILTER_R8 section 1 run over the w slots from ANY start value x in 0..2B-2 and with ANY incoming
// overflow digit r_t in 0..B-1 at each overflow slot (the incoming digits are not part of the abstract state, so they are left free);
// no closing condition, no root condition. C_w(ph) = closure of the bottom pattern (c = 0, d = overflow mask) under this step.
// Soundness (same induction as FILTER_R8 section 3): for a real edge I -> J the (c, d) content of J on slots s..s+w-1 is produced from
// the (c, d, r) content of I on those slots by the per-slot rule started at x_s; the abstract step allows every r, so it contains that
// successor. Hence every reachable interface has all its (c, d) windows in C_w. Wrapped windows: as in winbits.h (x_T = x_0, L | T).
#pragma once
#include "winbits.h"

namespace wcd {
typedef uint64_t u64; typedef unsigned __int128 u128;
static int CW = 0, CLEN = 1, CB = 10, CT = 0; static bool CWRAP = false; static u64 CTMASK = 0;
static std::vector<const u64*> bits;

static inline std::string fname(const std::string& dir, int B, const std::string& pat, int w, int ph) {
  return dir + "/wcd_B" + std::to_string(B) + "_" + pat + "_w" + std::to_string(w) + "_ph" + std::to_string(ph) + ".bits";
}
// Expansion by subset construction: carry the SET of running values (bitmask over 0..2B-2) that are possible after a given (c', d') prefix;
// a window (c', d') is produced iff its set is non-empty at the end. This equals running the rule from every x0 and every incoming digit.
struct SetExp {
  int w, B; int wovf[64]; u64 cc, cd; u64* S; std::atomic<u64>* added;
  void dfs(int t, uint32_t X, u64 cs, u64 ds) {
    if (!X) return;
    if (t == w) {
      u64 idx = cs | (ds << w); u64 bit = 1ULL << (idx & 63);
      u64 old = __atomic_fetch_or(&S[idx >> 6], bit, __ATOMIC_RELAXED);
      if (!(old & bit)) added->fetch_add(1, std::memory_order_relaxed);
      return;
    }
    int cin = (cc >> t) & 1, dneed = (cd >> t) & 1;
    // group the x in X by the outputs (d, co); collect the next running-value set for each group
    uint32_t nxt[2][2] = {{0, 0}, {0, 0}};
    for (int x = 0; x <= 2 * B - 2; x++) {
      if (!((X >> x) & 1)) continue;
      for (int d = 0; d < 2; d++) {
        if ((x + d) / B != dneed) continue;
        int e = (x + cin) % B, r = (x + d) % B, co = (x + cin) / B;
        if (wovf[t]) { for (int rin = 0; rin < B; rin++) nxt[d][co] |= 1u << (e + rin); }
        else nxt[d][co] |= 1u << (e + r);
      }
    }
    for (int d = 0; d < 2; d++) for (int co = 0; co < 2; co++)
      if (nxt[d][co]) dfs(t + 1, nxt[d][co], cs | ((u64)co << t), ds | ((u64)d << t));
  }
  void expand(u64 idx) { u64 m = (1ULL << w) - 1; cc = idx & m; cd = (idx >> w) & m; dfs(0, (1u << (2 * B - 1)) - 1, 0, 0); }
};
static u64 buildPhase(int B, const std::string& pat, int w, int ph, int nth, const std::string& out) {
  u64 nb = 1ULL << (2 * w), nw = (nb + 63) / 64;
  u64* S = (u64*)calloc(nw, 8); u64* D = (u64*)calloc(nw, 8);
  if (!S || !D) { fprintf(stderr, "alloc failed\n"); exit(3); }
  int wovf[64]; for (int t = 0; t < w; t++) wovf[t] = pat[(ph + t) % pat.size()] - '0';
  u64 bd = 0; for (int t = 0; t < w; t++) if (wovf[t]) bd |= 1ULL << t;
  u64 b0 = bd << w; S[b0 >> 6] |= 1ULL << (b0 & 63);
  std::atomic<u64> added{1}; int sweep = 0;
  while (true) {
    std::atomic<u64> next{0}, expanded{0}; const u64 CH = 1 << 12;
    auto work = [&]() {
      SetExp ex; ex.w = w; ex.B = B; ex.S = S; ex.added = &added; for (int t = 0; t < w; t++) ex.wovf[t] = wovf[t];
      u64 loc = 0;
      while (true) {
        u64 a = next.fetch_add(CH); if (a >= nw) break; u64 bnd = std::min(nw, a + CH);
        for (u64 i = a; i < bnd; i++) while (true) {
          u64 m = __atomic_load_n(&S[i], __ATOMIC_RELAXED) & ~D[i]; if (!m) break;
          int b = __builtin_ctzll(m); D[i] |= 1ULL << b; ex.expand(i * 64 + b); loc++;
        }
      }
      expanded.fetch_add(loc);
    };
    std::vector<std::thread> th; for (int i = 0; i < nth; i++) th.emplace_back(work); for (auto& x : th) x.join();
    sweep++;
    fprintf(stdout, "  buildcd w=%d ph=%d sweep %d: expanded %llu, reached %llu\n", w, ph, sweep, (unsigned long long)expanded.load(), (unsigned long long)added.load()); fflush(stdout);
    if (expanded.load() == 0) break;
  }
  u64 total = 0; for (u64 i = 0; i < nw; i++) total += __builtin_popcountll(S[i]);
  FILE* f = fopen((out + ".tmp").c_str(), "wb"); if (!f || fwrite(S, 8, nw, f) != nw) { fprintf(stderr, "write failed\n"); exit(3); }
  fclose(f); rename((out + ".tmp").c_str(), out.c_str()); free(S); free(D);
  return total;
}
static bool load(const std::string& dir, int B, const std::string& pat, int w, int T) {
  CB = B; CW = w; CLEN = pat.size(); CT = T; CTMASK = (T == 64) ? ~0ULL : ((1ULL << T) - 1);
  bits.assign(CLEN, nullptr);
  for (int ph = 0; ph < CLEN; ph++) {
    std::string fn = fname(dir, B, pat, w, ph); u64 nw = ((1ULL << (2 * w)) + 63) / 64;
    int fd = open(fn.c_str(), O_RDONLY); if (fd < 0) { fprintf(stderr, "missing %s\n", fn.c_str()); return false; }
    struct stat st; fstat(fd, &st); if ((u64)st.st_size != nw * 8) { fprintf(stderr, "bad size %s\n", fn.c_str()); return false; }
    void* p = mmap(nullptr, nw * 8, PROT_READ, MAP_SHARED, fd, 0); close(fd); if (p == MAP_FAILED) return false;
    bits[ph] = (const u64*)p;
  }
  const char* e = getenv("WRAP"); CWRAP = e && atoi(e);
  if (CWRAP && T % CLEN != 0) return false;
  return true;
}
static inline bool testw(int ph, u64 cw, u64 dw) { u64 idx = cw | (dw << CW); return (bits[ph][idx >> 6] >> (idx & 63)) & 1; }
static inline bool winAt(u64 c, u64 d, int s0) { u64 m = (1ULL << CW) - 1; return testw(s0 % CLEN, (c >> s0) & m, (d >> s0) & m); }
static inline bool winOK(u64 c, u64 d, int t1) { if (!CW || t1 < CW) return true; return winAt(c, d, t1 - CW); }
static inline bool winWrapAt(u64 c, u64 d, int s0) {
  u64 c2 = ((c >> s0) | (c << (CT - s0))) & CTMASK, d2 = ((d >> s0) | (d << (CT - s0))) & CTMASK, m = (1ULL << CW) - 1;
  return testw(s0 % CLEN, c2 & m, d2 & m);
}
static inline bool wrapOK(u64 c, u64 d) { if (!CW || !CWRAP) return true; for (int s0 = CT - CW + 1; s0 < CT; s0++) if (!winWrapAt(c, d, s0)) return false; return true; }
static inline bool allOK(u64 c, u64 d) { if (!CW) return true; for (int s0 = 0; s0 + CW <= CT; s0++) if (!winAt(c, d, s0)) return false; return wrapOK(c, d); }
}  // namespace wcd
