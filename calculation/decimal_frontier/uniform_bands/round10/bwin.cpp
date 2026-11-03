// bwin.cpp -- r9u experiment: backward window abstraction inside A_w. B_w(ph) = the window contents in A_w(ph) from which a TARGET window
// (a window of a 9-wire interface: d = complement of c, r = (B-1) at overflow slots with c = 1, 0 at c = 0; or a window of a uniform band)
// can be reached by abstract steps. Prints |A_w|, |B_w| per phase (measurement only).
// usage: bwin B CLOCK w DIR threads [ph...]   (writes DIR/bwin_..._ph<ph>.bits)
#include "winbits.h"
#include <set>
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
  B = atoi(argv[1]); PAT = argv[2]; W = atoi(argv[3]); string dir = argv[4]; int nth = atoi(argv[5]);
  int T = PAT.size(); while (T < 32) T += PAT.size();
  int nov = 0; for (int t = 0; t < T; t++) nov += PAT[t % PAT.size()] == '1';
  if (!wb::load(dir, B, PAT, W, T, nov)) return 2;
  vector<int> phs; for (int i = 6; i < argc; i++) phs.push_back(atoi(argv[i])); if (phs.empty()) for (int ph = 0; ph < (int)PAT.size(); ph++) phs.push_back(ph);
  for (int ph : phs) {
    { struct stat st; if (stat(wb::bname(dir, B, PAT, W, ph).c_str(), &st) == 0) { printf("ph %d exists, skipped\n", ph); continue; } }
    int k = wb::wk[ph]; u64 nb = wb::spaceBits(W, k), nw = (nb + 63) / 64; const u64* A = wb::bits[ph];
    u64* M = (u64*)calloc(nw, 8);
    int wovf[64], wOVI[64]; { int nv = 0; for (int t = 0; t < W; t++) { wovf[t] = PAT[(ph + t) % PAT.size()] - '0'; wOVI[t] = wovf[t] ? nv++ : -1; } }
    // target windows: 9-wire
    u64 nt = 0;
    for (u64 c = 0; c < (1ULL << W); c++) {
      u64 d = (~c) & ((1ULL << W) - 1), rv = 0;
      for (int t = 0; t < W; t++) if (wovf[t]) rv += (u64)((B - 1) * ((c >> t) & 1)) * wb::wpow[wOVI[t]];
      u64 idx = c | (d << W) | (rv << (2 * W)); if ((A[idx >> 6] >> (idx & 63)) & 1) { M[idx >> 6] |= 1ULL << (idx & 63); nt++; }
    }
    // band windows: uniform cycles v -> 2*((v+c) mod B), c = v >= B   (r10: NOBAND=1 skips them -> targets = 9-wire windows only)
    if (!(getenv("NOBAND") && atoi(getenv("NOBAND")))) { auto f = [&](int v) { int c = v >= B; return 2 * ((v + c) % B); };
      for (int v0 = 0; v0 <= 2 * B - 2; v0++) { int v = v0; for (int i = 0; i < 4 * B; i++) v = f(v);
        vector<int> cy; int u = v; do { cy.push_back(u); u = f(u); } while (u != v && (int)cy.size() <= 2 * B);
        if (u != v) continue; bool bad = false; for (int z : cy) if (z == B - 1) bad = true; if (bad) continue;
        for (int o = 0; o < (int)cy.size(); o++) { u64 c = 0, rv = 0; for (int t = 0; t < W; t++) { int z = cy[(t + o) % cy.size()], cv = z >= B; c |= (u64)cv << t; if (wovf[t]) rv += (u64)((z + cv) % B) * wb::wpow[wOVI[t]]; }
          u64 idx = c | (c << W) | (rv << (2 * W)); if ((A[idx >> 6] >> (idx & 63)) & 1) { if (!((M[idx >> 6] >> (idx & 63)) & 1)) nt++; M[idx >> 6] |= 1ULL << (idx & 63); } } } }
    u64 total = nt; int sweep = 0;
    while (true) {
      atomic<u64> next{0}, added{0}; const u64 CH = 1 << 12;
      auto work = [&]() { SuccExp ex; ex.w = W; ex.k = k; ex.M = M; for (int t = 0; t < W; t++) { ex.wovf[t] = wovf[t]; ex.wOVI[t] = wOVI[t]; } u64 loc = 0;
        while (true) { u64 a = next.fetch_add(CH); if (a >= nw) break; u64 bnd = min(nw, a + CH);
          for (u64 i = a; i < bnd; i++) { u64 m = A[i] & ~__atomic_load_n(&M[i], __ATOMIC_RELAXED); while (m) { int b = __builtin_ctzll(m); m &= m - 1;
            if (ex.any(i * 64 + b)) { __atomic_fetch_or(&M[i], 1ULL << b, __ATOMIC_RELAXED); loc++; } } } }
        added.fetch_add(loc); };
      vector<thread> th; for (int i = 0; i < nth; i++) th.emplace_back(work); for (auto& x : th) x.join();
      total += added; sweep++; printf("  ph %d sweep %d: +%llu\n", ph, sweep, (unsigned long long)added.load()); fflush(stdout); if (added == 0) break;
    }
    u64 na = 0; for (u64 i = 0; i < nw; i++) na += __builtin_popcountll(A[i]);
    printf("ph %d k=%d: |A|=%llu targets=%llu |B within A|=%llu (%.1f%%) sweeps %d\n", ph, k, (unsigned long long)na, (unsigned long long)nt, (unsigned long long)total, 100.0 * total / na, sweep); fflush(stdout);
    { string fn = wb::bname(dir, B, PAT, W, ph); FILE* f = fopen((fn + ".tmp").c_str(), "wb"); if (!f || fwrite(M, 8, nw, f) != nw) { fprintf(stderr, "write failed\n"); return 3; } fclose(f); rename((fn + ".tmp").c_str(), fn.c_str()); }
    free(M);
  }
}
