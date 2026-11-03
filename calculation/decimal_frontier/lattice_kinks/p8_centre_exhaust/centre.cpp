// Exhaustive fixed-centre 80-step return check for p8 rec0/rec1 (m=20, |B|=39).
// P(q,C) = B0 W0^q C rev(W0)^q rev(B0); exact coefficient pairword step (= klib.pairword_step).
// usage: centre TBL L q0 threads [dump]   (dump: print per-centre "index prefix flags")
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <thread>
#include <atomic>
#include <mutex>
#include <cstdint>
typedef uint8_t u8;
int p, nB, m; int g[8]; std::vector<std::vector<int>> Bt, Wt;
int L, q0, NT, DUMP;
struct Stat { uint64_t n=0, ret=0, clockdev=0, lenerr=0, guardfail=0; int maxpre=-1; uint64_t argmax=0; uint64_t hist[400]={0}; };
std::mutex mu;
static inline int step(const u8* a, int n, u8* d, u8* out) {
    int c = 0;
    for (int i = 0; i < n; i++) { int s = a[i] + c; c = s >= 10; d[i] = s - 10*c; }
    int n2 = n; if (c) d[n2++] = 1;
    for (int i = 0; i < n2; i++) out[i] = d[i] + d[n2-1-i];
    return n2;
}
int main(int argc, char** argv) {
    FILE* f = fopen(argv[1], "r"); L = atoi(argv[2]); q0 = atoi(argv[3]); NT = atoi(argv[4]); DUMP = argc > 5;
    if (fscanf(f, "%d %d %d", &p, &nB, &m) != 3) return 1;
    for (int t = 0; t < p; t++) if (fscanf(f, "%d", &g[t]) != 1) return 1;
    Bt.assign(p, std::vector<int>(nB)); Wt.assign(p, std::vector<int>(m));
    for (int t = 0; t < p; t++) for (int x = 0; x < nB; x++) if (fscanf(f, "%d", &Bt[t][x]) != 1) return 1;
    for (int t = 0; t < p; t++) for (int x = 0; x < m; x++) if (fscanf(f, "%d", &Wt[t][x]) != 1) return 1;
    int h = L/2, odd = L % 2;
    uint64_t total = 1; for (int i = 0; i < h; i++) total *= 19; if (odd) total *= 10;
    int H0 = nB + m*q0, H1 = nB + m*(q0+1);
    int n0 = 2*H0 + L, nT = 2*H1 + L;
    Stat G;
    std::atomic<uint64_t> next(0);
    const uint64_t CH = 4096;
    auto work = [&]() {
        Stat S; std::vector<u8> A(nT+200), Bb(nT+200), D(nT+200), base(n0), tgt(nT), rootc(p*(nB+m));
        for (int t = 0; t < p; t++) for (int x = 0; x < nB+m; x++) rootc[t*(nB+m)+x] = x < nB ? Bt[t][x] : Wt[t][x-nB];
        std::vector<int> half(H1);
        for (int x = 0; x < H1; x++) half[x] = x < nB ? Bt[0][x] : Wt[0][(x-nB)%m];
        for (int x = 0; x < H0; x++) { base[x] = half[x]; base[n0-1-x] = half[x]; }
        for (int x = 0; x < H1; x++) { tgt[x] = half[x]; tgt[nT-1-x] = half[x]; }
        std::vector<int> C(L);
        for (;;) {
            uint64_t s = next.fetch_add(CH); if (s >= total) break;
            uint64_t e = s + CH < total ? s + CH : total;
            for (uint64_t idx = s; idx < e; idx++) {
                uint64_t r = idx; int mid = 0;
                if (odd) { mid = 2*(r % 10); r /= 10; }
                for (int i = h-1; i >= 0; i--) { C[i] = r % 19; r /= 19; }   // base-19, first coefficient most significant
                for (int i = 0; i < h; i++) C[L-1-i] = C[i];
                if (odd) C[h] = mid;
                memcpy(A.data(), base.data(), n0);
                for (int i = 0; i < L; i++) { A[H0+i] = C[i]; tgt[H1+i] = C[i]; }
                int n = n0; bool clk = true, guard = true;
                u8 *a = A.data(), *b = Bb.data();
                for (int t = 0; t < 80; t++) {
                    if (memcmp(a, &rootc[(t%p)*(nB+m)], nB+m)) guard = false;
                    int n2 = step(a, n, D.data(), b);
                    if (n2 - n != g[t%p]) clk = false;
                    n = n2; u8* tmp = a; a = b; b = tmp;
                    if (n > nT + 100) { clk = false; break; }
                }
                int pre = 0, lim = n < nT ? n : nT;
                while (pre < lim && a[pre] == tgt[pre]) pre++;
                bool lenok = (n == nT);
                bool ret = lenok && pre == nT;
                S.n++; S.ret += ret; S.clockdev += !clk; S.lenerr += !lenok; S.guardfail += !guard;
                S.hist[pre < 399 ? pre : 399]++;
                if (pre > S.maxpre) { S.maxpre = pre; S.argmax = idx; }
                if (ret) { std::lock_guard<std::mutex> lk(mu); printf("RETURN idx=%llu C=", (unsigned long long)idx); for (int x : C) printf("%d,", x); printf("\n"); fflush(stdout); }
                if (DUMP) { std::lock_guard<std::mutex> lk(mu); printf("D %llu %d %d %d %d\n", (unsigned long long)idx, pre, (int)clk, n, (int)guard); }
            }
        }
        std::lock_guard<std::mutex> lk(mu);
        G.n += S.n; G.ret += S.ret; G.clockdev += S.clockdev; G.lenerr += S.lenerr; G.guardfail += S.guardfail;
        for (int i = 0; i < 400; i++) G.hist[i] += S.hist[i];
        if (S.maxpre > G.maxpre || (S.maxpre == G.maxpre && S.argmax < G.argmax)) { G.maxpre = S.maxpre; G.argmax = S.argmax; }
    };
    std::vector<std::thread> th; for (int i = 0; i < NT; i++) th.emplace_back(work); for (auto& t : th) t.join();
    printf("RESULT tbl=%s L=%d q0=%d centres=%llu returns=%llu clockdev=%llu lenerr=%llu guardfail=%llu maxprefix=%d argmax_idx=%llu targetlen=%d\n",
        argv[1], L, q0, (unsigned long long)G.n, (unsigned long long)G.ret, (unsigned long long)G.clockdev, (unsigned long long)G.lenerr,
        (unsigned long long)G.guardfail, G.maxpre, (unsigned long long)G.argmax, nT);
    printf("HIST"); for (int i = 0; i < 400; i++) if (G.hist[i]) printf(" %d:%llu", i, (unsigned long long)G.hist[i]); printf("\n");
}
