/* scc.c -- strongly connected component of a word w0 inside a forward-closed word set F,
 * and BFS distances from w0 (for extracting short cycle witnesses).
 *
 *   scc K F_BITSET OUT_SCC_BITSET OUT_DIST w0_0 ... w0_{K-1}
 *
 * SCC(w0) = F ∩ Bwd(w0), where Bwd(w0) = { x : w0 reachable from x }  (computed by
 * repeated sweeps "mark x if some successor of x is marked" until a fixpoint; F must be
 * Fwd(w0) for this to be the SCC).
 * OUT_DIST: one byte per word code, forward BFS distance from w0 (255 = unreached / >= 255).
 * Prints: K |F| |SCC| sweeps maxdist
 * Build: cc -O3 -march=native -o scc scc.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int K;
static uint64_t P19[16];
static inline void decode(uint64_t c, int *w) { for (int i = 0; i < K; i++) { w[i] = (int)(c % 19); c /= 19; } }
static inline uint64_t encode(const int *w) { uint64_t c = 0; for (int i = K - 1; i >= 0; i--) c = c * 19 + (uint64_t)w[i]; return c; }
static inline void fwd(const int *w, int e, int *out) {
    int lo[16], hi[16], x = 0, c = e;
    for (int i = 0; i < K; i++) { int s = w[i] + x; lo[i] = s % 10; x = s / 10; }
    for (int i = K - 1; i >= 0; i--) { int s = w[i] + c; hi[i] = s % 10; c = s / 10; }
    if (c == 0) { for (int i = 0; i < K; i++) out[i] = lo[i] + hi[i]; }
    else { out[0] = lo[0] + 1; for (int i = 1; i < K; i++) out[i] = lo[i] + hi[i - 1]; }
}
static inline int get(const uint64_t *b, uint64_t c) { return (b[c >> 6] >> (c & 63)) & 1; }
static inline void set(uint64_t *b, uint64_t c) { b[c >> 6] |= 1ULL << (c & 63); }

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage\n"); return 1; }
    K = atoi(argv[1]);
    if (argc != 5 + K) { fprintf(stderr, "word\n"); return 1; }
    P19[0] = 1; for (int i = 1; i < 16; i++) P19[i] = P19[i - 1] * 19;
    uint64_t N = P19[K], nw = (N + 63) / 64;
    uint64_t *F = calloc(nw, 8), *B = calloc(nw, 8);
    FILE *f = fopen(argv[2], "rb");
    if (!F || !B || !f || fread(F, 8, nw, f) != nw) { fprintf(stderr, "load\n"); return 1; }
    fclose(f);
    int w0[16]; for (int i = 0; i < K; i++) w0[i] = atoi(argv[5 + i]);
    uint64_t c0 = encode(w0);
    if (!get(F, c0)) { fprintf(stderr, "w0 not in F\n"); return 1; }
    set(B, c0);
    int w[16], a[16], b[16];
    int sweeps = 0, changed = 1;
    while (changed) {
        changed = 0; sweeps++;
        for (uint64_t j = 0; j < nw; j++) {
            uint64_t x = F[j] & ~B[j];
            while (x) {
                int bit = __builtin_ctzll(x); x &= x - 1;
                uint64_t c = (j << 6) | (uint64_t)bit;
                decode(c, w); fwd(w, 0, a); fwd(w, 1, b);
                if (get(B, encode(a)) || get(B, encode(b))) { set(B, c); changed = 1; }
            }
        }
    }
    uint64_t nF = 0, nS = 0;
    for (uint64_t j = 0; j < nw; j++) { nF += __builtin_popcountll(F[j]); nS += __builtin_popcountll(F[j] & B[j]); B[j] &= F[j]; }
    f = fopen(argv[3], "wb"); fwrite(B, 8, nw, f); fclose(f);
    free(B);
    /* forward BFS distances from w0 */
    uint8_t *dist = malloc(N);
    memset(dist, 255, N);
    uint64_t *cur = calloc(nw, 8), *nxt = calloc(nw, 8);
    dist[c0] = 0; set(cur, c0);
    int d = 0, any = 1;
    while (any && d < 254) {
        any = 0; memset(nxt, 0, nw * 8);
        for (uint64_t j = 0; j < nw; j++) {
            uint64_t x = cur[j];
            while (x) {
                int bit = __builtin_ctzll(x); x &= x - 1;
                decode((j << 6) | (uint64_t)bit, w);
                for (int e = 0; e < 2; e++) {
                    fwd(w, e, a); uint64_t c = encode(a);
                    if (dist[c] == 255) { dist[c] = (uint8_t)(d + 1); set(nxt, c); any = 1; }
                }
            }
        }
        uint64_t *t = cur; cur = nxt; nxt = t; if (any) d++;
    }
    f = fopen(argv[4], "wb"); fwrite(dist, 1, N, f); fclose(f);
    printf("%d %llu %llu %d %d\n", K, (unsigned long long)nF, (unsigned long long)nS, sweeps, d);
    return 0;
}
