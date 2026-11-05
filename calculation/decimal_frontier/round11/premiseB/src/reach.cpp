// reach.cpp -- exact reachability over periodic left-end interfaces, ANY height (replaces the per-height iteration of
// up4/upband2/up5, whose interface sets need not repeat quickly: round 4 saw no repeat at T=24 after 400 heights).
//
// Left end = cells 0..H-1 of the pair word (P_x = d_x + d_{n-1-x}), every cell periodic in time with period T, overflow
// clock CLOCK (repeated to length T). Cell rule (same as up4/upband2): e=(x+a)%B, r=(x+D)%B, carry up (x+a)/B, carry down
// (x+D)/B; next value e+r (no overflow) or e+r_{cell below} (overflow step).
// Interface between cell x-1 and x = (carry provided upward c[t], carry required from above d[t], r-digit at overflow
// times). Bottom: carry 0 into cell 0, r_{-1}=1, carry out of cell 0 downward = overflow bit, cell 0 >= 1 at ALL times
// (it contains the leading digit). This is a finite graph; "some left end of some height H fits" <=> "an accepting
// interface is reachable from the bottom". BFS with a visited set decides it exactly (RESULT COMPLETE when the frontier
// is empty). BFS order gives the minimal height. Parent pointers give the left end itself (printed on a fit).
//
// usage: BAND='1:3,0:6' PH=0 ./reach B T CLOCK BAND [cap] [maxdepth]   uniform band acceptance (stops at first fit,
//                                                                        ALLFITS=1 continues and counts)
//        ./reach B T CLOCK WIRE [cap] [maxdepth]                        9-wire acceptance (lists every stream)
// BAND = "c:r,c:r,..." carry bit and r-digit of the band per band time step; PH = band phase at t=0.
// Output: "BAND FITS at height H (phase PH)" + LEFTEND block | "NEW STREAM at height H: ..." |
//         "RESULT COMPLETE: ..." | "RESULT EMPTY at height 1" | "RESULT TOO_BIG ..." | "RESULT MAXDEPTH ..."
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <set>
#include <algorithm>
#include <chrono>
#include <sys/resource.h>
using namespace std;
typedef uint64_t u64; typedef unsigned __int128 u128;
struct Node { u64 c, d; u128 r; };

static int B, T, NOV = 0, PH = 0, Q = 0; static bool WIRE = false, ALLFITS = false;
static int ovf[64], OVI[64], BC[64], BR[64];
static u64 MASK;

// chunked storage: no reallocation copies for huge runs
static const int CH = 20; static const u64 CHN = 1ULL << CH;
static vector<Node*> nodeChunks; static vector<uint32_t*> parChunks; static u64 NN = 0;
static inline Node& node(u64 i) { return nodeChunks[i >> CH][i & (CHN - 1)]; }
static inline uint32_t& par(u64 i) { return parChunks[i >> CH][i & (CHN - 1)]; }
static void push(const Node& n, uint32_t p) {
  if ((NN >> CH) >= nodeChunks.size()) { nodeChunks.push_back((Node*)malloc(sizeof(Node) * CHN)); parChunks.push_back((uint32_t*)malloc(4 * CHN)); }
  node(NN) = n; par(NN) = p; NN++;
}
static vector<uint32_t> table; static u64 tmask;  // open addressing, slot = index+1, 0 = empty
static inline u64 hnode(const Node& n) {
  u64 lo = (u64)n.r, hi = (u64)(n.r >> 64);
  u64 h = n.c * 0x9E3779B97F4A7C15ULL ^ (n.d + 0x632BE59BD9B4E019ULL) * 0xBF58476D1CE4E5B9ULL;
  h ^= lo * 0x94D049BB133111EBULL; h ^= (hi + 0x2545F4914F6CDD1DULL) * 0xD6E8FEB86659FD93ULL;
  h ^= h >> 31; h *= 0xBF58476D1CE4E5B9ULL; h ^= h >> 29; return h;
}
static void rehash(u64 newsize) {
  vector<uint32_t> nt(newsize, 0); u64 m = newsize - 1;
  for (u64 i = 0; i < NN; i++) { u64 k = hnode(node(i)) & m; while (nt[k]) k = (k + 1) & m; nt[k] = (uint32_t)(i + 1); }
  table.swap(nt); tmask = m;
}
// returns index of node (new or old), sets isnew
static u64 insert(const Node& n, uint32_t p, bool& isnew) {
  if ((NN + 1) * 2 > table.size()) rehash(table.size() * 2);
  u64 k = hnode(n) & tmask;
  while (true) {
    uint32_t v = table[k];
    if (!v) { push(n, p); table[k] = (uint32_t)NN; isnew = true; return NN - 1; }
    const Node& m = node(v - 1);
    if (m.c == n.c && m.d == n.d && m.r == n.r) { isnew = false; return v - 1; }
    k = (k + 1) & tmask;
  }
}

