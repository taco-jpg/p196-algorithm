// Lean rooted closure for one clock (outer frame), with depth histogram and the "born periodic" fold test:
// a certificate without centre is an infinite walk in which every column satisfies the fold conditions during
// the steps in which it is the innermost column.
// usage: bigclos CLOCK CAP [dumpfile]
#include <bits/stdc++.h>
using namespace std;
static const int B = 10;
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
static vector<uint8_t> pool; static vector<uint32_t> table; static uint64_t mask; static vector<uint32_t> parent; static vector<uint16_t> depth;
static inline uint64_t hashn(const uint8_t* s) { uint64_t h = 1469598103934665603ULL; for (int i = 0; i < 2 * P; i++) { h ^= s[i]; h *= 1099511628211ULL; } h ^= h >> 29; h *= 0xbf58476d1ce4e5b9ULL; h ^= h >> 32; return h; }
static inline int64_t lookup(const uint8_t* s) {
    uint64_t h = hashn(s) & mask;
    while (true) { uint32_t v = table[h]; if (v == 0xffffffffu) return -1; if (memcmp(&pool[(size_t)v * 2 * P], s, 2 * P) == 0) return v; h = (h + 1) & mask; }
}
static inline uint32_t insert(const uint8_t* s, uint32_t par, int dep) {
    uint64_t h = hashn(s) & mask;
    while (true) { uint32_t v = table[h]; if (v == 0xffffffffu) break; if (memcmp(&pool[(size_t)v * 2 * P], s, 2 * P) == 0) return v; h = (h + 1) & mask; }
    uint32_t n = (uint32_t)(pool.size() / (2 * P)); pool.insert(pool.end(), s, s + 2 * P); table[h] = n; parent.push_back(par); depth.push_back((uint16_t)dep); return n;
}
// fold test: column born at time tb (step tb-1 overflowed)
static int birth_ok(const uint8_t* H, int tb) {
    int t = tb, stage = 0;
    while (true) {
        int tt = t % P; uint8_t x = H[2 * tt], y = H[2 * tt + 1]; int a = x >> 4, b = x & 15, c = y >> 2, d = y & 3; int s = a + b;
        if (stage == 0) { if (a != b || !(d == 2 || d == c)) return -1; }
        else { int cp = (s + c >= B) ? 1 : 0; if (!(d == 2 || d == cp)) return -1; }
        if (ga[tt] == 1) { stage++; if (stage == 2) return (t + 1) % P; }
        t++;
    }
}
int main(int argc, char** argv) {
    string s = argv[1]; long long cap = atoll(argv[2]); P = s.size(); ga.resize(P); for (int t = 0; t < P; t++) ga[t] = s[t] - '0';
    Ha.assign(P, 0); Hb.assign(P, 0); Hc.assign(P, 0); Hd.assign(P, 0); Hs.assign(P, 0); Hcp.assign(P, 0); A.assign(P + 1, 0); Bv.assign(P + 1, 0); D.assign(P, 0);
    uint64_t tsz = 1; while (tsz < (uint64_t)cap * 2) tsz <<= 1; mask = tsz - 1; table.assign(tsz, 0xffffffffu);
    pool.reserve((size_t)min(cap, 20000000LL) * 2 * P);
    vector<uint8_t> z(P, 0), dg(P), root(2 * P); for (int t = 0; t < P; t++) dg[t] = ga[t];
    packn(root.data(), z.data(), z.data(), z.data(), dg.data());
    expand(root.data()); { vector<uint8_t> em = emitted; int k = nem; for (int e = 0; e < k; e++) insert(&em[(size_t)e * 2 * P], 0xffffffffu, 0); }
    size_t i = 0; bool complete = true; vector<uint8_t> cur(2 * P); int lastd = -1; size_t lvlstart = 0;
    while (i < pool.size() / (2 * P)) {
        if (depth[i] != lastd) { if (lastd >= 0) { fprintf(stderr, "depth %d: %zu nodes\n", lastd, i - lvlstart); } lastd = depth[i]; lvlstart = i; }
        memcpy(cur.data(), &pool[i * 2 * P], 2 * P); expand(cur.data());
        vector<uint8_t> em(emitted.begin(), emitted.begin() + (size_t)nem * 2 * P); int k = nem;
        for (int e = 0; e < k; e++) insert(&em[(size_t)e * 2 * P], (uint32_t)i, depth[i] + 1);
        i++;
        if ((long long)(pool.size() / (2 * P)) > cap) { complete = false; break; }
    }
    size_t n = pool.size() / (2 * P);
    fprintf(stderr, "depth %d: %zu nodes (processed up to %zu)\n", lastd, i - lvlstart, i);
    printf("clock=%s nodes=%zu complete=%d expanded=%zu\n", s.c_str(), n, complete ? 1 : 0, i);
    // fold test
    vector<int> births; for (int t = 0; t < P; t++) if (ga[(t + P - 1) % P] == 1) births.push_back(t);
    unordered_map<uint64_t, int> ok; // key = node*64 + tb  -> next tb
    for (size_t v = 0; v < n; v++) for (int tb : births) { int nx = birth_ok(&pool[v * 2 * P], tb); if (nx >= 0) ok[(uint64_t)v * 64 + tb] = nx; }
    printf("birth-compatible pairs: %zu\n", ok.size());
    unordered_map<uint64_t, vector<uint64_t>> adj; unordered_set<uint64_t> unexp;
    for (auto& kv : ok) {
        uint64_t v = kv.first / 64; int nx = kv.second;
        if (v >= i) { unexp.insert(kv.first); continue; }   // not expanded (cap): unknown successors
        memcpy(cur.data(), &pool[v * 2 * P], 2 * P); expand(cur.data());
        vector<uint64_t> out;
        for (int e = 0; e < nem; e++) { int64_t w = lookup(&emitted[(size_t)e * 2 * P]); if (w >= 0 && ok.count((uint64_t)w * 64 + nx)) out.push_back((uint64_t)w * 64 + nx); }
        adj[kv.first] = out;
    }
    unordered_set<uint64_t> alive; for (auto& kv : ok) alive.insert(kv.first);
    bool ch = true; size_t walklen = 0;
    while (ch) { ch = false; walklen++; vector<uint64_t> kill; for (uint64_t v : alive) { if (unexp.count(v)) continue; bool any = false; for (uint64_t w : adj[v]) if (alive.count(w)) { any = true; break; } if (!any) kill.push_back(v); } for (uint64_t v : kill) { alive.erase(v); ch = true; } }
    size_t real = 0; for (uint64_t v : alive) if (!unexp.count(v)) real++;
    printf("pairs surviving pruning: %zu (of which expanded: %zu, unexpanded frontier: %zu); pruning rounds=%zu\n", alive.size(), real, alive.size() - real, walklen);
    if (real > 0 && argc > 3) {
        FILE* f = fopen(argv[3], "w");
        for (uint64_t v : alive) { if (unexp.count(v)) continue; uint64_t node = v / 64; int tb = v % 64; fprintf(f, "%llu %d %d :", (unsigned long long)node, tb, depth[node]); for (int t = 0; t < 2 * P; t++) fprintf(f, " %d", pool[node * 2 * P + t]); fprintf(f, " | par %u\n", parent[node]); }
        fclose(f);
    }
    return 0;
}
