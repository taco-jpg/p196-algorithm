// Driven fold machine: a settled periodic column (node) on the left feeds carry and digits into an interior that
// contains the real fold. A seed interior survives as long as the carry it returns equals the one the node needs.
// usage: foldmachine LIVEFILE MAXLEN0 MAXSTEPS
#include <bits/stdc++.h>
using namespace std;
int P, NL; int BASE = 10; vector<int> g; vector<int> ids; vector<array<int,4>> H; // H[v*P+t] = a,b,c,d
static inline int run(int v, int t0, const int* seed, int len0, int maxsteps) {
    static int y[20000], o[20000]; int len = len0; for (int i = 0; i < len; i++) y[i] = seed[i];
    for (int t = 0; t < maxsteps; t++) {
        int tt = (t0 + t) % P; const array<int,4>& h = H[(size_t)v * P + tt];
        int carry = (h[0] + h[1] + h[2] >= BASE) ? 1 : 0;
        for (int i = 0; i < len; i++) { int x = y[i] + y[len - 1 - i] + carry; if (x >= BASE) { o[i] = x - BASE; carry = 1; } else { o[i] = x; carry = 0; } }
        if (h[3] != 2 && carry != h[3]) return t;
        if (g[tt] == 1) { o[len] = (h[0] + h[1] + carry) % BASE; len++; }
        memcpy(y, o, sizeof(int) * len);
        if (len > 19000) return maxsteps;
    }
    return maxsteps;
}
int main(int argc, char** argv) {
    FILE* f = fopen(argv[1], "r"); int maxlen0 = atoi(argv[2]); int maxsteps = atoi(argv[3]); if (argc > 4) BASE = atoi(argv[4]);
    if (fscanf(f, "%d %d", &P, &NL) != 2) return 1; g.resize(P); for (int t = 0; t < P; t++) if (fscanf(f, "%d", &g[t]) != 1) return 1;
    ids.resize(NL); H.resize((size_t)NL * P);
    for (int v = 0; v < NL; v++) { if (fscanf(f, "%d", &ids[v]) != 1) return 1; for (int t = 0; t < P; t++) for (int k = 0; k < 4; k++) if (fscanf(f, "%d", &H[(size_t)v * P + t][k]) != 1) return 1; }
    for (int len0 = 0; len0 <= maxlen0; len0++) {
        long long tot = 1; for (int i = 0; i < len0; i++) tot *= BASE;
        vector<long long> hist(64, 0); int best = 0; long long bestseed = 0; int bestv = 0, bestt = 0; long long runs = 0;
        vector<tuple<int,int,int,long long>> top;
        for (int v = 0; v < NL; v++) for (int t0 = 0; t0 < P; t0++) for (long long sd = 0; sd < tot; sd++) {
            int seed[32]; long long z = sd; for (int i = 0; i < len0; i++) { seed[i] = z % BASE; z /= BASE; }
            int s = run(v, t0, seed, len0, maxsteps); runs++;
            int b = 0; while ((1 << b) <= s && b < 62) b++; hist[b]++;
            if (s > best) { best = s; bestseed = sd; bestv = v; bestt = t0; }
            if (s >= 150) top.push_back(make_tuple(s, ids[v], t0, sd));
        }
        printf("seed length %d: runs=%lld best survival=%d steps (node %d phase %d seed %lld)\n   log2 histogram:", len0, runs, best, ids[bestv], bestt, bestseed);
        for (int b = 0; b < 16; b++) printf(" %lld", hist[b]); printf("\n");
        sort(top.rbegin(), top.rend()); for (size_t k = 0; k < top.size() && k < 8; k++) printf("   %d steps: node %d phase %d seed %lld\n", get<0>(top[k]), get<1>(top[k]), get<2>(top[k]), get<3>(top[k]));
        fflush(stdout);
    }
    return 0;
}
