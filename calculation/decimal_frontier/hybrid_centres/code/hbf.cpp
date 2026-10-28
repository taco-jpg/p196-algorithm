// hbf.cpp -- brute-force enumeration of hybrid centre states (C,c,phase) of width <= W, following the exact dynamics
// usage: hbf b W gam e1 loopvals...   (gam,e1: bit strings of the stream period)
// Finds all cycles of the deterministic dynamics (trimmed state) with max width <= W.  Reports cycles with sum gam - 2A >= 0 (A = sum of v).
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> V;
int b, N, p;
vector<int> GAM, E1;
struct Res { bool ok; V C; int c; int v; int pp; };
// one step; returns false if flip fails
static bool cstep(const V& C, int c, int t, V& Cn, int& cn, int& vtr, int& ptr, int& Wmaxout) {
    int m = C.size();
    int e1 = E1[t], gam = GAM[t];
    int k = c >= b ? 1 : 0;
    // ascending digits with carry-in e1
    static int da[64], dd[64];
    int a = e1;
    for (int i = 0; i < m; i++) { int s = C[i] + a; da[i] = s % b; a = s / b; }
    int e2 = a;
    int d = k;
    for (int i = m - 1; i >= 0; i--) { int s = C[i] + d; dd[i] = s % b; d = s / b; }
    int e3 = d;
    if (e1 + e3 != 1) return false;
    int z = (c + e2) % b, y = (c + k) % b;
    int w = (N + e3) % b;
    static int Cp[70];
    int n;
    if (gam == 0) {
        for (int i = 0; i < m; i++) Cp[i] = da[i] + dd[i];
        Cp[m] = z + y; n = m + 1;
    } else {
        if (m == 0) { Cp[0] = z + w; n = 1; }
        else {
            Cp[0] = da[0] + w;
            for (int i = 1; i < m; i++) Cp[i] = da[i] + dd[i - 1];
            Cp[m] = z + dd[m - 1]; n = m + 1;
        }
    }
    cn = 2 * y;
    int lo = 0, hi = n; vtr = 0; ptr = 0;
    while (lo < hi && Cp[lo] == N) { lo++; vtr++; }
    while (hi > lo && Cp[hi - 1] == cn) { hi--; ptr++; }
    Cn.assign(Cp + lo, Cp + hi);
    return true;
}
int main(int argc, char** argv) {
    b = atoi(argv[1]); N = b - 1; int W = atoi(argv[2]);
    string g = argv[3], e = argv[4]; p = g.size();
    for (char ch : g) GAM.push_back(ch - '0');
    for (char ch : e) E1.push_back(ch - '0');
    vector<int> loopv; for (int i = 5; i < argc; i++) loopv.push_back(atoi(argv[i]));
    int S = 0; for (int x : GAM) S += x;
    long long nstates = 0, ncycles = 0;
    long long maxsurv = 0;
    // enumerate C of width w in [0..W], entries 0..2b-2, canonical: C[0]!=N, C.back()!=c (depends on c; check per loop value)
    int R = 2 * b - 1;
    for (int w = 0; w <= W; w++) {
        V C(w, 0);
        while (true) {
            bool canon = (w == 0) || (C[0] != N);
            if (canon) {
                for (int c0 : loopv) {
                    if (w > 0 && C[w - 1] == c0) continue;
                    for (int ph = 0; ph < p; ph++) {
                        nstates++;
                        // simulate until death, width>W, or repeat (Brent-like with map)
                        V cur = C; int c = c0; int t = ph;
                        // history of (state) to detect cycle: up to limit steps
                        map<tuple<V,int,int>, int> seen;
                        int steps = 0; long long sumv = 0; vector<int> vs;
                        while (true) {
                            auto key = make_tuple(cur, c, t);
                            auto it = seen.find(key);
                            if (it != seen.end()) {
                                int start = it->second; long long A = 0, Sg = 0, T = steps - start;
                                for (int j = start; j < steps; j++) { A += vs[j]; Sg += GAM[(ph + j) % p]; }
                                ncycles++;
                                printf("CYCLE w=%d C0=", w);
                                for (int x : C) printf("%d,", x);
                                printf(" c0=%d ph=%d T=%lld A=%lld Sgam=%lld  %s\n", c0, ph, T, A, Sg, (Sg - 2 * A >= 0) ? "HYBRID-OK" : "h-shrinks");
                                break;
                            }
                            seen[key] = steps;
                            V nx; int cn, vt, pt;
                            if (!cstep(cur, c, t, nx, cn, vt, pt, steps)) break;
                            vs.push_back(vt);
                            steps++;
                            if ((int)nx.size() > W) break;
                            cur = nx; c = cn; t = (t + 1) % p;
                            if (steps > 400) break;
                        }
                        if (steps > maxsurv) maxsurv = steps;
                    }
                }
            }
            // next C
            int i = 0;
            while (i < w) { if (++C[i] < R) break; C[i] = 0; i++; }
            if (i == w) break;
        }
        fprintf(stderr, "w=%d done: states so far %lld cycles %lld max steps survived %lld\n", w, nstates, ncycles, maxsurv);
    }
    printf("DONE b=%d W=%d states=%lld cycles=%lld\n", b, W, nstates, ncycles);
}
