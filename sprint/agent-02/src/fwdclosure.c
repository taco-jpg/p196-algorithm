/*
 * fwdclosure.c -- forward closure of the k-column prefix abstraction (sprint agent 02).
 *
 * Mirror of SevenColumnProjection.forwardPrefix (lean/P196/Agent104P620Witness/ActualPrefix.lean):
 *   state  = first k column sums (q_0 .. q_{k-1}), q_i in 0..18, q_0 = outermost column
 *   step   = forwardPrefix(s, e) for the unknown inner carry e in {0,1}
 *
 * Usage:
 *   fwdclosure K OUT_PREFIX w0_0,w0_1,...[,...]      (only the first K entries of w0 are used)
 *
 * Output:
 *   OUT_PREFIX.bits   raw bitset, bit idx set iff word idx is in F; idx = sum_i q_i * 19^(K-1-i)
 *   stdout            |F|, digit words in F, timing
 *
 * Untrusted: every set used in Lean is re-checked by kernel reduction.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static int K;
static uint64_t N; /* 19^K */
static uint64_t *vis, *done;

static inline int getb(const uint64_t *b, uint64_t i) { return (b[i >> 6] >> (i & 63)) & 1; }
static inline void setb(uint64_t *b, uint64_t i) { b[i >> 6] |= (uint64_t)1 << (i & 63); }

static void decode(uint64_t idx, int *w) {
  for (int i = K - 1; i >= 0; i--) { w[i] = (int)(idx % 19); idx /= 19; }
}
static uint64_t encode(const int *w) {
  uint64_t x = 0;
  for (int i = 0; i < K; i++) x = x * 19 + (uint64_t)w[i];
  return x;
}

/* forwardPrefix(s, e) */
static void fwd(const int *s, int e, int *out) {
  int lo[32], hi[32];
  int c = 0;
  for (int i = 0; i < K; i++) { int v = s[i] + c; lo[i] = v % 10; c = v / 10; }
  c = e;
  for (int i = K - 1; i >= 0; i--) { int v = s[i] + c; hi[i] = v % 10; c = v / 10; }
  if (c == 0) {
    for (int i = 0; i < K; i++) out[i] = lo[i] + hi[i];
  } else {
    out[0] = lo[0] + 1;
    for (int i = 1; i < K; i++) out[i] = lo[i] + hi[i - 1];
  }
}

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: %s K OUT w0csv\n", argv[0]); return 2; }
  K = atoi(argv[1]);
  if (K < 1 || K > 15) { fprintf(stderr, "K out of range\n"); return 2; }
  N = 1;
  for (int i = 0; i < K; i++) N *= 19;
  int w0[64], n0 = 0;
  char *tok = strtok(argv[3], ",");
  while (tok && n0 < 64) { w0[n0++] = atoi(tok); tok = strtok(NULL, ","); }
  if (n0 < K) { fprintf(stderr, "w0 too short\n"); return 2; }
  uint64_t nwords = (N + 63) / 64;
  vis = calloc(nwords, 8);
  done = calloc(nwords, 8);
  if (!vis || !done) { fprintf(stderr, "alloc failed\n"); return 1; }
  clock_t t0 = clock();
  setb(vis, encode(w0));
  int s[32], o[32];
  int changed = 1, passes = 0;
  uint64_t count = 1;
  while (changed) {
    changed = 0;
    passes++;
    for (uint64_t wi = 0; wi < nwords; wi++) {
      uint64_t todo;
      while ((todo = vis[wi] & ~done[wi]) != 0) {
        int b = __builtin_ctzll(todo);
        uint64_t idx = wi * 64 + (uint64_t)b;
        done[wi] |= (uint64_t)1 << b;
        decode(idx, s);
        for (int e = 0; e <= 1; e++) {
          fwd(s, e, o);
          uint64_t j = encode(o);
          if (!getb(vis, j)) {
            setb(vis, j);
            count++;
            if ((j >> 6) < wi) changed = 1; /* behind the scan: need another pass */
          }
        }
      }
    }
  }
  double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
  /* digit words: every entry <= 9 */
  uint64_t digit = 0, digit_lead[10] = {0};
  int w[32];
  for (uint64_t wi = 0; wi < nwords; wi++) {
    uint64_t x = vis[wi];
    while (x) {
      int b = __builtin_ctzll(x);
      x &= x - 1;
      decode(wi * 64 + (uint64_t)b, w);
      int ok = 1;
      for (int i = 0; i < K; i++) if (w[i] > 9) { ok = 0; break; }
      if (ok) { digit++; digit_lead[w[0]]++; }
    }
  }
  char path[4096];
  snprintf(path, sizeof path, "%s.bits", argv[2]);
  FILE *f = fopen(path, "wb");
  if (!f) { perror("fopen"); return 1; }
  fwrite(vis, 8, nwords, f);
  fclose(f);
  printf("{\"k\": %d, \"w0\": [", K);
  for (int i = 0; i < K; i++) printf("%s%d", i ? ", " : "", w0[i]);
  printf("], \"F\": %llu, \"space\": %llu, \"digit_words_in_F\": %llu, \"digit_by_lead\": [",
         (unsigned long long)count, (unsigned long long)N, (unsigned long long)digit);
  for (int a = 0; a < 10; a++) printf("%s%llu", a ? ", " : "", (unsigned long long)digit_lead[a]);
  printf("], \"passes\": %d, \"cpu_seconds\": %.2f}\n", passes, secs);
  return 0;
}
