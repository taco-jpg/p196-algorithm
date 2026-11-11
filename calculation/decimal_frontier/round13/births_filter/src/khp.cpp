// khxt.cpp (r12e): r12b's khx (exact K-head closed-walk filter) + three additions, for the UNDECIDED words of r12b section 9.
//
//  (1) -top : at every level K, on the kept set S_K, the closed-L-walk test restricted to
//        TOP99_K = kept nodes whose two top digits are (9,9)                       (edges: kept edges between such nodes), and
//        TOPUU_K = kept nodes whose two top digits are (u,u), u an f-periodic band value != b-1, with only the edges whose
//                  target top digit is f(u), f(u) = 2((u + [u>=b]) mod b).
//      Line "TOP K=.. n99=.. c99=.. nUU=.. cUU=.." per level (n = nodes in the subset, c = 1 iff a closed L-walk exists inside).
//      A closed L-walk inside TOP99_K is a wire-accepting reach history of height K (top cell 9 at all times, delta_K = 1 - c_K
//      forced, rho_K = 9 c_K), i.e. an exterior of width <= K-2 (Theorem B); conversely every exterior of width W gives one at every
//      K >= W+2.  Inside TOPUU_K: a strict band acceptance at height K-1 (uniform-band template, Theorem B').  So "c99 = 0 at level
//      K" means: no 9-wire exterior of width <= K-2;  "cUU = 0": no uniform-band template of left-end height <= K-3.
//      With -dump FILE and a hit, the closed part is written with full windows (needs the parent chains: KEEP).
//  (2) -exactset : after khx's pruning (trim, SCC period | L, exact closure test + one-lap refinement), reduce the kept set to
//      EXACTLY the nodes lying on a closed walk of length L (some L in Ls): node v at phase offset k from the anchor layer t0 is on
//      such a walk iff some anchor-layer node s has s ->^k v and v ->^(L-k) s (per-source bitsets, forward P-1 steps, backward L
//      steps).  This is the canonical (smallest possible) kept set; deaths are unchanged.
//  (3) -inv : per level a Weisfeiler-Lehman hash of the attributed kept graph (phase, top digit, carry L_K, labelled edges), to
//      detect candidate stabilisation (Theorem U of r12b needs an isomorphism kept_K0 ~ kept_K0+d; this only finds candidates).
//      -gdump K1,K2,..  writes the attributed kept graph at those levels to FILE.K (idx t dig lc pdig o0 o1) for an ISO check.
// Everything else (graph, trans, incremental children, trim, SCC, exactTest) is r12b's khx.cpp, unchanged.
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
#include <utility>
using namespace std;
typedef unsigned long long u64;

static int b = 10, NV = 19;
static int P; static vector<int> pat; static vector<int> Ls;
static bool USE_EXACT = true, USE_SCC = true, VERB = false, CHECK = false, KEEP = false; static string DUMPF;
static bool PERIODS = false, ALLM = false; static long long CHUNK = 0; static long long SMAX = 4096; static long long NODECAP = 200000000LL; static double SEC = 1e18; static int KMAX = 60, KMIN = 1;
static int PRIMD = 0; static string PRIMLIST; static bool PRIMON = false;
static bool TOPCHK = false, EXACTSET = false, INV = false, STOPHIT = false; static int TOPEVERY = 1; static set<int> GDUMP; static string GDUMPF, WDUMPF, CPF, ANF; static int CPD = 0, AND_ = 0; static bool ANCON = false;
struct AncLv { vector<int32_t> par; vector<uint8_t> dig, t; };
static vector<AncLv> ANC;
static double now() { return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }

struct Level {
  int K = 0;
  vector<uint8_t> t, dig, lc, pdig;  // phase, top digit x_{K-1}, forward carry into position K, parent's top digit x_{K-2} (255 at K=1)
  vector<int32_t> o0, o1;
  vector<int32_t> par;
  size_t n() const { return t.size(); }
};

static void trans(const vector<int>& x, int h, vector<int>& y, int& g) {
  int K = x.size(); vector<int> H(K + 1), L(K + 1, 0); H[K] = h;
  for (int i = K - 1; i >= 0; i--) H[i] = (x[i] + H[i + 1]) / b;
  g = H[0];
  for (int i = 0; i < K; i++) L[i + 1] = (x[i] + L[i]) / b;
  y.assign(K, 0);
  for (int i = 0; i < K; i++) { int part = g ? (i == 0 ? 1 : (x[i - 1] + H[i]) % b) : (x[i] + H[i + 1]) % b; y[i] = (x[i] + L[i]) % b + part; }
}

static void buildLevel1(Level& L1) {
  int nq = NV - 1; size_t n = (size_t)P * nq;
  L1.K = 1; L1.t.resize(n); L1.dig.resize(n); L1.lc.resize(n); L1.pdig.assign(n, 255); L1.o0.assign(n, -1); L1.o1.assign(n, -1); L1.par.assign(n, -1);
  for (int tt = 0; tt < P; tt++) for (int q = 1; q <= 2 * b - 2; q++) {
    size_t id = (size_t)tt * nq + (q - 1);
    L1.t[id] = tt; L1.dig[id] = q; L1.lc[id] = (q >= b);
    for (int h = 0; h < 2; h++) {
      int g = (q + h >= b); if (g != pat[tt]) continue;
      int y = (q % b) + (g ? 1 : (q + h) % b);
      int32_t tg = (int32_t)(((tt + 1) % P) * nq + (y - 1));
      (h ? L1.o1 : L1.o0)[id] = tg;
    }
  }
}

