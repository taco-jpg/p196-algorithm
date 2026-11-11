// r12g2 indep.cpp -- INDEPENDENT re-implementation of the K1 pipeline for the decimal period-8 lattices.
// Written from the definitions (reverse-and-add on palindromic pair words), NOT from kink6.cpp / kcommon.h / ktop.cpp:
//   * every step is computed on an EXPLICIT word: the lattice rows (exterior + q bulk periods) below the window, carries
//     propagated cell by cell from x = 0 (ascending) and from the top (descending).  No carry tables, no truncated loops.
//   * the exact fold map F_K is a genuine addition N + rev(N) on the full palindromic pair word (fstep).
//   * cyclic sets are replaced by the bi-infinite CORE (queue trimming of states without successor or predecessor), a
//     superset of the cyclic set, equal to it when the phase orbit has one cyclic SCC.
//   * forward iteration A_{n+1} = F(A_n) cap Z with chunked A_0, own code.
// Lattice input: rows file written by mklat.py (own parser of p8_scc.txt).
// Key formats (only to compare files with kink6/kink7/ktop): core key = ((t*m+j)*2+par) << PS | sum cell_i << 5i,
// PS = 100 (K <= 20); top key = (t*2+par) << 100 | sum cell_i << 5i, cell 0 = lowest cell (h-k).
// modes:
//   indep selftest ROWS K q nsamp seed tau sigma
//   indep core     ROWS t0 j0 p0 Kmax OUTDIR threads [q]
//   indep topcore  ROWS kmax OUTDIR
//   indep fold     ROWS K COREFILE [q]
//   indep fwd      ROWS K Kb COREFILE Kt TOPFILE t0 j0 p0 threads s0 chunklog2 [q] [maxsteps]
//   indep cmp      FILE1 FILE2 [PS]   (PS given: restrict FILE2 to the phases of FILE1)
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <random>
#include <string>
#include <thread>
#include <vector>
using namespace std;
typedef unsigned __int128 u128;
typedef long long ll;

static int Pp, NB, MM, BS = 10, DV = 19;   // time period, exterior length, bulk period, base, number of cell values 2B-1
static vector<int> GG;               // clock
static vector<vector<int>> BB, WW;   // exterior rows BB[t][x], bulk rows WW[t][j]
static const int XMAX = 1200;
static vector<int> ROW;              // ROW[t*XMAX + x] = lattice cell (explicit, precomputed from BB/WW)
static inline int row(int t, int x) { return ROW[t * XMAX + x]; }
static double now_s() { return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }

static void load_rows(const char* fn) {
    FILE* f = fopen(fn, "r"); if (!f) { perror(fn); exit(1); }
    char hdr[256]; if (!fgets(hdr, sizeof hdr, f)) exit(1);
    int nr = sscanf(hdr, "%d %d %d %d", &Pp, &NB, &MM, &BS); if (nr < 3) exit(1); if (nr < 4) BS = 10; DV = 2 * BS - 1;
    GG.resize(Pp); for (auto& x : GG) if (fscanf(f, "%d", &x) != 1) exit(1);
    BB.assign(Pp, vector<int>(NB)); WW.assign(Pp, vector<int>(MM));
    for (int t = 0; t < Pp; t++) for (auto& x : BB[t]) if (fscanf(f, "%d", &x) != 1) exit(1);
    for (int t = 0; t < Pp; t++) for (auto& x : WW[t]) if (fscanf(f, "%d", &x) != 1) exit(1);
    fclose(f);
    ROW.assign(Pp * XMAX, 0);
    for (int t = 0; t < Pp; t++) for (int x = 0; x < XMAX; x++) ROW[t * XMAX + x] = x < NB ? BB[t][x] : WW[t][(x - NB) % MM];
}
static inline void next_phase(int t, int j, int par, int& t2, int& j2, int& p2) {
    int g = GG[t], dh = (g == 1 && par == 0);
    t2 = (t + 1) % Pp; j2 = (j + dh) % MM; p2 = (par + g) % 2;
}
static inline unsigned phid(int t, int j, int par) { return (unsigned)((t * MM + j) * 2 + par); }
static inline void phdec(unsigned ph, int& t, int& j, int& par) { par = ph % 2; ph /= 2; j = ph % MM; t = ph / MM; }
static inline u128 cells_enc(const int* w, int K) { u128 k = 0; for (int i = 0; i < K; i++) k |= (u128)w[i] << (5 * i); return k; }
static inline void cells_dec(u128 k, int* w, int K) { for (int i = 0; i < K; i++) w[i] = (int)((k >> (5 * i)) & 31); }
static const int PSC = 100;
// window-set keys for the forward iteration: 5-bit cells for K <= 25; for K > 25 two 64-bit halves in base DV
// (cells 0..14 in the low half, 15..K-1 in the high half; DV^15 < 2^64 for DV <= 19)
static int WK = 0;
static inline u128 wkey(const int* w) {
    if (WK <= 25) return cells_enc(w, WK);
    uint64_t lo = 0, hi = 0, f = 1;
    for (int i = 0; i < 15; i++) { lo += (uint64_t)w[i] * f; f *= (uint64_t)DV; }
    f = 1; for (int i = 15; i < WK; i++) { hi += (uint64_t)w[i] * f; f *= (uint64_t)DV; }
    return ((u128)hi << 64) | lo;
}
static inline void wunkey(u128 k, int* w) {
    if (WK <= 25) { cells_dec(k, w, WK); return; }
    uint64_t lo = (uint64_t)k, hi = (uint64_t)(k >> 64);
    for (int i = 0; i < 15; i++) { w[i] = (int)(lo % DV); lo /= DV; }
    for (int i = 15; i < WK; i++) { w[i] = (int)(hi % DV); hi /= DV; }
}

