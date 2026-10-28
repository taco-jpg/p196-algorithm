// bauto5: exact position-automaton census of periodic-lattice exterior cycles (any base b <= 32, p <= 60).
// Same transition system as bauto3 (validated against the repo's bauto for neutral bands), but
//  * 192-bit state keys,
//  * streams generated from the exact regular language of the position-0 counter (small DFA, backward-pruned),
//  * for each nontrivial SCC the globally shortest cycle length (if <= S = #ones) is reported (SCCMIN) for the self-mirror lattice test.
// usage: bauto5 b pmin pmax [-cap N] [-maxscc k] [-g stream] [-dens4] [-v]
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <array>
#include <string>
#include <map>
#include <set>
#include <unordered_map>
#include <algorithm>
#include <chrono>
using namespace std;
typedef uint64_t u64;
struct Key {
  u64 w[3];
  Key() { w[0] = w[1] = w[2] = 0; }
  bool operator==(const Key& o) const { return w[0] == o.w[0] && w[1] == o.w[1] && w[2] == o.w[2]; }
};
static inline void kput(Key& k, int pos, int nb, u64 v) { for (int i = 0; i < nb; i++) { int q = pos + i; if ((v >> i) & 1) k.w[q >> 6] |= 1ULL << (q & 63); } }
static inline u64 kget(const Key& k, int pos, int nb) { u64 v = 0; for (int i = 0; i < nb; i++) { int q = pos + i; v |= ((k.w[q >> 6] >> (q & 63)) & 1ULL) << i; } return v; }
struct KH { size_t operator()(const Key& k) const { return (size_t)((k.w[0] * 0x9E3779B97F4A7C15ULL) ^ (k.w[1] * 0xC2B2AE3D27D4EB4FULL) ^ (k.w[2] * 0x165667B19E3779F9ULL) ^ (k.w[0] >> 29)); } };
int b, p, ydig, ng;
vector<int> g, Gidx;
static inline u64 mask_p() { return p >= 64 ? ~0ULL : ((1ULL << p) - 1); }
static inline Key pack(u64 L, u64 H, const int* Y) { Key k; kput(k, 0, p, L); kput(k, p, p, H); int sh = 2 * p; for (int i = 0; i < ng; i++) { kput(k, sh, ydig, (u64)Y[i]); sh += ydig; } return k; }
static inline void unpack(const Key& k, u64& L, u64& H, int* Y) { L = kget(k, 0, p); H = kget(k, p, p); int sh = 2 * p; for (int i = 0; i < ng; i++) { Y[i] = (int)kget(k, sh, ydig); sh += ydig; } }

template <class F> void transitions(u64 L, u64 H, const int* Y, bool first, F emit) {
  int yi[64]; { int c = 0; for (int t = 0; t < p; t++) yi[t] = g[t] ? c++ : -1; }
  for (int x0 = (first ? 1 : 0); x0 <= 2 * b - 2; x0++) {
    int xs[64]; int hn[64];
    struct Fr { int t; int x; int ch; };
    vector<Fr> st; st.push_back({0, x0, 0}); xs[0] = x0;
    while (!st.empty()) {
      Fr& f = st.back();
      if (f.t == p) {
        if (f.x == x0) {
          u64 L2 = 0, H2 = 0; int Y2[64];
          for (int t = 0; t < p; t++) { L2 |= (u64)((xs[t] + ((L >> t) & 1)) / b) << t; H2 |= (u64)hn[t] << t; }
          for (int i = 0; i < ng; i++) { int t = Gidx[i]; Y2[i] = (xs[t] + hn[t]) % b; }
          emit(L2, H2, Y2, xs, hn);
        }
        st.pop_back(); continue;
      }
      if (f.ch >= 2) { st.pop_back(); continue; }
      int c = f.ch++; int t = f.t, x = f.x;
      if (first && x == 0) continue;
      if ((x + c) / b != (int)((H >> t) & 1)) continue;
      int nx = (x + (int)((L >> t) & 1)) % b + (g[t] ? Y[yi[t]] : (x + c) % b);
      xs[t] = x; hn[t] = c;
      if (t + 1 < p) { xs[t + 1] = nx; st.push_back({t + 1, nx, 0}); }
      else {
        if (nx == x0) {
          u64 L2 = 0, H2 = 0; int Y2[64];
          for (int tt = 0; tt < p; tt++) { L2 |= (u64)((xs[tt] + ((L >> tt) & 1)) / b) << tt; H2 |= (u64)hn[tt] << tt; }
          for (int i = 0; i < ng; i++) { int tt = Gidx[i]; Y2[i] = (xs[tt] + hn[tt]) % b; }
          emit(L2, H2, Y2, xs, hn);
        }
      }
    }
  }
}

