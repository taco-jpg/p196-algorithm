// khx.cpp (r12b): K-head closed-walk filter for an overflow word, grown one coordinate (spatial position) at a time.
//
// Graph G_K (three_divides_r/PROOF.md, EXTERIOR.md 2.5): node (x_0..x_{K-1}, t), x_0 in 1..2b-2, x_i in 0..2b-2, t in Z/P;
// for h in {0,1}: (y,g) = trans(x,h) (backward carries H_K=h, H_i=floor((x_i+H_{i+1})/b), g=H_0; forward carries L_0=0,
// L_{i+1}=floor((x_i+L_i)/b); y_i=(x_i+L_i)%b + [g=0: (x_i+H_{i+1})%b ; g=1: i=0 ? 1 : (x_{i-1}+H_i)%b]); keep the edge
// (x,t)->(y,t+1) iff g = pat[t].   A closed walk of length L (P | L) is what every exterior / band template of period L gives.
//
// Incremental construction (equivalent to trans, see PROOF): a level-K node is (parent level-(K-1) node j, top digit v).
// Its edge for bit h uses the parent's edge for bit h' = floor((v+h)/b) (projection lemma A3) and the new top digit
//     y_{K-1} = (v + Lc_j) % b + ( g ? (dig_j + h') % b : (v + h) % b ),   Lc_j = forward carry into position K-1.
// Level 1 is built directly from trans.   Validation: -check compares every edge with a direct trans() (slow).
//
// Pruning per level (each step keeps a SUPERSET of the nodes lying on closed walks of an admissible length L in Ls):
//   1. trim: iteratively drop nodes without in- or out-edge;
//   2. SCC: keep nodes of cyclic SCCs whose period divides some L in Ls (Lemma A4 of three_divides_r, "period | L");
//   3. exact closure (if the smallest phase layer has <= SMAX nodes): multi-source bitset propagation over m = L/P laps from
//      the smallest layer t0; C = sources that return to themselves.  C empty for all L  <=>  no closed walk of length L
//      in G_K (every such walk crosses layer t0).  Otherwise keep only nodes reachable in one lap from C and reaching C in one
//      lap (every node of such a walk is), then trim again.
// DIES at K  <=>  the kept set is empty  =>  G_K has no closed walk of any length in Ls.
//
// usage: khx b (-g WORD | -f FILE) [-pat] [-L L1,L2,..] [-kmin K] [-kmax K] [-nodecap N] [-sec S] [-smax S] [-noexact] [-noscc] [-v] [-check]
//   default L = |WORD|.  Output: one line per word
//   KHX b=.. p=.. g=.. DIES K=k nodes=<max level size> secs=..      or   KHX ... SURVIVES K=<last complete level> kept=.. reason=kmax|nodecap|time
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
static bool PERIODS = false, ALLM = false; static long long CHUNK = 0; /* r12b v3: CHUNK>0 -> exact test always runs, sources in batches of CHUNK */ static long long SMAX = 4096; static long long NODECAP = 200000000LL; static double SEC = 1e18; static int KMAX = 60, KMIN = 1;
static double now() { return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }

struct Level {
  int K = 0;
  vector<uint8_t> t, dig, lc;     // phase, top digit x_{K-1}, forward carry into position K
  vector<int32_t> o0, o1;         // out-edge for h=0 / h=1 (only label-matching edges), -1 = none
  vector<int32_t> par;            // parent index (for -check reconstruction only)
  size_t n() const { return t.size(); }
};

// ---------- direct trans (for -check) ----------
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
  L1.K = 1; L1.t.resize(n); L1.dig.resize(n); L1.lc.resize(n); L1.o0.assign(n, -1); L1.o1.assign(n, -1); L1.par.assign(n, -1);
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

