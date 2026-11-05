// K-head pattern graph for the overflow pattern (0001) (base 10), grown one coordinate at a time,
// keeping only nodes on cycles (cyclic SCCs).  C++ port of repo py/khead_family.py (same trans()).
// Node = (x[0..K-1], phase mod 4).  Edge (x,ph) -> (y,ph+1) for h in {0,1} with g(x,h) == pat[ph].
// Output per K: #nodes on cycles, list of cyclic SCCs (size, period = gcd of cycle lengths).
// r11d variant: usage: khead_len Kmax pattern L1,L2,...  keep only cyclic SCCs whose period divides some target length Li (sound for closed walks of length Li)
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <numeric>
using namespace std;
const int b = 10, NX = 19;
int P; vector<int> pat;
struct HS { size_t operator()(const string& s) const { return hash<string>()(s); } };

static void trans(const string& x, int h, string& y, int& g) {
  int K = x.size();
  vector<int> H(K + 1), L(K + 1, 0);
  H[K] = h;
  for (int i = K - 1; i >= 0; i--) H[i] = (x[i] + H[i + 1]) / b;
  g = H[0];
  for (int i = 0; i < K; i++) L[i + 1] = (x[i] + L[i]) / b;
  y.assign(K, 0);
  for (int i = 0; i < K; i++) {
    int part = g ? (i == 0 ? 1 : (x[i - 1] + H[i]) % b) : (x[i] + H[i + 1]) % b;
    y[i] = (char)((x[i] + L[i]) % b + part);
  }
}

int main(int argc, char** argv) {
  int Kmax = atoi(argv[1]);
  string ps = argc > 2 ? argv[2] : "0001";
  int dumpK = -1; vector<int> Ls; { string a = argv[3]; size_t q = 0; while (q < a.size()) { size_t r = a.find(",", q); if (r == string::npos) r = a.size(); Ls.push_back(atoi(a.substr(q, r - q).c_str())); q = r + 1; } }
  P = ps.size(); for (char c : ps) pat.push_back(c - '0');
  // node key: phase char + x chars
  vector<string> nodes;
  for (int x = 1; x < NX; x++) for (int ph = 0; ph < P; ph++) nodes.push_back(string(1, (char)ph) + string(1, (char)x));
  for (int K = 1; K <= Kmax; K++) {
    if (K > 1) {
      vector<string> nn; nn.reserve(nodes.size() * NX);
      for (auto& s : nodes) for (int v = 0; v < NX; v++) { string t = s; t.push_back((char)v); nn.push_back(t); }
      nodes.swap(nn);
    }
    int N = nodes.size();
    unordered_map<string, int, HS> id; id.reserve(N * 2);
    for (int i = 0; i < N; i++) id[nodes[i]] = i;
    vector<vector<int>> out(N);
    string x, y; int g;
    for (int i = 0; i < N; i++) {
      int ph = nodes[i][0]; x = nodes[i].substr(1);
      for (int h = 0; h < 2; h++) {
        trans(x, h, y, g);
        if (g != pat[ph]) continue;
        string key = string(1, (char)((ph + 1) % P)) + y;
        auto it = id.find(key);
        if (it != id.end()) out[i].push_back(it->second);
      }
    }
    // iterative Tarjan
    vector<int> idx(N, -1), low(N, 0), comp(N, -1); vector<char> on(N, 0); vector<int> st; int cnt = 0, nc = 0;
    vector<pair<int, int>> cs;
    for (int v0 = 0; v0 < N; v0++) {
      if (idx[v0] >= 0) continue;
      cs.push_back({v0, 0}); idx[v0] = low[v0] = cnt++; st.push_back(v0); on[v0] = 1;
      while (!cs.empty()) {
        int u = cs.back().first; int& pi = cs.back().second;
        if (pi < (int)out[u].size()) {
          int w = out[u][pi++];
          if (idx[w] < 0) { idx[w] = low[w] = cnt++; st.push_back(w); on[w] = 1; cs.push_back({w, 0}); }
          else if (on[w]) low[u] = min(low[u], idx[w]);
          continue;
        }
        cs.pop_back();
        if (!cs.empty()) low[cs.back().first] = min(low[cs.back().first], low[u]);
        if (low[u] == idx[u]) { while (true) { int w = st.back(); st.pop_back(); on[w] = 0; comp[w] = nc; if (w == u) break; } nc++; }
      }
    }
    vector<int> csize(nc, 0); for (int i = 0; i < N; i++) csize[comp[i]]++;
    vector<char> cyc(nc, 0);
    for (int i = 0; i < N; i++) for (int w : out[i]) if (comp[w] == comp[i]) cyc[comp[i]] = 1;
    // period per cyclic component: BFS distances within component
    vector<int> dist(N, -1), per(nc, 0);
    vector<int> root(nc, -1); for (int i = 0; i < N; i++) if (cyc[comp[i]] && root[comp[i]] < 0) root[comp[i]] = i;
    for (int c = 0; c < nc; c++) {
      if (!cyc[c]) continue;
      vector<int> q{root[c]}; dist[root[c]] = 0; int gg = 0;
      for (size_t qi = 0; qi < q.size(); qi++) { int u = q[qi]; for (int w : out[u]) { if (comp[w] != c) continue; if (dist[w] < 0) { dist[w] = dist[u] + 1; q.push_back(w); } else gg = gcd(gg, dist[u] + 1 - dist[w]); } }
      per[c] = gg;
    }
    vector<string> keep; vector<pair<int, int>> info;
    for (int i = 0; i < N; i++) if (cyc[comp[i]]) { int q = per[comp[i]]; bool ok = false; for (int L : Ls) if (q > 0 && L % q == 0) ok = true; if (ok) keep.push_back(nodes[i]); }
    for (int c = 0; c < nc; c++) if (cyc[c]) info.push_back({csize[c], per[c]});
    sort(info.rbegin(), info.rend());
    printf("K=%d: nodes on cycles %zu, cyclic SCCs %zu:", K, keep.size(), info.size());
    for (size_t i = 0; i < info.size() && i < 20; i++) printf(" (%d,%d)", info[i].first, info[i].second);
    // histogram of periods
    unordered_map<int, long> ph; for (auto& p : info) ph[p.second] += p.first;
    printf("  | nodes by period:"); vector<pair<int,long>> hv(ph.begin(), ph.end()); sort(hv.begin(), hv.end());
    for (auto& p : hv) printf(" %d:%ld", p.first, p.second);
    printf("\n"); fflush(stdout);
    if (K == dumpK) {
      FILE* f = fopen("khead_dump.txt", "w");
      for (int i = 0; i < N; i++) if (cyc[comp[i]]) { fprintf(f, "%d %d %d", comp[i], per[comp[i]], (int)nodes[i][0]); for (size_t j = 1; j < nodes[i].size(); j++) fprintf(f, " %d", nodes[i][j]); fprintf(f, "\n"); }
      fclose(f);
    }
    nodes.swap(keep);
    if (nodes.empty()) { printf("family dies at K=%d\n", K); break; }
  }
}