// ---------------- position-0 language DFA (counter) ----------------
struct Dfa {
  vector<vector<u64>> st; map<vector<u64>, int> id; vector<array<int, 2>> nx; vector<char> acc; int nn;
  Dfa(int b) {
    nn = 2 * b - 2;
    vector<u64> init(nn); for (int i = 0; i < nn; i++) init[i] = 1ULL << i;
    auto succ = [&](int x, int gg, vector<int>& out) { // x in 1..nn
      out.clear();
      for (int hn = 0; hn < 2; hn++) { int s = x + hn; if (s / b != gg) continue; int xn = x % b + (gg ? 1 : s % b); if (xn >= 1 && xn <= nn) out.push_back(xn); }
    };
    id[init] = 0; st.push_back(init); nx.push_back({-1, -1});
    for (size_t i = 0; i < st.size(); i++) {
      for (int gg = 0; gg < 2; gg++) {
        vector<u64> ns(nn, 0); bool any = false;
        for (int j = 0; j < nn; j++) {
          u64 m = st[i][j]; vector<int> o;
          for (int xi = 0; xi < nn; xi++) if ((m >> xi) & 1) { succ(xi + 1, gg, o); for (int xn : o) ns[j] |= 1ULL << (xn - 1); }
          if (ns[j]) any = true;
        }
        if (!any) { nx[i][gg] = -1; continue; }
        auto it = id.find(ns);
        if (it == id.end()) { int k = st.size(); id[ns] = k; st.push_back(ns); nx.push_back({-1, -1}); nx[i][gg] = k; }
        else nx[i][gg] = it->second;
      }
    }
    acc.assign(st.size(), 0);
    for (size_t i = 0; i < st.size(); i++) for (int j = 0; j < nn; j++) if ((st[i][j] >> j) & 1) acc[i] = 1;
  }
  vector<u64> gen(int P, bool dens4) {
    int S = st.size();
    vector<vector<char>> feas(P + 1, vector<char>(S, 0));
    for (int s = 0; s < S; s++) feas[0][s] = acc[s];
    for (int r = 1; r <= P; r++) for (int s = 0; s < S; s++) { char f = 0; for (int gg = 0; gg < 2; gg++) { int n2 = nx[s][gg]; if (n2 >= 0 && feas[r - 1][n2]) f = 1; } feas[r][s] = f; }
    vector<u64> out;
    // iterative DFS
    vector<int> stS(P + 1), stC(P + 1); u64 w = 0;
    if (!feas[P][0]) return out;
    int d = 0; stS[0] = 0; stC[0] = 0;
    while (d >= 0) {
      if (d == P) {
        // canonical (minimal rotation), optional density
        bool ok = true; for (int r = 1; r < P && ok; r++) { u64 rot = ((w >> r) | (w << (P - r))) & mask_p(); if (rot < w) ok = false; }
        if (ok && dens4 && 4 * __builtin_popcountll(w) < P) ok = false;
        if (ok) out.push_back(w);
        d--; continue;
      }
      if (stC[d] >= 2) { d--; continue; }
      int gg = stC[d]++; int n2 = nx[stS[d]][gg];
      if (n2 < 0 || !feas[P - d - 1][n2]) continue;
      if (gg) w |= 1ULL << d; else w &= ~(1ULL << d);
      stS[d + 1] = n2; stC[d + 1] = 0; d++;
    }
    return out;
  }
};


