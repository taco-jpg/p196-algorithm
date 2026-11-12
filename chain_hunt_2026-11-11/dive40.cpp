// Exploratory dive: clock (01)^k with time period T=8k. Look for infinite chains made of columns whose period does
// NOT divide 8 (genuinely longer temporal period), entered from the known period-8 rooted structure.
// usage: dive40 K SECONDS SEED [budget]
#include <bits/stdc++.h>
using namespace std;
static const int B = 10;
static int P;
static vector<int> ga;
static vector<uint8_t> Ha, Hb, Hc, Hd, Hs, Hcp, A, Bv, D;
static vector<uint8_t> emitted; static int nem;
static inline void packn(uint8_t* s, const uint8_t* a, const uint8_t* b, const uint8_t* c, const uint8_t* d) { for (int t = 0; t < P; t++) { s[2 * t] = (uint8_t)(a[t] * 16 + b[t]); s[2 * t + 1] = (uint8_t)(c[t] * 4 + d[t]); } }
static inline void unpackn(const uint8_t* s, uint8_t* a, uint8_t* b, uint8_t* c, uint8_t* d) { for (int t = 0; t < P; t++) { uint8_t x = s[2 * t], y = s[2 * t + 1]; a[t] = x >> 4; b[t] = x & 15; c[t] = y >> 2; d[t] = y & 3; } }
static void dfs(int t) {
    if (t == P) { if (A[P] == A[0] && Bv[P] == Bv[0]) { emitted.resize((size_t)(nem + 1) * 2 * P); packn(&emitted[(size_t)nem * 2 * P], A.data(), Bv.data(), Hcp.data(), D.data()); nem++; } return; }
    int sp = A[t] + Bv[t]; int dt = Hd[t]; int dopts[2], nd;
    if (dt != 2) { if (sp == B - 1) { dopts[0] = dt; nd = 1; } else { if ((sp >= B ? 1 : 0) != dt) return; if (ga[t] == 0) { dopts[0] = 0; dopts[1] = 1; nd = 2; } else { dopts[0] = 2; nd = 1; } } }
    else { if (sp == B - 1) { dopts[0] = 0; dopts[1] = 1; nd = 2; } else { dopts[0] = 2; nd = 1; } }
    for (int k = 0; k < nd; k++) { int dp = dopts[k]; D[t] = dp; int nb;
        if (ga[t] == 0) nb = (sp + dp) % B; else { int actual; if (dt != 2) actual = dt; else actual = (sp == B - 1) ? dp : (sp >= B ? 1 : 0); nb = (Hs[t] + actual) % B; }
        Bv[t + 1] = nb; A[t + 1] = (sp + Hcp[t]) % B; dfs(t + 1); }
}
static void expand(const uint8_t* H) {
    unpackn(H, Ha.data(), Hb.data(), Hc.data(), Hd.data());
    for (int t = 0; t < P; t++) { Hs[t] = Ha[t] + Hb[t]; Hcp[t] = (Hs[t] + Hc[t] >= B) ? 1 : 0; }
    nem = 0; bool b0known = (ga[P - 1] == 1 && Hd[P - 1] != 2); int b0fix = b0known ? (Hs[P - 1] + Hd[P - 1]) % B : -1;
    for (int a0 = 0; a0 < B; a0++) for (int b0 = 0; b0 < B; b0++) { if (b0known && b0 != b0fix) continue; A[0] = a0; Bv[0] = b0; dfs(0); }
}
static inline uint64_t hashn(const uint8_t* s) { uint64_t h = 1469598103934665603ULL; for (int i = 0; i < 2 * P; i++) { h ^= s[i]; h *= 1099511628211ULL; } h ^= h >> 29; h *= 0xbf58476d1ce4e5b9ULL; h ^= h >> 32; return h | 1; }
static bool per8(const uint8_t* s) { for (int i = 0; i + 16 < 2 * P; i++) if (s[i] != s[i + 16]) return false; return true; }
int main(int argc, char** argv) {
    int K = atoi(argv[1]); double secs = atof(argv[2]); unsigned seed = atoi(argv[3]); long long budget = argc > 4 ? atoll(argv[4]) : 200000;
    P = 8 * K; ga.resize(P); for (int t = 0; t < P; t++) ga[t] = t & 1;
    Ha.assign(P, 0); Hb.assign(P, 0); Hc.assign(P, 0); Hd.assign(P, 0); Hs.assign(P, 0); Hcp.assign(P, 0); A.assign(P + 1, 0); Bv.assign(P + 1, 0); D.assign(P, 0);
    mt19937 rng(seed);
    // period-8 part: BFS
    vector<vector<uint8_t>> p8; unordered_set<uint64_t> seen8;
    vector<uint8_t> z(P, 0), dg(P), root(2 * P); for (int t = 0; t < P; t++) dg[t] = ga[t]; packn(root.data(), z.data(), z.data(), z.data(), dg.data());
    expand(root.data()); { vector<uint8_t> em = emitted; int k = nem; for (int e = 0; e < k; e++) { const uint8_t* s = &em[(size_t)e * 2 * P]; if (per8(s) && seen8.insert(hashn(s)).second) p8.push_back(vector<uint8_t>(s, s + 2 * P)); } }
    vector<int> dep8(p8.size(), 0);
    for (size_t i = 0; i < p8.size(); i++) { vector<uint8_t> cur = p8[i]; expand(cur.data()); vector<uint8_t> em(emitted.begin(), emitted.begin() + (size_t)nem * 2 * P); int k = nem;
        for (int e = 0; e < k; e++) { const uint8_t* s = &em[(size_t)e * 2 * P]; if (per8(s) && seen8.insert(hashn(s)).second) { p8.push_back(vector<uint8_t>(s, s + 2 * P)); dep8.push_back(dep8[i] + 1); } } }
    fprintf(stderr, "period-8 nodes: %zu\n", p8.size());
    auto t0 = chrono::steady_clock::now();
    unordered_set<uint64_t> done; long long expansions = 0, dives = 0; int gmax = 0; long long entriesSeen = 0; bool found = false;
    map<int, long long> depthHist;
    while (!found) {
        double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count(); if (el > secs) break;
        size_t i = rng() % p8.size(); vector<uint8_t> cur = p8[i]; expand(cur.data());
        vector<vector<uint8_t>> ent; for (int e = 0; e < nem; e++) { const uint8_t* s = &emitted[(size_t)e * 2 * P]; if (!per8(s)) ent.push_back(vector<uint8_t>(s, s + 2 * P)); }
        entriesSeen += ent.size(); if (ent.empty()) continue;
        // a few random entries, DFS each with a budget
        for (int rep = 0; rep < 3 && !found; rep++) {
            vector<uint8_t> start = ent[rng() % ent.size()]; if (done.count(hashn(start.data()))) continue;
            dives++; long long used = 0; int maxd = 0;
            vector<vector<vector<uint8_t>>> stk; vector<size_t> pos; vector<uint64_t> pathh; unordered_map<uint64_t, int> onpath;
            vector<vector<uint8_t>> first; first.push_back(start); stk.push_back(first); pos.push_back(0);
            while (!stk.empty() && used < budget) {
                int d = stk.size() - 1;
                if (pos[d] >= stk[d].size()) { stk.pop_back(); pos.pop_back(); if (!pathh.empty()) { done.insert(pathh.back()); onpath.erase(pathh.back()); pathh.pop_back(); } continue; }
                vector<uint8_t>& nd = stk[d][pos[d]++]; uint64_t h = hashn(nd.data());
                auto it = onpath.find(h);
                if (it != onpath.end()) { printf("CYCLE of new-period nodes: length %d at depth %d (entry from period-8 node at depth %d)\n", (int)pathh.size() - it->second, (int)pathh.size(), dep8[i]); found = true;
                    for (int t = 0; t < P; t++) printf("%d%d ", nd[2 * t] >> 4, nd[2 * t] & 15); printf("\n"); break; }
                if (done.count(h)) continue;
                expand(nd.data()); used++; expansions++;
                vector<vector<uint8_t>> ch; for (int e = 0; e < nem; e++) { const uint8_t* s = &emitted[(size_t)e * 2 * P]; if (!per8(s)) ch.push_back(vector<uint8_t>(s, s + 2 * P)); }
                shuffle(ch.begin(), ch.end(), rng);
                pathh.push_back(h); onpath[h] = pathh.size() - 1; maxd = max(maxd, (int)pathh.size());
                stk.push_back(ch); pos.push_back(0);
            }
            // nodes left on the path when the budget ran out are not marked done
            gmax = max(gmax, maxd); depthHist[min(maxd / 10, 60)]++;
        }
    }
    printf("K=%d T=%d: dives=%lld expansions=%lld entry nodes seen=%lld max chain of new-period columns=%d found_cycle=%d\n", K, P, dives, expansions, entriesSeen, gmax, found ? 1 : 0);
    printf("max-depth histogram (bucket of 10 columns: dives):"); for (auto& kv : depthHist) printf(" %d:%lld", kv.first * 10, kv.second); printf("\n");
    return 0;
}
