// khr.cpp (r13c): birth-rooted relative K-head towers (the "primitive part" filter of r13c).
//
// Setting: base b, clock pattern g (length P), d0 a multiple of P, L a multiple of d0.
// Interface of a d0-periodic head of height a: I = (c[t], xb[t], A[t], root), t in Z/d0:
//   c[t] = forward carry into column a, xb[t] = digit of column a-1 at gamma=1 phases (root: -1, part = 1),
//   A[t] = set of allowed backward carries H_a(t) (bitmask 1<<H), root = (a == 0) (column digits >= 1).
// A column v (time series) above I: edge (v,t) -> (y,t+1) with top bit h iff H = floor((v+h)/b) in A[t] and
//   y = (v + c[t]) mod b + (g_t ? (xb[t] + H) mod b [root: 1] : (v + h) mod b).
// Step 1 (-listif): BFS over interfaces from the root interface, adding d0-periodic columns (saturation = finite list IF(d0)).
// Step 2: for each interface, enumerate the closed L-columns v that are NOT d0-periodic (the possible "births"),
//   compute the L-periodic interface I' above v, and deduplicate the I'.
// Step 3: for each distinct I', run the relative K-head tower above v: nodes (window w_1..w_k, t mod L), root = I',
//   exact closed-L-walk pruning (trim, SCC, exact closure, exactset) as in r12b/r12e khx/khxt; "DIES at level k" means no
//   closed L-walk with k columns above v exists.  Theorem B of r13c: if all towers die, every infinite closed L-history of G(g)
//   is d0-periodic.
//
// Build: clang++ -std=c++17 -O3 -march=native -o bin/khr src/khr.cpp
#include <execinfo.h>
#include <csignal>
#include <unistd.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <algorithm>
#include <numeric>
#include <chrono>
#include <set>
#include <map>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <functional>
using namespace std;
typedef unsigned long long u64;

static int b = 10, NV = 19;
static double now() { return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }

// ---------- interfaces ----------
struct Iface { vector<int8_t> c, xb, A; bool root = false; };
static string keyOf(const Iface& I) {
  string s; s.reserve(I.c.size() * 3 + 1);
  for (size_t i = 0; i < I.c.size(); i++) { s.push_back(I.c[i]); s.push_back((char)(I.xb[i] + 2)); s.push_back(I.A[i]); }
  s.push_back(I.root ? 1 : 0); return s;
}
static vector<int> gpat; static int gP;
static inline int gAt(int t) { return gpat[t % gP]; }

// successors of (t, v) above interface I (phases of I modulo |I.c|): returns list of pairs (y, hmask)
static inline int colStep(const Iface& I, int t, int v, int* ys, int* hm) {
  int T = I.c.size(); int tt = t % T; int n = 0; int gg = gAt(t);
  for (int h = 0; h < 2; h++) {
    int H = (v + h) / b; if (!((I.A[tt] >> H) & 1)) continue;
    int part = gg ? (I.xb[tt] < 0 ? 1 : (I.xb[tt] + H) % b) : (v + h) % b;
    int y = (v + I.c[tt]) % b + part;
    if (I.root && y < 1) continue;
    int k; for (k = 0; k < n; k++) if (ys[k] == y) break;
    if (k == n) { ys[n] = y; hm[n] = 0; n++; }
    hm[k] |= 1 << h;
  }
  return n;
}
static inline int colHmask(const Iface& I, int t, int v, int y) {
  int ys[2], hm[2]; int n = colStep(I, t, v, ys, hm);
  for (int k = 0; k < n; k++) if (ys[k] == y) return hm[k];
  return 0;
}

// enumerate closed columns of period Lc above interface I (phases mod Lc); callback(col) for each
static void enumColumns(const Iface& I, int Lc, const function<void(const vector<int>&)>& emit, long long& count, long long limit) {
  // backward DP: R[t][v] = set of final digits reachable from (t,v) at time Lc (bitmask over 19 digits)
  static thread_local vector<vector<uint32_t>> R; R.assign(Lc + 1, vector<uint32_t>(NV, 0));
  for (int v = 0; v < NV; v++) R[Lc][v] = 1u << v;
  int ys[2], hm[2];
  for (int t = Lc - 1; t >= 0; t--) for (int v = 0; v < NV; v++) {
    if (I.root && v < 1) { R[t][v] = 0; continue; }
    int n = colStep(I, t, v, ys, hm); uint32_t m = 0;
    for (int k = 0; k < n; k++) if (ys[k] >= 0 && ys[k] < NV) m |= R[t + 1][ys[k]];
    R[t][v] = m;
  }
  vector<int> col(Lc + 1);
  int startv = I.root ? 1 : 0;
  function<void(int)> dfs = [&](int t) {
    if (count >= limit) return;
    if (t == Lc) { if (col[Lc] == col[0]) { count++; emit(col); } return; }
    int ys2[2], hm2[2]; int n = colStep(I, t, col[t], ys2, hm2);
    for (int k = 0; k < n; k++) {
      int y = ys2[k]; if (y < 0 || y >= NV) continue;
      if (!((R[t + 1][y] >> col[0]) & 1)) continue;
      col[t + 1] = y; dfs(t + 1);
    }
  };
  for (int v0 = startv; v0 < NV; v0++) { if (!((R[0][v0] >> v0) & 1)) continue; col[0] = v0; dfs(0); }
}

