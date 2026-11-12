// Rooted-band hunt, base 10, outer frame: for a time period T enumerate every overflow clock that the top column
// can realise, then build the rooted column chain and report every clock that carries an infinite (cyclic) structure.
// usage: census T [cap]
#include <bits/stdc++.h>
using namespace std;
static const int B = 10;
static int P;
static vector<int> ga;
static vector<uint8_t> Ha, Hb, Hc, Hd, Hs, Hcp, A, Bv, D;
static vector<string> emitted;
static inline string packn(const uint8_t* a, const uint8_t* b, const uint8_t* c, const uint8_t* d) {
    string s(2 * P, 0);
    for (int t = 0; t < P; t++) { s[2 * t] = (char)(a[t] * 16 + b[t]); s[2 * t + 1] = (char)(c[t] * 4 + d[t]); }
    return s;
}
static inline void unpackn(const string& s, uint8_t* a, uint8_t* b, uint8_t* c, uint8_t* d) {
    for (int t = 0; t < P; t++) { uint8_t x = (uint8_t)s[2 * t], y = (uint8_t)s[2 * t + 1]; a[t] = x >> 4; b[t] = x & 15; c[t] = y >> 2; d[t] = y & 3; }
}
static void dfs(int t) {
    if (t == P) { if (A[P] == A[0] && Bv[P] == Bv[0]) emitted.push_back(packn(A.data(), Bv.data(), Hcp.data(), D.data())); return; }
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
static void expand(const string& H) {
    unpackn(H, Ha.data(), Hb.data(), Hc.data(), Hd.data());
    for (int t = 0; t < P; t++) { Hs[t] = Ha[t] + Hb[t]; Hcp[t] = (Hs[t] + Hc[t] >= B) ? 1 : 0; }
    emitted.clear();
    bool b0known = (ga[P - 1] == 1 && Hd[P - 1] != 2);
    int b0fix = b0known ? (Hs[P - 1] + Hd[P - 1]) % B : -1;
    for (int a0 = 0; a0 < B; a0++) for (int b0 = 0; b0 < B; b0++) { if (b0known && b0 != b0fix) continue; A[0] = a0; Bv[0] = b0; dfs(0); }
}
struct Cyc { int size; int kind; int depth; };   // kind 1 = 9-wire, 2 = uniform, 0 = lattice
struct Res { int nodes; bool complete; int live; vector<Cyc> cyc; };
static Res closure(const vector<int>& g, int cap) {
    ga = g; P = g.size();
    Ha.assign(P, 0); Hb.assign(P, 0); Hc.assign(P, 0); Hd.assign(P, 0); Hs.assign(P, 0); Hcp.assign(P, 0);
    A.assign(P + 1, 0); Bv.assign(P + 1, 0); D.assign(P, 0);
    vector<uint8_t> z(P, 0), dg(P);
    for (int t = 0; t < P; t++) dg[t] = g[t];
    string root = packn(z.data(), z.data(), z.data(), dg.data());
    unordered_map<string, int> id; vector<string> nodes; vector<vector<int>> edges; vector<int> depth; deque<int> dq;
    expand(root);
    vector<string> st = emitted;
    for (auto& S : st) if (!id.count(S)) { id[S] = nodes.size(); nodes.push_back(S); edges.emplace_back(); depth.push_back(0); dq.push_back(nodes.size() - 1); }
    Res R; R.complete = true;
    while (!dq.empty()) {
        int i = dq.front(); dq.pop_front();
        string H = nodes[i]; expand(H);
        vector<string> em = emitted;
        for (auto& S : em) {
            int w; auto it = id.find(S);
            if (it == id.end()) { w = nodes.size(); id[S] = w; nodes.push_back(S); edges.emplace_back(); depth.push_back(depth[i] + 1); dq.push_back(w); } else w = it->second;
            edges[i].push_back(w);
        }
        if ((int)nodes.size() > cap) { R.complete = false; break; }
    }
    int n = nodes.size(); R.nodes = n;
    vector<int> index(n, -1), low(n, 0), comp(n, -1); vector<char> onst(n, 0); vector<int> stk; int idx = 0, ncomp = 0; vector<int> compsize;
    for (int r = 0; r < n; r++) {
        if (index[r] != -1) continue;
        vector<pair<int, int>> work; work.push_back({r, 0});
        while (!work.empty()) {
            int v = work.back().first; int pi = work.back().second;
            if (pi == 0) { index[v] = low[v] = idx++; stk.push_back(v); onst[v] = 1; }
            bool rec = false;
            while (pi < (int)edges[v].size()) { int w = edges[v][pi++]; if (index[w] == -1) { work.back().second = pi; work.push_back({w, 0}); rec = true; break; } else if (onst[w]) low[v] = min(low[v], index[w]); }
            if (rec) continue;
            work.pop_back();
            if (!work.empty()) { int u = work.back().first; low[u] = min(low[u], low[v]); }
            if (low[v] == index[v]) { int sz = 0; while (true) { int w = stk.back(); stk.pop_back(); onst[w] = 0; comp[w] = ncomp; sz++; if (w == v) break; } compsize.push_back(sz); ncomp++; }
        }
    }
    vector<char> cyc(ncomp, 0);
    for (int v = 0; v < n; v++) { if (compsize[comp[v]] > 1) cyc[comp[v]] = 1; else for (int w : edges[v]) if (w == v) cyc[comp[v]] = 1; }
    vector<char> livec(ncomp, 0); vector<vector<int>> members(ncomp);
    for (int v = 0; v < n; v++) members[comp[v]].push_back(v);
    for (int k = 0; k < ncomp; k++) { if (cyc[k]) { livec[k] = 1; continue; } for (int v : members[k]) for (int w : edges[v]) if (livec[comp[w]]) livec[k] = 1; }
    R.live = 0; for (int v = 0; v < n; v++) if (livec[comp[v]]) R.live++;
    for (int k = 0; k < ncomp; k++) if (cyc[k]) {
        int v = members[k][0]; int md = INT_MAX; for (int u : members[k]) md = min(md, depth[u]);
        bool wire = true; for (int t = 0; t < P; t++) { uint8_t x = (uint8_t)nodes[v][2 * t]; if ((x >> 4) + (x & 15) != B - 1) wire = false; }
        R.cyc.push_back({compsize[k], wire ? 1 : (compsize[k] == 1 ? 2 : 0), md});
    }
    return R;
}
// ---- clock enumeration from the top column ----
static int T; static vector<int> gw; static unordered_set<string> clocks; static long long nhist = 0;
static string canon(const vector<int>& g) {
    string s(T, '0'); for (int t = 0; t < T; t++) s[t] = '0' + g[t];
    string best = s; string dd = s + s;
    for (int r = 1; r < T; r++) { if (dd.compare(r, T, best) < 0) best = dd.substr(r, T); }
    return best;
}
static void cdfs(int t, int x, int h, int x0) {
    if (t == T) { if (x == x0 && h == 1 && gw[T - 1] == 1) { nhist++; clocks.insert(canon(gw)); } return; }
    int s = x + h;
    if (s >= 10) { gw[t] = 1; cdfs(t + 1, s - 10, 1, x0); }
    else if (s == 9) { gw[t] = 1; cdfs(t + 1, 9, 1, x0); gw[t] = 0; cdfs(t + 1, 9, 9, x0); }
    else { gw[t] = 0; cdfs(t + 1, s, s, x0); cdfs(t + 1, s, s + 1, x0); }
}
int main(int argc, char** argv) {
    if (argc > 2 && string(argv[1]) == "-c") {
        string s = argv[2]; int cap = argc > 3 ? atoi(argv[3]) : 1000000; T = s.size();
        vector<int> g(T); int S = 0; for (int t = 0; t < T; t++) { g[t] = s[t] - '0'; S += g[t]; }
        Res R = closure(g, cap);
        printf("T=%d clock=%s S=%d nodes=%d complete=%d live=%d cycles:", T, s.c_str(), S, R.nodes, R.complete ? 1 : 0, R.live);
        for (auto& c : R.cyc) printf(" [m=%d %s depth=%d%s]", c.size, c.kind == 1 ? "wire" : (c.kind == 2 ? "uniform" : "lattice"), c.depth, (c.kind == 0 && S % c.size == 0) ? " m|S" : "");
        printf("\n"); return 0;
    }
    T = atoi(argv[1]); int cap = argc > 2 ? atoi(argv[2]) : 60000;
    gw.assign(T, 0);
    for (int x0 = 0; x0 < 10; x0++) cdfs(0, x0, 1, x0);
    long long nclock = clocks.size(), nlive = 0, ncap = 0; int maxnodes = 0;
    vector<string> cl(clocks.begin(), clocks.end()); sort(cl.begin(), cl.end());
    for (auto& s : cl) {
        vector<int> g(T); int S = 0; for (int t = 0; t < T; t++) { g[t] = s[t] - '0'; S += g[t]; }
        Res R = closure(g, cap);
        maxnodes = max(maxnodes, R.nodes);
        if (!R.complete) ncap++;
        if (R.live > 0 || !R.complete) {
            if (R.live > 0) nlive++;
            printf("T=%d clock=%s S=%d nodes=%d complete=%d live=%d cycles:", T, s.c_str(), S, R.nodes, R.complete ? 1 : 0, R.live);
            for (auto& c : R.cyc) printf(" [m=%d %s depth=%d%s]", c.size, c.kind == 1 ? "wire" : (c.kind == 2 ? "uniform" : "lattice"), c.depth, (c.kind == 0 && S % c.size == 0) ? " m|S" : "");
            printf("\n"); fflush(stdout);
        }
    }
    printf("SUMMARY T=%d root_histories=%lld clocks=%lld live=%lld capped=%lld maxnodes=%d\n", T, nhist, nclock, nlive, ncap, maxnodes);
    return 0;
}
