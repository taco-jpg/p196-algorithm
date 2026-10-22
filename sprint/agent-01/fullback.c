// Full long-regime backward closure B_K(P) of the width-K initial words of a
// 4-digit prefix P (P ++ decimal tail), with an open-addressing hash set.
// Reports |B_K(P)| and, if it is acyclic, the longest backward path ending at an
// initial word (long regime only; short-width ancestry not included).
// Usage: fullback K CAP P1 [P2 ...]      (CAP = max nodes, e.g. 150000000)
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static int K;
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
static int npred, cur[16];
static int predbuf[8192][16];
static void noov(const int *p, int i, int x, int y) {
  if (i == K) { if (cur[0] > 0) memcpy(predbuf[npred++], cur, sizeof cur); return; }
  for (int a = 0; a < 19; a++)
    for (int z = 0; z < 2; z++)
      if ((a + z) / 10 == y && p[i] == (a + x) % 10 + (a + z) % 10) { cur[i] = a; noov(p, i + 1, (a + x) / 10, z); }
}
static void ovtail(const int *p, int i, int prev, int x, int y) {
  if (i == K) {
    for (int z = 0; z < 2; z++) if ((prev + z) / 10 == y) { memcpy(predbuf[npred++], cur, sizeof cur); return; }
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
}
// hash set: code -> index
static uint64_t HCAP, *hkey; static uint32_t *hval;
static inline uint64_t hh(uint64_t x) { x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; return x; }
static int64_t hfind(uint64_t c) {
  uint64_t i = hh(c) & (HCAP - 1);
  while (hkey[i] != ~0ULL) { if (hkey[i] == c) return hval[i]; i = (i + 1) & (HCAP - 1); }
  return -1;
}
static int hins(uint64_t c, uint32_t v) {
  uint64_t i = hh(c) & (HCAP - 1);
  while (hkey[i] != ~0ULL) { if (hkey[i] == c) return 0; i = (i + 1) & (HCAP - 1); }
  hkey[i] = c; hval[i] = v; return 1;
}
int main(int argc, char **argv) {
  K = atoi(argv[1]);
  uint64_t CAP = strtoull(argv[2], 0, 10);
  HCAP = 1;
  while (HCAP < CAP * 2) HCAP <<= 1;
  hkey = malloc(HCAP * 8); hval = malloc(HCAP * 4);
  uint64_t *nodes = malloc(CAP * 8);
  for (int a = 3; a < argc; a++) {
    time_t t0 = time(NULL);
    int P = atoi(argv[a]);
    memset(hkey, 0xff, HCAP * 8);
    uint64_t n = 0, ntail = 1;
    for (int i = 4; i < K; i++) ntail *= 10;
    for (uint64_t t = 0; t < ntail; t++) {
      int w[16];
      w[0] = P / 1000; w[1] = P / 100 % 10; w[2] = P / 10 % 10; w[3] = P % 10;
      uint64_t x = t;
      for (int i = K - 1; i >= 4; i--) { w[i] = (int)(x % 10); x /= 10; }
      uint64_t c = encode(w);
      if (hins(c, (uint32_t)n)) nodes[n++] = c;
    }
    uint64_t ninit = n, head = 0;
    int capped = 0;
    while (head < n) {
      int w[16];
      decode(nodes[head++], w);
      preds(w);
      for (int j = 0; j < npred; j++) {
        uint64_t c = encode(predbuf[j]);
        if (hfind(c) < 0) {
          if (n >= CAP) { capped = 1; break; }
          hins(c, (uint32_t)n);
          nodes[n++] = c;
        }
      }
      if (capped) break;
    }
    if (capped) { printf("K=%d prefix=%d CAPPED at %llu nodes (%lds)\n", K, P, (unsigned long long)n, (long)(time(NULL) - t0)); fflush(stdout); continue; }
    // peel inside the closure (in-degrees from closure sources)
    uint16_t *deg = calloc(n, 2);
    uint8_t *rnd = calloc(n, 1);
    for (uint64_t i = 0; i < n; i++) {
      int s[16], o[16];
      decode(nodes[i], s);
      if (s[0] == 0) continue;
      for (int e = 0; e < 2; e++) { forward(s, e, o); int64_t j = hfind(encode(o)); if (j >= 0) deg[j]++; }
    }
    uint64_t *q = malloc(n * 8), qh = 0, qt = 0;
    for (uint64_t i = 0; i < n; i++) if (!deg[i]) { q[qt++] = i; rnd[i] = 1; }
    while (qh < qt) {
      uint64_t i = q[qh++];
      int s[16], o[16];
      decode(nodes[i], s);
      if (s[0] == 0) continue;
      for (int e = 0; e < 2; e++) {
        forward(s, e, o);
        int64_t j = hfind(encode(o));
        if (j >= 0 && --deg[j] == 0) { q[qt++] = (uint64_t)j; rnd[j] = (uint8_t)(rnd[i] + 1 > 250 ? 250 : rnd[i] + 1); }
      }
    }
    int maxr = 0; uint64_t alive = 0;
    for (uint64_t i = 0; i < ninit; i++) { if (!rnd[i]) alive++; else if (rnd[i] > maxr) maxr = rnd[i]; }
    printf("K=%d prefix=%d |B|=%llu cyclic_nodes=%llu initial_on_or_after_cycle=%llu longest_long_path_to_initial=%d (%lds)\n",
           K, P, (unsigned long long)n, (unsigned long long)(n - qt), (unsigned long long)alive, maxr - 1,
           (long)(time(NULL) - t0));
    fflush(stdout);
    free(deg); free(rnd); free(q);
  }
  return 0;
}
