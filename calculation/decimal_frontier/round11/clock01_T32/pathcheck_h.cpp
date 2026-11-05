// pathcheck_h.cpp -- r11b variant: tests the sparse LEVEL family BB'_w of lvl.cpp (winhash.h) instead of the bitset BB_w.
// usage: HDIR=dir pathcheck_h B T CLOCK w
// (original header) pathcheck.cpp -- r9u: exhaustive check of the co-reachability window family BB_w on small exact graphs.
// Builds the WHOLE reach graph from the bottom interface in memory (no quotient), marks every state from which a target
// (uniform band with period | T, or 9-wire interface) is reachable, and tests every state that lies on a bottom -> target path
// (reachable AND co-reachable) against A_w and BB_w (all windows, wrapped ones included). Any failure would refute the BB_w filter.
// Also reports the first target height (shortest path) found by plain BFS.
// usage: WINDIR=dir pathcheck B T CLOCK w
#include "winhash.h"
#include <unordered_map>
#include <set>
#include <deque>
#include <algorithm>
using namespace std;
typedef uint64_t u64; typedef unsigned __int128 u128;
static int B, T, NOV; static int ovf[64], OVI[64]; static u64 MASK;
struct K { u64 c, d; u128 r; bool operator==(const K& o) const { return c == o.c && d == o.d && r == o.r; } };
struct KH { size_t operator()(const K& k) const { u64 h = k.c * 0x9E3779B97F4A7C15ULL ^ (k.d + 0x632BE59BD9B4E019ULL) * 0xBF58476D1CE4E5B9ULL ^ (u64)k.r * 0x94D049BB133111EBULL ^ (u64)(k.r >> 64); h ^= h >> 31; return h; } };
struct Fwd {   // identical to backdisk's FwdExp
  u64 cc, cd; u128 cr; int x0; bool root; u64 cs, ds; u128 rs; vector<K>* out;
  void dfs(int t, int x) {
    if (t == T) { if (x == x0) out->push_back({cs, ds, rs}); return; }
    if (root && x == 0) return;
    int cin = (cc >> t) & 1, dneed = (cd >> t) & 1;
    for (int d = 0; d < 2; d++) {
      if ((x + d) / B != dneed) continue;
      int e = (x + cin) % B, r = (x + d) % B, co = (x + cin) / B;
      int nx = ovf[t] ? e + (int)((cr >> (4 * OVI[t])) & 15) : e + r;
      u64 sc = cs, sd = ds; u128 sr = rs;
      cs |= (u64)co << t; ds |= (u64)d << t; if (ovf[t]) rs |= (u128)r << (4 * OVI[t]);
      dfs(t + 1, nx); cs = sc; ds = sd; rs = sr;
    }
  }
  void expand(const K& k, bool isRoot, vector<K>& o) { cc = k.c; cd = k.d; cr = k.r; root = isRoot; out = &o; for (x0 = isRoot ? 1 : 0; x0 <= 2 * B - 2; x0++) { cs = ds = 0; rs = 0; dfs(0, x0); } }
};
int main(int argc, char** argv) {
  B = atoi(argv[1]); T = atoi(argv[2]); string pat = argv[3]; int w = atoi(argv[4]);
  MASK = (T == 64) ? ~0ULL : ((1ULL << T) - 1); NOV = 0;
  for (int t = 0; t < T; t++) { ovf[t] = pat[t % pat.size()] - '0'; OVI[t] = ovf[t] ? NOV++ : -1; }
  if (!wh::load(getenv("HDIR"), B, pat, w, T, NOV, 4)) return 2;
  // targets
  set<pair<u64, u128>> bandKeys;   // (c, r) with d = c
  { auto f = [&](int v) { int c = v >= B; return 2 * ((v + c) % B); };
    for (int v0 = 0; v0 <= 2 * B - 2; v0++) { int v = v0; for (int i = 0; i < 4 * B; i++) v = f(v);
      vector<int> cy; int u = v; bool bad = false; do { if (u == B - 1) bad = true; cy.push_back(u); u = f(u); } while (u != v && (int)cy.size() <= 2 * B);
      if (bad || u != v || T % (int)cy.size()) continue;
      for (int ph = 0; ph < (int)cy.size(); ph++) { u64 c = 0; u128 r = 0; for (int t = 0; t < T; t++) { int z = cy[(t + ph) % cy.size()], cv = z >= B; c |= (u64)cv << t; if (ovf[t]) r |= (u128)((z + cv) % B) << (4 * OVI[t]); } bandKeys.insert({c, r}); } } }
  auto isTarget = [&](const K& k) {
    if (k.c == k.d && bandKeys.count({k.c, k.r})) return true;
    if (((~k.c) & MASK) == k.d) { for (int t = 0; t < T; t++) if (ovf[t] && (int)((k.r >> (4 * OVI[t])) & 15) != (B - 1) * (int)((k.c >> t) & 1)) return false; return true; }
    return false;
  };
  u64 BOTD = 0; u128 BOTR = 0; for (int t = 0; t < T; t++) if (ovf[t]) { BOTD |= 1ULL << t; BOTR |= (u128)1 << (4 * OVI[t]); }
  K bot{0, BOTD, BOTR};
  unordered_map<K, uint32_t, KH> id; vector<K> st; vector<vector<uint32_t>> succ; vector<int> height;
  Fwd fx; vector<K> tmp; deque<uint32_t> q;
  // node 0 = bottom (root edges); a later return to the bottom interface is a separate node (non-root edges)
  st.push_back(bot); succ.emplace_back(); height.push_back(0); q.push_back(0);
  int firstHit = -1;
  while (!q.empty()) {
    uint32_t i = q.front(); q.pop_front(); tmp.clear(); fx.expand(st[i], i == 0, tmp);
    for (const K& s : tmp) {
      auto it = id.find(s); uint32_t j;
      if (it == id.end()) { j = st.size(); id[s] = j; st.push_back(s); succ.emplace_back(); height.push_back(height[i] + 1); q.push_back(j);
        if (isTarget(s) && firstHit < 0) firstHit = height[j]; }
      else j = it->second;
      succ[i].push_back(j);
    }
    if (st.size() > 30000000) { printf("TOO_BIG\n"); return 3; }
  }
  size_t n = st.size(); vector<char> co(n, 0); vector<vector<uint32_t>> pred(n);
  for (size_t i = 0; i < n; i++) { sort(succ[i].begin(), succ[i].end()); succ[i].erase(unique(succ[i].begin(), succ[i].end()), succ[i].end()); for (uint32_t j : succ[i]) pred[j].push_back(i); }
  deque<uint32_t> bq; size_t ntg = 0;
  for (size_t i = 1; i < n; i++) if (isTarget(st[i])) { co[i] = 1; bq.push_back(i); ntg++; }
  while (!bq.empty()) { uint32_t j = bq.front(); bq.pop_front(); for (uint32_t i : pred[j]) if (!co[i]) { co[i] = 1; bq.push_back(i); } }
  size_t onPath = 0, failA = 0, failB = 0, offPathInB = 0, reach = n - 1;
  for (size_t i = 1; i < n; i++) {
    bool a = true, b = wh::allInB(st[i].c, st[i].d, st[i].r);
    if (!a) failA++;
    if (co[i]) { onPath++; if (!b) failB++; } else if (b) offPathInB++;
  }
  printf("PATHCHECK B=%d T=%d clock=%s w=%d: reachable %zu, target states %zu, first target height %d, on bottom->target paths %zu, "
         "(A_w not tested) %zu, on-path outside BB'_w %zu (must be 0), off-path states that pass BB'_w %zu (of %zu off-path) -> %s\n",
         B, T, pat.c_str(), w, reach, ntg, firstHit, onPath, failA, failB, offPathInB, reach - onPath, (failA || failB) ? "FAIL" : "PASS");
  return 0;
}
