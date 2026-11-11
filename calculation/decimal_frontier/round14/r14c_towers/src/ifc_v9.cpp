// ifd = ifc.cpp + memo-free tree DFS (mode -tree): no interface memo at all (the interface graph above births is a forest in practice, 6.8K merges in 1.47e9 edges at L=24; a merged node is simply re-explored, exact and rigorous), only an on-stack set for cycle detection.
// ifc.cpp (r14c): chunked version of ifb.cpp: the L phases are split in two halves; closed columns are pairs of half-walks; a child interface is kept only if its halves' reachability matrices close (live filter).
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
#include <set>
#include <cmath>
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
static u32 PT[2][2][4][MAXV][MAXV]; // g, c, Amask, xb, y -> mask of x with y in succ(x)
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
    for (int k = 0; k < e.n; k++) PT[g][c][a][xb][e.y[k]] |= 1u << v;
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
  canon(sn);
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
// ---------- chunked expansion (L even): halves [0,ELL) and [ELL,L) ----------
static int ELL = 0, CCLS[2], CW = 0; static bool NOCHUNK = false, TREE = false;
struct CT { u64* K = nullptr; u32* V = nullptr; size_t cap = 0, mask = 0, count = 0; };
static bool scratchUsed = false; static CT ctab[2]; static vector<u32> NM; static vector<u8> NANY; static size_t MAXCH = 20000000; static long long chHit = 0, chMiss = 0, pairsTried = 0, pairsLive = 0, nWalks = 0;
static inline u64 hashC(const u64* k) { u64 h = 0xA0761D6478BD642FULL; for (int i = 0; i < CW; i++) { h ^= k[i]; h *= 0xE7037ED1A0B428DBULL; h ^= h >> 31; h *= 0x8EBC6AF09C88C6E3ULL; h ^= h >> 29; } return h; }
static void ctabAlloc(CT& c, size_t slots) { c.cap = slots; c.mask = slots - 1; c.K = (u64*)malloc(slots * CW * 8); c.V = (u32*)calloc(slots, 4); c.count = 0; if (!c.K || !c.V) { fprintf(stderr, "ctab alloc failed\n"); exit(3); } }
static void ctabGrow(CT& c) {
  CT o = c; ctabAlloc(c, o.cap * 2); c.count = o.count;
  for (size_t i = 0; i < o.cap; i++) if (o.V[i]) { const u64* k = o.K + i * CW; size_t p = hashC(k) & c.mask; while (c.V[p]) p = (p + 1) & c.mask; memcpy(c.K + p * CW, k, CW * 8); c.V[p] = o.V[i]; }
  free(o.K); free(o.V);
}
static inline void packChunk(const u8* cs, int base, u64* key) {
  memset(key, 0, CW * 8); int bit = 0;
  for (int t = 0; t < ELL; t++) { int nb = G[base + t] ? 7 : 3; u64 v = cs[t]; key[bit >> 6] |= v << (bit & 63); int used = 64 - (bit & 63); if (used < nb) key[(bit >> 6) + 1] |= v >> used; bit += nb; }
}
static inline u32 computeN(const u8* cs, int base) {
  static u32 Rn[MAXL / 2 + 2][MAXV]; const TE* te[MAXL / 2];
  for (int t = 0; t < ELL; t++) { int sy = cs[t]; te[t] = (const TE*)TT[G[base + t]][sy & 1][((sy >> 1) & 3) + 1][sy >> 3]; }
  for (int v = 0; v < NV; v++) Rn[ELL][v] = 1u << v;
  for (int t = ELL - 1; t >= 0; t--) { const TE* tb = te[t]; u32* Rnx = Rn[t + 1]; u32* Rc = Rn[t]; for (int v = 0; v < NV; v++) { const TE& e = tb[v]; u32 m = 0; for (int k = 0; k < e.n; k++) m |= Rnx[e.y[k]]; Rc[v] = m; } }
  size_t idx = NM.size() / (2 * NV); NM.resize((idx + 1) * 2 * NV, 0); u32* N = NM.data() + idx * 2 * NV; u32* Nt = N + NV; u32 any = 0;
  for (int p = 0; p < NV; p++) { N[p] = Rn[0][p]; any |= N[p]; }
  for (int p = 0; p < NV; p++) for (int q = 0; q < NV; q++) if ((N[p] >> q) & 1) Nt[q] |= 1u << p;
  NANY.push_back(any != 0);
  return (u32)idx;
}
static inline u32 chunkNid(const u8* cs, int i) {
  int base = i * ELL; int cls = CCLS[i]; CT& c = ctab[cls]; u64 key[MAXW];
  packChunk(cs, base, key);
  if ((c.count + 1) * 10 > c.cap * 7) ctabGrow(c);
  size_t p = hashC(key) & c.mask;
  while (c.V[p]) { if (memcmp(c.K + p * CW, key, CW * 8) == 0) { chHit++; return c.V[p] - 1; } p = (p + 1) & c.mask; }
  chMiss++;
  if (NM.size() / (2 * NV) >= MAXCH) { /* table full: compute into a scratch entry beyond MAXCH (truncated after this expansion) */ scratchUsed = true; u32 idx = computeN(cs, base); return idx; }
  u32 idx = computeN(cs, base);
  memcpy(c.K + p * CW, key, CW * 8); c.V[p] = idx + 1; c.count++;
  return idx;
}
static bool scratchUsedDummy;
struct Walk { u32 nid; u8 p, q; u8 cs[MAXL / 2]; };
static vector<Walk> walks[2]; static u32 Rr[2][MAXL / 2 + 2][MAXV]; static const TE* teC[2][MAXL / 2]; static u8 curW[MAXL / 2 + 2], hmW[MAXL / 2 + 1];
static const u8* curSym; static int curChunk;
static void dfsW(int tau, int p, u32 allowedEnd) {
  int i = curChunk;
  if (tau == ELL) {
    Walk w; w.p = (u8)p; w.q = curW[ELL]; int base = i * ELL;
    for (int t = 0; t < ELL; t++) { int v = curW[t]; int sym = curSym[base + t]; int c2 = (v + (sym & 1)) >= b; int xb2 = G[base + t] ? v % b : 0; w.cs[t] = (u8)(c2 | ((hmW[t] - 1) << 1) | (xb2 << 3)); }
    w.nid = chunkNid(w.cs, i);
    walks[i].push_back(w); nWalks++;
    return;
  }
  int v = curW[tau]; const TE& e = teC[i][tau][v];
  for (int k = 0; k < e.n; k++) { int y = e.y[k]; if (!(Rr[i][tau + 1][y] & allowedEnd)) continue; curW[tau + 1] = (u8)y; hmW[tau] = e.hm[k]; dfsW(tau + 1, p, allowedEnd); }
}
// returns whether a closed column exists above s; appends the canonical keys of the live children to arena
static bool DBG = false; static bool expandC2(const u8* s);
static bool expandC(const u8* s);
static long long dbgChecked = 0;
static void dbgCompare(const u8* s) {
  // plain expansion of s, liveness of every child; compare to the chunk filter's child list (arena suffix)
}
static bool expandC(const u8* s) {
  if (!DBG) return expandC2(s);
  size_t a0 = arena.size();
  bool any = expandC2(s);
  // compare
  vector<u64> chunkKids(arena.begin() + a0, arena.end()); arena.resize(a0);
  u8 norm[MAXL]; size_t a1 = arena.size();
  bool anyP = expandNorm(s, norm);
  size_t cnt = (arena.size() - a1) / W; vector<u64> plainLive; 
  vector<u64> plainKids(arena.begin() + a1, arena.end()); arena.resize(a1);
  set<vector<u64>> liveSet, chunkSet;
  for (size_t j = 0; j < cnt; j++) { u8 sn[MAXL]; unpackKey(plainKids.data() + j * W, sn); size_t sv = arena.size(); u8 n2[MAXL]; bool live = expandNorm(sn, n2); arena.resize(sv); vector<u64> k(plainKids.begin() + j * W, plainKids.begin() + (j + 1) * W); if (live) liveSet.insert(k); }
  for (size_t j = 0; j < chunkKids.size() / W; j++) { vector<u64> k(chunkKids.begin() + j * W, chunkKids.begin() + (j + 1) * W); chunkSet.insert(k); }
  dbgChecked++;
  if (anyP != any || liveSet != chunkSet) { printf("DBG MISMATCH anyP=%d any=%d plainLive=%zu chunkLive=%zu\n", anyP, any, liveSet.size(), chunkSet.size());
    for (int t = 0; t < L; t++) printf("%d,", s[t]); printf("\n");
    int shown = 0; for (auto& k : liveSet) if (!chunkSet.count(k) && shown < 3) { shown++; u8 sn[MAXL]; unpackKey(k.data(), sn); printf(" plain-only:"); for (int t = 0; t < L; t++) printf("%d,", sn[t]); printf("\n"); }
    for (int i = 0; i < 2; i++) for (auto& w : walks[i]) { printf(" walk chunk%d p=%d q=%d nid=%u any=%d cs:", i, w.p, w.q, w.nid, (int)NANY[w.nid]); for (int t = 0; t < ELL; t++) printf("%d,", w.cs[t]); printf(" N:"); const u32* N = NM.data() + (size_t)w.nid * 2 * NV; for (int x = 0; x < NV; x++) printf("%x,", N[x]); printf("\n"); }
    exit(9); }
  arena.insert(arena.end(), chunkKids.begin(), chunkKids.end());
  return any;
}
static bool expandC2(const u8* s) {
  nExpand++; curSym = s;
  for (int i = 0; i < 2; i++) {
    int base = i * ELL;
    for (int t = 0; t < ELL; t++) { int sy = s[base + t]; teC[i][t] = (const TE*)TT[G[base + t]][sy & 1][((sy >> 1) & 3) + 1][sy >> 3]; }
    for (int v = 0; v < NV; v++) Rr[i][ELL][v] = 1u << v;
    for (int t = ELL - 1; t >= 0; t--) { const TE* tb = teC[i][t]; u32* Rnx = Rr[i][t + 1]; u32* Rc = Rr[i][t]; for (int v = 0; v < NV; v++) { const TE& e = tb[v]; u32 m = 0; for (int k = 0; k < e.n; k++) m |= Rnx[e.y[k]]; Rc[v] = m; } }
  }
  u32 B0[MAXV], B1[MAXV], Bt0[MAXV], Bt1[MAXV]; memset(Bt0, 0, sizeof Bt0); memset(Bt1, 0, sizeof Bt1);
  for (int p = 0; p < NV; p++) { B0[p] = Rr[0][0][p]; B1[p] = Rr[1][0][p]; }
  for (int p = 0; p < NV; p++) for (int q = 0; q < NV; q++) { if ((B0[p] >> q) & 1) Bt0[q] |= 1u << p; if ((B1[p] >> q) & 1) Bt1[q] |= 1u << p; }
  u32 A0[MAXV], A1[MAXV]; u32 anyA = 0;
  for (int p = 0; p < NV; p++) { A0[p] = B0[p] & Bt1[p]; A1[p] = B1[p] & Bt0[p]; anyA |= A0[p]; }
  if (!anyA) return false;
  walks[0].clear(); walks[1].clear();
  for (int i = 0; i < 2; i++) { curChunk = i; for (int p = 0; p < NV; p++) { u32 allowed = i == 0 ? A0[p] : A1[p]; if (!allowed) continue; curW[0] = (u8)p; dfsW(0, p, allowed); } }
  // group walks by (p,q)
  static vector<u32> byPQ[2][MAXV][MAXV]; for (int i = 0; i < 2; i++) for (int p = 0; p < NV; p++) for (int q = 0; q < NV; q++) byPQ[i][p][q].clear();
  for (int i = 0; i < 2; i++) for (u32 j = 0; j < walks[i].size(); j++) byPQ[i][walks[i][j].p][walks[i][j].q].push_back(j);
  bool anyClosed = false; u8 sn[MAXL];
  for (int p = 0; p < NV; p++) for (int q = 0; q < NV; q++) {
    auto& L0 = byPQ[0][p][q]; auto& L1 = byPQ[1][q][p];
    if (L0.empty() || L1.empty()) continue;
    anyClosed = true;
    for (u32 ui : L0) { const Walk& u = walks[0][ui]; if (!NANY[u.nid]) { pairsTried += L1.size(); continue; } const u32* Nu = NM.data() + (size_t)u.nid * 2 * NV;
      for (u32 wi : L1) { const Walk& w = walks[1][wi]; pairsTried++; if (!NANY[w.nid]) continue;
        const u32* Ntw = NM.data() + (size_t)w.nid * 2 * NV + NV; bool live = false;
        for (int x = 0; x < NV; x++) if (Nu[x] & Ntw[x]) { live = true; break; }
        if (!live) continue;
        pairsLive++;
        memcpy(sn, u.cs, ELL); memcpy(sn + ELL, w.cs, ELL); canon(sn);
        size_t pos = arena.size(); arena.resize(pos + W); packKey(sn, arena.data() + pos);
      }
    }
  }
  if (scratchUsed) { NM.resize(MAXCH * 2 * NV); NANY.resize(MAXCH); scratchUsed = false; }
  return anyClosed;
}