// ------------------------------------------------------------------ relaxation R_K (bottom window, free top inputs)
// Window = cells [c, c+K) of the lower half, c = NB + j + q*MM, exact lattice below c at time t.  The cells above the
// window are unknown; they act on the window only through
//   Din  = carry into the mirror of cell c+K-1 (0/1), and
//   topv = low output digit of cell c+K (0..9), which enters the window only when the frame shifts (dh = 1).
// For each Din, compute the new cells; the lattice cells below the new frame c+dh must be exact at t+1 and the carry out
// of the top digit (= mirror of cell 0) must equal the clock g[t].  out[Din][i]; topv only changes out[.][K-1] when dh.
// returns a bitmask: bit Din set if that Din is admissible.
static int rstep2(int t, int j, int par, const int* w, int K, int q, int out[2][64]) {
    const int g = GG[t], dh = (g == 1 && par == 0);
    const int c = NB + j + q * MM, H = c + K, t1 = (t + 1) % Pp;
    int P[XMAX], e[XMAX], r[XMAX];
    for (int x = 0; x < c; x++) P[x] = row(t, x);
    for (int i = 0; i < K; i++) P[c + i] = w[i];
    int a = 0;
    for (int x = 0; x < H; x++) { int s = P[x] + a; e[x] = s % BS; a = s / BS; }
    int mask = 0;
    for (int Din = 0; Din < 2; Din++) {
        int b = Din;
        for (int x = H - 1; x >= 0; x--) { int s = P[x] + b; r[x] = s % BS; b = s / BS; }
        if (b != g) continue;
        bool ok = true;
        for (int x = 0; x < c + dh && ok; x++) { int rr = (g == 0) ? r[x] : (x == 0 ? 1 : r[x - 1]); if (e[x] + rr != row(t1, x)) ok = false; }
        if (!ok) continue;
        for (int i = 0; i < K; i++) {
            int x = c + dh + i;
            int ex = (x < H) ? e[x] : 0;                 // topv added by the caller when dh
            int rr = (g == 0) ? r[x] : r[x - 1];
            out[Din][i] = ex + rr;
        }
        mask |= 1 << Din;
    }
    return mask;
}

// ------------------------------------------------------------------ exact fold map: genuine addition on the full word
static long long fold_overflow_mismatch = 0;
static bool fstep(int t, int j, int par, const int* w, int K, int q, int* out) {
    const int g = GG[t];
    const int c = NB + j + q * MM, h = c + K, n = 2 * h - par;
    int P[2 * XMAX + 2], O[2 * XMAX + 2];
    for (int x = 0; x < c; x++) P[x] = row(t, x);
    for (int i = 0; i < K; i++) P[c + i] = w[i];
    for (int x = h; x < n; x++) P[x] = P[n - 1 - x];
    int a = 0;
    for (int x = 0; x < n; x++) { int s = P[x] + a; O[x] = s % BS; a = s / BS; }
    int n2 = n; if (a) { O[n] = a; n2 = n + 1; }
    if (n2 - n != g) { fold_overflow_mismatch++; return false; }
    const int h2 = (n2 + 1) / 2, c2 = h2 - K, dh = (g == 1 && par == 0), t1 = (t + 1) % Pp;
    if (c2 != c + dh) { fprintf(stderr, "frame bug\n"); exit(9); }
    for (int x = 0; x < c2; x++) if (O[x] + O[n2 - 1 - x] != row(t1, x)) return false;
    for (int i = 0; i < K; i++) { int x = c2 + i; out[i] = O[x] + O[n2 - 1 - x]; }
    return true;
}

// ------------------------------------------------------------------ top relaxation (top k cells, fold exact, free below)
// a_in = carry into cell h-k, r_in = high output digit of cell h-k-1 (used only when g = 1 and the frame does not shift).
static void tstep(int t, int par, const int* w, int k, int ain, int rin, int* out) {
    int g = GG[t], dh = (g == 1 && par == 0);
    int A[66], e[66], r[66], nw[66];
    int a = ain;
    for (int i = 0; i < k; i++) { A[i] = a; int s = w[i] + a; e[i] = s % BS; a = s / BS; }
    A[k] = a;
    int b = (par == 0) ? A[k] : A[k - 1];    // even n: carry into position h; odd n: carry into the middle cell
    for (int i = k - 1; i >= 0; i--) { int s = w[i] + b; r[i] = s % BS; b = s / BS; }
    for (int i = 0; i < k + dh; i++) {
        if (i == k) { nw[i] = 2 * r[k - 1]; continue; }       // new middle cell = twice the digit at position h
        int rr = (g == 0) ? r[i] : (i >= 1 ? r[i - 1] : rin);
        nw[i] = e[i] + rr;
    }
    for (int i = 0; i < k; i++) out[i] = nw[i + dh];
}

