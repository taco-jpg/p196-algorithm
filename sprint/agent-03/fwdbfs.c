/* fwdbfs.c -- forward closure of the k-column prefix abstraction, optionally
 * enriched with a finite automaton E driven by (overflow bit b, inner carry e).
 *
 * Abstract step (identical to Lean SevenColumnProjection.forwardPrefix):
 *   w --e--> forwardPrefix(w, e),  e in {0,1},  with overflow bit b(w,e) = highDigits(w,e).1
 * Enriched step:
 *   (w, E) --e--> (forwardPrefix(w,e), delta[E][b][e])        (no guard: every e allowed)
 *
 * Word code: code(w) = sum_i w[i] * 19^i   (w[0] = outermost column sum, least significant).
 * State index: code * NE + E.  Visited / frontier are bitsets.
 *
 * Usage:
 *   fwdbfs K TABLE OUTPROJ [w0_0 ... w0_{K-1}]
 *     TABLE   : "none" or a file: first line "NE E0", then NE lines "d00 d01 d10 d11"
 *               where dbe = delta[E][b][e]
 *     OUTPROJ : file to receive the projection bitset (19^K bits, bit = word code), or "-"
 *     w0      : initial word (K entries, outermost first)
 * Prints one summary line:
 *   K NE reach_states proj_words branching_words passes seconds
 *   branching_words = projected words w with forwardPrefix(w,0) != forwardPrefix(w,1)
 * Build: cc -O3 -march=native -o fwdbfs fwdbfs.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

static int K;
static uint64_t P19[16];

static inline void decode(uint64_t c, int *w) { for (int i = 0; i < K; i++) { w[i] = (int)(c % 19); c /= 19; } }
static inline uint64_t encode(const int *w) { uint64_t c = 0; for (int i = K - 1; i >= 0; i--) c = c * 19 + (uint64_t)w[i]; return c; }

/* forwardPrefix(w, e); returns overflow bit, writes successor into out */
static inline int fwd(const int *w, int e, int *out) {
    int lo[16], hi[16];
    int x = 0;
    for (int i = 0; i < K; i++) { int s = w[i] + x; lo[i] = s % 10; x = s / 10; }
    int c = e;                       /* carry into column L-K */
    for (int i = K - 1; i >= 0; i--) { int s = w[i] + c; hi[i] = s % 10; c = s / 10; }
    /* hi[i] = output digit of column L-1-i ; c = final carry c_L */
    if (c == 0) { for (int i = 0; i < K; i++) out[i] = lo[i] + hi[i]; }
    else { out[0] = lo[0] + 1; for (int i = 1; i < K; i++) out[i] = lo[i] + hi[i - 1]; }
    return c;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s K TABLE OUTPROJ w0...\n", argv[0]); return 1; }
    K = atoi(argv[1]);
    if (K < 1 || K > 15 || argc != 4 + K) { fprintf(stderr, "bad K / word\n"); return 1; }
    P19[0] = 1; for (int i = 1; i < 16; i++) P19[i] = P19[i - 1] * 19;
    int NE = 1, E0 = 0;
    int (*delta)[2][2] = NULL;
    if (strcmp(argv[2], "none") != 0) {
        FILE *f = fopen(argv[2], "r");
        if (!f || fscanf(f, "%d %d", &NE, &E0) != 2) { fprintf(stderr, "table\n"); return 1; }
        delta = malloc(sizeof(int[2][2]) * NE);
        for (int s = 0; s < NE; s++)
            for (int b = 0; b < 2; b++) for (int e = 0; e < 2; e++)
                if (fscanf(f, "%d", &delta[s][b][e]) != 1 || delta[s][b][e] < 0 || delta[s][b][e] >= NE) { fprintf(stderr, "table row\n"); return 1; }
        fclose(f);
    }
    int w0[16];
    for (int i = 0; i < K; i++) { w0[i] = atoi(argv[4 + i]); if (w0[i] < 0 || w0[i] > 18) { fprintf(stderr, "w0\n"); return 1; } }
    uint64_t nwords = P19[K];
    uint64_t nstates = nwords * (uint64_t)NE;
    uint64_t nw64 = (nstates + 63) / 64;
    uint64_t *vis = calloc(nw64, 8), *fr = calloc(nw64, 8);
    if (!vis || !fr) { fprintf(stderr, "alloc %llu words\n", (unsigned long long)nw64); return 1; }
    clock_t t0 = clock();
    uint64_t s0 = encode(w0) * NE + E0;
    vis[s0 >> 6] |= 1ULL << (s0 & 63); fr[s0 >> 6] |= 1ULL << (s0 & 63);
    uint64_t reach = 1; int passes = 0, changed = 1;
    int w[16], v[16];
    while (changed) {
        changed = 0; passes++;
        for (uint64_t j = 0; j < nw64; j++) {
            while (fr[j]) {
                int bit = __builtin_ctzll(fr[j]);
                fr[j] &= fr[j] - 1;
                uint64_t s = (j << 6) | (uint64_t)bit;
                uint64_t code = s / NE; int E = (int)(s % NE);
                decode(code, w);
                for (int e = 0; e < 2; e++) {
                    int b = fwd(w, e, v);
                    int E2 = delta ? delta[E][b][e] : 0;
                    uint64_t s2 = encode(v) * NE + E2;
                    uint64_t m = 1ULL << (s2 & 63);
                    if (!(vis[s2 >> 6] & m)) {
                        vis[s2 >> 6] |= m; fr[s2 >> 6] |= m; reach++;
                        if ((s2 >> 6) <= j) changed = 1; /* behind the scan: needs another pass */
                    }
                }
            }
        }
    }
    /* projection */
    uint64_t pw64 = (nwords + 63) / 64;
    free(fr); fr = NULL;                     /* frontier is empty now; release before projecting */
    uint64_t *proj = NE == 1 ? vis : calloc(pw64, 8);   /* NE == 1: the projection is vis itself */
    if (!proj) { fprintf(stderr, "alloc proj\n"); return 1; }
    uint64_t projn = 0, branching = 0;
    if (NE == 1) projn = reach;
    else for (uint64_t j = 0; j < nw64; j++) {
        uint64_t x = vis[j];
        while (x) {
            int bit = __builtin_ctzll(x); x &= x - 1;
            uint64_t code = ((j << 6) | (uint64_t)bit) / NE;
            uint64_t m = 1ULL << (code & 63);
            if (!(proj[code >> 6] & m)) { proj[code >> 6] |= m; projn++; }
        }
    }
    for (uint64_t j = 0; j < pw64; j++) {
        uint64_t x = proj[j];
        while (x) {
            int bit = __builtin_ctzll(x); x &= x - 1;
            decode((j << 6) | (uint64_t)bit, w);
            int a[16], c[16];
            fwd(w, 0, a); fwd(w, 1, c);
            if (memcmp(a, c, sizeof(int) * K) != 0) branching++;
        }
    }
    double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
    printf("%d %d %llu %llu %llu %d %.2f\n", K, NE, (unsigned long long)reach, (unsigned long long)projn,
           (unsigned long long)branching, passes, secs);
    if (strcmp(argv[3], "-") != 0) {
        FILE *f = fopen(argv[3], "wb");
        if (!f) { fprintf(stderr, "out\n"); return 1; }
        fwrite(proj, 8, pw64, f); fclose(f);
    }
    if (proj != vis) free(proj);
    free(vis); free(delta);
    return 0;
}
