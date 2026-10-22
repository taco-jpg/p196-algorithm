/* orbit196.c -- iterate reverse-and-add from 196 and record, for every time t,
 * the data the k-column abstraction sees (k = 1..KMAX):
 *
 *   t  L  ovf  r99  pal  q_0..q_{KMAX-1}  e_1..e_KMAX
 *
 * L     : number of decimal digits of orbit(196,t)
 * ovf   : 1 if orbit(196,t+1) has L+1 digits (final carry c_L of the addition), else 0
 * r99   : orbit(196,t) mod 99
 * pal   : 1 if orbit(196,t) is a palindrome
 * q_i   : column sum d_i + d_{L-1-i} (outer columns, i < KMAX)
 * e_k   : actual inner carry c_{L-k} of the addition n + rev(n)  (the value the
 *         abstraction treats as free), for k = 1..KMAX
 *
 * Usage: orbit196 T [every]      prints rows for t = 0..T with t % every == 0 (default every=1)
 * Build: cc -O2 -o orbit196 orbit196.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define KMAX 12

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s T [every]\n", argv[0]); return 1; }
    long T = atol(argv[1]);
    long every = argc > 2 ? atol(argv[2]) : 1;
    size_t cap = (size_t)(T * 0.42) + 64;  /* length grows ~0.4142 digits/step */
    uint8_t *d = calloc(cap, 1), *o = calloc(cap, 1);
    uint8_t *cin = calloc(cap + 1, 1);     /* carry into column i */
    if (!d || !o || !cin) { fprintf(stderr, "alloc\n"); return 1; }
    long L = 3; d[0] = 6; d[1] = 9; d[2] = 1; /* 196, least significant first */
    for (long t = 0; t <= T; t++) {
        if ((size_t)L + 2 >= cap) { fprintf(stderr, "capacity exceeded at t=%ld\n", t); return 1; }
        /* addition with carries */
        cin[0] = 0;
        for (long i = 0; i < L; i++) {
            int s = d[i] + d[L - 1 - i] + cin[i];
            o[i] = (uint8_t)(s % 10);
            cin[i + 1] = (uint8_t)(s / 10);
        }
        int ovf = cin[L];
        if (t % every == 0) {
            int pal = 1;
            for (long i = 0; i < L / 2; i++) if (d[i] != d[L - 1 - i]) { pal = 0; break; }
            /* n mod 99: 100 = 1 mod 99, so sum two-digit chunks */
            long r = 0;
            for (long i = 0; i < L; i += 2) {
                r += d[i] + (i + 1 < L ? 10 * d[i + 1] : 0);
                if (r > 1000000000L) r %= 99;
            }
            r %= 99;
            printf("%ld %ld %d %ld %d", t, L, ovf, r, pal);
            for (int i = 0; i < KMAX; i++) printf(" %d", i < L ? d[i] + d[L - 1 - i] : -1);
            for (int k = 1; k <= KMAX; k++) printf(" %d", k <= L ? cin[L - k] : -1);
            printf("\n");
        }
        if (ovf) { o[L] = 1; L++; }
        uint8_t *tmp = d; d = o; o = tmp;
    }
    free(d); free(o); free(cin);
    return 0;
}
