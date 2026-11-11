// r12g kfwd: complete search for periodic centres ("kinks") of depth <= K, ANY time period, by forward image iteration.
//
// F = exact fold step of the top K-window [h-K, h) (lattice exact below h-K), Z = {states whose bottom K-k cells lie in the
// relaxation cyclic set Cyc(K-k)} (Z = everything if k = K).  Every periodic orbit of F (= every centre of depth <= K) lies in
// Cyc(K) subset Z and passes through every phase of its phase orbit, in particular through phi0.  Iterate
//     A_0 = Z(phi0) (genuine states only: even middle cell when n is odd),   A_{n+1} = F(A_n) cap Z(phi_{n+1}).
// Then A_{n+Lo} subset A_n (Lo = phase orbit length), every periodic orbit meets every A_n, and
//   A_n empty            => no periodic orbit of F through this phase class (no centre of depth <= K in this class);
//   A_{n+Lo} == A_n != {} => every state of A_n is periodic (printed, then classified lattice / non-lattice).
// With k = K the last non-empty n is the exact maximal lifetime of a free top-K window from phase phi0 (survscan "lifetime").
//
// usage: kfwd lat.tbl K k FILTER|- t0 j0 par0 [maxsteps] [threads] [trace] [TOPFILE Kt]
//   TOPFILE: ktop cyclic set TopCyc(Kt), Kt <= k: the top Kt cells must lie in it at every step (sound: every centre's top window does).
//   FILTER: kink6/kink7 binary cyclic set of depth K-k ('-' if k == K).  trace=1: keep all A_n and print one longest-lived
//   initial window (for a big-integer replay of the lifetime).
#include "kcommon.h"

int K, kfree, Kf, PSf;
KeyIndex FI;
KeyIndex TI; int Kt = 0;            // optional top filter TopCyc(Kt) (ktop format: (t*2+par)<<100 | cells, cell 0 = h-Kt)
std::vector<ll> phlo, phhi;   // filter key range per phase

static inline bool in_top(int t, int par, const int* w) {
    if (Kt == 0) return true;
    return TI.find(((u128)(unsigned)(t * 2 + par) << 100) | enc_cells(w + (K - Kt), Kt)) >= 0;
}
static inline bool in_filter(int t, int j, int par, const int* w) {
    if (!in_top(t, par, w)) return false;
    if (Kf == 0) return true;
    return FI.find(enc(t, j, par, w, Kf, PSf)) >= 0;
}
// apply F to window w at phase (t,j,par); returns false if the lattice breaks or the image leaves Z
static inline bool Fstep(int t, int j, int par, const int* w, int* nw) {
    if (!exact_step(K, t, j, par, w, nw)) return false;
    int t2, j2, p2; next_phase(t, j, par, t2, j2, p2);
    return in_filter(t2, j2, p2, nw);
}

