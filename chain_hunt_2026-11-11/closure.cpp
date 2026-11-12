// Column-history chain closure in a sheared frame (see chain.py for the rules).
// Input (text, stdin):
//   B P maxnodes dump(0/1)
//   alpha[0..P-1]
//   gamma[0..P-1]
//   npar            (number of parity sequences for mirror tests, 0..2)
//   for each: case(1=i,2=ii) par[0..P-1]
//   nstart
//   for each start: a[P] b[P] c[P] d[P]   (d: 0,1,2=wildcard)
// Output: summary on stdout; if dump=1, nodes -> nodes.bin (2P bytes each), edges -> edges.bin (int32 pairs)
#include <bits/stdc++.h>
using namespace std;
static int B, P;
static vector<int> al, ga;
static vector<uint8_t> Ha, Hb, Hc, Hd, Hs, Hcp;
static vector<uint8_t> A, Bv, D;
static vector<string> emitted;
static inline string packn(const uint8_t* a, const uint8_t* b, const uint8_t* c, const uint8_t* d) {
    string s(2 * P, 0);
    for (int t = 0; t < P; t++) { s[2 * t] = (char)(a[t] * 16 + b[t]); s[2 * t + 1] = (char)(c[t] * 4 + d[t]); }
    return s;
}
static inline void unpackn(const string& s, uint8_t* a, uint8_t* b, uint8_t* c, uint8_t* d) {
    for (int t = 0; t < P; t++) { uint8_t x = (uint8_t)s[2 * t], y = (uint8_t)s[2 * t + 1]; a[t] = x >> 4; b[t] = x & 15; c[t] = y >> 2; d[t] = y & 3; }
}
static long long dfs_calls = 0;
static void dfs(int t) {
    dfs_calls++;
    if (t == P) {
        if (A[P] == A[0] && Bv[P] == Bv[0]) emitted.push_back(packn(A.data(), Bv.data(), Hcp.data(), D.data()));
        return;
    }
    int sp = A[t] + Bv[t];
    if (al[t] == 1 && (sp + Hcp[t]) % B != Ha[(t + 1) % P]) return;
    int dt = Hd[t];
    int dopts[2], nd;
    if (dt != 2) {
        if (sp == B - 1) { dopts[0] = dt; nd = 1; }
        else {
            if ((sp >= B ? 1 : 0) != dt) return;
            if (ga[t] == 0) { dopts[0] = 0; dopts[1] = 1; nd = 2; } else { dopts[0] = 2; nd = 1; }
        }
    } else {
        if (sp == B - 1) { dopts[0] = 0; dopts[1] = 1; nd = 2; } else { dopts[0] = 2; nd = 1; }
    }
    for (int k = 0; k < nd; k++) {
        int dp = dopts[k];
        D[t] = dp;
        int nb;
        if (ga[t] == 0) nb = (sp + dp) % B;
        else {
            int actual;
            if (dt != 2) actual = dt; else actual = (sp == B - 1) ? dp : (sp >= B ? 1 : 0);
            nb = (Hs[t] + actual) % B;
        }
        Bv[t + 1] = nb;
        if (al[t] == 0) { A[t + 1] = (sp + Hcp[t]) % B; dfs(t + 1); }
        else { for (int na = 0; na < B; na++) { A[t + 1] = na; dfs(t + 1); } }
    }
}
static void expand(const string& H) {
    Ha.assign(P, 0); Hb.assign(P, 0); Hc.assign(P, 0); Hd.assign(P, 0); Hs.assign(P, 0); Hcp.assign(P, 0);
    unpackn(H, Ha.data(), Hb.data(), Hc.data(), Hd.data());
    for (int t = 0; t < P; t++) { Hs[t] = Ha[t] + Hb[t]; Hcp[t] = (Hs[t] + Hc[t] >= B) ? 1 : 0; }
    emitted.clear();
    A.assign(P + 1, 0); Bv.assign(P + 1, 0); D.assign(P, 0);
    bool b0known = (ga[P - 1] == 1 && Hd[P - 1] != 2);
    int b0fix = b0known ? (Hs[P - 1] + Hd[P - 1]) % B : -1;
    for (int a0 = 0; a0 < B; a0++) for (int b0 = 0; b0 < B; b0++) {
        if (b0known && b0 != b0fix) continue;
        A[0] = a0; Bv[0] = b0; dfs(0);
    }
}
static inline bool dmatch(int x, int y) { return x == 2 || y == 2 || x == y; }
static bool mirror_edge(const string& H, const string& Hn, const vector<int>& par, int cas) {
    for (int t = 0; t < P; t++) {
        uint8_t x = (uint8_t)H[2 * t], y = (uint8_t)H[2 * t + 1], xn = (uint8_t)Hn[2 * t], yn = (uint8_t)Hn[2 * t + 1];
        int a = x >> 4, b = x & 15, c = y >> 2, d = y & 3, an = xn >> 4, bn = xn & 15, cn = yn >> 2, dn = yn & 3;
        if (cas == 1) {
            if (par[t] == 0) { if (!(an == b && bn == a && dmatch(dn, c) && dmatch(d, cn))) return false; }
            else { if (!(an == bn && dmatch(dn, cn))) return false; }
        } else {
            if (par[t] == 1) { if (!(a == b && dmatch(d, c))) return false; }
            else { if (!(an == b && bn == a && dmatch(dn, c) && dmatch(d, cn))) return false; }
        }
    }
    return true;
}
static void printnode(const string& s) {
    vector<uint8_t> a(P), b(P), c(P), d(P);
    unpackn(s, a.data(), b.data(), c.data(), d.data());
    for (int t = 0; t < P; t++) printf("%d ", a[t]);
    for (int t = 0; t < P; t++) printf("%d ", b[t]);
    for (int t = 0; t < P; t++) printf("%d ", c[t]);
    for (int t = 0; t < P; t++) printf("%d ", d[t]);
    printf("\n");
}
int main() {
    long long maxnodes; int dump;
    if (scanf("%d %d %lld %d", &B, &P, &maxnodes, &dump) != 4) return 1;
    al.resize(P); ga.resize(P);
    for (int t = 0; t < P; t++) scanf("%d", &al[t]);
    for (int t = 0; t < P; t++) scanf("%d", &ga[t]);
    int npar; scanf("%d", &npar);
    vector<int> pcase(npar); vector<vector<int>> pars(npar, vector<int>(P));
    for (int k = 0; k < npar; k++) { scanf("%d", &pcase[k]); for (int t = 0; t < P; t++) scanf("%d", &pars[k][t]); }
    int ns; scanf("%d", &ns);
    unordered_map<string, int> id;
    vector<string> nodes; vector<int> parent; vector<vector<int>> edges;
    deque<int> dq;
    for (int k = 0; k < ns; k++) {
        vector<uint8_t> a(P), b(P), c(P), d(P); int x;
        for (int t = 0; t < P; t++) { scanf("%d", &x); a[t] = x; }
        for (int t = 0; t < P; t++) { scanf("%d", &x); b[t] = x; }
        for (int t = 0; t < P; t++) { scanf("%d", &x); c[t] = x; }
        for (int t = 0; t < P; t++) { scanf("%d", &x); d[t] = x; }
        string s = packn(a.data(), b.data(), c.data(), d.data());
        if (!id.count(s)) { id[s] = nodes.size(); nodes.push_back(s); parent.push_back(-1); edges.emplace_back(); dq.push_back(nodes.size() - 1); }
    }
    bool complete = true;
    struct Cand { int cas, i, w; };
    vector<Cand> cands;
    long long expanded = 0;
    while (!dq.empty()) {
        int i = dq.front(); dq.pop_front();
        string H = nodes[i];
        expand(H);
        expanded++;
        vector<string> em = emitted;
        for (auto& S : em) {
            int w;
            auto it = id.find(S);
            if (it == id.end()) { w = nodes.size(); id[S] = w; nodes.push_back(S); parent.push_back(i); edges.emplace_back(); dq.push_back(w); }
            else w = it->second;
            edges[i].push_back(w);
            for (int k = 0; k < npar; k++) if (mirror_edge(H, S, pars[k], pcase[k])) cands.push_back({pcase[k], i, w});
        }
        if ((long long)nodes.size() > maxnodes) { complete = false; break; }
    }
    int n = nodes.size();
    // Tarjan SCC (iterative)
    vector<int> index(n, -1), low(n, 0), comp(n, -1); vector<char> onst(n, 0); vector<int> st; int idx = 0, ncomp = 0;
    vector<int> compsize;
    for (int r = 0; r < n; r++) {
        if (index[r] != -1) continue;
        vector<pair<int, int>> work; work.push_back({r, 0});
        while (!work.empty()) {
            int v = work.back().first; int pi = work.back().second;
            if (pi == 0) { index[v] = low[v] = idx++; st.push_back(v); onst[v] = 1; }
            bool rec = false;
            while (pi < (int)edges[v].size()) {
                int w = edges[v][pi++];
                if (index[w] == -1) { work.back().second = pi; work.push_back({w, 0}); rec = true; break; }
                else if (onst[w]) low[v] = min(low[v], index[w]);
            }
            if (rec) continue;
            work.pop_back();
            if (!work.empty()) { int u = work.back().first; low[u] = min(low[u], low[v]); }
            if (low[v] == index[v]) {
                int sz = 0;
                while (true) { int w = st.back(); st.pop_back(); onst[w] = 0; comp[w] = ncomp; sz++; if (w == v) break; }
                compsize.push_back(sz); ncomp++;
            }
        }
    }
    vector<char> cyc(ncomp, 0);
    for (int v = 0; v < n; v++) { if (compsize[comp[v]] > 1) cyc[comp[v]] = 1; else for (int w : edges[v]) if (w == v) cyc[comp[v]] = 1; }
    // live nodes: comps come out in reverse topological order (successors first)
    vector<char> livec(ncomp, 0);
    {
        vector<vector<int>> members(ncomp);
        for (int v = 0; v < n; v++) members[comp[v]].push_back(v);
        for (int k = 0; k < ncomp; k++) {
            if (cyc[k]) { livec[k] = 1; continue; }
            for (int v : members[k]) for (int w : edges[v]) if (livec[comp[w]]) livec[k] = 1;
        }
    }
    long long nlive = 0; for (int v = 0; v < n; v++) if (livec[comp[v]]) nlive++;
    printf("NODES %d EXPANDED %lld COMPLETE %d LIVE %lld DFS %lld\n", n, expanded, complete ? 1 : 0, nlive, dfs_calls);
    // cyclic components: size, whether it contains a start node, one representative
    vector<int> startcomp(ncomp, 0);
    for (int v = 0; v < ns && v < n; v++) startcomp[comp[v]] = 1;
    vector<int> rep(ncomp, -1);
    for (int v = 0; v < n; v++) if (rep[comp[v]] == -1) rep[comp[v]] = v;
    for (int k = 0; k < ncomp; k++) if (cyc[k]) { printf("CYC size %d hasstart %d rep %d\n", compsize[k], startcomp[k], rep[k]); }
    for (auto& c : cands) {
        printf("CAND case %d edge %d %d path", c.cas, c.i, c.w);
        vector<int> path; int v = c.i; while (v != -1) { path.push_back(v); v = parent[v]; }
        reverse(path.begin(), path.end());
        for (int x : path) printf(" %d", x);
        printf("\n");
    }
    if (dump) {
        FILE* f = fopen("nodes.bin", "wb"); for (auto& s : nodes) fwrite(s.data(), 1, 2 * P, f); fclose(f);
        f = fopen("edges.bin", "wb"); for (int v = 0; v < n; v++) for (int w : edges[v]) { int32_t pr[2] = {v, w}; fwrite(pr, 4, 2, f); } fclose(f);
        f = fopen("comp.bin", "wb"); fwrite(comp.data(), 4, n, f); fclose(f);
    }
    return 0;
}
