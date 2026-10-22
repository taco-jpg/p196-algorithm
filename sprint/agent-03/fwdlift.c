/* fwdlift.c -- forward closure at width K+1, indexed through the width-K closure.
 *
 * The width-(K+1) abstraction refines width K: the first K entries of a reachable
 * (K+1)-word form a reachable K-word (pi_K(F_{K+1}) ⊆ F_K; asserted at run time).
 * So a (K+1)-word v is stored at index  rank_K(code(v[0..K-1])) * 19 + v[K],
 * where rank_K counts the set bits of the width-K closure F_K below the code.
 * Memory: |F_K| bitset (19^K bits) + rank directory + 2 * 19*|F_K| bits.
 *
 * Usage: [QUERY="q_0 .. q_K"] fwdlift K FK_BITSET LIST4_OUT w0_0 ... w0_K   (K+1 entries for the start word)
 *        QUERY: optionally report whether the (K+1)-word q is in the computed closure
 * Prints |F_{K+1}|, |pi_K F_{K+1}|, passes, and for prefix lengths j = 1..min(K+1,6) the number
 * of j-digit prefixes p (p[0] >= 1, noOverflowPre) with no (K+1)-digit digit-extension in F_{K+1};
 * the excluded 4-digit prefixes are written to LIST4_OUT.
 * Build: cc -O3 -march=native -o fwdlift fwdlift.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

static int K, K1;
static uint64_t P19[17], P10[17];
static uint64_t *F, nwF;          /* width-K closure bitset */
static uint64_t *super;           /* cumulative popcount before each 512-bit superblock */

static inline int getF(uint64_t c) { return (F[c >> 6] >> (c & 63)) & 1; }
static inline uint64_t rankF(uint64_t c) {   /* number of set bits of F with index < c */
    uint64_t sb = c >> 9, r = super[sb];
    uint64_t w = sb << 3, wc = c >> 6;
    for (; w < wc; w++) r += __builtin_popcountll(F[w]);
    uint64_t m = (c & 63) ? (F[wc] & ((1ULL << (c & 63)) - 1)) : 0;
    return r + __builtin_popcountll(m);
}
static inline void fwd(const int *w, int e, int *out, int n) {
    int lo[17], hi[17], x = 0, c = e;
    for (int i = 0; i < n; i++) { int s = w[i] + x; lo[i] = s % 10; x = s / 10; }
    for (int i = n - 1; i >= 0; i--) { int s = w[i] + c; hi[i] = s % 10; c = s / 10; }
    if (c == 0) { for (int i = 0; i < n; i++) out[i] = lo[i] + hi[i]; }
    else { out[0] = lo[0] + 1; for (int i = 1; i < n; i++) out[i] = lo[i] + hi[i - 1]; }
}
static inline uint64_t codeK(const int *w) { uint64_t c = 0; for (int i = K - 1; i >= 0; i--) c = c * 19 + (uint64_t)w[i]; return c; }

static uint64_t *vis, *fr, nidx, nwI;
static inline int getb(const uint64_t *b, uint64_t i) { return (b[i >> 6] >> (i & 63)) & 1; }
static inline void setb(uint64_t *b, uint64_t i) { b[i >> 6] |= 1ULL << (i & 63); }