static Iface succIface(const Iface& I, const vector<int>& col, int Lc) {
  // new interface of period Lc above column col (Lc multiple of |I.c|)
  Iface J; J.c.resize(Lc); J.xb.resize(Lc); J.A.resize(Lc); J.root = false;
  int T0 = I.c.size();
  for (int t = 0; t < Lc; t++) {
    int v = col[t], tt = t % T0; int vnext = col[(t + 1)];
    J.c[t] = (int8_t)((v + I.c[tt]) / b);
    J.xb[t] = gAt(t) ? (int8_t)v : (int8_t)0;
    J.A[t] = (int8_t)colHmask(I, t, v, vnext);
  }
  return J;
}

// ---------- BFS over d0-periodic interfaces ----------
static vector<Iface> IFS; static vector<int> IFLVL; static vector<vector<int>> IFSUCC; static bool RECSUCC = false;
static int bfsInterfaces(int d0, long long capStates) {
  Iface root; root.c.assign(d0, 0); root.xb.assign(d0, -1); root.A.resize(d0); root.root = true;
  for (int t = 0; t < d0; t++) root.A[t] = 1 << gAt(t);
  unordered_map<string, int> seen; IFS.clear(); IFLVL.clear();
  seen[keyOf(root)] = 0; IFS.push_back(root); IFLVL.push_back(0); if (RECSUCC) { IFSUCC.clear(); IFSUCC.emplace_back(); }
  size_t head = 0; int level = 0;
  while (head < IFS.size()) {
    size_t levelEnd = IFS.size(); int newc = 0;
    for (; head < levelEnd; head++) {
      Iface cur = IFS[head];
      long long cnt = 0;
      enumColumns(cur, d0, [&](const vector<int>& col) {
        vector<int> cc(col.begin(), col.begin() + d0); vector<int> cl = cc; cl.push_back(cc[0]);
        Iface J = succIface(cur, cl, d0); // col[d0]=col[0]
        string key = keyOf(J);
        if (!seen.count(key)) { seen[key] = (int)IFS.size(); IFS.push_back(J); IFLVL.push_back(level + 1); newc++; if (RECSUCC) IFSUCC.emplace_back(); }
        if (RECSUCC) { int j = seen[key]; auto& v = IFSUCC[head]; if (find(v.begin(), v.end(), j) == v.end()) v.push_back(j); }
      }, cnt, (long long)1e12);
    }
    level++;
    if ((long long)IFS.size() > capStates) { fprintf(stderr, "interface cap exceeded\n"); return -1; }
    if (newc == 0 || head >= IFS.size()) { if (newc == 0) break; }
  }
  return level - 1; // a0 = last level at which new states appeared
}

