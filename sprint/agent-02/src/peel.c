/*
 * peel.c -- recurrent part R_k of the k-column abstraction, and its comparison with a forward closure F.
 *
 * Graph: all words with entries < 19 and q_0 >= 1 (positive outer source sum, as in
 * SevenColumn.prefixPredecessors), edges w -> forwardPrefix(w, e), e in {0,1} (duplicate edge
 * counted once). q_0 >= 1 is preserved by forwardPrefix. Words with q_0 = 0 get rank 0 and are
 * excluded from the graph.
 * Peeling: repeatedly delete words of in-degree 0. The words that survive are exactly the words with
 * an infinite backward path, i.e. the words reachable from some cycle ("recurrent part" R_k).
 * The deletion round of a word is the length of its longest backward path ("rank"); a prefix whose
 * initial words all have finite rank is what the backward (Agent124 ancestry) method certifies.
 *
 * Usage: peel K FBITS OUTPREFIX
 *   writes OUTPREFIX.R.bits (bitset of R_k) and OUTPREFIX.rank (uint8 rank per word, 255 = in R_k)
 *   prints |R|, |F|, |F & R|, |F \ R|, |R \ F|, and the same restricted to all-digit words.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int K;
static uint64_t N;
static inline int getb(const uint64_t *b, uint64_t i) { return (b[i >> 6] >> (i & 63)) & 1; }
static inline void setb(uint64_t *b, uint64_t i) { b[i >> 6] |= (uint64_t)1 << (i & 63); }
static void decode(uint64_t idx, int *w) { for (int i = K - 1; i >= 0; i--) { w[i] = (int)(idx % 19); idx /= 19; } }
static uint64_t encode(const int *w) { uint64_t x = 0; for (int i = 0; i < K; i++) x = x * 19 + (uint64_t)w[i]; return x; }
static void fwd(const int *s, int e, int *out) {
  int lo[32], hi[32], c = 0;
  for (int i = 0; i < K; i++) { int v = s[i] + c; lo[i] = v % 10; c = v / 10; }
  c = e;
  for (int i = K - 1; i >= 0; i--) { int v = s[i] + c; hi[i] = v % 10; c = v / 10; }
  if (c == 0) for (int i = 0; i < K; i++) out[i] = lo[i] + hi[i];
  else { out[0] = lo[0] + 1; for (int i = 1; i < K; i++) out[i] = lo[i] + hi[i - 1]; }
}
static void succ(uint64_t idx, uint64_t *a, uint64_t *b) {
  int s[32], o[32];
  decode(idx, s);
  fwd(s, 0, o); *a = encode(o);
  fwd(s, 1, o); *b = encode(o);
}

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: %s K FBITS OUT\n", argv[0]); return 2; }
  K = atoi(argv[1]);
  N = 1; for (int i = 0; i < K; i++) N *= 19;
  uint64_t nw = (N + 63) / 64;
  uint16_t *indeg = calloc(N, 2);
  uint8_t *rank = malloc(N);
  if (!indeg || !rank) { fprintf(stderr, "alloc\n"); return 1; }
  memset(rank, 255, N);
  uint32_t maxin = 0;
  uint64_t top = N / 19; /* words with q_0 = 0 are indices < 19^(k-1) */
  for (uint64_t i = top; i < N; i++) {
    uint64_t a, b; succ(i, &a, &b);
    if (indeg[a] < 65535) indeg[a]++;
    if (b != a && indeg[b] < 65535) indeg[b]++;
  }
  for (uint64_t i = 0; i < N; i++) if (indeg[i] > maxin) maxin = indeg[i];
  /* peel in rounds */
  uint64_t *cur = calloc(nw, 8), *nxt = calloc(nw, 8);
  uint64_t removed = 0;
  for (uint64_t i = 0; i < top; i++) rank[i] = 0;
  for (uint64_t i = top; i < N; i++) if (indeg[i] == 0) setb(cur, i);
  int round = 0;
  for (;;) {
    uint64_t cnt = 0;
    memset(nxt, 0, nw * 8);
    for (uint64_t wi = 0; wi < nw; wi++) {
      uint64_t x = cur[wi];
      while (x) {
        int bb = __builtin_ctzll(x); x &= x - 1;
        uint64_t i = wi * 64 + (uint64_t)bb;
        rank[i] = (uint8_t)(round < 254 ? round : 254);
        cnt++;
        uint64_t a, b; succ(i, &a, &b);
        if (--indeg[a] == 0) setb(nxt, a);
        if (b != a && --indeg[b] == 0) setb(nxt, b);
      }
    }
    if (!cnt) break;
    removed += cnt;
    round++;
    uint64_t *t = cur; cur = nxt; nxt = t;
  }
  uint64_t *R = calloc(nw, 8);
  for (uint64_t i = 0; i < N; i++) if (rank[i] == 255) setb(R, i);
  uint64_t *F = malloc(nw * 8);
  FILE *f = fopen(argv[2], "rb");
  if (!f || fread(F, 8, nw, f) != nw) { fprintf(stderr, "read F\n"); return 1; }
  fclose(f);
  uint64_t nR = 0, nF = 0, nFR = 0, nFnR = 0, nRnF = 0, dR = 0, dF = 0, dFnR = 0, dRnF = 0;
  int w[32];
  for (uint64_t i = 0; i < N; i++) {
    int r = getb(R, i), fl = getb(F, i);
    nR += r; nF += fl; nFR += r && fl; nFnR += fl && !r; nRnF += r && !fl;
    if (r || fl) {
      decode(i, w);
      int dig = 1; for (int j = 0; j < K; j++) if (w[j] > 9) { dig = 0; break; }
      if (dig) { dR += r; dF += fl; dFnR += fl && !r; dRnF += r && !fl; }
    }
  }
  char path[4096];
  snprintf(path, sizeof path, "%s.R.bits", argv[3]);
  f = fopen(path, "wb"); fwrite(R, 8, nw, f); fclose(f);
  snprintf(path, sizeof path, "%s.rank", argv[3]);
  f = fopen(path, "wb"); fwrite(rank, 1, N, f); fclose(f);
  printf("{\"k\": %d, \"space\": %llu, \"max_indegree\": %u, \"peel_rounds\": %d, \"R\": %llu, \"F\": %llu, "
         "\"F_and_R\": %llu, \"F_minus_R\": %llu, \"R_minus_F\": %llu, \"digit_R\": %llu, \"digit_F\": %llu, "
         "\"digit_F_minus_R\": %llu, \"digit_R_minus_F\": %llu}\n",
         K, (unsigned long long)N, maxin, round, (unsigned long long)nR, (unsigned long long)nF,
         (unsigned long long)nFR, (unsigned long long)nFnR, (unsigned long long)nRnF, (unsigned long long)dR,
         (unsigned long long)dF, (unsigned long long)dFnR, (unsigned long long)dRnF);
  return 0;
}
