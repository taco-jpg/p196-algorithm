/* settool.c -- operations on word-set bitsets written by fwdbfs.c (bit index = word code,
 * code(w) = sum_i w[i]*19^i, w[0] = outermost column sum).
 *
 *   settool proj IN K OUT     project a width-K set onto its first K-1 entries (code mod 19^(K-1))
 *   settool diff A B K        print |A| |B| |A\B| |B\A|
 *   settool excl IN K [LIST4] for each prefix length j = 1..K print the number of j-digit prefixes p
 *                             (digits <= 9, p[0] >= 1, noOverflowPre(p)) all of whose K-digit digit
 *                             extensions are outside the set; optionally write the excluded 4-digit
 *                             prefixes (j = 4) to LIST4, one per line.
 * Build: cc -O3 -march=native -o settool settool.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static uint64_t P19[16];

static uint64_t *load(const char *path, int K, uint64_t *nw) {
    *nw = (P19[K] + 63) / 64;
    uint64_t *b = calloc(*nw, 8);
    FILE *f = fopen(path, "rb");
    if (!b || !f || fread(b, 8, *nw, f) != *nw) { fprintf(stderr, "load %s\n", path); exit(1); }
    fclose(f);
    return b;
}
static inline int get(const uint64_t *b, uint64_t c) { return (b[c >> 6] >> (c & 63)) & 1; }
static uint64_t popcnt(const uint64_t *b, uint64_t nw) { uint64_t s = 0; for (uint64_t i = 0; i < nw; i++) s += __builtin_popcountll(b[i]); return s; }

static int noOverflowPre(const int *p, int j) {
    if (p[0] >= 2) return 1;
    for (int i = 0; i < j; i++) if (p[i] >= 3) return 1;
    return 0;
}

int main(int argc, char **argv) {
    P19[0] = 1; for (int i = 1; i < 16; i++) P19[i] = P19[i - 1] * 19;
    if (argc >= 5 && !strcmp(argv[1], "proj")) {
        int K = atoi(argv[3]); uint64_t nw; uint64_t *a = load(argv[2], K, &nw);
        uint64_t ow = (P19[K - 1] + 63) / 64; uint64_t *o = calloc(ow, 8);
        for (uint64_t j = 0; j < nw; j++) { uint64_t x = a[j]; while (x) { int bit = __builtin_ctzll(x); x &= x - 1;
            uint64_t c = ((j << 6) | (uint64_t)bit) % P19[K - 1]; o[c >> 6] |= 1ULL << (c & 63); } }
        FILE *f = fopen(argv[4], "wb"); fwrite(o, 8, ow, f); fclose(f);
        printf("proj %s K=%d -> %llu words at K=%d\n", argv[2], K, (unsigned long long)popcnt(o, ow), K - 1);
        return 0;
    }
    if (argc >= 5 && !strcmp(argv[1], "diff")) {
        int K = atoi(argv[4]); uint64_t nw; uint64_t *a = load(argv[2], K, &nw), *b = load(argv[3], K, &nw);
        uint64_t ab = 0, ba = 0;
        for (uint64_t i = 0; i < nw; i++) { ab += __builtin_popcountll(a[i] & ~b[i]); ba += __builtin_popcountll(b[i] & ~a[i]); }
        printf("|A|=%llu |B|=%llu |A\\B|=%llu |B\\A|=%llu\n", (unsigned long long)popcnt(a, nw),
               (unsigned long long)popcnt(b, nw), (unsigned long long)ab, (unsigned long long)ba);
        return 0;
    }
    if (argc >= 4 && !strcmp(argv[1], "excl")) {
        int K = atoi(argv[3]); uint64_t nw; uint64_t *a = load(argv[2], K, &nw);
        FILE *list = argc >= 5 ? fopen(argv[4], "w") : NULL;
        /* inside[j][p] = 1 if some K-digit digit-extension of the j-digit prefix p is in the set */
        uint64_t P10[16]; P10[0] = 1; for (int i = 1; i < 16; i++) P10[i] = P10[i - 1] * 10;
        uint8_t *hit = calloc(P10[K], 1);
        int w[16];
        for (uint64_t n = 0; n < P10[K]; n++) {           /* n = decimal word, most significant digit = w[0] */
            uint64_t x = n; for (int i = K - 1; i >= 0; i--) { w[i] = (int)(x % 10); x /= 10; }
            uint64_t c = 0; for (int i = K - 1; i >= 0; i--) c = c * 19 + (uint64_t)w[i];
            hit[n] = (uint8_t)get(a, c);
        }
        for (int j = K; j >= 1; j--) {
            uint64_t cnt = 0;
            for (uint64_t p = P10[j - 1]; p < P10[j]; p++) {     /* leading digit >= 1 */
                int pd[16]; uint64_t x = p; for (int i = j - 1; i >= 0; i--) { pd[i] = (int)(x % 10); x /= 10; }
                if (!noOverflowPre(pd, j)) continue;
                int any = 0;
                for (uint64_t s = 0; s < P10[K - j] && !any; s++) if (hit[p * P10[K - j] + s]) any = 1;
                if (!any) { cnt++; if (list && j == 4) fprintf(list, "%llu\n", (unsigned long long)p); }
            }
            printf("K=%d prefix_len=%d excluded=%llu\n", K, j, (unsigned long long)cnt);
        }
        if (list) fclose(list);
        return 0;
    }
    fprintf(stderr, "usage: see header\n");
    return 1;
}
