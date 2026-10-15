/* Independent exact ancestry-depth DP (arithmetic reversal), up to LIMIT.
   depth[T(n)] = max(depth[T(n)], depth[n]+1), n increasing (T(n) > n).
   Reports, for each of the 13 prefixes, #palindromes, max depth, argmax,
   and any violation of the claimed bound. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static uint64_t rev(uint64_t n) { uint64_t r = 0; while (n) { r = r * 10 + n % 10; n /= 10; } return r; }

int main(int argc, char **argv) {
    uint64_t LIMIT = argc > 1 ? strtoull(argv[1], 0, 10) : 1000000000ULL;
    uint8_t *depth = calloc(LIMIT, 1);
    if (!depth) { perror("calloc"); return 1; }
    int pa[13] = {1,2,3,4,4,6,6,6,7,8,8,8,8};
    int pb[13] = {0,0,2,0,1,0,4,5,6,0,1,2,3};
    int bd[13] = {1,2,2,3,3,3,3,6,3,4,4,4,4};
    int idx[100]; for (int i = 0; i < 100; i++) idx[i] = -1;
    for (int j = 0; j < 13; j++) idx[pa[j] * 10 + pb[j]] = j;
    uint64_t cnt[13] = {0}, arg[13] = {0}; int mx[13]; for (int j = 0; j < 13; j++) mx[j] = -1;
    uint64_t hist[13][32] = {{0}};
    uint64_t viol = 0; int gmax = 0;
    for (uint64_t n = 1; n < LIMIT; n++) {
        uint64_t r = rev(n);
        if (r == n && n >= 10) {
            uint64_t p = n; while (p >= 100) p /= 10;
            int j = idx[p];
            if (j >= 0) {
                int d = depth[n];
                cnt[j]++; hist[j][d]++;
                if (d > mx[j]) { mx[j] = d; arg[j] = n; }
                if (d > bd[j]) { viol++; if (viol < 20) printf("VIOLATION %d%d n=%llu d=%d\n", pa[j], pb[j], (unsigned long long)n, d); }
            }
        }
        uint64_t v = n + r;
        if (v < LIMIT) { int dn = depth[n] + 1; if (dn > depth[v]) depth[v] = dn; }
        if (depth[n] > gmax) gmax = depth[n];
    }
    printf("LIMIT=%llu\n", (unsigned long long)LIMIT);
    for (int j = 0; j < 13; j++) {
        printf("  %d%d bound=%d count=%llu maxDepth=%d firstArgmax=%llu hist:", pa[j], pb[j], bd[j],
               (unsigned long long)cnt[j], mx[j], (unsigned long long)arg[j]);
        for (int d = 0; d < 32; d++) if (hist[j][d]) printf(" %d:%llu", d, (unsigned long long)hist[j][d]);
        printf("\n");
    }
    printf("violations=%llu globalMaxDepth=%d\n", (unsigned long long)viol, gmax);
    free(depth);
    return 0;
}
