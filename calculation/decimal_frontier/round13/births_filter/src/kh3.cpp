// kh3.cpp (r13c): INDEPENDENT checker of relative tower death levels (no shared code with khr.cpp).
// Tower: nodes = (window w_0..w_{k-1}, t) above an L-periodic interface (c, xb, A) with gamma = g^{L/|g|}.
// Each edge recomputed from the full window (no incremental rule), node sets stored as hash maps of (t, digits) strings,
// closed L-walk node set computed by forward+backward walks from every anchor node of the smallest layer (std::unordered_set per layer).
// usage: kh3 b g L FILE [maxk] [maxnodes]   FILE: lines "ID K c|x,x,..|A" ; prints ID K kh3_K SAME/DIFF/SKIP
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>
#include <iostream>
#include <sstream>
using namespace std;
static int b, L;
static vector<int> C, XB, A, G;
struct Node { string w; int t; };
static inline string makeKey(const string& w, int t) { string k; k.push_back((char)t); k += w; return k; }
// compute successor window for node (w,t) and top bit h; returns false if edge absent
static bool transW(const string& w, int t, int h, string& y) {
  int k = w.size();
  static vector<int> H, Lc; H.assign(k + 2, 0); H[k] = h; // H[i] carry into column i-1 ... H[k] = h
  for (int i = k - 1; i >= 0; i--) H[i] = (int(w[i]) + H[i + 1]) / b;
  if (!((A[t] >> H[0]) & 1)) return false;
  y.resize(k);
  int carry = C[t];
  for (int i = 0; i < k; i++) {
    int wi = w[i]; int part;
    if (G[t]) part = (i == 0) ? (XB[t] + H[0]) % b : (int(w[i - 1]) + H[i]) % b;
    else part = (wi + H[i + 1]) % b;
    y[i] = (char)((wi + carry) % b + part);
    carry = (wi + carry) / b;
  }
  return true;
}
// returns death level or -k if skipped
static int runTower(int maxk, size_t maxnodes) {
  // Level 1 candidates: all digits at all phases
  vector<vector<string>> kept(L);       // kept windows per phase of previous level
  for (int t = 0; t < L; t++) { string s = ""; kept[t].push_back(s); }
  for (int k = 1; k <= maxk; k++) {
    // candidates = children of kept windows
    vector<vector<string>> cand(L);
    size_t total = 0;
    for (int t = 0; t < L; t++) for (auto& w : kept[t]) for (int d = 0; d < 2 * b - 1; d++) { string n = w; n.push_back((char)d); cand[t].push_back(n); total++; }
    if (total > maxnodes) return -k;
    vector<unordered_map<string,int>> idx(L);
    for (int t = 0; t < L; t++) { idx[t].reserve(cand[t].size()); for (int i = 0; i < (int)cand[t].size(); i++) idx[t][cand[t][i]] = i; }
    // adjacency: succ[t][i] = list of (index in layer t+1)
    vector<vector<vector<int>>> succ(L);
    for (int t = 0; t < L; t++) { succ[t].resize(cand[t].size()); int t1 = (t + 1) % L;
      for (int i = 0; i < (int)cand[t].size(); i++) { string y;
        vector<int> tg;
        for (int h = 0; h < 2; h++) if (transW(cand[t][i], t, h, y)) { auto it = idx[t1].find(y); if (it != idx[t1].end()) { if (find(tg.begin(), tg.end(), it->second) == tg.end()) tg.push_back(it->second); } }
        succ[t][i] = tg; } }
    // anchor layer: smallest candidate layer after trimming layer-wise (simple): choose layer with fewest nodes
    int t0 = 0; for (int t = 1; t < L; t++) if (cand[t].size() < cand[t0].size()) t0 = t;
    // closed walk nodes: forward/backward from each anchor node
    vector<vector<char>> onW(L); for (int t = 0; t < L; t++) onW[t].assign(cand[t].size(), 0);
    bool any = false;
    // forward reachability from every anchor individually
    for (int s = 0; s < (int)cand[t0].size(); s++) {
      // forward sets per step
      vector<vector<int>> fw(L + 1); vector<vector<char>> seen(L + 1);
      vector<int> layerIdx(L + 1); layerIdx[0] = t0; for (int i = 1; i <= L; i++) layerIdx[i] = (layerIdx[i - 1] + 1) % L;
      fw[0].push_back(s);
      for (int st = 0; st < L; st++) { int tt = layerIdx[st]; seen[st + 1].assign(cand[layerIdx[st + 1]].size(), 0);
        for (int u : fw[st]) for (int v : succ[tt][u]) if (!seen[st + 1][v]) { seen[st + 1][v] = 1; fw[st + 1].push_back(v); } }
      bool closes = false; for (int v : fw[L]) if (v == s) closes = true;
      if (!closes) continue;
      any = true;
      // backward: mark nodes on walks s -> ... -> s (length L): walk backward from s at step L
      vector<vector<char>> bk(L + 1); for (int i = 0; i <= L; i++) bk[i].assign(cand[layerIdx[i]].size(), 0);
      bk[L][s] = 1;
      for (int st = L - 1; st >= 0; st--) { int tt = layerIdx[st]; for (int u : fw[st]) { bool on = false; for (int v : succ[tt][u]) if (bk[st + 1][v]) { on = true; break; } if (on) bk[st][u] = 1; } }
      for (int st = 0; st < L; st++) { int tt = layerIdx[st]; for (int u = 0; u < (int)cand[tt].size(); u++) if (bk[st][u]) onW[tt][u] = 1; }
    }
    if (!any) return k;
    // keep nodes on closed walks (windows)
    size_t keptn = 0;
    for (int t = 0; t < L; t++) { vector<string> nk; for (int i = 0; i < (int)cand[t].size(); i++) if (onW[t][i]) { nk.push_back(cand[t][i]); keptn++; } kept[t].swap(nk); }
    // no node on any closed walk => handled by any == false
    if (keptn == 0) return k;
  }
  return -maxk;
}
int main(int argc, char** argv) {
  b = atoi(argv[1]); string gw = argv[2]; L = atoi(argv[3]); string fn = argv[4]; int maxk = argc > 5 ? atoi(argv[5]) : 200; size_t maxnodes = argc > 6 ? atoll(argv[6]) : 200000;
  G.resize(L); for (int t = 0; t < L; t++) G[t] = gw[t % gw.size()] - '0';
  FILE* f = fopen(fn.c_str(), "r"); char id[64], kbuf[64], spec[4096];
  int same = 0, diff = 0, skip = 0;
  while (fscanf(f, "%63s %63s %4095s", id, kbuf, spec) == 3) {
    string sp = spec; int K = atoi(kbuf);
    size_t b1 = sp.find('|'), b2 = sp.find('|', b1 + 1);
    string cs = sp.substr(0, b1), xs = sp.substr(b1 + 1, b2 - b1 - 1), as = sp.substr(b2 + 1);
    C.assign(L, 0); A.assign(L, 0); XB.assign(L, 0);
    for (int t = 0; t < L; t++) { C[t] = cs[t] - '0'; A[t] = as[t] - '0'; }
    { size_t q = 0; for (int t = 0; t < L; t++) { size_t r = xs.find(',', q); if (r == string::npos) r = xs.size(); XB[t] = atoi(xs.substr(q, r - q).c_str()); q = r + 1; } }
    int r = runTower(maxk, maxnodes);
    if (r < 0) { skip++; printf("SKIP %s K=%d (reached level %d)\n", id, K, -r); }
    else if (r == K) { same++; }
    else { diff++; printf("DIFF %s khr=%d kh3=%d spec=%s\n", id, K, r, spec); }
    fflush(stdout);
  }
  printf("KH3 file=%s same=%d diff=%d skip=%d\n", fn.c_str(), same, diff, skip);
  return 0;
}
