// Lean rooted closure for one clock (outer frame): complete BFS, liveness (infinite chains), cyclic components,
// and the centre-free fold test (every column periodic from birth).
// usage: bigclos2 CLOCK CAPNODES
#include <bits/stdc++.h>
using namespace std;
static int B = 10;
static int P;
static vector<int> ga;
static vector<uint8_t> Ha, Hb, Hc, Hd, Hs, Hcp, A, Bv, D;
static vector<uint8_t> emitted; static int nem;
static inline void packn(uint8_t* s, const uint8_t* a, const uint8_t* b, const uint8_t* c, const uint8_t* d) {
    for (int t = 0; t < P; t++) { s[2 * t] = (uint8_t)(a[t] * 16 + b[t]); s[2 * t + 1] = (uint8_t)(c[t] * 4 + d[t]); }
}
static inline void unpackn(const uint8_t* s, uint8_t* a, uint8_t* b, uint8_t* c, uint8_t* d) {
    for (int t = 0; t < P; t++) { uint8_t x = s[2 * t], y = s[2 * t + 1]; a[t] = x >> 4; b[t] = x & 15; c[t] = y >> 2; d[t] = y & 3; }
}
static void dfs(int t) {
    if (t == P) { if (A[P] == A[0] && Bv[P] == Bv[0]) { emitted.resize((size_t)(nem + 1) * 2 * P); packn(&emitted[(size_t)nem * 2 * P], A.data(), Bv.data(), Hcp.data(), D.data()); nem++; } return; }
    int sp = A[t] + Bv[t];
    int dt = Hd[t];
    int dopts[2], nd;
    if (dt != 2) {
        if (sp == B - 1) { dopts[0] = dt; nd = 1; }
        else { if ((sp >= B ? 1 : 0) != dt) return; if (ga[t] == 0) { dopts[0] = 0; dopts[1] = 1; nd = 2; } else { dopts[0] = 2; nd = 1; } }
    } else { if (sp == B - 1) { dopts[0] = 0; dopts[1] = 1; nd = 2; } else { dopts[0] = 2; nd = 1; } }
    for (int k = 0; k < nd; k++) {
        int dp = dopts[k]; D[t] = dp; int nb;
        if (ga[t] == 0) nb = (sp + dp) % B;
        else { int actual; if (dt != 2) actual = dt; else actual = (sp == B - 1) ? dp : (sp >= B ? 1 : 0); nb = (Hs[t] + actual) % B; }
        Bv[t + 1] = nb; A[t + 1] = (sp + Hcp[t]) % B; dfs(t + 1);
    }
}
static void expand(const uint8_t* H) {
    unpackn(H, Ha.data(), Hb.data(), Hc.data(), Hd.data());
    for (int t = 0; t < P; t++) { Hs[t] = Ha[t] + Hb[t]; Hcp[t] = (Hs[t] + Hc[t] >= B) ? 1 : 0; }
    nem = 0;
    bool b0known = (ga[P - 1] == 1 && Hd[P - 1] != 2);
    int b0fix = b0known ? (Hs[P - 1] + Hd[P - 1]) % B : -1;
    for (int a0 = 0; a0 < B; a0++) for (int b0 = 0; b0 < B; b0++) { if (b0known && b0 != b0fix) continue; A[0] = a0; Bv[0] = b0; dfs(0); }
}
static vector<uint8_t> pool; static vector<uint32_t> table; static uint64_t mask; static vector<uint16_t> depth;
static inline uint64_t hashn(const uint8_t* s) { uint64_t h = 1469598103934665603ULL; for (int i = 0; i < 2 * P; i++) { h ^= s[i]; h *= 1099511628211ULL; } h ^= h >> 29; h *= 0xbf58476d1ce4e5b9ULL; h ^= h >> 32; return h; }
static inline uint32_t insert(const uint8_t* s, int dep) {
    uint64_t h = hashn(s) & mask;
    while (true) { uint32_t v = table[h]; if (v == 0xffffffffu) break; if (memcmp(&pool[(size_t)v * 2 * P], s, 2 * P) == 0) return v; h = (h + 1) & mask; }
    uint32_t n = (uint32_t)(pool.size() / (2 * P)); pool.insert(pool.end(), s, s + 2 * P); table[h] = n; depth.push_back((uint16_t)dep); return n;
}
static int birth_ok(const uint8_t* H, int tb) {
    int t = tb, stage = 0;
    while (true) {
        int tt = t % P; uint8_t x = H[2 * tt], y = H[2 * tt + 1]; int a = x >> 4, b = x & 15, c = y >> 2, d = y & 3; int s = a + b;
        if (stage == 0) { if (a != b || !(d == 2 || d == c)) return -1; }
        else { int cp = (s + c >= B) ? 1 : 0; if (!(d == 2 || d == cp)) return -1; }
        if (ga[tt] == 1) { stage++; if (stage == 2) return (t + 1) % P; }
        t++;
        if (t > tb + 3 * P) return -1;
    }
}
int main(int argc, char** argv) {
    string s = argv[1]; long long cap = atoll(argv[2]); if (argc > 3) B = atoi(argv[3]); P = s.size(); ga.resize(P); int S = 0; for (int t = 0; t < P; t++) { ga[t] = s[t] - '0'; S += ga[t]; }
    Ha.assign(P, 0); Hb.assign(P, 0); Hc.assign(P, 0); Hd.assign(P, 0); Hs.assign(P, 0); Hcp.assign(P, 0); A.assign(P + 1, 0); Bv.assign(P + 1, 0); D.assign(P, 0);
    uint64_t tsz = 1 << 16; table.assign(tsz, 0xffffffffu); mask = tsz - 1;
    vector<uint8_t> z(P, 0), dg(P), root(2 * P); for (int t = 0; t < P; t++) dg[t] = ga[t];
    packn(root.data(), z.data(), z.data(), z.data(), dg.data());
    expand(root.data()); { vector<uint8_t> em = emitted; int k = nem; for (int e = 0; e < k; e++) insert(&em[(size_t)e * 2 * P], 0); }
    vector<uint32_t> eoff; vector<uint32_t> edst; eoff.push_back(0);
    size_t i = 0; bool complete = true; vector<uint8_t> cur(2 * P), em;
    while (i < pool.size() / (2 * P)) {
        size_t n = pool.size() / (2 * P);
        if (n * 2 > tsz) {   // grow table
            tsz <<= 2; mask = tsz - 1; table.assign(tsz, 0xffffffffu);
            for (size_t v = 0; v < n; v++) { uint64_t h = hashn(&pool[v * 2 * P]) & mask; while (table[h] != 0xffffffffu) h = (h + 1) & mask; table[h] = (uint32_t)v; }
        }
        memcpy(cur.data(), &pool[i * 2 * P], 2 * P); expand(cur.data());
        em.assign(emitted.begin(), emitted.begin() + (size_t)nem * 2 * P); int k = nem;
        for (int e = 0; e < k; e++) { uint32_t w = insert(&em[(size_t)e * 2 * P], depth[i] + 1); edst.push_back(w); }
        eoff.push_back((uint32_t)edst.size());
        i++;
        if ((long long)(pool.size() / (2 * P)) > cap) { complete = false; break; }
    }
    size_t n = pool.size() / (2 * P); size_t nexp = i;
    int maxd = 0; for (size_t v = 0; v < n; v++) maxd = max(maxd, (int)depth[v]);
    // liveness: dead = expanded and all successors dead; unexpanded nodes (cap) count as unknown = alive
    vector<uint8_t> dead(n, 0); bool ch = true; int passes = 0;
    while (ch) { ch = false; passes++; for (size_t v = nexp; v-- > 0;) { if (dead[v]) continue; bool all = true; for (uint32_t e = eoff[v]; e < eoff[v + 1]; e++) if (!dead[edst[e]]) { all = false; break; } if (all) { dead[v] = 1; ch = true; } } }
    size_t live = 0, frontier = 0; for (size_t v = 0; v < n; v++) if (!dead[v]) { if (v < nexp) live++; else frontier++; }
    printf("T=%d clock=%s S=%d nodes=%zu complete=%d maxdepth=%d live=%zu frontier=%zu", P, s.c_str(), S, n, complete ? 1 : 0, maxd, live, frontier);
    // cyclic components among live expanded nodes (Tarjan, iterative)
    if (live > 0) {
        vector<uint32_t> L; for (size_t v = 0; v < nexp; v++) if (!dead[v]) L.push_back((uint32_t)v);
        unordered_map<uint32_t, int> idx; for (size_t k = 0; k < L.size(); k++) idx[L[k]] = (int)k;
        int m = L.size(); vector<vector<int>> ad(m);
        for (int k = 0; k < m; k++) { uint32_t v = L[k]; for (uint32_t e = eoff[v]; e < eoff[v + 1]; e++) { auto it = idx.find(edst[e]); if (it != idx.end()) ad[k].push_back(it->second); } }
        vector<int> index(m, -1), low(m, 0), comp(m, -1); vector<char> onst(m, 0); vector<int> stk; int id2 = 0, ncomp = 0; vector<int> csz;
        for (int r = 0; r < m; r++) { if (index[r] != -1) continue; vector<pair<int, int>> work; work.push_back({r, 0});
            while (!work.empty()) { int v = work.back().first; int pi = work.back().second; if (pi == 0) { index[v] = low[v] = id2++; stk.push_back(v); onst[v] = 1; }
                bool rec = false; while (pi < (int)ad[v].size()) { int w = ad[v][pi++]; if (index[w] == -1) { work.back().second = pi; work.push_back({w, 0}); rec = true; break; } else if (onst[w]) low[v] = min(low[v], index[w]); }
                if (rec) continue; work.pop_back(); if (!work.empty()) { int u = work.back().first; low[u] = min(low[u], low[v]); }
                if (low[v] == index[v]) { int sz = 0; while (true) { int w = stk.back(); stk.pop_back(); onst[w] = 0; comp[w] = ncomp; sz++; if (w == v) break; } csz.push_back(sz); ncomp++; } } }
        vector<char> cyc(ncomp, 0); vector<int> mind(ncomp, INT_MAX), rep(ncomp, -1);
        for (int k = 0; k < m; k++) { if (csz[comp[k]] > 1) cyc[comp[k]] = 1; else for (int w : ad[k]) if (w == k) cyc[comp[k]] = 1; mind[comp[k]] = min(mind[comp[k]], (int)depth[L[k]]); rep[comp[k]] = k; }
        printf(" cycles:");
        for (int c = 0; c < ncomp; c++) if (cyc[c]) { const uint8_t* H = &pool[(size_t)L[rep[c]] * 2 * P]; bool wire = true; for (int t = 0; t < P; t++) { uint8_t x = H[2 * t]; if ((x >> 4) + (x & 15) != B - 1) wire = false; }
            printf(" [m=%d %s depth=%d%s]", csz[c], wire ? "wire" : (csz[c] == 1 ? "uniform" : "lattice"), mind[c], (!wire && S % csz[c] == 0) ? " m|S" : ""); }
        // centre-free fold test on live nodes
        vector<int> births; for (int t = 0; t < P; t++) if (ga[(t + P - 1) % P] == 1) births.push_back(t);
        unordered_map<uint64_t, int> ok;
        for (int k = 0; k < m; k++) for (int tb : births) { int nx = birth_ok(&pool[(size_t)L[k] * 2 * P], tb); if (nx >= 0) ok[(uint64_t)k * 64 + tb] = nx; }
        unordered_set<uint64_t> alive; for (auto& kv : ok) alive.insert(kv.first);
        bool c2 = true; int rounds = 0;
        while (c2) { c2 = false; rounds++; vector<uint64_t> kill; for (uint64_t v : alive) { int k = v / 64; int nx = ok[v]; bool any = false; for (int w : ad[k]) if (alive.count((uint64_t)w * 64 + nx)) { any = true; break; } if (!any) kill.push_back(v); } for (uint64_t v : kill) { alive.erase(v); c2 = true; } }
        printf(" born-periodic: compatible=%zu surviving=%zu rounds=%d", ok.size(), alive.size(), rounds);
        if (!alive.empty()) printf(" ***CENTRE-FREE CANDIDATE***");
    }
    printf("\n");
    return 0;
}