// ---------- relative tower (khxt core with custom level 1) ----------
static int P; static vector<int> pat; static vector<int> Ls;
static int PRED = 0; static string PREDF;
static bool ROT = false, ROT2 = false;
static bool BULK = false, ALLL = false; static string RUNFILE, DEATHF, ONLYIF; static vector<char> ONLYMASK; static bool USEONLY = false;
static long long NODECAP = 20000000LL; static double SEC = 1e18; static int KMAX = 400;
static long long CHUNK = 4096;
static bool EXACTSET = true;
struct Level { int K = 0; vector<uint8_t> t, dig, lc, pdig, d1; vector<int32_t> o0, o1; size_t n() const { return t.size(); } };
static void buildLevel1(Level& L1, const Iface& J) {
  int Lc = J.c.size(); size_t n = (size_t)Lc * NV;
  L1.K = 1; L1.t.resize(n); L1.dig.resize(n); L1.lc.resize(n); L1.pdig.assign(n, 255); L1.d1.resize(n); L1.o0.assign(n, -1); L1.o1.assign(n, -1);
  for (int tt = 0; tt < Lc; tt++) for (int v = 0; v < NV; v++) {
    size_t id = (size_t)tt * NV + v;
    L1.t[id] = tt; L1.dig[id] = v; L1.d1[id] = v; L1.lc[id] = (v + J.c[tt] >= b);
    for (int h = 0; h < 2; h++) {
      int H = (v + h) / b; if (!((J.A[tt] >> H) & 1)) continue;
      int gg = pat[tt]; int part = gg ? (J.xb[tt] < 0 ? 1 : (J.xb[tt] + H) % b) : (v + h) % b;
      int y = (v + J.c[tt]) % b + part;
      int32_t tg = (int32_t)(((tt + 1) % Lc) * NV + y);
      (h ? L1.o1 : L1.o0)[id] = tg;
    }
  }
}
static bool buildChild(const Level& Pa, Level& C) {
  size_t m = Pa.n(); size_t n = m * NV;
  if ((long long)n > NODECAP) return false;
  C.K = Pa.K + 1; C.t.resize(n); C.dig.resize(n); C.lc.resize(n); C.pdig.resize(n); C.d1.resize(n); C.o0.assign(n, -1); C.o1.assign(n, -1);
  for (size_t j = 0; j < m; j++) {
    int tt = Pa.t[j], g = pat[tt], dj = Pa.dig[j], lj = Pa.lc[j];
    for (int v = 0; v < NV; v++) {
      size_t id = j * NV + v;
      C.t[id] = tt; C.dig[id] = v; C.lc[id] = (v + lj >= b); C.pdig[id] = (uint8_t)dj; C.d1[id] = Pa.d1[j];
      for (int h = 0; h < 2; h++) {
        int hp = (v + h >= b);
        int32_t tp = hp ? Pa.o1[j] : Pa.o0[j];
        if (tp < 0) continue;
        int y = (v + lj) % b + (g ? (dj + hp) % b : (v + h) % b);
        (h ? C.o1 : C.o0)[id] = (int32_t)((size_t)tp * NV + y);
      }
    }
  }
  return true;
}
static vector<uint8_t> alive; static vector<int32_t> indeg, outdeg, qbuf, rstart, rlist;
static void trim(Level& Lv) {
  size_t n = Lv.n();
  indeg.assign(n, 0); outdeg.assign(n, 0);
  for (size_t i = 0; i < n; i++) if (alive[i]) {
    int32_t a = Lv.o0[i], c = Lv.o1[i];
    if (a >= 0 && !alive[a]) a = -1; if (c >= 0 && !alive[c]) c = -1;
    if (a >= 0) { outdeg[i]++; indeg[a]++; }
    if (c >= 0) { outdeg[i]++; indeg[c]++; }
  }
  rstart.assign(n + 1, 0);
  for (size_t i = 0; i < n; i++) rstart[i + 1] = rstart[i] + indeg[i];
  rlist.assign(rstart[n], 0);
  { vector<int32_t> fill(rstart.begin(), rstart.end() - 1);
    for (size_t i = 0; i < n; i++) if (alive[i]) {
      int32_t a = Lv.o0[i], c = Lv.o1[i];
      if (a >= 0 && alive[a]) rlist[fill[a]++] = (int32_t)i;
      if (c >= 0 && alive[c]) rlist[fill[c]++] = (int32_t)i;
    } }
  qbuf.clear();
  for (size_t i = 0; i < n; i++) if (alive[i] && (indeg[i] == 0 || outdeg[i] == 0)) { alive[i] = 0; qbuf.push_back((int32_t)i); }
  for (size_t qi = 0; qi < qbuf.size(); qi++) {
    int32_t u = qbuf[qi];
    int32_t a = Lv.o0[u], c = Lv.o1[u];
    if (a >= 0 && alive[a]) { if (--indeg[a] == 0) { alive[a] = 0; qbuf.push_back(a); } }
    if (c >= 0 && alive[c] && c != a) { if (--indeg[c] == 0) { alive[c] = 0; qbuf.push_back(c); } }
    else if (c >= 0 && alive[c] && c == a) { if (--indeg[c] == 0) { alive[c] = 0; qbuf.push_back(c); } }
    for (int32_t k = rstart[u]; k < rstart[u + 1]; k++) { int32_t w = rlist[k]; if (alive[w]) { if (--outdeg[w] == 0) { alive[w] = 0; qbuf.push_back(w); } } }
  }
}
// exact closed-L-walk node set (phases mod L: one lap), per-source batches of CHUNK sources: returns kept count, or 0 if none.
static long long exactSet(Level& Lv) {
  size_t n = Lv.n(); int Lc = P;
  vector<long long> cnt(Lc, 0);
  for (size_t i = 0; i < n; i++) if (alive[i]) cnt[Lv.t[i]]++;
  int t0 = 0; for (int tt = 1; tt < Lc; tt++) if (cnt[tt] < cnt[t0]) t0 = tt;
  if (cnt[t0] == 0) { for (size_t i = 0; i < n; i++) alive[i] = 0; return 0; }
  vector<vector<int32_t>> lay(Lc);
  for (size_t i = 0; i < n; i++) if (alive[i]) lay[Lv.t[i]].push_back((int32_t)i);
  vector<int32_t> pos(n, -1);
  for (int tt = 0; tt < Lc; tt++) for (size_t k = 0; k < lay[tt].size(); k++) pos[lay[tt][k]] = (int32_t)k;
  long long s = cnt[t0];
  vector<uint8_t> ex(n, 0);
  long long CH = CHUNK;
  for (long long base = 0; base < s; base += CH) {
    long long sb = min(CH, s - base); int W = (int)((sb + 63) / 64);
    vector<vector<u64>> F(Lc);
    for (int tt = 0; tt < Lc; tt++) F[tt].assign(lay[tt].size() * (size_t)W, 0);
    for (long long i = 0; i < sb; i++) F[t0][(size_t)(base + i) * W + (i >> 6)] |= 1ULL << (i & 63);
    int tt = t0;
    for (int st = 0; st < Lc - 1; st++) {
      int t1 = (tt + 1) % Lc;
      for (size_t k = 0; k < lay[tt].size(); k++) {
        int32_t u = lay[tt][k]; const u64* src = &F[tt][k * W];
        bool any = false; for (int w = 0; w < W; w++) if (src[w]) { any = true; break; }
        if (!any) continue;
        int32_t a = Lv.o0[u], c = Lv.o1[u];
        if (a >= 0 && alive[a]) { u64* d = &F[t1][(size_t)pos[a] * W]; for (int w = 0; w < W; w++) d[w] |= src[w]; }
        if (c >= 0 && alive[c]) { u64* d = &F[t1][(size_t)pos[c] * W]; for (int w = 0; w < W; w++) d[w] |= src[w]; }
      }
      tt = t1;
    }
    vector<u64> cur(lay[t0].size() * (size_t)W, 0), nxt;
    for (long long i = 0; i < sb; i++) cur[(size_t)(base + i) * W + (i >> 6)] |= 1ULL << (i & 63);
    for (int tau = Lc - 1; tau >= 0; tau--) {
      int lt = (t0 + tau) % Lc;
      nxt.assign(lay[lt].size() * (size_t)W, 0);
      for (size_t k = 0; k < lay[lt].size(); k++) {
        int32_t u = lay[lt][k]; u64* d = &nxt[k * W];
        int32_t a = Lv.o0[u], c = Lv.o1[u];
        if (a >= 0 && alive[a]) { const u64* sr = &cur[(size_t)pos[a] * W]; for (int w = 0; w < W; w++) d[w] |= sr[w]; }
        if (c >= 0 && alive[c]) { const u64* sr = &cur[(size_t)pos[c] * W]; for (int w = 0; w < W; w++) d[w] |= sr[w]; }
        const u64* f = &F[lt][k * W]; for (int w = 0; w < W; w++) if (f[w] & d[w]) { ex[u] = 1; break; }
      }
      cur.swap(nxt);
    }
  }
  long long kept = 0;
  for (size_t i = 0; i < n; i++) { if (alive[i] && !ex[i]) alive[i] = 0; kept += alive[i]; }
  return kept;
}
static void compact(const Level& Lv, Level& Out) {
  size_t n = Lv.n(); vector<int32_t> nid(n, -1); size_t m = 0;
  for (size_t i = 0; i < n; i++) if (alive[i]) nid[i] = (int32_t)m++;
  Out.K = Lv.K; Out.t.resize(m); Out.dig.resize(m); Out.lc.resize(m); Out.pdig.resize(m); Out.d1.resize(m); Out.o0.resize(m); Out.o1.resize(m);
  for (size_t i = 0; i < n; i++) if (alive[i]) {
    int32_t k = nid[i]; Out.t[k] = Lv.t[i]; Out.dig[k] = Lv.dig[i]; Out.lc[k] = Lv.lc[i]; Out.pdig[k] = Lv.pdig[i]; Out.d1[k] = Lv.d1[i];
    int32_t a = Lv.o0[i], c = Lv.o1[i];
    Out.o0[k] = (a >= 0) ? nid[a] : -1; Out.o1[k] = (c >= 0) ? nid[c] : -1;
  }
}
// run the relative tower; returns death level (>=1), or -k if survived k levels (cap), maxnodes; keptLast
static unordered_map<string,int> MEMO; static size_t MEMOMAX = 3000000; static long long memoHits = 0;
static string ifaceKeyFromComp(const Level& comp, int Lc) {
  // comp has exactly one node per phase; interface above it: c = lc, xb = dig (gamma=1 phases only, else 0), A = edge mask
  vector<int32_t> id(Lc, -1); for (size_t i = 0; i < comp.n(); i++) id[comp.t[i]] = (int32_t)i;
  string k; k.reserve(3 * Lc + 1);
  for (int t = 0; t < Lc; t++) { int i = id[t]; int mask = (comp.o0[i] >= 0 ? 1 : 0) | (comp.o1[i] >= 0 ? 2 : 0);
    k.push_back((char)comp.lc[i]); k.push_back((char)((pat[t] ? (int)comp.dig[i] : 0) + 2)); k.push_back((char)mask); }
  k.push_back(0); return k;
}
static int runTower(const Iface& J, long long& maxnodes, long long& keptLast, double& secs, string& reason) {
  double t0 = now();
  Level cur, nxt, comp;
  buildLevel1(cur, J);
  maxnodes = 0; keptLast = 0; reason = "";
  vector<pair<string,int>> checkpoints;
  int K = 1;
  while (true) {
    maxnodes = max(maxnodes, (long long)cur.n());
    alive.assign(cur.n(), 1);
    trim(cur);
    size_t kept = 0; for (size_t i = 0; i < cur.n(); i++) kept += alive[i];
    if (kept) kept = exactSet(cur);
    if (kept == 0) { secs = now() - t0; for (auto& cp : checkpoints) if (MEMO.size() < MEMOMAX) MEMO[cp.first] = K - cp.second; return K; }
    keptLast = kept;
    compact(cur, comp);
    if ((int)comp.n() == P) {   // one node per phase: bottleneck column; the rest depends only on the interface above it
      string ck = ifaceKeyFromComp(comp, P);
      auto it = MEMO.find(ck);
      if (it != MEMO.end()) { memoHits++; int R = K + it->second; secs = now() - t0; for (auto& cp : checkpoints) if (MEMO.size() < MEMOMAX) MEMO[cp.first] = R - cp.second; return R; }
      checkpoints.push_back({ck, K});
    }
    if (K >= KMAX) { secs = now() - t0; reason = "kmax"; return -K; }
    if (now() - t0 > SEC) { secs = now() - t0; reason = "time"; return -K; }
    if ((long long)comp.n() * NV > NODECAP) { secs = now() - t0; reason = "nodecap"; return -K; }
    buildChild(comp, nxt);
    cur.d1.swap(nxt.d1); cur.t.swap(nxt.t); cur.dig.swap(nxt.dig); cur.lc.swap(nxt.lc); cur.pdig.swap(nxt.pdig); cur.o0.swap(nxt.o0); cur.o1.swap(nxt.o1); cur.K = nxt.K;
    K++;
  }
}