int main(int argc, char** argv) {
    if (argc < 8) { fprintf(stderr, "usage: kfwd lat.tbl K k FILTER|- t0 j0 par0 [maxsteps] [threads] [trace]\n"); return 1; }
    load_tbl(argv[1]); K = atoi(argv[2]); kfree = atoi(argv[3]); Kf = K - kfree;
    const char* ffn = argv[4]; int t0 = atoi(argv[5]), j0 = atoi(argv[6]), p0 = atoi(argv[7]);
    int maxsteps = argc > 8 ? atoi(argv[8]) : 4000; int T = argc > 9 ? atoi(argv[9]) : 4; int trace = argc > 10 ? atoi(argv[10]) : 0;
    const char* tfn = argc > 12 ? argv[11] : nullptr; if (tfn) Kt = atoi(argv[12]);
    if (K > 25 || kfree < 0 || Kf < 0 || Kt > kfree) { fprintf(stderr, "bad K/k/Kt (need Kt <= k)\n"); return 1; }
    double T0 = now_s();
    PSf = PSof(Kf);
    if (Kf > 0) {
        FI.keys = read_keys(ffn);
        if (!std::is_sorted(FI.keys.begin(), FI.keys.end())) { fprintf(stderr, "filter not sorted\n"); return 1; }
        FI.build();
    }
    std::vector<u128> topset;   // TopCyc(Kt) cells at phase (t0,p0), used to enumerate the top Kt cells of A_0
    if (Kt > 0) {
        TI.keys = read_keys(tfn); std::sort(TI.keys.begin(), TI.keys.end()); TI.build();
        u128 m100 = ((u128)1 << 100) - 1;
        for (auto k : TI.keys) if ((unsigned)(k >> 100) == (unsigned)(t0 * 2 + p0)) topset.push_back(k & m100);
    }
    // phase orbit of phi0
    int Lo = 0; { int t = t0, j = j0, p = p0; do { int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; Lo++; } while (!(t == t0 && j == j0 && p == p0)); }
    printf("kfwd base=%d P=%d M=%d K=%d k=%d filterdepth=%d filterkeys=%zu phi0=(%d,%d,%d) orbitlen=%d threads=%d\n",
           B_, P_, M_, K, kfree, Kf, FI.keys.size(), t0, j0, p0, Lo, T);
    // ---- A_1 from the streamed A_0
    ll blo = 0, bhi = 1;
    if (Kf > 0) {
        u128 ph = (u128)phase_id(t0, j0, p0) << PSf;
        blo = std::lower_bound(FI.keys.begin(), FI.keys.end(), ph) - FI.keys.begin();
        bhi = std::lower_bound(FI.keys.begin(), FI.keys.end(), ph + ((u128)1 << PSf)) - FI.keys.begin();
    }
    ll nb = bhi - blo; ll nfree = 1; for (int i = 0; i < kfree - Kt; i++) nfree *= D_;
    ll ntop = nfree * (Kt > 0 ? (ll)topset.size() : 1);
    ll N0 = nb * ntop;
    printf("A_0: bottom states %lld x top %lld = %lld (before the parity filter; top filter depth %d, %zu top states at phi0)\n", nb, ntop, N0, Kt, topset.size()); fflush(stdout);
    // A_0 is streamed in chunks (env KFWD_CHUNK = log2 chunk size, default 27); each chunk is iterated alone for s0 steps
    // (env KFWD_S0, default 8) and the results are merged: F is deterministic and the filters are pointwise, so the union of
    // the chunk images after s0 steps is exactly A_{s0}.  trace=1 forces one chunk and s0 = 1.
    ll CH = 1LL << (getenv("KFWD_CHUNK") ? atoi(getenv("KFWD_CHUNK")) : 27);
    int s0 = getenv("KFWD_S0") ? atoi(getenv("KFWD_S0")) : 8;
    if (trace) { CH = std::max<ll>(N0, 1); s0 = 1; }
    if (s0 < 1) s0 = 1;
    auto step_set = [&](std::vector<u128>& Aset, int tt, int jj, int pp) {
        std::vector<std::vector<u128>> lo2(T); size_t NA = Aset.size(); std::vector<std::thread> th;
        for (int q = 0; q < T; q++) th.emplace_back([&, q] {
            size_t a0 = NA * q / T, a1 = NA * (q + 1) / T; int w[64], nw[64];
            for (size_t i = a0; i < a1; i++) { dec_cells(Aset[i], w, K); if (Fstep(tt, jj, pp, w, nw)) lo2[q].push_back(enc_cells(nw, K)); }
        });
        for (auto& x : th) x.join();
        std::vector<u128> B2; { size_t tot = 0; for (auto& v : lo2) tot += v.size(); B2.reserve(tot); for (auto& v : lo2) { B2.insert(B2.end(), v.begin(), v.end()); std::vector<u128>().swap(v); } }
        psort_unique(B2, T); Aset.swap(B2);
    };
    std::atomic<ll> n0genuine(0);
    std::vector<u128> A; std::vector<ll> chunksum(s0 + 1, 0); ll lastnonempty = 0; ll nchunks = 0;
    for (ll c0 = 0; c0 < N0; c0 += CH) {
        ll c1 = std::min(N0, c0 + CH); nchunks++;
        std::vector<std::vector<u128>> loc(T);
        std::vector<std::thread> th;
        for (int q = 0; q < T; q++) th.emplace_back([&, q] {
            ll lo = c0 + (c1 - c0) * q / T, hi = c0 + (c1 - c0) * (q + 1) / T, gen = 0;
            int w[64], nw[64];
            auto& out = loc[q];
            for (ll x = lo; x < hi; x++) {
                ll bi = x / ntop, ti = x % ntop;
                if (Kf > 0) dec_cells(FI.keys[blo + bi], w, Kf);
                for (int i = 0; i < kfree - Kt; i++) { w[Kf + i] = (int)(ti % D_); ti /= D_; }
                if (Kt > 0) dec_cells(topset[ti], w + (K - Kt), Kt);
                if (p0 == 1 && (w[K - 1] & 1)) continue;          // odd n: the middle pair cell is 2*digit
                gen++;
                if (Fstep(t0, j0, p0, w, nw)) out.push_back(enc_cells(nw, K));
                if (out.size() > (1u << 26)) { std::sort(out.begin(), out.end()); out.erase(std::unique(out.begin(), out.end()), out.end()); }
            }
            n0genuine += gen;
        });
        for (auto& x : th) x.join();
        std::vector<u128> Bc;
        { size_t tot = 0; for (auto& v : loc) tot += v.size(); Bc.reserve(tot); for (auto& v : loc) { Bc.insert(Bc.end(), v.begin(), v.end()); std::vector<u128>().swap(v); } }
        psort_unique(Bc, T);
        int tt = t0, jj = j0, pp = p0; { int a, b, c; next_phase(tt, jj, pp, a, b, c); tt = a; jj = b; pp = c; }
        int s = 1; chunksum[1] += Bc.size(); if (!Bc.empty()) lastnonempty = std::max<ll>(lastnonempty, 1);
        while (s < s0 && !Bc.empty()) {
            step_set(Bc, tt, jj, pp); { int a, b, c; next_phase(tt, jj, pp, a, b, c); tt = a; jj = b; pp = c; }
            s++; chunksum[s] += Bc.size(); if (!Bc.empty()) lastnonempty = std::max<ll>(lastnonempty, s);
        }
        if (s == s0) A.insert(A.end(), Bc.begin(), Bc.end());
        if (nchunks % 16 == 1 || c1 == N0) { printf("  chunk %lld [%lld,%lld) done, acc %zu  [%.1fs]\n", nchunks, c0, c1, A.size(), now_s() - T0); fflush(stdout); }
        if (A.size() > (1u << 27)) psort_unique(A, T);
    }
    psort_unique(A, T);
    int t = t0, j = j0, p = p0; for (int s = 0; s < s0; s++) { int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; }
    printf("STEP 0 size %lld (genuine), %lld chunks\n", (ll)n0genuine, nchunks);
    for (int s = 1; s < s0; s++) printf("STEP %d size <= %lld (sum over chunks)\n", s, chunksum[s]);
    printf("STEP %d size %zu  [%.1fs]\n", s0, A.size(), now_s() - T0); fflush(stdout);
    std::vector<std::vector<u128>> hist; if (trace) hist.push_back(A);
    std::vector<u128> prev0; bool have_prev0 = false; int n = s0; if (!A.empty()) lastnonempty = s0;
    bool stable = false, nest_ok = true;
    while (!A.empty() && n < maxsteps) {
        std::vector<std::vector<u128>> lo2(T);
        size_t NA = A.size();
        std::vector<std::thread> th;
        for (int q = 0; q < T; q++) th.emplace_back([&, q] {
            size_t a0 = NA * q / T, a1 = NA * (q + 1) / T; int w[64], nw[64];
            for (size_t i = a0; i < a1; i++) { dec_cells(A[i], w, K); if (Fstep(t, j, p, w, nw)) lo2[q].push_back(enc_cells(nw, K)); }
        });
        for (auto& x : th) x.join();
        std::vector<u128> B2; { size_t tot = 0; for (auto& v : lo2) tot += v.size(); B2.reserve(tot); for (auto& v : lo2) B2.insert(B2.end(), v.begin(), v.end()); }
        psort_unique(B2, T);
        A.swap(B2); n++;
        { int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; }
        if (!A.empty()) lastnonempty = n;
        if (n < 400 || n % 40 == 0 || A.size() < 1000) { printf("STEP %d size %zu  [%.1fs]\n", n, A.size(), now_s() - T0); fflush(stdout); }
        if (trace) hist.push_back(A);
        if (n % Lo == 0) {
            if (!(t == t0 && j == j0 && p == p0)) { printf("PHASE BUG\n"); return 2; }
            if (have_prev0) {
                if (!std::includes(prev0.begin(), prev0.end(), A.begin(), A.end())) { nest_ok = false; printf("NESTING VIOLATED at %d\n", n); }
                if (A == prev0 && !A.empty()) { stable = true; break; }
            }
            prev0 = A; have_prev0 = true;
        }
    }
    if (A.empty()) printf("EMPTY at step %d: no periodic orbit through phase class of (%d,%d,%d); max lifetime from phi0 = %lld steps; nesting_ok=%d [%.1fs]\n",
                          n, t0, j0, p0, lastnonempty, (int)nest_ok, now_s() - T0);
    else if (!stable) printf("UNDECIDED: maxsteps %d reached with |A| = %zu [%.1fs]\n", n, A.size(), now_s() - T0);
    else {
        printf("STABLE at step %d: %zu periodic states at phi0\n", n, A.size());
        std::vector<char> seen(A.size(), 0); int norb = 0;
        for (size_t i = 0; i < A.size(); i++) {
            if (seen[i]) continue;
            int w[64], nw[64]; dec_cells(A[i], w, K); int tt = t0, jj = j0, pp = p0; ll len = 0; bool nonlat = false;
            u128 cur = A[i];
            do {
                for (int q = 0; q < K; q++) if (w[q] != L[tt][md(jj + q, M_)]) nonlat = true;
                if (!Fstep(tt, jj, pp, w, nw)) { printf("  orbit broke (bug)\n"); break; }
                int a, b, c; next_phase(tt, jj, pp, a, b, c); tt = a; jj = b; pp = c; memcpy(w, nw, sizeof(int) * K); len++;
                cur = enc_cells(w, K);
                if (tt == t0 && jj == j0 && pp == p0) { auto it = std::lower_bound(A.begin(), A.end(), cur); if (it != A.end() && *it == cur) seen[it - A.begin()] = 1; }
            } while (!(cur == A[i] && tt == t0 && jj == j0 && pp == p0) && len < 100000000);
            norb++;
            dec_cells(A[i], w, K);
            printf("  PERIODIC ORBIT %d: period %lld %s; state at phi0:", norb, len, nonlat ? "NON-LATTICE" : "all-lattice");
            for (int q = 0; q < K; q++) printf(" %d", w[q]);
            printf("\n");
        }
    }
    if (trace && lastnonempty >= 1 && !hist.empty() && !stable) {
        // backtrack one longest-lived chain: hist[m] = A_{m+1}
        int Lm = (int)lastnonempty;
        std::vector<u128> chain(Lm + 1);
        chain[Lm] = hist[Lm - 1][0];
        // phases along the way
        std::vector<int> pt(Lm + 1), pj(Lm + 1), pp(Lm + 1); pt[0] = t0; pj[0] = j0; pp[0] = p0;
        for (int m = 0; m < Lm; m++) next_phase(pt[m], pj[m], pp[m], pt[m + 1], pj[m + 1], pp[m + 1]);
        for (int m = Lm - 1; m >= 1; m--) {
            bool found = false; int w[64], nw[64];
            for (auto s : hist[m - 1]) { dec_cells(s, w, K); if (Fstep(pt[m], pj[m], pp[m], w, nw) && enc_cells(nw, K) == chain[m + 1]) { chain[m] = s; found = true; break; } }
            if (!found) { printf("TRACE failed at %d\n", m); return 3; }
        }
        bool found = false; int w[64], nw[64];
        for (ll x = 0; x < N0 && !found; x++) {
            ll bi = x / ntop, ti = x % ntop;
            if (Kf > 0) dec_cells(FI.keys[blo + bi], w, Kf);
            for (int i = 0; i < kfree - Kt; i++) { w[Kf + i] = (int)(ti % D_); ti /= D_; }
            if (Kt > 0) dec_cells(topset[ti], w + (K - Kt), Kt);
            if (p0 == 1 && (w[K - 1] & 1)) continue;
            if (Fstep(t0, j0, p0, w, nw) && enc_cells(nw, K) == chain[1]) { chain[0] = enc_cells(w, K); found = true; }
        }
        if (!found) { printf("TRACE failed at 0\n"); return 3; }
        dec_cells(chain[0], w, K);
        printf("LONGEST t=%d j=%d par=%d lifetime=%d window", t0, j0, p0, Lm);
        for (int q = 0; q < K; q++) printf(" %d", w[q]);
        printf("\n");
    }
    printf("DONE [%.1fs]\n", now_s() - T0);
    return 0;
}
