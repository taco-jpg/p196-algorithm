/* peel.c -- infinite-rank region of the full width-K long-word graph.
 *
 * Nodes: all words w of length K with entries 0..18 and w[0] >= 1.
 * Edges: w -> forwardPrefix(w, e), e in {0,1} (multi-edges counted once).
 * Repeatedly delete nodes of in-degree 0 (Kahn peeling). A node survives iff it has
 * backward paths of every length, i.e. iff its backward closure contains a cycle
 * (equivalently it is forward-reachable from a cycle).  This is exactly the set of
 * words on which the backward rank certificate (Agent124 framework) cannot exist.
 * The deletion round of a deleted node is its rank (length of the longest backward path).
 *
 * Usage: peel K OUT_BITSET
 * Prints: K nodes survivors max_rank rank_histogram...
 * Build: cc -O3 -march=native -o peel peel.c
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
/* distinct successors of node c; returns count (1 or 2) */
static inline int succ(uint64_t c, uint64_t *s) {
    int w[16], a[16], b[16];
    decode(c, w); fwd(w, 0, a); fwd(w, 1, b);
    s[0] = encode(a); s[1] = encode(b);
    return s[0] == s[1] ? 1 : 2;
}

int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: %s K OUT\n", argv[0]); return 1; }
    K = atoi(argv[1]);
    P19[0] = 1; for (int i = 1; i < 16; i++) P19[i] = P19[i - 1] * 19;
    uint64_t N = P19[K];
    uint16_t *indeg = calloc(N, 2);     /* in-degree; overflow is checked below */
    uint64_t nw = (N + 63) / 64;
    uint64_t *alive = calloc(nw, 8), *cur = calloc(nw, 8), *nxt = calloc(nw, 8);
    if (!indeg || !alive || !cur || !nxt) { fprintf(stderr, "alloc\n"); return 1; }
    uint64_t nodes = 0;
    for (uint64_t c = 0; c < N; c++) if (c % 19 != 0) { alive[c >> 6] |= 1ULL << (c & 63); nodes++; }
    uint64_t s[2];
    for (uint64_t c = 0; c < N; c++) {
        if (c % 19 == 0) continue;
        int n = succ(c, s);
        for (int i = 0; i < n; i++) {
            if (s[i] % 19 == 0) { fprintf(stderr, "successor with zero head\n"); return 1; }
            if (indeg[s[i]] == 65535) { fprintf(stderr, "indegree overflow\n"); return 1; }
            indeg[s[i]]++;
        }
    }
    /* round 0: nodes with in-degree 0 */
    uint64_t hist[4096] = {0}; int round = 0; uint64_t removed = 0, layer = 0;
    for (uint64_t c = 0; c < N; c++) if (c % 19 != 0 && indeg[c] == 0) { cur[c >> 6] |= 1ULL << (c & 63); layer++; }
    while (layer) {
        hist[round < 4095 ? round : 4095] += layer; removed += layer;
        memset(nxt, 0, nw * 8); uint64_t nl = 0;
        for (uint64_t j = 0; j < nw; j++) {
            uint64_t x = cur[j];
            while (x) {
                int bit = __builtin_ctzll(x); x &= x - 1;
                uint64_t c = (j << 6) | (uint64_t)bit;
                alive[c >> 6] &= ~(1ULL << (c & 63));
                int n = succ(c, s);
                for (int i = 0; i < n; i++) if (--indeg[s[i]] == 0) { nxt[s[i] >> 6] |= 1ULL << (s[i] & 63); nl++; }
            }
        }
        uint64_t *t = cur; cur = nxt; nxt = t; layer = nl; round++;
    }
    printf("K=%d nodes=%llu survivors=%llu max_rank=%d\nrank_hist:", K, (unsigned long long)nodes,
           (unsigned long long)(nodes - removed), round - 1);
    for (int r = 0; r < round && r < 4096; r++) printf(" %llu", (unsigned long long)hist[r]);
    printf("\n");
    FILE *f = fopen(argv[2], "wb"); fwrite(alive, 8, nw, f); fclose(f);
    return 0;
}