static inline uint64_t indexOf(const int *v) {
    uint64_t c = codeK(v);
    if (!getF(c)) { fprintf(stderr, "refinement violated: prefix not in F_K\n"); exit(2); }
    return rankF(c) * 19 + (uint64_t)v[K];
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage\n"); return 1; }
    K = atoi(argv[1]); K1 = K + 1;
    if (argc != 4 + K1) { fprintf(stderr, "need %d start entries\n", K1); return 1; }
    P19[0] = P10[0] = 1; for (int i = 1; i < 17; i++) { P19[i] = P19[i - 1] * 19; P10[i] = P10[i - 1] * 10; }
    nwF = (P19[K] + 63) / 64;
    uint64_t nwF8 = (nwF + 7) & ~7ULL;
    F = calloc(nwF8, 8);
    FILE *f = fopen(argv[2], "rb");
    if (!F || !f || fread(F, 8, nwF, f) != nwF) { fprintf(stderr, "load F\n"); return 1; }
    fclose(f);
    uint64_t nsb = nwF8 / 8 + 1;
    super = calloc(nsb, 8);
    uint64_t acc = 0;
    for (uint64_t s = 0; s < nsb; s++) { super[s] = acc; if (s < nwF8 / 8) for (int j = 0; j < 8; j++) acc += __builtin_popcountll(F[s * 8 + j]); }
    uint64_t nF = acc;
    nidx = nF * 19; nwI = (nidx + 63) / 64;
    vis = calloc(nwI, 8); fr = calloc(nwI, 8);
    if (!vis || !fr) { fprintf(stderr, "alloc idx\n"); return 1; }
    int w0[17]; for (int i = 0; i < K1; i++) w0[i] = atoi(argv[4 + i]);
    clock_t t0 = clock();
    uint64_t s0 = indexOf(w0);
    setb(vis, s0); setb(fr, s0);
    uint64_t reach = 1; int passes = 0, changed = 1;
    int w[17], v[17];
    while (changed) {
        changed = 0; passes++;
        uint64_t r = 0;                              /* rank of the current prefix */
        for (uint64_t j = 0; j < nwF; j++) {
            uint64_t x = F[j];
            while (x) {
                int bit = __builtin_ctzll(x); x &= x - 1;
                uint64_t base = r * 19; r++;
                /* any frontier bit in [base, base+19)? */
                uint64_t lo = base >> 6, hi = (base + 18) >> 6;
                uint64_t m = fr[lo] >> (base & 63);
                if (hi != lo) m |= fr[hi] << (64 - (base & 63));
                m &= (1ULL << 19) - 1;
                if (!m) continue;
                uint64_t c = (j << 6) | (uint64_t)bit;
                for (int i = 0; i < K; i++) { w[i] = (int)(c % 19); c /= 19; }
                while (m) {
                    int last = __builtin_ctzll(m); m &= m - 1;
                    uint64_t idx = base + (uint64_t)last;
                    fr[idx >> 6] &= ~(1ULL << (idx & 63));
                    w[K] = last;
                    for (int e = 0; e < 2; e++) {
                        fwd(w, e, v, K1);
                        uint64_t i2 = indexOf(v);
                        if (!getb(vis, i2)) {
                            setb(vis, i2); setb(fr, i2); reach++;
                            if (i2 < base + 19) changed = 1;   /* at or behind the scan position */
                        }
                    }
                }
            }
        }
    }
    double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
    /* projection count */
    uint64_t proj = 0;
    for (uint64_t r = 0; r < nF; r++) {
        uint64_t base = r * 19, lo = base >> 6, hi = (base + 18) >> 6;
        uint64_t m = vis[lo] >> (base & 63);
        if (hi != lo) m |= vis[hi] << (64 - (base & 63));
        if (m & ((1ULL << 19) - 1)) proj++;
    }
    printf("K+1=%d |F_K|=%llu |F_K+1|=%llu |pi_K F_K+1|=%llu passes=%d bfs_secs=%.1f\n", K1,
           (unsigned long long)nF, (unsigned long long)reach, (unsigned long long)proj, passes, secs);
    /* optional membership query: env QUERY="q_0 ... q_K" */
    const char *qs = getenv("QUERY");
    if (qs) {
        int q[17], n = 0; char *end; const char *pp = qs;
        while (n < K1) { long val = strtol(pp, &end, 10); if (end == pp) break; q[n++] = (int)val; pp = end; }
        if (n == K1) {
            uint64_t c = codeK(q);
            int in = getF(c) && getb(vis, rankF(c) * 19 + (uint64_t)q[K]);
            printf("QUERY %s : %s\n", qs, in ? "IN closure" : "NOT in closure");
        }
    }
    fflush(stdout);
    /* excluded prefixes: hit[j][p] = some digit-extension of p is in F_{K+1} */
    int JM = K1 < 6 ? K1 : 6;
    uint8_t *hit[7];
    for (int j = 1; j <= JM; j++) hit[j] = calloc(P10[j], 1);
    for (uint64_t n = P10[K1 - 1]; n < P10[K1]; n++) {
        uint64_t x = n;
        for (int i = K1 - 1; i >= 0; i--) { w[i] = (int)(x % 10); x /= 10; }
        uint64_t c = codeK(w);
        if (!getF(c)) continue;
        uint64_t idx = rankF(c) * 19 + (uint64_t)w[K];
        if (getb(vis, idx)) for (int j = 1; j <= JM; j++) hit[j][n / P10[K1 - j]] = 1;
    }
    FILE *list = fopen(argv[3], "w");
    for (int j = 1; j <= JM; j++) {
        uint64_t cnt = 0;
        for (uint64_t p = P10[j - 1]; p < P10[j]; p++) {
            int pd[17]; uint64_t x = p; for (int i = j - 1; i >= 0; i--) { pd[i] = (int)(x % 10); x /= 10; }
            int noov = pd[0] >= 2; for (int i = 0; i < j; i++) if (pd[i] >= 3) noov = 1;
            if (!noov) continue;
            if (!hit[j][p]) { cnt++; if (j == 4 && list) fprintf(list, "%llu\n", (unsigned long long)p); }
        }
        printf("K=%d prefix_len=%d excluded=%llu\n", K1, j, (unsigned long long)cnt);
    }
    if (list) fclose(list);
    return 0;
}