// ------------------------------------------------------------------ hash index of sorted u128 keys
static inline uint64_t mixh(u128 k) {
    uint64_t x = (uint64_t)k * 0x9E3779B97F4A7C15ULL ^ (uint64_t)(k >> 64) * 0xC2B2AE3D27D4EB4FULL;
    x ^= x >> 31; x *= 0xBF58476D1CE4E5B9ULL; x ^= x >> 29; return x;
}
struct HIdx {
    const vector<u128>* keys = nullptr; vector<uint32_t> sl; uint64_t mask = 0;
    void build(const vector<u128>& k) {
        keys = &k; uint64_t cap = 1; while (cap < 2 * k.size() + 8) cap <<= 1;
        sl.assign(cap, 0); mask = cap - 1;
        for (uint64_t i = 0; i < k.size(); i++) { uint64_t h = mixh(k[i]) & mask; while (sl[h]) h = (h + 1) & mask; sl[h] = (uint32_t)(i + 1); }
    }
    inline ll find(u128 x) const { uint64_t h = mixh(x) & mask; while (true) { uint32_t s = sl[h]; if (!s) return -1; if ((*keys)[s - 1] == x) return s - 1; h = (h + 1) & mask; } }
};
static vector<u128> readk(const char* fn) {
    FILE* f = fopen(fn, "rb"); if (!f) { perror(fn); exit(1); }
    fseek(f, 0, SEEK_END); long sz = ftell(f); fseek(f, 0, SEEK_SET);
    vector<u128> v(sz / 16); if (!v.empty() && fread(v.data(), 16, v.size(), f) != v.size()) exit(1); fclose(f); return v;
}
static void writek(const char* fn, const vector<u128>& v) { FILE* f = fopen(fn, "wb"); fwrite(v.data(), 16, v.size(), f); fclose(f); }
static void sort_unique(vector<u128>& v) { sort(v.begin(), v.end()); v.erase(unique(v.begin(), v.end()), v.end()); }

// ------------------------------------------------------------------ queue trimming to the bi-infinite core
// graph: nodes 0..N-1, CSR (off, tg); returns alive flags
static vector<uint8_t> trim_core(uint64_t N, const vector<uint32_t>& off, const vector<uint32_t>& tg) {
    vector<uint32_t> indeg(N, 0), outdeg(N, 0);
    for (uint64_t s = 0; s < N; s++) { outdeg[s] = (uint32_t)(off[s + 1] - off[s]); for (uint64_t e = off[s]; e < (uint64_t)off[s + 1]; e++) indeg[tg[e]]++; }
    // reverse CSR
    vector<uint32_t> roff(N + 1, 0); for (uint64_t s = 0; s < N; s++) roff[s + 1] = roff[s] + indeg[s];
    vector<uint32_t> rsrc(tg.size()); { vector<uint32_t> pos(roff.begin(), roff.end() - 1); for (uint64_t s = 0; s < N; s++) for (uint64_t e = off[s]; e < (uint64_t)off[s + 1]; e++) rsrc[pos[tg[e]]++] = (uint32_t)s; }
    vector<uint8_t> alive(N, 1); vector<uint32_t> Q; Q.reserve(1 << 20);
    for (uint64_t s = 0; s < N; s++) if (indeg[s] == 0 || outdeg[s] == 0) { alive[s] = 0; Q.push_back((uint32_t)s); }
    size_t qh = 0;
    while (qh < Q.size()) {
        uint32_t s = Q[qh++];
        for (uint64_t e = off[s]; e < (uint64_t)off[s + 1]; e++) { uint32_t u = tg[e]; if (alive[u] && --indeg[u] == 0) { alive[u] = 0; Q.push_back(u); } }
        for (uint64_t e = roff[s]; e < (uint64_t)roff[s + 1]; e++) { uint32_t v = rsrc[e]; if (alive[v] && --outdeg[v] == 0) { alive[v] = 0; Q.push_back(v); } }
    }
    return alive;
}

