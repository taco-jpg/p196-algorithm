/* Agent 19 review: forward scan used to falsification-test the ancestry bounds and the
 * five-layer obstruction of the reviewed results.
 *
 * For every seed A in [lo, hi) and every time 0 <= t <= T it computes orbit(A, t) exactly
 * (decimal digit arrays). Whenever orbit(A, t) is a palindrome of width >= 3 it records
 * the largest t seen for its 3-digit and 4-digit leading prefixes (and one seed attaining
 * it). It also checks Agent113's OuterPattern (width >= 5, q0 in {10,12,14,16}, q1 = 0,
 * q2 in {0,10,12,14,16}, q3 = 0, where qi = d_i + d_{W-1-i}) at every t >= 5 and prints
 * any hit, which would contradict Agent113.FiveLayer.five_layer_strong.
 *
 * Build:  cc -O2 -o scan scan.c
 * Run:    ./scan lo hi T > out.txt        (seeds lo .. hi-1)
 *         ./scan 0 0 T < seeds.txt > out.txt   (seeds read from stdin, one per line)
 * Output: lines "P3 <prefix> <maxT> <seed>", "P4 <prefix> <maxT> <seed>",
 *         "OUTER <seed> <t>" (should never appear), and a final "DONE ..." line.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXD 512

static int maxt3[1000], seed3[1000];
static long long seed3l[1000];
static int maxt4[10000];
static long long seed4l[10000];

static int is_even_pair(int q) { return q == 0 || q == 10 || q == 12 || q == 14 || q == 16; }

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s lo hi T\n", argv[0]); return 2; }
    long long lo = atoll(argv[1]), hi = atoll(argv[2]);
    int T = atoi(argv[3]);
    memset(maxt3, -1, sizeof maxt3);
    memset(maxt4, -1, sizeof maxt4);
    (void)seed3;
    unsigned char d[MAXD], r[MAXD];
    long long pal_hits = 0, outer_hits = 0;
    int from_stdin = (lo == 0 && hi == 0);
    long long A = lo;
    for (;;) {
        if (from_stdin) { if (scanf("%lld", &A) != 1) break; }
        else if (A >= hi) break;
        int W = 0;
        long long x = A;
        while (x > 0) { d[W++] = (unsigned char)(x % 10); x /= 10; }
        for (int t = 0; t <= T; t++) {
            /* palindrome test */
            int pal = 1;
            for (int i = 0; i < W / 2; i++) if (d[i] != d[W - 1 - i]) { pal = 0; break; }
            if (pal && W >= 3) {
                pal_hits++;
                int p3 = d[W - 1] * 100 + d[W - 2] * 10 + d[W - 3];
                if (t > maxt3[p3]) { maxt3[p3] = t; seed3l[p3] = A; }
                if (W >= 4) {
                    int p4 = p3 * 10 + d[W - 4];
                    if (t > maxt4[p4]) { maxt4[p4] = t; seed4l[p4] = A; }
                }
            }
            if (t >= 5 && W >= 5) {
                int q0 = d[0] + d[W - 1], q1 = d[1] + d[W - 2], q2 = d[2] + d[W - 3], q3 = d[3] + d[W - 4];
                if ((q0 == 10 || q0 == 12 || q0 == 14 || q0 == 16) && q1 == 0 && is_even_pair(q2) && q3 == 0) {
                    outer_hits++;
                    printf("OUTER %lld %d\n", A, t);
                }
            }
            if (t == T) break;
            /* step: d + reverse(d) */
            int c = 0;
            for (int i = 0; i < W; i++) {
                int s = d[i] + d[W - 1 - i] + c;
                r[i] = (unsigned char)(s % 10);
                c = s / 10;
            }
            if (c) r[W++] = 1;
            if (W >= MAXD - 1) { fprintf(stderr, "width overflow\n"); return 1; }
            memcpy(d, r, (size_t)W);
        }
        if (!from_stdin) A++;
    }
    for (int p = 100; p < 1000; p++)
        if (maxt3[p] >= 0) printf("P3 %d %d %lld\n", p, maxt3[p], seed3l[p]);
    for (int p = 1000; p < 10000; p++)
        if (maxt4[p] >= 0) printf("P4 %d %d %lld\n", p, maxt4[p], seed4l[p]);
    printf("DONE lo=%lld hi=%lld T=%d palindrome_hits=%lld outer_hits=%lld\n", lo, hi, T, pal_hits, outer_hits);
    return 0;
}