static bool buildChild(const Level& Pa, Level& C) {
  size_t m = Pa.n(); size_t n = m * NV;
  if ((long long)n > NODECAP) return false;
  C.K = Pa.K + 1; C.t.resize(n); C.dig.resize(n); C.lc.resize(n); C.pdig.resize(n); C.o0.assign(n, -1); C.o1.assign(n, -1);
  if (CHECK || KEEP || ANCON || PRIMON) C.par.resize(n);
  for (size_t j = 0; j < m; j++) {
    int tt = Pa.t[j], g = pat[tt], dj = Pa.dig[j], lj = Pa.lc[j];
    for (int v = 0; v < NV; v++) {
      size_t id = j * NV + v;
      C.t[id] = tt; C.dig[id] = v; C.lc[id] = (v + lj >= b); C.pdig[id] = (uint8_t)dj; if (CHECK || KEEP || ANCON || PRIMON) C.par[id] = (int32_t)j;
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

static vector<Level*> ALL;
static vector<int> recon(int lev, size_t id) {
  vector<int> x(lev + 1);
  for (int k = lev; k >= 0; k--) { x[k] = ALL[k]->dig[id]; id = (size_t)ALL[k]->par[id]; }
  return x;
}

// ---------- pruning (r12b khx, unchanged) ----------
static vector<uint8_t> alive;
static vector<int32_t> indeg, outdeg, qbuf, rstart, rlist;

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

static long long gcdll(long long a, long long c) { if (a < 0) a = -a; if (c < 0) c = -c; while (c) { long long r = a % c; a = c; c = r; } return a; }

static vector<int32_t> idxv, lowv, compv, stk, dist;
static vector<pair<int32_t, int>> cs;
static size_t sccFilter(Level& Lv) {
  size_t n = Lv.n();
  idxv.assign(n, -1); lowv.assign(n, 0); compv.assign(n, -1); stk.clear(); cs.clear();
  vector<uint8_t> onst(n, 0);
  int32_t cnt = 0, nc = 0;
  auto nb = [&](int32_t u, int k) -> int32_t { int32_t w = k == 0 ? Lv.o0[u] : Lv.o1[u]; if (w >= 0 && !alive[w]) w = -1; return w; };
  for (size_t v0 = 0; v0 < n; v0++) {
    if (!alive[v0] || idxv[v0] >= 0) continue;
    cs.push_back({(int32_t)v0, 0}); idxv[v0] = lowv[v0] = cnt++; stk.push_back((int32_t)v0); onst[v0] = 1;
    while (!cs.empty()) {
      int32_t u = cs.back().first; int& pi = cs.back().second;
      if (pi < 2) {
        int32_t w = nb(u, pi++);
        if (w < 0) continue;
        if (idxv[w] < 0) { idxv[w] = lowv[w] = cnt++; stk.push_back(w); onst[w] = 1; cs.push_back({w, 0}); }
        else if (onst[w]) lowv[u] = min(lowv[u], idxv[w]);
        continue;
      }
      cs.pop_back();
      if (!cs.empty()) { int32_t pu = cs.back().first; lowv[pu] = min(lowv[pu], lowv[u]); }
      if (lowv[u] == idxv[u]) { while (true) { int32_t w = stk.back(); stk.pop_back(); onst[w] = 0; compv[w] = nc; if (w == u) break; } nc++; }
    }
  }
  vector<long long> per(nc, 0); vector<int32_t> root(nc, -1);
  dist.assign(n, -1);
  for (size_t i = 0; i < n; i++) if (alive[i] && root[compv[i]] < 0) root[compv[i]] = (int32_t)i;
  vector<int32_t> q;
  for (int c = 0; c < nc; c++) {
    int32_t r = root[c]; if (r < 0) continue;
    q.clear(); q.push_back(r); dist[r] = 0; long long gg = 0;
    for (size_t qi = 0; qi < q.size(); qi++) {
      int32_t u = q[qi];
      for (int k = 0; k < 2; k++) { int32_t w = nb(u, k); if (w < 0 || compv[w] != c) continue;
        if (dist[w] < 0) { dist[w] = dist[u] + 1; q.push_back(w); } else gg = gcdll(gg, (long long)dist[u] + 1 - dist[w]); }
    }
    per[c] = gg;
  }
  size_t kept = 0;
  for (size_t i = 0; i < n; i++) if (alive[i]) {
    long long qq = per[compv[i]]; bool ok = false;
    if (ALLM) ok = (qq > 0);
    else if (qq > 0) for (int L : Ls) if (L % qq == 0) { ok = true; break; }
    if (!ok) alive[i] = 0; else kept++;
  }
  if (PERIODS) {
    map<long long, pair<long long, long long>> pm; vector<char> seenc(nc, 0);
    for (size_t i = 0; i < n; i++) if (alive[i]) { int c = compv[i]; pm[per[c]].second++; if (!seenc[c]) { seenc[c] = 1; pm[per[c]].first++; } }
    fprintf(stderr, "  PERIODS K=%d", Lv.K); for (auto& kv : pm) fprintf(stderr, " %lld:%lldx%lld", kv.first, kv.second.first, kv.second.second); fprintf(stderr, "\n");
  }
  return kept;
}

static int exactTest(Level& Lv, long long& smallest) {
  size_t n = Lv.n();
  vector<long long> cnt(P, 0);
  for (size_t i = 0; i < n; i++) if (alive[i]) cnt[Lv.t[i]]++;
  int t0 = 0; for (int tt = 1; tt < P; tt++) if (cnt[tt] < cnt[t0]) t0 = tt;
  smallest = cnt[t0];
  if (cnt[t0] == 0) return 0;
  if (CHUNK == 0 && cnt[t0] > SMAX) return -1;
  vector<vector<int32_t>> lay(P);
  for (size_t i = 0; i < n; i++) if (alive[i]) lay[Lv.t[i]].push_back((int32_t)i);
  vector<int32_t> pos(n, -1);
  for (int tt = 0; tt < P; tt++) for (size_t k = 0; k < lay[tt].size(); k++) pos[lay[tt][k]] = (int32_t)k;
  long long s = cnt[t0];
  int maxm = 0; for (int L : Ls) maxm = max(maxm, L / P);
  vector<char> wantm(maxm + 1, 0); for (int L : Ls) wantm[L / P] = 1;
  vector<uint8_t> Cf((size_t)s, 0);
  long long CH = CHUNK > 0 ? CHUNK : s;
  for (long long base = 0; base < s; base += CH) {
    long long sb = min(CH, s - base); int W = (int)((sb + 63) / 64);
    vector<u64> cur((size_t)s * W, 0), nxt;
    for (long long i = 0; i < sb; i++) cur[(size_t)(base + i) * W + (i >> 6)] |= 1ULL << (i & 63);
    int tt = t0;
    for (int lap = 1; lap <= maxm; lap++) {
      for (int st = 0; st < P; st++) {
        int t1 = (tt + 1) % P;
        nxt.assign(lay[t1].size() * (size_t)W, 0);
        for (size_t k = 0; k < lay[tt].size(); k++) {
          int32_t u = lay[tt][k]; const u64* src = &cur[k * W];
          bool any = false; for (int w = 0; w < W; w++) if (src[w]) { any = true; break; }
          if (!any) continue;
          int32_t a = Lv.o0[u], c = Lv.o1[u];
          if (a >= 0 && alive[a]) { u64* d = &nxt[(size_t)pos[a] * W]; for (int w = 0; w < W; w++) d[w] |= src[w]; }
          if (c >= 0 && alive[c]) { u64* d = &nxt[(size_t)pos[c] * W]; for (int w = 0; w < W; w++) d[w] |= src[w]; }
        }
        cur.swap(nxt); tt = t1;
      }
      if (wantm[lap]) for (long long i = 0; i < sb; i++) if ((cur[(size_t)(base + i) * W + (i >> 6)] >> (i & 63)) & 1) Cf[base + i] = 1;
    }
  }
  bool anyC = false; for (long long i = 0; i < s; i++) if (Cf[i]) { anyC = true; break; }
  if (!anyC) return 0;
  vector<uint8_t> fm(n, 0), bm(n, 0);
  for (long long i = 0; i < s; i++) if (Cf[i]) { fm[lay[t0][i]] = 1; bm[lay[t0][i]] = 1; }
  int tt = t0;
  for (int st = 0; st < P - 1; st++) {
    for (int32_t u : lay[tt]) if (fm[u]) { int32_t a = Lv.o0[u], c = Lv.o1[u]; if (a >= 0 && alive[a]) fm[a] = 1; if (c >= 0 && alive[c]) fm[c] = 1; }
    tt = (tt + 1) % P;
  }
  tt = (t0 + P - 1) % P;
  for (int st = 0; st < P - 1; st++) {
    for (int32_t u : lay[tt]) { int32_t a = Lv.o0[u], c = Lv.o1[u]; if ((a >= 0 && alive[a] && bm[a]) || (c >= 0 && alive[c] && bm[c])) bm[u] = 1; }
    tt = (tt + P - 1) % P;
  }
  for (size_t i = 0; i < n; i++) if (alive[i] && !(fm[i] && bm[i])) alive[i] = 0;
  return 1;
}

// ---------- r12e (2): exact closed-walk node set ----------
// On the alive subgraph: mark v iff exists s in anchor layer t0 and L in Ls with s ->^k v ->^(L-k) s, k = (t(v)-t0) mod P.
static long long exactSet(Level& Lv) {
  size_t n = Lv.n();
  vector<long long> cnt(P, 0);
  for (size_t i = 0; i < n; i++) if (alive[i]) cnt[Lv.t[i]]++;
  int t0 = 0; for (int tt = 1; tt < P; tt++) if (cnt[tt] < cnt[t0]) t0 = tt;
  if (cnt[t0] == 0) { for (size_t i = 0; i < n; i++) alive[i] = 0; return 0; }
  vector<vector<int32_t>> lay(P);
  for (size_t i = 0; i < n; i++) if (alive[i]) lay[Lv.t[i]].push_back((int32_t)i);
  vector<int32_t> pos(n, -1);
  for (int tt = 0; tt < P; tt++) for (size_t k = 0; k < lay[tt].size(); k++) pos[lay[tt][k]] = (int32_t)k;
  long long s = cnt[t0];
  vector<uint8_t> ex(n, 0);
  long long CH = CHUNK > 0 ? CHUNK : 4096;
  for (int L : Ls) {
    int m = L / P;
    for (long long base = 0; base < s; base += CH) {
      long long sb = min(CH, s - base); int W = (int)((sb + 63) / 64);
      // forward: F[t] for layers t0 .. t0+P-1 (offset k = 0..P-1)
      vector<vector<u64>> F(P);
      for (int tt = 0; tt < P; tt++) F[tt].assign(lay[tt].size() * (size_t)W, 0);
      for (long long i = 0; i < sb; i++) F[t0][(size_t)(base + i) * W + (i >> 6)] |= 1ULL << (i & 63);
      int tt = t0;
      for (int st = 0; st < P - 1; st++) {
        int t1 = (tt + 1) % P;
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
      // backward: tau = L (layer t0, identity on the batch) down to 0; at tau < P intersect with F
      vector<u64> cur(lay[t0].size() * (size_t)W, 0), nxt;
      for (long long i = 0; i < sb; i++) cur[(size_t)(base + i) * W + (i >> 6)] |= 1ULL << (i & 63);
      int curLayer = t0;
      for (int tau = L - 1; tau >= 0; tau--) {
        int lt = ((t0 + tau) % P + P) % P;   // layer of time tau; its successors are in curLayer = lt+1
        nxt.assign(lay[lt].size() * (size_t)W, 0);
        for (size_t k = 0; k < lay[lt].size(); k++) {
          int32_t u = lay[lt][k]; u64* d = &nxt[k * W];
          int32_t a = Lv.o0[u], c = Lv.o1[u];
          if (a >= 0 && alive[a]) { const u64* sr = &cur[(size_t)pos[a] * W]; for (int w = 0; w < W; w++) d[w] |= sr[w]; }
          if (c >= 0 && alive[c]) { const u64* sr = &cur[(size_t)pos[c] * W]; for (int w = 0; w < W; w++) d[w] |= sr[w]; }
          if (tau < P) {   // offset k(u) = tau: exact iff F(u) & B(u) != 0
            const u64* f = &F[lt][k * W]; for (int w = 0; w < W; w++) if (f[w] & d[w]) { ex[u] = 1; break; }
          }
        }
        cur.swap(nxt); curLayer = lt;
      }
      (void)m; (void)curLayer;
    }
  }
  long long kept = 0;
  for (size_t i = 0; i < n; i++) { if (alive[i] && !ex[i]) alive[i] = 0; kept += alive[i]; }
  return kept;
}

static void compact(const Level& Lv, Level& Out) {
  size_t n = Lv.n(); vector<int32_t> nid(n, -1); size_t m = 0;
  for (size_t i = 0; i < n; i++) if (alive[i]) nid[i] = (int32_t)m++;
  Out.K = Lv.K; Out.t.resize(m); Out.dig.resize(m); Out.lc.resize(m); Out.pdig.resize(m); Out.o0.resize(m); Out.o1.resize(m);
  if (CHECK || KEEP || ANCON || PRIMON) Out.par.resize(m);
  for (size_t i = 0; i < n; i++) if (alive[i]) {
    int32_t k = nid[i]; Out.t[k] = Lv.t[i]; Out.dig[k] = Lv.dig[i]; Out.lc[k] = Lv.lc[i]; Out.pdig[k] = Lv.pdig[i];
    int32_t a = Lv.o0[i], c = Lv.o1[i];
    Out.o0[k] = (a >= 0) ? nid[a] : -1; Out.o1[k] = (c >= 0) ? nid[c] : -1;
    if (CHECK || KEEP || ANCON || PRIMON) Out.par[k] = Lv.par[i];
  }
}

// ---------- r12e (1): TOP99 / TOPUU closed-L-walk test on the compacted kept level ----------
static int fband(int u) { return 2 * ((u + (u >= b ? 1 : 0)) % b); }
static vector<char> isBand;   // f-periodic values != b-1
static void initBand() {
  isBand.assign(NV, 0);
  for (int u = 0; u < NV; u++) { if (u == b - 1) continue; int x = u; bool per = false; for (int k = 0; k < 2 * NV + 2; k++) { x = fband(x); if (x == u) { per = true; break; } } isBand[u] = per; }
}
struct TopRes { long long n99 = 0, k99 = 0, nUU = 0, kUU = 0; int c99 = 0, cUU = 0; };
static FILE* hitf = nullptr;
static void dumpSubset(Level& Lv, int K, const char* tag) {
  if (!KEEP || DUMPF.empty()) return;
  if (!hitf) hitf = fopen(DUMPF.c_str(), "w");
  fprintf(hitf, "# %s K=%d L=", tag, K); for (int L : Ls) fprintf(hitf, "%d,", L); fprintf(hitf, "\n");
  for (size_t i = 0; i < Lv.n(); i++) if (alive[i]) {
    vector<int> x = recon(K - 1, i);
    int32_t a = Lv.o0[i], c = Lv.o1[i]; if (a >= 0 && !alive[a]) a = -1; if (c >= 0 && !alive[c]) c = -1;
    fprintf(hitf, "%zu %d %d %d :", i, (int)Lv.t[i], a, c); for (int d : x) fprintf(hitf, " %d", d); fprintf(hitf, "\n");
  }
  fflush(hitf);
}
static TopRes topCheck(Level& Lv, int K) {
  TopRes r; size_t n = Lv.n(); long long sm;
  long long saveCH = CHUNK; if (CHUNK == 0) CHUNK = 4096;
  // TOP99
  alive.assign(n, 0);
  if (K >= 2) for (size_t i = 0; i < n; i++) if (Lv.dig[i] == b - 1 && Lv.pdig[i] == b - 1) { alive[i] = 1; r.n99++; }
  if (r.n99) {
    trim(Lv); long long k = 0; for (size_t i = 0; i < n; i++) k += alive[i];
    if (k) k = sccFilter(Lv);
    if (k) { int ex = exactTest(Lv, sm); if (ex == 1) { trim(Lv); k = 0; for (size_t i = 0; i < n; i++) k += alive[i]; r.c99 = (k > 0); } else k = 0; }
    r.k99 = k;
    if (r.c99) { if (EXACTSET) { r.k99 = exactSet(Lv); } dumpSubset(Lv, K, "TOP99_HIT"); }
  }
  // TOPUU (edges restricted to top digit u -> f(u))
  alive.assign(n, 0);
  if (K >= 2) for (size_t i = 0; i < n; i++) if (Lv.dig[i] == Lv.pdig[i] && isBand[Lv.dig[i]]) { alive[i] = 1; r.nUU++; }
  if (r.nUU) {
    vector<int32_t> s0 = Lv.o0, s1 = Lv.o1;
    for (size_t i = 0; i < n; i++) if (alive[i]) {
      int fu = fband(Lv.dig[i]);
      if (Lv.o0[i] >= 0 && Lv.dig[Lv.o0[i]] != fu) Lv.o0[i] = -1;
      if (Lv.o1[i] >= 0 && Lv.dig[Lv.o1[i]] != fu) Lv.o1[i] = -1;
    }
    trim(Lv); long long k = 0; for (size_t i = 0; i < n; i++) k += alive[i];
    if (k) k = sccFilter(Lv);
    if (k) { int ex = exactTest(Lv, sm); if (ex == 1) { trim(Lv); k = 0; for (size_t i = 0; i < n; i++) k += alive[i]; r.cUU = (k > 0); } else k = 0; }
    r.kUU = k;
    if (r.cUU) { if (EXACTSET) { r.kUU = exactSet(Lv); } dumpSubset(Lv, K, "TOPUU_HIT"); }
    Lv.o0.swap(s0); Lv.o1.swap(s1);
  }
  CHUNK = saveCH;
  return r;
}

// ---------- r12e (3): WL hash of the attributed kept graph ----------
static inline u64 mix(u64 x) { x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ULL; x ^= x >> 33; return x; }
static u64 wlHash(const Level& Lv, int rounds) {
  size_t n = Lv.n(); vector<u64> c(n), c2(n);
  for (size_t i = 0; i < n; i++) c[i] = mix(((u64)Lv.t[i] << 16) ^ ((u64)Lv.dig[i] << 8) ^ (u64)Lv.lc[i] ^ 0x9e3779b97f4a7c15ULL);
  for (int r = 0; r < rounds; r++) {
    for (size_t i = 0; i < n; i++) {
      u64 a = Lv.o0[i] >= 0 ? c[Lv.o0[i]] : 0x1234567ULL, d = Lv.o1[i] >= 0 ? c[Lv.o1[i]] : 0x7654321ULL;
      c2[i] = mix(c[i] ^ mix(a + 0x51ULL) ^ mix(mix(d) + 0x77ULL));
    }
    c.swap(c2);
  }
  sort(c.begin(), c.end());
  u64 h = 0xcbf29ce484222325ULL; for (u64 v : c) h = mix(h ^ v);
  return h;
}
static void gdump(const Level& Lv, int K) {
  string fn = GDUMPF + "." + to_string(K); FILE* f = fopen(fn.c_str(), "w"); if (!f) return;
  fprintf(f, "# khxt gdump b=%d P=%d K=%d n=%zu L=", b, P, K, Lv.n()); for (int L : Ls) fprintf(f, "%d,", L); fprintf(f, "\n# idx t dig lc pdig o0 o1\n");
  for (size_t i = 0; i < Lv.n(); i++) fprintf(f, "%zu %d %d %d %d %d %d\n", i, (int)Lv.t[i], (int)Lv.dig[i], (int)Lv.lc[i], (int)Lv.pdig[i], Lv.o0[i], Lv.o1[i]);
  fclose(f);
}


// ---------- r13c: primitive test on the compact kept level ----------
// Requires -exactset compact level comp (Ls single L, multiple of d0). Windows: flat byte array WIN (n x K).
static vector<uint8_t> WIN; static int WINK = 0;
static set<int> PRIMK; static int PRIMFROM = 1; static bool PRIMALL = false;
static void updateWindows(const Level& comp, int K) {
  size_t m = comp.n();
  vector<uint8_t> nw(m * K);
  if (K == 1) { for (size_t k = 0; k < m; k++) nw[k] = comp.dig[k]; }
  else { for (size_t k = 0; k < m; k++) { size_t p = (size_t)comp.par[k]; memcpy(&nw[k * K], &WIN[p * (K - 1)], K - 1); nw[k * K + K - 1] = comp.dig[k]; } }
  WIN.swap(nw); WINK = K;
}
static inline int lcpWin(size_t u, size_t v, int K) { const uint8_t* a = &WIN[u * K]; const uint8_t* c = &WIN[v * K]; for (int i = 0; i < K; i++) if (a[i] != c[i]) return i; return K; }
// returns min over off-diagonal closure pairs (u,u') of lcp; Rig = min lcp. nd = number of off-diagonal pairs, nsrc = sources with any off-diag.
static void primTest(const Level& Lv, int K, int d0, int L, long long& minlcp, long long& nd, long long& ntrivial, FILE* witf) {
  minlcp = K; nd = 0; ntrivial = 0;
  size_t n = Lv.n();
  vector<vector<int32_t>> lay(P);
  for (size_t i = 0; i < n; i++) lay[Lv.t[i]].push_back((int32_t)i);
  vector<int32_t> pos(n, -1);
  for (int tt = 0; tt < P; tt++) for (size_t k = 0; k < lay[tt].size(); k++) pos[lay[tt][k]] = (int32_t)k;
  long long CH = 4096;
  for (int t0 = 0; t0 < P; t0++) {
    long long s = lay[t0].size();
    for (long long base = 0; base < s; base += CH) {
      long long sb = min(CH, s - base); int W = (int)((sb + 63) / 64);
      // forward d0 steps
      vector<u64> cur(lay[t0].size() * (size_t)W, 0), nxt;
      for (long long i = 0; i < sb; i++) cur[(size_t)(base + i) * W + (i >> 6)] |= 1ULL << (i & 63);
      int tt = t0;
      for (int st = 0; st < d0; st++) {
        int t1 = (tt + 1) % P;
        nxt.assign(lay[t1].size() * (size_t)W, 0);
        for (size_t k = 0; k < lay[tt].size(); k++) {
          int32_t u = lay[tt][k]; const u64* src = &cur[k * W];
          bool any = false; for (int w = 0; w < W; w++) if (src[w]) { any = true; break; }
          if (!any) continue;
          int32_t a = Lv.o0[u], c = Lv.o1[u];
          if (a >= 0) { u64* d = &nxt[(size_t)pos[a] * W]; for (int w = 0; w < W; w++) d[w] |= src[w]; }
          if (c >= 0) { u64* d = &nxt[(size_t)pos[c] * W]; for (int w = 0; w < W; w++) d[w] |= src[w]; }
        }
        cur.swap(nxt); tt = t1;
      }
      vector<u64> Fv = cur; // F at layer t0 (time d0)
      // backward L-d0 steps: B_L = identity on layer t0; B_tau from B_{tau+1}
      vector<u64> bc(lay[t0].size() * (size_t)W, 0), bn;
      for (long long i = 0; i < sb; i++) bc[(size_t)(base + i) * W + (i >> 6)] |= 1ULL << (i & 63);
      int lt = t0; // bc is at layer t0 (time L)
      for (int tau = L - 1; tau >= d0; tau--) {
        int ltau = ((t0 + tau) % P + P) % P;
        bn.assign(lay[ltau].size() * (size_t)W, 0);
        for (size_t k = 0; k < lay[ltau].size(); k++) {
          int32_t u = lay[ltau][k]; u64* d = &bn[k * W];
          int32_t a = Lv.o0[u], c = Lv.o1[u];
          if (a >= 0) { const u64* sr = &bc[(size_t)pos[a] * W]; for (int w = 0; w < W; w++) d[w] |= sr[w]; }
          if (c >= 0) { const u64* sr = &bc[(size_t)pos[c] * W]; for (int w = 0; w < W; w++) d[w] |= sr[w]; }
        }
        bc.swap(bn); lt = ltau;
      }
      // now bc at layer t0 (time d0), Fv at layer t0
      for (size_t kp = 0; kp < lay[t0].size(); kp++) {
        const u64* f = &Fv[kp * W]; const u64* g = &bc[kp * W];
        for (int w = 0; w < W; w++) { u64 e = f[w] & g[w]; while (e) { int bit = __builtin_ctzll(e); e &= e - 1;
          long long si = base + (long long)w * 64 + bit; int32_t us = lay[t0][si], ud = lay[t0][kp];
          if (us == ud) { ntrivial++; continue; }
          nd++; int l = lcpWin(us, ud, K); if (l < minlcp) { minlcp = l; if (witf) fprintf(witf, "K=%d t0=%d lcp=%d u=%d u'=%d\n", K, t0, l, us, ud); }
        } }
      }
    }
  }
}
int main(int argc, char** argv) {
  if (argc < 3) { fprintf(stderr, "usage: khxt b (-g WORD | -f FILE) [khx options] [-top] [-topevery N] [-stophit] [-exactset] [-inv] [-gdump K1,K2 -gfile F] [-dump F] [-wdump F]\n"); return 2; }
  b = atoi(argv[1]); NV = 2 * b - 1;
  string gword, gfile, Lspec;
  for (int i = 2; i < argc; i++) { string a = argv[i];
    if (a == "-g") gword = argv[++i]; else if (a == "-f") gfile = argv[++i]; else if (a == "-L") Lspec = argv[++i];
    else if (a == "-kmax") KMAX = atoi(argv[++i]); else if (a == "-kmin") KMIN = atoi(argv[++i]);
    else if (a == "-nodecap") NODECAP = atoll(argv[++i]); else if (a == "-sec") SEC = atof(argv[++i]);
    else if (a == "-smax") SMAX = atoll(argv[++i]); else if (a == "-batch") CHUNK = atoll(argv[++i]);
    else if (a == "-periods") PERIODS = true; else if (a == "-noexact") USE_EXACT = false; else if (a == "-noscc") USE_SCC = false;
    else if (a == "-v") VERB = true;
    else if (a == "-dump") { DUMPF = argv[++i]; KEEP = true; }
    else if (a == "-top") TOPCHK = true; else if (a == "-topevery") TOPEVERY = atoi(argv[++i]); else if (a == "-stophit") STOPHIT = true;
    else if (a == "-exactset") EXACTSET = true; else if (a == "-inv") INV = true;
    else if (a == "-gdump") { string s = argv[++i]; size_t q = 0; while (q < s.size()) { size_t r = s.find(',', q); if (r == string::npos) r = s.size(); GDUMP.insert(atoi(s.substr(q, r - q).c_str())); q = r + 1; } }
    else if (a == "-gfile") GDUMPF = argv[++i];
    else if (a == "-wdump") { WDUMPF = argv[++i]; KEEP = true; }
    else if (a == "-prim") { PRIMD = atoi(argv[++i]); PRIMON = true; } else if (a == "-primk") { string s2 = argv[++i]; size_t q = 0; while (q < s2.size()) { size_t r = s2.find(',', q); if (r == string::npos) r = s2.size(); PRIMK.insert(atoi(s2.substr(q, r - q).c_str())); q = r + 1; } PRIMALL = PRIMK.empty(); } else if (a == "-primfrom") PRIMFROM = atoi(argv[++i]);
    else if (a == "-coreproj") { CPD = atoi(argv[++i]); CPF = argv[++i]; KEEP = true; }
    else if (a == "-anc") { AND_ = atoi(argv[++i]); ANF = argv[++i]; ANCON = true; }
    else { fprintf(stderr, "unknown arg %s\n", a.c_str()); return 2; } }
  if (EXACTSET && CHUNK == 0) CHUNK = 4096;
  initBand();
  vector<string> words;
  if (!gword.empty()) words.push_back(gword);
  if (!gfile.empty()) { FILE* f = fopen(gfile.c_str(), "r"); if (!f) { perror("open"); return 2; } char buf[512];
    while (fgets(buf, sizeof buf, f)) { string s(buf); size_t k = s.find_first_of(" \t\r\n"); if (k != string::npos) s = s.substr(0, k); if (!s.empty()) words.push_back(s); } fclose(f); }
  for (auto& gs : words) {
    double t0 = now();
    P = gs.size(); pat.assign(P, 0); for (int i = 0; i < P; i++) pat[i] = gs[i] - '0';
    Ls.clear();
    if (Lspec.empty()) Ls.push_back(P);
    else { size_t q = 0; while (q < Lspec.size()) { size_t r = Lspec.find(',', q); if (r == string::npos) r = Lspec.size(); int L = atoi(Lspec.substr(q, r - q).c_str()); if (L % P == 0 && L > 0) Ls.push_back(L); q = r + 1; } }
    if (Ls.empty()) { printf("KHXT b=%d p=%d g=%s BADL\n", b, P, gs.c_str()); continue; }
    Level cur, nxt, comp; buildLevel1(cur);
    for (auto* l : ALL) delete l; ALL.clear();
    long long maxn = 0; int K = 1; string status, reason; long long keptLast = 0;
    int first99 = -1, firstUU = -1; long long maxk99 = 0, maxkUU = 0;
    while (true) {
      maxn = max<long long>(maxn, (long long)cur.n());
      alive.assign(cur.n(), 1);
      if (KEEP) ALL.push_back(new Level(cur));
      trim(cur);
      size_t kept = 0; for (size_t i = 0; i < cur.n(); i++) kept += alive[i];
      size_t keptScc = 0;
      if (kept && USE_SCC) kept = sccFilter(cur);
      keptScc = kept;
      long long smallest = -1; int ex = -1;
      if (kept && USE_EXACT) { ex = exactTest(cur, smallest); if (ex == 0) kept = 0; else if (ex == 1) { trim(cur); kept = 0; for (size_t i = 0; i < cur.n(); i++) kept += alive[i]; } }
      size_t keptRef = kept;
      if (kept && EXACTSET) kept = exactSet(cur);
      if (VERB) fprintf(stderr, "  K=%d nodes=%zu scc=%zu kept=%zu exactset=%zu exact=%d smallest=%lld t=%.2f\n", K, cur.n(), keptScc, keptRef, kept, ex, smallest, now() - t0);
      if (kept == 0) { status = "DIES"; break; }
      keptLast = kept;
      compact(cur, comp);
      if (KEEP) { delete ALL.back(); ALL.back() = new Level(comp); }
      if (ANCON) { AncLv a; a.par = comp.par; a.dig = comp.dig; a.t = comp.t; if (K == 1) a.par.assign(comp.n(), -1); ANC.push_back(std::move(a)); }
      if (PRIMON) { updateWindows(comp, K); if (PRIMK.empty() ? (K >= PRIMFROM) : PRIMK.count(K) > 0) { long long ml, nd, ntr; primTest(comp, K, PRIMD, Ls[0], ml, nd, ntr, nullptr); fprintf(stderr, "  PRIM K=%d kept=%zu d0=%d L=%d Rig=%lld offdiag=%lld trivial=%lld t=%.2f\n", K, comp.n(), PRIMD, Ls[0], ml, nd, ntr, now() - t0); } }
      if (INV) { u64 h = wlHash(comp, 6); fprintf(stderr, "  INV K=%d n=%zu h=%016llx\n", K, comp.n(), (unsigned long long)h); }
      if (GDUMP.count(K) && !GDUMPF.empty()) gdump(comp, K);
      bool hit = false;
      if (TOPCHK && (K % TOPEVERY == 0 || K >= KMAX)) {
        TopRes r = topCheck(comp, K);
        maxk99 = max(maxk99, r.k99); maxkUU = max(maxkUU, r.kUU);
        if (r.c99 && first99 < 0) first99 = K; if (r.cUU && firstUU < 0) firstUU = K;
        fprintf(stderr, "  TOP K=%d kept=%zu n99=%lld c99=%d k99=%lld nUU=%lld cUU=%d kUU=%lld\n", K, comp.n(), r.n99, r.c99, r.k99, r.nUU, r.cUU, r.kUU);
        if (r.c99 || r.cUU) { hit = true; printf("KHXT_HIT b=%d p=%d g=%s K=%d c99=%d k99=%lld cUU=%d kUU=%lld\n", b, P, gs.c_str(), K, r.c99, r.k99, r.cUU, r.kUU); fflush(stdout); }
      }
      if (hit && STOPHIT) { status = "SURVIVES"; reason = "tophit"; break; }
      if (K >= KMAX) { status = "SURVIVES"; reason = "kmax"; break; }
      if (now() - t0 > SEC) { status = "SURVIVES"; reason = "time"; break; }
      if ((long long)comp.n() * NV > NODECAP) { status = "SURVIVES"; reason = "nodecap"; break; }
      buildChild(comp, nxt);
      cur.t.swap(nxt.t); cur.dig.swap(nxt.dig); cur.lc.swap(nxt.lc); cur.pdig.swap(nxt.pdig); cur.o0.swap(nxt.o0); cur.o1.swap(nxt.o1); cur.par.swap(nxt.par); cur.K = nxt.K;
      K++;
    }
    if (!WDUMPF.empty() && status == "SURVIVES") {   // final kept level with full windows (needs KEEP chains)
      FILE* df = fopen(WDUMPF.c_str(), "w");
      fprintf(df, "# khxt wdump b=%d p=%d g=%s K=%d L=", b, P, gs.c_str(), K); for (int L : Ls) fprintf(df, "%d,", L); fprintf(df, "\n# idx t o0 o1 : x_0 .. x_{K-1}\n");
      for (size_t i = 0; i < comp.n(); i++) { vector<int> x = recon(K - 1, i);
        fprintf(df, "%zu %d %d %d :", i, (int)comp.t[i], comp.o0[i], comp.o1[i]); for (int d : x) fprintf(df, " %d", d); fprintf(df, "\n"); }
      fclose(df);
    }
    if (CPD > 0 && status == "SURVIVES") {   // ancestors (projections) of the final kept set at every level; dump level K-CPD
      vector<vector<uint8_t>> mk(K); mk[K - 1].assign(ALL[K - 1]->n(), 1);
      for (int k = K - 1; k >= 1; k--) { mk[k - 1].assign(ALL[k - 1]->n(), 0); for (size_t i = 0; i < ALL[k]->n(); i++) if (mk[k][i]) mk[k - 1][ALL[k]->par[i]] = 1; }
      FILE* cf = fopen(CPF.c_str(), "w");
      fprintf(cf, "# khxt coreproj b=%d p=%d g=%s K=%d D=%d L=", b, P, gs.c_str(), K, CPD); for (int L : Ls) fprintf(cf, "%d,", L); fprintf(cf, "\n# ANC k kept_k ancestors_k\n");
      for (int k = 1; k <= K; k++) { long long c = 0; for (uint8_t v : mk[k - 1]) c += v; fprintf(cf, "ANC %d %zu %lld\n", k, ALL[k - 1]->n(), c); }
      int kd = K - CPD; if (kd >= 1) {
        Level* Lk = ALL[kd - 1];
        fprintf(cf, "# level %d ancestors: idx t o0 o1 : x_0 .. x_{k-1}  (edges restricted to ancestors)\n", kd);
        for (size_t i = 0; i < Lk->n(); i++) if (mk[kd - 1][i]) { vector<int> x = recon(kd - 1, i);
          int32_t a = Lk->o0[i], c2 = Lk->o1[i]; if (a >= 0 && !mk[kd - 1][a]) a = -1; if (c2 >= 0 && !mk[kd - 1][c2]) c2 = -1;
          fprintf(cf, "%zu %d %d %d :", i, (int)Lk->t[i], a, c2); for (int d : x) fprintf(cf, " %d", d); fprintf(cf, "\n"); }
      }
      fclose(cf);
    }
    if (ANCON && status == "SURVIVES" && (int)ANC.size() == K) {   // ancestors of the final level in the light store
      vector<vector<uint8_t>> mk(K); mk[K - 1].assign(ANC[K - 1].dig.size(), 1);
      for (int k = K - 1; k >= 1; k--) { mk[k - 1].assign(ANC[k - 1].dig.size(), 0); for (size_t i = 0; i < ANC[k].dig.size(); i++) if (mk[k][i]) mk[k - 1][ANC[k].par[i]] = 1; }
      FILE* cf = fopen(ANF.c_str(), "w");
      fprintf(cf, "# khxt anc b=%d p=%d g=%s K=%d D=%d L=", b, P, gs.c_str(), K, AND_); for (int L : Ls) fprintf(cf, "%d,", L); fprintf(cf, "\n# ANC k kept_k ancestors_k\n");
      for (int k = 1; k <= K; k++) { long long c = 0; for (uint8_t v : mk[k - 1]) c += v; fprintf(cf, "ANC %d %zu %lld\n", k, ANC[k - 1].dig.size(), c); }
      int kd = K - AND_; if (kd >= 1) {
        fprintf(cf, "# level %d ancestors: idx t -1 -1 : x_0 .. x_{k-1}\n", kd);
        for (size_t i = 0; i < ANC[kd - 1].dig.size(); i++) if (mk[kd - 1][i]) {
          vector<int> x(kd); size_t id = i; for (int k = kd; k >= 1; k--) { x[k - 1] = ANC[k - 1].dig[id]; id = (size_t)ANC[k - 1].par[id]; }
          fprintf(cf, "%zu %d -1 -1 :", i, (int)ANC[kd - 1].t[i]); for (int d : x) fprintf(cf, " %d", d); fprintf(cf, "\n"); }
      }
      fclose(cf);
    }
    ANC.clear();
    string tops = TOPCHK ? (" top99_first=" + to_string(first99) + " topUU_first=" + to_string(firstUU)) : string("");
    if (status == "DIES") printf("KHXT b=%d p=%d g=%s DIES K=%d maxnodes=%lld secs=%.3f%s\n", b, P, gs.c_str(), K, maxn, now() - t0, tops.c_str());
    else printf("KHXT b=%d p=%d g=%s SURVIVES K=%d kept=%lld reason=%s maxnodes=%lld secs=%.3f%s\n", b, P, gs.c_str(), K, keptLast, reason.c_str(), maxn, now() - t0, tops.c_str());
    fflush(stdout);
  }
  if (hitf) fclose(hitf);
  return 0;
}
