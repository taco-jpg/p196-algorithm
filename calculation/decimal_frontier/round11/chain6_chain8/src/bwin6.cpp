// bwin6.cpp -- r11f: co-reachability window family BB_w(ph) inside A_w(ph) (as round 9u bwin.cpp) but with TARGET windows read from a
// file (lines "ph idx", from wtargets.py: every cyclic window of the target interfaces). Abstract step, A_w and the fixpoint are
// exactly those of bwin.cpp. Reports, per phase, how many target windows lie in A_w, |BB_w|, and whether the bottom window
// (c = 0, d = overflow mask, r = 1 at overflow slots) lies in BB_w.  If the bottom window of some phase is outside BB_w, no target is
// reachable from the bottom at ANY period T (the abstraction does not depend on T).
// usage: bwin6 B CLOCK w ADIR TARGETS OUTPREFIX threads
#include "winbits.h"
using namespace std;
typedef uint64_t u64;
static int B, W; static string PAT;
struct SuccExp {
  int w, k; int wovf[64], wOVI[64]; u64 cc, cd; int cdig[16]; u64 cs, ds, rsv; const u64* M; bool hit;
  void dfs(int t, int x) {
    if (hit) return;
    if (t == w) { u64 idx = cs | (ds << w) | (rsv << (2 * w)); if ((__atomic_load_n(&M[idx >> 6], __ATOMIC_RELAXED) >> (idx & 63)) & 1) hit = true; return; }
    int cin = (cc >> t) & 1, dneed = (cd >> t) & 1;
    for (int d = 0; d < 2; d++) {
      if ((x + d) / B != dneed) continue;
      int e = (x + cin) % B, r = (x + d) % B, co = (x + cin) / B;
      int nx = wovf[t] ? e + cdig[wOVI[t]] : e + r;
      u64 sc = cs, sd = ds, sr = rsv;
      cs |= (u64)co << t; ds |= (u64)d << t; if (wovf[t]) rsv += (u64)r * wb::wpow[wOVI[t]];
      dfs(t + 1, nx); cs = sc; ds = sd; rsv = sr;
    }
  }
  bool any(u64 idx) {
    u64 m = (1ULL << w) - 1; cc = idx & m; cd = (idx >> w) & m; u64 rv = idx >> (2 * w);
    for (int j = 0; j < k; j++) { cdig[j] = rv % B; rv /= B; }
    hit = false; for (int x0 = 0; x0 <= 2 * B - 2 && !hit; x0++) { cs = ds = 0; rsv = 0; dfs(0, x0); }
    return hit;
  }
};
int main(int argc, char** argv) {
  if (argc < 8) { fprintf(stderr, "usage: bwin6 B CLOCK w ADIR TARGETS OUTPREFIX threads\n"); return 2; }
  B = atoi(argv[1]); PAT = argv[2]; W = atoi(argv[3]); string dir = argv[4]; string tfile = argv[5]; string outp = argv[6]; int nth = atoi(argv[7]);
  int T = PAT.size(); while (T < 32) T += PAT.size();
  int nov = 0; for (int t = 0; t < T; t++) nov += PAT[t % PAT.size()] == '1';
  if (!wb::load(dir, B, PAT, W, T, nov)) return 2;
  vector<vector<u64>> tg(PAT.size());
  { FILE* f = fopen(tfile.c_str(), "r"); if (!f) { perror("targets"); return 2; } int ph; unsigned long long idx;
    while (fscanf(f, "%d %llu", &ph, &idx) == 2) tg[ph].push_back(idx); fclose(f); }
  bool allBottom = true;
  for (int ph = 0; ph < (int)PAT.size(); ph++) {
    int k = wb::wk[ph]; u64 nb = wb::spaceBits(W, k), nw = (nb + 63) / 64; const u64* A = wb::bits[ph];
    u64* M = (u64*)calloc(nw, 8);
    int wovf[64], wOVI[64]; { int nv = 0; for (int t = 0; t < W; t++) { wovf[t] = PAT[(ph + t) % PAT.size()] - '0'; wOVI[t] = wovf[t] ? nv++ : -1; } }
    u64 bd = 0, br = 0; for (int t = 0; t < W; t++) if (wovf[t]) { bd |= 1ULL << t; br += wb::wpow[wOVI[t]]; }
    u64 b0 = (bd << W) | (br << (2 * W));
    u64 nt = 0, nin = 0;
    for (u64 idx : tg[ph]) { nt++; if (idx >= nb) { fprintf(stderr, "target index out of range\n"); return 3; }
      if ((A[idx >> 6] >> (idx & 63)) & 1) { if (!((M[idx >> 6] >> (idx & 63)) & 1)) nin++; M[idx >> 6] |= 1ULL << (idx & 63); } }
    u64 total = nin; int sweep = 0;
    while (true) {
      atomic<u64> next{0}, added{0}; const u64 CH = 1 << 12;
      auto work = [&]() { SuccExp ex; ex.w = W; ex.k = k; ex.M = M; for (int t = 0; t < W; t++) { ex.wovf[t] = wovf[t]; ex.wOVI[t] = wOVI[t]; } u64 loc = 0;
        while (true) { u64 a = next.fetch_add(CH); if (a >= nw) break; u64 bnd = min(nw, a + CH);
          for (u64 i = a; i < bnd; i++) { u64 m = A[i] & ~__atomic_load_n(&M[i], __ATOMIC_RELAXED); while (m) { int b = __builtin_ctzll(m); m &= m - 1;
            if (ex.any(i * 64 + b)) { __atomic_fetch_or(&M[i], 1ULL << b, __ATOMIC_RELAXED); loc++; } } } }
        added.fetch_add(loc); };
      vector<thread> th; for (int i = 0; i < nth; i++) th.emplace_back(work); for (auto& x : th) x.join();
      total += added; sweep++; if (added == 0) break;
    }
    u64 na = 0; for (u64 i = 0; i < nw; i++) na += __builtin_popcountll(A[i]);
    bool binA = (A[b0 >> 6] >> (b0 & 63)) & 1, binB = (M[b0 >> 6] >> (b0 & 63)) & 1;
    if (!binB) allBottom = false;
    printf("ph %d k=%d: |A|=%llu target windows=%llu (in A: %llu) |BB|=%llu (%.3f%% of A) sweeps %d bottom_in_A=%d bottom_in_BB=%d\n", ph, k,
           (unsigned long long)na, (unsigned long long)nt, (unsigned long long)nin, (unsigned long long)total, 100.0 * total / na, sweep, binA, binB); fflush(stdout);
    { string fn = outp + "_ph" + to_string(ph) + ".bits"; FILE* f = fopen((fn + ".tmp").c_str(), "wb"); if (!f || fwrite(M, 8, nw, f) != nw) { fprintf(stderr, "write failed\n"); return 3; } fclose(f); rename((fn + ".tmp").c_str(), fn.c_str()); }
    free(M);
  }
  printf("RESULT %s\n", allBottom ? "BOTTOM_IN_BB (no exclusion)" : "BOTTOM_NOT_IN_BB (no target reachable at any T)");
  return 0;
}