static bool accepts(const Node& n) {
  if (WIRE) {
    if (((~n.c) & MASK) != n.d) return false;
    for (int t = 0; t < T; t++) if (ovf[t]) { int r = (int)((n.r >> (4 * OVI[t])) & 15); if (r != (B - 1) * (int)((n.c >> t) & 1)) return false; }
    return true;
  }
  for (int t = 0; t < T; t++) {
    int k = (t + PH) % Q, hi = BC[k];
    if ((int)((n.c >> t) & 1) != hi || (int)((n.d >> t) & 1) != hi) return false;
    if (ovf[t] && (int)((n.r >> (4 * OVI[t])) & 15) != BR[k]) return false;
  }
  return true;
}

// expansion of one interface
static Node cur; static int x0g; static u64 cs, ds; static u128 rs; static bool rootExp; static uint32_t curIdx;
static int depthNow; static u64 fitIdx = ~0ULL; static int fitH = -1; static u64 nfits = 0;
static set<u64> streams;
// reconstruction mode
static bool recMode = false; static Node target; static int xs[64], xsFound[64]; static bool found;

static void leaf() {
  Node n{cs, ds, rs};
  if (recMode) { if (!found && n.c == target.c && n.d == target.d && n.r == target.r) { found = true; memcpy(xsFound, xs, sizeof(xs)); } return; }
  bool isnew; u64 idx = insert(n, curIdx, isnew);
  if (isnew && accepts(n)) {
    nfits++;
    if (WIRE) { if (!streams.count(n.c)) { streams.insert(n.c); printf("  NEW STREAM at height %d: ", depthNow + 1); for (int t = 0; t < T; t++) printf("%d", (int)((n.c >> t) & 1)); printf("\n"); fflush(stdout); } }
    else if (fitIdx == ~0ULL) { fitIdx = idx; fitH = depthNow + 1; }
  }
}
static void dfs(int t, int x) {
  if (recMode && found) return;
  if (t == T) { if (x == x0g) leaf(); return; }
  if (rootExp && x == 0) return;  // cell 0 contains the leading digit: >= 1 at all times
  xs[t] = x;
  int cin = (cur.c >> t) & 1, dneed = (cur.d >> t) & 1;
  for (int d = 0; d < 2; d++) {
    if ((x + d) / B != dneed) continue;
    int e = (x + cin) % B, r = (x + d) % B, co = (x + cin) / B;
    int nx = ovf[t] ? e + (int)((cur.r >> (4 * OVI[t])) & 15) : e + r;
    u64 sc = cs, sd = ds; u128 sr = rs;
    cs |= (u64)co << t; ds |= (u64)d << t; if (ovf[t]) rs |= (u128)r << (4 * OVI[t]);
    dfs(t + 1, nx);
    cs = sc; ds = sd; rs = sr;
  }
}
static void expand(const Node& f, bool root) {
  cur = f; rootExp = root;
  for (x0g = root ? 1 : 0; x0g <= 2 * B - 2; x0g++) { cs = ds = 0; rs = 0; dfs(0, x0g); }
}
static double rssGB() {
  struct rusage ru; getrusage(RUSAGE_SELF, &ru);
#ifdef __APPLE__
  return ru.ru_maxrss / 1e9;
#else
  return ru.ru_maxrss / 1e6;
#endif
}

