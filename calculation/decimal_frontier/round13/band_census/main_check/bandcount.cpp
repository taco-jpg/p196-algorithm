// bandcount.cpp -- main-session independent recount of the r13a band census.
// A band for clock g (period p): cyclic word V of length s, letters 0..18, V_(t+1) = R_(g_t)(V_t), V_T = V, every V_t has a letter != 9.
// R_g uses the unique periodic carries.  Bands = cycles of F = R_(g_(p-1)) o ... o R_(g_0) on phase-0 words, up to rotation; only
// primitive words (exact spatial period s).  Also prints, for each band, a canonical word and T (for later checks).
// usage: bandcount G S THREADS [list]
#include <algorithm>
#include <atomic>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <set>
#include <string>
#include <thread>
#include <vector>
using namespace std;
typedef uint64_t u64;
static int p, s;
static vector<int> g;
static u64 NW;
static u64 POW[10];

static inline bool rowstep(const int *x, int gam, int *y) {
  bool any = false;
  for (int c = 0; c < s; c++)
    if (x[c] != 9) {
      any = true;
      break;
    }
  if (!any) return false;
  // ascending carries: start at a position after a non-9 cell
  int al[8], be[8];
  int st = 0;
  while (x[st] == 9) st++;
  // carry out of cell st does not depend on its carry-in
  int a = (x[st] >= 10);
  for (int k = 1; k <= s; k++) {
    int c = (st + k) % s;
    al[c] = a;
    a = (x[c] + a >= 10);
  }
  // descending: beta_c = [x_c + beta_(c+1) >= 10]; carry out of a non-9 cell does not depend on its carry-in
  int b = (x[st] >= 10);
  for (int k = 1; k <= s; k++) {
    int c = (st - k + 2 * s) % s;
    // b = beta_(c+1)
    be[(c + 1) % s] = b;
    b = (x[c] + b >= 10);
  }
  int hi[8], lo[8];
  for (int c = 0; c < s; c++) {
    lo[c] = (x[c] + al[c]) % 10;
    hi[c] = (x[c] + be[(c + 1) % s]) % 10;
  }
  for (int c = 0; c < s; c++) y[c] = lo[c] + (gam ? hi[(c - 1 + s) % s] : hi[c]);
  return true;
}
static inline void decode(u64 w, int *x) {
  for (int c = 0; c < s; c++) {
    x[c] = (int)(w % 19);
    w /= 19;
  }
}
static inline u64 encode(const int *x) {
  u64 w = 0;
  for (int c = s - 1; c >= 0; c--) w = w * 19 + x[c];
  return w;
}
static inline bool Fmap(u64 w, u64 &out) {
  int a[8], bb[8];
  decode(w, a);
  for (int t = 0; t < p; t++) {
    if (!rowstep(a, g[t], bb)) return false;
    memcpy(a, bb, sizeof(int) * s);
  }
  // the final row must also have a letter != 9 (it is the next phase-0 row and is tested when it is used)
  bool any = false;
  for (int c = 0; c < s; c++)
    if (a[c] != 9) any = true;
  if (!any) return false;
  out = encode(a);
  return true;
}
static inline u64 rot(u64 w, int r) {
  int a[8], bb[8];
  decode(w, a);
  for (int c = 0; c < s; c++) bb[c] = a[(c + r) % s];
  return encode(bb);
}
static inline bool primitive(u64 w) {
  for (int d = 1; d < s; d++)
    if (s % d == 0 && rot(w, d) == w) return false;
  return true;
}

int main(int argc, char **argv) {
  string G = argv[1];
  s = atoi(argv[2]);
  int nth = atoi(argv[3]);
  bool list = argc > 4;
  p = (int)G.size();
  g.resize(p);
  for (int i = 0; i < p; i++) g[i] = G[i] - '0';
  NW = 1;
  for (int i = 0; i < s; i++) NW *= 19;
  vector<atomic<u64>> A(NW / 64 + 1), Bn(NW / 64 + 1);
  for (auto &x : A) x.store(~0ULL);
  // clear surplus bits
  {
    u64 extra = NW % 64;
    if (extra) A[NW / 64].store((1ULL << extra) - 1);
    else A[NW / 64].store(0);
  }
  u64 prev = NW + 1;
  int pass = 0;
  for (;;) {
    pass++;
    for (auto &x : Bn) x.store(0);
    atomic<u64> cnt(0), next_(0);
    vector<thread> th;
    for (int i = 0; i < nth; i++)
      th.emplace_back([&]() {
        const u64 CH = 1 << 16;
        for (;;) {
          u64 a = next_.fetch_add(CH);
          if (a >= NW) break;
          u64 e = min(NW, a + CH);
          for (u64 w = a; w < e; w++) {
            if (!((A[w >> 6].load(memory_order_relaxed) >> (w & 63)) & 1)) continue;
            u64 v;
            if (Fmap(w, v)) Bn[v >> 6].fetch_or(1ULL << (v & 63), memory_order_relaxed);
          }
        }
      });
    for (auto &x : th) x.join();
    // new set = image
    u64 c = 0;
    for (size_t i = 0; i < A.size(); i++) {
      u64 v = Bn[i].load();
      A[i].store(v);
      c += __builtin_popcountll(v);
    }
    if (c == prev) break;
    prev = c;
  }
  u64 total = prev;
  // F is a permutation of A; cycles up to rotation
  vector<atomic<u64>> seen(NW / 64 + 1);
  for (auto &x : seen) x.store(0);
  map<string, int> bands;
  u64 cycles_seen = 0;
  for (u64 w = 0; w < NW; w++) {
    if (!((A[w >> 6].load() >> (w & 63)) & 1)) continue;
    if ((seen[w >> 6].load() >> (w & 63)) & 1) continue;
    // cycle
    vector<u64> cyc;
    u64 x = w;
    do {
      seen[x >> 6].fetch_or(1ULL << (x & 63));
      cyc.push_back(x);
      u64 v;
      if (!Fmap(x, v)) {
        fprintf(stderr, "not a permutation\n");
        exit(2);
      }
      x = v;
    } while (x != w);
    cycles_seen++;
    if (!primitive(w)) continue;
    // canonical: minimal word among all rotations of all rows of the cycle
    u64 best = ~0ULL;
    for (u64 y : cyc)
      for (int r = 0; r < s; r++) best = min(best, rot(y, r));
    int a[8];
    decode(best, a);
    string k;
    for (int c = 0; c < s; c++) k += to_string(a[c]) + (c + 1 < s ? "," : "");
    int T = (int)cyc.size() * p;
    auto it = bands.find(k);
    if (it == bands.end())
      bands[k] = T;
    else if (it->second != T)
      fprintf(stderr, "same canonical word, different T: %s %d %d\n", k.c_str(), it->second, T);
  }
  printf("clock %s s=%d passes %d stable words %llu cycles %llu primitive bands up to rotation %zu\n", G.c_str(), s, pass, (unsigned long long)total, (unsigned long long)cycles_seen, bands.size());
  if (list)
    for (auto &kv : bands) printf("BAND %s T=%d\n", kv.first.c_str(), kv.second);
  return 0;
}
