// kheadc.cpp -- r11f chain 8: C++ re-implementation (independent of khead_root.py) of root-restricted K-head lifting for a fixed
// overflow clock G. Vertex (phase mod |G|, x_0..x_{K-1}), x_0 in 1..2B-2, x_i in 0..2B-2. For h in {0,1}: H_K = h,
// H_i = (x_i + H_{i+1}) / B, g = H_0 must equal G[phase]; L_0 = 0, L_{i+1} = (x_i + L_i) / B;
// y_i = (x_i + L_i) % B + (g ? (i == 0 ? 1 : (x_{i-1} + H_i) % B) : (x_i + H_{i+1}) % B).
// S_K = union of the cyclic SCCs of the K-graph (vertices S_{K-1} x [0..2B-2]) that contain a ROOT vertex (phase ph0, prefix root).
// Closed edges (actual exterior of width <= K, 9-padded): h = 1 - L_K and, if g = 1, (x_{K-1} + h) % B == (B-1) * L_K.
// A cycle of closed edges through a root vertex inside S_K = a genuine periodic exterior of width <= K with that root (Agent120 model).
// usage: kheadc G Kmax root(e.g. 9,17,5) ph0 [B] [maxcand]
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <map>
using namespace std;
typedef uint64_t u64;
static int B = 10, P, NX, KW;  // KW = bytes per vertex (1 phase + K digits)
static string G;
static vector<int> rootv; static int ph0;
struct Cmp { const vector<uint8_t>* D; int w; bool operator()(u64 a, u64 b) const { return memcmp(&(*D)[a * w], &(*D)[b * w], w) < 0; } };
int main(int argc, char** argv) {
  if (argc < 5) { fprintf(stderr, "usage: kheadc G Kmax root ph0 [B] [maxcand]\n"); return 2; }
  G = argv[1]; P = G.size(); int Kmax = atoi(argv[2]);
  if (string(argv[3]) != "-") { string s = argv[3]; size_t p = 0; while (p < s.size()) { size_t q = s.find(',', p); if (q == string::npos) q = s.size(); rootv.push_back(atoi(s.substr(p, q - p).c_str())); p = q + 1; } }
  ph0 = atoi(argv[4]); if (argc > 5) B = atoi(argv[5]); u64 maxc = argc > 6 ? strtoull(argv[6], 0, 10) : 400000000ULL; NX = 2 * B - 1;
  vector<uint8_t> S; u64 nS = 0;   // vertices of width K-1, each (phase, x...)
  for (int K = 1; K <= Kmax; K++) {
    int w = K + 1;
    vector<uint8_t> C; u64 N;
    if (K == 1) { for (int ph = 0; ph < P; ph++) for (int a = 1; a < NX; a++) { C.push_back(ph); C.push_back(a); } N = C.size() / 2; }
    else {
      N = nS * NX; if (N > maxc) { printf("K=%d: %llu candidates > cap, STOP\n", K, (unsigned long long)N); return 3; }
      C.resize(N * w); u64 j = 0;
      for (u64 i = 0; i < nS; i++) for (int a = 0; a < NX; a++, j++) { memcpy(&C[j * w], &S[i * K], K); C[j * w + K] = a; }
    }
    // C is sorted lexicographically (S sorted, digits appended in order)
    auto find = [&](const uint8_t* key) -> int64_t {
      u64 lo = 0, hi = N; while (lo < hi) { u64 m = (lo + hi) / 2; int c = memcmp(&C[m * w], key, w); if (c < 0) lo = m + 1; else hi = m; }
      return (lo < N && memcmp(&C[lo * w], key, w) == 0) ? (int64_t)lo : -1;
    };
    vector<u64> off(N + 1, 0); vector<uint32_t> adj; vector<uint8_t> closedArc; adj.reserve(N * 2);
    for (u64 v = 0; v < N; v++) {
      const uint8_t* p = &C[v * w]; int ph = p[0]; const uint8_t* x = p + 1;
      int Hc[80], Lc[80]; uint8_t y[81]; int last = -1;
      Lc[0] = 0; for (int i = 0; i < K; i++) Lc[i + 1] = (x[i] + Lc[i]) / B;
      for (int h = 0; h < 2; h++) {
        Hc[K] = h; for (int i = K - 1; i >= 0; i--) Hc[i] = (x[i] + Hc[i + 1]) / B;
        int g = Hc[0]; if (g != G[ph] - '0') continue;
        y[0] = (ph + 1) % P;
        for (int i = 0; i < K; i++) y[i + 1] = (x[i] + Lc[i]) % B + (g ? (i == 0 ? 1 : (x[i - 1] + Hc[i]) % B) : (x[i] + Hc[i + 1]) % B);
        int64_t t = find(y); if (t < 0) continue;
        bool cl = (h == 1 - Lc[K]) && (!g || (x[K - 1] + h) % B == (B - 1) * Lc[K]);
        if (t == last) { if (cl) closedArc.back() = 1; continue; }
        adj.push_back((uint32_t)t); closedArc.push_back(cl); last = (int)t;
      }
      off[v + 1] = adj.size();
    }
    // iterative Tarjan
    vector<int64_t> idx(N, -1), low(N, 0), comp(N, -1); vector<uint32_t> st; vector<char> on(N, 0); int64_t cnt = 0, nc = 0;
    vector<pair<uint32_t, u64>> cs;
    for (u64 s = 0; s < N; s++) {
      if (idx[s] >= 0) continue;
      cs.push_back({(uint32_t)s, off[s]}); idx[s] = low[s] = cnt++; st.push_back(s); on[s] = 1;
      while (!cs.empty()) {
        uint32_t u = cs.back().first; u64& e = cs.back().second;
        if (e < off[u + 1]) { uint32_t t = adj[e++];
          if (idx[t] < 0) { idx[t] = low[t] = cnt++; st.push_back(t); on[t] = 1; cs.push_back({t, off[t]}); }
          else if (on[t]) low[u] = min(low[u], idx[t]);
        } else {
          cs.pop_back(); if (!cs.empty()) { uint32_t p = cs.back().first; low[p] = min(low[p], low[u]); }
          if (low[u] == idx[u]) { while (true) { uint32_t t = st.back(); st.pop_back(); on[t] = 0; comp[t] = nc; if (t == u) break; } nc++; }
        }
      }
    }
    // cyclic components containing a root vertex
    vector<u64> csize(nc, 0); vector<char> selfl(nc, 0), hasRoot(nc, 0);
    auto isRoot = [&](u64 v) { const uint8_t* p = &C[v * w]; if (p[0] != ph0) return false; int m = min((int)rootv.size(), K); for (int i = 0; i < m; i++) if (p[1 + i] != rootv[i]) return false; return true; };
    for (u64 v = 0; v < N; v++) { csize[comp[v]]++; if (isRoot(v)) hasRoot[comp[v]] = 1; for (u64 e = off[v]; e < off[v + 1]; e++) if (adj[e] == v) selfl[comp[v]] = 1; }
    vector<char> keep(nc, 0); u64 nk = 0, nroot = 0; map<u64, int> sizes;
    for (int64_t c = 0; c < nc; c++) if ((csize[c] > 1 || selfl[c]) && hasRoot[c]) { keep[c] = 1; sizes[csize[c]]++; }
    // closed-arc cycles through a root vertex inside kept components: SCC of the closed subgraph restricted to kept comps
    // (simple approach: iterate removal of vertices with no closed in/out arc inside kept set)
    vector<char> alive(N, 0); for (u64 v = 0; v < N; v++) if (keep[comp[v]]) { alive[v] = 1; nk++; if (isRoot(v)) nroot++; }
    vector<uint32_t> indeg(N, 0), outdeg(N, 0);
    for (u64 v = 0; v < N; v++) if (alive[v]) for (u64 e = off[v]; e < off[v + 1]; e++) if (closedArc[e] && alive[adj[e]] && comp[adj[e]] == comp[v]) { outdeg[v]++; indeg[adj[e]]++; }
    vector<char> calive = alive; vector<uint32_t> q; for (u64 v = 0; v < N; v++) if (calive[v] && (!indeg[v] || !outdeg[v])) { calive[v] = 0; q.push_back(v); }
    vector<vector<uint32_t>> rin(0);
    { // reverse closed adjacency
      vector<u64> roff(N + 1, 0); for (u64 v = 0; v < N; v++) if (alive[v]) for (u64 e = off[v]; e < off[v + 1]; e++) if (closedArc[e] && alive[adj[e]] && comp[adj[e]] == comp[v]) roff[adj[e] + 1]++;
      for (u64 v = 0; v < N; v++) roff[v + 1] += roff[v]; vector<uint32_t> radj(roff[N]); vector<u64> fill(roff.begin(), roff.end() - 1);
      for (u64 v = 0; v < N; v++) if (alive[v]) for (u64 e = off[v]; e < off[v + 1]; e++) if (closedArc[e] && alive[adj[e]] && comp[adj[e]] == comp[v]) radj[fill[adj[e]]++] = v;
      while (!q.empty()) { uint32_t v = q.back(); q.pop_back();
        for (u64 e = off[v]; e < off[v + 1]; e++) { uint32_t t = adj[e]; if (closedArc[e] && calive[t] && comp[t] == comp[v] && --indeg[t] == 0) { calive[t] = 0; q.push_back(t); } }
        for (u64 e = roff[v]; e < roff[v + 1]; e++) { uint32_t s = radj[e]; if (calive[s] && --outdeg[s] == 0) { calive[s] = 0; q.push_back(s); } } }
    }
    u64 ncl = 0, nclroot = 0; for (u64 v = 0; v < N; v++) if (calive[v]) { ncl++; if (isRoot(v)) nclroot++; }
    printf("K=%d: candidates %llu arcs %zu | core %llu (root vertices %llu) cyclic root SCCs:", K, (unsigned long long)N, adj.size(), (unsigned long long)nk, (unsigned long long)nroot);
    int shown = 0; for (auto it = sizes.rbegin(); it != sizes.rend() && shown < 6; ++it, ++shown) printf(" %llux%d", (unsigned long long)it->first, it->second);
    printf(" | closed-arc core %llu (root %llu)\n", (unsigned long long)ncl, (unsigned long long)nclroot); fflush(stdout);
    if (nclroot) { // print one closed cycle through a root vertex (follow closed arcs inside calive)
      u64 r = 0; for (u64 v = 0; v < N; v++) if (calive[v] && isRoot(v)) { r = v; break; }
      // BFS back to r over closed arcs
      vector<int64_t> par(N, -2); vector<uint32_t> qq{(uint32_t)r}; par[r] = -1; bool found = false; uint32_t lastv = 0;
      for (size_t i = 0; i < qq.size() && !found; i++) { uint32_t u = qq[i]; for (u64 e = off[u]; e < off[u + 1]; e++) { uint32_t t = adj[e]; if (!closedArc[e] || !calive[t] || comp[t] != comp[u]) continue; if (t == r) { found = true; lastv = u; break; } if (par[t] == -2) { par[t] = u; qq.push_back(t); } } }
      if (found) { vector<uint32_t> path; for (int64_t v = lastv; v != -1; v = par[v]) path.push_back(v); reverse(path.begin(), path.end());
        printf("  CLOSEDCYCLE K=%d len=%zu:", K, path.size()); for (uint32_t v : path) { printf(" %d:[", C[v * w]); for (int i = 0; i < K; i++) printf("%d%s", C[v * w + 1 + i], i + 1 < K ? "," : "]"); } printf("\n"); fflush(stdout); }
    }
    S.clear(); nS = 0; for (u64 v = 0; v < N; v++) if (alive[v]) { S.insert(S.end(), &C[v * w], &C[v * w] + w); nS++; }
    if (!nS) { printf("RESULT: core EMPTY at K=%d: no periodic exterior (any period, any width) with phase-%d prefix", K, ph0); for (int a : rootv) printf(" %d", a); printf("\n"); return 0; }
    if (K == Kmax) { // per-phase value sets of coordinates 0..min(K,6)-1
      for (int i = 0; i < min(K, 6); i++) { printf("  coord %d values per phase:", i); for (int ph = 0; ph < P; ph++) { vector<int> vs(NX, 0); for (u64 v = 0; v < nS; v++) if (S[v * w] == ph) vs[S[v * w + 1 + i]] = 1; printf(" {"); bool f = true; for (int a = 0; a < NX; a++) if (vs[a]) { printf(f ? "%d" : ",%d", a); f = false; } printf("}"); } printf("\n"); }
    }
  }
  printf("RESULT: stopped at K=%d, core nonempty\n", Kmax); return 1;
}
