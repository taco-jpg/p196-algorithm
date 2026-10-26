// Exact layer-automaton for the C-system (symmetric centre block) under a periodic driver stream.
// C++ port of cauto2.py (validated against brute force, see ctest*.py).
//
// usage: cauto b e g m0lo m0hi [-v pattern | -vall] [-w] [-part i n] [-cap N]
//   b        base
//   e, g     driver bit strings (length P): e_t = carry into C at step t (= e1 of B), g_t = overflow (gam) at step t.
//            If sum(g) is odd, pass the stream repeated twice (C's period must have even total overflow).
//   m0lo..m0hi   range of |C_0| to try
//   -v pat   trim pattern v_t in {0,1} per step (sum v = sum g / 2);  -vall  tries every such pattern
//   -w       print the witness C_0..C_{P-1}
// Output lines:  FEASIBLE b=.. e=.. g=.. v=.. m0=..  [C_t=...]   (one per feasible instance)
// Model: C_t symmetric (length m_t, entries 0..2b-2), carry(C_t, e_t) = 1-e_t,  C_{t+1} = trim_{v_t}(pairsum(DC_t [+ y])),
//        m_{t+1} = m_t + g_t - 2 v_t, closure C_P = C_0.  Layers j = 0,1,.. are the symmetric pairs (j, m_t-1-j), scanned from the
//        outer end inward; v_t=1 needs a one-layer look-ahead (pending guess Z).
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
using namespace std;
typedef unsigned __int128 K128;
struct KH { size_t operator()(const K128& k) const { uint64_t a = (uint64_t)k, c = (uint64_t)(k >> 64); return (size_t)((a * 0x9E3779B97F4A7C15ULL) ^ (c * 0xC2B2AE3D27D4EB4FULL) ^ (a >> 29)); } };
const int MAXP = 32;
const int NONE = -1;
struct St { int8_t l[MAXP], r[MAXP], Rd[MAXP], Z[MAXP]; };
int b, P;
vector<int> e, g, v;
// instance data
vector<int> m, J, Jp, yd;
vector<vector<int>> order; int nseg;
int Jall;
bool noV;
static inline int nx(int t) { return (t + 1) % P; }
K128 pack(const St& s) {
  K128 k = 0; int sh = 0;
  for (int t = 0; t < P; t++) { k |= (K128)(s.l[t] & 1) << sh; sh++; }
  for (int t = 0; t < P; t++) { k |= (K128)(s.r[t] & 1) << sh; sh++; }
  for (int t = 0; t < P; t++) if (g[t]) { k |= (K128)(uint8_t)(s.Rd[t] + 1) << sh; sh += 7; }
  for (int t = 0; t < P; t++) if (v[t]) { k |= (K128)(uint8_t)(s.Z[t] + 1) << sh; sh += 8; }
  return k;
}
struct Layer { vector<St> st; vector<uint32_t> par; vector<vector<uint8_t>> cols; unordered_map<K128, uint32_t, KH> idx; };
// per-layer search context
struct Ctx {
  int j; const St* S; Layer* out; uint32_t parent; bool wit; long cap; bool capped;
  int guess0;
};
void emit(Ctx& C, const St& w, const vector<uint8_t>& cols) {
  K128 k = pack(w);
  if (C.out->idx.count(k)) return;
  uint32_t id = C.out->st.size();
  C.out->idx[k] = id; C.out->st.push_back(w); C.out->par.push_back(C.parent);
  if (C.wit) C.out->cols.push_back(cols);
  if ((long)C.out->st.size() > C.cap) C.capped = true;
}
void nextseg(Ctx& C, int si, St w, vector<uint8_t>& cols);
void walk(Ctx& C, int si, int k, int c, St w, vector<uint8_t>& cols) {
  if (C.capped) return;
  const int j = C.j; const St& S = *C.S;
  const vector<int>& seg = order[si]; int t = seg[k];
  struct Out { int rin, Rj, lout, cp; };
  Out outs[2]; int no = 0;
  if (j < J[t]) {
    int lin = S.l[t]; int sm = c + lin; int Ld = sm % b; int lout = sm / b; int rreq = S.r[t];
    int rp = (j == 0) ? yd[t] : S.Rd[t];
    if (m[t] % 2 == 1 && j == J[t] - 1) {
      if (lout != rreq) return;
      int cp = g[t] == 0 ? 2 * Ld : Ld + rp;
      outs[no++] = {-1, Ld, lout, cp};
    } else if (m[t] % 2 == 0 && j == J[t] - 1) {
      int rin = lout;
      if ((c + rin) / b != rreq) return;
      int Rj = (c + rin) % b; int cp = g[t] == 0 ? Ld + Rj : Ld + rp;
      outs[no++] = {rin, Rj, lout, cp};
    } else {
      for (int rin = 0; rin < 2; rin++) if ((c + rin) / b == rreq) {
        int Rj = (c + rin) % b; int cp = g[t] == 0 ? Ld + Rj : Ld + rp;
        outs[no++] = {rin, Rj, lout, cp};
      }
    }
  } else {
    if (j < Jp[t]) outs[no++] = {-1, -1, -1, 2 * S.Rd[t]};
    else outs[no++] = {-1, -1, -1, NONE};
  }
  for (int oi = 0; oi < no; oi++) {
    Out o = outs[oi]; St w2 = w; uint8_t saved = cols[t];
    if (j < J[t]) {
      w2.l[t] = o.lout; if (o.rin >= 0) w2.r[t] = o.rin; if (g[t]) w2.Rd[t] = o.Rj;
      cols[t] = (uint8_t)c;
    }
    if (noV) {
      // single segment covering all times; closure: c'_{P-1}[j] == c_0[j]
      if (o.cp != NONE && o.cp > 2 * b - 2) { cols[t] = saved; continue; }
      if (k + 1 < (int)seg.size()) walk(C, si, k + 1, o.cp, w2, cols);
      else {
        int c0 = C.guess0;
        if (o.cp != c0) { cols[t] = saved; continue; }
        emit(C, w2, cols);
      }
    } else if (v[t] == 0) {
      if (o.cp != NONE && o.cp > 2 * b - 2) { cols[t] = saved; continue; }
      if (k + 1 < (int)seg.size()) walk(C, si, k + 1, o.cp, w2, cols);
      else nextseg(C, si + 1, w2, cols);
    } else {
      bool ok = true;
      if (o.cp != NONE) { if (j == 0) { if (o.cp != b - 1) ok = false; } else if (S.Z[t] != o.cp) ok = false; }
      else { if (j > 0 && S.Z[t] != NONE) ok = false; }
      if (ok) {
        if (si == nseg - 1) w2.Z[t] = C.guess0;
        nextseg(C, si + 1, w2, cols);
      }
    }
    cols[t] = saved;
  }
}
void nextseg(Ctx& C, int si, St w, vector<uint8_t>& cols) {
  if (si == nseg) { if (!noV) emit(C, w, cols); return; }
  int s = order[si][0];
  int endPrev = (si > 0) ? order[si - 1].back() : -1;
  if (C.j < J[s]) {
    for (int c0 = 0; c0 <= 2 * b - 2; c0++) {
      St w2 = w; if (si > 0) w2.Z[endPrev] = c0; else C.guess0 = c0;
      walk(C, si, 0, c0, w2, cols);
    }
  } else {
    St w2 = w; if (si > 0) w2.Z[endPrev] = NONE; else C.guess0 = NONE;
    walk(C, si, 0, NONE, w2, cols);
  }
}

