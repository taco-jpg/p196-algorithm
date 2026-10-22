// Backward "infinite-history" core of the width-K prefix abstraction.
//
// Graph G_K: nodes = words q_0..q_{K-1} (entries 0..18); edges s -> forwardPrefix(s,e),
// e in {0,1}, for every source with s_0 > 0 (exactly the converse of Lean's
// longPred/prefixPredecessors, checked by check_ref.py).
// Peeling nodes of in-degree 0 round by round leaves C_K = the set of nodes with
// arbitrarily long backward paths (= nodes reachable from a cycle).  For a peeled
// node, its round number = 1 + length of the longest backward path ending at it
// (long regime only; short-width ancestry is NOT counted).
//
// Usage: peel K F.bits OUT
//   F.bits: forward-closure bitset from fwdclosure (same K), used to test F subset C.
// Output OUT.tsv: one line per 4-digit prefix P (1000..9999) [or 3-digit if K==3]:
//   P  hitF  hitC  maxdepth
//     hitF     = 1 iff some word of F with all entries <= 9 starts with P
//     hitC     = 1 iff some node of C_K with all entries <= 9 starts with P
//     maxdepth = max peel round over long initial words P++tail (tail digits),
//                -1 if hitC
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static int K;
static uint64_t NW, NWORDS64;
static uint64_t P19[16];

