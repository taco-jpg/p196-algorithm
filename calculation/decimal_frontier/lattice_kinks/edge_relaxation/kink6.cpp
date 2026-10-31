// kink6: exact incremental edge relaxation (centre frame) + complete exact-centre search, 128-bit state keys.
//   kink6 lat.tbl K full  OUT          (K <= 4)    : all states, write cyclic set of R_K to OUT (binary)
//   kink6 lat.tbl K incr  PREV OUT                 : candidates = Cyc(K-1) x {0..18}; write Cyc(K) to OUT
// Every run also performs the exact-centre check on Cyc(K): exact deterministic step of the top-K window
// (lattice below, centre carries determined) restricted to Cyc(K); any cycle = periodic centre of depth <= K (printed).
// Binary file: sequence of unsigned __int128 keys, key = phase<<100 | sum cell_i << (5 i).
#include <bits/stdc++.h>
using namespace std;
typedef long long ll; typedef unsigned __int128 u128;
int P_, M_, K_;
vector<int> G; vector<vector<int>> L, UP, DN;
static inline int md(int a, int m) { a %= m; return a < 0 ? a + m : a; }

bool wstep(int t, int j, const int* win, int Din, int dh, int topv, int* out) {
    const int K = K_; int g = G[t];
    int e[40], D[40], r[40];
    int up = UP[t][j];
    for (int i = 0; i < K; i++) { int s = win[i] + up; e[i] = s % 10; up = s / 10; }
    D[K - 1] = Din;
    for (int i = K - 1; i > 0; i--) D[i - 1] = (win[i] + D[i]) / 10;
    for (int i = 0; i < K; i++) r[i] = (win[i] + D[i]) % 10;
    int Dx = (win[0] + D[0]) / 10;
    bool ok = true; int rlow1 = -1; int t1 = (t + 1) % P_;
    for (int k = 1; k <= 4 * M_; k++) {
        int col = md(j - k, M_); int Lx = L[t][col];
        if (Dx == DN[t][col]) break;
        int rx = (Lx + Dx) % 10;
        if (k == 1) rlow1 = rx;
        int tgt = -k + g;
        if (tgt < 0) { int tc = md(j + tgt, M_); if ((L[t][tc] + UP[t][tc]) % 10 + rx != L[t1][tc]) ok = false; }
        Dx = (Lx + Dx) / 10;
    }
    int nw[41];
    for (int i = 0; i < K + dh; i++) {
        if (i == K) { nw[i] = (g == 1) ? topv + r[K - 1] : topv; continue; }
        int src = i - g, rr;
        if (src >= 0) rr = r[src];
        else { if (rlow1 >= 0) rr = rlow1; else { int col = md(j - 1, M_); rr = (L[t][col] + DN[t][col]) % 10; } }
        nw[i] = e[i] + rr;
    }
    if (dh) { if (nw[0] != L[t1][md(j, M_)]) ok = false; for (int i = 0; i < K; i++) out[i] = nw[i + 1]; }
    else for (int i = 0; i < K; i++) out[i] = nw[i];
    return ok;
}
void load(const char* fn) {
    FILE* f = fopen(fn, "r"); if (!f) { perror(fn); exit(1); }
    if (fscanf(f, "%d %d", &P_, &M_) != 2) exit(1);
    G.resize(P_); for (auto& x : G) if (fscanf(f, "%d", &x) != 1) exit(1);
    L.assign(P_, vector<int>(M_)); UP = L; DN = L;
    for (int t = 0; t < P_; t++) {
        for (auto& x : L[t]) if (fscanf(f, "%d", &x) != 1) exit(1);
        for (auto& x : UP[t]) if (fscanf(f, "%d", &x) != 1) exit(1);
        for (auto& x : DN[t]) if (fscanf(f, "%d", &x) != 1) exit(1);
    }
    fclose(f);
}
static inline u128 enc(int t, int j, int par, const int* w, int K) {
    u128 k = (u128)((t * M_ + j) * 2 + par) << 100;
    for (int i = 0; i < K; i++) k |= (u128)w[i] << (5 * i);
    return k;
}
static inline void dec(u128 k, int& t, int& j, int& par, int* w, int K) {
    unsigned ph = (unsigned)(k >> 100); par = ph % 2; ph /= 2; j = ph % M_; t = ph / M_;
    for (int i = 0; i < K; i++) w[i] = (int)((k >> (5 * i)) & 31);
}
vector<u128> C;   // sorted candidates
static inline ll pos(u128 s) { auto it = lower_bound(C.begin(), C.end(), s); return (it != C.end() && *it == s) ? (ll)(it - C.begin()) : -1; }
// k-th successor (k in 0..19): Din = k&1, topv = k>>1 ; returns key or 0-flag via ok
static inline bool succ(u128 s, int k, u128& out) {
    int t, j, par, w[40], nw[40]; dec(s, t, j, par, w, K_);
    int g = G[t]; int dh = (g == 1 && par == 0);
    int Din = k & 1, tv = k >> 1;
    if (!dh && tv) return false;
    if (tv > 9) return false;
    if (!wstep(t, j, w, Din, dh, tv, nw)) return false;
    out = enc((t + 1) % P_, (j + dh) % M_, (par + g) % 2, nw, K_);
    return true;
}
static inline bool accepting(u128 s) { int t, j, par, w[40]; dec(s, t, j, par, w, K_); return w[0] != L[t][j]; }
// exact centre successor
static inline bool exact_succ(u128 s, u128& out) {
    int t, j, par, w[40], nw[40]; dec(s, t, j, par, w, K_);
    const int K = K_; int a = UP[t][j], aK1 = 0;
    for (int i = 0; i < K; i++) { if (i == K - 1) aK1 = a; a = (w[i] + a) / 10; }
    int Din = (par == 0) ? a : aK1;              // n even: carry into position h; n odd: carry into middle cell
    int ghost = (w[K - 1] + Din) % 10;
    int g = G[t]; int dh = (g == 1 && par == 0);
    if (!wstep(t, j, w, Din, dh, ghost, nw)) return false;
    out = enc((t + 1) % P_, (j + dh) % M_, (par + g) % 2, nw, K);
    return true;
}

