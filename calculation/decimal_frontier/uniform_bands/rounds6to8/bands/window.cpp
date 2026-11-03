// window.cpp -- round 7: window abstraction of the reach graph (sound over-approximation, independent of T).
// A window is the content of the interface on w consecutive time slots starting at clock phase PH: c, d and the r digits at the
// overflow slots inside the window. The running value x at the window start is unknown (any of 0..2B-2), and the closure x_T = x0 is
// dropped. Every real edge I -> J induces an abstract edge between the window contents, so the window contents of every real reachable
// interface (of ANY period T whose clock is the given word) lie in the abstract reachable set A_w (BFS from the bottom pattern).
// If a window of a target stream is not in A_w, no left end of any period T (clock word repeated) can carry that stream: UNREACHABLE.
// usage: window B CLOCK PH w cap WORD [WORD...]   (WORD = a periodic stream; all alignments are tested, d = complement, r = (B-1) c at overflows)
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <string>
#include <vector>
#include <unordered_set>
#include <deque>
using namespace std;
typedef unsigned __int128 u128; typedef uint64_t u64;
static int B, W, PH; static string PAT; static int ovf[64], OVI[64], NOV = 0;
struct H { size_t operator()(const u128& k) const { u64 a = (u64)k, b = (u64)(k >> 64); u64 h = a * 0x9E3779B97F4A7C15ULL ^ (b + 0x632BE59BD9B4E019ULL) * 0xBF58476D1CE4E5B9ULL; h ^= h >> 31; return h; } };
// key layout: c at bits 0..w-1, d at w..2w-1, r nibbles from bit 2w
static inline u128 mk(u64 c, u64 d, u128 r) { return (u128)c | ((u128)d << W) | (r << (2 * W)); }
static inline void un(u128 k, u64& c, u64& d, u128& r) { u64 m = (W == 64) ? ~0ULL : ((1ULL << W) - 1); c = (u64)k & m; d = (u64)(k >> W) & m; r = k >> (2 * W); }
struct Exp {
  u64 cc, cd; u128 cr; u64 cs, ds; u128 rs; vector<u128>* out;
  void dfs(int t, int x) {
    if (t == W) { out->push_back(mk(cs, ds, rs)); return; }
    int cin = (cc >> t) & 1, dneed = (cd >> t) & 1;
    for (int d = 0; d < 2; d++) {
      if ((x + d) / B != dneed) continue;
      int e = (x + cin) % B, r = (x + d) % B, co = (x + cin) / B;
      int nx = ovf[t] ? e + (int)((cr >> (4 * OVI[t])) & 15) : e + r;
      u64 sc = cs, sd = ds; u128 sr = rs;
      cs |= (u64)co << t; ds |= (u64)d << t; if (ovf[t]) rs |= (u128)r << (4 * OVI[t]);
      dfs(t + 1, nx);
      cs = sc; ds = sd; rs = sr;
    }
  }
  void expand(u128 k, vector<u128>& o) {
    un(k, cc, cd, cr); out = &o;
    for (int x0 = 0; x0 <= 2 * B - 2; x0++) { cs = ds = 0; rs = 0; dfs(0, x0); }
  }
};
int main(int argc, char** argv) {
  if (argc < 7) { fprintf(stderr, "usage: window B CLOCK PH w cap WORD...\n"); return 2; }
  B = atoi(argv[1]); PAT = argv[2]; PH = atoi(argv[3]); W = atoi(argv[4]); u64 cap = strtoull(argv[5], 0, 10);
  if (W > 32) { fprintf(stderr, "w <= 32\n"); return 2; }
  for (int t = 0; t < W; t++) { ovf[t] = PAT[(PH + t) % PAT.size()] - '0'; OVI[t] = -1; if (ovf[t]) OVI[t] = NOV++; }
  u64 bc = 0, bd = 0; u128 br = 0;
  for (int t = 0; t < W; t++) if (ovf[t]) { bd |= 1ULL << t; br |= (u128)1 << (4 * OVI[t]); }
  unordered_set<u128, H> seen; deque<u128> q; u128 b0 = mk(bc, bd, br); seen.insert(b0); q.push_back(b0);
  Exp ex; vector<u128> succ; u64 expanded = 0;
  while (!q.empty()) {
    u128 k = q.front(); q.pop_front(); succ.clear(); ex.expand(k, succ); expanded++;
    for (u128 s : succ) if (seen.insert(s).second) q.push_back(s);
    if (seen.size() > cap) { printf("WINDOW B=%d clock=%s ph=%d w=%d: TOO_BIG (%zu states)\n", B, PAT.c_str(), PH, W, seen.size()); return 3; }
  }
  printf("WINDOW B=%d clock=%s ph=%d w=%d: abstract reachable set %zu states\n", B, PAT.c_str(), PH, W, seen.size());
  for (int a = 6; a < argc; a++) {
    string word = argv[a]; int L = word.size(); int hit = 0;
    for (int o = 0; o < L; o++) {
      u64 c = 0; for (int t = 0; t < W; t++) if (word[(o + t) % L] == '1') c |= 1ULL << t;
      u64 m = (1ULL << W) - 1, d = (~c) & m; u128 r = 0;
      for (int t = 0; t < W; t++) if (ovf[t]) r |= (u128)((B - 1) * (int)((c >> t) & 1)) << (4 * OVI[t]);
      bool in = seen.count(mk(c, d, r)) > 0; hit += in;
      printf("  word %s alignment %d: %s\n", word.c_str(), o, in ? "IN the abstract set (not excluded)" : "NOT in the abstract set -> UNREACHABLE for every T");
    }
    printf("  word %s: %d of %d alignments not excluded\n", word.c_str(), hit, L);
  }
  return 0;
}
