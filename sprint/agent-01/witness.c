// Shortest forward walks in the width-K abstraction from a start word (196's
// projection at t = 100) to a "digit word" (all entries <= 9, s_0 >= 1) with
// each reachable 4-digit prefix.  Works inside U_K = pi^{-1}(X) as in layer.c.
//
// Usage: witness K Xprev.bits start_word OUT.tsv
// Output lines: prefix <TAB> length <TAB> target word <TAB> carry bits e_1..e_n
//   meaning forwardPrefix(...forwardPrefix(start, e_1)..., e_n) = target.
// Every printed walk is re-executed forward before printing (self-check).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int K;
static uint64_t P19[16];
static uint64_t *X, nXw, *cnt, nblk, nX, NU, NUw;
static inline int xget(uint64_t p) { return (X[p >> 6] >> (p & 63)) & 1; }
static inline uint64_t rank_(uint64_t p) {
  uint64_t b = p >> 9, r = cnt[b];
  for (uint64_t w = b << 3; w < (p >> 6); w++) r += (uint64_t)__builtin_popcountll(X[w]);
  return r + (uint64_t)__builtin_popcountll(X[p >> 6] & ((1ULL << (p & 63)) - 1));
}
static uint64_t cur_blk;
static uint64_t select_(uint64_t r) {
  if (cur_blk >= nblk || cnt[cur_blk] > r) cur_blk = 0;
  while (cur_blk + 1 < nblk && cnt[cur_blk + 1] <= r) cur_blk++;
  uint64_t rr = cnt[cur_blk];
  for (uint64_t w = cur_blk << 3; w < nXw; w++) {
    uint64_t m = X[w];
    int pc = __builtin_popcountll(m);
    if (rr + (uint64_t)pc > r) {
      uint64_t need = r - rr;
      while (need--) m &= m - 1;
      return (w << 6) | (uint64_t)__builtin_ctzll(m);
    }
    rr += (uint64_t)pc;
  }
  exit(2);
}
static void decode(uint64_t c, int *w) { for (int i = K - 1; i >= 0; i--) { w[i] = (int)(c % 19); c /= 19; } }
static uint64_t encode(const int *w) { uint64_t c = 0; for (int i = 0; i < K; i++) c = c * 19 + (uint64_t)w[i]; return c; }
static void forward(const int *s, int e, int *out) {
  int lo[16], hi[16];
  int x = 0;
  for (int i = 0; i < K; i++) { lo[i] = (s[i] + x) % 10; x = (s[i] + x) / 10; }
  int c = e;
  for (int i = K - 1; i >= 0; i--) { hi[i] = (s[i] + c) % 10; c = (s[i] + c) / 10; }
  if (c == 0) for (int i = 0; i < K; i++) out[i] = lo[i] + hi[i];
  else { out[0] = lo[0] + 1; for (int i = 1; i < K; i++) out[i] = lo[i] + hi[i - 1]; }
}
static inline int c2u(uint64_t c, uint64_t *u) {
  uint64_t p = c / 19;
  if (!xget(p)) return 0;
  *u = rank_(p) * 19 + c % 19;
  return 1;
}
static inline uint64_t u2c(uint64_t u) { return select_(u / 19) * 19 + u % 19; }
#define GET(b, u) (((b)[(u) >> 6] >> ((u) & 63)) & 1)
#define SET(b, u) ((b)[(u) >> 6] |= 1ULL << ((u) & 63))

// predecessors (literal translation of PrefixInverse.lean), collected into out[]
static int npred;
static int predbuf[4096][16];
static int cur[16];
static void noov(const int *p, int i, int x, int y) {
  if (i == K) { if (cur[0] > 0 && npred < 4096) memcpy(predbuf[npred++], cur, sizeof cur); return; }
  for (int a = 0; a < 19; a++)
    for (int z = 0; z < 2; z++)
      if ((a + z) / 10 == y && p[i] == (a + x) % 10 + (a + z) % 10) { cur[i] = a; noov(p, i + 1, (a + x) / 10, z); }
}
static void ovtail(const int *p, int i, int prev, int x, int y) {
  if (i == K) {
    for (int z = 0; z < 2; z++) if ((prev + z) / 10 == y) { if (npred < 4096) memcpy(predbuf[npred++], cur, sizeof cur); return; }
    return;
  }
  for (int a = 0; a < 19; a++)
    for (int z = 0; z < 2; z++)
      if ((prev + z) / 10 == y && p[i] == (a + x) % 10 + (prev + z) % 10) { cur[i] = a; ovtail(p, i + 1, a, (a + x) / 10, z); }
}
static void preds(const int *p) {
  npred = 0;
  noov(p, 0, 0, 0);
  int v = p[0];
  if (0 < v && v <= 10) {
    int a = v <= 9 ? v + 9 : 9;
    cur[0] = a;
    ovtail(p, 1, a, a / 10, 1);
  }
}

