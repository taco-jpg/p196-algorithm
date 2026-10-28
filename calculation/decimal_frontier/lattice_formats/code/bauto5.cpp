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

int main(int argc, char** argv) {
  b = atoi(argv[1]); int pmin = atoi(argv[2]), pmax = atoi(argv[3]);
  unsigned long long CAPS = 3000000ULL; int maxscc = 6; string gfix; bool dens4 = false;
  for (int i = 4; i < argc; i++) { string a = argv[i]; if (a == "-cap") CAPS = strtoull(argv[++i], 0, 10); else if (a == "-maxscc") maxscc = atoi(argv[++i]); else if (a == "-g") gfix = argv[++i]; else if (a == "-dens4") dens4 = true; }
  ydig = 1; while ((1 << ydig) < b) ydig++;
  Dfa* dfa = nullptr; if (gfix.empty()) { dfa = new Dfa(b); fprintf(stderr, "b=%d DFA states %zu\n", b, dfa->st.size()); }
  for (p = pmin; p <= pmax; p++) {
    vector<u64> streams;
    if (!gfix.empty()) { if ((int)gfix.size() != p) continue; u64 v = 0; for (int t = 0; t < p; t++) if (gfix[t] == '1') v |= 1ULL << t; streams.push_back(v); }
    else streams = dfa->gen(p, dens4);
    long nstreams = streams.size(), nsurv = 0, ndeep = 0, ncap = 0, nscc = 0, nskip = 0;
    auto tstart = chrono::steady_clock::now();
    for (u64 gm : streams) {
      g.assign(p, 0); Gidx.clear(); for (int t = 0; t < p; t++) { g[t] = (gm >> t) & 1; if (g[t]) Gidx.push_back(t); }
      ng = Gidx.size();
      // Key has three 64-bit words, so an exactly 192-bit encoding is valid.
      if (2 * p + ydig * ng > 192 || p > 60) { nskip++; fprintf(stderr, "key too long p=%d ng=%d\n", p, ng); continue; }
      string gs; for (int t = 0; t < p; t++) gs += char('0' + g[t]);
      int Y0[64]; for (int i = 0; i < ng; i++) Y0[i] = 1;
      u64 Hs = 0; for (int t = 0; t < p; t++) Hs |= (u64)g[t] << t;
      Key start = pack(0, Hs, Y0);
      unordered_map<Key, int, KH> id; vector<Key> keys; vector<int> parent; vector<vector<int>> adj;
      id[start] = 0; keys.push_back(start); parent.push_back(-1); adj.emplace_back();
      bool capped = false;
      for (size_t i = 0; i < keys.size(); i++) {
        u64 L, H; int Y[64]; unpack(keys[i], L, H, Y);
        vector<int> out;
        transitions(L, H, Y, i == 0, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) {
          Key k = pack(L2, H2, Y2);
          auto it = id.find(k); int j;
          if (it == id.end()) { if (keys.size() >= CAPS) { capped = true; return; } j = keys.size(); id[k] = j; keys.push_back(k); parent.push_back((int)i); adj.emplace_back(); }
          else j = it->second;
          for (int q : out) if (q == j) return;
          out.push_back(j);
        });
        adj[i] = out;
        if (capped) break;
      }
      size_t N = keys.size();
      if (N > 1) nsurv++;
      if (capped) { ncap++; printf("CAPPED p=%d g=%s states=%zu\n", p, gs.c_str(), N); fflush(stdout); continue; }
      // levels
      vector<int> lev(N, 0); int ml = 0; for (size_t i = 1; i < N; i++) { lev[i] = lev[parent[i]] + 1; ml = max(ml, lev[i]); }
      if (ml >= 6) ndeep++;
      if (getenv("LEVPROF")) { vector<long> cnt(ml + 1, 0); for (size_t i = 0; i < N; i++) cnt[lev[i]]++; printf("LEV p=%d g=%s S=%d N=%zu maxlev=%d prof:", p, gs.c_str(), ng, N, ml); for (int q = 0; q <= ml && q < 48; q++) printf(" %ld", cnt[q]); printf("\n"); }
      // Tarjan
      vector<int> low(N, -1), num(N, -1), comp(N, -1); vector<char> on(N, 0); vector<int> stk; int cnt = 0, nc = 0; vector<vector<int>> comps;
      for (size_t r = 0; r < N; r++) {
        if (num[r] != -1) continue;
        vector<pair<int, int>> cs; cs.push_back({(int)r, 0}); num[r] = low[r] = cnt++; stk.push_back(r); on[r] = 1;
        while (!cs.empty()) {
          int v = cs.back().first; int& ei = cs.back().second;
          if (ei < (int)adj[v].size()) { int w = adj[v][ei++]; if (num[w] == -1) { num[w] = low[w] = cnt++; stk.push_back(w); on[w] = 1; cs.push_back({w, 0}); } else if (on[w]) low[v] = min(low[v], num[w]); }
          else { if (low[v] == num[v]) { vector<int> c; while (true) { int w = stk.back(); stk.pop_back(); on[w] = 0; comp[w] = nc; c.push_back(w); if (w == v) break; } nc++; comps.push_back(c); } cs.pop_back(); if (!cs.empty()) { int u = cs.back().first; low[u] = min(low[u], low[v]); } }
        }
      }
      int nontriv = 0;
      for (auto& c : comps) { bool self = false; if (c.size() == 1) for (int w : adj[c[0]]) if (w == c[0]) self = true; if (c.size() > 1 || self) nontriv++; }
      if (!nontriv) continue;
      nscc++;
      printf("G p=%d g=%s states=%zu edges=0 nontrivial_sccs=%d maxlev=%d S=%d\n", p, gs.c_str(), N, nontriv, ml, ng);
      auto cols = [&](const vector<int>& seq, bool closeBack) {
        string out;
        for (size_t i = 0; i + (closeBack ? 0 : 1) < seq.size(); i++) {
          int a = seq[i]; int bb = (i + 1 < seq.size()) ? seq[i + 1] : seq[0];
          u64 L, H; int Y[64]; unpack(keys[a], L, H, Y);
          vector<int> xf; bool got = false;
          transitions(L, H, Y, a == 0, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { if (got) return; Key k = pack(L2, H2, Y2); if (k == keys[bb]) { got = true; xf.assign(xs, xs + p); } });
          out += "["; for (int t = 0; t < p; t++) { out += to_string(xf[t]); if (t + 1 < p) out += ","; } out += "]";
        }
        return out;
      };
      int shown = 0;
      for (auto& c : comps) {
        bool self = false; if (c.size() == 1) for (int w : adj[c[0]]) if (w == c[0]) self = true; if (!(c.size() > 1 || self)) continue;
        if (shown >= maxscc) break; shown++;
        int r = c[0]; for (int w : c) if (w < r) r = w;
        vector<int> pr(N, -2), q; q.push_back(r); pr[r] = -1; int tgt = -1;
        for (size_t qi = 0; qi < q.size() && tgt < 0; qi++) { int v = q[qi]; for (int w : adj[v]) { if (comp[w] != comp[r]) continue; if (w == r) { tgt = v; break; } if (pr[w] == -2) { pr[w] = v; q.push_back(w); } } }
        vector<int> cyc; { int v = tgt; while (v != -1) { cyc.push_back(v); v = pr[v]; } reverse(cyc.begin(), cyc.end()); }
        vector<int> path; { int v = r; while (v != -1) { path.push_back(v); v = parent[v]; } reverse(path.begin(), path.end()); }
        string pcols = cols(path, false), ccols = cols(cyc, true);
        printf("SCC p=%d g=%s size=%zu cyclen=%zu depth=%zu path=%s cyc=%s\n", p, gs.c_str(), c.size(), cyc.size(), path.size() - 1, pcols.c_str(), ccols.c_str());
        // global shortest cycle length (<= ng) inside the component
        if (c.size() <= 6000) {
          int best = 1 << 30, bestv = -1; vector<int> bpr;
          for (int v0 : c) {
            if (best <= 1) break;
            vector<int> dist; unordered_map<int, int> dm; vector<int> prv; vector<int> qq; dm[v0] = 0; qq.push_back(v0); unordered_map<int, int> par; par[v0] = -1; int found = -1;
            for (size_t qi = 0; qi < qq.size() && found < 0; qi++) { int v = qq[qi]; int dv = dm[v]; if (dv + 1 > min(best - 1, ng)) break; for (int w : adj[v]) { if (comp[w] != comp[v0]) continue; if (w == v0) { found = v; break; } if (!dm.count(w)) { dm[w] = dv + 1; par[w] = v; qq.push_back(w); } } }
            if (found >= 0) { int len = dm[found] + 1; if (len < best) { best = len; bestv = v0; bpr.clear(); int v = found; while (v != -1) { bpr.push_back(v); v = par[v]; } reverse(bpr.begin(), bpr.end()); } }
          }
          if (bestv >= 0 && best <= ng) {
            printf("SCCMIN p=%d g=%s S=%d minc=%d depth=%d cyc=%s\n", p, gs.c_str(), ng, best, lev[bestv], cols(bpr, true).c_str());
          }
        }
      }
      fflush(stdout);
    }
    double el = chrono::duration<double>(chrono::steady_clock::now() - tstart).count();
    printf("SUMMARY b=%d p=%d streams=%ld survive_pos0=%ld deep(maxlev>=6)=%ld capped=%ld with_scc=%ld skipped=%ld time=%.1fs\n", b, p, nstreams, nsurv, ndeep, ncap, nscc, nskip, el);
    fflush(stdout);
  }
}