// ------------------------------------------------------------------ mode core
static int mode_core(int argc, char** argv) {
    int t0 = atoi(argv[3]), j0 = atoi(argv[4]), p0 = atoi(argv[5]), Kmax = atoi(argv[6]); string od = argv[7];
    int T = argc > 8 ? atoi(argv[8]) : 4; int q = argc > 9 ? atoi(argv[9]) : 3;
    // phase orbit
    vector<unsigned> orb; { int t = t0, j = j0, p = p0; do { orb.push_back(phid(t, j, p)); int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; } while (!(t == t0 && j == j0 && p == p0)); }
    sort(orb.begin(), orb.end());
    printf("core: phase orbit of (%d,%d,%d): %zu phases, q=%d\n", t0, j0, p0, orb.size(), q); fflush(stdout);
    vector<u128> par;   // Core(K-1) keys, sorted (K-1 = 0: phases only)
    for (auto ph : orb) par.push_back((u128)ph << PSC);
    for (int K = 1; K <= Kmax; K++) {
        double T0 = now_s();
        HIdx PI; PI.build(par);
        const uint64_t N = (uint64_t)par.size() * DV;
        if (N >= 0xFFFFFFF0ULL) { fprintf(stderr, "too big\n"); return 1; }
        // edges, threaded over candidate ranges
        vector<vector<uint32_t>> tgs(T); vector<vector<uint32_t>> cnts(T);
        vector<thread> th;
        for (int z = 0; z < T; z++) th.emplace_back([&, z] {
            uint64_t lo = N * z / T, hi = N * (z + 1) / T; auto& TG = tgs[z]; auto& CN = cnts[z]; CN.reserve(hi - lo);
            int w[64], out[2][64]; uint32_t loc[24];
            for (uint64_t ci = lo; ci < hi; ci++) {
                u128 pk = par[ci / DV]; int t, j, p; phdec((unsigned)(pk >> PSC), t, j, p);
                cells_dec(pk, w, K - 1); w[K - 1] = (int)(ci % DV);
                int g = GG[t], dh = (g == 1 && p == 0); int t2, j2, p2; next_phase(t, j, p, t2, j2, p2);
                int mask = rstep2(t, j, p, w, K, q, out); int nl = 0;
                for (int Din = 0; Din < 2; Din++) {
                    if (!(mask >> Din & 1)) continue;
                    for (int tv = 0; tv < (dh ? BS : 1); tv++) {
                        int top = out[Din][K - 1] + (dh ? tv : 0);
                        u128 pk2 = ((u128)phid(t2, j2, p2) << PSC) | cells_enc(out[Din], K - 1);
                        ll pi = PI.find(pk2); if (pi < 0) continue;
                        loc[nl++] = (uint32_t)(pi * DV + top);
                    }
                }
                sort(loc, loc + nl); nl = (int)(unique(loc, loc + nl) - loc);
                CN.push_back((uint32_t)nl); for (int i = 0; i < nl; i++) TG.push_back(loc[i]);
            }
        });
        for (auto& x : th) x.join();
        uint64_t E = 0; for (int z = 0; z < T; z++) E += tgs[z].size();
        if (E >= 0xFFFFFFF0ULL) { fprintf(stderr, "too many edges\n"); return 1; }
        vector<uint32_t> off(N + 1, 0);
        vector<uint32_t> tg; tg.reserve(E);
        { uint64_t s = 0; for (int z = 0; z < T; z++) { for (auto c : cnts[z]) { off[s + 1] = off[s] + c; s++; } tg.insert(tg.end(), tgs[z].begin(), tgs[z].end()); vector<uint32_t>().swap(tgs[z]); vector<uint32_t>().swap(cnts[z]); } }
        vector<uint8_t> alive = trim_core(N, off, tg);
        vector<uint32_t>().swap(off); vector<uint32_t>().swap(tg);
        vector<u128> cur; ll nacc = 0;
        for (uint64_t ci = 0; ci < N; ci++) if (alive[ci]) {
            u128 k = par[ci / DV] | ((u128)(ci % DV) << (5 * (K - 1))); cur.push_back(k);
            int t, j, p; phdec((unsigned)(k >> PSC), t, j, p); int c = NB + j + q * MM; if ((int)(k & 31) != row(t, c)) nacc++;
        }
        sort(cur.begin(), cur.end());
        char fn[512]; snprintf(fn, sizeof fn, "%s/core_%d.bin", od.c_str(), K); writek(fn, cur);
        printf("CORE K=%d candidates=%llu edges(unique)=%llu core=%zu accepting=%lld [%.1fs]\n", K, (unsigned long long)N, (unsigned long long)E, cur.size(), nacc, now_s() - T0); fflush(stdout);
        par.swap(cur);
    }
    return 0;
}

// ------------------------------------------------------------------ mode topcore
static int mode_topcore(int argc, char** argv) {
    int kmax = atoi(argv[3]); string od = argv[4];
    vector<u128> par; for (int t = 0; t < Pp; t++) for (int p = 0; p < 2; p++) par.push_back((u128)(unsigned)(t * 2 + p) << 100);
    for (int k = 1; k <= kmax; k++) {
        double T0 = now_s();
        // TopCore(k) subset {new bottom cell} x TopCore(k-1): candidate = (parent index, new cell 0)
        HIdx PI; PI.build(par); const uint64_t N = (uint64_t)par.size() * DV;
        vector<uint32_t> off(N + 1, 0); vector<uint32_t> tg;
        int w[64], nw[64]; uint32_t loc[24];
        for (uint64_t ci = 0; ci < N; ci++) {
            u128 pk = par[ci / DV]; unsigned ph = (unsigned)(pk >> 100); int t = ph >> 1, p = ph & 1;
            w[0] = (int)(ci % DV); cells_dec(pk, w + 1, k - 1);
            int g = GG[t]; int t2 = (t + 1) % Pp, p2 = (p + g) % 2; int nl = 0;
            for (int ain = 0; ain < 2; ain++) for (int rin = 0; rin < ((g == 1 && p == 1) ? BS : 1); rin++) {
                tstep(t, p, w, k, ain, rin, nw);
                u128 pk2 = ((u128)(unsigned)(t2 * 2 + p2) << 100) | cells_enc(nw + 1, k - 1);
                ll pi = PI.find(pk2); if (pi < 0) continue;
                loc[nl++] = (uint32_t)(pi * DV + nw[0]);
            }
            sort(loc, loc + nl); nl = (int)(unique(loc, loc + nl) - loc);
            off[ci + 1] = off[ci] + nl; for (int i = 0; i < nl; i++) tg.push_back(loc[i]);
        }
        vector<uint8_t> alive = trim_core(N, off, tg);
        vector<u128> cur;
        for (uint64_t ci = 0; ci < N; ci++) if (alive[ci]) { u128 pk = par[ci / DV]; u128 ph = pk >> 100, cl = pk & (((u128)1 << 100) - 1); cur.push_back((ph << 100) | (cl << 5) | (u128)(ci % DV)); }
        sort(cur.begin(), cur.end());
        char fn[512]; snprintf(fn, sizeof fn, "%s/top_%d.bin", od.c_str(), k); writek(fn, cur);
        printf("TOPCORE k=%d candidates=%llu edges=%zu core=%zu [%.1fs]\n", k, (unsigned long long)N, tg.size(), cur.size(), now_s() - T0); fflush(stdout);
        par.swap(cur);
    }
    return 0;
}

