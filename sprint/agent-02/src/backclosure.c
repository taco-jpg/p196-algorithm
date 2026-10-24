/*
 * backclosure.c -- size and depth of the backward closure B(P) of a digit prefix P at width k,
 * under the exact executable inverse SevenColumn.prefixPredecessors (mirrored from
 * lean/P196/Agent104P620Witness/PrefixInverse.lean), long words only.
 *
 * Initial words: P ++ tail, tail in {0..9}^(k-n) (full-width last-predecessor projections).
 * Prints |B(P)|, the longest backward path (rank of the deepest initial word) if B(P) is acyclic,
 * or "cycle" otherwise. Optional FBITS: assert that no word of B(P) lies in the forward closure
 * F_k (which would contradict acyclicity).
 *
 * Usage: backclosure K PREFIX [FBITS] [--cap N]
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int K;
static uint64_t enc(const int *w) { uint64_t x = 0; for (int i = 0; i < K; i++) x = x * 19 + (uint64_t)w[i]; return x; }
static void dec(uint64_t idx, int *w) { for (int i = K - 1; i >= 0; i--) { w[i] = (int)(idx % 19); idx /= 19; } }

/* ---- predecessor enumeration, exact mirror of the Lean definitions ---- */
static uint64_t *pbuf; static int pn, pcap;
static int cur[40];
static void emit(void) { if (pn == pcap) { pcap *= 2; pbuf = realloc(pbuf, (size_t)pcap * 8); } pbuf[pn++] = enc(cur); }
/* noOverflowPred p[i..] x y, writing source entries at cur[i..] */
static const int *P;
static void noov(int i, int x, int y) {
  if (i == K) { emit(); return; }
  int v = P[i];
  for (int a = 0; a < 19; a++) for (int z = 0; z < 2; z++) {
    if ((a + z) / 10 == y && v == (a + x) % 10 + (a + z) % 10) { cur[i] = a; noov(i + 1, (a + x) / 10, z); }
  }
}
/* overflowTailPred p[i..] prev x y; cur[i-1] = prev already set */
static void ovtail(int i, int prev, int x, int y) {
  if (i == K) { for (int z = 0; z < 2; z++) if ((prev + z) / 10 == y) { emit(); return; } return; }
  int v = P[i];
  for (int a = 0; a < 19; a++) for (int z = 0; z < 2; z++) {
    if ((prev + z) / 10 == y && v == (a + x) % 10 + (prev + z) % 10) { cur[i] = a; ovtail(i + 1, a, (a + x) / 10, z); }
  }
}
static void preds(const int *p) {
  pn = 0; P = p;
  /* no-overflow branch, x = 0, y = 0, keep head > 0 */
  int start = pn; noov(0, 0, 0);
  int w = start;
  for (int j = start; j < pn; j++) { int t[40]; dec(pbuf[j], t); if (t[0] > 0) pbuf[w++] = pbuf[j]; }
  pn = w;
  /* overflow branch */
  int v = p[0];
  if (v > 0 && v <= 10) {
    int a = v <= 9 ? v + 9 : 9;
    cur[0] = a;
    ovtail(1, a, (a + 0) / 10, 1);
  }
}

/* ---- forward map (for the self-test) ---- */
static void fwd(const int *s, int e, int *out) {
  int lo[40], hi[40], c = 0;
  for (int i = 0; i < K; i++) { int vv = s[i] + c; lo[i] = vv % 10; c = vv / 10; }
  c = e;
  for (int i = K - 1; i >= 0; i--) { int vv = s[i] + c; hi[i] = vv % 10; c = vv / 10; }
  if (c == 0) for (int i = 0; i < K; i++) out[i] = lo[i] + hi[i];
  else { out[0] = lo[0] + 1; for (int i = 1; i < K; i++) out[i] = lo[i] + hi[i - 1]; }
}

