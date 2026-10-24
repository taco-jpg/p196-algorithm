/*
 * scc.c -- strongly connected components of the positive k-column abstraction restricted to a set R
 * (normally the recurrent part R_k = forward closure of 196 at time 100).
 *
 * Usage: scc K RBITS
 * Prints: number of SCCs inside R, size of the largest, number of trivial (single node, no self loop)
 * components, and whether R is one SCC.
 * Iterative Kosaraju over explicit edge arrays (both successors of every node of R stay in R
 * because R is forward closed; this is asserted).
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int K;
static uint64_t N;
static uint64_t *Rb;
static inline int getb(const uint64_t *b, uint64_t i) { return (b[i >> 6] >> (i & 63)) & 1; }
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

/* dense renumbering of R */
static uint64_t *ids;   /* dense id -> word index */
static uint32_t nR;
static uint32_t dense(uint64_t w) { /* binary search */
  uint64_t lo = 0, hi = nR;
  while (lo < hi) { uint64_t m = (lo + hi) / 2; if (ids[m] < w) lo = m + 1; else hi = m; }
  if (lo >= nR || ids[lo] != w) { fprintf(stderr, "successor outside R: not closed\n"); exit(3); }
  return (uint32_t)lo;
}

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: %s K RBITS\n", argv[0]); return 2; }
  K = atoi(argv[1]);
  N = 1; for (int i = 0; i < K; i++) N *= 19;
  uint64_t nw = (N + 63) / 64;
  Rb = malloc(nw * 8);
  FILE *f = fopen(argv[2], "rb");
  if (!f || fread(Rb, 8, nw, f) != nw) { fprintf(stderr, "read\n"); return 1; }
  fclose(f);
  nR = 0;
  for (uint64_t i = 0; i < N; i++) if (getb(Rb, i)) nR++;
  ids = malloc((uint64_t)nR * 8);
  uint32_t j = 0;
  for (uint64_t i = 0; i < N; i++) if (getb(Rb, i)) ids[j++] = i;
  uint32_t *succ = malloc((uint64_t)nR * 2 * 4);
  int s[32], o[32];
  for (uint32_t v = 0; v < nR; v++) {
    decode(ids[v], s);
    fwd(s, 0, o); succ[2 * v] = dense(encode(o));
    fwd(s, 1, o); succ[2 * v + 1] = dense(encode(o));
  }
  /* reverse graph in CSR */
  uint32_t *rdeg = calloc((uint64_t)nR + 1, 4);
  for (uint64_t e = 0; e < (uint64_t)2 * nR; e++) rdeg[succ[e] + 1]++;
  for (uint32_t v = 0; v < nR; v++) rdeg[v + 1] += rdeg[v];
  uint32_t *radj = malloc((uint64_t)2 * nR * 4), *fill = calloc(nR, 4);
  for (uint32_t v = 0; v < nR; v++) for (int e = 0; e < 2; e++) {
    uint32_t t = succ[2 * v + e];
    radj[rdeg[t] + fill[t]++] = v;
  }
  /* pass 1: iterative DFS finishing order on forward graph */
  uint8_t *seen = calloc(nR, 1);
  uint32_t *order = malloc((uint64_t)nR * 4), no = 0;
  uint32_t *stk = malloc((uint64_t)nR * 4 * 2 + 16);
  uint8_t *it = calloc(nR, 1);
  for (uint32_t r = 0; r < nR; r++) {
    if (seen[r]) continue;
    uint64_t sp = 0; stk[sp++] = r; seen[r] = 1;
    while (sp) {
      uint32_t v = stk[sp - 1];
      if (it[v] < 2) {
        uint32_t t = succ[2 * v + it[v]]; it[v]++;
        if (!seen[t]) { seen[t] = 1; stk[sp++] = t; }
      } else { order[no++] = v; sp--; }
    }
  }
  /* pass 2: reverse graph in decreasing finish order */
  uint32_t *comp = malloc((uint64_t)nR * 4);
  memset(comp, 0xff, (uint64_t)nR * 4);
  uint32_t ncomp = 0, largest = 0, trivial = 0;
  for (int64_t x = (int64_t)nR - 1; x >= 0; x--) {
    uint32_t r = order[x];
    if (comp[r] != 0xffffffffu) continue;
    uint64_t sp = 0, size = 0; stk[sp++] = r; comp[r] = ncomp;
    while (sp) {
      uint32_t v = stk[--sp]; size++;
      for (uint32_t a = rdeg[v]; a < rdeg[v + 1]; a++) {
        uint32_t u = radj[a];
        if (comp[u] == 0xffffffffu) { comp[u] = ncomp; stk[sp++] = u; }
      }
    }
    if (size > largest) largest = (uint32_t)size;
    if (size == 1 && succ[2 * r] != r && succ[2 * r + 1] != r) trivial++;
    ncomp++;
  }
  printf("{\"k\": %d, \"R\": %u, \"sccs\": %u, \"largest_scc\": %u, \"trivial_sccs\": %u, \"strongly_connected\": %s}\n",
         K, nR, ncomp, largest, trivial, ncomp == 1 ? "true" : "false");
  return 0;
}
