// Does the backward closure of a prefix's initial words contain a cycle at
// width K?  (= is some initial word in the infinite-history core C_K?)
//
// Only nodes in U_K = pi^{-1}(X) are explored, X = dense width-(K-1) bitset
// containing C_{K-1}: every node of C_K projects into C_{K-1} and every
// backward path inside C_K stays inside C_K, so cycles that reach an initial
// word are found inside U_K.  Nodes outside U_K have finite backward history.
//
// Usage: backcore K Xprev.bits P1 [P2 ...]      (Pi = 4-digit prefixes)
// For each prefix: |S| = size of the backward closure inside U_K of the
// initial words P ++ digits that lie in U_K; then peels S (in-degrees counted
// within S) and reports how many initial words survive (= lie in C_K) and the
// longest backward path ending at an initial word (in rounds) if none survive.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

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
static int npred, cur[16];
static int predbuf[8192][16];
static void noov(const int *p, int i, int x, int y) {
  if (i == K) { if (cur[0] > 0 && npred < 8192) memcpy(predbuf[npred++], cur, sizeof cur); return; }
  for (int a = 0; a < 19; a++)
    for (int z = 0; z < 2; z++)
      if ((a + z) / 10 == y && p[i] == (a + x) % 10 + (a + z) % 10) { cur[i] = a; noov(p, i + 1, (a + x) / 10, z); }
}
static void ovtail(const int *p, int i, int prev, int x, int y) {
  if (i == K) {
    for (int z = 0; z < 2; z++) if ((prev + z) / 10 == y) { if (npred < 8192) memcpy(predbuf[npred++], cur, sizeof cur); return; }
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
  if (0 < v && v <= 10) { int a = v <= 9 ? v + 9 : 9; cur[0] = a; ovtail(p, 1, a, a / 10, 1); }
  if (npred >= 8192) { fprintf(stderr, "pred overflow\n"); exit(7); }
}
static int cmpu(const void *a, const void *b) {
  uint64_t x = *(const uint64_t *)a, y = *(const uint64_t *)b;
  return x < y ? -1 : x > y;
}
static uint64_t *arr; static uint64_t narr;
static int64_t idx(uint64_t u) {
  uint64_t lo = 0, hi = narr;
  while (lo < hi) { uint64_t m = (lo + hi) / 2; if (arr[m] < u) lo = m + 1; else hi = m; }
  return (lo < narr && arr[lo] == u) ? (int64_t)lo : -1;
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
  nX = acc; NU = nX * 19; NUw = (NU + 63) / 64;
  uint64_t *S = calloc(NUw, 8), *fr = calloc(NUw, 8);
  if (!S || !fr) { fprintf(stderr, "alloc\n"); return 1; }
  for (int a = 3; a < argc; a++) {
    time_t t0 = time(NULL);
    int P = atoi(argv[a]);
    memset(S, 0, NUw * 8);
    memset(fr, 0, NUw * 8);
    uint64_t ntail = 1;
    for (int i = 4; i < K; i++) ntail *= 10;
    uint64_t ninit = 0, *init = malloc(ntail * 8);
    for (uint64_t t = 0; t < ntail; t++) {
      int w[16];
      w[0] = P / 1000; w[1] = P / 100 % 10; w[2] = P / 10 % 10; w[3] = P % 10;
      uint64_t x = t;
      for (int i = K - 1; i >= 4; i--) { w[i] = (int)(x % 10); x /= 10; }
      uint64_t u;
      if (!c2u(encode(w), &u)) continue;
      init[ninit++] = u;
      SET(S, u); SET(fr, u);
    }
    // backward closure inside U
    uint64_t total = ninit;
    for (;;) {
      uint64_t n = 0;
      cur_blk = 0;
      for (uint64_t wi = 0; wi < NUw; wi++) {
        while (fr[wi]) {
          int b = __builtin_ctzll(fr[wi]);
          fr[wi] &= ~(1ULL << b);
          uint64_t u = (wi << 6) | (uint64_t)b;
          int w[16];
          decode(u2c(u), w);
          preds(w);
          uint64_t sc = cur_blk;
          for (int j = 0; j < npred; j++) {
            uint64_t v;
            if (!c2u(encode(predbuf[j]), &v)) continue;
            if (!GET(S, v)) { SET(S, v); SET(fr, v); total++; }
          }
          cur_blk = sc;
          n++;
        }
      }
      if (!n) break;
    }
    // compact S, peel inside S
    narr = 0;
    for (uint64_t wi = 0; wi < NUw; wi++) narr += (uint64_t)__builtin_popcountll(S[wi]);
    arr = malloc(narr * 8);
    uint16_t *deg = calloc(narr, 2);
    uint8_t *rnd = calloc(narr, 1);
    uint64_t k2 = 0;
    for (uint64_t wi = 0; wi < NUw; wi++) {
      uint64_t m = S[wi];
      while (m) { int b = __builtin_ctzll(m); m &= m - 1; arr[k2++] = (wi << 6) | (uint64_t)b; }
    }
    cur_blk = 0;
    for (uint64_t i = 0; i < narr; i++) {
      int s[16], o[16];
      decode(u2c(arr[i]), s);
      if (s[0] == 0) continue;
      for (int e = 0; e < 2; e++) {
        forward(s, e, o);
        uint64_t v;
        if (!c2u(encode(o), &v)) continue;
        int64_t j = idx(v);
        if (j >= 0) deg[j]++;
      }
    }
    uint64_t *q = malloc(narr * 8), qh = 0, qt = 0;
    for (uint64_t i = 0; i < narr; i++) if (!deg[i]) { q[qt++] = i; rnd[i] = 1; }
    while (qh < qt) {
      uint64_t i = q[qh++];
      int s[16], o[16];
      cur_blk = 0;
      decode(u2c(arr[i]), s);
      if (s[0] == 0) continue;
      for (int e = 0; e < 2; e++) {
        forward(s, e, o);
        uint64_t v;
        if (!c2u(encode(o), &v)) continue;
        int64_t j = idx(v);
        if (j >= 0 && --deg[j] == 0) { q[qt++] = (uint64_t)j; rnd[j] = (uint8_t)(rnd[i] + 1 > 250 ? 250 : rnd[i] + 1); }
      }
    }
    uint64_t alive_init = 0;
    int maxr = 0;
    for (uint64_t i = 0; i < ninit; i++) {
      int64_t j = idx(init[i]);
      if (rnd[j] == 0) alive_init++;
      else if (rnd[j] > maxr) maxr = rnd[j];
    }
    printf("K=%d prefix=%d initial_in_U=%llu |S|=%llu core_nodes_in_S=%llu initial_in_core=%llu maxRoundInitial=%d (%lds)\n",
           K, P, (unsigned long long)ninit, (unsigned long long)narr, (unsigned long long)(narr - qt),
           (unsigned long long)alive_init, maxr, (long)(time(NULL) - t0));
    fflush(stdout);
    free(arr); free(deg); free(rnd); free(q); free(init);
  }
  return 0;
}