// ------------------------------------------------------------------ mode fold: exact fold check inside a core file
static int mode_fold(int argc, char** argv) {
    int K = atoi(argv[3]); vector<u128> C = readk(argv[4]); int q = argc > 5 ? atoi(argv[5]) : 3;
    HIdx I; I.build(C); const uint64_t N = C.size();
    vector<int64_t> nx(N, -1); ll nsucc = 0;
    for (uint64_t i = 0; i < N; i++) {
        int t, j, p, w[64], nw[64]; phdec((unsigned)(C[i] >> PSC), t, j, p); cells_dec(C[i], w, K);
        if (!fstep(t, j, p, w, K, q, nw)) continue;
        int t2, j2, p2; next_phase(t, j, p, t2, j2, p2);
        ll k = I.find(((u128)phid(t2, j2, p2) << PSC) | cells_enc(nw, K)); if (k >= 0) { nx[i] = k; nsucc++; }
    }
    vector<uint8_t> col(N, 0); ll cyc = 0;
    for (uint64_t i = 0; i < N; i++) {
        if (col[i]) continue; vector<int64_t> path; int64_t x = i;
        while (x >= 0 && col[x] == 0) { col[x] = 1; path.push_back(x); x = nx[x]; }
        if (x >= 0 && col[x] == 1) { cyc++; int t, j, p, w[64]; phdec((unsigned)(C[x] >> PSC), t, j, p); cells_dec(C[x], w, K); printf("CYCLE through t=%d j=%d par=%d win", t, j, p); for (int z = 0; z < K; z++) printf(" %d", w[z]); printf("\n"); }
        for (auto y : path) col[y] = 2;
    }
    printf("FOLD K=%d states=%llu fold-successors-inside=%lld cycles=%lld overflow-mismatch=%lld\n", K, (unsigned long long)N, nsucc, cyc, fold_overflow_mismatch);
    return 0;
}

