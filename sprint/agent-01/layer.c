// Width-K forward closure (and optionally the infinite-history core) computed
// inside U_K = pi^{-1}(X), where X is a dense bitset at width K-1 and
// pi drops the innermost column (code c -> c / 19).
//
// Soundness of the restriction: pi(forwardPrefix s e) = forwardPrefix (pi s) e'
// for some e' in {0,1} (the high scan passes one carry inward->outward), so if X
// is forward closed then U_K is forward closed, the forward closure of a start
// word in U_K stays in U_K, and every infinite backward path of G_K whose
// projection lies in X stays in U_K.  The program ABORTS if a successor ever
// projects outside X (so a wrong X cannot silently give a wrong answer).
//
// Usage: layer K Xprev.bits OUTPREFIX MODE start_word [extra_words ...]
//   MODE letters: f forward closure + prefix hits (always); s single-SCC check;
//         c infinite-history core by peeling, compared with F;
//         d also write the dense width-K bitset OUTPREFIX.bits
//   extra_words: later 196 states; reports membership in F and in R (reach-to-start).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static int K;
static uint64_t P19[16];
static uint64_t *X, nXw, *cnt, nblk, nX;  // level K-1
static uint64_t NU, NUw;                   // |U| bits

static inline int xget(uint64_t p) { return (X[p >> 6] >> (p & 63)) & 1; }
static inline uint64_t rank_(uint64_t p) {
  uint64_t b = p >> 9, r = cnt[b];
  for (uint64_t w = b << 3; w < (p >> 6); w++) r += (uint64_t)__builtin_popcountll(X[w]);
  return r + (uint64_t)__builtin_popcountll(X[p >> 6] & ((1ULL << (p & 63)) - 1));
}
// monotone select cursor
static uint64_t cur_blk;
static uint64_t select_(uint64_t r) {
  if (cur_blk >= nblk || cnt[cur_blk] > r) cur_blk = 0;  // reset if needed
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
  fprintf(stderr, "select overflow\n");
  exit(2);
}
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
static inline uint64_t c2u(uint64_t c) {
  uint64_t p = c / 19;
  if (!xget(p)) { fprintf(stderr, "ABORT: successor projects outside X (code %llu)\n", (unsigned long long)c); exit(3); }
  return rank_(p) * 19 + c % 19;
}
static inline uint64_t u2c(uint64_t u) { return select_(u / 19) * 19 + u % 19; }
static inline void succ(uint64_t u, uint64_t *o) {
  int s[16], w[16];
  decode(u2c(u), s);
  for (int e = 0; e < 2; e++) { forward(s, e, w); o[e] = c2u(encode(w)); }
}
#define GET(b, u) (((b)[(u) >> 6] >> ((u) & 63)) & 1)
#define SET(b, u) ((b)[(u) >> 6] |= 1ULL << ((u) & 63))

static uint64_t parse(const char *p) {
  int w[16], n = 0;
  char *q = (char *)p;
  while (*q && n < 16) { w[n++] = (int)strtol(q, &q, 10); if (*q == ',') q++; }
  if (n != K) { fprintf(stderr, "bad word %s\n", p); exit(1); }
  return encode(w);
}

