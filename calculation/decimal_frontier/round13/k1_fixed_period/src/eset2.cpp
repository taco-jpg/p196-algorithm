// r13b eset2: E(K,T) = states of the bottom relaxation R_K on a closed walk of length exactly T (T = L*Lo, Lo = phase orbit length),
// built incrementally: E(K,T) subset E(K-1,T) x {0..18} (projection lemma). One phase orbit. Keys: WORDS x u64, 12 cells/word, 5 bits/cell.
//   usage: eset2 lat.tbl orbit L Kmax OUTDIR [-threads N] [-from K0 FILE] [-noE] [-walks] [-save] [-savefrom K] [-foldstats]
// Rule: kcommon.h wstep (validated by r12g), candidate = (parent index)*D + top cell (implicit indexing, as kink7).
// Pipeline per level: bitset trim (forward/backward sweeps) -> CSR graph -> per-source 64-bit batches forward+backward through
// T unrolled layers -> E(K,T) -> exact fold-map orbit check inside E.
#include "kcommon.h"
#include <cmath>
#include <map>
#ifndef WORDS
#define WORDS 4
#endif
typedef unsigned long long ull;
struct Key { uint64_t w[WORDS]; bool operator==(const Key& o) const { for (int i = 0; i < WORDS; i++) if (w[i] != o.w[i]) return false; return true; } bool operator<(const Key& o) const { for (int i = WORDS - 1; i >= 0; i--) if (w[i] != o.w[i]) return w[i] < o.w[i]; return false; } };
static inline Key enc_k(const int* c, int K) { Key k; memset(&k, 0, sizeof k); for (int i = 0; i < K; i++) k.w[i / 12] |= (uint64_t)c[i] << (5 * (i % 12)); return k; }
static inline void dec_k(const Key& k, int* c, int K) { for (int i = 0; i < K; i++) c[i] = (int)((k.w[i / 12] >> (5 * (i % 12))) & 31); }
static inline Key with_top(Key k, int K, int x) { k.w[(K - 1) / 12] |= (uint64_t)x << (5 * ((K - 1) % 12)); return k; }
static inline uint64_t hk(const Key& k) { uint64_t h = 0; for (int i = 0; i < WORDS; i++) h = mix64(h ^ mix64(k.w[i] + 0x1234567ULL * i)); return h; }
struct Idx {
    std::vector<Key> keys; std::vector<uint32_t> slot; uint64_t mask = 0;
    void build() {
        uint64_t n = keys.size(), cap = 1; while (cap < 2 * n + 16) cap <<= 1;
        slot.assign(cap, 0); mask = cap - 1;
        for (uint64_t i = 0; i < n; i++) { uint64_t h = hk(keys[i]) & mask; while (slot[h]) h = (h + 1) & mask; slot[h] = (uint32_t)(i + 1); }
    }
    inline ll find(const Key& k) const { uint64_t h = hk(k) & mask; while (true) { uint32_t s = slot[h]; if (!s) return -1; if (keys[s - 1] == k) return (ll)(s - 1); h = (h + 1) & mask; } }
};
struct Layer { int t, j, par, g, dh; Idx PI; std::vector<uint64_t> alive, mark; uint64_t Nc = 0; };
static std::vector<Layer> Ls;
static int Lo, THR = 8;
static bool noE = false, doWalks = false, doSave = false, doFoldStats = false; static int saveFrom = 1;
static inline bool bget(const std::vector<uint64_t>& b, uint64_t i) { return (b[i >> 6] >> (i & 63)) & 1; }
static inline void bset_at(std::vector<uint64_t>& b, uint64_t i) { __atomic_fetch_or(&b[i >> 6], 1ULL << (i & 63), __ATOMIC_RELAXED); }
static inline void bclr_at(std::vector<uint64_t>& b, uint64_t i) { __atomic_fetch_and(&b[i >> 6], ~(1ULL << (i & 63)), __ATOMIC_RELAXED); }
template <class F> static void parfor(uint64_t n, F f, uint64_t grain = 1ULL << 14) {
    if (n <= grain || THR <= 1) { f(0, n); return; }
    uint64_t chunks = std::max<uint64_t>(n / grain, 1); chunks = std::min<uint64_t>(chunks, THR * 256ULL);
    std::atomic<uint64_t> nx(0); std::vector<std::thread> th;
    for (int i = 0; i < THR; i++) th.emplace_back([&] { uint64_t c; while ((c = nx.fetch_add(1)) < chunks) f(n * c / chunks, n * (c + 1) / chunks); });
    for (auto& x : th) x.join();
}
static inline int succs(int l, uint64_t c, int K, int64_t* out) {
    Layer& A = Ls[l]; int nl = (l + 1) % Lo; Layer& B = Ls[nl];
    int w[64], nw[65]; uint64_t i = c / D_; int x = c % D_;
    dec_k(A.PI.keys[i], w, K - 1); w[K - 1] = x;
    int cnt = 0;
    for (int Din = 0; Din < 2; Din++) {
        if (!wstep(K, A.t, A.j, w, Din, A.dh, 0, nw)) continue;
        ll pi = B.PI.find(enc_k(nw, K - 1));
        if (pi < 0) continue;
        if (A.dh) { int top0 = nw[K - 1]; for (int tv = 0; tv < B_; tv++) { int top = top0 + tv; if (top >= D_) continue; out[cnt++] = pi * (int64_t)D_ + top; } }
        else out[cnt++] = pi * (int64_t)D_ + nw[K - 1];
    }
    return cnt;
}
struct CSR { std::vector<uint32_t> off, ed; uint32_t n = 0; };
int main(int argc, char** argv) {
    if (argc < 6) { fprintf(stderr, "usage: eset2 lat.tbl orbit L Kmax OUTDIR [-threads N] [-from K0 FILE] [-noE] [-walks] [-save] [-savefrom K] [-foldstats]\n"); return 1; }
    load_tbl(argv[1]); int which = atoi(argv[2]); int LL = atoi(argv[3]); int Kmax = atoi(argv[4]); std::string outdir = argv[5];
    int K0 = 0; std::string fromfn;
    for (int i = 6; i < argc; i++) {
        std::string a = argv[i];
        if (a == "-threads") THR = atoi(argv[++i]); else if (a == "-from") { K0 = atoi(argv[++i]); fromfn = argv[++i]; }
        else if (a == "-noE") noE = true; else if (a == "-walks") doWalks = true; else if (a == "-save") doSave = true; else if (a == "-foldstats") doFoldStats = true; else if (a == "-savefrom") saveFrom = atoi(argv[++i]);
    }
    if (Kmax > 12 * WORDS) { fprintf(stderr, "Kmax > %d\n", 12 * WORDS); return 1; }
    int NPH = 2 * P_ * M_; std::vector<int> orb(NPH, -1); int norb = 0; std::vector<int> reps;
    for (int s = 0; s < NPH; s++) {
        if (orb[s] >= 0) continue; reps.push_back(s);
        int t, j, p; phase_dec(s, t, j, p); int x = s;
        do { orb[x] = norb; int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; x = phase_id(t, j, p); } while (x != s);
        norb++;
    }
    int t, j, p; phase_dec(reps[which], t, j, p);
    { int x = reps[which]; do { Layer A; A.t = t; A.j = j; A.par = p; A.g = G[t]; A.dh = (A.g == 1 && p == 0); Ls.push_back(std::move(A)); int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; x = phase_id(t, j, p); } while (x != reps[which]); }
    Lo = Ls.size(); int TT = LL * Lo;
    fprintf(stderr, "eset2 orbit %d/%d Lo=%d T=%d Kmax=%d threads=%d WORDS=%d\n", which, norb, Lo, TT, Kmax, THR, WORDS);
    int Kstart = 1;
    if (K0 > 0) {
        FILE* f = fopen(fromfn.c_str(), "rb"); if (!f) { perror("from"); return 1; }
        int lo2; fread(&lo2, 4, 1, f); int wds; fread(&wds, 4, 1, f); if (lo2 != Lo || wds != WORDS) { fprintf(stderr, "header mismatch Lo %d Words %d\n", lo2, wds); return 1; }
        for (int l = 0; l < Lo; l++) { uint64_t n; fread(&n, 8, 1, f); Ls[l].PI.keys.resize(n); fread(Ls[l].PI.keys.data(), sizeof(Key), n, f); }
        fclose(f); Kstart = K0 + 1;
    } else for (int l = 0; l < Lo; l++) { Key z; memset(&z, 0, sizeof z); Ls[l].PI.keys.assign(1, z); }
    double Tstart = now_s();
    for (int K = Kstart; K <= Kmax; K++) {
        double T0 = now_s();
        uint64_t Ntot = 0;
        for (int l = 0; l < Lo; l++) {
            Layer& A = Ls[l]; A.PI.build();
            A.Nc = A.PI.keys.size() * (uint64_t)D_;
            A.alive.assign((A.Nc + 63) / 64, ~0ULL); if (A.Nc % 64) A.alive.back() = (1ULL << (A.Nc % 64)) - 1;
            Ntot += A.Nc;
        }
        std::atomic<bool> changed(true); int round = 0;
        while (changed && round < 400) {
            changed = false; round++;
            for (int l = 0; l < Lo; l++) {
                int nl = (l + 1) % Lo; Layer& A = Ls[l]; Layer& B = Ls[nl];
                B.mark.assign(B.alive.size(), 0ULL);
                parfor(A.Nc, [&](uint64_t lo, uint64_t hi) {
                    int64_t out[64];
                    for (uint64_t c = lo; c < hi; c++) if (bget(A.alive, c)) { int n = succs(l, c, K, out); for (int q = 0; q < n; q++) bset_at(B.mark, out[q]); }
                });
                for (size_t w = 0; w < B.alive.size(); w++) { uint64_t a = B.alive[w] & B.mark[w]; if (a != B.alive[w]) changed = true; B.alive[w] = a; }
            }
            for (int l = Lo - 1; l >= 0; l--) {
                int nl = (l + 1) % Lo; Layer& A = Ls[l]; Layer& B = Ls[nl];
                std::atomic<bool> ch(false);
                parfor(A.Nc, [&](uint64_t lo, uint64_t hi) {
                    int64_t out[64];
                    for (uint64_t c = lo; c < hi; c++) if (bget(A.alive, c)) {
                        int n = succs(l, c, K, out); bool has = false; for (int q = 0; q < n && !has; q++) if (bget(B.alive, out[q])) has = true;
                        if (!has) { bclr_at(A.alive, c); ch = true; }
                    }
                });
                if (ch) changed = true;
            }
        }
        double Ttrim = now_s() - T0;
        uint64_t Nalive = 0; std::vector<CSR> G_(Lo); std::vector<std::vector<uint32_t>> rankw(Lo);
        for (int l = 0; l < Lo; l++) {
            Layer& A = Ls[l]; rankw[l].resize(A.alive.size() + 1); uint32_t s = 0;
            for (size_t w = 0; w < A.alive.size(); w++) { rankw[l][w] = s; s += __builtin_popcountll(A.alive[w]); }
            rankw[l][A.alive.size()] = s; G_[l].n = s; Nalive += s; std::vector<uint64_t>().swap(A.mark);
        }
        auto rk = [&](int l, uint64_t c) -> uint32_t { const auto& a = Ls[l].alive; uint64_t w = c >> 6; return rankw[l][w] + __builtin_popcountll(a[w] & ((1ULL << (c & 63)) - 1)); };
        uint64_t Nedges = 0;
        for (int l = 0; l < Lo; l++) {
            int nl = (l + 1) % Lo; Layer& A = Ls[l]; CSR& C = G_[l];
            C.off.assign((size_t)C.n + 1, 0);
            std::vector<uint32_t> deg(C.n, 0);
            parfor(A.Nc, [&](uint64_t lo, uint64_t hi) {
                int64_t out[64];
                for (uint64_t c = lo; c < hi; c++) if (bget(A.alive, c)) {
                    int n = succs(l, c, K, out); int d = 0; std::sort(out, out + n);
                    for (int q = 0; q < n; q++) if ((q == 0 || out[q] != out[q - 1]) && bget(Ls[nl].alive, out[q])) d++;
                    deg[rk(l, c)] = d;
                }
            });
            for (uint32_t v = 0; v < C.n; v++) C.off[v + 1] = C.off[v] + deg[v];
            C.ed.resize(C.off[C.n]); Nedges += C.ed.size();
            parfor(A.Nc, [&](uint64_t lo, uint64_t hi) {
                int64_t out[64];
                for (uint64_t c = lo; c < hi; c++) if (bget(A.alive, c)) {
                    int n = succs(l, c, K, out); std::sort(out, out + n); uint32_t v = rk(l, c); uint32_t p = C.off[v];
                    for (int q = 0; q < n; q++) if ((q == 0 || out[q] != out[q - 1]) && bget(Ls[nl].alive, out[q])) C.ed[p++] = rk(nl, out[q]);
                }
            });
        }
        double Tcsr = now_s() - T0 - Ttrim;
        int anc = 0; for (int l = 1; l < Lo; l++) if (G_[l].n < G_[anc].n) anc = l;
        uint64_t Nanchor = G_[anc].n, maxlayer = 0; for (int l = 0; l < Lo; l++) maxlayer = std::max<uint64_t>(maxlayer, G_[l].n);
        std::vector<std::vector<uint64_t>> onw(Lo);
        for (int l = 0; l < Lo; l++) onw[l].assign((G_[l].n + 63) / 64, noE ? ~0ULL : 0ULL);
        uint64_t Nclosed = Nanchor;
        if (!noE && Nanchor) {
            uint64_t batches = (Nanchor + 63) / 64;
            std::atomic<uint64_t> nx(0), closedcnt(0);
            std::vector<std::thread> th;
            for (int ti = 0; ti < THR; ti++) th.emplace_back([&] {
                std::vector<std::vector<uint64_t>> Fu(TT + 1), Bu(TT + 1);
                for (int k = 0; k <= TT; k++) { int l = (anc + k) % Lo; Fu[k].assign(G_[l].n, 0ULL); Bu[k].assign(G_[l].n, 0ULL); }
                uint64_t b;
                while ((b = nx.fetch_add(1)) < batches) {
                    uint64_t s0 = b * 64, s1 = std::min<uint64_t>(s0 + 64, Nanchor);
                    for (int k = 0; k <= TT; k++) std::fill(Fu[k].begin(), Fu[k].end(), 0ULL);
                    for (uint64_t s = s0; s < s1; s++) Fu[0][s] = 1ULL << (s - s0);
                    for (int k = 0; k < TT; k++) {
                        int l = (anc + k) % Lo; CSR& C = G_[l]; const uint64_t* Fk = Fu[k].data(); uint64_t* Fn = Fu[k + 1].data();
                        for (uint32_t x = 0; x < C.n; x++) { uint64_t fx = Fk[x]; if (!fx) continue; for (uint32_t q = C.off[x]; q < C.off[x + 1]; q++) Fn[C.ed[q]] |= fx; }
                    }
                    uint64_t closed = 0;
                    for (uint64_t s = s0; s < s1; s++) if (Fu[TT][s] >> (s - s0) & 1ULL) closed |= 1ULL << (s - s0);
                    closedcnt.fetch_add(__builtin_popcountll(closed));
                    if (!closed) continue;
                    for (int k = 0; k <= TT; k++) std::fill(Bu[k].begin(), Bu[k].end(), 0ULL);
                    for (uint64_t s = s0; s < s1; s++) if (closed >> (s - s0) & 1ULL) Bu[TT][s] = 1ULL << (s - s0);
                    for (int k = TT - 1; k >= 0; k--) {
                        int l = (anc + k) % Lo; CSR& C = G_[l]; const uint64_t* Bn = Bu[k + 1].data(); uint64_t* Bk2 = Bu[k].data();
                        for (uint32_t x = 0; x < C.n; x++) { uint64_t bx = 0; for (uint32_t q = C.off[x]; q < C.off[x + 1]; q++) bx |= Bn[C.ed[q]]; Bk2[x] = bx; }
                    }
                    for (int k = 0; k < TT; k++) {
                        int l = (anc + k) % Lo; auto& ow = onw[l]; const uint64_t* Fx = Fu[k].data(); const uint64_t* Bx = Bu[k].data();
                        for (uint32_t x = 0; x < G_[l].n; x++) if (Fx[x] & Bx[x]) __atomic_fetch_or(&ow[x >> 6], 1ULL << (x & 63), __ATOMIC_RELAXED);
                    }
                }
            });
            for (auto& x : th) x.join();
            Nclosed = closedcnt;
        } else if (noE) {
            for (int l = 0; l < Lo; l++) if (G_[l].n % 64) onw[l].back() = (1ULL << (G_[l].n % 64)) - 1;
        }
        double Tfilter = now_s() - T0 - Ttrim - Tcsr;
        uint64_t Etot = 0; ll nacc = 0;
        for (int l = 0; l < Lo; l++) for (auto w : onw[l]) Etot += __builtin_popcountll(w);
        if (doWalks && !noE) {
            long double Wtot = 0, Wmax = 0;
            std::atomic<uint64_t> nx(0); std::vector<std::thread> th;
            std::vector<long double> res(THR, 0), res2(THR, 0);
            for (int ti = 0; ti < THR; ti++) th.emplace_back([&, ti] {
                std::vector<std::vector<long double>> C_(TT + 1); for (int k = 0; k <= TT; k++) C_[k].assign(G_[(anc + k) % Lo].n, 0.0L);
                uint64_t s;
                while ((s = nx.fetch_add(1)) < Nanchor) {
                    for (int k = 0; k <= TT; k++) std::fill(C_[k].begin(), C_[k].end(), 0.0L);
                    C_[0][s] = 1.0L;
                    for (int k = 0; k < TT; k++) { int l = (anc + k) % Lo; CSR& C = G_[l]; for (uint32_t x = 0; x < C.n; x++) { long double v = C_[k][x]; if (v == 0.0L) continue; for (uint32_t q = C.off[x]; q < C.off[x + 1]; q++) C_[k + 1][C.ed[q]] += v; } }
                    res[ti] += C_[TT][s]; res2[ti] = std::max(res2[ti], C_[TT][s]);
                }
            });
            for (auto& x : th) x.join();
            for (int i = 0; i < THR; i++) { Wtot += res[i]; Wmax = std::max(Wmax, res2[i]); }
            printf("WALKS K=%d T=%d closed-walks-through-anchor-layer=%.6Le maxPerSource=%.6Le\n", K, TT, Wtot, Wmax);
        }
        // exact fold map orbit check inside E(K,T)
        ll exactOrbits = 0, succInside = 0;
        auto E_of = [&](int l, const int* w) -> bool {
            ll pi = Ls[l].PI.find(enc_k(w, K - 1)); if (pi < 0) return false;
            uint64_t c = pi * (uint64_t)D_ + w[K - 1]; if (!bget(Ls[l].alive, c)) return false;
            uint32_t v = rk(l, c); return (onw[l][v >> 6] >> (v & 63)) & 1;
        };
        if (doFoldStats) for (int l = 0; l < Lo; l++) for (uint64_t c = 0; c < Ls[l].Nc; c++) {
            if (!bget(Ls[l].alive, c)) continue; uint32_t v = rk(l, c); if (!((onw[l][v >> 6] >> (v & 63)) & 1)) continue;
            int w[64], nw[64]; uint64_t i = c / D_; dec_k(Ls[l].PI.keys[i], w, K - 1); w[K - 1] = c % D_;
            if (!exact_step(K, Ls[l].t, Ls[l].j, Ls[l].par, w, nw)) continue;
            if (E_of((l + 1) % Lo, nw)) succInside++;
        }
        for (uint64_t c = 0; c < Ls[anc].Nc; c++) {
            if (!bget(Ls[anc].alive, c)) continue; uint32_t v = rk(anc, c); if (!((onw[anc][v >> 6] >> (v & 63)) & 1)) continue;
            int w0[64], w[64], nw[64]; uint64_t i = c / D_; dec_k(Ls[anc].PI.keys[i], w0, K - 1); w0[K - 1] = c % D_;
            memcpy(w, w0, sizeof(int) * K); bool ok = true; int l = anc;
            for (int k = 0; k < TT && ok; k++) { if (!exact_step(K, Ls[l].t, Ls[l].j, Ls[l].par, w, nw)) { ok = false; break; } l = (l + 1) % Lo; if (!E_of(l, nw)) { ok = false; break; } memcpy(w, nw, sizeof(int) * K); }
            if (ok && memcmp(w, w0, sizeof(int) * K) == 0) {
                exactOrbits++; bool nonlat = false; for (int q = 0; q < K; q++) if (w0[q] != L[Ls[anc].t][md(Ls[anc].j + q, M_)]) nonlat = true;
                printf("EXACT FOLD ORBIT K=%d T=%d %s anchor layer %d (t=%d j=%d par=%d) win", K, TT, nonlat ? "NON-LATTICE" : "all-lattice", anc, Ls[anc].t, Ls[anc].j, Ls[anc].par); for (int q = 0; q < K; q++) printf(" %d", w0[q]); printf("\n"); fflush(stdout);
            }
        }
        double Tfold = now_s() - T0 - Ttrim - Tcsr - Tfilter;
        // accepting states (bottom cell off lattice), number of parents kept
        uint64_t parentsKept = 0;
        std::vector<std::vector<Key>> newp(Lo);
        for (int l = 0; l < Lo; l++) {
            auto& np = newp[l]; uint64_t lastp = ~0ULL;
            for (uint64_t c = 0; c < Ls[l].Nc; c++) if (bget(Ls[l].alive, c)) {
                uint32_t v = rk(l, c); if (!((onw[l][v >> 6] >> (v & 63)) & 1)) continue;
                uint64_t i = c / D_; int x = c % D_; if (i != lastp) { parentsKept++; lastp = i; }
                Key k = with_top(Ls[l].PI.keys[i], K, x); np.push_back(k);
                int w0 = (K == 1) ? x : (int)(k.w[0] & 31); if (w0 != L[Ls[l].t][Ls[l].j]) nacc++;
            }
        }
        uint64_t parentsTotal = 0; for (int l = 0; l < Lo; l++) parentsTotal += Ls[l].PI.keys.size();
        printf("K=%d T=%d Lo=%d orbit=%d parents=%llu parentsKept=%llu candidates=%llu trimmed(Core)=%llu edges=%llu anchor=%llu (layer %d; maxlayer %llu) closedSources=%llu E=%llu accepting=%lld foldSuccInE=%lld exactOrbits=%lld | rounds=%d trim %.1fs csr %.1fs filter %.1fs fold %.1fs total %.1fs (%.0fs)\n",
               K, TT, Lo, which, (ull)parentsTotal, (ull)parentsKept, (ull)Ntot, (ull)Nalive, (ull)Nedges, (ull)Nanchor, anc, (ull)maxlayer, (ull)Nclosed, (ull)Etot, nacc, succInside, exactOrbits, round, Ttrim, Tcsr, Tfilter, Tfold, now_s() - T0, now_s() - Tstart);
        fflush(stdout);
        if (Etot == 0) { printf("E(K=%d) EMPTY -> stop\n", K); break; }
        if (nacc == 0) { printf("ACCEPTING(K=%d) = 0: no closed T-walk through an accepting state => E(K') has no accepting states for K' >= K\n", K); fflush(stdout); }
        if (doSave && K >= saveFrom) {
            std::string fn = outdir + "/E_K" + std::to_string(K) + ".bin"; FILE* f = fopen(fn.c_str(), "wb"); fwrite(&Lo, 4, 1, f); int wds = WORDS; fwrite(&wds, 4, 1, f);
            for (int l = 0; l < Lo; l++) { uint64_t n = newp[l].size(); fwrite(&n, 8, 1, f); fwrite(newp[l].data(), sizeof(Key), n, f); } fclose(f);
        }
        for (int l = 0; l < Lo; l++) { Ls[l].PI.keys.swap(newp[l]); std::vector<Key>().swap(newp[l]); std::vector<uint64_t>().swap(Ls[l].alive); std::vector<uint32_t>().swap(Ls[l].PI.slot); }
    }
    return 0;
}
