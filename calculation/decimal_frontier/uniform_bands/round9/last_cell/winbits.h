// winbits.h -- round 9u: the window abstraction of FILTER_R8.md stored as bitsets (one file per clock phase), so that w = 10 fits in
// memory for clocks with up to 5 overflow slots per window. The abstraction is EXACTLY the one of backdisk.cpp's buildWindowSet:
// A_w(ph) = closure of the bottom pattern (c = 0, d = overflow mask, r = 1 at the overflow slots) under the per-slot rule run from ANY
// start value x in 0..2B-2, no closing condition, no root condition. Only the storage changes (hash set -> bitset).
// Index of a window content: c (w bits) | d (w bits) << w | (sum_j r_j B^j) << 2w, r_j = digit at the j-th overflow slot of the window.
//
// New in r9u: WRAP=1 also tests the windows that wrap around t = T-1 -> 0 (start slots T-w+1 .. T-1). Soundness: an edge has x_T = x_0,
// so slot 0 receives exactly the running value that slot T-1 produced; a wrapped window is therefore also one application of the
// per-slot rule from the start value x_s, and its clock phases are (s + j) mod L because L divides T. The induction of FILTER_R8 section 3
// goes through unchanged (see FINAL_R9U.md). Requires T % L == 0.
#pragma once
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>
#include <atomic>
#include <thread>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

