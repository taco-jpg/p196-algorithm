// winbits.cpp -- round 9: the window abstraction of window.cpp / backdisk (WIN=w), built as an exact bitset per clock phase so that
// larger w (12) fits in memory. Same abstract step, same bottom pattern, same closure (BFS until no new state); only the storage differs.
// Window state index: c (w bits) + d (w bits) << w + rnum << 2w, rnum = sum_j r_j 10^j over the overflow slots of the window (r_j in 0..B-1).
// Output: OUTPREFIX_ph<k>.bin = header (magic, B, w, nv, clock) + bitset of 4^w * B^nv bits.
// usage: THREADS=n winbits B CLOCK w OUTPREFIX [PH]
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>
#include <thread>
#include <atomic>
#include <chrono>
using namespace std;
typedef uint64_t u64;
static int B, W, NV; static string PAT; static int ovf[64], OVI[64];
static u64 POWB[8];
static inline u64 enc(u64 c, u64 d, const int* r) { u64 rn = 0; for (int j = NV - 1; j >= 0; j--) rn = rn * B + r[j]; return c | (d << W) | (rn << (2 * W)); }
static inline void dec(u64 k, u64& c, u64& d, int* r) { u64 m = (1ULL << W) - 1; c = k & m; d = (k >> W) & m; u64 rn = k >> (2 * W); for (int j = 0; j < NV; j++) { r[j] = rn % B; rn /= B; } }
static inline bool testb(const u64* v, u64 i) { return (v[i >> 6] >> (i & 63)) & 1; }
static inline bool setb_atomic(u64* v, u64 i) { u64 m = 1ULL << (i & 63); u64 old = __atomic_fetch_or(&v[i >> 6], m, __ATOMIC_RELAXED); return !(old & m); }
struct Exp {
  u64 cc, cd; int cr[8]; u64 cs, ds; int rs[8];
  u64* V; u64* N; u64 news = 0;
  void dfs(int t, int x) {
    if (t == W) { u64 k = enc(cs, ds, rs); if (!testb(V, k) && setb_atomic(V, k)) { setb_atomic(N, k); news++; } return; }
    int cin = (cc >> t) & 1, dneed = (cd >> t) & 1;
    for (int d = 0; d < 2; d++) {
      if ((x + d) / B != dneed) continue;
      int e = (x + cin) % B, r = (x + d) % B, co = (x + cin) / B;
      int nx = ovf[t] ? e + cr[OVI[t]] : e + r;
      u64 sc = cs, sd = ds;
      cs |= (u64)co << t; ds |= (u64)d << t; if (ovf[t]) rs[OVI[t]] = r;
      dfs(t + 1, nx);
      cs = sc; ds = sd;
    }
  }
  void expand(u64 k) { dec(k, cc, cd, cr); for (int x0 = 0; x0 <= 2 * B - 2; x0++) { cs = ds = 0; dfs(0, x0); } }
};
int main(int argc, char** argv) {
  if (argc < 5) { fprintf(stderr, "usage: winbits B CLOCK w OUTPREFIX [PH]\n"); return 2; }
  B = atoi(argv[1]); PAT = argv[2]; W = atoi(argv[3]); string out = argv[4];
  int nth = getenv("THREADS") ? atoi(getenv("THREADS")) : 8;
  int ph0 = 0, ph1 = PAT.size(); if (argc > 5) { ph0 = atoi(argv[5]); ph1 = ph0 + 1; }
  for (int ph = ph0; ph < ph1; ph++) {
    auto t0 = chrono::steady_clock::now();
    NV = 0; for (int t = 0; t < W; t++) { ovf[t] = PAT[(ph + t) % PAT.size()] - '0'; OVI[t] = -1; if (ovf[t]) OVI[t] = NV++; }
    if (NV > 7 || 2 * W > 40) { fprintf(stderr, "too large\n"); return 2; }
    u64 U = (1ULL << (2 * W)); for (int j = 0; j < NV; j++) U *= B; u64 NW = (U + 63) / 64;
    vector<u64> V(NW, 0), F(NW, 0), N(NW, 0);
    u64 bd = 0; int br[8]; for (int t = 0; t < W; t++) if (ovf[t]) { bd |= 1ULL << t; br[OVI[t]] = 1; }
    u64 b0 = enc(0, bd, br); V[b0 >> 6] |= 1ULL << (b0 & 63); F[b0 >> 6] |= 1ULL << (b0 & 63);
    u64 total = 1; int level = 0;
    while (true) {
      atomic<u64> chunk{0}; atomic<u64> nnew{0}; const u64 CH = 1 << 16;
      auto work = [&]() {
        Exp ex; ex.V = V.data(); ex.N = N.data();
        while (true) {
          u64 s = chunk.fetch_add(CH); if (s >= NW) break; u64 e = min(NW, s + CH);
          for (u64 i = s; i < e; i++) { u64 w = F[i]; while (w) { int b = __builtin_ctzll(w); w &= w - 1; ex.expand(i * 64 + b); } }
        }
        nnew += ex.news;
      };
      vector<thread> th; for (int i = 0; i < nth; i++) th.emplace_back(work); for (auto& x : th) x.join();
      level++; total += nnew;
      if (nnew == 0) break;
      F.swap(N); memset(N.data(), 0, NW * 8);
      if (level % 10 == 0) { printf("  ph %d level %d: total %llu\n", ph, level, (unsigned long long)total); fflush(stdout); }
    }
    u64 cnt = 0; for (u64 x : V) cnt += __builtin_popcountll(x);
    double secs = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    printf("WINBITS B=%d clock=%s w=%d phase %d: %llu abstract states (levels %d, universe %llu, %.1f s)\n", B, PAT.c_str(), W, ph, (unsigned long long)cnt, level, (unsigned long long)U, secs); fflush(stdout);
    string fn = out + "_ph" + to_string(ph) + ".bin"; FILE* f = fopen(fn.c_str(), "wb");
    char hdr[64]; memset(hdr, 0, 64); snprintf(hdr, 64, "WINBITS1 %d %d %d %s", B, W, NV, PAT.c_str());
    fwrite(hdr, 1, 64, f); fwrite(V.data(), 8, NW, f); fclose(f);
  }
  return 0;
}