// ------------------------------------------------------------------ mode fwd: forward image iteration with the genuine fold map
static int mode_fwd(int argc, char** argv) {
    int K = atoi(argv[3]), Kb = atoi(argv[4]); vector<u128> CB = readk(argv[5]); int Kt = atoi(argv[6]); vector<u128> TP = readk(argv[7]);
    int t0 = atoi(argv[8]), j0 = atoi(argv[9]), p0 = atoi(argv[10]), T = atoi(argv[11]), s0 = atoi(argv[12]), cl = atoi(argv[13]);
    int q = argc > 14 ? atoi(argv[14]) : 3; int maxsteps = argc > 15 ? atoi(argv[15]) : 4000;
    const int Km = K - Kb - Kt; if (Km < 0) { fprintf(stderr, "K < Kb + Kt\n"); return 1; }
    WK = K; if (K > 30 || Kb > 23) { fprintf(stderr, "K <= 30, Kb <= 23\n"); return 1; }
    const int PSb = Kb <= 20 ? 100 : 118;      // kink6/kink7 key format of the bottom filter file
    { mt19937_64 R(1); int w[64], v[64]; for (int r = 0; r < 1000000; r++) { for (int i = 0; i < K; i++) w[i] = (int)(R() % DV); wunkey(wkey(w), v); if (memcmp(w, v, sizeof(int) * K)) { fprintf(stderr, "packing bug\n"); return 1; } } }
    sort(CB.begin(), CB.end()); sort(TP.begin(), TP.end());
    HIdx IB; IB.build(CB); HIdx IT; IT.build(TP);
    auto inZ = [&](int t, int j, int p, const int* w) -> bool {
        if (IT.find(((u128)(unsigned)(t * 2 + p) << 100) | cells_enc(w + K - Kt, Kt)) < 0) return false;
        return IB.find(((u128)phid(t, j, p) << PSb) | cells_enc(w, Kb)) >= 0;
    };
    vector<u128> b0, u0;   // bottom states at phi0, top states at (t0,p0)
    for (auto k : CB) if ((unsigned)(k >> PSb) == phid(t0, j0, p0)) b0.push_back(k & (((u128)1 << PSb) - 1));
    for (auto k : TP) if ((unsigned)(k >> 100) == (unsigned)(t0 * 2 + p0)) u0.push_back(k & (((u128)1 << 100) - 1));
    ll nmid = 1; for (int i = 0; i < Km; i++) nmid *= DV;
    const ll N0 = (ll)b0.size() * nmid * (ll)u0.size();
    int Lo = 0; { int t = t0, j = j0, p = p0; do { int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; Lo++; } while (!(t == t0 && j == j0 && p == p0)); }
    printf("ifwd base=%d K=%d Kb=%d Kt=%d mid=%d phi0=(%d,%d,%d) orbit %d: |bottom| %zu x %d^%d x |top| %zu = %lld, q=%d\n", BS, K, Kb, Kt, Km, t0, j0, p0, Lo, b0.size(), DV, Km, u0.size(), N0, q);
    fflush(stdout);
    double T0 = now_s();
    auto stepset = [&](const vector<u128>& A, int t, int j, int p) {
        vector<vector<u128>> loc(T); vector<thread> th; size_t NA = A.size();
        for (int z = 0; z < T; z++) th.emplace_back([&, z] {
            int w[64], nw[64]; int t2, j2, p2; next_phase(t, j, p, t2, j2, p2);
            for (size_t i = NA * z / T; i < NA * (z + 1) / T; i++) { wunkey(A[i], w); if (fstep(t, j, p, w, K, q, nw) && inZ(t2, j2, p2, nw)) loc[z].push_back(wkey(nw)); }
        });
        for (auto& x : th) x.join();
        vector<u128> B; for (auto& v : loc) B.insert(B.end(), v.begin(), v.end()); sort_unique(B); return B;
    };
    const ll CH = 1LL << cl; vector<u128> acc; vector<ll> sums(s0 + 1, 0); ll ngen = 0;
    for (ll c0 = 0; c0 < N0; c0 += CH) {
        ll c1 = min(N0, c0 + CH);
        vector<vector<u128>> loc(T); vector<thread> th; vector<ll> gen(T, 0);
        for (int z = 0; z < T; z++) th.emplace_back([&, z] {
            int w[64], nw[64]; int t2, j2, p2; next_phase(t0, j0, p0, t2, j2, p2);
            for (ll x = c0 + (c1 - c0) * z / T; x < c0 + (c1 - c0) * (z + 1) / T; x++) {
                ll bi = x / (nmid * (ll)u0.size()), rem = x % (nmid * (ll)u0.size()), mi = rem / (ll)u0.size(), ui = rem % (ll)u0.size();
                cells_dec(b0[bi], w, Kb); for (int i = 0; i < Km; i++) { w[Kb + i] = (int)(mi % DV); mi /= DV; } cells_dec(u0[ui], w + Kb + Km, Kt);
                if (p0 == 1 && (w[K - 1] & 1)) continue;      // odd length: the middle pair cell is twice a digit
                gen[z]++;
                if (fstep(t0, j0, p0, w, K, q, nw) && inZ(t2, j2, p2, nw)) loc[z].push_back(wkey(nw));
            }
        });
        for (auto& x : th) x.join();
        for (auto g : gen) ngen += g;
        vector<u128> B; for (auto& v : loc) { B.insert(B.end(), v.begin(), v.end()); vector<u128>().swap(v); } sort_unique(B);
        int t = t0, j = j0, p = p0; { int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; }
        sums[1] += B.size(); int s = 1;
        while (s < s0 && !B.empty()) { B = stepset(B, t, j, p); { int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; } s++; sums[s] += B.size(); }
        if (s == s0) acc.insert(acc.end(), B.begin(), B.end());
        if (acc.size() > (1u << 26)) sort_unique(acc);
    }
    sort_unique(acc);
    printf("STEP 0 size %lld (genuine)\n", ngen);
    for (int s = 1; s < s0; s++) printf("STEP %d size <= %lld (sum over chunks)\n", s, sums[s]);
    int t = t0, j = j0, p = p0; for (int s = 0; s < s0; s++) { int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; }
    int n = s0; vector<u128> A = acc, prev; bool havep = false; int last = A.empty() ? 0 : s0;
    printf("STEP %d size %zu [%.1fs]\n", n, A.size(), now_s() - T0); fflush(stdout);
    bool stable = false;
    while (!A.empty() && n < maxsteps) {
        A = stepset(A, t, j, p); { int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; } n++;
        if (!A.empty()) last = n;
        printf("STEP %d size %zu [%.1fs]", n, A.size(), now_s() - T0);
        if (getenv("IFWD_FRONT")) {   // front statistics: lowest off-lattice window index (K = window all-lattice)
            vector<ll> hist(K + 1, 0); int c = NB + j + q * MM; int w[64];
            for (auto x : A) { wunkey(x, w); int f = K; for (int z = 0; z < K; z++) if (w[z] != row(t, c + z)) { f = z; break; } hist[f]++; }
            printf(" front:"); for (int z = 0; z <= K; z++) if (hist[z]) printf(" %d:%lld", z, hist[z]);
        }
        printf("\n"); fflush(stdout);
        if (n % Lo == 0) { if (havep && A == prev) { stable = true; break; } prev = A; havep = true; }
    }
    if (A.empty()) printf("EMPTY at step %d (lifetime %d); overflow-mismatch %lld [%.1fs]\n", n, last, fold_overflow_mismatch, now_s() - T0);
    else if (stable) {
        printf("STABLE at step %d with %zu states at phi0 (all periodic)\n", n, A.size());
        for (size_t i = 0; i < A.size() && i < 8; i++) {
            int w[64], nw[64]; wunkey(A[i], w); int tt = t0, jj = j0, pp = p0; int len = 0; bool nonlat = false;
            vector<int> w0(w, w + K);
            do { int c = NB + jj + q * MM; for (int z = 0; z < K; z++) if (w[z] != row(tt, c + z)) nonlat = true;
                 if (!fstep(tt, jj, pp, w, K, q, nw)) { printf("  broke\n"); break; } int a, b, c2; next_phase(tt, jj, pp, a, b, c2); tt = a; jj = b; pp = c2; memcpy(w, nw, sizeof(int) * K); len++;
            } while (!(tt == t0 && jj == j0 && pp == p0 && vector<int>(w, w + K) == w0) && len < 1000000);
            printf("  periodic state %zu: period %d %s:", i, len, nonlat ? "NON-LATTICE" : "all-lattice"); for (int z = 0; z < K; z++) printf(" %d", w0[z]); printf("\n");
        }
    }
    else printf("UNDECIDED at %d\n", n);
    return 0;
}