namespace wb {
typedef uint64_t u64; typedef unsigned __int128 u128;
static int WW = 0, WLEN = 1, WBASE = 10, WT = 0, WNOV = 0; static bool WRAP = false; static u64 WTMASK = 0;
static int wk[64];        // overflow slots in the window of phase ph
static int wpre[256];     // overflow slots before slot t of the T-periodic clock (pattern repeated)
static u64 wpow[40];
static std::vector<const u64*> bits; static std::vector<u64> nbitsv;
static std::string pat_;

static inline std::string fname(const std::string& dir, int B, const std::string& pat, int w, int ph) {
  return dir + "/win_B" + std::to_string(B) + "_" + pat + "_w" + std::to_string(w) + "_ph" + std::to_string(ph) + ".bits";
}
static inline u64 spaceBits(int w, int k) { u64 n = 1ULL << (2 * w); for (int i = 0; i < k; i++) n *= (u64)WBASE; return n; }

static void initGeom(int B, const std::string& pat, int w) {
  WBASE = B; WW = w; WLEN = pat.size(); pat_ = pat;
  wpow[0] = 1; for (int i = 1; i < 40; i++) wpow[i] = wpow[i - 1] * (u64)B;
  { int c = 0; for (int t = 0; t < 256; t++) { wpre[t] = c; if (pat[t % pat.size()] == '1') c++; } }
  for (int ph = 0; ph < WLEN; ph++) { int k = 0; for (int t = 0; t < w; t++) if (pat[(ph + t) % pat.size()] == '1') k++; wk[ph] = k; }
}

// ---- builder (chaotic parallel closure on two bitsets: S = reached, D = expanded)
struct BuildExp {
  int w, B, k; int wovf[64], wOVI[64];
  u64 cc, cd; int cdig[16]; u64 cs, ds; u64 rsv;   // rsv = sum r'_j B^j built so far
  u64* S; std::atomic<u64>* added;
  void dfs(int t, int x) {
    if (t == w) {
      u64 idx = cs | (ds << w) | (rsv << (2 * w));
      u64 bit = 1ULL << (idx & 63);
      u64 old = __atomic_fetch_or(&S[idx >> 6], bit, __ATOMIC_RELAXED);
      if (!(old & bit)) added->fetch_add(1, std::memory_order_relaxed);
      return;
    }
    int cin = (cc >> t) & 1, dneed = (cd >> t) & 1;
    for (int d = 0; d < 2; d++) {
      if ((x + d) / B != dneed) continue;
      int e = (x + cin) % B, r = (x + d) % B, co = (x + cin) / B;
      int nx = wovf[t] ? e + cdig[wOVI[t]] : e + r;
      u64 sc = cs, sd = ds, sr = rsv;
      cs |= (u64)co << t; ds |= (u64)d << t; if (wovf[t]) rsv += (u64)r * wpow[wOVI[t]];
      dfs(t + 1, nx);
      cs = sc; ds = sd; rsv = sr;
    }
  }
  void expand(u64 idx) {
    u64 m = (1ULL << w) - 1; cc = idx & m; cd = (idx >> w) & m; u64 rv = idx >> (2 * w);
    for (int j = 0; j < k; j++) { cdig[j] = (int)(rv % (u64)B); rv /= (u64)B; }
    for (int x0 = 0; x0 <= 2 * B - 2; x0++) { cs = ds = 0; rsv = 0; dfs(0, x0); }
  }
};
// returns the number of abstract states; writes the bitset to `out`
static u64 buildPhase(int B, const std::string& pat, int w, int ph, int nth, const std::string& out) {
  initGeom(B, pat, w);
  int k = wk[ph]; u64 nb = spaceBits(w, k), nw = (nb + 63) / 64;
  u64* S = (u64*)calloc(nw, 8); u64* D = (u64*)calloc(nw, 8);
  if (!S || !D) { fprintf(stderr, "alloc failed (%llu words)\n", (unsigned long long)nw); exit(3); }
  int wovf[64], wOVI[64]; { int nv = 0; for (int t = 0; t < w; t++) { wovf[t] = pat[(ph + t) % pat.size()] - '0'; wOVI[t] = wovf[t] ? nv++ : -1; } }
  u64 bd = 0, br = 0; for (int t = 0; t < w; t++) if (wovf[t]) { bd |= 1ULL << t; br += wpow[wOVI[t]]; }
  u64 b0 = 0 | (bd << w) | (br << (2 * w)); S[b0 >> 6] |= 1ULL << (b0 & 63);
  std::atomic<u64> added{1}; u64 total = 1; int sweep = 0;
  while (true) {
    std::atomic<u64> next{0}, expanded{0}; const u64 CH = 1 << 14;
    auto work = [&]() {
      BuildExp ex; ex.w = w; ex.B = B; ex.k = k; ex.S = S; ex.added = &added; for (int t = 0; t < w; t++) { ex.wovf[t] = wovf[t]; ex.wOVI[t] = wOVI[t]; }
      u64 loc = 0;
      while (true) {
        u64 a = next.fetch_add(CH); if (a >= nw) break; u64 bnd = std::min(nw, a + CH);
        for (u64 i = a; i < bnd; i++) {
          while (true) {
            u64 m = __atomic_load_n(&S[i], __ATOMIC_RELAXED) & ~D[i]; if (!m) break;
            int b = __builtin_ctzll(m); D[i] |= 1ULL << b; ex.expand(i * 64 + b); loc++;
          }
        }
      }
      expanded.fetch_add(loc);
    };
    std::vector<std::thread> th; for (int i = 0; i < nth; i++) th.emplace_back(work); for (auto& x : th) x.join();
    sweep++;
    fprintf(stdout, "  build w=%d ph=%d sweep %d: expanded %llu, reached %llu\n", w, ph, sweep, (unsigned long long)expanded.load(), (unsigned long long)added.load()); fflush(stdout);
    if (expanded.load() == 0) break;
  }
  total = 0; for (u64 i = 0; i < nw; i++) total += __builtin_popcountll(S[i]);
  FILE* f = fopen((out + ".tmp").c_str(), "wb"); if (!f || fwrite(S, 8, nw, f) != nw) { fprintf(stderr, "write failed %s\n", out.c_str()); exit(3); }
  fclose(f); rename((out + ".tmp").c_str(), out.c_str());
  free(S); free(D);
  return total;
}

// ---- consumer side
static bool load(const std::string& dir, int B, const std::string& pat, int w, int T, int nov) {
  initGeom(B, pat, w); WT = T; WNOV = nov; WTMASK = (T == 64) ? ~0ULL : ((1ULL << T) - 1);
  bits.assign(WLEN, nullptr); nbitsv.assign(WLEN, 0);
  for (int ph = 0; ph < WLEN; ph++) {
    std::string fn = fname(dir, B, pat, w, ph); u64 nb = spaceBits(w, wk[ph]), nw = (nb + 63) / 64;
    int fd = open(fn.c_str(), O_RDONLY); if (fd < 0) { fprintf(stderr, "missing window file %s\n", fn.c_str()); return false; }
    struct stat st; fstat(fd, &st); if ((u64)st.st_size != nw * 8) { fprintf(stderr, "bad size %s\n", fn.c_str()); return false; }
    void* p = mmap(nullptr, nw * 8, PROT_READ, MAP_SHARED, fd, 0); close(fd);
    if (p == MAP_FAILED) { fprintf(stderr, "mmap failed %s\n", fn.c_str()); return false; }
    bits[ph] = (const u64*)p; nbitsv[ph] = nb;
  }
  const char* e = getenv("WRAP"); WRAP = e && atoi(e);
  if (WRAP && T % WLEN != 0) { fprintf(stderr, "WRAP needs T %% clock length == 0\n"); return false; }
  return true;
}
static inline bool testIn(const std::vector<const u64*>& bs, int ph, u64 cw, u64 dw, u128 r, int j0) {
  int k = wk[ph]; u64 rv = 0;
  for (int j = k - 1; j >= 0; j--) { int dg = (int)((r >> (4 * (j0 + j))) & 15); if (dg >= WBASE) return false; rv = rv * (u64)WBASE + (u64)dg; }
  u64 idx = cw | (dw << WW) | (rv << (2 * WW));
  return (bs[ph][idx >> 6] >> (idx & 63)) & 1;
}
static inline bool test(int ph, u64 cw, u64 dw, u128 r, int j0) { return testIn(bits, ph, cw, dw, r, j0); }
// non-wrapping window starting at slot s0 (s0 + w <= T)
static inline bool winAt(u64 c, u64 d, u128 r, int s0) {
  u64 m = (1ULL << WW) - 1;
  return test(s0 % WLEN, (c >> s0) & m, (d >> s0) & m, r, wpre[s0]);
}
// the window that ends just before slot t1 (backdisk / reachdisk convention)
static inline bool winOK(u64 c, u64 d, u128 r, int t1) { if (!WW || t1 < WW) return true; return winAt(c, d, r, t1 - WW); }
// wrapped window starting at slot s0 (T - w < s0 < T): rotate so that s0 becomes slot 0
static inline bool winWrapAt(u64 c, u64 d, u128 r, int s0) {
  u64 c2 = ((c >> s0) | (c << (WT - s0))) & WTMASK, d2 = ((d >> s0) | (d << (WT - s0))) & WTMASK;
  int q = WNOV ? wpre[s0] % WNOV : 0; int rb = 4 * WNOV; u128 rmask = (rb >= 128) ? ~(u128)0 : (((u128)1 << rb) - 1);
  u128 r2 = q ? (((r >> (4 * q)) | (r << (rb - 4 * q))) & rmask) : r;
  u64 m = (1ULL << WW) - 1;
  return test(s0 % WLEN, c2 & m, d2 & m, r2, 0);
}
static inline bool wrapOK(u64 c, u64 d, u128 r) {
  if (!WW || !WRAP) return true;
  for (int s0 = WT - WW + 1; s0 < WT; s0++) if (!winWrapAt(c, d, r, s0)) return false;
  return true;
}
static inline bool allOK(u64 c, u64 d, u128 r) {
  if (!WW) return true;
  for (int s0 = 0; s0 + WW <= WT; s0++) if (!winAt(c, d, r, s0)) return false;
  return wrapOK(c, d, r);
}
}  // namespace wb

