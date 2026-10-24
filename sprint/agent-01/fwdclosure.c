// Forward closure of the k-column prefix abstraction (Agent104 forwardPrefix,
// both inner carries e in {0,1}) from one or more start words.
//
// Usage: fwdclosure K OUT_PREFIX w0,w1,...,w_{K-1} [more start words...]
//   Words are column sums q_0..q_{K-1} (units end first), entries 0..18.
//   Codes: c = sum_i q_i * 19^(K-1-i) (q_0 most significant; = Lean wordCode
//   without the leading marker).
// Outputs:
//   OUT_PREFIX.bits     bitset of the reachable set over all 19^K codes
//   OUT_PREFIX.pre4     9000 chars '0'/'1': 1 iff some reachable word with all
//                       entries <= 9 begins with that 4-digit prefix
//                       (index = prefix - 1000)   [only if K >= 4]
//   OUT_PREFIX.pre3     900 chars, same for 3-digit prefixes
// Algorithm: exact worklist closure with a visited bitset and a frontier bitset
// processed in code order (each word expanded exactly once).  No caps.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static int K;
static uint64_t NW, NWORDS64;
static uint64_t *vis, *fr;
static uint64_t P19[16];

static inline int setb(uint64_t *b, uint64_t c) {
  uint64_t m = 1ULL << (c & 63);
  if (b[c >> 6] & m) return 0;
  b[c >> 6] |= m;
  return 1;
}
static void decode(uint64_t c, int *w) {
  for (int i = K - 1; i >= 0; i--) { w[i] = (int)(c % 19); c /= 19; }
}
static uint64_t encode(const int *w) {
  uint64_t c = 0;
  for (int i = 0; i < K; i++) c = c * 19 + (uint64_t)w[i];
  return c;
}
// forwardPrefix s e, literal translation of ActualPrefix.lean.
static void forward(const int *s, int e, int *out) {
  int lo[16], hi[16];
  int x = 0;
  for (int i = 0; i < K; i++) { lo[i] = (s[i] + x) % 10; x = (s[i] + x) / 10; }
  int c = e;
  for (int i = K - 1; i >= 0; i--) { hi[i] = (s[i] + c) % 10; c = (s[i] + c) / 10; }
  if (c == 0) {
    for (int i = 0; i < K; i++) out[i] = lo[i] + hi[i];
  } else {
    out[0] = lo[0] + 1;
    for (int i = 1; i < K; i++) out[i] = lo[i] + hi[i - 1];
  }
}

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: fwdclosure K OUT w0,..,wK-1 ...\n"); return 1; }
  K = atoi(argv[1]);
  const char *outp = argv[2];
  P19[0] = 1;
  for (int i = 1; i < 16; i++) P19[i] = P19[i - 1] * 19;
  NW = P19[K];
  NWORDS64 = (NW + 63) / 64;
  vis = calloc(NWORDS64, 8);
  fr = calloc(NWORDS64, 8);
  if (!vis || !fr) { fprintf(stderr, "alloc failed\n"); return 1; }
  for (int a = 3; a < argc; a++) {
    int w[16], n = 0;
    char *p = argv[a];
    while (*p && n < 16) { w[n++] = (int)strtol(p, &p, 10); if (*p == ',') p++; }
    if (n != K) { fprintf(stderr, "bad start word %s\n", argv[a]); return 1; }
    uint64_t c = encode(w);
    setb(vis, c);
    setb(fr, c);
  }
  time_t t0 = time(NULL);
  int sweep = 0;
  uint64_t expanded = 0;
  for (;;) {
    uint64_t done_this = 0;
    for (uint64_t wi = 0; wi < NWORDS64; wi++) {
      while (fr[wi]) {
        uint64_t m = fr[wi];
        int b = __builtin_ctzll(m);
        fr[wi] &= ~(1ULL << b);
        uint64_t c = (wi << 6) | (uint64_t)b;
        int s[16], o[16];
        decode(c, s);
        for (int e = 0; e < 2; e++) {
          forward(s, e, o);
          uint64_t oc = encode(o);
          if (setb(vis, oc)) setb(fr, oc);
        }
        done_this++;
      }
    }
    expanded += done_this;
    sweep++;
    if (!done_this) break;
  }
  uint64_t total = 0;
  for (uint64_t wi = 0; wi < NWORDS64; wi++) total += (uint64_t)__builtin_popcountll(vis[wi]);
  static char pre4[9000], pre3[900];
  memset(pre4, '0', sizeof pre4);
  memset(pre3, '0', sizeof pre3);
  uint64_t small = 0;
  for (uint64_t wi = 0; wi < NWORDS64; wi++) {
    uint64_t m = vis[wi];
    while (m) {
      int b = __builtin_ctzll(m);
      m &= m - 1;
      int s[16];
      decode((wi << 6) | (uint64_t)b, s);
      int ok = 1;
      for (int i = 0; i < K; i++) if (s[i] > 9) { ok = 0; break; }
      if (!ok || s[0] == 0) continue;
      small++;
      if (K >= 3) pre3[s[0] * 100 + s[1] * 10 + s[2] - 100] = '1';
      if (K >= 4) pre4[s[0] * 1000 + s[1] * 100 + s[2] * 10 + s[3] - 1000] = '1';
    }
  }
  uint64_t adm = 18 * P19[K - 1];
  uint64_t dig = 9;
  for (int i = 1; i < K; i++) dig *= 10;
  int n3 = 0, n4 = 0;
  for (int i = 0; i < 900; i++) n3 += pre3[i] == '1';
  for (int i = 0; i < 9000; i++) n4 += pre4[i] == '1';
  printf("K=%d sweeps=%d expanded=%llu reachable=%llu admissible(q0>0)=%llu fraction=%.6f "
         "digitwords_in_F=%llu/%llu pre3_hit=%d/900 pre4_hit=%d/9000 seconds=%ld\n",
         K, sweep, (unsigned long long)expanded, (unsigned long long)total,
         (unsigned long long)adm, (double)total / (double)adm, (unsigned long long)small,
         (unsigned long long)dig, n3, K >= 4 ? n4 : -1, (long)(time(NULL) - t0));
  char fn[4096];
  snprintf(fn, sizeof fn, "%s.bits", outp);
  FILE *f = fopen(fn, "wb");
  fwrite(vis, 8, NWORDS64, f);
  fclose(f);
  snprintf(fn, sizeof fn, "%s.pre3", outp);
  f = fopen(fn, "w");
  fwrite(pre3, 1, 900, f);
  fclose(f);
  if (K >= 4) {
    snprintf(fn, sizeof fn, "%s.pre4", outp);
    f = fopen(fn, "w");
    fwrite(pre4, 1, 9000, f);
    fclose(f);
  }
  return 0;
}
