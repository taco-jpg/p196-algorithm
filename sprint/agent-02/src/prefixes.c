/*
 * prefixes.c -- which n-digit palindrome prefixes are excluded by a forward-closed set F_k (n <= k).
 *
 * A prefix P = (p_0..p_{n-1}) (p_0 >= 1, digits 0..9) is "forward-excluded at width k" iff
 *   noOverflowPre(P)  (p_0 >= 2 or some p_i >= 3)   and
 *   no word P ++ tail, tail in {0..9}^(k-n), lies in F_k.
 * (Last predecessor of a non-overflow palindrome has all column sums <= 9 equal to the
 *  palindrome's digits: Agent124.PrefixL.canonical_last_step_initialL.)
 *
 * Usage: prefixes K BITSFILE N OUTFILE
 * OUTFILE gets one excluded prefix per line (digits concatenated); stdout gets counts.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int K;
static uint64_t *F;
static inline int getb(uint64_t i) { return (F[i >> 6] >> (i & 63)) & 1; }

int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage: %s K BITS N OUT\n", argv[0]); return 2; }
  K = atoi(argv[1]);
  int n = atoi(argv[3]);
  if (n < 1 || n > K) { fprintf(stderr, "need 1 <= N <= K\n"); return 2; }
  uint64_t S = 1;
  for (int i = 0; i < K; i++) S *= 19;
  uint64_t nw = (S + 63) / 64;
  F = malloc(nw * 8);
  FILE *f = fopen(argv[2], "rb");
  if (!f || fread(F, 8, nw, f) != nw) { fprintf(stderr, "read failed\n"); return 1; }
  fclose(f);
  FILE *out = fopen(argv[4], "w");
  uint64_t p10n = 1, p10t = 1;
  for (int i = 0; i < n; i++) p10n *= 10;
  for (int i = n; i < K; i++) p10t *= 10;
  uint64_t pw19t = 1;
  for (int i = n; i < K; i++) pw19t *= 19;
  long excl = 0, excl_lead[10] = {0}, total = 0, overflow_skip = 0;
  int d[32];
  for (uint64_t P = p10n / 10; P < p10n; P++) {
    uint64_t x = P;
    for (int i = n - 1; i >= 0; i--) { d[i] = (int)(x % 10); x /= 10; }
    total++;
    int nov = d[0] >= 2;
    for (int i = 0; i < n; i++) if (d[i] >= 3) nov = 1;
    /* base index of prefix in base 19 */
    uint64_t base = 0;
    for (int i = 0; i < n; i++) base = base * 19 + (uint64_t)d[i];
    base *= pw19t;
    int found = 0;
    for (uint64_t t = 0; t < p10t && !found; t++) {
      uint64_t y = t, off = 0, m = 1;
      for (int i = K - 1; i >= n; i--) { off += (y % 10) * m; y /= 10; m *= 19; }
      if (getb(base + off)) found = 1;
    }
    if (!found) {
      if (!nov) { overflow_skip++; continue; }
      excl++;
      excl_lead[d[0]]++;
      for (int i = 0; i < n; i++) fputc('0' + d[i], out);
      fputc('\n', out);
    }
  }
  fclose(out);
  printf("{\"k\": %d, \"n\": %d, \"prefixes\": %ld, \"excluded\": %ld, \"absent_but_overflow_possible\": %ld, \"by_lead\": [",
         K, n, total, excl, overflow_skip);
  for (int a = 0; a < 10; a++) printf("%s%ld", a ? ", " : "", excl_lead[a]);
  printf("]}\n");
  return 0;
}