// ------------------------------------------------------------------ selftest
static int mode_selftest(int argc, char** argv) {
    int K = atoi(argv[3]), q = atoi(argv[4]); ll ns = atoll(argv[5]); int seed = atoi(argv[6]);
    int tau = argc > 7 ? atoi(argv[7]) : -1, sig = argc > 8 ? atoi(argv[8]) : 0;
    mt19937_64 R(seed);
    auto rnd = [&](int n) { return (int)(R() % (uint64_t)n); };
    // (a) clock/lattice: pure lattice word of depth K (window = lattice cells), genuine step: cells far below the centre
    //     must be lattice at t+1, overflow = clock
    ll bad_a = 0, of_a = 0;
    for (int t = 0; t < Pp; t++) for (int j = 0; j < MM; j++) for (int par = 0; par < 2; par++) {
        int c = NB + j + q * MM; int w[64], nw[64]; for (int i = 0; i < K; i++) w[i] = row(t, c + i);
        int h = c + K, n = 2 * h - par; vector<int> P(n), O(n + 1);
        for (int x = 0; x < h; x++) P[x] = row(t, x); for (int x = h; x < n; x++) P[x] = P[n - 1 - x];
        int a = 0; for (int x = 0; x < n; x++) { int s = P[x] + a; O[x] = s % BS; a = s / BS; }
        int n2 = n + a; if (a) O[n] = 1; if (n2 - n != GG[t]) of_a++;
        for (int x = 0; x < c - 2 * MM; x++) if (O[x] + O[n2 - 1 - x] != row((t + 1) % Pp, x)) bad_a++;
        (void)nw;
    }
    printf("(a) lattice rows are an exact solution far below the centre: mismatches %lld, overflow != clock %lld\n", bad_a, of_a);
    // (b) relaxation rule vs genuine step with random cells above the window
    ll nb = 0, bad_b = 0, okc = 0;
    for (ll s = 0; s < ns; s++) {
        int t = rnd(Pp), j = rnd(MM), par = rnd(2), u = 1 + rnd(6);
        int c = NB + j + q * MM, Kf = K + u; int w[64], nw[64], out[2][64];
        for (int i = 0; i < K; i++) w[i] = (rnd(3) == 0) ? rnd(DV) : row(t, c + i);
        int big[64]; for (int i = 0; i < K; i++) big[i] = w[i]; for (int i = K; i < Kf; i++) big[i] = rnd(DV);
        if (par == 1 && (big[Kf - 1] & 1)) big[Kf - 1] ^= 1;
        // genuine full word of depth Kf
        int h = c + Kf, n = 2 * h - par; vector<int> P(n), O(n + 2), Car(n + 2);
        for (int x = 0; x < c; x++) P[x] = row(t, x); for (int i = 0; i < Kf; i++) P[c + i] = big[i]; for (int x = h; x < n; x++) P[x] = P[n - 1 - x];
        int a = 0; for (int x = 0; x < n; x++) { Car[x] = a; int s2 = P[x] + a; O[x] = s2 % BS; a = s2 / BS; }
        int n2 = n + a; if (a) O[n] = 1;
        int g = GG[t], dh = (g == 1 && par == 0);
        bool gen_ok = (n2 - n == g);
        int c2 = c + dh;
        if (gen_ok) for (int x = 0; x < c2; x++) if (O[x] + O[n2 - 1 - x] != row((t + 1) % Pp, x)) gen_ok = false;
        int Din = Car[n - c - K];          // carry into position n-1-(c+K-1) = mirror of the top window cell
        int topv = O[c + K];               // low digit of cell c+K
        int mask = rstep2(t, j, par, w, K, q, out);
        bool r_ok = (mask >> Din) & 1;
        nb++;
        if (r_ok != gen_ok) { bad_b++; continue; }
        if (!gen_ok) continue;
        okc++;
        for (int i = 0; i < K; i++) { int v = out[Din][i] + ((dh && i == K - 1) ? topv : 0); int x = c2 + i; if (v != O[x] + O[n2 - 1 - x]) { bad_b++; break; } }
        (void)nw;
    }
    printf("(b) relaxation step vs genuine step (random window + random cells above): %lld samples (%lld lattice-ok), mismatches %lld\n", nb, okc, bad_b);
    // (c) fold map independent of q; (d) top relaxation vs genuine; (e) complement symmetry
    ll bad_c = 0, nc = 0, bad_d = 0, nd = 0, bad_e = 0, ne = 0, alive_e = 0;
    for (ll s = 0; s < ns; s++) {
        int t = rnd(Pp), j = rnd(MM), par = rnd(2); int c = NB + j + q * MM; int w[64], o1[64], o2[64];
        for (int i = 0; i < K; i++) w[i] = (rnd(3) == 0) ? rnd(DV) : row(t, c + i);
        if (par == 1 && (w[K - 1] & 1)) w[K - 1] ^= 1;
        bool a1 = fstep(t, j, par, w, K, q, o1), a2 = fstep(t, j, par, w, K, q + 2, o2); nc++;
        if (a1 != a2 || (a1 && memcmp(o1, o2, sizeof(int) * K))) bad_c++;
        // (d): genuine top-k window vs tstep with the genuine inputs from below
        int k = 1 + rnd(min(K - 1, 6));
        {
            int h = c + K, n = 2 * h - par; vector<int> P(n), O(n + 2), Car(n + 2);
            for (int x = 0; x < c; x++) P[x] = row(t, x); for (int i = 0; i < K; i++) P[c + i] = w[i]; for (int x = h; x < n; x++) P[x] = P[n - 1 - x];
            int a = 0; for (int x = 0; x < n; x++) { Car[x] = a; int s2 = P[x] + a; O[x] = s2 % BS; a = s2 / BS; }
            int n2 = n + a; if (a) O[n] = 1;
            if (n2 - n == GG[t]) {
                int h2 = (n2 + 1) / 2; int ain = Car[h - k], rin = O[n - 1 - (h - k - 1)];
                int tw[64], tout[64]; for (int i = 0; i < k; i++) tw[i] = w[K - k + i];
                tstep(t, par, tw, k, ain, rin, tout); nd++;
                for (int i = 0; i < k; i++) { int x = h2 - k + i; if (tout[i] != O[x] + O[n2 - 1 - x]) { bad_d++; break; } }
            }
        }
        if (tau >= 0) {
            int wc[64], oc[64]; for (int i = 0; i < K; i++) wc[i] = 2 * BS - 2 - w[i];
            int tc = (t + tau) % Pp, jc = (j + sig) % MM;
            bool b1 = fstep(tc, jc, par, wc, K, q, oc); ne++;
            if (a1 != b1) bad_e++;
            else if (a1) { alive_e++; for (int i = 0; i < K; i++) if (oc[i] != 2 * BS - 2 - o1[i]) { bad_e++; break; } }
        }
    }
    printf("(c) fold map with q and q+2 bulk periods: %lld samples, mismatches %lld\n", nc, bad_c);
    printf("(d) top relaxation rule vs genuine step: %lld samples, mismatches %lld\n", nd, bad_d);
    if (tau >= 0) printf("(e) complement symmetry (t+%d, j+%d, 18-w) commutes with the fold map: %lld samples (%lld alive), mismatches %lld\n", tau, sig, ne, alive_e, bad_e);
    return 0;
}

