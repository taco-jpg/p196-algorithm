// cauto_fast: faster, answer-identical replacement for structure/cauto.cpp (exact layer automaton for the C-system).
//
// Same model, same command line, same FEASIBLE / FEASIBLE_CLASS / CAPPED / NOPERIOD lines.  What changed (all exact):
//  1. Segment factorisation.  A layer step only couples the time steps inside one "segment" (the times between two trim steps);
//     segments interact only through the guess c0 of the next segment, which becomes the Z entry at the end of the previous
//     segment.  A global state is therefore a tuple of small segment-local ids, and the successor set of a state is the
//     product of per-segment successor lists, which are computed once per distinct local input and cached.
//  2. Shared prefix.  For every C length m0 the first j0 = min_t J[t]-1 layers are the SAME generic layers (they do not
//     depend on m0).  The frontier F_j of the generic run is computed once per pattern; an instance m0 only needs its
//     short tail (layers j0..Jall-1) started from F_{j0}.  Once the generic frontier is periodic (jstar, per) the tail depends
//     only on (m0 mod 2, index of F_{j0} mod the period), so every tail is computed once and memoised.
//  3. Compact hashing (open addressing on tuples of 32-bit ids), no witness storage unless a hit has to be printed
//     (hits are re-solved with the original slow code so that the witness lines are exactly the old ones).
//  4. New options: -patterns FILE, -skip FILE, -sym (one trim pattern per shift orbit), per-pattern DONE line with the index.
//
// usage: cauto_fast b e g m0lo m0hi [-v pattern | -vall] [-allm] [-w] [-part i n] [-cap N] [-sz]
//                   [-patterns FILE] [-skip FILE] [-sym] [-legacy] [-q]
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <map>
#include <set>
#include <algorithm>
#include <chrono>
#include <fstream>
#include <sstream>
#include <memory>
#include <sys/resource.h>
using namespace std;
typedef unsigned __int128 K128;

// ============================================================================================================
// LEGACY CODE (the original cauto.cpp; only change: the packed key is 256 bits wide so that it never truncates)
// ============================================================================================================
struct LKey { K128 lo, hi; bool operator==(const LKey& o) const { return lo == o.lo && hi == o.hi; } };
struct LKH { size_t operator()(const LKey& kk) const {
  uint64_t a = (uint64_t)kk.lo, c = (uint64_t)(kk.lo >> 64), d = (uint64_t)kk.hi, f = (uint64_t)(kk.hi >> 64);
  return (size_t)((a * 0x9E3779B97F4A7C15ULL) ^ (c * 0xC2B2AE3D27D4EB4FULL) ^ (a >> 29) ^ (d * 0x165667B19E3779F9ULL) ^ (f * 0x27D4EB2F165667C5ULL) ^ (d >> 31)); } };