// ---- open-addressing visited set ----
struct VSet {
  vector<int> tab; vector<Key> keys; vector<int> parent; vector<short> lev; size_t mask;
  VSet(size_t cap) { size_t sz = 1; while (sz < cap * 2) sz <<= 1; tab.assign(sz, -1); mask = sz - 1; keys.reserve(cap); parent.reserve(cap); lev.reserve(cap); }
  int find(const Key& k) const { size_t h = KH()(k) & mask; while (true) { int v = tab[h]; if (v < 0) return -1; if (keys[v] == k) return v; h = (h + 1) & mask; } }
  int add(const Key& k, int par, int lv) { size_t h = KH()(k) & mask; while (tab[h] >= 0) h = (h + 1) & mask; int id = keys.size(); keys.push_back(k); parent.push_back(par); lev.push_back((short)lv); tab[h] = id; return id; }
};

int main(int argc, char** argv) {
  b = atoi(argv[1]); int pmin = atoi(argv[2]), pmax = atoi(argv[3]);
  unsigned long long CAPS = 20000000ULL; string gfix; bool dens4 = false; int maxcand = 2000000; int maxlen = -1;
  for (int i = 4; i < argc; i++) { string a = argv[i]; if (a == "-cap") CAPS = strtoull(argv[++i], 0, 10); else if (a == "-g") gfix = argv[++i]; else if (a == "-dens4") dens4 = true; else if (a == "-maxlen") maxlen = atoi(argv[++i]); }
  ydig = 1; while ((1 << ydig) < b) ydig++;
  Dfa* dfa = nullptr; if (gfix.empty()) { dfa = new Dfa(b); fprintf(stderr, "b=%d DFA states %zu\n", b, dfa->st.size()); }
  for (p = pmin; p <= pmax; p++) {
    vector<u64> streams;
    if (!gfix.empty()) { if ((int)gfix.size() != p) continue; u64 v = 0; for (int t = 0; t < p; t++) if (gfix[t] == '1') v |= 1ULL << t; streams.push_back(v); }
    else streams = dfa->gen(p, dens4);
    long nstreams = streams.size(), nsurv = 0, ndeep = 0, ncap = 0, nhit = 0, nskip = 0;
    auto tstart = chrono::steady_clock::now();
    for (u64 gm : streams) {
      g.assign(p, 0); Gidx.clear(); for (int t = 0; t < p; t++) { g[t] = (gm >> t) & 1; if (g[t]) Gidx.push_back(t); }
      ng = Gidx.size();
      if (2 * p + ydig * ng > 191 || p > 60) { nskip++; continue; }
      int Smax = maxlen > 0 ? maxlen : ng;   // look for cycles of length <= Smax
      string gs; for (int t = 0; t < p; t++) gs += char('0' + g[t]);
      int Y0[64]; for (int i = 0; i < ng; i++) Y0[i] = 1;
      u64 Hs = 0; for (int t = 0; t < p; t++) Hs |= (u64)g[t] << t;
      Key start = pack(0, Hs, Y0);
      // small initial capacity; grow by re-creating? use staged caps: first try 200k, double on demand
      size_t capNow = 200000; if (capNow > CAPS) capNow = CAPS;
      VSet* V = new VSet(capNow);
      V->add(start, -1, 0);
      vector<pair<int, int>> cand; // back edges (s -> t) with 0 <= lev(s)-lev(t) <= Smax-1
      bool capped = false; size_t nedges = 0;
      for (size_t i = 0; i < V->keys.size(); i++) {
        u64 L, H; int Y[64]; Key ki = V->keys[i]; int li = V->lev[i]; unpack(ki, L, H, Y);
        transitions(L, H, Y, i == 0, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) {
          Key k = pack(L2, H2, Y2); int j = V->find(k); nedges++;
          if (j < 0) {
            if (V->keys.size() >= capNow) {
              if (capNow >= CAPS) { capped = true; return; }
              // grow: rebuild
              size_t nc = min<size_t>(capNow * 4, CAPS); VSet* W = new VSet(nc);
              for (size_t q = 0; q < V->keys.size(); q++) W->add(V->keys[q], V->parent[q], V->lev[q]);
              delete V; V = W; capNow = nc;
            }
            V->add(k, (int)i, li + 1);
          } else {
            int d = li - V->lev[j];
            if (d >= 0 && d <= Smax - 1 && (int)cand.size() < maxcand) cand.push_back({(int)i, j});
          }
        });
        if (capped) break;
      }
      size_t N = V->keys.size();
      if (N > 1) nsurv++;
      int ml = 0; for (size_t i = 0; i < N; i++) ml = max(ml, (int)V->lev[i]);
      if (ml >= 6) ndeep++;
      if (capped) { ncap++; printf("CAPPED p=%d g=%s S=%d states=%zu maxlev=%d cand=%zu\n", p, gs.c_str(), ng, N, ml, cand.size()); fflush(stdout); }
      // verify candidates: shortest return path from t to s of length <= Smax-1 (cycle length <= Smax)
      int bestLen = 1 << 30; vector<int> bestCyc; int bestDepth = 0;
      for (auto& cd : cand) {
        int s = cd.first, t = cd.second;
        if (s == t) { if (1 < bestLen) { bestLen = 1; bestCyc = {s}; bestDepth = V->lev[s]; } continue; }
        // BFS from t, find s within depth Smax-1 (edges), restricted by levels not needed
        unordered_map<int, int> par; par[t] = -1; vector<pair<int,int>> q; q.push_back({t, 0}); bool found = false; size_t qi = 0;
        // map for nodes by index (recompute transitions)
        while (qi < q.size() && !found) {
          int v = q[qi].first, dv = q[qi].second; qi++;
          if (dv >= Smax - 1 || dv + 1 >= bestLen - 0) continue;
          u64 L, H; int Y[64]; unpack(V->keys[v], L, H, Y);
          transitions(L, H, Y, v == 0, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) {
            if (found) return; Key k = pack(L2, H2, Y2); int j = V->find(k); if (j < 0) return;
            if (j == s) { par[s] = v; found = true; return; }
            if (!par.count(j)) { par[j] = v; q.push_back({j, dv + 1}); }
          });
        }
        if (found) {
          vector<int> pth; int v = s; while (v != -1) { pth.push_back(v); v = par[v]; } reverse(pth.begin(), pth.end()); // t ... s
          int len = pth.size();
          if (len < bestLen) { bestLen = len; bestCyc = pth; bestDepth = V->lev[t]; }
        }
      }
      if (bestLen <= Smax) {
        nhit++;
        auto cols = [&](const vector<int>& seq) {
          string out;
          for (size_t i = 0; i < seq.size(); i++) {
            int a = seq[i]; int bb = (i + 1 < seq.size()) ? seq[i + 1] : seq[0];
            u64 L, H; int Y[64]; unpack(V->keys[a], L, H, Y);
            vector<int> xf; bool got = false;
            transitions(L, H, Y, a == 0, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { if (got) return; Key k = pack(L2, H2, Y2); if (k == V->keys[bb]) { got = true; xf.assign(xs, xs + p); } });
            out += "["; for (int tt = 0; tt < p; tt++) { out += to_string(xf[tt]); if (tt + 1 < p) out += ","; } out += "]";
          }
          return out;
        };
        // path from start to bestCyc[0]
        vector<int> path; { int v = bestCyc[0]; while (v != -1) { path.push_back(v); v = V->parent[v]; } reverse(path.begin(), path.end()); }
        string pc; for (size_t i = 0; i + 1 < path.size(); i++) { vector<int> two = {path[i], path[i + 1]}; string c = cols(two); pc += c.substr(0, c.find(']') + 1); }
        printf("CYC p=%d g=%s S=%d minc=%d depth=%d states=%zu capped=%d path=%s cyc=%s\n", p, gs.c_str(), ng, bestLen, bestDepth, N, (int)capped, pc.c_str(), cols(bestCyc).c_str());
        fflush(stdout);
      }
      delete V;
    }
    double el = chrono::duration<double>(chrono::steady_clock::now() - tstart).count();
    printf("SUMMARY b=%d p=%d streams=%ld survive_pos0=%ld deep=%ld capped=%ld short_cycle_streams=%ld skipped=%ld time=%.1fs\n", b, p, nstreams, nsurv, ndeep, ncap, nhit, nskip, el);
    fflush(stdout);
  }
}
