// r12g kink7: kink6's incremental relaxation cyclic set, one phase orbit at a time, with implicit candidate indexing
// (candidate = (index of its bottom K-1 cells in Cyc(K-1)) * D + top cell) and a hash index instead of binary search.
// Same transition rule (kcommon.h wstep = kink6 wstep, any base), same exact-centre check inside Cyc(K).
// usage: kink7 lat.tbl K PREV OUT orbit       PREV = Cyc(K-1) file (kink6 format or a kink7 per-orbit file)
//   orbit = index (0..) of the phase orbit, orbits ordered by their smallest phase id.  OUT gets the cyclic states of
//   this orbit, sorted, kink6 key format (PS = 100 for K <= 20, 118 beyond).
#include "kcommon.h"
int K, PSp, PSn;
std::vector<unsigned> orbit_phases(int which, int& norb) {
    int NPH = 2 * P_ * M_; std::vector<int> orb(NPH, -1); norb = 0;
    for (int s = 0; s < NPH; s++) {
        if (orb[s] >= 0) continue;
        int t, j, p; phase_dec(s, t, j, p); int x = s;
        do { orb[x] = norb; int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; x = phase_id(t, j, p); } while (x != s);
        norb++;
    }
    std::vector<unsigned> r; for (int s = 0; s < NPH; s++) if (orb[s] == which) r.push_back(s);
    return r;
}
int main(int argc, char** argv) {
    if (argc < 6) { fprintf(stderr, "usage: kink7 lat.tbl K PREV OUT orbit [threads]\n"); return 1; }
    load_tbl(argv[1]); K = atoi(argv[2]); const char* pfn = argv[3]; const char* ofn = argv[4]; int which = atoi(argv[5]);
    int T = argc > 6 ? atoi(argv[6]) : 1;
    PSp = PSof(K - 1); PSn = PSof(K);
    double T0 = now_s();
    int norb; std::vector<unsigned> ph = orbit_phases(which, norb);
    std::vector<char> inorb(2 * P_ * M_, 0); for (auto s : ph) inorb[s] = 1;
    KeyIndex PI;
    {
        std::vector<u128> all = read_keys(pfn);
        for (auto k : all) { unsigned p = (unsigned)(k >> PSp); if (inorb[p]) PI.keys.push_back(k); }
    }
    if (!std::is_sorted(PI.keys.begin(), PI.keys.end())) { fprintf(stderr, "PREV not sorted\n"); return 1; }
    if (PSp != PSn) { u128 cm = ((u128)1 << PSp) - 1; for (auto& k : PI.keys) k = ((k >> PSp) << PSn) | (k & cm); }
    PI.build();
    const uint64_t N1 = PI.keys.size(), N = N1 * (uint64_t)D_;
    if (N >= 0xFFFFFFF0ULL) { fprintf(stderr, "too many candidates %llu\n", (unsigned long long)N); return 1; }
    fprintf(stderr, "kink7 K=%d orbit %d/%d phases %zu prev %llu candidates %llu\n", K, which, norb, ph.size(), (unsigned long long)N1, (unsigned long long)N);
    const int NK = 2 * B_;
    auto decode = [&](uint32_t c, int& t, int& j, int& par, int* w) {
        uint64_t i = c / D_; int x = c % D_; u128 k = PI.keys[i];
        phase_dec((unsigned)(k >> PSn), t, j, par); dec_cells(k, w, K - 1); w[K - 1] = x;
    };
    auto lookup = [&](int t, int j, int par, const int* nw) -> int64_t {
        ll i = PI.find(enc(t, j, par, nw, K - 1, PSn)); if (i < 0) return -1; return (int64_t)i * D_ + nw[K - 1];
    };
    // k-th successor; returns candidate index or -1
    auto succ = [&](uint32_t c, int kk) -> int64_t {
        int t, j, par, w[64], nw[64]; decode(c, t, j, par, w);
        int g = G[t]; int dh = (g == 1 && par == 0); int Din = kk & 1, tv = kk >> 1;
        if (!dh && tv) return -1;
        if (tv >= B_) return -1;
        if (!wstep(K, t, j, w, Din, dh, tv, nw)) return -1;
        int t2, j2, p2; next_phase(t, j, par, t2, j2, p2);
        return lookup(t2, j2, p2, nw);
    };
    // ---- iterative Tarjan
    std::vector<uint32_t> idx(N, 0), low(N, 0);
    std::vector<uint64_t> onst((N + 63) / 64, 0), cyc((N + 63) / 64, 0);
    auto bget = [](const std::vector<uint64_t>& b, uint64_t i) { return (b[i >> 6] >> (i & 63)) & 1; };
    auto bset = [](std::vector<uint64_t>& b, uint64_t i) { b[i >> 6] |= 1ULL << (i & 63); };
    auto bclr = [](std::vector<uint64_t>& b, uint64_t i) { b[i >> 6] &= ~(1ULL << (i & 63)); };
    std::vector<uint32_t> st, wv; std::vector<uint8_t> wk;
    uint32_t counter = 0; ll nscc = 0, ncyc = 0, nacc = 0, edges = 0;
    for (uint64_t root = 0; root < N; root++) {
        if (idx[root]) continue;
        idx[root] = low[root] = ++counter; st.push_back(root); bset(onst, root); wv.push_back(root); wk.push_back(0);
        while (!wv.empty()) {
            uint32_t v = wv.back(); bool pushed = false;
            while (wk.back() < NK) {
                int kk = wk.back()++;
                int64_t w = succ(v, kk); if (w < 0) continue; edges++;
                if (!idx[w]) { idx[w] = low[w] = ++counter; st.push_back(w); bset(onst, w); wv.push_back(w); wk.push_back(0); pushed = true; break; }
                else if (bget(onst, w) && idx[w] < low[v]) low[v] = idx[w];
            }
            if (pushed) continue;
            wv.pop_back(); wk.pop_back();
            if (!wv.empty()) { uint32_t u = wv.back(); if (low[v] < low[u]) low[u] = low[v]; }
            if (low[v] == idx[v]) {
                size_t base = st.size(); while (st[base - 1] != v) base--; base--;
                bool c = st.size() - base > 1;
                if (!c) for (int kk = 0; kk < NK; kk++) if (succ(v, kk) == (int64_t)v) c = true;
                for (size_t q = base; q < st.size(); q++) {
                    uint32_t w = st[q]; bclr(onst, w);
                    if (c) {
                        bset(cyc, w); ncyc++;
                        int t, j, par, ww[64]; decode(w, t, j, par, ww); if (ww[0] != L[t][j]) nacc++;
                    }
                }
                if (c) nscc++;
                st.resize(base);
            }
        }
    }
    std::vector<uint32_t>().swap(low); std::vector<uint32_t>().swap(st);
    double tT = now_s() - T0;
    // ---- write Cyc(K) of this orbit in sorted key order: phase, then top cell, then the PREV order
    {
        FILE* of = fopen(ofn, "wb"); if (!of) { perror(ofn); return 1; }
        std::vector<u128> buf; buf.reserve(1 << 20);
        uint64_t i0 = 0;
        while (i0 < N1) {
            unsigned p = (unsigned)(PI.keys[i0] >> PSn); uint64_t i1 = i0; while (i1 < N1 && (unsigned)(PI.keys[i1] >> PSn) == p) i1++;
            for (int x = 0; x < D_; x++) for (uint64_t i = i0; i < i1; i++) {
                uint64_t c = i * D_ + x;
                if (bget(cyc, c)) { buf.push_back(PI.keys[i] | ((u128)x << (5 * (K - 1)))); if (buf.size() == buf.capacity()) { fwrite(buf.data(), 16, buf.size(), of); buf.clear(); } }
            }
            i0 = i1;
        }
        fwrite(buf.data(), 16, buf.size(), of); fclose(of);
    }
    // ---- exact centre check inside Cyc(K): functional graph of the exact fold step (idx reused as colour/next marker)
    ll nex = 0, exact_cycles = 0, exact_nonlat = 0;
    std::fill(idx.begin(), idx.end(), 0);   // 0 = unvisited, 1 = on current path, 2 = done
    auto exact_next = [&](uint32_t c) -> int64_t {
        int t, j, par, w[64], nw[64]; decode(c, t, j, par, w);
        if (!exact_step(K, t, j, par, w, nw)) return -1;
        int t2, j2, p2; next_phase(t, j, par, t2, j2, p2);
        int64_t d = lookup(t2, j2, p2, nw); if (d < 0 || !bget(cyc, d)) return -1; return d;
    };
    for (uint64_t i = 0; i < N; i++) { if (bget(cyc, i) && exact_next(i) >= 0) nex++; }
    std::vector<uint32_t> path;
    for (uint64_t i = 0; i < N; i++) {
        if (!bget(cyc, i) || idx[i]) continue;
        path.clear(); int64_t x = i;
        while (x >= 0 && idx[x] == 0) { idx[x] = 1; path.push_back(x); x = exact_next(x); }
        if (x >= 0 && idx[x] == 1) {
            exact_cycles++; int64_t y = x; bool nonlat = false; ll len = 0;
            do { int t, j, par, w[64]; decode(y, t, j, par, w); for (int q = 0; q < K; q++) if (w[q] != L[t][md(j + q, M_)]) nonlat = true; y = exact_next(y); len++; } while (y != x && y >= 0);
            if (nonlat) exact_nonlat++;
            int t, j, par, w[64]; decode(x, t, j, par, w);
            printf("EXACT CYCLE length %lld %s first state: t=%d j=%d par=%d win", len, nonlat ? "NON-LATTICE" : "all-lattice", t, j, par);
            for (int q = 0; q < K; q++) printf(" %d", w[q]); printf("\n");
        }
        for (auto y : path) idx[y] = 2;
    }
    printf("K=%d orbit=%d/%d candidates=%llu edges=%lld cyclicSCCs=%lld cyclicStates=%lld acceptingStates=%lld | exact: successors-in-Cyc=%lld cycles=%lld nonlattice=%lld | tarjan %.0fs total %.0fs\n",
           K, which, norb, (unsigned long long)N, edges, nscc, ncyc, nacc, nex, exact_cycles, exact_nonlat, tT, now_s() - T0);
    return 0;
}