// ---------- expandC3: chunked expansion without chunk memo (direct N per walk, no transposes) ----------
struct Walk3 { u8 p, q; u8 cs[MAXL / 2]; u32 N[MAXV]; u32 any, rows; };
static vector<Walk3> walks3[2]; static long long nTest3 = 0;
static inline u32 computeN3(const u8* cs, int base, u32* N) {
  static u32 Rn[MAXL / 2 + 2][MAXV]; const TE* te[MAXL / 2];
  for (int t = 0; t < ELL; t++) { int sy = cs[t]; te[t] = (const TE*)TT[G[base + t]][sy & 1][((sy >> 1) & 3) + 1][sy >> 3]; }
  for (int v = 0; v < NV; v++) Rn[ELL][v] = 1u << v;
  for (int t = ELL - 1; t >= 0; t--) { const TE* tb = te[t]; u32* Rnx = Rn[t + 1]; u32* Rc = Rn[t]; for (int v = 0; v < NV; v++) { const TE& e = tb[v]; u32 m = 0; for (int k = 0; k < e.n; k++) m |= Rnx[e.y[k]]; Rc[v] = m; } }
  u32 any = 0; for (int p = 0; p < NV; p++) { N[p] = Rn[0][p]; any |= N[p]; }
  return any;
}
static void dfsW3(int tau, int p, u32 allowedEnd) {
  int i = curChunk;
  if (tau == ELL) {
    walks3[i].emplace_back(); Walk3& w = walks3[i].back(); w.p = (u8)p; w.q = curW[ELL]; int base = i * ELL;
    for (int t = 0; t < ELL; t++) { int v = curW[t]; int sym = curSym[base + t]; int c2 = (v + (sym & 1)) >= b; int xb2 = G[base + t] ? v % b : 0; w.cs[t] = (u8)(c2 | ((hmW[t] - 1) << 1) | (xb2 << 3)); }
    w.any = computeN3(w.cs, base, w.N); nWalks++;
    return;
  }
  int v = curW[tau]; const TE& e = teC[i][tau][v];
  for (int k = 0; k < e.n; k++) { int y = e.y[k]; if (!(Rr[i][tau + 1][y] & allowedEnd)) continue; curW[tau + 1] = (u8)y; hmW[tau] = e.hm[k]; dfsW3(tau + 1, p, allowedEnd); }
}
static bool expandC3(const u8* s) {
  nExpand++; curSym = s;
  for (int i = 0; i < 2; i++) {
    int base = i * ELL;
    for (int t = 0; t < ELL; t++) { int sy = s[base + t]; teC[i][t] = (const TE*)TT[G[base + t]][sy & 1][((sy >> 1) & 3) + 1][sy >> 3]; }
    for (int v = 0; v < NV; v++) Rr[i][ELL][v] = 1u << v;
    for (int t = ELL - 1; t >= 0; t--) { const TE* tb = teC[i][t]; u32* Rnx = Rr[i][t + 1]; u32* Rc = Rr[i][t]; for (int v = 0; v < NV; v++) { const TE& e = tb[v]; u32 m = 0; for (int k = 0; k < e.n; k++) m |= Rnx[e.y[k]]; Rc[v] = m; } }
  }
  u32 B0[MAXV], B1[MAXV], Bt0[MAXV], Bt1[MAXV]; memset(Bt0, 0, sizeof Bt0); memset(Bt1, 0, sizeof Bt1);
  for (int p = 0; p < NV; p++) { B0[p] = Rr[0][0][p]; B1[p] = Rr[1][0][p]; }
  for (int p = 0; p < NV; p++) for (int q = 0; q < NV; q++) { if ((B0[p] >> q) & 1) Bt0[q] |= 1u << p; if ((B1[p] >> q) & 1) Bt1[q] |= 1u << p; }
  u32 A0[MAXV], A1[MAXV]; u32 anyA = 0;
  for (int p = 0; p < NV; p++) { A0[p] = B0[p] & Bt1[p]; A1[p] = B1[p] & Bt0[p]; anyA |= A0[p]; }
  if (!anyA) return false;
  walks3[0].clear(); walks3[1].clear();
  for (int i = 0; i < 2; i++) { curChunk = i; for (int p = 0; p < NV; p++) { u32 allowed = i == 0 ? A0[p] : A1[p]; if (!allowed) continue; curW[0] = (u8)p; dfsW3(0, p, allowed); } }
  bool anyClosed = false; u8 sn[MAXL];
  static vector<u32> grp[2][MAXV][MAXV];
  for (int i = 0; i < 2; i++) for (int a = 0; a < NV; a++) for (int c = 0; c < NV; c++) grp[i][a][c].clear();
  for (int i = 0; i < 2; i++) for (u32 j = 0; j < walks3[i].size(); j++) grp[i][walks3[i][j].p][walks3[i][j].q].push_back(j);
  for (int p = 0; p < NV; p++) for (int q = 0; q < NV; q++) {
    auto& G0 = grp[0][p][q]; auto& G1 = grp[1][q][p]; if (G0.empty() || G1.empty()) continue;
    anyClosed = true;
    for (u32 ui : G0) { const Walk3& u = walks3[0][ui];
      for (u32 wi : G1) { const Walk3& w = walks3[1][wi]; pairsTried++;
        if (!(u.rows & w.any) || !(u.any & w.rows)) continue;  // necessary: a start digit x of a row of u must be an end digit of w, and vice versa
        bool live = false;
        u32 cand = u.rows & w.any;
        while (cand && !live) { int x = __builtin_ctz(cand); cand &= cand - 1; u32 m = u.N[x] & w.rows; while (m) { int q2 = __builtin_ctz(m); m &= m - 1; if ((w.N[q2] >> x) & 1) { live = true; break; } } }
        if (!live) continue;
        pairsLive++;
        memcpy(sn, u.cs, ELL); memcpy(sn + ELL, w.cs, ELL); canon(sn);
        size_t pos = arena.size(); arena.resize(pos + W); packKey(sn, arena.data() + pos);
      }
    }
  }
  return anyClosed;
}

