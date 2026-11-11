// r13b indep_acc.cpp: independent re-computation of E_acc(K,T) (closed T-walks of the bottom relaxation R_K through an accepting
// state).  Rule: r12g2 indep.cpp rstep2/fstep (explicit lattice rows, genuine carries, own parser mklat.py), NOT kcommon.h.
// Closure algorithm: NOT eset3's anchor-layer flag DP but per-accepting-source forward/backward reachability from every accepting
// node (one start layer at a time, 64 sources per batch); keys = explicit byte arrays. Compares sets with eset3 E_K files (-cmp DIR).
//   usage: indep_scc ROWS orbit 1 Kmax OUTDIR threads [q] [-noexact]   (all-period closure Cyc_acc)
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <thread>
#include <unordered_map>
#include <string>
#include <vector>
using namespace std;
typedef unsigned __int128 u128;
typedef long long ll; typedef unsigned long long ull;
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

static inline uint64_t hbytes(const uint8_t* p, int n) { uint64_t h = 0xcbf29ce484222325ULL; for (int i = 0; i < n; i++) { h ^= p[i]; h *= 0x100000001b3ULL; } h ^= h >> 29; h *= 0xbf58476d1ce4e5b9ULL; h ^= h >> 32; return h; }
struct LayerI { int t, j, par, g, dh; vector<uint8_t> par_cells; uint64_t np = 0; vector<uint32_t> slot; uint64_t mask = 0; };
static vector<LayerI> Ls; static int Lo, Q = 3, THR = 4, KW = 0;
static void build_index(LayerI& A, int Km1) {
    uint64_t cap = 1; while (cap < 2 * A.np + 16) cap <<= 1; A.slot.assign(cap, 0); A.mask = cap - 1;
    for (uint64_t i = 0; i < A.np; i++) { const uint8_t* p = A.par_cells.data() + i * Km1; uint64_t h = hbytes(p, Km1) & A.mask; while (A.slot[h]) h = (h + 1) & A.mask; A.slot[h] = (uint32_t)(i + 1); }
}
static inline ll find_parent(const LayerI& A, const uint8_t* cells, int Km1) {
    if (A.np == 0) return -1;
    uint64_t h = hbytes(cells, Km1) & A.mask;
    while (true) { uint32_t s = A.slot[h]; if (!s) return -1; const uint8_t* p = A.par_cells.data() + (uint64_t)(s - 1) * Km1; if (memcmp(p, cells, Km1) == 0) return (ll)(s - 1); h = (h + 1) & A.mask; }
}
struct LayerG { uint64_t nc = 0; vector<uint32_t> off, ed; vector<uint8_t> alive; vector<uint32_t> did; uint32_t n = 0; vector<uint32_t> revdid; };
static uint64_t Tall = 0;
int main(int argc, char** argv) {
    if (argc < 7) { fprintf(stderr, "usage: indep_acc ROWS orbit L Kmax OUTDIR threads [q] [-cmp DIR] [-noexact]\n"); return 1; }
    load_rows(argv[1]); int which = atoi(argv[2]); int LL = atoi(argv[3]); int Kmax = atoi(argv[4]); string out = argv[5]; THR = atoi(argv[6]);
    string cmpd; bool noexact = false; for (int i = 7; i < argc; i++) { string a = argv[i]; if (a == "-cmp") cmpd = argv[++i]; else if (a == "-noexact") noexact = true; else Q = atoi(argv[i]); }
    // phase orbits by smallest phase id (same convention)
    int NPH = 2 * Pp * MM; vector<int> seen(NPH, -1); vector<int> reps; int cnt = 0;
    for (int s = 0; s < NPH; s++) { if (seen[s] >= 0) continue; reps.push_back(s); int t, j, p; phdec(s, t, j, p); int x = s; do { seen[x] = cnt; int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; x = phid(t, j, p); } while (x != s); cnt++; }
    { int t, j, p; phdec(reps[which], t, j, p); int x = reps[which]; do { LayerI A; A.t = t; A.j = j; A.par = p; A.g = GG[t]; A.dh = (A.g == 1 && p == 0); Ls.push_back(std::move(A)); int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; x = phid(t, j, p); } while (x != reps[which]); }
    Lo = Ls.size(); int TT = Lo; (void)LL;
    printf("indep_scc(all periods) orbit %d/%d Lo=%d T=%d Kmax=%d q=%d thr=%d\n", which, cnt, Lo, TT, Kmax, Q, THR); fflush(stdout);
    for (auto& A : Ls) { A.np = 1; A.par_cells.clear(); }   // empty parents at K-1 = 0: one parent (empty window)
    double Tst = now_s();
    for (int K = 1; K <= Kmax; K++) {
        double T0 = now_s(); int Km1 = K - 1; uint64_t Ntot = 0;
        for (auto& A : Ls) { build_index(A, Km1); }
        vector<LayerG> G_(Lo);
        for (int l = 0; l < Lo; l++) G_[l].nc = Ls[l].np * DV;
        // edges (candidate to candidate)
        for (int l = 0; l < Lo; l++) {
            LayerG& Gg = G_[l]; LayerI& A = Ls[l]; LayerI& B = Ls[(l + 1) % Lo];
            Gg.off.assign(Gg.nc + 1, 0); vector<vector<uint32_t>> tgs(THR); vector<vector<uint32_t>> deg(THR);
            vector<thread> th; atomic<ull> nx(0); ull chunks = max<ull>(1, Gg.nc / 4096 + 1);
            vector<vector<pair<ull, uint32_t>>> res(THR);
            vector<vector<uint32_t>> res2(chunks);
            atomic<ull> done(0);
            for (int z = 0; z < THR; z++) th.emplace_back([&, z] {
                int w[64], o[2][64]; uint8_t tmp[64]; ull ci;
                while ((ci = nx.fetch_add(1)) < chunks) {
                    ull lo = Gg.nc * ci / chunks, hi = Gg.nc * (ci + 1) / chunks; vector<uint32_t> loc; loc.reserve((hi - lo) * 3);
                    for (ull c = lo; c < hi; c++) {
                        uint64_t pi = c / DV; int x = c % DV; const uint8_t* p = A.par_cells.data() + pi * Km1; for (int i = 0; i < Km1; i++) w[i] = p[i]; w[K - 1] = x;
                        int mask = rstep2(A.t, A.j, A.par, w, K, Q, o); int nl = 0; uint32_t ts[64];
                        for (int Din = 0; Din < 2; Din++) if (mask >> Din & 1) {
                            for (int tv = 0; tv < (A.dh ? BS : 1); tv++) {
                                int top = o[Din][K - 1] + (A.dh ? tv : 0);
                                for (int i = 0; i < Km1; i++) tmp[i] = (uint8_t)o[Din][i];
                                ll pp = find_parent(B, tmp, Km1); if (pp < 0) continue;
                                ts[nl++] = (uint32_t)(pp * DV + top);
                            }
                        }
                        sort(ts, ts + nl); nl = unique(ts, ts + nl) - ts; loc.push_back(nl); loc.insert(loc.end(), ts, ts + nl);
                    }
                    res2[ci].swap(loc);
                }
            });
            for (auto& t : th) t.join();
            uint64_t ne = 0; for (auto& r : res2) { uint64_t i = 0; while (i < r.size()) { ne += r[i]; i += r[i] + 1; } }
            Gg.ed.resize(ne); uint64_t pos = 0, cidx = 0;
            for (auto& r : res2) { uint64_t i = 0; while (i < r.size()) { uint32_t d = r[i]; Gg.off[cidx + 1] = Gg.off[cidx] + d; cidx++; for (uint32_t q = 0; q < d; q++) Gg.ed[pos++] = r[i + 1 + q]; i += d + 1; } }
            Ntot += Gg.nc;
        }
        double Ted = now_s() - T0;
        // trim to bi-infinite core (flags, repeated sweeps)
        for (int l = 0; l < Lo; l++) G_[l].alive.assign(G_[l].nc, 1);
        bool ch = true; int rounds = 0;
        while (ch) {
            ch = false; rounds++;
            for (int l = 0; l < Lo; l++) { LayerG& A = G_[l]; LayerG& B = G_[(l + 1) % Lo];
                vector<uint8_t> hasin(B.nc, 0);
                for (uint64_t c = 0; c < A.nc; c++) if (A.alive[c]) { bool any = false; for (uint32_t q = A.off[c]; q < A.off[c + 1]; q++) if (B.alive[A.ed[q]]) { any = true; hasin[A.ed[q]] = 1; } if (!any) { A.alive[c] = 0; ch = true; } }
                for (uint64_t c = 0; c < B.nc; c++) if (B.alive[c] && !hasin[c]) { B.alive[c] = 0; ch = true; }
            }
        }
        // dense ids
        uint64_t core = 0, redges = 0;
        for (int l = 0; l < Lo; l++) { LayerG& A = G_[l]; A.did.assign(A.nc, 0xFFFFFFFFu); uint32_t n = 0; for (uint64_t c = 0; c < A.nc; c++) if (A.alive[c]) A.did[c] = n++; A.n = n; core += n; }
        vector<vector<uint32_t>> OFF(Lo), EDGE(Lo);
        for (int l = 0; l < Lo; l++) { LayerG& A = G_[l]; LayerG& B = G_[(l + 1) % Lo]; OFF[l].assign(A.n + 1, 0); vector<uint32_t>& E = EDGE[l]; E.clear();
            for (uint64_t c = 0; c < A.nc; c++) if (A.alive[c]) { uint32_t v = A.did[c]; for (uint32_t q = A.off[c]; q < A.off[c + 1]; q++) if (B.alive[A.ed[q]]) E.push_back(B.did[A.ed[q]]); OFF[l][v + 1] = E.size(); }
            redges += E.size(); }
        // accepting flags
        vector<vector<uint8_t>> Acc(Lo); ull nacc = 0;
        for (int l = 0; l < Lo; l++) { LayerG& A = G_[l]; LayerI& I = Ls[l]; Acc[l].assign(A.n, 0); int c0 = NB + I.j + Q * MM; for (uint64_t c = 0; c < A.nc; c++) if (A.alive[c]) { uint32_t v = A.did[c]; int w0 = (K == 1) ? (int)(c % DV) : (int)I.par_cells[c / DV * Km1]; if (w0 != row(I.t, c0)) { Acc[l][v] = 1; nacc++; } } }
        // closure (all periods): Kosaraju SCCs on the dense graph; keep SCCs of size >= 2 containing an accepting node
        vector<vector<uint8_t>> on(Lo); for (int l = 0; l < Lo; l++) on[l].assign(G_[l].n, 0);
        ull closed = 0, nodeops = 0; (void)nodeops;
        {
            vector<uint64_t> gb(Lo + 1, 0); for (int l = 0; l < Lo; l++) gb[l + 1] = gb[l] + G_[l].n;
            uint64_t NN = gb[Lo];
            if (NN >= 0xFFFFFFF0ULL) { fprintf(stderr, "too many nodes\n"); exit(9); }
            vector<uint32_t> ro(NN + 2, 0), re;
            vector<uint8_t> layerOf_acc(NN, 0);
            for (int l = 0; l < Lo; l++) for (uint32_t v = 0; v < G_[l].n; v++) { layerOf_acc[gb[l] + v] = Acc[l][v]; for (uint32_t q = OFF[l][v]; q < OFF[l][v + 1]; q++) { uint64_t tg = gb[(l + 1) % Lo] + EDGE[l][q]; ro[tg + 1]++; } }
            for (uint64_t i = 0; i < NN; i++) ro[i + 1] += ro[i];
            re.resize(ro[NN]);
            { vector<uint32_t> pos(ro.begin(), ro.end()); for (int l = 0; l < Lo; l++) for (uint32_t v = 0; v < G_[l].n; v++) for (uint32_t q = OFF[l][v]; q < OFF[l][v + 1]; q++) { uint64_t tg = gb[(l + 1) % Lo] + EDGE[l][q]; re[pos[tg]++] = (uint32_t)(gb[l] + v); } }
            // pass 1: iterative DFS, finishing order
            vector<uint32_t> fin; fin.reserve(NN);
            vector<uint8_t> seen(NN, 0);
            struct F { uint32_t id; uint32_t e, eend; int l; };
            vector<F> st;
            for (int l0 = 0; l0 < Lo; l0++) for (uint32_t v0 = 0; v0 < G_[l0].n; v0++) {
                uint32_t g0 = (uint32_t)(gb[l0] + v0);
                if (seen[g0]) continue;
                seen[g0] = 1;
                st.push_back({g0, OFF[l0][v0], OFF[l0][v0 + 1], l0});
                while (!st.empty()) {
                    F& f = st.back();
                    if (f.e < f.eend) {
                        int l2 = (f.l + 1) % Lo; uint32_t w = EDGE[f.l][f.e++];
                        uint32_t g2 = (uint32_t)(gb[l2] + w);
                        if (!seen[g2]) { seen[g2] = 1; st.push_back({g2, OFF[l2][w], OFF[l2][w + 1], l2}); }
                    } else { fin.push_back(f.id); st.pop_back(); }
                }
            }
            // pass 2: reverse graph in decreasing finishing order
            vector<uint32_t> compid(NN, 0xFFFFFFFFu); uint32_t ncomp = 0;
            vector<uint32_t> stack2, members;
            vector<uint32_t> csize; vector<uint8_t> cacc;
            for (int64_t i = (int64_t)NN - 1; i >= 0; i--) {
                uint32_t s = fin[i]; if (compid[s] != 0xFFFFFFFFu) continue;
                compid[s] = ncomp; stack2.clear(); stack2.push_back(s); uint32_t sz = 0; uint8_t a = 0;
                while (!stack2.empty()) { uint32_t x = stack2.back(); stack2.pop_back(); sz++; a |= layerOf_acc[x]; for (uint32_t q = ro[x]; q < ro[x + 1]; q++) { uint32_t y = re[q]; if (compid[y] == 0xFFFFFFFFu) { compid[y] = ncomp; stack2.push_back(y); } } }
                csize.push_back(sz); cacc.push_back(a); ncomp++;
            }
            for (int l = 0; l < Lo; l++) for (uint32_t v = 0; v < G_[l].n; v++) { uint32_t c = compid[gb[l] + v]; if (csize[c] >= 2 && cacc[c]) { on[l][v] = 1; closed++; } }
        }
        // E_acc(K): per layer windows (bytes), sorted
        ull Etot = 0, naccE = 0; vector<vector<uint8_t>> NP(Lo);
        for (int l = 0; l < Lo; l++) {
            LayerG& A = G_[l]; LayerI& I = Ls[l]; int c0 = NB + I.j + Q * MM;
            for (uint64_t c = 0; c < A.nc; c++) if (A.alive[c] && on[l][A.did[c]]) {
                Etot++; const uint8_t* p = I.par_cells.data() + (c / DV) * Km1;
                NP[l].insert(NP[l].end(), p, p + Km1); NP[l].push_back((uint8_t)(c % DV));
                int w0 = (K == 1) ? (int)(c % DV) : (int)p[0]; if (w0 != row(I.t, c0)) naccE++;
            }
        }
        // exact fold orbits of any period inside Cyc_acc (genuine addition): functional graph of the one-lap return map on the anchor layer
        ull exactO = 0;
        if (Etot && !noexact) {
            int anc = -1; for (int l = 0; l < Lo; l++) if (!NP[l].empty() && (anc < 0 || NP[l].size() < NP[anc].size())) anc = l;
            auto inE = [&](int l, const int* w) -> bool { uint8_t tmp[64]; for (int i = 0; i < Km1; i++) tmp[i] = (uint8_t)w[i]; ll pi = find_parent(Ls[l], tmp, Km1); if (pi < 0) return false; uint64_t c = pi * DV + w[K - 1]; LayerG& A = G_[l]; if (!A.alive[c]) return false; return on[l][A.did[c]]; };
            uint64_t na = NP[anc].size() / K;
            std::unordered_map<std::string, int64_t> idx; idx.reserve(na * 2);
            for (uint64_t i = 0; i < na; i++) idx[std::string((const char*)NP[anc].data() + i * K, K)] = (int64_t)i;
            vector<int64_t> ret(na, -1);
            for (uint64_t i = 0; i < na; i++) {
                int w0[64], w[64], nw[64]; for (int q = 0; q < K; q++) w0[q] = NP[anc][i * K + q]; memcpy(w, w0, sizeof(int) * K); int l = anc; bool ok = true;
                for (int k = 0; k < TT && ok; k++) { LayerI& I = Ls[l]; if (!fstep(I.t, I.j, I.par, w, K, Q + 1, nw)) { ok = false; break; } l = (l + 1) % Lo; if (!inE(l, nw)) { ok = false; break; } memcpy(w, nw, sizeof(int) * K); }
                if (ok) { std::string key(K, 0); for (int q = 0; q < K; q++) key[q] = (char)w[q]; auto it = idx.find(key); ret[i] = it == idx.end() ? -1 : it->second; }
            }
            vector<uint8_t> col(na, 0);
            for (uint64_t i = 0; i < na; i++) { if (col[i]) continue; vector<int64_t> path; int64_t x = (int64_t)i; while (x >= 0 && col[x] == 0) { col[x] = 1; path.push_back(x); x = ret[x]; }
                if (x >= 0 && col[x] == 1) { size_t z = 0; while (path[z] != x) z++; exactO += path.size() - z; printf("EXACT PERIODIC K=%d laps=%zu anchor layer %d win", K, path.size() - z, anc); for (int q = 0; q < K; q++) printf(" %d", (int)NP[anc][(uint64_t)x * K + q]); puts(""); }
                for (int64_t y : path) col[y] = 2; }
        }
        string cmpmsg;
        printf("K=%d T=%d orbit=%d candidates=%llu core=%llu edges=%llu acceptingInCore=%llu sourcesClosed=%llu E_acc=%llu acceptingInEacc=%llu exactOrbits=%llu rounds=%d | %.1fs (%.0fs)%s\n", K, TT, which, (ull)Ntot, core, redges, nacc, closed, Etot, naccE, exactO, rounds, now_s() - T0, now_s() - Tst, cmpmsg.c_str()); fflush(stdout);
        for (int l = 0; l < Lo; l++) { Ls[l].par_cells.swap(NP[l]); Ls[l].np = Ls[l].par_cells.size() / K; vector<uint32_t>().swap(Ls[l].slot); }
        if (Etot == 0) { printf("E_acc(K=%d) EMPTY\n", K); break; }
    }
    return 0;
}
