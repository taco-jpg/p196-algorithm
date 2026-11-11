// cen3.cpp (r12d: cen2.cpp with the period S = 2 m p K / sum(g) instead of 80K) -- lane-parallel (SIMD over centres) version of p8_centre_exhaust/centre.cpp, generalised to K periods.
// Test per centre C (same index -> C map as centre.cpp):  T^(80K)(P(q0,C)) == P(q0+K,C),
//   P(q,C) = B0 W0^q C rev(W0)^q rev(B0), exact coefficient pairword step (= klib.pairword_step).
// Each lane follows the common clock g_t; a lane whose top carry differs from g_t is flagged and recomputed
// by the scalar reference routine (identical to centre.cpp), so results are exact for every centre.
// usage: cen2 TBL L q0 K threads [lo hi]     (idx range [lo,hi), default all)
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <thread>
#include <atomic>
#include <mutex>
#include <cstdint>
#ifndef FORCEDEV
#define FORCEDEV 0
#endif
#ifndef VW
#define VW 32
#endif
typedef uint8_t u8;
typedef u8 vec __attribute__((vector_size(VW)));
int p, nB, m; int g[8]; std::vector<std::vector<int>> Bt, Wt;
int L, q0, K, NT, S;
const int HN = 2048;  // r12d: 1024 is too small for K=6 (target length ~1170)
struct Stat { uint64_t n=0, ret=0, clockdev=0, lenerr=0, guardfail=0, scalar=0; int maxpre=-1; uint64_t argmax=0; uint64_t hist[HN]={0}; };
std::mutex mu;
static inline int sstep(const u8* a, int n, u8* d, u8* out) {
    int c = 0;
    for (int i = 0; i < n; i++) { int s = a[i] + c; c = s >= 10; d[i] = s - 10*c; }
    int n2 = n; if (c) d[n2++] = 1;
    for (int i = 0; i < n2; i++) out[i] = d[i] + d[n2-1-i];
    return n2;
}
int main(int argc, char** argv) {
    if (argc < 6) { fprintf(stderr, "usage\n"); return 1; }
    FILE* f = fopen(argv[1], "r"); L = atoi(argv[2]); q0 = atoi(argv[3]); K = atoi(argv[4]); NT = atoi(argv[5]);
    if (fscanf(f, "%d %d %d", &p, &nB, &m) != 3) return 1;
    for (int t = 0; t < p; t++) if (fscanf(f, "%d", &g[t]) != 1) return 1;
    { int gs = 0; for (int t = 0; t < p; t++) gs += g[t]; S = 2*m*p*K/gs; }  // r12d: general period (80K for m=20, 192K for m=48)
    Bt.assign(p, std::vector<int>(nB)); Wt.assign(p, std::vector<int>(m));
    for (int t = 0; t < p; t++) for (int x = 0; x < nB; x++) if (fscanf(f, "%d", &Bt[t][x]) != 1) return 1;
    for (int t = 0; t < p; t++) for (int x = 0; x < m; x++) if (fscanf(f, "%d", &Wt[t][x]) != 1) return 1;
    int h = L/2, odd = L % 2;
    uint64_t total = 1; for (int i = 0; i < h; i++) total *= 19; if (odd) total *= 10;
    uint64_t lo = 0, hi = total;
    if (argc > 7) { lo = strtoull(argv[6], 0, 10); hi = strtoull(argv[7], 0, 10); if (hi > total) hi = total; }
    int H0 = nB + m*q0, H1 = nB + m*(q0+K);
    int n0 = 2*H0 + L, nT = 2*H1 + L;
    if (nT >= HN) { fprintf(stderr, "HN too small\n"); return 1; }
    int gsum = 0; for (int t = 0; t < S; t++) gsum += g[t%p];
    if (n0 + gsum != nT) { fprintf(stderr, "clock/length mismatch %d %d %d\n", n0, gsum, nT); return 1; }
    Stat G;
    std::atomic<uint64_t> next(lo);
    const uint64_t CH = 4096;
    auto work = [&]() {
        Stat St;
        std::vector<int> half(H1);
        for (int x = 0; x < H1; x++) half[x] = x < nB ? Bt[0][x] : Wt[0][(x-nB)%m];
        std::vector<u8> base(n0), tgt(nT), rootc(p*(nB+m));
        for (int x = 0; x < H0; x++) { base[x] = half[x]; base[n0-1-x] = half[x]; }
        for (int x = 0; x < H1; x++) { tgt[x] = half[x]; tgt[nT-1-x] = half[x]; }
        for (int t = 0; t < p; t++) for (int x = 0; x < nB+m; x++) rootc[t*(nB+m)+x] = x < nB ? Bt[t][x] : Wt[t][x-nB];
        int NM = nT + 8;
        std::vector<vec> A(NM), Bv(NM), D(NM);
        std::vector<u8> sa(NM+200), sb(NM+200), sd(NM+200), stg(nT);
        memcpy(stg.data(), tgt.data(), nT);
        std::vector<std::vector<int>> Cl(VW, std::vector<int>(L));
        auto centre_of = [&](uint64_t idx, std::vector<int>& C) {
            uint64_t r = idx; int mid = 0;
            if (odd) { mid = 2*(r % 10); r /= 10; }
            for (int i = h-1; i >= 0; i--) { C[i] = r % 19; r /= 19; }
            for (int i = 0; i < h; i++) C[L-1-i] = C[i];
            if (odd) C[h] = mid;
        };
        auto record = [&](uint64_t idx, const std::vector<int>& C, int pre, bool clk, bool lenok, bool guard) {
            bool ret = lenok && pre == nT;
            St.n++; St.ret += ret; St.clockdev += !clk; St.lenerr += !lenok; St.guardfail += !guard;
            St.hist[pre < HN-1 ? pre : HN-1]++;
            if (pre > St.maxpre || (pre == St.maxpre && idx < St.argmax)) { St.maxpre = pre; St.argmax = idx; }
            if (ret) { std::lock_guard<std::mutex> lk(mu); printf("RETURN idx=%llu C=", (unsigned long long)idx); for (int x : C) printf("%d,", x); printf("\n"); fflush(stdout); }
        };
        auto scalar = [&](uint64_t idx, const std::vector<int>& C) {
            St.scalar++;
            memcpy(sa.data(), base.data(), n0);
            for (int i = 0; i < L; i++) sa[H0+i] = C[i];
            for (int i = 0; i < L; i++) stg[H1+i] = C[i];
            int n = n0; bool clk = true, guard = true;
            u8 *a = sa.data(), *b = sb.data();
            for (int t = 0; t < S; t++) {
                if (memcmp(a, &rootc[(t%p)*(nB+m)], nB+m)) guard = false;
                int n2 = sstep(a, n, sd.data(), b);
                if (n2 - n != g[t%p]) clk = false;
                n = n2; u8* tmp = a; a = b; b = tmp;
                if (n > NM) { clk = false; break; }
            }
            int pre = 0, lim = n < nT ? n : nT;
            while (pre < lim && a[pre] == stg[pre]) pre++;
            record(idx, C, pre, clk, n == nT, guard);
        };
        for (;;) {
            uint64_t s = next.fetch_add(CH); if (s >= hi) break;
            uint64_t e = s + CH < hi ? s + CH : hi;
            for (uint64_t gidx = s; gidx < e; gidx += VW) {
                int nl = (int)((e - gidx) < (uint64_t)VW ? (e - gidx) : VW);
                for (int x = 0; x < n0; x++) { vec v; for (int l = 0; l < VW; l++) v[l] = base[x]; A[x] = v; }
                for (int l = 0; l < VW; l++) {
                    centre_of(gidx + (l < nl ? l : 0), Cl[l]);
                    for (int i = 0; i < L; i++) A[H0+i][l] = Cl[l][i];
                }
                vec dev = {}, gbad = {};
                int n = n0;
                vec *a = A.data(), *b = Bv.data(), *d = D.data();
                for (int t = 0; t < S; t++) {
                    const u8* rc = &rootc[(t%p)*(nB+m)];
                    for (int x = 0; x < nB+m; x++) gbad |= (vec)(a[x] != rc[x]);
                    vec c = {};
                    for (int i = 0; i < n; i++) {
                        vec sm = a[i] + c; vec mk = (vec)(sm > 9);
                        d[i] = sm - (mk & 10); c = mk & 1;
                    }
                    int n2 = n;
                    if (g[t%p]) { dev |= (c ^ 1); d[n] = c; n2 = n+1; } else dev |= c;
                    for (int i = 0; i < (n2+1)/2; i++) { vec v = d[i] + d[n2-1-i]; b[i] = v; b[n2-1-i] = v; }
                    n = n2; vec* tmp = a; a = b; b = tmp;
                }
                // n == nT for every non-deviated lane
                for (int l = 0; l < nl; l++) {
                    uint64_t idx = gidx + l;
                    if (dev[l] || (FORCEDEV && idx % 7 == 0)) { scalar(idx, Cl[l]); continue; }
                    int pre = 0;
                    while (pre < H1 && a[pre][l] == tgt[pre]) pre++;
                    if (pre == H1) { // compare the centre and the mirrored half
                        for (int i = 0; i < L && pre == H1 + i; i++) if (a[H1+i][l] == Cl[l][i]) pre++;
                        if (pre == H1 + L) while (pre < nT && a[pre][l] == tgt[pre]) pre++;
                    }
                    record(idx, Cl[l], pre, true, true, gbad[l] == 0);
                }
            }
        }
        std::lock_guard<std::mutex> lk(mu);
        G.n += St.n; G.ret += St.ret; G.clockdev += St.clockdev; G.lenerr += St.lenerr; G.guardfail += St.guardfail; G.scalar += St.scalar;
        for (int i = 0; i < HN; i++) G.hist[i] += St.hist[i];
        if (St.maxpre > G.maxpre || (St.maxpre == G.maxpre && St.argmax < G.argmax)) { G.maxpre = St.maxpre; G.argmax = St.argmax; }
    };
    std::vector<std::thread> th; for (int i = 0; i < NT; i++) th.emplace_back(work); for (auto& t : th) t.join();
    printf("RESULT tbl=%s L=%d q0=%d K=%d steps=%d range=[%llu,%llu) centres=%llu returns=%llu clockdev=%llu lenerr=%llu guardfail=%llu scalar=%llu maxprefix=%d argmax_idx=%llu targetlen=%d\n",
        argv[1], L, q0, K, S, (unsigned long long)lo, (unsigned long long)hi, (unsigned long long)G.n, (unsigned long long)G.ret,
        (unsigned long long)G.clockdev, (unsigned long long)G.lenerr, (unsigned long long)G.guardfail, (unsigned long long)G.scalar,
        G.maxpre, (unsigned long long)G.argmax, nT);
    printf("HIST"); for (int i = 0; i < HN; i++) if (G.hist[i]) printf(" %d:%llu", i, (unsigned long long)G.hist[i]); printf("\n");
}