// ---------- r13c: all-L relative test: phases mod d0, keep all cyclic SCCs; "birth-free" if in every cyclic SCC the first column digit is a function of the phase ----------
static vector<int32_t> idxv, lowv, compv, stk; 
static long long sccAll(Level& Lv, bool& oneOK) {
  size_t n = Lv.n(); idxv.assign(n, -1); lowv.assign(n, 0); compv.assign(n, -1); stk.clear();
  vector<pair<int32_t,int>> cs; vector<uint8_t> onst(n, 0); int32_t cnt = 0; int nc = 0;
  auto nb = [&](int32_t u, int k) -> int32_t { int32_t w = k == 0 ? Lv.o0[u] : Lv.o1[u]; if (w >= 0 && !alive[w]) w = -1; return w; };
  for (size_t v0 = 0; v0 < n; v0++) { if (!alive[v0] || idxv[v0] >= 0) continue;
    cs.push_back({(int32_t)v0, 0}); idxv[v0] = lowv[v0] = cnt++; stk.push_back((int32_t)v0); onst[v0] = 1;
    while (!cs.empty()) { int32_t u = cs.back().first; int& pi = cs.back().second;
      if (pi < 2) { int32_t w = nb(u, pi++); if (w < 0) continue;
        if (idxv[w] < 0) { idxv[w] = lowv[w] = cnt++; stk.push_back(w); onst[w] = 1; cs.push_back({w, 0}); } else if (onst[w]) lowv[u] = min(lowv[u], idxv[w]); continue; }
      cs.pop_back(); if (!cs.empty()) { int32_t pu = cs.back().first; lowv[pu] = min(lowv[pu], lowv[u]); }
      if (lowv[u] == idxv[u]) { while (true) { int32_t w = stk.back(); stk.pop_back(); onst[w] = 0; compv[w] = nc; if (w == u) break; } nc++; } } }
  // cyclic SCC: has an internal edge
  vector<char> cyc(nc, 0); 
  for (size_t i = 0; i < n; i++) if (alive[i]) { int c = compv[i]; for (int k = 0; k < 2; k++) { int32_t w = nb((int32_t)i, k); if (w >= 0 && compv[w] == c) cyc[c] = 1; } }
  long long kept = 0;
  for (size_t i = 0; i < n; i++) if (alive[i]) { if (cyc[compv[i]]) kept++; else alive[i] = 0; }
  // first-digit uniqueness per SCC per phase
  oneOK = true;
  map<pair<int,int>, int> dig; // (comp, t) -> d1
  for (size_t i = 0; i < n; i++) if (alive[i]) { auto key = make_pair(compv[i], (int)Lv.t[i]); auto it = dig.find(key); if (it == dig.end()) dig[key] = Lv.d1[i]; else if (it->second != Lv.d1[i]) { oneOK = false; break; } }
  return kept;
}
static int runAllL(const Iface& I, int Lc, int kcap, long long nodecap, long long& maxn, string& verdict, int& atr) {
  // phases mod Lc = |I.c|, level-1 from interface I (root flag honoured via digit >= 1)
  Level cur, nxt, comp;
  buildLevel1(cur, I); if (I.root) for (size_t i = 0; i < cur.n(); i++) if (cur.dig[i] < 1) { cur.o0[i] = cur.o1[i] = -1; }
  maxn = 0; int K = 1;
  while (true) {
    maxn = max(maxn, (long long)cur.n());
    alive.assign(cur.n(), 1);
    if (I.root) for (size_t i = 0; i < cur.n(); i++) if (K == 1 && cur.dig[i] < 1) alive[i] = 0;
    trim(cur);
    size_t kept = 0; for (size_t i = 0; i < cur.n(); i++) kept += alive[i];
    bool oneOK = true; long long k2 = 0;
    if (kept) { k2 = sccAll(cur, oneOK); }
    if (k2 == 0) { verdict = "DEAD"; atr = K; return K; }
    if (oneOK) { verdict = "BIRTHFREE"; atr = K; return K; }
    compact(cur, comp);
    if (K >= kcap || (long long)comp.n() * NV > nodecap) { verdict = K >= kcap ? "KCAP" : "NCAP"; atr = K; return -K; }
    buildChild(comp, nxt);
    cur.t.swap(nxt.t); cur.dig.swap(nxt.dig); cur.lc.swap(nxt.lc); cur.pdig.swap(nxt.pdig); cur.d1.swap(nxt.d1); cur.o0.swap(nxt.o0); cur.o1.swap(nxt.o1); cur.K = nxt.K;
    K++;
  }
}


