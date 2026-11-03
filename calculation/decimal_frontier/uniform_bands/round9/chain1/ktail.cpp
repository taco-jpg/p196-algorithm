// ktail.cpp -- round 9: the reach graph read column by column (time direction), from the 9-wire end outward.
// Rows: I_0 = the 9-wire target stream (c = e, d = 1 - e, r = (B-1) e at overflow slots), I_1, ..., I_K = interfaces moving outward;
// edge k (I_{k+1} -> I_k) has running value x_k in 0..2B-2 (same step relation as reach/backdisk). A K-tail node is (x_0..x_{K-1}, time phase
// mod lcm(|clock|, |e|)); the edge label is the outer interface I_K at that slot (c bit, and r digit at overflow slots). Given node and label
// the successor is unique: d propagates outward, c propagates inward, r follows from x and d (formulas below).
// A reach path bottom -> target of height h and period T  <=>  a closed walk of length T in the h-tail graph whose labels are the bottom
// interface (c = 0, r = 1 at overflows), with d_h = clock bit and x_{h-1} >= 1 (root rule).
// S_K = nodes of the K-tail graph (free labels) that lie on a bi-infinite walk (iterated trimming; contains every node on a cycle).
// The inner K digits of any closed walk of a wider tail are a closed walk of the K-tail graph, so S_{K} is contained in S_{K-1} x [0..2B-2].
// If S_K is empty, no reach path to this target exists at height >= K for ANY period T. Root cycles inside S_K give every height-K path.
// usage: THREADS=n ktail B CLOCK E Kmax [maxnodes]
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>
#include <algorithm>
#include <thread>
#include <atomic>
#include <chrono>
#include <numeric>
using namespace std;
typedef unsigned __int128 u128; typedef uint64_t u64;
static int B, P, Q, PER, NX; static string CLK, E;
static inline int dig(u128 k, int i) { return (int)((k >> (5 * i)) & 31); }
static inline int phs(u128 k) { return (int)(k >> 120); }
static inline u128 mk(const int* x, int K, int ph) { u128 k = 0; for (int i = 0; i < K; i++) k |= (u128)x[i] << (5 * i); return k | ((u128)ph << 120); }
// one time step of the K-tail; returns false if the labels are inconsistent. outd = d_K (the outer d bit)
static inline bool step(const int* x, int K, int ph, int cK, int rK, int* nx, int& outd) {
  int ov = CLK[ph % P] - '0', et = E[ph % Q] - '0';
  int d[40], c[40], r[40];
  d[0] = 1 - et; for (int k = 0; k < K; k++) d[k + 1] = (x[k] + d[k]) / B;
  if (ov && (x[0] + d[0]) % B != (B - 1) * et) return false;
  for (int k = 1; k < K; k++) r[k] = (x[k] + d[k]) % B; r[K] = rK;
  c[K] = cK; for (int k = K - 1; k >= 0; k--) c[k] = (x[k] + c[k + 1]) / B;
  if (c[0] != et) return false;
  for (int k = 0; k < K; k++) nx[k] = (x[k] + c[k + 1]) % B + (ov ? r[k + 1] : (x[k] + d[k]) % B);
  outd = d[K]; return true;
}
int main(int argc, char** argv) {
  if (argc < 5) { fprintf(stderr, "usage: ktail B CLOCK E Kmax [maxnodes]\n"); return 2; }
  B = atoi(argv[1]); CLK = argv[2]; E = argv[3]; int Kmax = atoi(argv[4]); u64 maxn = argc > 5 ? strtoull(argv[5], 0, 10) : 2000000000ULL;
  P = CLK.size(); Q = E.size(); PER = P; while (PER % Q) PER += P; NX = 2 * B - 1;
  int nth = getenv("THREADS") ? atoi(getenv("THREADS")) : 8;
  if (Kmax > 24) Kmax = 24;
  printf("ktail B=%d clock=%s e=%s phases=%d\n", B, CLK.c_str(), E.c_str(), PER); fflush(stdout);
  vector<u128> S;
  for (int K = 1; K <= Kmax; K++) {
    auto t0 = chrono::steady_clock::now();
    vector<u128> C;
    if (K == 1) { for (int a = 0; a < NX; a++) for (int ph = 0; ph < PER; ph++) { int x[1] = {a}; C.push_back(mk(x, 1, ph)); } }
    else { C.reserve(S.size() * NX); for (u128 k : S) { u128 base = k & ~((u128)63 << 120); int ph = phs(k); for (int a = 0; a < NX; a++) C.push_back(base | ((u128)a << (5 * (K - 1))) | ((u128)ph << 120)); } }
    if (C.size() > maxn) { printf("K=%d: %zu candidates > cap: STOP (UNDECIDED beyond K=%d)\n", K, C.size(), K - 1); return 3; }
    sort(C.begin(), C.end()); size_t N = C.size();
    // edges (CSR) inside C
    vector<vector<uint32_t>> outs(N); vector<atomic<uint32_t>> indeg(N);
    for (auto& a : indeg) a = 0;
    atomic<size_t> nb{0};
    auto work = [&]() {
      int x[40], nx[40]; vector<uint32_t> tmp;
      while (true) {
        size_t s = nb.fetch_add(4096); if (s >= N) break; size_t e2 = min(N, s + 4096);
        for (size_t i = s; i < e2; i++) {
          int ph = phs(C[i]); for (int k = 0; k < K; k++) x[k] = dig(C[i], k);
          int ov = CLK[ph % P] - '0'; tmp.clear();
          for (int cK = 0; cK < 2; cK++) for (int rK = 0; rK < (ov ? B : 1); rK++) {
            int od; if (!step(x, K, ph, cK, rK, nx, od)) continue;
            u128 nk = mk(nx, K, (ph + 1) % PER);
            auto it = lower_bound(C.begin(), C.end(), nk);
            if (it != C.end() && *it == nk) tmp.push_back((uint32_t)(it - C.begin()));
          }
          sort(tmp.begin(), tmp.end()); tmp.erase(unique(tmp.begin(), tmp.end()), tmp.end());
          outs[i] = tmp; for (uint32_t j : tmp) indeg[j]++;
        }
      }
    };
    { vector<thread> th; for (int i = 0; i < nth; i++) th.emplace_back(work); for (auto& t : th) t.join(); }
    // reverse edges
    vector<vector<uint32_t>> ins(N); for (size_t i = 0; i < N; i++) for (uint32_t j : outs[i]) ins[j].push_back((uint32_t)i);
    vector<uint32_t> outdeg(N); vector<char> dead(N, 0); vector<uint32_t> q;
    for (size_t i = 0; i < N; i++) { outdeg[i] = outs[i].size(); if (outdeg[i] == 0 || indeg[i] == 0) { dead[i] = 1; q.push_back(i); } }
    while (!q.empty()) {
      uint32_t v = q.back(); q.pop_back();
      for (uint32_t j : outs[v]) if (!dead[j] && --indeg[j] == 0) { dead[j] = 1; q.push_back(j); }
      for (uint32_t j : ins[v]) if (!dead[j] && --outdeg[j] == 0) { dead[j] = 1; q.push_back(j); }
    }
    vector<u128> S2; for (size_t i = 0; i < N; i++) if (!dead[i]) S2.push_back(C[i]);
    // root walks at height K: labels = bottom (c = 0, r = 1 at overflow), d_K = clock bit, x_{K-1} >= 1; functional graph inside S2
    vector<int64_t> nxt(S2.size(), -1);
    { int x[40], nx[40];
      for (size_t i = 0; i < S2.size(); i++) {
        int ph = phs(S2[i]); for (int k = 0; k < K; k++) x[k] = dig(S2[i], k);
        if (x[K - 1] < 1) continue; int ov = CLK[ph % P] - '0'; int od;
        if (!step(x, K, ph, 0, ov ? 1 : 0, nx, od)) continue; if (od != ov) continue;
        if (nx[K - 1] < 1) continue;
        u128 nk = mk(nx, K, (ph + 1) % PER); auto it = lower_bound(S2.begin(), S2.end(), nk);
        if (it != S2.end() && *it == nk) nxt[i] = it - S2.begin();
      } }
    vector<int> color(S2.size(), 0); vector<int> lens; vector<size_t> reps;
    for (size_t i = 0; i < S2.size(); i++) {
      if (color[i]) continue; vector<size_t> path; size_t u = i;
      while (true) { if (color[u] == 1) { // cycle found from u
          int L = 0; size_t v = u; do { L++; v = nxt[v]; } while (v != u); lens.push_back(L); reps.push_back(u); break; }
        if (color[u] == 2) break; color[u] = 1; path.push_back(u); if (nxt[u] < 0) break; u = nxt[u]; }
      for (size_t v : path) color[v] = 2;
    }
    double secs = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    printf("K=%d: candidates %zu, S_K %zu nodes, root cycles %zu", K, N, S2.size(), lens.size());
    for (size_t j = 0; j < lens.size() && j < 10; j++) printf(" len%d", lens[j]); printf(" (%.1f s)\n", secs); fflush(stdout);
    for (size_t j = 0; j < reps.size() && j < 4; j++) {   // print the column of one node per cycle for replay: x_0..x_{K-1} at each time of the cycle
      size_t v = reps[j]; printf("  ROOTCYCLE K=%d len=%d start_phase=%d columns:", K, lens[j], phs(S2[v]));
      do { printf(" ["); for (int k = 0; k < K; k++) printf("%d%s", dig(S2[v], k), k + 1 < K ? "," : "]"); v = nxt[v]; } while (v != reps[j]);
      printf("\n");
    }
    S.swap(S2);
    if (S.empty()) { printf("RESULT: S_%d is EMPTY: no reach path to this stream at height >= %d, for any period T\n", K, K); return 0; }
  }
  printf("RESULT: stopped at K=%d with S_K nonempty\n", Kmax); return 1;
}
