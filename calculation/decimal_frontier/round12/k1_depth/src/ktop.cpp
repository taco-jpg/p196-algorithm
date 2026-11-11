// r12g ktop: cyclic set TopCyc(k) of the TOP relaxation: window = the k folded cells just below the fold, [h-k, h),
// fold exact at the top (palindromic step), everything below FREE (ascending carry a_in into cell h-k every step, r-digit
// r_in of cell h-k-1 entering cell h-k on overflow steps), no lattice condition.  The rule does not use the lattice at all:
// the phase is (t mod P, n mod 2) only.  Projection: dropping the BOTTOM cell of a top-k cycle gives a top-(k-1) cycle, so
// TopCyc(k) = cyclic part of the induced graph on {0..2B-2} x TopCyc(k-1) (new cell at the bottom).
// Every centre of any depth, for any lattice with this clock, has its top-k window in TopCyc(k) at all times.
// usage: ktop lat.tbl k full OUT      (k <= 5)
//        ktop lat.tbl k incr PREV OUT
// key: phase (t*2+par) << 100 | cell_i << 5i (cell 0 = bottom = h-k).
#include "kcommon.h"
int k_;
static inline void tdec(u128 s, int& t, int& par, int* w) { unsigned ph = (unsigned)(s >> 100); par = ph & 1; t = ph >> 1; dec_cells(s, w, k_); }
static inline u128 tenc(int t, int par, const int* w) { return ((u128)(unsigned)(t * 2 + par) << 100) | enc_cells(w, k_); }
// one step; a_in, r_in free inputs from below
static inline void tstep(int t, int par, const int* w, int a_in, int r_in, int* out, int& t2, int& p2) {
    const int K = k_, Bb = B_; int g = G[t]; int dh = (g == 1 && par == 0);
    int e[64], D[64], r[64];
    int a = a_in, aK1 = 0;
    for (int i = 0; i < K; i++) { if (i == K - 1) aK1 = a; int s = w[i] + a; e[i] = s % Bb; a = s / Bb; }
    int Din = (par == 0) ? a : aK1;
    D[K - 1] = Din;
    for (int i = K - 1; i > 0; i--) D[i - 1] = (w[i] + D[i]) / Bb;
    for (int i = 0; i < K; i++) r[i] = (w[i] + D[i]) % Bb;
    int nw[65];
    for (int i = 0; i < K + dh; i++) {
        if (i == K) { nw[i] = r[K - 1] + r[K - 1]; continue; }          // dh: new middle cell 2*r_{h-1}
        int src = i - g; int rr = src >= 0 ? r[src] : r_in;
        nw[i] = e[i] + rr;
    }
    if (dh) for (int i = 0; i < K; i++) out[i] = nw[i + 1]; else for (int i = 0; i < K; i++) out[i] = nw[i];
    t2 = (t + 1) % P_; p2 = (par + g) % 2;
}
std::vector<u128> C;
static inline ll pos(u128 s) { auto it = std::lower_bound(C.begin(), C.end(), s); return (it != C.end() && *it == s) ? (ll)(it - C.begin()) : -1; }
static inline bool succ(u128 s, int kk, u128& o) {   // kk = a_in + 2*r_in
    int t, par, w[64], nw[64]; tdec(s, t, par, w);
    int a_in = kk & 1, r_in = kk >> 1; int g = G[t];
    bool rmat = (g == 1 && par == 1);
    if (!rmat && r_in) return false;
    if (r_in >= B_) return false;
    int t2, p2; tstep(t, par, w, a_in, r_in, nw, t2, p2);
    o = tenc(t2, p2, nw); return true;
}
int main(int argc, char** argv) {
    load_tbl(argv[1]); k_ = atoi(argv[2]); std::string how = argv[3]; const char* outfn;
    double T0 = now_s();
    if (how == "full") {
        ll nw = 1; for (int i = 0; i < k_; i++) nw *= D_;
        int w[64];
        for (int t = 0; t < P_; t++) for (int par = 0; par < 2; par++) for (ll x = 0; x < nw; x++) {
            ll y = x; for (int i = 0; i < k_; i++) { w[i] = y % D_; y /= D_; }
            C.push_back(tenc(t, par, w));
        }
        outfn = argv[4];
    } else {
        std::vector<u128> prev = read_keys(argv[4]);
        C.reserve(prev.size() * D_);
        for (u128 p : prev) { u128 ph = p >> 100, cells = p & (((u128)1 << 100) - 1); for (int x = 0; x < D_; x++) C.push_back((ph << 100) | (cells << 5) | (u128)x); }
        outfn = argv[5];
    }
    std::sort(C.begin(), C.end()); C.erase(std::unique(C.begin(), C.end()), C.end());
    ll NC = C.size(); int NK = 2 * B_;
    std::vector<uint32_t> idx(NC, 0), low(NC, 0); std::vector<bool> onst(NC, false), cyc(NC, false);
    std::vector<uint32_t> st; struct Fr { uint32_t v; uint8_t k; }; std::vector<Fr> work;
    uint32_t counter = 0; ll nscc = 0, ncyc = 0, edges = 0;
    for (ll root = 0; root < NC; root++) {
        if (idx[root]) continue;
        idx[root] = low[root] = ++counter; st.push_back(root); onst[root] = true; work.push_back({(uint32_t)root, 0});
        while (!work.empty()) {
            Fr& fr = work.back(); uint32_t v = fr.v; bool pushed = false;
            while (fr.k < NK) {
                int kk = fr.k++; u128 ws;
                if (!succ(C[v], kk, ws)) continue;
                ll w = pos(ws); if (w < 0) continue; edges++;
                if (!idx[w]) { idx[w] = low[w] = ++counter; st.push_back(w); onst[w] = true; work.push_back({(uint32_t)w, 0}); pushed = true; break; }
                else if (onst[w] && idx[w] < low[v]) low[v] = idx[w];
            }
            if (pushed) continue;
            work.pop_back();
            if (!work.empty()) { uint32_t u = work.back().v; if (low[v] < low[u]) low[u] = low[v]; }
            if (low[v] == idx[v]) {
                std::vector<uint32_t> comp;
                while (true) { uint32_t w = st.back(); st.pop_back(); onst[w] = false; comp.push_back(w); if (w == v) break; }
                bool c = comp.size() > 1;
                if (!c) for (int kk = 0; kk < NK; kk++) { u128 ws; if (succ(C[v], kk, ws) && ws == C[v]) c = true; }
                if (c) { nscc++; for (auto w : comp) { cyc[w] = true; ncyc++; } }
            }
        }
    }
    std::vector<u128> Cy; for (ll i = 0; i < NC; i++) if (cyc[i]) Cy.push_back(C[i]);
    FILE* of = fopen(outfn, "wb"); fwrite(Cy.data(), sizeof(u128), Cy.size(), of); fclose(of);
    // per-phase counts
    std::vector<ll> per(2 * P_, 0); for (auto s : Cy) per[(unsigned)(s >> 100)]++;
    printf("TOP k=%d candidates=%lld edges=%lld cyclicSCCs=%lld cyclicStates=%lld | per (t,par):", k_, NC, edges, nscc, ncyc);
    for (int i = 0; i < 2 * P_; i++) printf(" %lld", per[i]);
    printf(" | %.0fs\n", now_s() - T0);
    return 0;
}