int main(int argc, char **argv) {
  K = atoi(argv[1]);
  P19[0] = 1;
  for (int i = 1; i < 16; i++) P19[i] = P19[i - 1] * 19;
  uint64_t NX = P19[K - 1];
  nXw = (NX + 63) / 64;
  nblk = (nXw + 7) / 8;
  X = calloc(nXw + 8, 8);
  cnt = calloc(nblk + 1, 8);
  FILE *f = fopen(argv[2], "rb");
  if (!f || fread(X, 8, nXw, f) != nXw) return 1;
  fclose(f);
  uint64_t acc = 0;
  for (uint64_t b = 0; b < nblk; b++) {
    cnt[b] = acc;
    for (uint64_t w = b * 8; w < b * 8 + 8 && w < nXw; w++) acc += (uint64_t)__builtin_popcountll(X[w]);
  }
  cnt[nblk] = acc;
  nX = acc;
  NU = nX * 19;
  NUw = (NU + 63) / 64;
  uint8_t *dist = malloc(NU);
  memset(dist, 255, NU);
  uint64_t *fr = calloc(NUw, 8), *nx = calloc(NUw, 8);
  int sw[16], n = 0;
  { char *q = argv[3]; while (*q && n < 16) { sw[n++] = (int)strtol(q, &q, 10); if (*q == ',') q++; } }
  uint64_t start;
  if (!c2u(encode(sw), &start)) { fprintf(stderr, "start not in U\n"); return 1; }
  dist[start] = 0;
  SET(fr, start);
  int d = 0;
  for (;;) {
    uint64_t cntl = 0;
    memset(nx, 0, NUw * 8);
    cur_blk = 0;
    for (uint64_t wi = 0; wi < NUw; wi++) {
      uint64_t m = fr[wi];
      while (m) {
        int b = __builtin_ctzll(m);
        m &= m - 1;
        uint64_t u = (wi << 6) | (uint64_t)b;
        int s[16], o[16];
        decode(u2c(u), s);
        for (int e = 0; e < 2; e++) {
          forward(s, e, o);
          uint64_t v;
          if (!c2u(encode(o), &v)) { fprintf(stderr, "ABORT outside X\n"); return 3; }
          if (dist[v] == 255) { if (d + 1 >= 255) { fprintf(stderr, "depth overflow\n"); return 4; } dist[v] = (uint8_t)(d + 1); SET(nx, v); cntl++; }
        }
      }
    }
    if (!cntl) break;
    d++;
    uint64_t *t = fr; fr = nx; nx = t;
  }
  fprintf(stderr, "BFS depth %d\n", d);
  // best digit word per prefix
  static uint64_t best[9000];
  static int bestd[9000];
  for (int i = 0; i < 9000; i++) bestd[i] = 1000;
  cur_blk = 0;
  for (uint64_t u = 0; u < NU; u++) {
    if (dist[u] == 255) continue;
    int s[16];
    decode(u2c(u), s);
    int ok = s[0] >= 1;
    for (int i = 0; i < K && ok; i++) if (s[i] > 9) ok = 0;
    if (!ok) continue;
    int p = s[0] * 1000 + s[1] * 100 + s[2] * 10 + s[3] - 1000;
    if (dist[u] < bestd[p]) { bestd[p] = dist[u]; best[p] = u; }
  }
  FILE *o = fopen(argv[4], "w");
  int nw = 0, maxlen = 0;
  for (int p = 0; p < 9000; p++) {
    if (bestd[p] == 1000) continue;
    // reconstruct backward
    int len = bestd[p];
    int bits[256];
    int w[16];
    uint64_t u = best[p];
    cur_blk = 0;
    decode(u2c(u), w);
    int target[16];
    memcpy(target, w, sizeof w);
    for (int dd = len; dd > 0; dd--) {
      preds(w);
      int found = 0;
      for (int j = 0; j < npred && !found; j++) {
        uint64_t pu;
        if (!c2u(encode(predbuf[j]), &pu)) continue;
        if (dist[pu] != dd - 1) continue;
        for (int e = 0; e < 2 && !found; e++) {
          int ot[16];
          forward(predbuf[j], e, ot);
          if (memcmp(ot, w, K * sizeof(int)) == 0) { bits[dd - 1] = e; memcpy(w, predbuf[j], sizeof w); found = 1; }
        }
      }
      if (!found) { fprintf(stderr, "reconstruction failed p=%d\n", p + 1000); return 5; }
    }
    // self-check: replay forward from start
    int s[16];
    memcpy(s, sw, sizeof sw);
    for (int i = 0; i < len; i++) { int t2[16]; forward(s, bits[i], t2); memcpy(s, t2, sizeof s); }
    if (memcmp(s, target, K * sizeof(int))) { fprintf(stderr, "replay mismatch p=%d\n", p + 1000); return 6; }
    fprintf(o, "%d\t%d\t", p + 1000, len);
    for (int i = 0; i < K; i++) fprintf(o, i ? ",%d" : "%d", target[i]);
    fprintf(o, "\t");
    for (int i = 0; i < len; i++) fprintf(o, "%d", bits[i]);
    fprintf(o, "\n");
    nw++;
    if (len > maxlen) maxlen = len;
  }
  fclose(o);
  printf("K=%d walks=%d maxlen=%d bfsdepth=%d\n", K, nw, maxlen, d);
  return 0;
}