// ---------- expandC4: chunk walks enumerated BACKWARD with incremental child reachability (shared along the DFS) ----------
static u32 FwC[2][MAXL / 2 + 2][MAXV]; // FwC[i][t][v] = set of start digits (phase 0 of chunk i) reaching digit v at chunk phase t
static u32 SuccMask[2][MAXL / 2][MAXV];
static u32 childR[MAXL / 2 + 2][MAXV]; static u32 nzC[MAXL / 2 + 2]; static u8 csW[MAXL / 2 + 1];
static void bdfs4(int tau, int y, int qEnd, u32 startsAllowed) {
  // choose digit v at phase tau (tau < ELL) with transition v -> y (y at phase tau+1)
  int i = curChunk; int base = i * ELL;
  int symParent = curSym[base + tau]; int cpar = symParent & 1; int g = G[base + tau];
  for (int v = 0; v < NV; v++) {
    if (!((SuccMask[i][tau][v] >> y) & 1)) continue;
    if (!(FwC[i][tau][v] & startsAllowed)) continue;
    const TE& e = teC[i][tau][v]; int hm = 0; for (int k = 0; k < e.n; k++) if (e.y[k] == y) hm = e.hm[k];
    int c2 = (v + cpar) >= b; int xb2 = g ? v % b : 0; u8 sy = (u8)(c2 | ((hm - 1) << 1) | (xb2 << 3)); csW[tau] = sy;
    // update child reachability from phase tau+1 to tau
    u32* Rc = childR[tau]; const u32* Rn = childR[tau + 1]; const u32* pt = PT[g][c2][hm][xb2];
    memset(Rc, 0, NV * 4); u32 nzn = nzC[tau + 1], nzc = 0;
    { u32 m = nzn; while (m) { int y2 = __builtin_ctz(m); m &= m - 1; u32 xs = pt[y2]; u32 r = Rn[y2]; while (xs) { int x = __builtin_ctz(xs); xs &= xs - 1; Rc[x] |= r; nzc |= 1u << x; } } }
    nzC[tau] = nzc;
    if (tau > 0) { bdfs4(tau - 1, v, qEnd, startsAllowed); }
    else {
      // walk complete: from v (start digit p) to qEnd
      if (!((startsAllowed >> v) & 1)) continue;
      walks3[i].emplace_back(); Walk3& w = walks3[i].back(); w.p = (u8)v; w.q = (u8)qEnd; memcpy(w.cs, csW, ELL); u32 any = 0, rows = 0; for (int x = 0; x < NV; x++) { w.N[x] = Rc[x]; any |= Rc[x]; if (Rc[x]) rows |= 1u << x; } w.any = any; w.rows = rows; nWalks++;
    }
  }
}
static bool expandC4(const u8* s) {
  nExpand++; curSym = s;
  for (int i = 0; i < 2; i++) {
    int base = i * ELL;
    for (int t = 0; t < ELL; t++) { int sy = s[base + t]; const TE* tb = (const TE*)TT[G[base + t]][sy & 1][((sy >> 1) & 3) + 1][sy >> 3]; teC[i][t] = tb; for (int v = 0; v < NV; v++) { u32 m = 0; const TE& e = tb[v]; for (int k = 0; k < e.n; k++) m |= 1u << e.y[k]; SuccMask[i][t][v] = m; } }
    for (int v = 0; v < NV; v++) FwC[i][0][v] = 1u << v;
    for (int t = 0; t < ELL; t++) { u32* Fc = FwC[i][t]; u32* Fn = FwC[i][t + 1]; for (int v = 0; v < NV; v++) Fn[v] = 0; for (int v = 0; v < NV; v++) { u32 f = Fc[v]; if (!f) continue; const TE& e = teC[i][t][v]; for (int k = 0; k < e.n; k++) Fn[e.y[k]] |= f; } }
  }
  // allowed pairs: chunk 0 from p to q needs chunk 1 from q to p
  u32 B0t[MAXV], B1t[MAXV]; // B0t[q] = set of p reaching q through chunk 0 (= FwC[0][ELL][q]); B1t[p] = set of q reaching p through chunk 1 (= FwC[1][ELL][p])
  for (int v = 0; v < NV; v++) { B0t[v] = FwC[0][ELL][v]; B1t[v] = FwC[1][ELL][v]; }
  // chunk 0 walk p->q allowed iff p in B0t[q] (automatic for enumerated walks) and q in B1t[p]; chunk 1 walk q->p allowed iff q in B1t[p] (automatic) and p in B0t[q]
  // starts allowed for chunk 0 ending at q: { p : q in B1t[p] } ; for chunk 1 ending at p: { q : p in B0t[q] }
  u32 S0[MAXV], S1[MAXV]; memset(S0, 0, sizeof S0); memset(S1, 0, sizeof S1); u32 anyPair = 0;
  for (int p = 0; p < NV; p++) for (int q = 0; q < NV; q++) { if (((B0t[q] >> p) & 1) && ((B1t[p] >> q) & 1)) { S0[q] |= 1u << p; S1[p] |= 1u << q; anyPair = 1; } }
  if (!anyPair) return false;
  walks3[0].clear(); walks3[1].clear();
  for (int i = 0; i < 2; i++) {
    curChunk = i; for (int x = 0; x < NV; x++) childR[ELL][x] = 1u << x; nzC[ELL] = (NV >= 32) ? 0xFFFFFFFFu : ((1u << NV) - 1);
    for (int e = 0; e < NV; e++) { u32 allowed = i == 0 ? S0[e] : S1[e]; if (!allowed) continue; bdfs4(ELL - 1, e, e, allowed); }
  }
  bool anyClosed = false; u8 sn[MAXL];
  static vector<u32> grp[2][MAXV][MAXV];
  for (int i = 0; i < 2; i++) for (int a = 0; a < NV; a++) for (int c = 0; c < NV; c++) grp[i][a][c].clear();
  for (int i = 0; i < 2; i++) for (u32 j = 0; j < walks3[i].size(); j++) grp[i][walks3[i][j].p][walks3[i][j].q].push_back(j);
  for (int p = 0; p < NV; p++) for (int q = 0; q < NV; q++) {
    auto& G0 = grp[0][p][q]; auto& G1 = grp[1][q][p]; if (G0.empty() || G1.empty()) continue;
    anyClosed = true;
    for (u32 ui : G0) { const Walk3& u = walks3[0][ui];
      for (u32 wi : G1) { const Walk3& w = walks3[1][wi]; pairsTried++;
        if (!(u.rows & w.any) || !(u.any & w.rows)) continue;  // necessary: a start digit x of a row of u must be an end digit of w, and vice versa
        bool live = false;
        u32 cand = u.rows & w.any;
        while (cand && !live) { int x = __builtin_ctz(cand); cand &= cand - 1; u32 m = u.N[x] & w.rows; while (m) { int q2 = __builtin_ctz(m); m &= m - 1; if ((w.N[q2] >> x) & 1) { live = true; break; } } }
        if (!live) continue;
        pairsLive++;
        memcpy(sn, u.cs, ELL); memcpy(sn + ELL, w.cs, ELL); canon(sn);
        size_t pos = arena.size(); arena.resize(pos + W); packKey(sn, arena.data() + pos);
      }
    }
  }
  return anyClosed;
}
static int EXPMODE = 4; static bool BFSCHUNK = false;
static inline bool expandAny(const u8* s) {
  if (ELL && !NOCHUNK) { if (EXPMODE == 4) return expandC4(s); if (EXPMODE == 3) return expandC3(s); return expandC(s); }
  u8 norm[MAXL]; return expandNorm(s, norm);
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
  Frame f; f.keyPos = kp; f.succBegin = b0; f.succEnd = arena.size(); f.next = b0; f.best = 1;
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
static int solveRaw(const u64* rootKeyRaw, double maxsec, bool& capped) {
  capped = false;
  u8 s[MAXL]; u64 nk[MAXW], rk[MAXW];
  size_t a0 = arena.size();
  unpackKey(rootKeyRaw, s); canon(s); packKey(s, nk);
  { size_t q = findSlot(nk); if (q != (size_t)-1) { if (VT[q] < 0) { fprintf(stderr, "unexpected: root on stack\n"); exit(5); } return VT[q]; } }
  if (!expandAny(s)) return 0;
  bool isNew; size_t sl = findOrInsert(nk, isNew);
  if (!isNew) { arena.resize(a0); return VT[sl]; }
  pushFrame(nk, a0);
  double tstart = now();
  while (!st.empty()) {
    Frame& f = st.back();
    if (f.next < f.succEnd) {
      memcpy(rk, arena.data() + f.next, W * 8); f.next += W;
      size_t q = findSlot(rk);
      if (q != (size_t)-1) { int32_t v = VT[q];
        if (v == VONSTACK) { nCycleEdges++; if (nCycleEdges <= 20) printCycleInfo(rk); if (f.best < INF) f.best = INF; }
        else f.best = max(f.best, v >= INF ? INF : v + 1);
        continue; }
      size_t b0 = arena.size();
      unpackKey(rk, s);
      if (!expandAny(s)) { if (f.best < 1) f.best = 1; continue; }
      bool nw; size_t p = findOrInsert(rk, nw); (void)p;
      if (!nw) { fprintf(stderr, "unexpected duplicate\n"); exit(6); }
      pushFrame(rk, b0);
    } else {
      int D = f.best;
      size_t p = findSlot(stackKeys.data() + f.keyPos);
      VT[p] = D >= INF ? INF : D;
      arena.resize(f.succBegin); stackKeys.resize(f.keyPos);
      st.pop_back();
      if (!st.empty()) { Frame& g = st.back(); g.best = max(g.best, D >= INF ? INF : D + 1); }
      if (st.empty()) return D;
    }
    if ((nExpand & 0x3FFFF) == 0) { double t = now(); if (t - lastPrint > 60) { lastPrint = t; fprintf(stderr, "progress t=%.0f states=%zu expand=%lld edges(plain)=%lld pairs=%lld live=%lld walks=%lld chTables=%zu chHit=%lld chMiss=%lld depth=%zu maxDepth=%d\n", t - T0, COUNT, nExpand, nEdges, pairsTried, pairsLive, nWalks, NM.size() / (2 * NV), chHit, chMiss, st.size(), maxDepth); fflush(stderr);
        if (t - tstart > maxsec) { capped = true; st.clear(); arena.clear(); stackKeys.clear(); return -1; } } }
  }
  return -1;
}

// ---------- memo-free tree DFS (mode -tree) ----------
static vector<u64> SK; static vector<uint8_t> SU; static size_t SKcap = 1 << 22, SKmask = (1 << 22) - 1, SKn = 0;
static inline u64 skHash(const u64* k) { u64 h = 0x9E3779B97F4A7C15ULL; for (int i = 0; i < W; i++) { h ^= k[i]; h *= 0xff51afd7ed558ccdULL; h ^= h >> 31; } return h; }
static inline void skInit() { SK.assign(SKcap * W, 0); SU.assign(SKcap, 0); SKn = 0; }
static inline bool skContains(const u64* k) { size_t p = skHash(k) & SKmask; while (SU[p]) { if (memcmp(SK.data() + p * W, k, W * 8) == 0) return true; p = (p + 1) & SKmask; } return false; }
static inline void skInsert(const u64* k) { size_t p = skHash(k) & SKmask; while (SU[p]) { if (memcmp(SK.data() + p * W, k, W * 8) == 0) return; p = (p + 1) & SKmask; } memcpy(SK.data() + p * W, k, W * 8); SU[p] = 1; SKn++; if (SKn * 2 > SKcap) { fprintf(stderr, "stack set full (depth %zu)\n", SKn); exit(7); } }
static inline void skErase(const u64* k) {
  size_t p = skHash(k) & SKmask; while (true) { if (!SU[p]) return; if (memcmp(SK.data() + p * W, k, W * 8) == 0) break; p = (p + 1) & SKmask; }
  SU[p] = 0; SKn--;
  size_t q = (p + 1) & SKmask;
  while (SU[q]) { size_t ideal = skHash(SK.data() + q * W) & SKmask; bool between = ((q - ideal) & SKmask) < ((q - p) & SKmask); if (!between) { memcpy(SK.data() + p * W, SK.data() + q * W, W * 8); SU[p] = 1; SU[q] = 0; p = q; } q = (q + 1) & SKmask; }
}
static long long treeCycleEdges = 0; static long long CAPNODES = 0; static long long towerNodes = 0; static bool nodeCapped = false;
static int solveTree(const u64* rootKeyRaw, double maxsec, bool& capped) {
  capped = false; u8 s[MAXL]; u64 rk[MAXW]; towerNodes = 0;
  size_t a0 = arena.size();
  unpackKey(rootKeyRaw, s); canon(s); packKey(s, rk);
  if (!expandAny(s)) return 0;
  skInsert(rk); pushFrame(rk, a0);
  double tstart = now();
  while (!st.empty()) {
    Frame& f = st.back();
    if (f.next < f.succEnd) {
      memcpy(rk, arena.data() + f.next, W * 8); f.next += W;
      if (skContains(rk)) { treeCycleEdges++; if (treeCycleEdges <= 20) { printf("TREE-CYCLE at depth %zu\n", st.size()); fflush(stdout); printCycleInfo(rk); } if (f.best < INF) f.best = INF; continue; }
      size_t b0 = arena.size();
      unpackKey(rk, s);
      if (!expandAny(s)) { if (f.best < 1) f.best = 1; continue; }
      towerNodes++;
      if (CAPNODES && towerNodes > CAPNODES) { capped = true; nodeCapped = true; arena.resize(a0); while (!st.empty()) { skErase(stackKeys.data() + st.back().keyPos); stackKeys.resize(st.back().keyPos); st.pop_back(); } return -1; }
      skInsert(rk); pushFrame(rk, b0);
    } else {
      int D = f.best;
      skErase(stackKeys.data() + f.keyPos);
      arena.resize(f.succBegin); stackKeys.resize(f.keyPos);
      st.pop_back();
      if (!st.empty()) { Frame& g = st.back(); g.best = max(g.best, D >= INF ? INF : D + 1); }
      if (st.empty()) return D;
    }
    if ((nExpand & 0xFFFFF) == 0) { double t = now(); if (t - lastPrint > 120) { lastPrint = t; fprintf(stderr, "progress t=%.0f expand=%lld edges(plain)=%lld pairs=%lld live=%lld walks=%lld depth=%zu maxDepth=%d skSize=%zu\n", t - T0, nExpand, nEdges, pairsTried, pairsLive, nWalks, st.size(), maxDepth, SKn); fflush(stderr);
        if (t - tstart > maxsec) { capped = true; st.clear(); arena.clear(); stackKeys.clear(); skInit(); return -1; } } }
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
    nxt.clear(); long long edges = 0, deadSucc = 0, maxCols = 0, newStates = 0, liveHere = 0, nper = 0; map<int,long long> colhist;
    for (size_t i = 0; i < nf; i++) {
      u8 s[MAXL], norm[MAXL]; unpackKey(frontier.data() + i * W, s);
      if (L % 2 == 0) { bool isper = true; for (int t = 0; t < L / 2; t++) if (s[t] != s[t + L / 2]) { isper = false; break; } nper += isper; }
      arena.clear(); nExpand++;
      bool has = BFSCHUNK ? expandAny(s) : expandNorm(s, norm);
      if (!has) continue;
      liveHere++;
      long long ncol = arena.size() / W; edges += ncol; maxCols = max(maxCols, ncol);
      int lg = 0; while ((1LL << (lg + 1)) <= ncol) lg++; colhist[lg]++;
      for (long long j = 0; j < ncol; j++) {
        u8 sn[MAXL]; unpackKey(arena.data() + j * W, sn); canon(sn); u64 k2[MAXW]; packKey(sn, k2);
        if (findSlot(k2) != (size_t)-1) continue;
        // liveness test of the successor (expansion only to see if a closed column exists); chunked children are live by construction
        if (!BFSCHUNK) { u8 norm2[MAXL]; size_t sv = arena.size(); bool live = expandNorm(sn, norm2); arena.resize(sv);
        if (!live) { deadSucc++; continue; } }
        bool isnew; size_t p = findOrInsert(k2, isnew); if (isnew) { VT[p] = lev; nxt.insert(nxt.end(), k2, k2 + W); newStates++; }
      }
      if ((nExpand & 0xFFFF) == 0 && now() - t0 > maxsec) { printf("BFS CAPPED time at level %d (frontier %zu, processed %zu)\n", lev, nf, i); return; }
    }
    printf("BFS level %d: frontier(live)=%zu halfperiodic=%lld edges=%lld deadSucc=%lld newLive=%lld maxCols=%lld seen=%zu t=%.1f hist(log2 cols):", lev, nf, nper, edges, deadSucc, newStates, maxCols, COUNT, now() - t0);
    for (auto& kv : colhist) printf(" %d:%lld", kv.first, kv.second); printf("\n"); fflush(stdout);
    if (nxt.size() / W > capFrontier) { printf("BFS CAPPED frontier %zu at level %d\n", nxt.size() / W, lev); return; }
    frontier.swap(nxt);
  }
}

// ---------- Knuth random-descent estimator of the live tree size (mode -knuth N) ----------
#include <random>
static void knuthEstimate(const u64* rootRaw, int samples, unsigned seed) {
  std::mt19937_64 rng(seed); double sumT = 0, sumT2 = 0; int maxDepthSeen = 0; double sumDepth = 0; int nDeep = 0;
  vector<u64> kids;
  for (int it = 0; it < samples; it++) {
    u64 cur[MAXW]; memcpy(cur, rootRaw, W * 8); u8 s[MAXL]; double wT = 1.0, total = 1.0; int depth = 0;
    { unpackKey(cur, s); canon(s); packKey(s, cur); }
    while (depth < 200000) {
      unpackKey(cur, s); arena.clear();
      bool any = expandAny(s);
      size_t m = arena.size() / W;
      if (!any || m == 0) break;
      wT *= (double)m; total += wT; depth++;
      size_t pick = (m == 1) ? 0 : (rng() % m);
      memcpy(cur, arena.data() + pick * W, W * 8);
      // (children are canonical keys; next loop unpacks)
    }
    sumT += total; sumT2 += total * total; maxDepthSeen = max(maxDepthSeen, depth); sumDepth += depth; if (depth >= 1) nDeep++;
  }
  double mean = sumT / samples; double var = sumT2 / samples - mean * mean; double se = sqrt(max(var, 0.0)) / sqrt((double)samples);
  printf("KNUTH samples=%d est_live_nodes=%.3e (se %.2e) maxDepthSample=%d meanDepth=%.1f\n", samples, mean, se, maxDepthSeen, sumDepth / samples); fflush(stdout);
}

// ---------- sequential Monte Carlo estimate of the live width per level (mode -smc N) ----------
#include <random>
static void smcEstimate(const u64* rootRaw, int Np, unsigned seed, int kmax, double maxsec, const string& tag) {
  std::mt19937_64 rng(seed); vector<u64> cur(W), kids, nxt; u8 s[MAXL];
  { memcpy(cur.data(), rootRaw, W * 8); unpackKey(cur.data(), s); canon(s); packKey(s, cur.data()); }
  double west = 1.0, tot = 1.0; int lev = 0; double t0 = now(); double maxWest = 1.0; int maxLev = 0;
  FILE* flog = nullptr; if (!tag.empty()) flog = fopen(("logs/t/smc_" + tag + ".txt").c_str(), "w");
  while (lev < kmax) {
    size_t n = cur.size() / W; if (n == 0) break;
    kids.clear(); long long live = 0;
    for (size_t i = 0; i < n; i++) { unpackKey(cur.data() + i * W, s); arena.clear(); bool any = expandAny(s); if (any) { kids.insert(kids.end(), arena.begin(), arena.end()); live++; } }
    lev++;
    size_t C = kids.size() / W;
    double est = west * ((double)C / (double)n); // estimated width of next level
    if (flog && (lev % 50 == 0 || lev < 20)) { fprintf(flog, "lev %d sample=%zu liveInSample=%lld children=%zu estWidthNext=%.3e estTotal=%.3e t=%.0f\n", lev, n, live, C, est, tot + est, now() - t0); fflush(flog); }
    west = est; tot += west; if (west > maxWest) { maxWest = west; maxLev = lev; }
    if (C == 0) { printf("SMC %s DIED(sample) at level %d estTotal=%.3e maxWidth=%.3e@%d samples=%d t=%.0f\n", tag.c_str(), lev, tot, maxWest, maxLev, Np, now() - t0); if (flog) fclose(flog); return; }
    if ((int)C > Np) { // sample Np uniformly without replacement (partial Fisher-Yates over key indices)
      vector<u32> idx(C); for (size_t i = 0; i < C; i++) idx[i] = (u32)i;
      nxt.resize(Np * W);
      for (int i = 0; i < Np; i++) { size_t j = i + rng() % (C - i); swap(idx[i], idx[j]); memcpy(nxt.data() + i * W, kids.data() + idx[i] * W, W * 8); }
      cur.swap(nxt);
    } else cur.swap(kids);
    if (now() - t0 > maxsec) { printf("SMC %s STOP(time) at level %d estWidth=%.3e estTotal=%.3e maxWidth=%.3e@%d t=%.0f\n", tag.c_str(), lev, west, tot, maxWest, maxLev, now() - t0); if (flog) fclose(flog); return; }
  }
  printf("SMC %s REACHED kmax level %d estWidth=%.3e estTotal=%.3e maxWidth=%.3e@%d t=%.0f\n", tag.c_str(), lev, west, tot, maxWest, maxLev, now() - t0); if (flog) fclose(flog);
}
int main(int argc, char** argv) {
  if (argc < 5) { fprintf(stderr, "usage: ifb b g L mode...\n"); return 2; }
  b = atoi(argv[1]); NV = 2 * b - 1; string gw = argv[2]; L = atoi(argv[3]); P = gw.size();
  if (L > MAXL) { fprintf(stderr, "L too large\n"); return 2; }
  for (int t = 0; t < L; t++) G[t] = gw[t % P] - '0';
  int EVERY = 0; string spec, runfile, smcTag; int smcN = 0, smcKmax = 100000; int d0 = 0; int knuthN = 0; int bfsK = 0; size_t bfsCap = 200000000; size_t slots0 = (size_t)1 << 24; double maxsec = 1e18; bool rot = true;
  for (int i = 4; i < argc; i++) { string a = argv[i];
    if (a == "-iface") spec = argv[++i]; else if (a == "-runfile") runfile = argv[++i]; else if (a == "-word") d0 = atoi(argv[++i]);
    else if (a == "-slots") slots0 = strtoull(argv[++i], nullptr, 10); else if (a == "-maxslots") MAXSLOTS = strtoull(argv[++i], nullptr, 10);
    else if (a == "-sec") maxsec = atof(argv[++i]); else if (a == "-norot") rot = false; else if (a == "-U") NORMU = true; else if (a == "-nochunk") NOCHUNK = true; else if (a == "-dbg") DBG = true; else if (a == "-bfschunk") BFSCHUNK = true; else if (a == "-smc") smcN = atoi(argv[++i]); else if (a == "-smctag") smcTag = argv[++i]; else if (a == "-smcmax") smcKmax = atoi(argv[++i]); else if (a == "-exp") EXPMODE = atoi(argv[++i]); else if (a == "-tree") TREE = true; else if (a == "-capnodes") CAPNODES = (long long)atof(argv[++i]); else if (a == "-knuth") knuthN = atoi(argv[++i]); else if (a == "-maxch") MAXCH = strtoull(argv[++i], nullptr, 10); else if (a == "-bfs") bfsK = atoi(argv[++i]); else if (a == "-bfscap") bfsCap = strtoull(argv[++i], nullptr, 10); else if (a == "-nodedup") DEDUP = false; else if (a == "-every") EVERY = atoi(argv[++i]); else if (a == "-cycfile") CYCFILE = argv[++i];
    else { fprintf(stderr, "unknown %s\n", a.c_str()); return 2; } }
  RN = rot ? L / P : 1; if (L % P) { fprintf(stderr, "P must divide L\n"); return 2; }
  int bits = keyBits(); W = (bits + 63) / 64; initTT();
  fprintf(stderr, "ifb b=%d g=%s L=%d P=%d keybits=%d W=%d rotations=%d\n", b, gw.c_str(), L, P, bits, W, RN);
  T0 = now(); tableAlloc(slots0); if (TREE) skInit();
  if (L % 2 == 0 && !NOCHUNK) { ELL = L / 2; CCLS[0] = 0; CCLS[1] = 0; for (int t = 0; t < ELL; t++) if (G[t] != G[t + ELL]) CCLS[1] = 1; int bits2 = 0; for (int t = 0; t < ELL; t++) bits2 += G[t] ? 7 : 3; int bits3 = 0; for (int t = 0; t < ELL; t++) bits3 += G[t + ELL] ? 7 : 3; CW = (max(bits2, bits3) + 63) / 64; for (int i = 0; i < 2; i++) ctabAlloc(ctab[i], 1u << 20); fprintf(stderr, "chunked: ELL=%d CW=%d classes=%d\n", ELL, CW, CCLS[1] + 1); }
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
    long long nb = birthKeys.size() / W, dies = 0, inf = 0, ncapped = 0; int maxK = 0; map<int,long long> hist;
    for (long long i = 0; i < nb; i++) {
      if (EVERY > 1 && (i % EVERY) != 0) continue;
      bool capped; int D = TREE ? solveTree(birthKeys.data() + i * W, maxsec, capped) : solveRaw(birthKeys.data() + i * W, maxsec, capped);
      if ((i & 0xFFF) == 0) { fprintf(stderr, "wordprogress tower %lld/%lld die=%lld inf=%lld capped=%lld maxK=%d expand=%lld t=%.0f\n", i, nb, dies, inf, ncapped, maxK, nExpand, now() - T0); fflush(stderr); }
      if (capped) { if (nodeCapped) { nodeCapped = false; ncapped++; u8 s[MAXL]; unpackKey(birthKeys.data() + i * W, s); printf("TCAP tower=%lld nodes=%lld iface=", i, towerNodes); for (int t = 0; t < L; t++) printf("%d", s[t] & 1); printf("|"); for (int t = 0; t < L; t++) printf("%d,", s[t] >> 3); printf("|"); for (int t = 0; t < L; t++) printf("%d", ((s[t] >> 1) & 3) + 1); printf("\n"); fflush(stdout); continue; }
        printf("CAPPED at tower %lld of %lld (time)\n", i, nb); fflush(stdout); return 0; }
      if (D >= INF) { inf++; u8 s[MAXL]; unpackKey(birthKeys.data() + i * W, s); printf("TINF tower=%lld iface=", i); for (int t = 0; t < L; t++) printf("%d", s[t] & 1); printf("|"); for (int t = 0; t < L; t++) printf("%d,", s[t] >> 3); printf("|"); for (int t = 0; t < L; t++) printf("%d", ((s[t] >> 1) & 3) + 1); printf("\n"); fflush(stdout); }
      else { dies++; hist[D + 1]++; maxK = max(maxK, D + 1); }
    }
    printf("IFB_WORD g=%s d0=%d L=%d interfaces=%zu a0=%d births=%lld die=%lld inf=%lld capped=%lld maxK=%d states=%zu expand=%lld edges=%lld maxDepth=%d t=%.1f\n", gw.c_str(), d0, L, ifs.size(), a0, nb, dies, inf, ncapped, maxK, COUNT, nExpand, nEdges, maxDepth, now() - T0);
    printf("HIST"); for (auto& kv : hist) printf(" %d:%lld", kv.first, kv.second); printf("\n");
    return 0;
  }
  vector<string> specs; if (!spec.empty()) specs.push_back(spec);
  if (!runfile.empty()) { FILE* f = fopen(runfile.c_str(), "r"); if (!f) { perror("runfile"); return 2; } char* line = nullptr; size_t cap = 0; while (getline(&line, &cap, f) > 0) { string sl(line); size_t p0 = sl.find("iface="); if (p0 == string::npos) continue; p0 += 6; size_t p1 = sl.find_first_of(" \n", p0); specs.push_back(sl.substr(p0, p1 - p0)); } fclose(f); }
  long long idx = 0;
  if (smcN) { for (auto& sp : specs) { idx++; u8 s[MAXL]; int Ln; if (!parseIface(sp, s, Ln) || Ln != L) continue; packKey(s, k); char tg[200]; snprintf(tg, 200, "%s_%lld", smcTag.c_str(), idx); smcEstimate(k, smcN, 7919 + idx, smcKmax, maxsec, tg); } return 0; }
  if (knuthN) { for (auto& sp : specs) { idx++; u8 s[MAXL]; int Ln; if (!parseIface(sp, s, Ln) || Ln != L) continue; packKey(s, k); printf("== KNUTH tower idx=%lld ", idx); knuthEstimate(k, knuthN, 12345); } return 0; }
  if (bfsK) { for (auto& sp : specs) { idx++; u8 s[MAXL]; int Ln; if (!parseIface(sp, s, Ln) || Ln != L) continue; packKey(s, k); printf("== BFS tower idx=%lld\n", idx); COUNT = 0; for (size_t i = 0; i < CAP; i++) VT[i] = VEMPTY; bfsStats(k, bfsK, bfsCap, maxsec); } return 0; }
  for (auto& sp : specs) {
    idx++;
    u8 s[MAXL]; int Ln; if (!parseIface(sp, s, Ln) || Ln != L) { fprintf(stderr, "bad spec %s\n", sp.c_str()); continue; }
    canon(s); packKey(s, k);
    bool capped; double t1 = now(); size_t c0 = COUNT;
    int D = TREE ? solveTree(k, maxsec, capped) : solveRaw(k, maxsec, capped);
    if (capped) { printf("TOWER idx=%lld CAPPED(%s) nodes=%lld states=%zu expand=%lld edges=%lld maxDepth=%d secs=%.1f iface=%s\n", idx, nodeCapped ? "nodes" : "time", towerNodes, COUNT, nExpand, nEdges, maxDepth, now() - t1, sp.c_str()); nodeCapped = false; }
    else if (D >= INF) printf("TOWER idx=%lld INF states=%zu expand=%lld edges=%lld maxDepth=%d cycleEdges=%lld secs=%.1f iface=%s\n", idx, COUNT, nExpand, nEdges, maxDepth, nCycleEdges, now() - t1, sp.c_str());
    else printf("TOWER idx=%lld DIES K=%d states=%zu newstates=%zu expand=%lld edges=%lld maxDepth=%d secs=%.1f iface=%s\n", idx, D + 1, COUNT, COUNT - c0, nExpand, nEdges, maxDepth, now() - t1, sp.c_str());
    fflush(stdout);
  }
  return 0;
}
