// kh2.cpp (r12b): INDEPENDENT re-implementation of the K-head closed-walk filter, for validating khx.
// Differences from khx (on purpose): nodes are explicit windows (string keys in a hash map), every edge is computed by a
// direct full-window trans() (no projection/incremental formula), SCCs by Kosaraju (khx: Tarjan), and the "exact" mode keeps
// EXACTLY the nodes lying on a closed walk of length L (lap-graph method from phase 0), not a superset.
//   mode -scc   : kept_K = union of cyclic SCCs of the level graph with period | L   (must equal khx -noexact, level by level)
//   mode -exact : kept_K = nodes on a closed walk of length L                       (must die no later than khx default)
// Level K+1 = all one-digit extensions (x, v), v in 0..2b-2, of kept_K; an edge exists iff trans() label = pat[t] and the target
// window is itself a node of level K+1 (i.e. its projection is in kept_K).  Lemma A3 makes this a superset of closed walks.
// usage: kh2 b WORD L (-scc|-exact) KMAX NODECAP      output: per level "K n kept", then "KH2 ... DIES K=k" or "SURVIVES K=k"
// r12e kh2s: optional 7th argument SEEDFILE = khxt dump ("idx t o0 o1 : x_0 .. x_{K0-1}" lines; edges ignored): the run starts at
// level K0 with exactly these windows as the level-K0 node set (instead of level 1), and continues with the unchanged kh2 rules.
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <cstring>
using namespace std;
int b, P, L, KMAX; long long NODECAP; vector<int> pat; bool EXACT;
static void trans(const string& x, int h, string& y, int& g) {
  int K = x.size(); vector<int> H(K + 1), Lc(K + 1, 0); H[K] = h;
  for (int i = K - 1; i >= 0; i--) H[i] = ((unsigned char)x[i] + H[i + 1]) / b;
  g = H[0];
  for (int i = 0; i < K; i++) Lc[i + 1] = ((unsigned char)x[i] + Lc[i]) / b;
  y.assign(K, 0);
  for (int i = 0; i < K; i++) { int xi = (unsigned char)x[i];
    int part = g ? (i == 0 ? 1 : ((unsigned char)x[i - 1] + H[i]) % b) : (xi + H[i + 1]) % b;
    y[i] = (char)((xi + Lc[i]) % b + part); }
}
static long long gcdl(long long a, long long c) { if (a < 0) a = -a; if (c < 0) c = -c; while (c) { long long r = a % c; a = c; c = r; } return a; }
int main(int argc, char** argv) {
  b = atoi(argv[1]); string w = argv[2]; P = w.size(); L = atoi(argv[3]); EXACT = string(argv[4]) == "-exact";
  KMAX = atoi(argv[5]); NODECAP = atoll(argv[6]);
  for (char c : w) pat.push_back(c - '0');
  if (L % P) { printf("bad L\n"); return 1; }
  int m = L / P;
  // level-1 node list
  vector<pair<int, string>> nodes; int K0 = 1;
  if (argc > 7) {
    FILE* sf = fopen(argv[7], "r"); if (!sf) { perror("seed"); return 2; }
    static char buf[1 << 16];
    while (fgets(buf, sizeof buf, sf)) {
      if (buf[0] == '#' || buf[0] == 'A') continue;
      char* c = strchr(buf, ':'); if (!c) continue;
      int idx, t, o0, o1; if (sscanf(buf, "%d %d %d %d", &idx, &t, &o0, &o1) != 4) continue;
      string x; char* p = c + 1; int v, nch;
      while (sscanf(p, "%d%n", &v, &nch) == 1) { x.push_back((char)v); p += nch; }
      nodes.push_back({t, x});
    }
    fclose(sf);
    K0 = nodes.empty() ? 1 : (int)nodes[0].second.size();
    fprintf(stderr, "seed: %zu windows of length %d\n", nodes.size(), K0);
  } else {
    for (int t = 0; t < P; t++) for (int q = 1; q <= 2 * b - 2; q++) nodes.push_back({t, string(1, (char)q)});
  }
  for (int K = K0; K <= KMAX; K++) {
    size_t n = nodes.size();
    unordered_map<string, int> id; id.reserve(n * 2);
    auto key = [](int t, const string& x) { string k(1, (char)t); k += x; return k; };
    for (size_t i = 0; i < n; i++) id[key(nodes[i].first, nodes[i].second)] = (int)i;
    vector<vector<int>> out(n), in(n);
    string y; int g;
    for (size_t i = 0; i < n; i++) for (int h = 0; h < 2; h++) {
      trans(nodes[i].second, h, y, g);
      if (g != pat[nodes[i].first]) continue;
      if ((unsigned char)y[0] < 1) continue;
      auto it = id.find(key((nodes[i].first + 1) % P, y));
      if (it == id.end()) continue;
      out[i].push_back(it->second); in[it->second].push_back((int)i);
    }
    // Kosaraju
    vector<int> order; order.reserve(n); vector<char> vis(n, 0);
    for (size_t s = 0; s < n; s++) if (!vis[s]) {
      vector<pair<int, int>> st; st.push_back({(int)s, 0}); vis[s] = 1;
      while (!st.empty()) { auto& tp = st.back(); int u = tp.first;
        if (tp.second < (int)out[u].size()) { int v = out[u][tp.second++]; if (!vis[v]) { vis[v] = 1; st.push_back({v, 0}); } }
        else { order.push_back(u); st.pop_back(); } }
    }
    vector<int> comp(n, -1); int nc = 0;
    for (int k = (int)n - 1; k >= 0; k--) { int s = order[k]; if (comp[s] >= 0) continue;
      vector<int> st{ s }; comp[s] = nc;
      while (!st.empty()) { int u = st.back(); st.pop_back(); for (int v : in[u]) if (comp[v] < 0) { comp[v] = nc; st.push_back(v); } }
      nc++; }
    // period per component: BFS depth labels inside the component
    vector<long long> per(nc, 0); vector<long long> dep(n, -1);
    for (size_t s = 0; s < n; s++) { int c = comp[s]; if (dep[s] >= 0) continue;
      vector<int> q{ (int)s }; dep[s] = 0;
      for (size_t qi = 0; qi < q.size(); qi++) { int u = q[qi]; for (int v : out[u]) if (comp[v] == c) {
        if (dep[v] < 0) { dep[v] = dep[u] + 1; q.push_back(v); } else per[c] = gcdl(per[c], dep[u] + 1 - dep[v]); } } }
    vector<char> keep(n, 0);
    for (size_t i = 0; i < n; i++) { long long q = per[comp[i]]; keep[i] = (q > 0 && L % q == 0); }
    if (EXACT) {
      // lap graph on phase-0 kept nodes
      vector<int> U; vector<int> uidx(n, -1);
      for (size_t i = 0; i < n; i++) if (keep[i] && nodes[i].first == 0) { uidx[i] = U.size(); U.push_back(i); }
      size_t nu = U.size();
      // forward one lap from each u: F[u] = nodes reachable (phases 0..P-1), lap[u] = phase-0 nodes reached after P steps
      vector<vector<int>> lap(nu);
      for (size_t a = 0; a < nu; a++) {
        vector<int> cur{ U[a] };
        for (int st = 0; st < P; st++) { vector<int> nx; for (int u : cur) for (int v : out[u]) if (keep[v]) nx.push_back(v);
          sort(nx.begin(), nx.end()); nx.erase(unique(nx.begin(), nx.end()), nx.end()); cur.swap(nx); }
        for (int v : cur) lap[a].push_back(uidx[v]);
      }
      // Ret(u) = { u' : u' ->^{m-1 laps} u } ; compute R[a] = set of a' with a' ->^{m-1} a via forward sets from each a'
      vector<vector<char>> reach(nu, vector<char>(nu, 0));   // reach[a'][a] : a' ->^{m-1 laps} a
      for (size_t a2 = 0; a2 < nu; a2++) { vector<char> cur(nu, 0); cur[a2] = 1;
        for (int k = 0; k < m - 1; k++) { vector<char> nx(nu, 0); for (size_t z = 0; z < nu; z++) if (cur[z]) for (int v : lap[z]) nx[v] = 1; cur.swap(nx); }
        reach[a2] = cur; }
      vector<char> good(n, 0);
      for (size_t a = 0; a < nu; a++) {
        // F: forward from U[a] for P-1 steps (phases 1..P-1) plus U[a] itself
        vector<char> F(n, 0); vector<int> cur{ U[a] }; F[U[a]] = 1;
        for (int st = 0; st < P - 1; st++) { vector<int> nx; for (int u : cur) for (int v : out[u]) if (keep[v] && !F[v]) { F[v] = 1; nx.push_back(v); } cur.swap(nx); }
        // Bk: nodes (phases 1..P-1, and phase 0 = U[a] itself) from which some u' with reach[u'][a] is reached by completing the lap
        vector<char> Bk(n, 0); vector<int> lay;
        for (size_t z = 0; z < nu; z++) if (reach[z][a]) { Bk[U[z]] = 2; lay.push_back(U[z]); }   // targets at phase P == 0
        // walk backwards P-1 steps through phases P-1 .. 1 (never re-enter phase 0 except the start node check below)
        for (int st = 0; st < P - 1; st++) { vector<int> nx; for (int v : lay) for (int u : in[v]) if (keep[u] && nodes[u].first != 0 && !(Bk[u] & 1)) { Bk[u] |= 1; nx.push_back(u); } lay.swap(nx); }
        // start node: on a closed walk iff one of its successors has Bk&1 (phase 1) or (P==1) reaches a target directly
        bool startOK = false;
        for (int v : out[U[a]]) if (keep[v] && ((P > 1 && (Bk[v] & 1)) || (P == 1 && (Bk[v] & 2)))) startOK = true;
        if (P > 1) { for (size_t i = 0; i < n; i++) if (F[i] && (Bk[i] & 1) && nodes[i].first != 0) good[i] = 1; }
        if (startOK) good[U[a]] = 1;
      }
      for (size_t i = 0; i < n; i++) keep[i] = keep[i] && good[i];
    }
    size_t kept = 0; for (size_t i = 0; i < n; i++) kept += keep[i];
    printf("K=%d n=%zu kept=%zu\n", K, n, kept); fflush(stdout);
    if (kept == 0) { printf("KH2 b=%d p=%d g=%s L=%d %s DIES K=%d\n", b, P, w.c_str(), L, EXACT ? "exact" : "scc", K); return 0; }
    if (K == KMAX || (long long)kept * (2 * b - 1) > NODECAP) { printf("KH2 b=%d p=%d g=%s L=%d %s SURVIVES K=%d\n", b, P, w.c_str(), L, EXACT ? "exact" : "scc", K); return 0; }
    vector<pair<int, string>> nx; nx.reserve(kept * (2 * b - 1));
    for (size_t i = 0; i < n; i++) if (keep[i]) for (int v = 0; v <= 2 * b - 2; v++) { string x = nodes[i].second; x.push_back((char)v); nx.push_back({nodes[i].first, x}); }
    nodes.swap(nx);
  }
}
