/*
 * liftclosure.c -- forward closure F_{k+1} of the (k+1)-column abstraction, computed inside the lift of F_k.
 *
 * Fact used (checked by assertion, and provable from the definitions): the first k entries of
 * forwardPrefix(w, e) for a (k+1)-word w equal forwardPrefix(w[0..k-1], e') with
 * e' = (w[k] + e) / 10 in {0,1}. Hence the k-prefix of every word of F_{k+1} lies in F_k, and
 * F_{k+1} can be stored as a bitset over (dense index of the F_k word) * 19 + last entry.
 *
 * Usage:
 *   liftclosure K FK_BITS OUTPREFIX w0csv          (computes F_{K+1}; K = width of FK_BITS)
 *   then queries:  liftclosure K FK_BITS OUTPREFIX w0csv --prefixes N OUTFILE  (after the closure)
 *
 * Output: OUTPREFIX.lift.bits (bitset over |F_K| * 19), JSON summary on stdout,
 *         and for --prefixes, the excluded N-digit prefixes at width K+1 (same rule as prefixes.c).
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static int K;          /* base width; closure is at width K+1 */
static uint64_t NK;    /* 19^K */
static uint64_t nwK;   /* 64-bit words of the F_K bitset */
static uint64_t *FK;   /* F_K bitset */
static uint64_t *blk;  /* cumulative popcount before each 512-bit block */
static uint64_t nF;    /* |F_K| */
static uint64_t *vis, *done; /* bitsets over nF*19 */

static inline int getb(const uint64_t *b, uint64_t i) { return (b[i >> 6] >> (i & 63)) & 1; }
static inline void setb(uint64_t *b, uint64_t i) { b[i >> 6] |= (uint64_t)1 << (i & 63); }

static uint64_t encodeK(const int *w) { uint64_t x = 0; for (int i = 0; i < K; i++) x = x * 19 + (uint64_t)w[i]; return x; }
static void decodeK(uint64_t idx, int *w) { for (int i = K - 1; i >= 0; i--) { w[i] = (int)(idx % 19); idx /= 19; } }

/* rank of a word index that must be in F_K; returns UINT64_MAX if not in F_K */
static inline uint64_t rankK(uint64_t idx) {
  uint64_t wi = idx >> 6;
  if (!((FK[wi] >> (idx & 63)) & 1)) return UINT64_MAX;
  uint64_t b = wi >> 3, r = blk[b];
  for (uint64_t j = b << 3; j < wi; j++) r += (uint64_t)__builtin_popcountll(FK[j]);
  uint64_t m = (idx & 63) ? (FK[wi] & ((((uint64_t)1) << (idx & 63)) - 1)) : 0;
  return r + (uint64_t)__builtin_popcountll(m);
}

static void fwd(int k, const int *s, int e, int *out) {
  int lo[40], hi[40], c = 0;
  for (int i = 0; i < k; i++) { int v = s[i] + c; lo[i] = v % 10; c = v / 10; }
  c = e;
  for (int i = k - 1; i >= 0; i--) { int v = s[i] + c; hi[i] = v % 10; c = v / 10; }
  if (c == 0) for (int i = 0; i < k; i++) out[i] = lo[i] + hi[i];
  else { out[0] = lo[0] + 1; for (int i = 1; i < k; i++) out[i] = lo[i] + hi[i - 1]; }
}

static uint64_t lifted(const int *w) { /* w has K+1 entries */
  uint64_t r = rankK(encodeK(w));
  if (r == UINT64_MAX) { fprintf(stderr, "prefix of a successor not in F_K: lift fact violated\n"); exit(3); }
  return r * 19 + (uint64_t)w[K];
}

