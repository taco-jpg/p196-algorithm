// ifb.cpp (r14c): exact interface-chain solver for relative towers (equivalent to Lemma I1 of r13c, but no K-head graphs).
//
// A closed L-history head above a fixed column is a chain of interfaces J0 -> J1 -> J2 ...; J_{k+1} is obtained from J_k by a closed
// L-column v (Lemma I1).  The tower above J dies at level r (no closed L-walk with r columns above the fixed column) iff the longest
// chain from J has r-1 columns; define D(I) = 0 if no closed L-column above I, else 1 + max_J D(J) over successors (D = INF if a cycle is
// reachable: then an infinite chain, i.e. an ICH with this tail, exists).  So tower death level K = D(J) + 1.
// DFS with a memo table on interfaces (canonicalised under time rotation by multiples of the clock period P).
//
// Modes: ifb b g L -iface "c|xb|A"      one tower given by an interface spec
//        ifb b g L -runfile F           towers from a file with "iface=c|xb|A" tokens
//        ifb b g L -word d0             whole word: my own BFS of IF(d0), births, all towers (shared memo)
// Build: clang++ -std=c++17 -O3 -march=native -o bin/ifb src/ifb.cpp
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <cassert>
#include <vector>
#include <string>
#include <algorithm>
#include <chrono>
#include <map>
#include <unordered_map>
#include <unordered_set>
using namespace std;
typedef unsigned long long u64; typedef uint32_t u32; typedef uint8_t u8;
static double now() { return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }
static const int MAXL = 128, MAXV = 39, MAXW = 16;
static int b = 10, NV = 19, L, P, W, RN;
static u8 G[MAXL];
static const int INF = 1 << 30;
struct TE { u8 n, y[2], hm[2]; };
static TE TT[2][2][4][MAXV][MAXV]; // g, c, Amask, xb, v
static void initTT() {
  for (int g = 0; g < 2; g++) for (int c = 0; c < 2; c++) for (int a = 1; a < 4; a++) for (int xb = 0; xb < NV; xb++) for (int v = 0; v < NV; v++) {
    TE e; memset(&e, 0, sizeof e);
    for (int h = 0; h < 2; h++) {
      int H = (v + h) / b; if (!((a >> H) & 1)) continue;
      int part = g ? (xb + H) % b : (v + h) % b;
      int y = (v + c) % b + part;
      int k; for (k = 0; k < e.n; k++) if (e.y[k] == y) break;
      if (k == e.n) { e.y[k] = (u8)y; e.hm[k] = 0; e.n++; }
      e.hm[k] |= (u8)(1 << h);
    }
    TT[g][c][a][xb][v] = e;
  }
}
// symbol of a phase: bit 0 = c, bits 1-2 = Amask-1 (0..2), bits 3-6 = xb mod b (0 at clock-0 phases); only xb mod b matters since part=(xb+H)%b (exact merge)
static inline void canon(u8* s) {
  if (RN <= 1) return;
  static u8 best[MAXL]; memcpy(best, s, L);
  for (int r = 1; r < RN; r++) {
    int sh = r * P; bool smaller = false;
    for (int t = 0; t < L; t++) { int i = t + sh; if (i >= L) i -= L; u8 a = s[i], z = best[t]; if (a < z) { smaller = true; break; } if (a > z) break; }
    if (smaller) { for (int t = 0; t < L; t++) { int i = t + sh; if (i >= L) i -= L; best[t] = s[i]; } }
  }
  memcpy(s, best, L);
}
static inline void packKey(const u8* s, u64* key) {
  memset(key, 0, W * 8);
  int bit = 0;
  for (int t = 0; t < L; t++) {
    int nb = G[t] ? 7 : 3; u64 v = s[t];
    key[bit >> 6] |= v << (bit & 63);
    int used = 64 - (bit & 63);
    if (used < nb) key[(bit >> 6) + 1] |= v >> used;
    bit += nb;
  }
}
static inline void unpackKey(const u64* key, u8* s) {
  int bit = 0;
  for (int t = 0; t < L; t++) {
    int nb = G[t] ? 7 : 3; u64 v = key[bit >> 6] >> (bit & 63);
    int used = 64 - (bit & 63);
    if (used < nb) v |= key[(bit >> 6) + 1] << used;
    s[t] = (u8)(v & ((1ULL << nb) - 1));
    bit += nb;
  }
}
static int keyBits() { int bits = 0; for (int t = 0; t < L; t++) bits += G[t] ? 7 : 3; return bits; }
// ---------- memo table ----------
static size_t CAP = 0, MASK = 0, COUNT = 0, MAXSLOTS = (size_t)1 << 34;
static u64* KT = nullptr; static int32_t* VT = nullptr;
static const int32_t VEMPTY = -2, VONSTACK = -1;
static inline u64 hashKey(const u64* k) {
  u64 h = 0x9E3779B97F4A7C15ULL;
  for (int i = 0; i < W; i++) { h ^= k[i]; h *= 0xff51afd7ed558ccdULL; h ^= h >> 29; h *= 0xc4ceb9fe1a85ec53ULL; h ^= h >> 32; }
  return h;
}
static void tableAlloc(size_t slots) { CAP = slots; MASK = CAP - 1; KT = (u64*)malloc(CAP * W * 8); VT = (int32_t*)malloc(CAP * 4); for (size_t i = 0; i < CAP; i++) VT[i] = VEMPTY; if (!KT || !VT) { fprintf(stderr, "alloc failed\n"); exit(3); } }
static void tableGrow() {
  size_t oldCap = CAP; u64* oldK = KT; int32_t* oldV = VT;
  if (CAP * 2 > MAXSLOTS) { fprintf(stderr, "FATAL table cap %zu exceeded\n", MAXSLOTS); printf("RESULT CAP table\n"); fflush(stdout); exit(4); }
  tableAlloc(CAP * 2);
  for (size_t i = 0; i < oldCap; i++) if (oldV[i] != VEMPTY) {
    const u64* k = oldK + i * W; size_t p = hashKey(k) & MASK;
    while (VT[p] != VEMPTY) p = (p + 1) & MASK;
    memcpy(KT + p * W, k, W * 8); VT[p] = oldV[i];
  }
  free(oldK); free(oldV);
}
static inline size_t findOrInsert(const u64* k, bool& isNew) {
  if ((COUNT + 1) * 10 > CAP * 7) tableGrow();
  size_t p = hashKey(k) & MASK;
  while (true) {
    int32_t v = VT[p];
    if (v == VEMPTY) { memcpy(KT + p * W, k, W * 8); VT[p] = VONSTACK; COUNT++; isNew = true; return p; }
    if (memcmp(KT + p * W, k, W * 8) == 0) { isNew = false; return p; }
    p = (p + 1) & MASK;
  }
}
static inline size_t findSlot(const u64* k) {
  size_t p = hashKey(k) & MASK;
  while (true) { if (VT[p] == VEMPTY) return (size_t)-1; if (memcmp(KT + p * W, k, W * 8) == 0) return p; p = (p + 1) & MASK; }
}
// ---------- expansion ----------
static vector<u64> arena; static u32 R[MAXL + 1][MAXV]; static u8 col[MAXL + 2], hmAt[MAXL + 1]; static const TE* teAt[MAXL]; static const u8* curS; static long long nEdges = 0, nExpand = 0;
static u8 Uset[MAXL]; static bool NORMU = false;
static void emitSucc() {
  u8 sn[MAXL];
  for (int t = 0; t < L; t++) {
    int c = curS[t] & 1; int v = col[t]; int c2 = (v + c) >= b;
    int a2 = hmAt[t];
    int xb2 = G[t] ? (v % b) : 0;
    sn[t] = (u8)(c2 | ((a2 - 1) << 1) | (xb2 << 3));
    for (int h = 0; h < 2; h++) if ((a2 >> h) & 1) Uset[t] |= (u8)(1 << ((v + h) / b));
  }
  size_t pos = arena.size(); arena.resize(pos + W);
  packKey(sn, arena.data() + pos);
  nEdges++;
}
static void dfsCol(int t, int v0) {
  if (t == L) { emitSucc(); return; }
  int v = col[t]; const TE& e = teAt[t][v];
  for (int k = 0; k < e.n; k++) {
    int y = e.y[k]; if (!((R[t + 1][y] >> v0) & 1)) continue;
    col[t + 1] = (u8)y; hmAt[t] = e.hm[k]; dfsCol(t + 1, v0);
  }
}
// expand interface s: append the raw (non-normalised, non-canonical) successor keys to the arena; compute normal form (c, xb, used carries U);
// returns false if there is no closed column above s (normal form undefined, D = 0).
static inline bool expandNorm(const u8* s, u8* norm) {
  curS = s; nExpand++;
  for (int t = 0; t < L; t++) { int c = s[t] & 1, a = ((s[t] >> 1) & 3) + 1, xb = s[t] >> 3; teAt[t] = (const TE*)TT[G[t]][c][a][xb]; }
  for (int v = 0; v < NV; v++) R[L][v] = 1u << v;
  for (int t = L - 1; t >= 0; t--) { const TE* tb = teAt[t]; u32* Rn = R[t + 1]; u32* Rc = R[t]; for (int v = 0; v < NV; v++) { const TE& e = tb[v]; u32 m = 0; for (int k = 0; k < e.n; k++) m |= Rn[e.y[k]]; Rc[v] = m; } }
  memset(Uset, 0, L); size_t before = arena.size();
  for (int v0 = 0; v0 < NV; v0++) if ((R[0][v0] >> v0) & 1) { col[0] = (u8)v0; dfsCol(0, v0); }
  if (arena.size() == before) return false;
  if (NORMU) for (int t = 0; t < L; t++) norm[t] = (u8)((s[t] & 1) | ((Uset[t] - 1) << 1) | ((s[t] >> 3) << 3));
  else memcpy(norm, s, L);
  return true;
}
// ---------- DFS solver ----------
struct Frame { size_t keyPos, succBegin, succEnd, next; int best; };
static vector<Frame> st; static vector<u64> stackKeys; static int maxDepth = 0; static long long nCycleEdges = 0; static bool DEDUP = true;
static double T0, lastPrint = 0; static string CYCFILE;
static void pushFrame(const u64* key, size_t b0) {
  size_t kp = stackKeys.size(); stackKeys.resize(kp + W); memcpy(stackKeys.data() + kp, key, W * 8);
  size_t cnt = (arena.size() - b0) / W;
  if (DEDUP && cnt > 1) {
    vector<size_t> idx(cnt); for (size_t i = 0; i < cnt; i++) idx[i] = i;
    const u64* base = arena.data() + b0;
    sort(idx.begin(), idx.end(), [&](size_t a, size_t c2) { return memcmp(base + a * W, base + c2 * W, W * 8) < 0; });
    vector<u64> tmp; tmp.reserve(cnt * W); const u64* prev = nullptr;
    for (size_t i = 0; i < cnt; i++) { const u64* k = base + idx[i] * W; if (prev && memcmp(prev, k, W * 8) == 0) continue; tmp.insert(tmp.end(), k, k + W); prev = k; }
    memcpy(arena.data() + b0, tmp.data(), tmp.size() * 8);
    arena.resize(b0 + tmp.size());
  }
  Frame f; f.keyPos = kp; f.succBegin = b0; f.succEnd = arena.size(); f.next = b0; f.best = 0;
  st.push_back(f);
  maxDepth = max(maxDepth, (int)st.size());
}
static void printCycleInfo(const u64* key) {
  int pos = -1; for (int i = (int)st.size() - 1; i >= 0; i--) if (memcmp(stackKeys.data() + st[i].keyPos, key, W * 8) == 0) { pos = i; break; }
  printf("CYCLE len=%d at depth %d (stack depth %zu)\n", (int)st.size() - pos, pos, st.size());
  if (!CYCFILE.empty()) {
    FILE* f = fopen(CYCFILE.c_str(), "a");
    fprintf(f, "CYCLE len=%d depth=%d\n", (int)st.size() - pos, pos);
    for (int i = pos; i < (int)st.size(); i++) { u8 s[MAXL]; unpackKey(stackKeys.data() + st[i].keyPos, s); fprintf(f, "  %d:", i); for (int t = 0; t < L; t++) fprintf(f, " %d,%d,%d", s[t] & 1, ((s[t] >> 1) & 3) + 1, s[t] >> 3); fprintf(f, "\n"); }
    fclose(f);
  }
  fflush(stdout);
}
static int solveRaw(const u64* rawKey, double maxsec, bool& capped) {
  capped = false;
  u8 s[MAXL], norm[MAXL]; u64 nk[MAXW], rk[MAXW];
  size_t a0 = arena.size();
  unpackKey(rawKey, s);
  if (!NORMU) { canon(s); packKey(s, nk); size_t q = findSlot(nk); if (q != (size_t)-1) { if (VT[q] < 0) { fprintf(stderr, "unexpected: root on stack\n"); exit(5); } return VT[q]; } }
  if (!expandNorm(s, norm)) return 0;
  canon(norm); packKey(norm, nk);
  bool isNew; size_t sl = findOrInsert(nk, isNew);
  if (!isNew) { arena.resize(a0); if (VT[sl] < 0) { fprintf(stderr, "unexpected: root on stack\n"); exit(5); } return VT[sl]; }
  pushFrame(nk, a0);
  double tstart = now();
  while (!st.empty()) {
    Frame& f = st.back();
    if (f.next < f.succEnd) {
      memcpy(rk, arena.data() + f.next, W * 8); f.next += W;
      size_t b0 = arena.size();
      unpackKey(rk, s);
      if (!NORMU) {   // lookup before expansion (saves the expansions of already-known interfaces)
        canon(s); packKey(s, nk); size_t q = findSlot(nk);
        if (q != (size_t)-1) { int32_t v = VT[q];
          if (v == VONSTACK) { nCycleEdges++; if (nCycleEdges <= 20) printCycleInfo(nk); if (f.best < INF) f.best = INF; }
          else f.best = max(f.best, v >= INF ? INF : v + 1);
          continue; }
      }
      if (!expandNorm(s, norm)) { if (f.best < 1) f.best = 1; continue; }
      canon(norm); packKey(norm, nk);
      bool nw; size_t p = findOrInsert(nk, nw);
      if (nw) { pushFrame(nk, b0); continue; }
      arena.resize(b0);
      int32_t v = VT[p];
      if (v == VONSTACK) { nCycleEdges++; if (nCycleEdges <= 20) printCycleInfo(nk); if (f.best < INF) f.best = INF; }
      else f.best = max(f.best, v >= INF ? INF : v + 1);
    } else {
      int D = f.best;
      size_t p = findSlot(stackKeys.data() + f.keyPos);
      VT[p] = D >= INF ? INF : D;
      arena.resize(f.succBegin); stackKeys.resize(f.keyPos);
      st.pop_back();
      if (!st.empty()) { Frame& g = st.back(); g.best = max(g.best, D >= INF ? INF : D + 1); }
      if (st.empty()) return D;
    }
    if ((nExpand & 0xFFFFF) == 0) { double t = now(); if (t - lastPrint > 60) { lastPrint = t; fprintf(stderr, "progress t=%.0f states=%zu expand=%lld edges=%lld depth=%zu maxDepth=%d\n", t - T0, COUNT, nExpand, nEdges, st.size(), maxDepth); fflush(stderr);
        if (t - tstart > maxsec) { capped = true; st.clear(); arena.clear(); stackKeys.clear(); return -1; } } }
  }
  return -1;
}
// ---------- spec parsing ----------
static bool parseIface(const string& spec, u8* s, int& Ln) {
  size_t bar1 = spec.find('|'), bar2 = spec.find('|', bar1 + 1);
  if (bar1 == string::npos || bar2 == string::npos) return false;
  string cs = spec.substr(0, bar1), xs = spec.substr(bar1 + 1, bar2 - bar1 - 1), as = spec.substr(bar2 + 1);
  Ln = cs.size(); size_t q = 0;
  for (int t = 0; t < Ln; t++) { size_t r = xs.find(',', q); if (r == string::npos) r = xs.size(); int xb = atoi(xs.substr(q, r - q).c_str()); q = r + 1; int a = as[t] - '0'; int c = cs[t] - '0';
    if (a < 1 || a > 3) return false; s[t] = (u8)(c | ((a - 1) << 1) | ((xb % b) << 3)); }
  return true;
}
// ---------- own BFS of IF(d0) and births (word mode) ----------
struct IFX { vector<int8_t> c, xb, A; bool root = false; };
static int rootStep(const IFX& I, int t, int v, int* ys, int* hm) {
  int Lc = I.c.size(), tt = t % Lc, n = 0;
  int g = G[t % P];
  for (int h = 0; h < 2; h++) {
    int H = (v + h) / b; if (!((I.A[tt] >> H) & 1)) continue;
    int part = g ? (I.root ? 1 : (I.xb[tt] + H) % b) : (v + h) % b;
    int y = (v + I.c[tt]) % b + part;
    if (I.root && y < 1) continue;
    int k; for (k = 0; k < n; k++) if (ys[k] == y) break;
    if (k == n) { ys[n] = y; hm[n] = 0; n++; }
    hm[k] |= 1 << h;
  }
  return n;
}
static void enumClosedColumns(const IFX& I, int Lc, vector<vector<int>>& out) {
  // explicit layered closed-walk enumeration (independent of expandInto): forward sets from each start digit restricted by a backward DP
  vector<vector<u32>> Reach(Lc + 1, vector<u32>(NV, 0));
  for (int v = 0; v < NV; v++) Reach[Lc][v] = 1u << v;
  int ys[2], hm[2];
  for (int t = Lc - 1; t >= 0; t--) for (int v = 0; v < NV; v++) {
    if (I.root && v < 1) continue;
    int n = rootStep(I, t, v, ys, hm); u32 m = 0;
    for (int k = 0; k < n; k++) m |= Reach[t + 1][ys[k]];
    Reach[t][v] = m;
  }
  vector<int> cl(Lc + 1);
  for (int v0 = I.root ? 1 : 0; v0 < NV; v0++) {
    if (!((Reach[0][v0] >> v0) & 1)) continue;
    // iterative DFS
    cl[0] = v0; vector<int> idx(Lc + 1, 0); int t = 0;
    while (t >= 0) {
      if (t == Lc) { if (cl[Lc] == cl[0]) out.push_back(cl); t--; continue; }
      int n = rootStep(I, t, cl[t], ys, hm);
      int k = idx[t];
      if (k >= n) { idx[t] = 0; t--; if (t >= 0) idx[t]++; continue; }
      int y = ys[k];
      if ((Reach[t + 1][y] >> v0) & 1) { cl[t + 1] = y; t++; if (t <= Lc) idx[t] = 0; if (t == Lc) { out.push_back(cl); t--; idx[t]++; } }
      else idx[t]++;
    }
  }
}
static IFX succIFX(const IFX& I, const vector<int>& v, int Lc) {
  IFX J; J.c.resize(Lc); J.xb.resize(Lc); J.A.resize(Lc); J.root = false;
  int T0_ = I.c.size(); int ys[2], hm[2];
  for (int t = 0; t < Lc; t++) {
    int n = rootStep(I, t, v[t], ys, hm); int mask = 0;
    for (int k = 0; k < n; k++) if (ys[k] == v[t + 1]) mask = hm[k];
    J.c[t] = (v[t] + I.c[t % T0_]) >= b; J.xb[t] = G[t % P] ? v[t] : 0; J.A[t] = (int8_t)mask;
  }
  return J;
}
static string keyIFX(const IFX& I) { string s; for (size_t i = 0; i < I.c.size(); i++) { s.push_back(I.c[i]); s.push_back((char)(I.xb[i] + 2)); s.push_back(I.A[i]); } s.push_back(I.root); return s; }
static void ifsBFS(int d0, vector<IFX>& ifs, int& a0) {
  IFX root; root.c.assign(d0, 0); root.xb.assign(d0, -1); root.A.resize(d0); root.root = true;
  for (int t = 0; t < d0; t++) root.A[t] = 1 << G[t % P];
  unordered_map<string, int> seen; seen[keyIFX(root)] = 0; ifs.clear(); ifs.push_back(root);
  size_t head = 0; int lvl = 0;
  while (head < ifs.size()) {
    size_t end = ifs.size();
    for (; head < end; head++) {
      IFX cur = ifs[head];
      vector<vector<int>> cols; enumClosedColumns(cur, d0, cols);
      for (auto& v : cols) { IFX J = succIFX(cur, v, d0); string k = keyIFX(J); if (!seen.count(k)) { seen[k] = ifs.size(); ifs.push_back(J); } }
    }
    if (ifs.size() > end) lvl++;
  }
  a0 = lvl;
}

