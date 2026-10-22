// Strong-connectivity check of a forward-closed set F (bitset from fwdclosure).
// Computes R = { x in F : x reaches w (some given word) }, by Gauss-Seidel
// sweeps, and reports |R| vs |F|.  If |R| == |F| and F is the forward closure
// of w, then F is a single strongly connected component.
// Also reports, for extra words given after w, whether each lies in F and in R.
// Usage: sccchk K F.bits w0,..,wK-1 [x0,..,xK-1 ...]
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int K;
static uint64_t NW, NWORDS64, P19[16];
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
  if (c == 0) for (int i = 0; i < K; i++) out[i] = lo[i] + hi[i];
  else { out[0] = lo[0] + 1; for (int i = 1; i < K; i++) out[i] = lo[i] + hi[i - 1]; }
}
static uint64_t parse(const char *p) {
  int w[16], n = 0;
  char *q = (char *)p;
  while (*q && n < 16) { w[n++] = (int)strtol(q, &q, 10); if (*q == ',') q++; }
  if (n != K) { fprintf(stderr, "bad word %s\n", p); exit(1); }
  return encode(w);
}
#define GET(b, c) (((b)[(c) >> 6] >> ((c) & 63)) & 1)
int main(int argc, char **argv) {
  K = atoi(argv[1]);
  P19[0] = 1;
  for (int i = 1; i < 16; i++) P19[i] = P19[i - 1] * 19;
  NW = P19[K];
  NWORDS64 = (NW + 63) / 64;
  uint64_t *F = malloc(NWORDS64 * 8), *R = calloc(NWORDS64, 8);
  FILE *f = fopen(argv[2], "rb");
  if (fread(F, 8, NWORDS64, f) != NWORDS64) return 1;
  fclose(f);
  uint64_t w = parse(argv[3]);
  R[w >> 6] |= 1ULL << (w & 63);
  int sweeps = 0;
  for (;;) {
    uint64_t added = 0;
    for (uint64_t wi = 0; wi < NWORDS64; wi++) {
      uint64_t m = F[wi] & ~R[wi];
      while (m) {
        int b = __builtin_ctzll(m);
        m &= m - 1;
        uint64_t c = (wi << 6) | (uint64_t)b;
        int s[16], o[16];
        decode(c, s);
        for (int e = 0; e < 2; e++) {
          forward(s, e, o);
          uint64_t oc = encode(o);
          if (GET(R, oc)) { R[wi] |= 1ULL << b; added++; break; }
        }
      }
    }
    sweeps++;
    if (!added) break;
  }
  uint64_t nf = 0, nr = 0;
  for (uint64_t wi = 0; wi < NWORDS64; wi++) {
    nf += (uint64_t)__builtin_popcountll(F[wi]);
    nr += (uint64_t)__builtin_popcountll(R[wi]);
  }
  printf("K=%d |F|=%llu |reach-to-w within F|=%llu sweeps=%d single_SCC=%s\n", K,
         (unsigned long long)nf, (unsigned long long)nr, sweeps, nf == nr ? "yes" : "no");
  for (int a = 4; a < argc; a++) {
    uint64_t x = parse(argv[a]);
    printf("  word %s inF=%d inR=%d\n", argv[a], (int)GET(F, x), (int)GET(R, x));
  }
  return 0;
}