int main(int argc, char** argv) {
    load(argv[1]); K_ = atoi(argv[2]); string how = argv[3];
    const char* outfn;
    auto T0 = chrono::steady_clock::now();
    if (how == "full") {
        if (K_ > 4) { fprintf(stderr, "full only for K<=4\n"); return 1; }
        int w[40]; ll nw = 1; for (int i = 0; i < K_; i++) nw *= 19;
        for (int t = 0; t < P_; t++) for (int j = 0; j < M_; j++) for (int par = 0; par < 2; par++)
            for (ll x = 0; x < nw; x++) { ll y = x; for (int i = 0; i < K_; i++) { w[i] = y % 19; y /= 19; } C.push_back(enc(t, j, par, w, K_)); }
        outfn = argv[4];
    } else {
        FILE* pf = fopen(argv[4], "rb"); if (!pf) { perror(argv[4]); return 1; }
        u128 k; vector<u128> prev;
        while (fread(&k, sizeof(u128), 1, pf) == 1) prev.push_back(k);
        fclose(pf);
        C.reserve(prev.size() * 19);
        for (u128 p : prev) for (int x = 0; x < 19; x++) C.push_back(p | ((u128)x << (5 * (K_ - 1))));
        outfn = argv[5];
    }
    sort(C.begin(), C.end()); C.erase(unique(C.begin(), C.end()), C.end());
    ll NC = C.size();
    fprintf(stderr, "K=%d candidates %lld\n", K_, NC);
    vector<uint32_t> idx(NC, 0), low(NC, 0); vector<bool> onst(NC, false), cyc(NC, false);
    vector<uint32_t> st; struct Fr { uint32_t v; uint8_t k; }; vector<Fr> work;
    uint32_t counter = 0; ll nscc = 0, ncyc = 0, nacc = 0, nacc_scc = 0, edges = 0;
    for (ll root = 0; root < NC; root++) {
        if (idx[root]) continue;
        idx[root] = low[root] = ++counter; st.push_back(root); onst[root] = true; work.push_back({(uint32_t)root, 0});
        while (!work.empty()) {
            Fr& fr = work.back(); uint32_t v = fr.v; bool pushed = false;
            while (fr.k < 20) {
                int k = fr.k++; u128 ws;
                if (!succ(C[v], k, ws)) continue;
                ll w = pos(ws); if (w < 0) continue; edges++;
                if (!idx[w]) { idx[w] = low[w] = ++counter; st.push_back(w); onst[w] = true; work.push_back({(uint32_t)w, 0}); pushed = true; break; }
                else if (onst[w] && idx[w] < low[v]) low[v] = idx[w];
            }
            if (pushed) continue;
            work.pop_back();
            if (!work.empty()) { uint32_t u = work.back().v; if (low[v] < low[u]) low[u] = low[v]; }
            if (low[v] == idx[v]) {
                vector<uint32_t> comp;
                while (true) { uint32_t w = st.back(); st.pop_back(); onst[w] = false; comp.push_back(w); if (w == v) break; }
                bool c = comp.size() > 1;
                if (!c) { for (int k = 0; k < 20; k++) { u128 ws; if (succ(C[v], k, ws) && ws == C[v]) c = true; } }
                if (c) {
                    nscc++; ll na = 0;
                    for (auto w : comp) { cyc[w] = true; ncyc++; if (accepting(C[w])) na++; }
                    if (na) { nacc_scc++; nacc += na; }
                }
            }
        }
    }
    // write Cyc(K)
    vector<u128> Cy; Cy.reserve(ncyc);
    for (ll i = 0; i < NC; i++) if (cyc[i]) Cy.push_back(C[i]);
    FILE* of = fopen(outfn, "wb"); fwrite(Cy.data(), sizeof(u128), Cy.size(), of); fclose(of);
    // exact centre check on Cyc(K)
    C.swap(Cy); vector<u128>().swap(Cy);
    ll NE = C.size(), nex = 0, exact_cycles = 0, exact_nonlat = 0;
    vector<int64_t> nxt(NE, -1);
    for (ll i = 0; i < NE; i++) { u128 o; if (exact_succ(C[i], o)) { ll p = pos(o); if (p >= 0) { nxt[i] = p; nex++; } } }
    vector<uint8_t> col(NE, 0);
    for (ll i = 0; i < NE; i++) {
        if (col[i]) continue;
        vector<ll> path; ll x = i;
        while (x >= 0 && col[x] == 0) { col[x] = 1; path.push_back(x); x = nxt[x]; }
        if (x >= 0 && col[x] == 1) {
            exact_cycles++;
            ll y = x; bool nonlat = false; ll len = 0;
            do { int t, j, par, w[40]; dec(C[y], t, j, par, w, K_); for (int q = 0; q < K_; q++) if (w[q] != L[t][md(j + q, M_)]) nonlat = true; y = nxt[y]; len++; } while (y != x);
            if (nonlat) exact_nonlat++;
            printf("EXACT CYCLE length %lld %s first state:", len, nonlat ? "NON-LATTICE" : "all-lattice");
            int t, j, par, w[40]; dec(C[x], t, j, par, w, K_); printf(" t=%d j=%d par=%d win", t, j, par); for (int q = 0; q < K_; q++) printf(" %d", w[q]); printf("\n");
        }
        for (ll y : path) col[y] = 2;
    }
    double secs = chrono::duration<double>(chrono::steady_clock::now() - T0).count();
    printf("K=%d candidates=%lld edges=%lld cyclicSCCs=%lld cyclicStates=%lld acceptingSCCs=%lld acceptingStates=%lld | exact: successors-in-Cyc=%lld cycles=%lld nonlattice=%lld | %.0fs\n",
           K_, NC, edges, nscc, ncyc, nacc_scc, nacc, nex, exact_cycles, exact_nonlat, secs);
    return 0;
}