static void decode(uint64_t c, int *w) {
  for (int i = K - 1; i >= 0; i--) { w[i] = (int)(c % 19); c /= 19; }
}
static uint64_t encode(const int *w) {
  uint64_t c = 0;
  for (int i = 0; i < K; i++) c = c * 19 + (uint64_t)w[i];
  return c;
}
static void forward(const int *s, int e, int *out) {
  int lo[16], hi[16];
  int x = 0;
  for (int i = 0; i < K; i++) { lo[i] = (s[i] + x) % 10; x = (s[i] + x) / 10; }
  int c = e;
  for (int i = K - 1; i >= 0; i--) { hi[i] = (s[i] + c) % 10; c = (s[i] + c) / 10; }
  if (c == 0) {
    for (int i = 0; i < K; i++) out[i] = lo[i] + hi[i];
  } else {
    out[0] = lo[0] + 1;
    for (int i = 1; i < K; i++) out[i] = lo[i] + hi[i - 1];
  }
}
static inline void succ2(uint64_t c, uint64_t *o0, uint64_t *o1) {
  int s[16], o[16];
  decode(c, s);
  forward(s, 0, o); *o0 = encode(o);
  forward(s, 1, o); *o1 = encode(o);
}

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: peel K F.bits OUT\n"); return 1; }
  K = atoi(argv[1]);
  P19[0] = 1;
  for (int i = 1; i < 16; i++) P19[i] = P19[i - 1] * 19;
  NW = P19[K];
  NWORDS64 = (NW + 63) / 64;
  uint16_t *deg = calloc(NW, 2);
  uint8_t *round_ = malloc(NW);  // 0 = alive (in C) ; r>=1 peeled in round r
  uint64_t *cur = calloc(NWORDS64, 8), *nxt = calloc(NWORDS64, 8);
  if (!deg || !round_ || !cur || !nxt) { fprintf(stderr, "alloc\n"); return 1; }
  memset(round_, 0, NW);
  time_t t0 = time(NULL);
  uint64_t lo19 = P19[K - 1];  // codes < lo19 have s_0 = 0 (no out-edges)
  int maxdeg = 0;
  for (uint64_t c = lo19; c < NW; c++) {
    uint64_t a, b;
    succ2(c, &a, &b);
    deg[a]++;
    deg[b]++;
  }
  for (uint64_t c = 0; c < NW; c++) if (deg[c] > maxdeg) maxdeg = deg[c];
  // round 1: all nodes with in-degree 0
  uint64_t peeled = 0;
  for (uint64_t c = 0; c < NW; c++) if (deg[c] == 0) cur[c >> 6] |= 1ULL << (c & 63);
  int r = 0;
  for (;;) {
    r++;
    uint64_t n = 0;
    memset(nxt, 0, NWORDS64 * 8);
    for (uint64_t wi = 0; wi < NWORDS64; wi++) {
      uint64_t m = cur[wi];
      while (m) {
        int b = __builtin_ctzll(m);
        m &= m - 1;
        uint64_t c = (wi << 6) | (uint64_t)b;
        round_[c] = (uint8_t)(r > 254 ? 254 : r);
        n++;
        if (c >= lo19) {
          uint64_t o[2];
          succ2(c, &o[0], &o[1]);
          for (int j = 0; j < 2; j++)
            if (--deg[o[j]] == 0) nxt[o[j] >> 6] |= 1ULL << (o[j] & 63);
        }
      }
    }
    peeled += n;
    if (!n) break;
    uint64_t *t = cur; cur = nxt; nxt = t;
  }
  uint64_t core = NW - peeled;
  // forward set
  FILE *f = fopen(argv[2], "rb");
  uint64_t *F = malloc(NWORDS64 * 8);
  if (!f || fread(F, 8, NWORDS64, f) != NWORDS64) { fprintf(stderr, "read F\n"); return 1; }
  fclose(f);
  uint64_t fsz = 0, fnotc = 0;
  for (uint64_t wi = 0; wi < NWORDS64; wi++) {
    uint64_t m = F[wi];
    while (m) {
      int b = __builtin_ctzll(m);
      m &= m - 1;
      uint64_t c = (wi << 6) | (uint64_t)b;
      fsz++;
      if (round_[c] != 0) fnotc++;
    }
  }
  // per-prefix classification
  int PL = K >= 4 ? 4 : 3;
  int NP = PL == 4 ? 9000 : 900, base = PL == 4 ? 1000 : 100;
  char *hitF = calloc(NP, 1), *hitC = calloc(NP, 1);
  int *md = calloc(NP, sizeof(int));
  uint64_t ndig = 9;
  for (int i = 1; i < K; i++) ndig *= 10;
  for (uint64_t d = 0; d < ndig; d++) {
    int w[16];
    uint64_t x = d;
    for (int i = K - 1; i >= 1; i--) { w[i] = (int)(x % 10); x /= 10; }
    w[0] = (int)x + 1;
    uint64_t c = encode(w);
    int p = 0;
    for (int i = 0; i < PL; i++) p = p * 10 + w[i];
    p -= base;
    if ((F[c >> 6] >> (c & 63)) & 1) hitF[p] = 1;
    if (round_[c] == 0) hitC[p] = 1;
    else if (round_[c] > md[p]) md[p] = round_[c];
  }
  char fn[4096];
  snprintf(fn, sizeof fn, "%s.tsv", argv[3]);
  FILE *o = fopen(fn, "w");
  int nF = 0, nC = 0, nFnotC = 0, nCnotF = 0, mdmax = 0;
  for (int p = 0; p < NP; p++) {
    fprintf(o, "%d\t%d\t%d\t%d\n", p + base, hitF[p], hitC[p], hitC[p] ? -1 : md[p]);
    nF += hitF[p];
    nC += hitC[p];
    nFnotC += hitF[p] && !hitC[p];
    nCnotF += hitC[p] && !hitF[p];
    if (!hitC[p] && md[p] > mdmax) mdmax = md[p];
  }
  fclose(o);
  printf("K=%d nodes=%llu maxindeg=%d rounds=%d core|C|=%llu |F|=%llu F_not_in_C=%llu "
         "prefixes(len %d): hitF=%d hitC=%d hitF&!hitC=%d hitC&!hitF=%d maxLongDepthUncycled=%d seconds=%ld\n",
         K, (unsigned long long)NW, maxdeg, r - 1, (unsigned long long)core, (unsigned long long)fsz,
         (unsigned long long)fnotc, PL, nF, nC, nFnotC, nCnotF, mdmax, (long)(time(NULL) - t0));
  return 0;
}