/* ---- hash map word -> node id ---- */
static uint64_t *hk; static uint32_t *hv; static uint64_t hcap;
static uint64_t *nodes; static uint32_t nn, ncap;
static uint32_t intern(uint64_t key, int *isnew) {
  uint64_t h = (key * 0x9E3779B97F4A7C15ull) & (hcap - 1);
  while (hk[h] != UINT64_MAX) { if (hk[h] == key) { *isnew = 0; return hv[h]; } h = (h + 1) & (hcap - 1); }
  if (nn == ncap) { ncap *= 2; nodes = realloc(nodes, (size_t)ncap * 8); }
  hk[h] = key; hv[h] = nn; nodes[nn] = key; *isnew = 1;
  return nn++;
}

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: %s K PREFIX [FBITS] [--cap N]\n", argv[0]); return 2; }
  K = atoi(argv[1]);
  const char *pre = argv[2];
  int n = (int)strlen(pre);
  const char *fbits = NULL; uint64_t cap = 50000000;
  for (int i = 3; i < argc; i++) {
    if (!strcmp(argv[i], "--cap") && i + 1 < argc) cap = strtoull(argv[++i], NULL, 10);
    else fbits = argv[i];
  }
  pcap = 1024; pbuf = malloc((size_t)pcap * 8);
  /* self-test of the inverse against the forward map on pseudo-random words */
  uint64_t seed = 12345;
  for (int t = 0; t < 20000; t++) {
    int s[40], o[40], e;
    for (int i = 0; i < K; i++) { seed = seed * 6364136223846793005ull + 1442695040888963407ull; s[i] = (int)((seed >> 33) % 19); }
    if (s[0] == 0) s[0] = 1;
    e = t & 1;
    fwd(s, e, o);
    preds(o);
    int found = 0; uint64_t key = enc(s);
    for (int j = 0; j < pn; j++) if (pbuf[j] == key) found = 1;
    if (!found) { fprintf(stderr, "self-test: forward edge missing from inverse\n"); return 4; }
    for (int j = 0; j < pn; j++) {
      int q[40], r0[40], r1[40]; dec(pbuf[j], q); fwd(q, 0, r0); fwd(q, 1, r1);
      if (enc(r0) != enc(o) && enc(r1) != enc(o)) { fprintf(stderr, "self-test: inverse edge not a forward edge\n"); return 4; }
    }
  }
  hcap = 1; while (hcap < 4 * cap) hcap <<= 1;
  hk = malloc(hcap * 8); hv = malloc(hcap * 4);
  memset(hk, 0xff, hcap * 8);
  ncap = 1 << 20; nodes = malloc((size_t)ncap * 8); nn = 0;
  /* initial words */
  int tails = 1; for (int i = n; i < K; i++) tails *= 10;
  int w[40];
  for (int i = 0; i < n; i++) w[i] = pre[i] - '0';
  uint32_t ninit = 0;
  for (int t = 0; t < tails; t++) {
    int x = t;
    for (int i = K - 1; i >= n; i--) { w[i] = x % 10; x /= 10; }
    int isnew; intern(enc(w), &isnew); ninit++;
  }
  /* BFS over predecessors, store edges child -> parent list implicitly by recomputation later */
  for (uint32_t i = 0; i < nn; i++) {
    if (nn > cap) { printf("{\"k\": %d, \"prefix\": \"%s\", \"status\": \"cap\", \"nodes\": %u}\n", K, pre, nn); return 0; }
    int p[40]; dec(nodes[i], p); preds(p);
    for (int j = 0; j < pn; j++) { int isnew; intern(pbuf[j], &isnew); }
  }
  /* longest backward path by iterative DFS with colors: rank(v) = 1 + max rank(pred), 0 if none */
  uint32_t *rank = malloc((size_t)nn * 4);
  uint8_t *col = calloc(nn, 1);
  uint32_t *stk = malloc((size_t)nn * 4 + 4), *ptr = malloc((size_t)nn * 4 + 4);
  int cyc = 0; uint32_t maxr = 0, maxinit = 0;
  for (uint32_t r = 0; r < nn && !cyc; r++) {
    if (col[r]) continue;
    uint32_t sp = 0; stk[sp] = r; ptr[sp] = 0; sp++; col[r] = 1; rank[r] = 0;
    while (sp && !cyc) {
      uint32_t v = stk[sp - 1];
      int p[40]; dec(nodes[v], p); preds(p);
      if (ptr[sp - 1] < (uint32_t)pn) {
        uint64_t key = pbuf[ptr[sp - 1]++];
        int isnew; uint32_t u = intern(key, &isnew);
        if (col[u] == 1) { cyc = 1; break; }
        if (col[u] == 0) { col[u] = 1; rank[u] = 0; stk[sp] = u; ptr[sp] = 0; sp++; }
        else if (rank[u] + 1 > rank[v]) rank[v] = rank[u] + 1;
      } else {
        col[v] = 2; sp--;
        if (sp) { uint32_t par = stk[sp - 1]; if (rank[v] + 1 > rank[par]) rank[par] = rank[v] + 1; }
        if (rank[v] > maxr) maxr = rank[v];
      }
    }
  }
  if (!cyc) for (uint32_t i = 0; i < ninit; i++) if (rank[i] > maxinit) maxinit = rank[i];
  long inF = -1;
  if (fbits && !cyc) {
    uint64_t N = 1; for (int i = 0; i < K; i++) N *= 19;
    uint64_t nw = (N + 63) / 64; uint64_t *F = malloc(nw * 8);
    FILE *f = fopen(fbits, "rb");
    if (f && fread(F, 8, nw, f) == nw) {
      inF = 0;
      for (uint32_t i = 0; i < nn; i++) if ((F[nodes[i] >> 6] >> (nodes[i] & 63)) & 1) inF++;
    }
    if (f) fclose(f);
  }
  printf("{\"k\": %d, \"prefix\": \"%s\", \"status\": \"%s\", \"nodes\": %u, \"initial_words\": %u, "
         "\"max_initial_rank\": %u, \"max_rank\": %u, \"nodes_in_F\": %ld}\n",
         K, pre, cyc ? "cycle" : "acyclic", nn, ninit, cyc ? 0 : maxinit, cyc ? 0 : maxr, inF);
  return 0;
}