// children of every node of the (compacted) parent level: id = j*NV + v
static bool buildChild(const Level& Pa, Level& C) {
  size_t m = Pa.n(); size_t n = m * NV;
  if ((long long)n > NODECAP) return false;
  C.K = Pa.K + 1; C.t.resize(n); C.dig.resize(n); C.lc.resize(n); C.o0.assign(n, -1); C.o1.assign(n, -1);
  if (CHECK || KEEP) C.par.resize(n);
  for (size_t j = 0; j < m; j++) {
    int tt = Pa.t[j], g = pat[tt], dj = Pa.dig[j], lj = Pa.lc[j];
    for (int v = 0; v < NV; v++) {
      size_t id = j * NV + v;
      C.t[id] = tt; C.dig[id] = v; C.lc[id] = (v + lj >= b); if (CHECK || KEEP) C.par[id] = (int32_t)j;
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

// reconstruct x of a node (needs par chains of all levels) -- check mode only
static vector<Level*> ALL;
static vector<int> recon(int lev, size_t id) {
  vector<int> x(lev + 1);
  for (int k = lev; k >= 0; k--) { x[k] = ALL[k]->dig[id]; id = (size_t)ALL[k]->par[id]; }
  return x;
}

// ---------- pruning ----------
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
  // reverse CSR over alive edges
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

// SCC (iterative Tarjan) on alive nodes; keep cyclic SCCs with period | some L.
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
  // period per component
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
    per[c] = gg;   // 0 = acyclic (single node without self-loop)
  }
  size_t kept = 0;
  for (size_t i = 0; i < n; i++) if (alive[i]) {
    long long qq = per[compv[i]]; bool ok = false;
    if (ALLM) ok = (qq > 0);   // -allm: every multiple of P is admissible, keep every cyclic SCC (exact test must be off)
    else if (qq > 0) for (int L : Ls) if (L % qq == 0) { ok = true; break; }
    if (!ok) alive[i] = 0; else kept++;
  }
  if (PERIODS) {   // multiset of periods of the kept cyclic SCCs (with node counts)
    map<long long, pair<long long, long long>> pm;   // period -> (#SCCs, #nodes)
    vector<char> seenc(nc, 0);
    for (size_t i = 0; i < n; i++) if (alive[i]) { int c = compv[i]; pm[per[c]].second++; if (!seenc[c]) { seenc[c] = 1; pm[per[c]].first++; } }
    fprintf(stderr, "  PERIODS K=%d", Lv.K); for (auto& kv : pm) fprintf(stderr, " %lld:%lldx%lld", kv.first, kv.second.first, kv.second.second); fprintf(stderr, "\n");
  }
  return kept;
}

// exact closure test from the smallest phase layer.  returns -1 if skipped, 0 if no closed walk (dies), 1 if some.
static int exactTest(Level& Lv, long long& smallest) {
  size_t n = Lv.n();
  vector<long long> cnt(P, 0);
  for (size_t i = 0; i < n; i++) if (alive[i]) cnt[Lv.t[i]]++;
  int t0 = 0; for (int tt = 1; tt < P; tt++) if (cnt[tt] < cnt[t0]) t0 = tt;
  smallest = cnt[t0];
  if (cnt[t0] == 0) return 0;
  if (CHUNK == 0 && cnt[t0] > SMAX) return -1;
  // layer lists
  vector<vector<int32_t>> lay(P);
  for (size_t i = 0; i < n; i++) if (alive[i]) lay[Lv.t[i]].push_back((int32_t)i);
  vector<int32_t> pos(n, -1);
  for (int tt = 0; tt < P; tt++) for (size_t k = 0; k < lay[tt].size(); k++) pos[lay[tt][k]] = (int32_t)k;
  long long s = cnt[t0];
  int maxm = 0; for (int L : Ls) maxm = max(maxm, L / P);
  vector<char> wantm(maxm + 1, 0); for (int L : Ls) wantm[L / P] = 1;
  vector<uint8_t> Cf((size_t)s, 0);   // sources (layer t0) that return to themselves after m laps, for some L = mP in Ls
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
  // refine: forward one lap from C, backward one lap to C
  vector<uint8_t> fm(n, 0), bm(n, 0);
  for (long long i = 0; i < s; i++) if (Cf[i]) { fm[lay[t0][i]] = 1; bm[lay[t0][i]] = 1; }
  int tt = t0;
  for (int st = 0; st < P - 1; st++) {
    for (int32_t u : lay[tt]) if (fm[u]) { int32_t a = Lv.o0[u], c = Lv.o1[u]; if (a >= 0 && alive[a]) fm[a] = 1; if (c >= 0 && alive[c]) fm[c] = 1; }
    tt = (tt + 1) % P;
  }
  // backward: process layers t0-1, t0-2, ..., t0+1 : node u marked if an out-neighbour is marked (layer t0 marks = C)
  tt = (t0 + P - 1) % P;
  for (int st = 0; st < P - 1; st++) {
    for (int32_t u : lay[tt]) { int32_t a = Lv.o0[u], c = Lv.o1[u]; if ((a >= 0 && alive[a] && bm[a]) || (c >= 0 && alive[c] && bm[c])) bm[u] = 1; }
    tt = (tt + P - 1) % P;
  }
  for (size_t i = 0; i < n; i++) if (alive[i] && !(fm[i] && bm[i])) alive[i] = 0;
  return 1;
}

static void compact(const Level& Lv, Level& Out) {
  size_t n = Lv.n(); vector<int32_t> nid(n, -1); size_t m = 0;
  for (size_t i = 0; i < n; i++) if (alive[i]) nid[i] = (int32_t)m++;
  Out.K = Lv.K; Out.t.resize(m); Out.dig.resize(m); Out.lc.resize(m); Out.o0.resize(m); Out.o1.resize(m);
  if (CHECK || KEEP) Out.par.resize(m);
  for (size_t i = 0; i < n; i++) if (alive[i]) {
    int32_t k = nid[i]; Out.t[k] = Lv.t[i]; Out.dig[k] = Lv.dig[i]; Out.lc[k] = Lv.lc[i];
    int32_t a = Lv.o0[i], c = Lv.o1[i];
    Out.o0[k] = (a >= 0) ? nid[a] : -1; Out.o1[k] = (c >= 0) ? nid[c] : -1;
    if (CHECK || KEEP) Out.par[k] = Lv.par[i];
  }
}

static long long checkedEdges = 0, checkFails = 0;
static long long checkedAbsent = 0;
static void checkLevel(int lev, Level& Lv) { // every node's edges vs direct trans (needs full chains: store all levels)
  size_t n = Lv.n();
  set<pair<int, vector<int>>> prevSet;   // (phase, window) of every kept node of the compacted level lev-1
  if (lev >= 1) for (size_t j = 0; j < ALL[lev - 1]->n(); j++) prevSet.insert(make_pair((int)ALL[lev - 1]->t[j], recon(lev - 1, j)));
  for (size_t i = 0; i < n; i++) {
    vector<int> x = recon(lev, i);
    for (int h = 0; h < 2; h++) {
      vector<int> y; int g; trans(x, h, y, g);
      int32_t tg = h ? Lv.o1[i] : Lv.o0[i];
      bool want = (g == pat[Lv.t[i]]);
      // edge exists in full G_K iff want; our edge may be -1 also when target parent was pruned (allowed); if present must match y
      if (tg >= 0) {
        checkedEdges++;
        vector<int> z = recon(lev, tg);
        if (!want || z != y || Lv.t[tg] != (Lv.t[i] + 1) % P) { checkFails++; if (checkFails < 10) fprintf(stderr, "CHECK FAIL lev=%d node=%zu h=%d\n", lev, i, h); }
      } else if (want) {
        // r12b strengthened check: an absent wanted edge is allowed ONLY if the target projection y[0..lev-1] (phase t+1)
        // was pruned at level lev-1 (then no child of it exists).  At level 1 every node exists, so absence is a failure.
        checkedAbsent++;
        bool present;
        if (lev == 0) present = (y[0] >= 1 && y[0] <= 2 * b - 2);
        else present = prevSet.count(make_pair((Lv.t[i] + 1) % P, vector<int>(y.begin(), y.begin() + lev))) > 0;
        if (present) { checkFails++; if (checkFails < 10) fprintf(stderr, "CHECK FAIL(absent) lev=%d node=%zu h=%d\n", lev, i, h); }
      }
    }
  }
}

// ---- r12e census driver (khxc): everything above this line is byte-identical to r12b src/khx.cpp (lines 1-307). ----
// Differences from khx main(): words are read and processed one at a time (streaming; no word list in memory), and with
// -summary only these lines are printed: every SURVIVES line, every DIES line with K >= KREP, every SAMP-th word (tag " samp"),
// and at the end one line
//   KHXC_SUMMARY words=N dies=D survives=S badl=B hist=K:count,...      (hist = DIES count per death level K).
// The per-word computation (levels, pruning, verdict) is unchanged.
int main(int argc, char** argv) {
  if (argc < 3) { fprintf(stderr, "usage: khxc b (-g WORD | -f FILE) [khx options] [-summary] [-krep K] [-samp S]\n"); return 2; }
  b = atoi(argv[1]); NV = 2 * b - 1;
  string gword, gfile, Lspec; bool SUMMARY = false; int KREP = 1000000; long long SAMP = 0;
  for (int i = 2; i < argc; i++) { string a = argv[i];
    if (a == "-g") gword = argv[++i]; else if (a == "-f") gfile = argv[++i]; else if (a == "-L") Lspec = argv[++i];
    else if (a == "-kmax") KMAX = atoi(argv[++i]); else if (a == "-kmin") KMIN = atoi(argv[++i]);
    else if (a == "-nodecap") NODECAP = atoll(argv[++i]); else if (a == "-sec") SEC = atof(argv[++i]);
    else if (a == "-smax") SMAX = atoll(argv[++i]); else if (a == "-batch") CHUNK = atoll(argv[++i]);
    else if (a == "-periods") PERIODS = true; else if (a == "-allm") { ALLM = true; USE_EXACT = false; } else if (a == "-noexact") USE_EXACT = false; else if (a == "-noscc") USE_SCC = false;
    else if (a == "-v") VERB = true;
    else if (a == "-summary") SUMMARY = true; else if (a == "-krep") KREP = atoi(argv[++i]); else if (a == "-samp") SAMP = atoll(argv[++i]);
    else { fprintf(stderr, "unknown arg %s\n", a.c_str()); return 2; } }
  FILE* inf = nullptr;
  if (!gfile.empty()) { inf = fopen(gfile.c_str(), "r"); if (!inf) { perror("open"); return 2; } }
  map<int, long long> hist; long long nWords = 0, nDies = 0, nSurv = 0, nBad = 0;
  bool usedG = false;
  char buf[512];
  while (true) {
    string gs;
    if (!gword.empty() && !usedG) { gs = gword; usedG = true; }
    else if (inf) { if (!fgets(buf, sizeof buf, inf)) break; string s(buf); size_t k = s.find_first_of(" \t\r\n"); if (k != string::npos) s = s.substr(0, k); if (s.empty()) continue; gs = s; }
    else break;
    long long widx = nWords++;
    double t0 = now();
    P = gs.size(); pat.assign(P, 0); for (int i = 0; i < P; i++) pat[i] = gs[i] - '0';
    Ls.clear();
    if (Lspec.empty()) Ls.push_back(P);
    else { size_t q = 0; while (q < Lspec.size()) { size_t r = Lspec.find(',', q); if (r == string::npos) r = Lspec.size(); int L = atoi(Lspec.substr(q, r - q).c_str()); if (L % P == 0 && L > 0) Ls.push_back(L); q = r + 1; } }
    if (Ls.empty()) { nBad++; printf("KHX b=%d p=%d g=%s BADL\n", b, P, gs.c_str()); continue; }
    Level cur, nxt, comp; buildLevel1(cur);
    long long maxn = 0; int K = 1; string status, reason; long long keptLast = 0;
    while (true) {
      maxn = max<long long>(maxn, (long long)cur.n());
      alive.assign(cur.n(), 1);
      trim(cur);
      size_t kept = 0; for (size_t i = 0; i < cur.n(); i++) kept += alive[i];
      if (kept && USE_SCC) kept = sccFilter(cur);
      long long smallest = -1; int ex = -1;
      if (kept && USE_EXACT) { ex = exactTest(cur, smallest); if (ex == 0) kept = 0; else if (ex == 1) { trim(cur); kept = 0; for (size_t i = 0; i < cur.n(); i++) kept += alive[i]; } }
      if (VERB) fprintf(stderr, "  K=%d nodes=%zu kept=%zu exact=%d smallest=%lld t=%.2f\n", K, cur.n(), kept, ex, smallest, now() - t0);
      if (kept == 0) { status = "DIES"; break; }
      keptLast = kept;
      if (K >= KMAX) { status = "SURVIVES"; reason = "kmax"; break; }
      if (now() - t0 > SEC) { status = "SURVIVES"; reason = "time"; break; }
      compact(cur, comp);
      if ((long long)comp.n() * NV > NODECAP) { status = "SURVIVES"; reason = "nodecap"; break; }
      buildChild(comp, nxt);
      cur.t.swap(nxt.t); cur.dig.swap(nxt.dig); cur.lc.swap(nxt.lc); cur.o0.swap(nxt.o0); cur.o1.swap(nxt.o1); cur.par.swap(nxt.par); cur.K = nxt.K;
      K++;
    }
    bool samp = (SAMP > 0 && widx % SAMP == 0);
    if (status == "DIES") { nDies++; hist[K]++; }
    else nSurv++;
    if (!SUMMARY || status != "DIES" || K >= KREP || samp) {
      if (status == "DIES") printf("KHX b=%d p=%d g=%s DIES K=%d maxnodes=%lld secs=%.3f%s\n", b, P, gs.c_str(), K, maxn, now() - t0, samp ? " samp" : "");
      else printf("KHX b=%d p=%d g=%s SURVIVES K=%d kept=%lld reason=%s maxnodes=%lld secs=%.3f%s\n", b, P, gs.c_str(), K, keptLast, reason.c_str(), maxn, now() - t0, samp ? " samp" : "");
      if (!SUMMARY) fflush(stdout);
    }
  }
  if (inf) fclose(inf);
  if (SUMMARY) {
    printf("KHXC_SUMMARY words=%lld dies=%lld survives=%lld badl=%lld hist=", nWords, nDies, nSurv, nBad);
    bool first = true; for (auto& kv : hist) { printf("%s%d:%lld", first ? "" : ",", kv.first, kv.second); first = false; }
    printf("\n");
  }
  fflush(stdout);
  return 0;
}