// ---------- instance setup / layer step / solve ----------
bool setup_instance(int m0) {
  m.assign(P, 0); m[0] = m0;
  for (int t = 0; t + 1 < P; t++) m[t + 1] = m[t] + g[t] - 2 * v[t];
  if (m[P - 1] + g[P - 1] - 2 * v[P - 1] != m0) return false;
  for (int t = 0; t < P; t++) if (m[t] < 1 || m[t] + g[t] - 2 * v[t] < 1) return false;
  J.assign(P, 0); Jp.assign(P, 0);
  for (int t = 0; t < P; t++) { J[t] = (m[t] + 1) / 2; Jp[t] = (m[t] + g[t] + 1) / 2; }
  Jall = *max_element(Jp.begin(), Jp.end());
  yd.assign(P, 0); for (int t = 0; t < P; t++) yd[t] = (b - 1) * e[t];
  order.clear();
  noV = true; for (int t = 0; t < P; t++) if (v[t]) noV = false;
  if (noV) { vector<int> seg; for (int t = 0; t < P; t++) seg.push_back(t); order.push_back(seg); nseg = 1; }
  else {
    for (int t = 0; t < P; t++) if (v[t]) {
      int s = nx(t); vector<int> seg{s}; int u = s;
      while (v[u] == 0) { u = nx(u); seg.push_back(u); }
      order.push_back(seg);
    }
    nseg = order.size();
  }
  return true;
}
St start_state() {
  St start; memset(&start, 0, sizeof(start));
  for (int t = 0; t < P; t++) { start.l[t] = e[t]; start.r[t] = 1 - e[t]; start.Rd[t] = g[t] ? yd[t] : NONE; start.Z[t] = NONE; }
  return start;
}
// one layer; returns false if capped
bool run_layer(int j, Layer& OL, Layer& NL, bool wit, long cap) {
  for (size_t si = 0; si < OL.st.size(); si++) {
    Ctx C; C.j = j; C.S = &OL.st[si]; C.out = &NL; C.parent = si; C.wit = wit; C.cap = cap; C.capped = false; C.guess0 = NONE;
    St w = OL.st[si]; for (int t = 0; t < P; t++) w.Z[t] = NONE;
    vector<uint8_t> cols(P, 255);
    if (noV) {
      int s = 0;
      if (j < J[s]) { for (int c0 = 0; c0 <= 2 * b - 2; c0++) { C.guess0 = c0; walk(C, 0, 0, c0, w, cols); } }
      else { C.guess0 = NONE; walk(C, 0, 0, NONE, w, cols); }
    } else nextseg(C, 0, w, cols);
    if (C.capped) return false;
  }
  return true;
}
// returns 1 feasible, 0 infeasible, -1 capped.  If wit, fills Cout.
int solve_instance(int m0, bool wit, long cap, vector<vector<int>>* Cout, vector<size_t>* sizes) {
  if (!setup_instance(m0)) return 0;
  vector<Layer> layers; layers.reserve(Jall + 1);
  layers.emplace_back(); layers[0].st.push_back(start_state()); layers[0].par.push_back(0);
  if (wit) layers[0].cols.push_back(vector<uint8_t>(P, 255));
  for (int j = 0; j < Jall; j++) {
    layers.emplace_back();
    if (!run_layer(j, layers[j], layers.back(), wit, cap)) { if (sizes) sizes->clear(); return -1; }
    if (sizes) sizes->push_back(layers.back().st.size());
    if (layers.back().st.empty()) return 0;
  }
  if (wit && Cout) {
    vector<vector<uint8_t>> colsByLayer(Jall);
    uint32_t id = 0;
    for (int j = Jall; j >= 1; j--) { colsByLayer[j - 1] = layers[j].cols[id]; id = layers[j].par[id]; }
    Cout->assign(P, vector<int>());
    for (int t = 0; t < P; t++) {
      vector<int> half(J[t]);
      for (int j = 0; j < J[t]; j++) half[j] = colsByLayer[j][t];
      vector<int> arr(m[t]);
      for (int j = 0; j < J[t]; j++) { arr[j] = half[j]; arr[m[t] - 1 - j] = half[j]; }
      (*Cout)[t] = arr;
    }
  }
  return 1;
}
// Detect the eventual period of the mid-layer frontier sets (valid for all long C): returns false if not found within JGEN layers.
// On success: jstar = first layer of the periodic regime, per = period (layers).
bool detect_period(int JGEN, long cap, int& jstar, int& per, vector<size_t>* sizes) {
  int Mbig = 2 * (JGEN + 2 * P + 8);
  // need m_t >= 1 everywhere and returning; shift guaranteed by large m0
  if (!setup_instance(Mbig)) return false;
  vector<vector<K128>> sets;   // sorted key sets per layer
  Layer cur; cur.st.push_back(start_state()); cur.par.push_back(0);
  auto keys = [&](Layer& L) { vector<K128> k; for (auto& s : L.st) k.push_back(pack(s)); sort(k.begin(), k.end()); return k; };
  sets.push_back(keys(cur));
  for (int j = 0; j < JGEN; j++) {
    Layer nxt;
    if (!run_layer(j, cur, nxt, false, cap)) return false;
    if (sizes) sizes->push_back(nxt.st.size());
    if (nxt.st.empty()) { jstar = j + 1; per = 1; return true; }   // dies: infeasible for all long C
    vector<K128> k = keys(nxt);
    for (int j1 = (int)sets.size() - 1; j1 >= 0; j1--) if (sets[j1] == k && j1 >= 1) { jstar = j1; per = (int)sets.size() - j1; return true; }
    sets.push_back(k);
    cur = std::move(nxt);
  }
  return false;
}
int main(int argc, char** argv) {
  if (argc < 6) { fprintf(stderr, "usage: cauto b e g m0lo m0hi [-v pat|-vall] [-allm] [-w] [-part i n] [-cap N] [-sz]\n"); return 1; }
  b = atoi(argv[1]); string es = argv[2], gs = argv[3]; int m0lo = atoi(argv[4]), m0hi = atoi(argv[5]);
  P = es.size(); e.resize(P); g.resize(P); for (int t = 0; t < P; t++) { e[t] = es[t] - '0'; g[t] = gs[t] - '0'; }
  string vpat; bool vall = false, wit = false, showsz = false, allm = false; int part = 0, nparts = 1; long cap = 4000000;
  for (int i = 6; i < argc; i++) {
    string a = argv[i];
    if (a == "-v") vpat = argv[++i]; else if (a == "-vall") vall = true; else if (a == "-w") wit = true;
    else if (a == "-part") { part = atoi(argv[++i]); nparts = atoi(argv[++i]); } else if (a == "-cap") cap = atol(argv[++i]);
    else if (a == "-sz") showsz = true; else if (a == "-allm") allm = true;
  }
  int G = 0; for (int t = 0; t < P; t++) G += g[t];
  if (G % 2) { fprintf(stderr, "sum(g) must be even (repeat the stream)\n"); return 1; }
  vector<string> pats;
  if (!vpat.empty()) pats.push_back(vpat);
  else if (vall) {
    int K = G / 2;
    vector<int> idx(K); for (int i = 0; i < K; i++) idx[i] = i;
    if (K == 0) pats.push_back(string(P, '0'));
    else while (true) {
      string p(P, '0'); for (int i : idx) p[i] = '1'; pats.push_back(p);
      int i = K - 1; while (i >= 0 && idx[i] == P - K + i) i--;
      if (i < 0) break; idx[i]++; for (int q = i + 1; q < K; q++) idx[q] = idx[q - 1] + 1;
    }
  } else { fprintf(stderr, "need -v or -vall\n"); return 1; }
  long count = 0; long ninst = 0, ncap = 0;
  auto report = [&](const string& pat, int m0, int r, vector<vector<int>>& Cw, const char* tag) {
    if (r == -1) { ncap++; printf("CAPPED b=%d e=%s g=%s v=%s m0=%d\n", b, es.c_str(), gs.c_str(), pat.c_str(), m0); fflush(stdout); }
    if (r == 1) {
      count++;
      printf("%s b=%d e=%s g=%s v=%s m0=%d", tag, b, es.c_str(), gs.c_str(), pat.c_str(), m0);
      if (wit) { for (int t = 0; t < P; t++) { printf(" C%d=[", t); for (size_t i = 0; i < Cw[t].size(); i++) printf("%d%s", Cw[t][i], i + 1 < Cw[t].size() ? "," : ""); printf("]"); } }
      printf("\n"); fflush(stdout);
    }
  };
  for (size_t pi = 0; pi < pats.size(); pi++) {
    if ((long)(pi % nparts) != part) continue;
    v.assign(P, 0); for (int t = 0; t < P; t++) v[t] = pats[pi][t] - '0';
    if (allm) {
      // exhaustive for short C (m0 < mlo), then period-reduced decision for ALL longer C
      int jstar = 0, per = 0; vector<size_t> gsz;
      bool okp = detect_period(120, cap, jstar, per, &gsz);
      if (showsz) { fprintf(stderr, "detect sizes:"); for (size_t x : gsz) fprintf(stderr, " %zu", x); fprintf(stderr, "\n"); }
      if (!okp) { printf("NOPERIOD b=%d e=%s g=%s v=%s (frontier not periodic within 120 layers or capped)\n", b, es.c_str(), gs.c_str(), pats[pi].c_str()); fflush(stdout); ncap++; continue; }
      // smallest m0 whose first closing layer is >= jstar
      int mlo = 1;
      for (int mm = 1; mm < 100000; mm++) { if (!setup_instance(mm)) continue; int j0 = *min_element(J.begin(), J.end()) - 1; if (j0 >= jstar && mm > 2 * P) { mlo = mm; break; } }
      // small ones
      for (int m0 = 1; m0 < mlo; m0++) {
        vector<vector<int>> Cw; vector<size_t> sz; ninst++;
        int r = solve_instance(m0, wit, cap, &Cw, &sz); report(pats[pi], m0, r, Cw, "FEASIBLE");
      }
      // representatives of each class mod 2*per
      int nclass = 0, nfeasc = 0;
      for (int m0 = mlo; m0 < mlo + 2 * per; m0++) {
        vector<vector<int>> Cw; vector<size_t> sz; ninst++;
        if (!setup_instance(m0)) continue;
        nclass++;
        int r = solve_instance(m0, wit, cap, &Cw, &sz);
        if (r == 1) nfeasc++;
        report(pats[pi], m0, r, Cw, "FEASIBLE_CLASS");   // feasible for m0 + 2*per*k, all k >= 0
      }
      fprintf(stderr, "allm v=%s jstar=%d period=%d mlo=%d classes=%d feasible_classes=%d\n", pats[pi].c_str(), jstar, per, mlo, nclass, nfeasc);
      continue;
    }
    for (int m0 = m0lo; m0 <= m0hi; m0++) {
      vector<vector<int>> Cw; vector<size_t> sz;
      ninst++;
      int r = solve_instance(m0, wit, cap, &Cw, &sz);
      if (showsz) { printf("sizes m0=%d r=%d:", m0, r); for (size_t x : sz) printf(" %zu", x); printf("\n"); }
      report(pats[pi], m0, r, Cw, "FEASIBLE");
    }
  }
  fprintf(stderr, "cauto b=%d e=%s g=%s: instances %ld feasible %ld capped/noperiod %ld\n", b, es.c_str(), gs.c_str(), ninst, count, ncap);
  return 0;
}