int main(int argc, char** argv) {
  if (argc < 5) { fprintf(stderr, "usage: [BAND=.. PH=..] reach B T CLOCK BAND|WIRE [cap] [maxdepth]\n"); return 2; }
  B = atoi(argv[1]); T = atoi(argv[2]); string pat = argv[3]; string mode = argv[4];
  u64 cap = argc > 5 ? strtoull(argv[5], 0, 10) : 2000000000ULL; int maxdepth = argc > 6 ? atoi(argv[6]) : 1000000;
  if (cap > 4000000000ULL) cap = 4000000000ULL;
  WIRE = (mode == "WIRE"); ALLFITS = getenv("ALLFITS") && atoi(getenv("ALLFITS"));
  PH = getenv("PH") ? atoi(getenv("PH")) : 0;
  if (B > 16 || T > 64 || T < 1) { fprintf(stderr, "need B<=16, T<=64\n"); return 2; }
  MASK = (T == 64) ? ~0ULL : ((1ULL << T) - 1);
  for (int t = 0; t < T; t++) { ovf[t] = pat[t % pat.size()] - '0'; OVI[t] = -1; if (ovf[t]) OVI[t] = NOV++; }
  if (NOV > 32) { fprintf(stderr, "more than 32 overflow steps per period\n"); return 2; }
  if (!WIRE) {
    string bs = getenv("BAND") ? getenv("BAND") : "1:3,0:6"; size_t p = 0;
    while (p < bs.size()) { size_t q = bs.find(',', p); if (q == string::npos) q = bs.size(); string it = bs.substr(p, q - p); BC[Q] = it[0] - '0'; BR[Q] = atoi(it.c_str() + 2); Q++; p = q + 1; }
    if (T % Q) { fprintf(stderr, "T must be a multiple of the band period %d\n", Q); return 2; }
  }
  printf("reach B=%d T=%d clock=%s mode=%s%s%s PH=%d cap=%llu\n", B, T, pat.c_str(), mode.c_str(), WIRE ? "" : " band=", WIRE ? "" : (getenv("BAND") ? getenv("BAND") : "1:3,0:6"), PH, (unsigned long long)cap);
  table.assign(1 << 20, 0); tmask = table.size() - 1;
  auto t0 = chrono::steady_clock::now();
  Node root{0, 0, 0};
  for (int t = 0; t < T; t++) if (ovf[t]) { root.d |= 1ULL << t; root.r |= (u128)1 << (4 * OVI[t]); }
  depthNow = 0; curIdx = UINT32_MAX; expand(root, true);
  u64 lo = 0, hi = NN; int depth = 1;
  printf("height 1: %llu interfaces\n", (unsigned long long)NN); fflush(stdout);
  if (NN == 0) { printf("RESULT EMPTY at height 1\n"); return 0; }
  bool stopped = false;
  while (lo < hi && !(fitIdx != ~0ULL && !ALLFITS)) {
    if (depth >= maxdepth) { printf("RESULT MAXDEPTH at height %d: %llu interfaces visited, frontier %llu\n", depth, (unsigned long long)NN, (unsigned long long)(hi - lo)); stopped = true; break; }
    depthNow = depth;
    for (u64 i = lo; i < hi; i++) {
      Node f = node(i); curIdx = (uint32_t)i; expand(f, false);
      if (NN > cap) break;
      if (fitIdx != ~0ULL && !ALLFITS) break;
    }
    double secs = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    printf("height %d: %llu new, %llu visited, %.1f s, maxrss %.2f GB%s\n", depth + 1, (unsigned long long)(NN - hi), (unsigned long long)NN, secs, rssGB(), nfits ? "  <-- FITS" : "");
    fflush(stdout);
    if (NN > cap) { printf("RESULT TOO_BIG at height %d: %llu interfaces visited (cap %llu)\n", depth + 1, (unsigned long long)NN, (unsigned long long)cap); stopped = true; break; }
    lo = hi; hi = NN; depth++;
  }
  if (!WIRE && fitIdx != ~0ULL) {
    printf("  BAND FITS at height %d (phase %d)\n", fitH, PH);
    // reconstruct the left end: path root -> fit node, then the cell evolution of every edge
    vector<u64> path; for (u64 i = fitIdx;; i = par(i)) { path.push_back(i); if (par(i) == UINT32_MAX) break; }
    reverse(path.begin(), path.end());
    printf("LEFTEND B=%d T=%d clock=%s band=%s PH=%d H=%zu\n", B, T, pat.c_str(), getenv("BAND") ? getenv("BAND") : "1:3,0:6", PH, path.size());
    recMode = true; Node prev = root; bool ok = true;
    for (size_t k = 0; k < path.size(); k++) {
      target = node(path[k]); found = false; expand(prev, k == 0);
      if (!found) { ok = false; printf("RECONSTRUCTION FAILED at cell %zu\n", k); break; }
      printf("cell %zu:", k); for (int t = 0; t < T; t++) printf(" %d", xsFound[t]); printf("\n");
      prev = target;
    }
    printf("END LEFTEND %s\n", ok ? "ok" : "FAILED");
    if (!ALLFITS) { printf("RESULT FIT at height %d\n", fitH); return 0; }
  }
  if (!stopped) {
    double secs = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    printf("RESULT COMPLETE: frontier empty after height %d; %llu interfaces reachable; accepting interfaces %llu; %s %zu; %.1f s; maxrss %.2f GB\n",
           depth, (unsigned long long)NN, (unsigned long long)nfits, WIRE ? "distinct streams" : "band fits", WIRE ? streams.size() : (size_t)(fitIdx != ~0ULL), secs, rssGB());
  }
  return 0;
}