static int mode_cmp(int argc, char** argv) {
    vector<u128> a = readk(argv[2]), b = readk(argv[3]); sort(a.begin(), a.end()); sort(b.begin(), b.end());
    if (argc > 4) {   // restrict file 2 to the phases that occur in file 1 (key >> PS, PS = argv[4])
        int ps = atoi(argv[4]); vector<unsigned> ph; for (auto k : a) ph.push_back((unsigned)(k >> ps)); sort(ph.begin(), ph.end()); ph.erase(unique(ph.begin(), ph.end()), ph.end());
        vector<u128> b2; for (auto k : b) if (binary_search(ph.begin(), ph.end(), (unsigned)(k >> ps))) b2.push_back(k); b.swap(b2);
        printf("(file 2 restricted to the %zu phases of file 1)\n", ph.size());
    }
    vector<u128> ab, ba; set_difference(a.begin(), a.end(), b.begin(), b.end(), back_inserter(ab)); set_difference(b.begin(), b.end(), a.begin(), a.end(), back_inserter(ba));
    printf("CMP %s (%zu) vs %s (%zu): only-in-1 %zu, only-in-2 %zu => %s\n", argv[2], a.size(), argv[3], b.size(), ab.size(), ba.size(), (ab.empty() && ba.empty()) ? "EQUAL" : "DIFFERENT");
    return 0;
}

int main(int argc, char** argv) {
    if (argc < 3) { fprintf(stderr, "see header\n"); return 1; }
    string m = argv[1];
    if (m == "cmp") return mode_cmp(argc, argv);
    load_rows(argv[2]);
    if (m == "selftest") return mode_selftest(argc, argv);
    if (m == "core") return mode_core(argc, argv);
    if (m == "topcore") return mode_topcore(argc, argv);
    if (m == "fold") return mode_fold(argc, argv);
    if (m == "fwd") return mode_fwd(argc, argv);
    fprintf(stderr, "unknown mode\n"); return 1;
}