int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage: %s K FK_BITS OUT w0csv [--prefixes N OUTFILE]\n", argv[0]); return 2; }
  K = atoi(argv[1]);
  NK = 1; for (int i = 0; i < K; i++) NK *= 19;
  nwK = (NK + 63) / 64;
  uint64_t nwpad = (nwK + 7) & ~(uint64_t)7;
  FK = calloc(nwpad, 8);
  FILE *f = fopen(argv[2], "rb");
  if (!f || fread(FK, 8, nwK, f) != nwK) { fprintf(stderr, "read FK\n"); return 1; }
  fclose(f);
  uint64_t nb = nwpad / 8;
  blk = malloc((nb + 1) * 8);
  uint64_t acc = 0;
  for (uint64_t b = 0; b < nb; b++) {
    blk[b] = acc;
    for (int j = 0; j < 8; j++) acc += (uint64_t)__builtin_popcountll(FK[b * 8 + j]);
  }
  blk[nb] = acc;
  nF = acc;
  uint64_t NL = nF * 19, nwL = (NL + 63) / 64;
  vis = calloc(nwL, 8);
  done = calloc(nwL, 8);
  if (!vis || !done) { fprintf(stderr, "alloc\n"); return 1; }
  int w0[64], n0 = 0;
  char *tok = strtok(argv[4], ",");
  while (tok && n0 < 64) { w0[n0++] = atoi(tok); tok = strtok(NULL, ","); }
  const int K1 = K + 1;
  char path[4096];
  snprintf(path, sizeof path, "%s.lift.bits", argv[3]);
  int query = argc >= 8 && strcmp(argv[5], "--prefixes") == 0;
  uint64_t count = 0;
  int passes = 0;
  clock_t t0 = clock();
  if (!query) {
    setb(vis, lifted(w0));
    count = 1;
    int s[40], o[40], changed = 1;
    while (changed) {
      changed = 0;
      passes++;
      /* walk F_K set bits in order; r = dense rank */
      uint64_t r = 0;
      for (uint64_t wi = 0; wi < nwK; wi++) {
        uint64_t x = FK[wi];
        while (x) {
          int b = __builtin_ctzll(x); x &= x - 1;
          uint64_t idx = wi * 64 + (uint64_t)b;
          uint64_t base = r * 19;
          int decoded = 0;
          for (int d = 0; d < 19; d++) {
            uint64_t L = base + (uint64_t)d;
            if (!getb(vis, L) || getb(done, L)) continue;
            setb(done, L);
            if (!decoded) { decodeK(idx, s); decoded = 1; }
            s[K] = d;
            for (int e = 0; e <= 1; e++) {
              fwd(K1, s, e, o);
              uint64_t j = lifted(o);
              if (!getb(vis, j)) {
                setb(vis, j);
                count++;
                if (j < L) changed = 1;
              }
            }
          }
          r++;
        }
      }
    }
    f = fopen(path, "wb"); fwrite(vis, 8, nwL, f); fclose(f);
  } else {
    f = fopen(path, "rb");
    if (!f || fread(vis, 8, nwL, f) != nwL) { fprintf(stderr, "read lift\n"); return 1; }
    fclose(f);
    for (uint64_t i = 0; i < nwL; i++) count += (uint64_t)__builtin_popcountll(vis[i]);
  }
  double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
  /* digit words in F_{K+1} */
  uint64_t dig = 0;
  {
    uint64_t P = 1; for (int i = 0; i < K1; i++) P *= 10;
    int w[40];
    for (uint64_t x = 0; x < P; x++) {
      uint64_t y = x;
      for (int i = K1 - 1; i >= 0; i--) { w[i] = (int)(y % 10); y /= 10; }
      uint64_t rr = rankK(encodeK(w));
      if (rr != UINT64_MAX && getb(vis, rr * 19 + (uint64_t)w[K])) dig++;
    }
  }
  long hwm = 0;
  { FILE *st = fopen("/proc/self/status", "r"); char line[256];
    while (st && fgets(line, sizeof line, st)) if (!strncmp(line, "VmHWM:", 6)) hwm = atol(line + 6);
    if (st) fclose(st); }
  printf("{\"k\": %d, \"F\": %llu, \"lift_space\": %llu, \"digit_words_in_F\": %llu, \"passes\": %d, "
         "\"cpu_seconds\": %.1f, \"peak_rss_kb\": %ld}\n",
         K1, (unsigned long long)count, (unsigned long long)NL, (unsigned long long)dig, passes, secs, hwm);
  if (query) {
    int n = atoi(argv[6]);
    FILE *out = fopen(argv[7], "w");
    uint64_t p10n = 1, p10t = 1;
    for (int i = 0; i < n; i++) p10n *= 10;
    for (int i = n; i < K1; i++) p10t *= 10;
    long excl = 0, skip = 0, lead[10] = {0};
    int w[40];
    for (uint64_t P = p10n / 10; P < p10n; P++) {
      uint64_t y = P;
      for (int i = n - 1; i >= 0; i--) { w[i] = (int)(y % 10); y /= 10; }
      int nov = w[0] >= 2;
      for (int i = 0; i < n; i++) if (w[i] >= 3) nov = 1;
      int found = 0;
      for (uint64_t t = 0; t < p10t && !found; t++) {
        uint64_t z = t;
        for (int i = K1 - 1; i >= n; i--) { w[i] = (int)(z % 10); z /= 10; }
        uint64_t rr = rankK(encodeK(w));
        if (rr != UINT64_MAX && getb(vis, rr * 19 + (uint64_t)w[K])) found = 1;
      }
      if (!found) {
        if (!nov) { skip++; continue; }
        excl++; lead[w[0]]++;
        for (int i = 0; i < n; i++) fputc('0' + w[i], out);
        fputc('\n', out);
      }
    }
    fclose(out);
    printf("{\"k\": %d, \"n\": %d, \"excluded\": %ld, \"absent_but_overflow_possible\": %ld, \"by_lead\": [", K1, n, excl, skip);
    for (int a = 0; a < 10; a++) printf("%s%ld", a ? ", " : "", lead[a]);
    printf("]}\n");
  }
  return 0;
}
