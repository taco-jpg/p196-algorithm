/* Agent #101: complete exterior graph (c,B), c in {2,4,...,16}, B canonical
   trimmed (B empty, or B[0] in 1..18, coefficients 0..18, B[last] != c),
   |B| <= L.  Reports state count, internal edges, directed cycles, and the
   maximum first-exit time (number of steps up to and including the step that
   leaves the cap).  Usage: ./exterior_cap L                                   */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static int L;
static uint64_t pw[16], off[16], per_phase;
static const int PH[8] = {2,4,6,8,10,12,14,16};
static int phidx(int c){ return c/2 - 1; }

static uint64_t encode(int c, const int *B, int b){
    uint64_t x = 0;
    for (int i = b-1; i >= 0; i--) x = x*19 + B[i];
    return (uint64_t)phidx(c)*per_phase + off[b] + x;
}
static void decode(uint64_t id, int *c, int *B, int *b){
    int p = id / per_phase; uint64_t r = id % per_phase;
    *c = PH[p];
    int bb = 0; while (bb < L && r >= off[bb+1]) bb++;
    r -= off[bb];
    for (int i = 0; i < bb; i++){ B[i] = r % 19; r /= 19; }
    *b = bb;
}
static int valid(int c, const int *B, int b){
    if (b == 0) return 1;
    if (B[0] == 0) return 0;
    if (B[b-1] == c) return 0;
    return 1;
}
/* returns new length (may exceed L -> exit), writes c',B',gamma */
static int step(int c, const int *B, int b, int *cp, int *Bp, int *gam){
    int k = c >= 10, t = c - 9*k;
    int DB[20], DRB[20], e = 0;
    for (int i = 0; i < b; i++){ int s = B[i] + e; DB[i] = s%10; e = s/10; }
    int u0 = c + e - 10*k;
    e = k;
    for (int i = 0; i < b; i++){ int s = B[b-1-i] + e; DRB[i] = s%10; e = s/10; }
    int g = e;
    int left[21], right[21], n = b+1;
    for (int i = 0; i < b; i++) left[i] = DB[i];
    left[b] = u0;
    if (g == 0){ for (int i = 0; i < b; i++) right[i] = DRB[b-1-i]; right[b] = t; }
    else       { right[0] = 1; for (int i = 0; i < b; i++) right[i+1] = DRB[b-1-i]; }
    *cp = 2*t;
    for (int i = 0; i < n; i++) Bp[i] = left[i] + right[i];
    while (n > 0 && Bp[n-1] == *cp) n--;
    *gam = g;
    return n;
}

int main(int argc, char **argv){
    L = atoi(argv[1]);
    pw[0] = 1; for (int i = 1; i < 16; i++) pw[i] = pw[i-1]*19;
    off[0] = 0; for (int i = 1; i <= L+1; i++) off[i] = off[i-1] + pw[i-1];
    per_phase = off[L+1];
    uint64_t total = 8*per_phase;
    /* tim: 0 unknown, 254 in-progress, 255 invalid slot, else exit time */
    uint8_t *tim = calloc(total, 1);
    uint64_t *stack = malloc(sizeof(uint64_t) * 1000000);
    uint64_t states = 0, internal = 0, cycles = 0, gamma_edges = 0;
    int maxT = 0; uint64_t argmax = 0;
    int B[20], Bp[24], b, c, cp, gam;
    for (uint64_t id = 0; id < total; id++){
        decode(id, &c, B, &b);
        if (!valid(c, B, b)) { tim[id] = 255; continue; }
        states++;
        int nb = step(c, B, b, &cp, Bp, &gam);
        if (nb <= L) internal++;
    }
    for (uint64_t id = 0; id < total; id++){
        if (tim[id]) continue;
        size_t sp = 0; uint64_t cur = id; int base;
        for (;;){
            if (tim[cur] == 254){ cycles++; base = 0; break; }
            if (tim[cur]) { base = tim[cur]; break; }
            tim[cur] = 254; stack[sp++] = cur;
            decode(cur, &c, B, &b);
            int nb = step(c, B, b, &cp, Bp, &gam);
            if (nb > L){ base = 0; break; }      /* exits */
            cur = encode(cp, Bp, nb);
            if (tim[cur] == 255){ fprintf(stderr,"invalid successor!\n"); return 2; }
        }
        if (cycles){ fprintf(stderr, "CYCLE detected at start id %llu\n",(unsigned long long)id); }
        while (sp){
            uint64_t s = stack[--sp];
            int T = base + 1; if (T > 250) { fprintf(stderr,"time overflow\n"); return 3; }
            tim[s] = T; base = T;
            if (T > maxT){ maxT = T; argmax = s; }
        }
    }
    decode(argmax, &c, B, &b);
    printf("cap=%d states=%llu internal_edges=%llu exit_edges=%llu cycles=%llu max_exit_time=%d  argmax c=%d B=(",
        L,(unsigned long long)states,(unsigned long long)internal,
        (unsigned long long)(states-internal),(unsigned long long)cycles,maxT,c);
    for (int i = 0; i < b; i++) printf(i?",%d":"%d", B[i]);
    printf(")\n");
    /* count how many states attain maxT */
    uint64_t nmax = 0; for (uint64_t id=0; id<total; id++) if (tim[id]==maxT) nmax++;
    printf("  states attaining max: %llu\n",(unsigned long long)nmax);
    return 0;
}