static string canonKey(const Iface& J, int stepP) {
  int L0 = J.c.size(); string best;
  int rots = L0 / stepP;
  for (int r = 0; r < rots; r++) {
    string k; k.reserve(L0 * 3 + 1); int sh = r * stepP;
    for (int t = 0; t < L0; t++) { int i = (t + sh) % L0; k.push_back(J.c[i]); k.push_back((char)(J.xb[i] + 2)); k.push_back(J.A[i]); }
    k.push_back(J.root ? 1 : 0);
    if (r == 0 || k < best) best.swap(k);
  }
  return best;
}
static string fmtIface(const Iface& J) {
  string s;
  for (size_t i = 0; i < J.c.size(); i++) { s += char('0' + J.c[i]); } s += "|";
  for (size_t i = 0; i < J.c.size(); i++) { char buf[8]; snprintf(buf, 8, "%d%s", (int)J.xb[i], i + 1 < J.c.size() ? "," : ""); s += buf; } s += "|";
  for (size_t i = 0; i < J.c.size(); i++) s += char('0' + J.A[i]);
  return s;
}

static void bh(int sig){ void* a[50]; int n=backtrace(a,50); write(2,"CRASH\n",6); backtrace_symbols_fd(a,n,2); _exit(99);} 
int main(int argc, char** argv) {
  signal(SIGBUS,bh); signal(SIGSEGV,bh);
  if (argc < 5) { fprintf(stderr, "usage: khr b g d0 L [-kmax N -nodecap N -sec S -shard i N -listif F -pairs F -plist] (root pattern g, d0 = base period, L multiple of d0)\n"); return 2; }
  b = atoi(argv[1]); NV = 2 * b - 1; string gw = argv[2]; int d0 = atoi(argv[3]); int L = atoi(argv[4]);
  gP = gw.size(); gpat.resize(gP); for (int i = 0; i < gP; i++) gpat[i] = gw[i] - '0';
  int shard = -1, nsh = 1; string listif, pairsf; double perSec = 60; bool plist = false; long long capI = 20000000; long long colLimit = 2000000000LL; int maxTowers = -1;
  for (int i = 5; i < argc; i++) { string a = argv[i];
    if (a == "-kmax") KMAX = atoi(argv[++i]); else if (a == "-nodecap") NODECAP = atoll(argv[++i]); else if (a == "-sec") perSec = atof(argv[++i]);
    else if (a == "-shard") { shard = atoi(argv[++i]); nsh = atoi(argv[++i]); } else if (a == "-listif") listif = argv[++i]; else if (a == "-pairs") pairsf = argv[++i];
    else if (a == "-plist") plist = true; else if (a == "-capI") capI = atoll(argv[++i]); else if (a == "-collimit") colLimit = atoll(argv[++i]); else if (a == "-max") maxTowers = atoi(argv[++i]);
    else if (a == "-batch") CHUNK = atoll(argv[++i]);
    else if (a == "-predict") { PRED = atoi(argv[++i]); PREDF = argv[++i]; RECSUCC = true; }
    else if (a == "-deaths") DEATHF = argv[++i];
    else if (a == "-bulk") BULK = true; else if (a == "-allL") ALLL = true; else if (a == "-rot") ROT = true; else if (a == "-rot2") { ROT = true; ROT2 = true; } else if (a == "-onlyif") ONLYIF = argv[++i]; else if (a == "-runfile") RUNFILE = argv[++i];
    else { fprintf(stderr, "unknown %s\n", a.c_str()); return 2; } }
  SEC = perSec;
  double t00 = now();
  int a0 = bfsInterfaces(d0, capI);
  if (a0 < 0) return 1;
  fprintf(stderr, "IFSAT g=%s d0=%d interfaces=%zu a0=%d t=%.2f\n", gw.c_str(), d0, IFS.size(), a0, now() - t00);
  if (L == 0) return 0;
  if (!listif.empty()) { FILE* f = fopen(listif.c_str(), "w"); for (size_t i = 0; i < IFS.size(); i++) fprintf(f, "%zu %d %s %d\n", i, IFLVL[i], fmtIface(IFS[i]).c_str(), IFS[i].root ? 1 : 0); fclose(f); }


  if (!ONLYIF.empty()) { ONLYMASK.assign(IFS.size(), 0); FILE* f = fopen(ONLYIF.c_str(), "r"); int x; while (fscanf(f, "%d", &x) == 1) if (x >= 0 && x < (int)IFS.size()) ONLYMASK[x] = 1; fclose(f); USEONLY = true; }
  if (ALLL) {
    P = d0; pat.resize(d0); for (int t = 0; t < d0; t++) pat[t] = gAt(t);
    long long bf = 0, dead = 0, cap = 0; map<string,long long> vc; map<int,long long> byr;
    for (size_t ii = 0; ii < IFS.size(); ii++) {
      if (USEONLY && !ONLYMASK[ii]) continue;
      if (shard >= 0 && (int)(ii % nsh) != shard) continue;
      long long maxn; string v; int atr;
      runAllL(IFS[ii], d0, KMAX, NODECAP, maxn, v, atr);
      vc[v]++; if (v == "BIRTHFREE" || v == "DEAD") byr[atr]++;
      if (v != "BIRTHFREE" && v != "DEAD") { printf("ALLL_CAP if=%zu lvl=%d %s r=%d maxn=%lld iface=%s\n", ii, IFLVL[ii], v.c_str(), atr, maxn, fmtIface(IFS[ii]).c_str()); fflush(stdout); }
    }
    printf("ALLL g=%s d0=%d shard=%d/%d:", gw.c_str(), d0, shard, nsh); for (auto& kv : vc) printf(" %s=%lld", kv.first.c_str(), kv.second); printf("\nALLL_RHIST"); for (auto& kv : byr) printf(" %d:%lld", kv.first, kv.second); printf("\n");
    return 0;
  }
  if (BULK) {
    // Memory-light mode: per-interface local dedupe, towers run during the enumeration; shard by interface index.
    P = L; pat.resize(L); for (int t = 0; t < L; t++) pat[t] = gAt(t);
    map<int, long long> hist; long long dies = 0, surv = 0, ran = 0, emitted = 0; unordered_set<string> local;
    for (size_t ii = 0; ii < IFS.size(); ii++) {
      if (USEONLY && !ONLYMASK[ii]) continue;
      if (ROT2) { // keep only interfaces canonical under rotation by the clock period; shard by interface index
        if (canonKey(IFS[ii], gP) != keyOf(IFS[ii]) ) {
          // not canonical: skip unless a rotation of this interface is itself and smaller... canonKey==keyOf means ii is the minimal rotation
          continue; }
        if (shard >= 0 && (int)(ii % nsh) != shard) continue;
      } else if (!ROT && shard >= 0 && (int)(ii % nsh) != shard) continue;
      Iface cur = IFS[ii]; long long cnt = 0; if (!ROT) local.clear();
      enumColumns(cur, L, [&](const vector<int>& col) {
        bool per = true; for (int t = 0; t + d0 < L; t++) if (col[t] != col[t + d0]) { per = false; break; }
        if (per) return;
        emitted++;
        vector<int> cc(col.begin(), col.end());
        Iface J = succIface(cur, cc, L);
        string key = ROT ? canonKey(J, gP) : keyOf(J);
        if (ROT && !ROT2) { size_t hs = std::hash<string>{}(key); if (shard >= 0 && (int)(hs % nsh) != shard) return; }
        if (!local.insert(key).second) return;
        long long maxn, keptl; double secs; string reason;
        int r = runTower(J, maxn, keptl, secs, reason);
        ran++;
        if (r > 0) { hist[r]++; dies++; if (r >= 300 || secs > 30) { printf("TDIES if=%zu K=%d maxn=%lld secs=%.2f\n", ii, r, maxn, secs); fflush(stdout); } }
        else { surv++; printf("TSURV if=%zu K=%d kept=%lld reason=%s maxn=%lld secs=%.2f iface=%s col=", ii, -r, keptl, reason.c_str(), maxn, secs, fmtIface(J).c_str()); for (int t = 0; t < L; t++) printf("%d,", col[t]); printf("\n"); fflush(stdout); }
        if ((ran & ((1LL<<16)-1)) == 0) { fprintf(stderr, "progress if=%zu ran=%lld dies=%lld surv=%lld t=%.1f\n", ii, ran, dies, surv, now() - t00); }
      }, cnt, colLimit);
    }
    printf("KHR_BULK g=%s d0=%d L=%d interfaces=%zu a0=%d shard=%d/%d emitted=%lld ran=%lld dies=%lld surv=%lld memohits=%lld memosize=%zu secs=%.1f\n", gw.c_str(), d0, L, IFS.size(), a0, shard, nsh, emitted, ran, dies, surv, memoHits, MEMO.size(), now() - t00);
    printf("HIST"); for (auto& kv : hist) printf(" %d:%lld", kv.first, kv.second); printf("\n");
    return 0;
  }
  if (!RUNFILE.empty()) {
    P = L; pat.resize(L); for (int t = 0; t < L; t++) pat[t] = gAt(t);
    FILE* f = fopen(RUNFILE.c_str(), "r"); if (!f) { perror("runfile"); return 2; }
    char* line = nullptr; size_t cap = 0; long long idx = 0; map<int,long long> hist; long long dies = 0, surv = 0, ran = 0;
    while (getline(&line, &cap, f) > 0) {
      string sl(line); size_t p0 = sl.find("iface="); if (p0 == string::npos) continue; p0 += 6; size_t p1 = sl.find_first_of(" \n", p0); string spec = sl.substr(p0, p1 - p0);
      idx++;
      if (shard >= 0 && (idx % nsh) != shard) continue;
      // parse c|xb|A
      size_t bar1 = spec.find('|'), bar2 = spec.find('|', bar1 + 1);
      string cs = spec.substr(0, bar1), xs = spec.substr(bar1 + 1, bar2 - bar1 - 1), as = spec.substr(bar2 + 1);
      Iface J; J.root = false; int Ln = cs.size();
      J.c.resize(Ln); J.xb.resize(Ln); J.A.resize(Ln);
      for (int t = 0; t < Ln; t++) { J.c[t] = cs[t] - '0'; J.A[t] = as[t] - '0'; }
      { size_t q = 0; for (int t = 0; t < Ln; t++) { size_t r = xs.find(',', q); if (r == string::npos) r = xs.size(); J.xb[t] = (int8_t)atoi(xs.substr(q, r - q).c_str()); q = r + 1; } }
      long long maxn, keptl; double secs; string reason;
      int r = runTower(J, maxn, keptl, secs, reason); ran++;
      string colpart; size_t p2 = sl.find("col="); if (p2 != string::npos) colpart = sl.substr(p2);
      if (r > 0) { hist[r]++; dies++; printf("RDIES idx=%lld K=%d maxn=%lld secs=%.2f iface=%s\n", idx, r, maxn, secs, spec.c_str()); }
      else { surv++; printf("RSURV idx=%lld K=%d kept=%lld reason=%s maxn=%lld secs=%.2f iface=%s %s\n", idx, -r, keptl, reason.c_str(), maxn, secs, spec.c_str(), colpart.c_str()); }
      fflush(stdout);
    }
    printf("KHR_RUN file=%s shard=%d/%d ran=%lld dies=%lld surv=%lld\n", RUNFILE.c_str(), shard, nsh, ran, dies, surv);
    printf("HIST"); for (auto& kv : hist) printf(" %d:%lld", kv.first, kv.second); printf("\n");
    return 0;
  }
  // Step 2: births
  P = L; pat.resize(L); for (int t = 0; t < L; t++) pat[t] = gAt(t);
  unordered_map<string,int> seen; vector<Iface> births; vector<int> bif; vector<vector<int>> bcol; vector<vector<int>> ifBirths(IFS.size());
  long long totalCols = 0, emitted = 0;
  for (size_t ii = 0; ii < IFS.size(); ii++) {
    Iface cur = IFS[ii]; long long cnt = 0;
    enumColumns(cur, L, [&](const vector<int>& col) {
      bool per = true; for (int t = 0; t + d0 < L; t++) if (col[t] != col[t + d0]) { per = false; break; }
      if (per) return;
      emitted++;
      vector<int> cc(col.begin(), col.end()); // col has Lc+1 entries, col[L]==col[0]
      Iface J = succIface(cur, cc, L);
      string key = keyOf(J);
      auto it = seen.find(key); int bidx;
      if (it == seen.end()) { bidx = (int)births.size(); seen[key] = bidx; births.push_back(J); bif.push_back((int)ii); bcol.push_back(vector<int>(col.begin(), col.begin() + L)); } else bidx = it->second;
      if (PRED) { auto& vb = ifBirths[ii]; if (vb.empty() || vb.back() != bidx) vb.push_back(bidx); }
    }, cnt, colLimit);
    totalCols += cnt;
    if (cnt >= colLimit) { fprintf(stderr, "COLUMN LIMIT at interface %zu\n", ii); }
    if ((long long)births.size() > 200000000LL) { fprintf(stderr, "too many births\n"); break; }
  }
  fprintf(stderr, "BIRTHS g=%s d0=%d L=%d closedcols=%lld nonperiodic=%lld distinct=%zu t=%.2f\n", gw.c_str(), d0, L, totalCols, emitted, births.size(), now() - t00);
  if (!pairsf.empty()) { FILE* f = fopen(pairsf.c_str(), "w"); for (size_t i = 0; i < births.size(); i++) { fprintf(f, "%zu %d ", i, bif[i]); for (int v : bcol[i]) fprintf(f, "%d,", v); fprintf(f, " %s\n", fmtIface(births[i]).c_str()); } fclose(f); }
  if (plist) return 0;
  // Step 3: towers
  map<int, long long> hist; long long dies = 0, surv = 0, ran = 0; vector<int> DV(births.size(), -1);
  for (size_t ii = 0; ii < births.size(); ii++) {
    if (shard >= 0 && (int)(ii % nsh) != shard) continue;
    if (maxTowers >= 0 && ran >= maxTowers) break;
    long long maxn, keptl; double secs; string reason;
    int r = runTower(births[ii], maxn, keptl, secs, reason);
    ran++;
    if (r > 0) { DV[ii] = r; hist[r]++; dies++; if (r >= 100 || secs > 5) { printf("TDIES idx=%zu K=%d maxn=%lld secs=%.2f\n", ii, r, maxn, secs); fflush(stdout); } }
    else { DV[ii] = 1000000000; surv++; printf("TSURV idx=%zu K=%d kept=%lld reason=%s maxn=%lld secs=%.2f iface=%s col=", ii, -r, keptl, reason.c_str(), maxn, secs, fmtIface(births[ii]).c_str()); for (int v : bcol[ii]) printf("%d,", v); printf(" fromIf=%d\n", bif[ii]); fflush(stdout); }
  }
  printf("KHR g=%s d0=%d L=%d interfaces=%zu a0=%d births=%zu shard=%d/%d ran=%lld dies=%lld surv=%lld secs=%.1f\n", gw.c_str(), d0, L, IFS.size(), a0, births.size(), shard, nsh, ran, dies, surv, now() - t00);
  printf("HIST"); for (auto& kv : hist) printf(" %d:%lld", kv.first, kv.second); printf("\n");
  if (!DEATHF.empty()) { FILE* f = fopen(DEATHF.c_str(), "w"); for (size_t i = 0; i < births.size(); i++) if (DV[i] > 0) fprintf(f, "%zu %d %s\n", i, DV[i], fmtIface(births[i]).c_str()); fclose(f); }
  if (PRED) {
    // heights: frontier sets
    int n = IFS.size(); vector<int> Dstar(n, 0);
    for (int i = 0; i < n; i++) for (int bi : ifBirths[i]) Dstar[i] = max(Dstar[i], DV[bi]);
    FILE* f = fopen(PREDF.c_str(), "w");
    vector<char> cur(n, 0), nxt(n, 0); cur[0] = 1;
    // best[a] : min over i in F_a of a + Dstar(i) large ... compute for each a: maxD[a] = max_{i in F_a} Dstar(i) (0 if none has a birth)
    vector<long long> reach(PRED + 2, 0); vector<int> maxDa;
    for (int a = 0; a <= PRED; a++) {
      int md = 0; bool any = false;
      for (int i = 0; i < n; i++) if (cur[i]) { any = true; md = max(md, Dstar[i]); }
      maxDa.push_back(md);
      fill(nxt.begin(), nxt.end(), 0);
      for (int i = 0; i < n; i++) if (cur[i]) for (int j : IFSUCC[i]) nxt[j] = 1;
      cur.swap(nxt);
      if (!any) break;
    }
    for (int K = 1; K <= PRED; K++) {
      int rig = -1;
      for (int a = 0; a < (int)maxDa.size() && a <= K - 1; a++) { long long lim = a + (long long)maxDa[a]; if (maxDa[a] >= 1 && lim >= K) { rig = a; break; } }
      if (rig < 0) fprintf(f, "K=%d Rig_pred=none\n", K); else fprintf(f, "K=%d Rig_pred=%d\n", K, rig);
    }
    fclose(f);
  }
  return 0;
}
