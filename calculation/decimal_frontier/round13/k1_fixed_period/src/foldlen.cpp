#include <functional>
#include <array>
typedef unsigned long long ull;
// r13b foldlen: inside an E_acc file (eset3, K, WORDS=4) compute the functional graph of the exact fold map F_K restricted to the set and the
// longest chain length (number of consecutive F_K steps staying inside E_acc).  usage: foldlen lat.tbl orbit K FILE
#include "kcommon.h"
#include <map>
struct K4 { uint64_t w[4]; bool operator<(const K4& o) const { for (int i = 3; i >= 0; i--) if (w[i] != o.w[i]) return w[i] < o.w[i]; return false; } bool operator==(const K4& o) const { for (int i = 0; i < 4; i++) if (w[i] != o.w[i]) return false; return true; } };
struct H4 { size_t operator()(const K4& k) const { return mix64(k.w[0] ^ mix64(k.w[1] ^ mix64(k.w[2] ^ mix64(k.w[3])))); } };
#include <unordered_map>
int main(int argc, char** argv) {
    load_tbl(argv[1]); int which = atoi(argv[2]); int K = atoi(argv[3]); FILE* f = fopen(argv[4], "rb"); if (!f) { perror(argv[4]); return 1; }
    int NPH = 2 * P_ * M_; std::vector<int> orb(NPH, -1); std::vector<int> reps; int norb = 0;
    for (int s = 0; s < NPH; s++) { if (orb[s] >= 0) continue; reps.push_back(s); int t, j, p; phase_dec(s, t, j, p); int x = s; do { orb[x] = norb; int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; x = phase_id(t, j, p); } while (x != s); norb++; }
    std::vector<std::array<int,3>> Ph; { int t, j, p; phase_dec(reps[which], t, j, p); int x = reps[which]; do { Ph.push_back({t, j, p}); int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; x = phase_id(t, j, p); } while (x != reps[which]); }
    int Lo2 = Ph.size(); int lo, wds; fread(&lo, 4, 1, f); fread(&wds, 4, 1, f); if (lo != Lo2 || wds != 4) { puts("bad header"); return 1; }
    std::vector<std::unordered_map<K4, uint32_t, H4>> idx(Lo2); std::vector<std::vector<K4>> st(Lo2);
    ull tot = 0;
    for (int l = 0; l < Lo2; l++) { uint64_t n; fread(&n, 8, 1, f); st[l].resize(n); fread(st[l].data(), sizeof(K4), n, f); idx[l].reserve(n * 2); for (uint64_t i = 0; i < n; i++) idx[l][st[l][i]] = i; tot += n; }
    // F map as (l,i) -> index in next layer or -1
    std::vector<std::vector<int>> nxt(Lo2);
    auto toKey = [&](const int* w, int KK) { K4 k; memset(&k, 0, sizeof k); for (int i = 0; i < KK; i++) k.w[i / 12] |= (uint64_t)w[i] << (5 * (i % 12)); return k; };
    ull inside = 0;
    for (int l = 0; l < Lo2; l++) {
        nxt[l].assign(st[l].size(), -1); int nl = (l + 1) % Lo2; int t = Ph[l][0], j = Ph[l][1], par = Ph[l][2];
        for (size_t i = 0; i < st[l].size(); i++) {
            int w[64], nw[64]; for (int q = 0; q < K; q++) w[q] = (st[l][i].w[q / 12] >> (5 * (q % 12))) & 31;
            if (!exact_step(K, t, j, par, w, nw)) continue;
            auto it = idx[nl].find(toKey(nw, K)); if (it == idx[nl].end()) continue; nxt[l][i] = it->second; inside++;
        }
    }
    // longest path by memo DFS (graph is functional; detect cycles)
    std::vector<std::vector<int>> dp(Lo2); for (int l = 0; l < Lo2; l++) dp[l].assign(st[l].size(), -2);
    int best = 0; int bestl = -1; ull cyc = 0; std::map<int, ull> hist;
    std::function<int(int,int)> go = [&](int l, int i) -> int {
        if (dp[l][i] != -2) return dp[l][i]; if (nxt[l][i] < 0) { dp[l][i] = 0; return 0; } dp[l][i] = -3; int v = go((l + 1) % Lo2, nxt[l][i]); int r = v == -3 ? -3 : v + 1; if (v == -3) { cyc++; r = -3; } dp[l][i] = r; return r; };
    for (int l = 0; l < Lo2; l++) for (size_t i = 0; i < st[l].size(); i++) { int d = go(l, i); hist[d]++; if (d > best) { best = d; bestl = l; } }
    printf("foldlen K=%d states=%llu F-successors-inside=%llu longest-chain=%d (from layer %d) cycles-seen=%llu  hist:", K, tot, inside, best, bestl, cyc); int c = 0; for (auto& p : hist) { if (++c > 12) break; printf(" %d:%llu", p.first, p.second); } puts("");
    return 0;
}
