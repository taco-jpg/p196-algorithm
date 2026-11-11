// fc_enum2.cpp (r12e): streaming / sharded version of r12b's fc_enum.cpp (same FKM generator, same F1 NFA, same pruning).
// Enumerates the rotation-canonical (necklace-minimal) binary words g of length p accepted by the first-coordinate NFA
// (cyclic: a closed walk labelled g exists), primitive AND imprimitive.
// usage: fc_enum2 b p [-shard i N]
//   stdout: the words of shard i (running index mod N == i), one per line;
//   stderr (one line at the end): FCE b=.. p=.. total=.. primitive=.. shard=i/N emitted=.. emitted_primitive=.. byG: G:count ...
//   (total / primitive / byG count ALL words, so every shard must report the same totals; sum of emitted = total.)
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <map>
using namespace std;
typedef uint64_t u64;
int b, NS;
u64 succ[2][64];
int p;
struct Rows { u64 r[64]; };
static inline bool nonempty(const Rows& R) { for (int s = 0; s < NS; s++) if (R.r[s]) return true; return false; }
static inline void extend(const Rows& R, int a, Rows& out) {
  for (int s = 0; s < NS; s++) { u64 m = R.r[s], o = 0; while (m) { int c = __builtin_ctzll(m); m &= m - 1; o |= succ[a][c]; } out.r[s] = o; }
}
static inline bool closed(const Rows& R) { for (int s = 0; s < NS; s++) if (R.r[s] & (1ULL << s)) return true; return false; }
vector<int> w;
map<int, long long> cntG; long long cntAll = 0, cntPrim = 0, emitted = 0, emittedPrim = 0;
long long SH_I = 0, SH_N = 1;
static char linebuf[256];
void emit(int G, bool prim) {
  long long idx = cntAll;
  cntAll++; cntG[G]++; if (prim) cntPrim++;
  if (idx % SH_N != SH_I) return;
  emitted++; if (prim) emittedPrim++;
  for (int i = 1; i <= p; i++) linebuf[i - 1] = (char)('0' + w[i]);
  linebuf[p] = '\n';
  fwrite(linebuf, 1, p + 1, stdout);
}
void gen(int t, int pp, int G, const Rows& R) {
  if (t > p) {
    if (p % pp == 0) { if (closed(R)) emit(G, pp == p); }
    return;
  }
  for (int a = w[t - pp]; a <= 1; a++) {
    Rows R2; extend(R, a, R2); if (!nonempty(R2)) continue;
    w[t] = a;
    gen(t + 1, (a == w[t - pp]) ? pp : t, G + a, R2);
  }
}
int main(int argc, char** argv) {
  if (argc < 3) { fprintf(stderr, "usage: fc_enum2 b p [-shard i N]\n"); return 2; }
  b = atoi(argv[1]); p = atoi(argv[2]); NS = 2 * b - 2;
  for (int i = 3; i < argc; i++) { string a = argv[i]; if (a == "-shard") { SH_I = atoll(argv[++i]); SH_N = atoll(argv[++i]); } }
  if (p < 1 || p > 250 || SH_N < 1 || SH_I < 0 || SH_I >= SH_N) { fprintf(stderr, "bad args\n"); return 2; }
  static char obuf[1 << 22]; setvbuf(stdout, obuf, _IOFBF, sizeof obuf);
  memset(succ, 0, sizeof succ);
  for (int q = 1; q <= NS; q++) for (int h = 0; h < 2; h++) {
    if (q + h < b) { int q2 = 2 * q + h; if (q2 <= NS) succ[0][q - 1] |= 1ULL << (q2 - 1); }
    else { int q2 = (q % b) + 1; if (q2 <= NS) succ[1][q - 1] |= 1ULL << (q2 - 1); }
  }
  w.assign(p + 2, 0); w[0] = 0;
  Rows R0; for (int s = 0; s < NS; s++) R0.r[s] = 1ULL << s;
  gen(1, 1, 0, R0);
  fflush(stdout);
  fprintf(stderr, "FCE b=%d p=%d total=%lld primitive=%lld shard=%lld/%lld emitted=%lld emitted_primitive=%lld byG:", b, p, cntAll, cntPrim, SH_I, SH_N, emitted, emittedPrim);
  for (auto& kv : cntG) fprintf(stderr, " %d:%lld", kv.first, kv.second);
  fprintf(stderr, "\n");
  return 0;
}