// ---------- level-wise BFS statistics (mode -bfs Kmax): distinct interfaces per level above a tower ----------
static void bfsStats(const u64* rootRaw, int Kmax, size_t capFrontier, double maxsec) {
  vector<u64> frontier(W), nxt; memcpy(frontier.data(), rootRaw, W * 8);
  { u8 s[MAXL]; unpackKey(frontier.data(), s); canon(s); packKey(s, frontier.data()); }
  double t0 = now();
  for (int lev = 1; lev <= Kmax; lev++) {
    size_t nf = frontier.size() / W; if (nf == 0) { printf("BFS level %d: frontier empty (tower dead)\n", lev); break; }
    nxt.clear(); long long edges = 0, deadSucc = 0, maxCols = 0, newStates = 0, liveHere = 0; map<int,long long> colhist;
    for (size_t i = 0; i < nf; i++) {
      u8 s[MAXL], norm[MAXL]; unpackKey(frontier.data() + i * W, s);
      arena.clear(); nExpand++;
      bool has = expandNorm(s, norm);
      if (!has) continue;
      liveHere++;
      long long ncol = arena.size() / W; edges += ncol; maxCols = max(maxCols, ncol);
      int lg = 0; while ((1LL << (lg + 1)) <= ncol) lg++; colhist[lg]++;
      for (long long j = 0; j < ncol; j++) {
        u8 sn[MAXL]; unpackKey(arena.data() + j * W, sn); canon(sn); u64 k2[MAXW]; packKey(sn, k2);
        if (findSlot(k2) != (size_t)-1) continue;
        // liveness test of the successor (expansion only to see if a closed column exists)
        u8 norm2[MAXL]; size_t sv = arena.size(); bool live = expandNorm(sn, norm2); arena.resize(sv);
        if (!live) { deadSucc++; continue; }
        bool isnew; size_t p = findOrInsert(k2, isnew); if (isnew) { VT[p] = lev; nxt.insert(nxt.end(), k2, k2 + W); newStates++; }
      }
      if ((nExpand & 0xFFFF) == 0 && now() - t0 > maxsec) { printf("BFS CAPPED time at level %d (frontier %zu, processed %zu)\n", lev, nf, i); return; }
    }
    printf("BFS level %d: frontier(live)=%zu edges=%lld deadSucc=%lld newLive=%lld maxCols=%lld seen=%zu t=%.1f hist(log2 cols):", lev, nf, edges, deadSucc, newStates, maxCols, COUNT, now() - t0);
    for (auto& kv : colhist) printf(" %d:%lld", kv.first, kv.second); printf("\n"); fflush(stdout);
    if (nxt.size() / W > capFrontier) { printf("BFS CAPPED frontier %zu at level %d\n", nxt.size() / W, lev); return; }
    frontier.swap(nxt);
  }
}
int main(int argc, char** argv) {
  if (argc < 5) { fprintf(stderr, "usage: ifb b g L mode...\n"); return 2; }
  b = atoi(argv[1]); NV = 2 * b - 1; string gw = argv[2]; L = atoi(argv[3]); P = gw.size();
  if (L > MAXL) { fprintf(stderr, "L too large\n"); return 2; }
  for (int t = 0; t < L; t++) G[t] = gw[t % P] - '0';
  int EVERY = 0; string spec, runfile; int d0 = 0; int bfsK = 0; size_t bfsCap = 200000000; size_t slots0 = (size_t)1 << 24; double maxsec = 1e18; bool rot = true;
  for (int i = 4; i < argc; i++) { string a = argv[i];
    if (a == "-iface") spec = argv[++i]; else if (a == "-runfile") runfile = argv[++i]; else if (a == "-word") d0 = atoi(argv[++i]);
    else if (a == "-slots") slots0 = strtoull(argv[++i], nullptr, 10); else if (a == "-maxslots") MAXSLOTS = strtoull(argv[++i], nullptr, 10);
    else if (a == "-sec") maxsec = atof(argv[++i]); else if (a == "-norot") rot = false; else if (a == "-U") NORMU = true; else if (a == "-bfs") bfsK = atoi(argv[++i]); else if (a == "-bfscap") bfsCap = strtoull(argv[++i], nullptr, 10); else if (a == "-nodedup") DEDUP = false; else if (a == "-every") EVERY = atoi(argv[++i]); else if (a == "-cycfile") CYCFILE = argv[++i];
    else { fprintf(stderr, "unknown %s\n", a.c_str()); return 2; } }
  RN = rot ? L / P : 1; if (L % P) { fprintf(stderr, "P must divide L\n"); return 2; }
  int bits = keyBits(); W = (bits + 63) / 64; initTT();
  fprintf(stderr, "ifb b=%d g=%s L=%d P=%d keybits=%d W=%d rotations=%d\n", b, gw.c_str(), L, P, bits, W, RN);
  T0 = now(); tableAlloc(slots0);
  u64 k[MAXW];
  if (d0) {
    vector<IFX> ifs; int a0; ifsBFS(d0, ifs, a0);
    printf("IF(d0) g=%s d0=%d interfaces=%zu a0=%d t=%.2f\n", gw.c_str(), d0, ifs.size(), a0, now() - T0); fflush(stdout);
    // births (distinct, rotation-canonical keys); also count distinct without canonicalisation is not needed
    vector<u64> birthKeys; { unordered_set<string> seenB; long long closed = 0, nonper = 0;
      for (auto& I : ifs) {
        IFX Il; Il.root = I.root; Il.c.resize(L); Il.xb.resize(L); Il.A.resize(L);
        for (int t = 0; t < L; t++) { Il.c[t] = I.c[t % d0]; Il.xb[t] = I.xb[t % d0]; Il.A[t] = I.A[t % d0]; }
        vector<vector<int>> cols; enumClosedColumns(Il, L, cols); closed += cols.size();
        for (auto& v : cols) {
          bool per = true; for (int t = 0; t + d0 < L; t++) if (v[t] != v[t + d0]) { per = false; break; }
          if (per) continue; nonper++;
          IFX J = succIFX(Il, v, L);
          u8 s[MAXL]; for (int t = 0; t < L; t++) s[t] = (u8)((J.c[t] & 1) | ((J.A[t] - 1) << 1) | ((G[t] ? J.xb[t] : 0) << 3));
          canon(s);
          string ks((char*)s, L);
          if (seenB.insert(ks).second) { for (int t = 0; t < L; t++) s[t] = (u8)((s[t] & 7) | (((s[t] >> 3) % b) << 3)); u64 kk[MAXW]; packKey(s, kk); birthKeys.insert(birthKeys.end(), kk, kk + W); }
        }
      }
      printf("BIRTHS closed=%lld nonperiodic=%lld distinct_rotclasses=%zu t=%.2f\n", closed, nonper, birthKeys.size() / W, now() - T0); fflush(stdout);
    }
    long long nb = birthKeys.size() / W, dies = 0, inf = 0; int maxK = 0; map<int,long long> hist;
    for (long long i = 0; i < nb; i++) {
      if (EVERY > 1 && (i % EVERY) != 0) continue;
      bool capped; int D = solveRaw(birthKeys.data() + i * W, maxsec, capped);
      if (capped) { printf("CAPPED at tower %lld of %lld (time)\n", i, nb); fflush(stdout); return 0; }
      if (D >= INF) { inf++; u8 s[MAXL]; unpackKey(birthKeys.data() + i * W, s); printf("TINF tower=%lld iface=", i); for (int t = 0; t < L; t++) printf("%d", s[t] & 1); printf("|"); for (int t = 0; t < L; t++) printf("%d,", s[t] >> 3); printf("|"); for (int t = 0; t < L; t++) printf("%d", ((s[t] >> 1) & 3) + 1); printf("\n"); fflush(stdout); }
      else { dies++; hist[D + 1]++; maxK = max(maxK, D + 1); }
    }
    printf("IFB_WORD g=%s d0=%d L=%d interfaces=%zu a0=%d births=%lld die=%lld inf=%lld maxK=%d states=%zu expand=%lld edges=%lld maxDepth=%d t=%.1f\n", gw.c_str(), d0, L, ifs.size(), a0, nb, dies, inf, maxK, COUNT, nExpand, nEdges, maxDepth, now() - T0);
    printf("HIST"); for (auto& kv : hist) printf(" %d:%lld", kv.first, kv.second); printf("\n");
    return 0;
  }
  vector<string> specs; if (!spec.empty()) specs.push_back(spec);
  if (!runfile.empty()) { FILE* f = fopen(runfile.c_str(), "r"); if (!f) { perror("runfile"); return 2; } char* line = nullptr; size_t cap = 0; while (getline(&line, &cap, f) > 0) { string sl(line); size_t p0 = sl.find("iface="); if (p0 == string::npos) continue; p0 += 6; size_t p1 = sl.find_first_of(" \n", p0); specs.push_back(sl.substr(p0, p1 - p0)); } fclose(f); }
  long long idx = 0;
  if (bfsK) { for (auto& sp : specs) { idx++; u8 s[MAXL]; int Ln; if (!parseIface(sp, s, Ln) || Ln != L) continue; packKey(s, k); printf("== BFS tower idx=%lld\n", idx); COUNT = 0; for (size_t i = 0; i < CAP; i++) VT[i] = VEMPTY; bfsStats(k, bfsK, bfsCap, maxsec); } return 0; }
  for (auto& sp : specs) {
    idx++;
    u8 s[MAXL]; int Ln; if (!parseIface(sp, s, Ln) || Ln != L) { fprintf(stderr, "bad spec %s\n", sp.c_str()); continue; }
    canon(s); packKey(s, k);
    bool capped; double t1 = now(); size_t c0 = COUNT;
    int D = solveRaw(k, maxsec, capped);
    if (capped) { printf("TOWER idx=%lld CAPPED(time) states=%zu expand=%lld edges=%lld maxDepth=%d secs=%.1f iface=%s\n", idx, COUNT, nExpand, nEdges, maxDepth, now() - t1, sp.c_str()); }
    else if (D >= INF) printf("TOWER idx=%lld INF states=%zu expand=%lld edges=%lld maxDepth=%d cycleEdges=%lld secs=%.1f iface=%s\n", idx, COUNT, nExpand, nEdges, maxDepth, nCycleEdges, now() - t1, sp.c_str());
    else printf("TOWER idx=%lld DIES K=%d states=%zu newstates=%zu expand=%lld edges=%lld maxDepth=%d secs=%.1f iface=%s\n", idx, D + 1, COUNT, COUNT - c0, nExpand, nEdges, maxDepth, now() - t1, sp.c_str());
    fflush(stdout);
  }
  return 0;
}