// ---- r9u: the backward (co-reachability) window family BB_w(ph) within A_w(ph), built by bwin.cpp. A window content is in BB_w(ph) iff it
// lies in A_w(ph) and some chain of abstract steps inside A_w(ph) leads from it to a TARGET window (a window of a 9-wire interface or of a
// uniform band). Every interface on a path bottom -> target has all its windows (wrapped ones included) in BB_w (FINAL_R9U.md section 2),
// so a forward search may drop every successor with a window outside BB_w without losing any bottom -> target path.
namespace wb {
static std::vector<const u64*> bbits;
static inline std::string bname(const std::string& dir, int B, const std::string& pat, int w, int ph) {
  return dir + "/bwin_B" + std::to_string(B) + "_" + pat + "_w" + std::to_string(w) + "_ph" + std::to_string(ph) + ".bits";
}
static bool loadB(const std::string& dir) {   // call after load(); same geometry
  bbits.assign(WLEN, nullptr);
  for (int ph = 0; ph < WLEN; ph++) {
    std::string fn = bname(dir, WBASE, pat_, WW, ph); u64 nw = (spaceBits(WW, wk[ph]) + 63) / 64;
    int fd = open(fn.c_str(), O_RDONLY); if (fd < 0) { fprintf(stderr, "missing %s\n", fn.c_str()); return false; }
    struct stat st; fstat(fd, &st); if ((u64)st.st_size != nw * 8) { fprintf(stderr, "bad size %s\n", fn.c_str()); return false; }
    void* p = mmap(nullptr, nw * 8, PROT_READ, MAP_SHARED, fd, 0); close(fd); if (p == MAP_FAILED) return false;
    bbits[ph] = (const u64*)p;
  }
  return true;
}
// all windows (non-wrapping and wrapping) of a T-periodic interface in BB_w
static inline bool allInB(u64 c, u64 d, u128 r) {
  u64 m = (1ULL << WW) - 1;
  for (int s0 = 0; s0 + WW <= WT; s0++) if (!testIn(bbits, s0 % WLEN, (c >> s0) & m, (d >> s0) & m, r, wpre[s0])) return false;
  int rb = 4 * WNOV; u128 rmask = (rb >= 128) ? ~(u128)0 : (((u128)1 << rb) - 1);
  for (int s0 = WT - WW + 1; s0 < WT; s0++) {
    u64 c2 = ((c >> s0) | (c << (WT - s0))) & WTMASK, d2 = ((d >> s0) | (d << (WT - s0))) & WTMASK;
    int q = WNOV ? wpre[s0] % WNOV : 0; u128 r2 = q ? (((r >> (4 * q)) | (r << (rb - 4 * q))) & rmask) : r;
    if (!testIn(bbits, s0 % WLEN, c2 & m, d2 & m, r2, 0)) return false;
  }
  return true;
}
}  // namespace wb