const int MAXP = 32;
const int NONE = -1;
struct St { int8_t l[MAXP], r[MAXP], Rd[MAXP], Z[MAXP]; };
int b, P;
vector<int> e, g, v;
vector<int> m, J, Jp, yd;
vector<vector<int>> order; int nseg;
int Jall;
bool noV;
static inline int nx(int t) { return (t + 1) % P; }
static inline void putbits(LKey& k, int& sh, uint64_t val, int w) {
  K128 x = (K128)val;
  if (sh >= 128) k.hi |= x << (sh - 128);
  else { k.lo |= x << sh; if (sh + w > 128) k.hi |= x >> (128 - sh); }
  sh += w;
}
LKey pack(const St& s) {
  LKey k; k.lo = 0; k.hi = 0; int sh = 0;
  for (int t = 0; t < P; t++) putbits(k, sh, s.l[t] & 1, 1);
  for (int t = 0; t < P; t++) putbits(k, sh, s.r[t] & 1, 1);
  for (int t = 0; t < P; t++) if (g[t]) putbits(k, sh, (uint8_t)(s.Rd[t] + 1), 6);
  for (int t = 0; t < P; t++) if (v[t]) putbits(k, sh, (uint8_t)(s.Z[t] + 1), 7);
  return k;
}
struct Layer { vector<St> st; vector<uint32_t> par; vector<vector<uint8_t>> cols; unordered_map<LKey, uint32_t, LKH> idx; };
struct Ctx { int j; const St* S; Layer* out; uint32_t parent; bool wit; long cap; bool capped; int guess0; };
void emit(Ctx& C, const St& w, const vector<uint8_t>& cols) {
  LKey k = pack(w);
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
    if (!wit && j >= 1) { layers[j - 1] = Layer(); }   // free memory (no witness needed)
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
bool detect_period_legacy(int JGEN, long cap, int& jstar, int& per, vector<size_t>* sizes) {
  int Mbig = 2 * (JGEN + 2 * P + 8);
  if (!setup_instance(Mbig)) return false;
  vector<vector<LKey>> sets;
  Layer cur; cur.st.push_back(start_state()); cur.par.push_back(0);
  auto keys = [&](Layer& L) { vector<LKey> k; for (auto& s : L.st) k.push_back(pack(s)); sort(k.begin(), k.end(), [](const LKey& a, const LKey& c) { return a.hi != c.hi ? a.hi < c.hi : a.lo < c.lo; }); return k; };
  sets.push_back(keys(cur));
  for (int j = 0; j < JGEN; j++) {
    Layer nxt;
    if (!run_layer(j, cur, nxt, false, cap)) return false;
    if (sizes) sizes->push_back(nxt.st.size());
    if (nxt.st.empty()) { jstar = j + 1; per = 1; return true; }
    vector<LKey> k = keys(nxt);
    for (int j1 = (int)sets.size() - 1; j1 >= 0; j1--) if (sets[j1] == k && j1 >= 1) { jstar = j1; per = (int)sets.size() - j1; return true; }
    sets.push_back(k);
    cur = std::move(nxt);
  }
  return false;
}

// ============================================================================================================
// FAST PATH
// ============================================================================================================
const int MAXNS = 16, MAXL = 32;
enum { T_GEN = 0, T_LODD = 1, T_LEVEN = 2, T_INP = 3, T_INZ = 4 };
struct OutE { uint32_t yid; int8_t c; };
struct Ent { uint32_t start, cnt; };
const uint32_t UNSET = 0xFFFFFFFFu;
struct SigTab { vector<uint8_t> types; bool j0; vector<Ent> ent; };
struct SegState {
  vector<int> times;
  unordered_map<string, uint32_t> yidMap; vector<string> cfg;     // local configuration (l,r,Rd per time) -> yid
  vector<int32_t> lidOf;                                          // yid*ZW + (z+1) -> lid
  vector<pair<uint32_t, int8_t>> lidInfo;                         // lid -> (yid, z)
  vector<OutE> pool; vector<uint8_t> colpool;   // colpool: L bytes (the columns c_t of the walk, 255 = inactive) per pool entry
  map<string, int> sigMap; vector<unique_ptr<SigTab>> sigs;
};
struct StateSet {
  int NS = 1; vector<uint32_t> data; vector<uint32_t> slots; size_t n = 0, mask = 0;
  void init(int ns, size_t expect = 1024) { NS = ns; data.clear(); n = 0; size_t sz = 1024; while (sz < expect * 2) sz <<= 1; slots.assign(sz, 0); mask = sz - 1; }
  static inline uint64_t hsh(const uint32_t* w, int NS) { uint64_t h = 0x9E3779B97F4A7C15ULL; for (int s = 0; s < NS; s++) { h ^= w[s]; h *= 0xff51afd7ed558ccdULL; h ^= h >> 32; } return h; }
  void grow() {
    size_t sz = slots.size() * 2; slots.assign(sz, 0); mask = sz - 1;
    for (size_t i = 0; i < n; i++) { uint64_t h = hsh(&data[i * NS], NS); size_t p = h & mask; while (slots[p]) p = (p + 1) & mask; slots[p] = (uint32_t)(i + 1); }
  }
  inline bool insert(const uint32_t* w) {
    uint64_t h = hsh(w, NS); size_t p = h & mask;
    while (true) {
      uint32_t s = slots[p];
      if (!s) break;
      if (memcmp(&data[(size_t)(s - 1) * NS], w, 4 * NS) == 0) return false;
      p = (p + 1) & mask;
    }
    slots[p] = (uint32_t)(n + 1); data.insert(data.end(), w, w + NS); n++;
    if (n * 2 > slots.size()) grow();
    return true;
  }
};
static inline uint64_t mix64(uint64_t x) { x += 0x9E3779B97F4A7C15ULL; x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ULL; x = (x ^ (x >> 27)) * 0x94D049BB133111EBULL; return x ^ (x >> 31); }

struct Fast {
  int NS, ZW;
  vector<SegState> sg;
  long cap;
  size_t maxStates = 0;      // largest frontier seen
  // generic frontiers
  vector<vector<uint32_t>> gen; vector<uint64_t> genFp; vector<size_t> genSize;
  Fast(long cap_) : cap(cap_) {}
  // ---- interning ----
  uint32_t internCfg(int s, const string& c) {
    SegState& S = sg[s]; auto it = S.yidMap.find(c);
    if (it != S.yidMap.end()) return it->second;
    uint32_t id = S.cfg.size(); S.cfg.push_back(c); S.yidMap.emplace(c, id); return id;
  }
  inline uint32_t getLid(int s, uint32_t yid, int z) {
    SegState& S = sg[s]; size_t ix = (size_t)yid * ZW + (z + 1);
    if (ix >= S.lidOf.size()) S.lidOf.resize(max(ix + 1, S.lidOf.size() * 2), -1);
    int32_t l = S.lidOf[ix];
    if (l < 0) { l = S.lidInfo.size(); S.lidInfo.push_back({yid, (int8_t)z}); S.lidOf[ix] = l; }
    return (uint32_t)l;
  }
  void init(const vector<vector<int>>& ord) {
    NS = ord.size(); ZW = 2 * b; sg.clear(); sg.resize(NS);
    for (int s = 0; s < NS; s++) sg[s].times = ord[s];
  }
  vector<uint32_t> startState() {
    vector<uint32_t> w(NS);
    for (int s = 0; s < NS; s++) {
      string c; for (int t : sg[s].times) { c.push_back((char)e[t]); c.push_back((char)(1 - e[t])); c.push_back((char)((g[t] ? (b - 1) * e[t] : NONE) + 1)); }
      w[s] = getLid(s, internCfg(s, c), NONE);
    }
    return w;
  }
  // ---- signatures ----
  SigTab* sigFor(int s, int j, bool generic) {
    SegState& S = sg[s]; const vector<int>& ts = S.times; string key; key.push_back(j == 0 ? 1 : 0);
    for (int t : ts) {
      int ty;
      if (generic) ty = T_GEN;
      else if (j < J[t] - 1) ty = T_GEN;
      else if (j == J[t] - 1) ty = (m[t] % 2) ? T_LODD : T_LEVEN;
      else ty = (j < Jp[t]) ? T_INP : T_INZ;
      key.push_back((char)ty);
    }
    auto it = S.sigMap.find(key);
    if (it != S.sigMap.end()) return S.sigs[it->second].get();
    unique_ptr<SigTab> st(new SigTab()); st->j0 = (j == 0); for (size_t k = 0; k < ts.size(); k++) st->types.push_back((uint8_t)key[k + 1]);
    S.sigMap[key] = S.sigs.size(); S.sigs.push_back(std::move(st)); return S.sigs.back().get();
  }
  // ---- local walk (one segment) ----
  struct WC {
    int s; const SigTab* sig; int8_t ol[MAXL], orr[MAXL], oRd[MAXL]; int z; int c0;
    map<pair<string, int>, string>* res; int8_t cc[MAXL];
  };
  void lwalk(WC& X, int k, int c, int8_t* nl, int8_t* nr, int8_t* nRd) {
    const vector<int>& ts = sg[X.s].times; int L = ts.size(); int t = ts[k]; int ty = X.sig->types[k];
    struct Out { int rin, Rj, lout, cp; } outs[2]; int no = 0;
    if (ty <= T_LEVEN) {
      int lin = X.ol[k]; int sm = c + lin; int Ld = sm % b; int lout = sm / b; int rreq = X.orr[k];
      int rp = X.sig->j0 ? yd[t] : X.oRd[k];
      if (ty == T_LODD) {
        if (lout != rreq) return;
        int cp = g[t] == 0 ? 2 * Ld : Ld + rp; outs[no++] = {-1, Ld, lout, cp};
      } else if (ty == T_LEVEN) {
        int rin = lout; if ((c + rin) / b != rreq) return;
        int Rj = (c + rin) % b; int cp = g[t] == 0 ? Ld + Rj : Ld + rp; outs[no++] = {rin, Rj, lout, cp};
      } else {
        for (int rin = 0; rin < 2; rin++) if ((c + rin) / b == rreq) {
          int Rj = (c + rin) % b; int cp = g[t] == 0 ? Ld + Rj : Ld + rp; outs[no++] = {rin, Rj, lout, cp};
        }
      }
    } else {
      if (ty == T_INP) outs[no++] = {-1, -1, -1, 2 * X.oRd[k]};
      else outs[no++] = {-1, -1, -1, NONE};
    }
    for (int oi = 0; oi < no; oi++) {
      Out o = outs[oi]; int8_t sl = nl[k], sr = nr[k], sR = nRd[k];
      X.cc[k] = (ty <= T_LEVEN) ? (int8_t)c : (int8_t)-1;
      if (ty <= T_LEVEN) { nl[k] = o.lout; if (o.rin >= 0) nr[k] = o.rin; if (g[t]) nRd[k] = o.Rj; }
      if (v[t] == 0) {
        if (!(o.cp != NONE && o.cp > 2 * b - 2) && k + 1 < L) lwalk(X, k + 1, o.cp, nl, nr, nRd);
      } else {
        bool ok = true;
        if (o.cp != NONE) { if (X.sig->j0) { if (o.cp != b - 1) ok = false; } else if (X.z != o.cp) ok = false; }
        else { if (!X.sig->j0 && X.z != NONE) ok = false; }
        if (ok) {
          string cfg; for (int q = 0; q < L; q++) { cfg.push_back((char)nl[q]); cfg.push_back((char)nr[q]); cfg.push_back((char)(nRd[q] + 1)); }
          string cs; for (int q = 0; q < L; q++) cs.push_back((char)X.cc[q]);
          X.res->emplace(make_pair(cfg, X.c0), cs);
        }
      }
      nl[k] = sl; nr[k] = sr; nRd[k] = sR;
    }
  }
  void fill(int s, SigTab* sig, uint32_t lid) {
    SegState& S = sg[s]; uint32_t yid = S.lidInfo[lid].first; int z = S.lidInfo[lid].second;
    const string cfg = S.cfg[yid]; int L = S.times.size();
    WC X; X.s = s; X.sig = sig; X.z = z;
    for (int q = 0; q < L; q++) { X.ol[q] = (int8_t)cfg[3 * q]; X.orr[q] = (int8_t)cfg[3 * q + 1]; X.oRd[q] = (int8_t)((int)(uint8_t)cfg[3 * q + 2] - 1); }
    map<pair<string, int>, string> res; X.res = &res;
    bool active0 = sig->types[0] <= T_LEVEN;
    int8_t nl[MAXL], nr[MAXL], nRd[MAXL];
    auto start = [&](int c0) { memcpy(nl, X.ol, L); memcpy(nr, X.orr, L); memcpy(nRd, X.oRd, L); X.c0 = c0; lwalk(X, 0, c0, nl, nr, nRd); };
    if (active0) { for (int c0 = 0; c0 <= 2 * b - 2; c0++) start(c0); } else start(NONE);
    vector<OutE> outs; vector<string> colv;
    for (auto& pr : res) { outs.push_back({internCfg(s, pr.first.first), (int8_t)pr.first.second}); colv.push_back(pr.second); }   // map order: deterministic
    // `S` may have been invalidated? (sg is not resized during fill) -- re-fetch references anyway
    SegState& S2 = sg[s];
    Ent en; en.start = S2.pool.size(); en.cnt = outs.size();
    for (size_t q = 0; q < outs.size(); q++) { S2.pool.push_back(outs[q]); S2.colpool.insert(S2.colpool.end(), colv[q].begin(), colv[q].end()); }
    if (sig->ent.size() <= lid) sig->ent.resize(S2.lidInfo.size() + 64, Ent{UNSET, 0});
    sig->ent[lid] = en;
  }
  // ---- one layer ----
  // returns false if capped.  Fin/Fout are flat tuples.  generic: types all T_GEN (detect run); otherwise use J/Jp/m.
  bool step(const vector<uint32_t>& Fin, int j, bool generic, StateSet& out, vector<uint32_t>* par = nullptr, vector<uint16_t>* ch = nullptr) {
    SigTab* sig[MAXNS];
    for (int s = 0; s < NS; s++) sig[s] = sigFor(s, j, generic);
    out.init(NS, Fin.size() / NS + 16);
    size_t n = Fin.size() / NS;
    const OutE* lst[MAXNS]; uint32_t cnt[MAXNS];
    for (size_t i = 0; i < n; i++) {
      const uint32_t* w = &Fin[i * NS]; bool dead = false;
      for (int s = 0; s < NS; s++) {
        SigTab* sg_ = sig[s];
        if (w[s] >= sg_->ent.size() || sg_->ent[w[s]].start == UNSET) fill(s, sg_, w[s]);
        const Ent& en = sg_->ent[w[s]];
        if (en.cnt == 0) { dead = true; break; }
        cnt[s] = en.cnt; lst[s] = nullptr; cnt[s] = en.cnt;
        lst[s] = &sg[s].pool[en.start];
      }
      if (dead) continue;
      uint32_t idx[MAXNS]; for (int s = 0; s < NS; s++) idx[s] = 0;
      uint32_t nw[MAXNS];
      while (true) {
        for (int s = 0; s < NS; s++) { int sn = (s + 1 == NS) ? 0 : s + 1; nw[s] = getLid(s, lst[s][idx[s]].yid, lst[sn][idx[sn]].c); }
        if (out.insert(nw) && par) { par->push_back((uint32_t)i); for (int s2 = 0; s2 < NS; s2++) ch->push_back((uint16_t)idx[s2]); }
        int s = NS - 1; while (s >= 0 && ++idx[s] == cnt[s]) { idx[s] = 0; s--; }
        if (s < 0) break;
      }
      if ((long)out.n > cap) return false;
    }
    if (out.n > maxStates) maxStates = out.n;
    return true;
  }
  static uint64_t fingerprint(const vector<uint32_t>& F, int NS) {
    uint64_t f = 0; size_t n = F.size() / NS;
    for (size_t i = 0; i < n; i++) { uint64_t h = 0x1234567; for (int s = 0; s < NS; s++) h = mix64(h ^ F[i * NS + s]); f += h; }
    return f;
  }
  static bool sameSet(const vector<uint32_t>& A, const vector<uint32_t>& B, int NS) {
    if (A.size() != B.size()) return false;
    size_t n = A.size() / NS;
    auto sorted = [&](const vector<uint32_t>& F) {
      vector<uint32_t> ord(n); for (size_t i = 0; i < n; i++) ord[i] = i;
      sort(ord.begin(), ord.end(), [&](uint32_t x, uint32_t y) { return memcmp(&F[(size_t)x * NS], &F[(size_t)y * NS], 4 * NS) < 0 ? true : false; });
      vector<uint32_t> o; o.reserve(F.size()); for (size_t i = 0; i < n; i++) o.insert(o.end(), &F[(size_t)ord[i] * NS], &F[(size_t)ord[i] * NS] + NS); return o; };
    return sorted(A) == sorted(B);
  }
  // generic run with period detection (mirrors detect_period).  Fills gen[0..jstar+per-1] (and gen[jstar]=empty on death).
  bool detect(int JGEN, int& jstar, int& per, vector<size_t>* sizes) {
    gen.clear(); genFp.clear(); genSize.clear();
    gen.push_back(startState()); genFp.push_back(fingerprint(gen[0], NS)); genSize.push_back(1);
    for (int j = 0; j < JGEN; j++) {
      StateSet out;
      if (!step(gen.back(), j, true, out)) return false;
      if (sizes) sizes->push_back(out.n);
      if (out.n == 0) { jstar = j + 1; per = 1; gen.push_back(vector<uint32_t>()); genFp.push_back(0); genSize.push_back(0); return true; }
      uint64_t fp = fingerprint(out.data, NS);
      for (int j1 = (int)gen.size() - 1; j1 >= 1; j1--)
        if (genSize[j1] == out.n && genFp[j1] == fp && sameSet(gen[j1], out.data, NS)) { jstar = j1; per = (int)gen.size() - j1; return true; }
      genSize.push_back(out.n); genFp.push_back(fp); gen.push_back(std::move(out.data));
    }
    return false;
  }
};

// -------- helpers shared by the two paths --------
bool g_wit = false, g_sz = false, g_wlegacy = false;
long g_cap = 4000000;
string es_, gs_;
double nowsec() { return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }
long rss_mb() { struct rusage ru; getrusage(RUSAGE_SELF, &ru);
#ifdef __APPLE__
  return ru.ru_maxrss / 1048576;   // bytes on macOS
#else
  return ru.ru_maxrss / 1024;      // kilobytes on Linux
#endif
}

long g_count = 0, g_ninst = 0, g_ncap = 0;
void report(const string& pat, int m0, int r, vector<vector<int>>& Cw, const char* tag) {
  if (r == -1) { g_ncap++; printf("CAPPED b=%d e=%s g=%s v=%s m0=%d\n", b, es_.c_str(), gs_.c_str(), pat.c_str(), m0); fflush(stdout); }
  if (r == 1) {
    g_count++;
    printf("%s b=%d e=%s g=%s v=%s m0=%d", tag, b, es_.c_str(), gs_.c_str(), pat.c_str(), m0);
    if (g_wit && !Cw.empty()) { for (int t = 0; t < P; t++) { printf(" C%d=[", t); for (size_t i = 0; i < Cw[t].size(); i++) printf("%d%s", Cw[t][i], i + 1 < Cw[t].size() ? "," : ""); printf("]"); } }
    printf("\n"); fflush(stdout);
  }
}

// Decision for one instance using the shared generic prefix.  F.gen[...] must be valid (see allm_fast).
struct AllmCtx { Fast* F; int jstar, per; map<pair<int,int>, int> memo; int ntails = 0; };
int decide(AllmCtx& A, int m0) {
  if (!setup_instance(m0)) return 0;
  int j0 = *min_element(J.begin(), J.end()) - 1;
  int idx = j0 < A.jstar ? j0 : A.jstar + (j0 - A.jstar) % A.per;
  pair<int,int> key = {m0 & 1, idx};
  auto it = A.memo.find(key); if (it != A.memo.end()) return it->second;
  A.ntails++;
  Fast& F = *A.F;
  vector<uint32_t> cur = F.gen[idx];
  int result = 1;
  if (cur.empty()) result = 0;
  else for (int j = j0; j < Jall; j++) {
    StateSet out;
    if (!F.step(cur, j, false, out)) { result = -1; break; }
    if (out.n == 0) { result = 0; break; }
    cur = std::move(out.data);
  }
  A.memo[key] = result; return result;
}


// ---- independent check of a witness: C_{t+1} = trim_{v_t}(pairsum(DC_t [+ y])), carry(C_t,e_t) = 1-e_t, cyclic ----
bool cstep_forced(const vector<int>& C, int e1, int gg, int vv, vector<int>& out) {
  int m_ = C.size(); vector<int> DC(m_); int c = e1;
  for (int i = 0; i < m_; i++) { int x = C[i] + c; DC[i] = x % b; c = x / b; }
  if (c != 1 - e1) return false;
  int ydv = (b - 1) * e1; vector<int> cp;
  if (gg == 0) { cp.resize(m_); for (int k = 0; k < m_; k++) cp[k] = DC[k] + DC[m_ - 1 - k]; }
  else { vector<int> W(DC); W.push_back(ydv); cp.resize(m_ + 1); for (int k = 0; k <= m_; k++) cp[k] = W[k] + W[m_ - k]; }
  int n = cp.size(); if (n - 2 * vv < 1) return false;
  for (int i = 0; i < vv; i++) if (cp[i] != b - 1 || cp[n - 1 - i] != b - 1) return false;
  out.assign(cp.begin() + vv, cp.end() - vv); return true;
}
bool verify_cycle(const vector<vector<int>>& Cw) {
  if ((int)Cw.size() != P) return false;
  for (int t = 0; t < P; t++) {
    const vector<int>& C = Cw[t]; int n = C.size();
    for (int i = 0; i < n; i++) if (C[i] != C[n - 1 - i] || C[i] < 0 || C[i] > 2 * b - 2) return false;
    vector<int> nx_; if (!cstep_forced(C, e[t], g[t], v[t], nx_)) return false;
    if (nx_ != Cw[(t + 1) % P]) return false;
  }
  return true;
}
// fast witness for a feasible instance: forward pass storing parents and choices, then backtrack (state 0 of the last layer)
int witness_fast(Fast& F, int m0, vector<vector<int>>& Cout) {
  if (!setup_instance(m0)) return 0;
  struct WL { vector<uint32_t> data, parent; vector<uint16_t> choice; };
  vector<WL> L(Jall + 1); int NS = F.NS;
  L[0].data = F.startState();
  for (int j = 0; j < Jall; j++) {
    StateSet out;
    if (!F.step(L[j].data, j, false, out, &L[j + 1].parent, &L[j + 1].choice)) return -1;
    L[j + 1].data = std::move(out.data);
    if (L[j + 1].data.empty()) return 0;
  }
  vector<vector<uint8_t>> colsByLayer(Jall, vector<uint8_t>(P, 255));
  size_t idx = 0;
  for (int j = Jall - 1; j >= 0; j--) {
    uint32_t p = L[j + 1].parent[idx]; const uint32_t* w = &L[j].data[(size_t)p * NS];
    for (int s = 0; s < NS; s++) {
      SigTab* sig = F.sigFor(s, j, false); const Ent& en = sig->ent[w[s]];
      size_t oi = en.start + L[j + 1].choice[idx * NS + s]; int Ls = F.sg[s].times.size();
      for (int k = 0; k < Ls; k++) colsByLayer[j][F.sg[s].times[k]] = F.sg[s].colpool[oi * Ls + k];
    }
    idx = p;
  }
  Cout.assign(P, vector<int>());
  for (int t = 0; t < P; t++) {
    vector<int> half(J[t]); for (int j = 0; j < J[t]; j++) half[j] = colsByLayer[j][t];
    vector<int> arr(m[t]); for (int j = 0; j < J[t]; j++) { arr[j] = half[j]; arr[m[t] - 1 - j] = half[j]; }
    Cout[t] = arr;
  }
  return 1;
}
// witness for a feasible instance m0: fast path (verified), legacy fallback
void get_witness(Fast* F, int m0, vector<vector<int>>& Cw) {
  Cw.clear();
  if (!g_wlegacy && F) {
    int r = witness_fast(*F, m0, Cw);
    if (r == 1 && verify_cycle(Cw)) return;
    fprintf(stderr, "warning: fast witness failed (r=%d) for m0=%d, using legacy witness\n", r, m0); Cw.clear();
  }
  vector<size_t> sz; solve_instance(m0, true, g_cap, &Cw, &sz);
}

// ---- one pattern, -allm.  returns status: 0 none, 1 hit, 2 capped, 3 noperiod
struct PatInfo { int jstar = 0, per = 0, mlo = 0, nclass = 0, nfeasc = 0, ntails = 0; size_t maxStates = 0; };
int allm_pattern(const string& pat, PatInfo& PI, bool legacy) {
  v.assign(P, 0); for (int t = 0; t < P; t++) v[t] = pat[t] - '0';
  long cnt0 = g_count, cap0 = g_ncap;
  int K = 0; for (int t = 0; t < P; t++) K += v[t];
  bool fast = !legacy && K >= 1 && K <= MAXNS;
  int jstar = 0, per = 0; vector<size_t> gsz;
  unique_ptr<Fast> F; AllmCtx A; bool okp;
  if (fast) {
    Fast* f = new Fast(g_cap); F.reset(f);
    int Mbig = 2 * (120 + 2 * P + 8);
    if (!setup_instance(Mbig)) { okp = false; }
    else { f->init(order); okp = f->detect(120, jstar, per, &gsz); }
  } else okp = detect_period_legacy(120, g_cap, jstar, per, &gsz);
  if (g_sz) { fprintf(stderr, "detect sizes:"); for (size_t x : gsz) fprintf(stderr, " %zu", x); fprintf(stderr, "\n"); }
  if (!okp) {
    printf("NOPERIOD b=%d e=%s g=%s v=%s (frontier not periodic within 120 layers or capped)\n", b, es_.c_str(), gs_.c_str(), pat.c_str()); fflush(stdout);
    g_ncap++; if (F) PI.maxStates = F->maxStates; return 3;
  }
  PI.jstar = jstar; PI.per = per;
  if (fast) { A.F = F.get(); A.jstar = jstar; A.per = per; }
  int mlo = 1;
  for (int mm = 1; mm < 100000; mm++) { if (!setup_instance(mm)) continue; int j0 = *min_element(J.begin(), J.end()) - 1; if (j0 >= jstar && mm > 2 * P) { mlo = mm; break; } }
  PI.mlo = mlo;
  auto solve = [&](int m0, bool needW, vector<vector<int>>& Cw) -> int {
    if (!fast) { vector<size_t> sz; return solve_instance(m0, needW, g_cap, &Cw, &sz); }
    int r = decide(A, m0);
    if (r == 1 && g_wit) get_witness(F.get(), m0, Cw);
    return r;
  };
  for (int m0 = 1; m0 < mlo; m0++) {
    vector<vector<int>> Cw; g_ninst++;
    int r = solve(m0, g_wit, Cw); report(pat, m0, r, Cw, "FEASIBLE");
  }
  int nclass = 0, nfeasc = 0;
  for (int m0 = mlo; m0 < mlo + 2 * per; m0++) {
    vector<vector<int>> Cw; g_ninst++;
    if (!setup_instance(m0)) continue;
    nclass++;
    int r = solve(m0, g_wit, Cw);
    if (r == 1) nfeasc++;
    report(pat, m0, r, Cw, "FEASIBLE_CLASS");
  }
  fprintf(stderr, "allm v=%s jstar=%d period=%d mlo=%d classes=%d feasible_classes=%d\n", pat.c_str(), jstar, per, mlo, nclass, nfeasc);
  PI.nclass = nclass; PI.nfeasc = nfeasc; PI.ntails = A.ntails; if (F) PI.maxStates = F->maxStates;
  return g_count > cnt0 ? 1 : (g_ncap > cap0 ? 2 : 0);
}

// ---- one pattern, explicit m0 range (non -allm).  Fast version uses a running generic frontier. ----
void range_pattern(const string& pat, int m0lo, int m0hi, bool legacy) {
  v.assign(P, 0); for (int t = 0; t < P; t++) v[t] = pat[t] - '0';
  int K = 0; for (int t = 0; t < P; t++) K += v[t];
  bool fast = !legacy && K >= 1 && K <= MAXNS;
  if (!fast) {
    for (int m0 = m0lo; m0 <= m0hi; m0++) {
      vector<vector<int>> Cw; vector<size_t> sz; g_ninst++;
      int r = solve_instance(m0, g_wit, g_cap, &Cw, &sz);
      if (g_sz) { printf("sizes m0=%d r=%d:", m0, r); for (size_t x : sz) printf(" %zu", x); printf("\n"); }
      report(pat, m0, r, Cw, "FEASIBLE");
    }
    return;
  }
  Fast F(g_cap);
  int Mbig = 2 * (120 + 2 * P + 8);
  setup_instance(Mbig); F.init(order);
  vector<uint32_t> curG = F.startState(); int jcur = 0; vector<size_t> hist; bool genCapped = false; // hist[i] = size of F_{i+1}
  for (int m0 = m0lo; m0 <= m0hi; m0++) {
    g_ninst++;
    vector<size_t> sz; int r = 0;
    if (!setup_instance(m0)) { if (g_sz) printf("sizes m0=%d r=0:\n", m0); continue; }
    int j0 = *min_element(J.begin(), J.end()) - 1;
    if (j0 < jcur) { curG = F.startState(); jcur = 0; hist.clear(); genCapped = false; }
    bool died = false;
    while (jcur < j0 && !genCapped && !died) {
      StateSet out;
      if (!F.step(curG, jcur, true, out)) { genCapped = true; break; }
      hist.push_back(out.n); curG = std::move(out.data); jcur++;
      if (curG.empty()) died = true;
    }
    if (genCapped && jcur < j0) { r = -1; }
    else if (jcur == j0 || died) {
      for (int q = 0; q < min<int>(j0, hist.size()); q++) sz.push_back(hist[q]);
      if (curG.empty()) { r = 0; }
      else {
        vector<uint32_t> cur = curG; r = 1;
        for (int j = j0; j < Jall; j++) {
          StateSet out;
          if (!F.step(cur, j, false, out)) { r = -1; break; }
          sz.push_back(out.n);
          if (out.n == 0) { r = 0; break; }
          cur = std::move(out.data);
        }
      }
    }
    if (r == -1) sz.clear();
    vector<vector<int>> Cw;
    if (r == 1 && g_wit) get_witness(&F, m0, Cw);
    if (g_sz) { printf("sizes m0=%d r=%d:", m0, r); for (size_t x : sz) printf(" %zu", x); printf("\n"); }
    report(pat, m0, r, Cw, "FEASIBLE");
  }
}

// ---- pattern enumeration helpers ----
static long binom(int n, int k) { if (k < 0 || k > n) return 0; double r = 1; for (int i = 1; i <= k; i++) r = r * (n - k + i) / i; return (long)(r + 0.5); }
long rank_of(const string& p, int K) {   // lexicographic rank among K-subsets of positions (ascending)
  int n = p.size(); long rk = 0; int i = 0, prev = -1;
  for (int pos = 0; pos < n; pos++) if (p[pos] == '1') {
    for (int x = prev + 1; x < pos; x++) rk += binom(n - 1 - x, K - 1 - i);
    prev = pos; i++;
  }
  return rk;
}
string shifted(const string& p, int s) { int n = p.size(); string q(n, '0'); for (int t = 0; t < n; t++) q[(t + s) % n] = p[t]; return q; }

// parse a done/patterns file: returns sets of pattern strings (good) and bad (undecided) ones
void parse_file(const char* fn, int Pn, int K, vector<string>& allPats, set<string>& good, set<string>& bad) {
  ifstream f(fn); if (!f) { fprintf(stderr, "cannot open %s\n", fn); exit(1); }
  auto asPat = [&](const string& tok) -> string {
    if ((int)tok.size() == Pn && tok.find_first_not_of("01") == string::npos) { int c = count(tok.begin(), tok.end(), '1'); return c == K ? tok : ""; }
    return "";
  };
  string line;
  while (getline(f, line)) {
    while (!line.empty() && (line.back() == '\n' || line.back() == '\r')) line.pop_back();
    vector<string> toks; { size_t i = 0; while (i < line.size()) { while (i < line.size() && isspace((unsigned char)line[i])) i++; size_t j = i; while (j < line.size() && !isspace((unsigned char)line[j])) j++; if (j > i) toks.push_back(line.substr(i, j - i)); i = j; } }
    if (toks.empty()) continue;
    const string& first = toks[0];
    // lines that mean "this pattern is NOT finished / is a hit": rerun it
    bool isBad = (first == "CAPPED" || first == "NOPERIOD" || first == "FEASIBLE" || first == "FEASIBLE_CLASS");
    // lines that mean "this pattern is finished": old stderr 'allm v=...' and new 'DONE ... status=none|hit'
    bool isOk = (first == "allm" || first == "DONE");
    long idxv = -1; string patv;
    for (auto& tk : toks) {
      if (tk.compare(0, 2, "v=") == 0) { string p = asPat(tk.substr(2)); if (!p.empty()) patv = p; }
      else if (tk.compare(0, 4, "idx=") == 0) idxv = atol(tk.c_str() + 4);
      else if (tk.compare(0, 7, "status=") == 0 && tk.substr(7) != "none") { isOk = false; isBad = true; }
    }
    if (toks.size() == 1) {   // bare token: an index or a pattern string
      string p = asPat(first);
      if (!p.empty()) { good.insert(p); continue; }
      char* end; long x = strtol(first.c_str(), &end, 10);
      if (*end == 0 && x >= 0 && x < (long)allPats.size()) good.insert(allPats[x]);
      continue;
    }
    if (patv.empty() && idxv >= 0 && idxv < (long)allPats.size()) patv = allPats[idxv];
    if (patv.empty()) continue;
    // old/new "allm"/"DONE" line with feasible_classes>0 = a hit for all long C: never treat as done
    for (auto& tk : toks) if (tk.compare(0, 17, "feasible_classes=") == 0 && atol(tk.c_str() + 17) > 0) { isOk = false; isBad = true; }
    if (isBad) bad.insert(patv); else if (isOk) good.insert(patv);
  }
}

int main(int argc, char** argv) {
  if (argc < 6) { fprintf(stderr, "usage: cauto_fast b e g m0lo m0hi [-v pat|-vall] [-allm] [-w] [-part i n] [-cap N] [-sz] [-patterns FILE] [-skip FILE] [-sym] [-legacy] [-wlegacy]\n"); return 1; }
  b = atoi(argv[1]); string es = argv[2], gs = argv[3]; int m0lo = atoi(argv[4]), m0hi = atoi(argv[5]);
  es_ = es; gs_ = gs;
  if (b < 2 || b > 62) { fprintf(stderr, "base must be in 2..62\n"); return 1; }
  P = es.size(); if (P > MAXP || (int)gs.size() != P) { fprintf(stderr, "bad stream length (max %d)\n", MAXP); return 1; }
  e.resize(P); g.resize(P); for (int t = 0; t < P; t++) { e[t] = es[t] - '0'; g[t] = gs[t] - '0'; }
  string vpat, patFile, skipFile; bool vall = false, allm = false, sym = false, legacy = false; int part = 0, nparts = 1;
  for (int i = 6; i < argc; i++) {
    string a = argv[i];
    if (a == "-v") vpat = argv[++i]; else if (a == "-vall") vall = true; else if (a == "-w") g_wit = true;
    else if (a == "-part") { part = atoi(argv[++i]); nparts = atoi(argv[++i]); } else if (a == "-cap") g_cap = atol(argv[++i]);
    else if (a == "-sz") g_sz = true; else if (a == "-allm") allm = true;
    else if (a == "-patterns") patFile = argv[++i]; else if (a == "-skip") skipFile = argv[++i];
    else if (a == "-sym") sym = true; else if (a == "-legacy") legacy = true; else if (a == "-wlegacy") g_wlegacy = true;
    else if (a == "-q") {} else { fprintf(stderr, "unknown option %s\n", a.c_str()); return 1; }
  }
  int G = 0; for (int t = 0; t < P; t++) G += g[t];
  if (G % 2) { fprintf(stderr, "sum(g) must be even (repeat the stream)\n"); return 1; }
  int K = G / 2;
  vector<string> pats;
  if (!vpat.empty()) pats.push_back(vpat);
  else if (vall) {
    vector<int> idx(K); for (int i = 0; i < K; i++) idx[i] = i;
    if (K == 0) pats.push_back(string(P, '0'));
    else while (true) {
      string p(P, '0'); for (int i : idx) p[i] = '1'; pats.push_back(p);
      int i = K - 1; while (i >= 0 && idx[i] == P - K + i) i--;
      if (i < 0) break; idx[i]++; for (int q = i + 1; q < K; q++) idx[q] = idx[q - 1] + 1;
    }
  } else { fprintf(stderr, "need -v or -vall\n"); return 1; }
  // ---- selection: -patterns, -skip, -sym, then -part over the remaining list ----
  vector<long> sel;   // indices into pats
  {
    set<string> only; bool useOnly = !patFile.empty();
    if (useOnly) { set<string> bad; parse_file(patFile.c_str(), P, K, pats, only, bad); for (auto& s : bad) only.insert(s); }
    set<string> done, undecided;
    if (!skipFile.empty()) { parse_file(skipFile.c_str(), P, K, pats, done, undecided); for (auto& s : undecided) done.erase(s); }
    // symmetry group: shifts s with e,g invariant
    vector<int> shifts; if (sym) for (int s = 1; s < P; s++) { bool ok = true; for (int t = 0; t < P; t++) if (e[(t + s) % P] != e[t] || g[(t + s) % P] != g[t]) { ok = false; break; } if (ok) shifts.push_back(s); }
    long nsym = 0, nskip = 0;
    for (size_t pi = 0; pi < pats.size(); pi++) {
      const string& p = pats[pi];
      if (useOnly && !only.count(p)) continue;
      bool covered = done.count(p) > 0;
      bool isRep = true;
      if (sym && !shifts.empty() && K > 0) {
        long myr = (long)pi;
        for (int s : shifts) { string q = shifted(p, s); if (done.count(q)) covered = true; if (vpat.empty() && rank_of(q, K) < myr) isRep = false; }
      }
      if (!isRep) { nsym++; continue; }
      if (covered) { nskip++; continue; }
      sel.push_back(pi);
    }
    fprintf(stderr, "cauto_fast: %zu patterns total, %ld skipped as done, %ld skipped as shift-equivalent to a lower index, %zu to run\n", pats.size(), nskip, nsym, sel.size());
  }
  long orbitSize = 1;
  vector<int> shiftsAll; if (sym) for (int s = 1; s < P; s++) { bool ok = true; for (int t = 0; t < P; t++) if (e[(t + s) % P] != e[t] || g[(t + s) % P] != g[t]) { ok = false; break; } if (ok) shiftsAll.push_back(s); }
  (void)orbitSize;
  double T0 = nowsec();
  for (size_t qi = 0; qi < sel.size(); qi++) {
    if ((long)(qi % nparts) != part) continue;
    size_t pi0 = sel[qi]; const string& pat = pats[pi0];
    long pi = vpat.empty() ? (long)pi0 : (count(vpat.begin(), vpat.end(), '1') == K && (int)vpat.size() == P ? rank_of(vpat, K) : -1L);
    double t0 = nowsec();
    if (allm) {
      PatInfo PI; int st = allm_pattern(pat, PI, legacy);
      const char* sn = st == 0 ? "none" : st == 1 ? "hit" : st == 2 ? "capped" : "noperiod";
      int orb = 1; if (sym && !shiftsAll.empty()) { set<string> os; os.insert(pat); for (int s : shiftsAll) os.insert(shifted(pat, s)); orb = os.size(); }
      printf("DONE idx=%ld v=%s status=%s jstar=%d period=%d mlo=%d classes=%d feasible_classes=%d maxstates=%zu tails=%d orbit=%d sec=%.2f rssMB=%ld\n",
             pi, pat.c_str(), sn, PI.jstar, PI.per, PI.mlo, PI.nclass, PI.nfeasc, PI.maxStates, PI.ntails, orb, nowsec() - t0, rss_mb());
      fflush(stdout);
    } else {
      long cnt1 = g_count, cap1 = g_ncap;
      range_pattern(pat, m0lo, m0hi, legacy);
      printf("DONE idx=%ld v=%s status=%s sec=%.2f\n", pi, pat.c_str(), g_count > cnt1 ? "hit" : (g_ncap > cap1 ? "capped" : "none"), nowsec() - t0); fflush(stdout);
    }
  }
  fprintf(stderr, "cauto b=%d e=%s g=%s: instances %ld feasible %ld capped/noperiod %ld (%.1fs)\n", b, es.c_str(), gs.c_str(), g_ninst, g_count, g_ncap, nowsec() - T0);
  return 0;
}