int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage\n"); return 1; }
  K = atoi(argv[1]);
  const char *outp = argv[3], *mode = argv[4];
  P19[0] = 1;
  for (int i = 1; i < 16; i++) P19[i] = P19[i - 1] * 19;
  uint64_t NX = P19[K - 1];
  nXw = (NX + 63) / 64;
  nblk = (nXw + 7) / 8;
  X = calloc(nXw + 8, 8);
  cnt = calloc(nblk + 1, 8);
  FILE *f = fopen(argv[2], "rb");
  if (!f || fread(X, 8, nXw, f) != nXw) { fprintf(stderr, "read X\n"); return 1; }
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
  time_t t0 = time(NULL);
  fprintf(stderr, "K=%d |X|=%llu |U|=%llu\n", K, (unsigned long long)nX, (unsigned long long)NU);
  uint64_t *vis = calloc(NUw, 8), *fr = calloc(NUw, 8);
  if (!vis || !fr) { fprintf(stderr, "alloc\n"); return 1; }
  uint64_t start = c2u(parse(argv[5]));
  SET(vis, start);
  SET(fr, start);
  // forward closure
  int sweeps = 0;
  uint64_t total = 0;
  for (;;) {
    uint64_t n = 0;
    cur_blk = 0;
    for (uint64_t wi = 0; wi < NUw; wi++) {
      while (fr[wi]) {
        int b = __builtin_ctzll(fr[wi]);
        fr[wi] &= ~(1ULL << b);
        uint64_t u = (wi << 6) | (uint64_t)b, o[2];
        succ(u, o);
        for (int e = 0; e < 2; e++)
          if (!GET(vis, o[e])) { SET(vis, o[e]); SET(fr, o[e]); }
        n++;
      }
    }
    total += n;
    sweeps++;
    fprintf(stderr, "  fwd sweep %d expanded %llu total %llu (%lds)\n", sweeps, (unsigned long long)n,
            (unsigned long long)total, (long)(time(NULL) - t0));
    if (!n) break;
  }
  // prefix hits of F
  static char pre4[9000];
  memset(pre4, '0', sizeof pre4);
  uint64_t ndig = 0;
  cur_blk = 0;
  for (uint64_t wi = 0; wi < NUw; wi++) {
    uint64_t m = vis[wi];
    while (m) {
      int b = __builtin_ctzll(m);
      m &= m - 1;
      int s[16];
      decode(u2c((wi << 6) | (uint64_t)b), s);
      int ok = s[0] >= 1;
      for (int i = 0; i < K && ok; i++) if (s[i] > 9) ok = 0;
      if (!ok) continue;
      ndig++;
      pre4[s[0] * 1000 + s[1] * 100 + s[2] * 10 + s[3] - 1000] = '1';
    }
  }
  int n4 = 0;
  for (int i = 0; i < 9000; i++) n4 += pre4[i] == '1';
  char fn[4096];
  snprintf(fn, sizeof fn, "%s.pre4", outp);
  f = fopen(fn, "w");
  fwrite(pre4, 1, 9000, f);
  fclose(f);
  printf("K=%d |X_{K-1}|=%llu |U|=%llu |F|=%llu sweeps=%d digitwords_in_F=%llu pre4_hit=%d/9000 (%lds)\n", K,
         (unsigned long long)nX, (unsigned long long)NU, (unsigned long long)total, sweeps,
         (unsigned long long)ndig, n4, (long)(time(NULL) - t0));
  fflush(stdout);
  if (strchr(mode, 'd')) {
    uint64_t NK = P19[K], nKw = (NK + 63) / 64;
    uint64_t *D = calloc(nKw, 8);
    cur_blk = 0;
    for (uint64_t wi = 0; wi < NUw; wi++) {
      uint64_t m = vis[wi];
      while (m) {
        int b = __builtin_ctzll(m);
        m &= m - 1;
        uint64_t c = u2c((wi << 6) | (uint64_t)b);
        SET(D, c);
      }
    }
    snprintf(fn, sizeof fn, "%s.bits", outp);
    f = fopen(fn, "wb");
    fwrite(D, 8, nKw, f);
    fclose(f);
    free(D);
  }
  // single-SCC check: R = nodes of F reaching start (reuse fr as R)
  if (strchr(mode, 's')) {
  memset(fr, 0, NUw * 8);
  SET(fr, start);
  int rs = 0;
  for (;;) {
    uint64_t added = 0;
    cur_blk = 0;
    for (uint64_t wi = 0; wi < NUw; wi++) {
      uint64_t m = vis[wi] & ~fr[wi];
      while (m) {
        int b = __builtin_ctzll(m);
        m &= m - 1;
        uint64_t u = (wi << 6) | (uint64_t)b, o[2];
        succ(u, o);
        if (GET(fr, o[0]) || GET(fr, o[1])) { fr[wi] |= 1ULL << b; added++; }
      }
    }
    rs++;
    if (!added) break;
  }
  uint64_t nr = 0;
  for (uint64_t wi = 0; wi < NUw; wi++) nr += (uint64_t)__builtin_popcountll(fr[wi]);
  printf("  single-SCC check: |R|=%llu |F|=%llu sweeps=%d single_SCC=%s (%lds)\n", (unsigned long long)nr,
         (unsigned long long)total, rs, nr == total ? "yes" : "no", (long)(time(NULL) - t0));
  for (int a = 6; a < argc; a++) {
    uint64_t c = parse(argv[a]);
    int inX = xget(c / 19);
    uint64_t u = inX ? rank_(c / 19) * 19 + c % 19 : 0;
    printf("  word %s inF=%d inR=%d\n", argv[a], inX ? (int)GET(vis, u) : 0, inX ? (int)GET(fr, u) : 0);
  }
  } else {
    for (int a = 6; a < argc; a++) {
      uint64_t c = parse(argv[a]);
      int inX = xget(c / 19);
      uint64_t u = inX ? rank_(c / 19) * 19 + c % 19 : 0;
      printf("  word %s inF=%d\n", argv[a], inX ? (int)GET(vis, u) : 0);
    }
  }
  fflush(stdout);
  if (strchr(mode, 'c')) {
    // infinite-history core of the subgraph induced on U by peeling
    free(fr);
    uint16_t *deg = calloc(NU, 2);
    uint64_t *cur = calloc(NUw, 8), *nxt = calloc(NUw, 8);
    if (!deg || !cur || !nxt) { fprintf(stderr, "alloc core\n"); return 1; }
    cur_blk = 0;
    for (uint64_t u = 0; u < NU; u++) {
      uint64_t c = u2c(u);
      if (c < P19[K - 1]) continue;  // s_0 = 0: not a source
      uint64_t o[2];
      int s[16], w[16];
      decode(c, s);
      for (int e = 0; e < 2; e++) { forward(s, e, w); o[e] = c2u(encode(w)); }
      if (deg[o[0]] == 65535 || deg[o[1]] == 65535) { fprintf(stderr, "deg overflow\n"); return 1; }
      deg[o[0]]++;
      deg[o[1]]++;
    }
    for (uint64_t u = 0; u < NU; u++) if (!deg[u]) SET(cur, u);
    uint64_t *dead = nxt;  // reuse: we need cur, nxt, dead -> allocate dead
    dead = calloc(NUw, 8);
    int rounds = 0;
    for (;;) {
      uint64_t n = 0;
      memset(nxt, 0, NUw * 8);
      cur_blk = 0;
      for (uint64_t wi = 0; wi < NUw; wi++) {
        uint64_t m = cur[wi];
        while (m) {
          int b = __builtin_ctzll(m);
          m &= m - 1;
          uint64_t u = (wi << 6) | (uint64_t)b;
          SET(dead, u);
          n++;
          uint64_t c = u2c(u);
          if (c < P19[K - 1]) continue;
          uint64_t o[2];
          int s[16], w[16];
          decode(c, s);
          for (int e = 0; e < 2; e++) { forward(s, e, w); o[e] = c2u(encode(w)); }
          for (int e = 0; e < 2; e++) if (--deg[o[e]] == 0) SET(nxt, o[e]);
        }
      }
      if (!n) break;
      rounds++;
      uint64_t *t = cur; cur = nxt; nxt = t;
    }
    uint64_t core = 0, fnotc = 0, cnotf = 0;
    for (uint64_t wi = 0; wi < NUw; wi++) {
      uint64_t c = ~dead[wi];
      if (wi == NUw - 1 && (NU & 63)) c &= (1ULL << (NU & 63)) - 1;
      core += (uint64_t)__builtin_popcountll(c);
      fnotc += (uint64_t)__builtin_popcountll(vis[wi] & ~c);
      cnotf += (uint64_t)__builtin_popcountll(c & ~vis[wi]);
    }
    printf("  core: rounds=%d |C|=%llu F_not_C=%llu C_not_F=%llu (%lds)\n", rounds, (unsigned long long)core,
           (unsigned long long)fnotc, (unsigned long long)cnotf, (long)(time(NULL) - t0));
  }
  return 0;
}
