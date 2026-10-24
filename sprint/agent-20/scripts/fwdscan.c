/* Forward falsification scan for prefix ancestry bounds.
 *
 * For every seed A in [lo, hi) (or every seed read from stdin with -s), iterate
 * reverse-and-add for t = 1..T and, at EVERY time t at which orbit(A,t) is a
 * palindrome, record its leading 2-, 3- and 4-digit prefix together with t.
 * Output (stdout): one line per prefix that was hit:
 *     prefix  maxT  seed_of_maxT  hits
 * The Lean endpoints claim  orbit A t = P, P palindrome with prefix p  ==>  t <= bound(p)+1
 * (resp. t <= B for the 2/3-digit endpoints); compare with compare_fwd.py.
 *
 * Build: cc -O3 -o fwdscan fwdscan.c
 * Usage: ./fwdscan LO HI T        (seeds LO..HI-1, decimal, fit in uint64)
 *        ./fwdscan -s T < seeds    (one decimal seed per line, any length)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXD 1200
static long long maxT[3][10000];
static char seedOf[3][10000][64];
static long long hits[3][10000];

static int load_u64(uint64_t s, unsigned char *d) {
    int L = 0;
    while (s) { d[L++] = (unsigned char)(s % 10); s /= 10; }
    return L;
}

static int load_str(const char *str, unsigned char *d) {
    int n = (int)strlen(str);
    while (n > 0 && (str[n-1] < '0' || str[n-1] > '9')) n--;
    int L = 0;
    for (int i = n - 1; i >= 0; i--) d[L++] = (unsigned char)(str[i] - '0');
    while (L > 1 && d[L-1] == 0) L--;
    return L;
}

static inline int is_pal(const unsigned char *d, int L) {
    for (int i = 0, j = L - 1; i < j; i++, j--) if (d[i] != d[j]) return 0;
    return 1;
}

/* one step in place: d <- d + reverse(d); digits LSB first */
static inline int step(unsigned char *d, int L, unsigned char *tmp) {
    int c = 0;
    for (int i = 0; i < L; i++) {
        int s = d[i] + d[L-1-i] + c;
        if (s >= 10) { tmp[i] = (unsigned char)(s - 10); c = 1; } else { tmp[i] = (unsigned char)s; c = 0; }
    }
    if (c) tmp[L++] = 1;
    memcpy(d, tmp, (size_t)L);
    return L;
}

static void record(const unsigned char *d, int L, long long t, const char *seed) {
    for (int k = 2; k <= 4; k++) {
        if (L < k) break;
        int p = 0;
        for (int i = 0; i < k; i++) p = p * 10 + d[L-1-i];
        hits[k-2][p]++;
        if (t > maxT[k-2][p]) {
            maxT[k-2][p] = t;
            strncpy(seedOf[k-2][p], seed, 63);
        }
    }
}

static void run(unsigned char *d, int L, int T, const char *seed, unsigned char *tmp) {
    for (int t = 1; t <= T; t++) {
        if (L + 2 >= MAXD) break;
        L = step(d, L, tmp);
        if (is_pal(d, L)) record(d, L, t, seed);
    }
}

int main(int argc, char **argv) {
    static unsigned char d[MAXD], tmp[MAXD];
    char seed[64];
    if (argc == 3 && strcmp(argv[1], "-s") == 0) {
        int T = atoi(argv[2]);
        char line[256];
        while (fgets(line, sizeof line, stdin)) {
            if (line[0] < '0' || line[0] > '9') continue;
            int L = load_str(line, d);
            snprintf(seed, sizeof seed, "%.*s", (int)strcspn(line, "\r\n \t"), line);
            run(d, L, T, seed, tmp);
        }
    } else if (argc == 4) {
        uint64_t lo = strtoull(argv[1], 0, 10), hi = strtoull(argv[2], 0, 10);
        int T = atoi(argv[3]);
        for (uint64_t s = lo; s < hi; s++) {
            int L = load_u64(s, d);
            snprintf(seed, sizeof seed, "%llu", (unsigned long long)s);
            run(d, L, T, seed, tmp);
        }
    } else {
        fprintf(stderr, "usage: %s LO HI T | -s T < seeds\n", argv[0]);
        return 2;
    }
    for (int k = 2; k <= 4; k++) {
        int lo = 1, hi = 10; for (int i = 1; i < k; i++) { lo *= 10; hi *= 10; }
        for (int p = lo; p < hi; p++)
            if (hits[k-2][p]) printf("%d %lld %s %lld\n", p, maxT[k-2][p], seedOf[k-2][p], hits[k-2][p]);
    }
    return 0;
}
