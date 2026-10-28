// blockabs: SOUND over-approximation ("open block abstraction") of the position automaton.
// The state of a full automaton projected to the time window [t0, t0+q) (cyclic) evolves under the OPEN chain transition
// (free start value x_{t0}, no closure condition).  proj(Reach(start)) is a subset of Reach_block(proj(start)).
// If the projection of a target state is NOT in Reach_block, the target is UNREACHABLE from the start (PROOF, given the engine).
// usage: blockabs b g q dumpfile [-cap N]   (tests every offset t0 in 0..p-1)
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <chrono>
using namespace std;
typedef uint64_t u64;
int b, P, Q, ydig;
vector<int> G;
// block state: L (q bits) | H (q bits) << q | Y digits (ydig bits each, ngb of them) << 2q   (<= 64 bits)
struct Blk { int t0; vector<int> gt; vector<int> gi; int ngb; };
static inline u64 packb(const Blk& B, u64 L, u64 H, const int* Y) { u64 k = L | (H << Q); int sh = 2 * Q; for (int i = 0; i < B.ngb; i++) { k |= (u64)Y[i] << sh; sh += ydig; } return k; }
static inline void unpackb(const Blk& B, u64 k, u64& L, u64& H, int* Y) { u64 m = (1ULL << Q) - 1; L = k & m; H = (k >> Q) & m; int sh = 2 * Q; for (int i = 0; i < B.ngb; i++) { Y[i] = (int)((k >> sh) & ((1u << ydig) - 1)); sh += ydig; } }
template <class F> static void trans(const Blk& B, u64 L, u64 H, const int* Y, bool first, F emit) {
  for (int x0 = first ? 1 : 0; x0 <= 2 * b - 2; x0++) {
    // DFS over hn choices
    int hn[64], xs[64];
    struct Fr { int i, x, ch; };
    vector<Fr> st; st.push_back({0, x0, 0}); xs[0] = x0;
    while (!st.empty()) {
      Fr& f = st.back();
      if (f.i == Q) {
        u64 L2 = 0, H2 = 0; int Y2[64];
        for (int i = 0; i < Q; i++) { L2 |= (u64)((xs[i] + ((L >> i) & 1)) / b) << i; H2 |= (u64)hn[i] << i; }
        for (int j = 0; j < B.ngb; j++) { int i = B.gi[j]; Y2[j] = (xs[i] + hn[i]) % b; }
        emit(L2, H2, Y2); st.pop_back(); continue;
      }
      if (f.ch >= 2) { st.pop_back(); continue; }
      int c = f.ch++; int i = f.i, x = f.x;
      if (first && x == 0) continue;
      if ((x + c) / b != (int)((H >> i) & 1)) continue;
      hn[i] = c; xs[i] = x;
      int yi = -1; if (G[(B.t0 + i) % P]) { for (int j = 0; j < B.ngb; j++) if (B.gi[j] == i) yi = j; }
      int nx = (x + (int)((L >> i) & 1)) % b + (G[(B.t0 + i) % P] ? Y[yi] : (x + c) % b);
      if (i + 1 < Q) { xs[i + 1] = nx; st.push_back({i + 1, nx, 0}); }
      else { // last: emit without closure
        u64 L2 = 0, H2 = 0; int Y2[64];
        for (int ii = 0; ii < Q; ii++) { L2 |= (u64)((xs[ii] + ((L >> ii) & 1)) / b) << ii; H2 |= (u64)hn[ii] << ii; }
        for (int j = 0; j < B.ngb; j++) { int ii = B.gi[j]; Y2[j] = (xs[ii] + hn[ii]) % b; }
        emit(L2, H2, Y2);
      }
    }
  }
}
int main(int argc, char** argv) {
  b = atoi(argv[1]); string gs = argv[2]; Q = atoi(argv[3]); string dump = argv[4]; P = gs.size(); size_t CAP = 20000000;
  for (int i = 5; i < argc; i++) { string a = argv[i]; if (a == "-cap") CAP = strtoull(argv[++i], 0, 10); }
  ydig = 1; while ((1 << ydig) < b) ydig++;
  G.assign(P, 0); for (int t = 0; t < P; t++) G[t] = gs[t] == '1';
  int ng = 0; for (int t = 0; t < P; t++) ng += G[t];
  // read lattice target states (full-state) from dump: L H Y_0..Y_{ng-1}; keep also the lattice index
  struct Tg { u64 L, H; vector<int> Y; int lat, pos; };
  vector<Tg> tg; int nlat = 0;
  { ifstream f(dump); string line; while (getline(f, line)) { if (line.rfind("LAT", 0) == 0) { int m; size_t ns; sscanf(line.c_str(), "LAT %d %zu", &m, &ns); for (int k = 0; k < m; k++) { getline(f, line); istringstream is(line); Tg t; is >> t.L >> t.H; t.Y.resize(ng); for (int i = 0; i < ng; i++) is >> t.Y[i]; t.lat = nlat; t.pos = k; tg.push_back(t); } nlat++; getline(f, line); } } }
  printf("targets: %zu states in %d lattices; q=%d p=%d\n", tg.size(), nlat, Q, P); fflush(stdout);
  vector<char> excluded(nlat, 0);  // lattice proven unreachable (some state excluded at some offset)
  vector<char> state_ex(tg.size(), 0);
  int nincl_all = 0;
  // block types: distinct stream windows; cache reach sets by window string
  unordered_map<string, unordered_set<u64>*> cache; unordered_map<string, bool> capped;
  for (int t0 = 0; t0 < P; t0++) {
    Blk B; B.t0 = t0; for (int i = 0; i < Q; i++) { int t = (t0 + i) % P; if (G[t]) B.gi.push_back(i); } B.ngb = B.gi.size();
    if (2 * Q + ydig * B.ngb > 64) { printf("block too wide\n"); return 1; }
    string win; for (int i = 0; i < Q; i++) win += char('0' + G[(t0 + i) % P]);
    unordered_set<u64>* R;
    if (!cache.count(win)) {
      R = new unordered_set<u64>(); vector<u64> fr; int Y0[64]; for (int j = 0; j < B.ngb; j++) Y0[j] = 1;
      u64 H0 = 0; for (int i = 0; i < Q; i++) H0 |= (u64)G[(t0 + i) % P] << i;
      u64 s0 = packb(B, 0, H0, Y0); R->insert(s0); fr.push_back(s0); bool cap = false;
      for (size_t i = 0; i < fr.size() && !cap; i++) { u64 L, H; int Y[64]; unpackb(B, fr[i], L, H, Y); trans(B, L, H, Y, i == 0, [&](u64 L2, u64 H2, int* Y2) { u64 k = packb(B, L2, H2, Y2); if (R->insert(k).second) { if (R->size() >= CAP) cap = true; else fr.push_back(k); } }); }
      cache[win] = R; capped[win] = cap; printf("window %s: |R_block|=%zu%s\n", win.c_str(), R->size(), cap ? " CAPPED" : ""); fflush(stdout);
    } else R = cache[win];
    if (capped[win]) continue;
    for (size_t j = 0; j < tg.size(); j++) {
      u64 L = 0, H = 0; int Y[64]; int yj = 0;
      for (int i = 0; i < Q; i++) { int t = (t0 + i) % P; L |= ((tg[j].L >> t) & 1) << i; H |= ((tg[j].H >> t) & 1) << i; }
      // Y indices: full gam index of time t = number of gam times before t
      for (int i = 0; i < Q; i++) { int t = (t0 + i) % P; if (G[t]) { int gidx = 0; for (int s = 0; s < t; s++) gidx += G[s]; Y[yj++] = tg[j].Y[gidx]; } }
      u64 k = packb(B, L, H, Y);
      if (!R->count(k)) state_ex[j] = 1;
    }
  }
  // a lattice is unreachable if ANY of its states is excluded?  No: reachability needs only ONE state of the lattice reachable
  // (then the whole cycle is).  A lattice is proven unreachable iff EVERY state of the lattice is excluded at some offset.
  int nex = 0, nlt = nlat; vector<int> cnt(nlat, 0), tot(nlat, 0);
  for (size_t j = 0; j < tg.size(); j++) { tot[tg[j].lat]++; if (state_ex[j]) cnt[tg[j].lat]++; }
  for (int l = 0; l < nlat; l++) if (cnt[l] == tot[l]) nex++;
  printf("RESULT: lattices=%d proven_unreachable_by_block_abstraction=%d (all states excluded at some window offset)\n", nlat, nex);
}
