// lock.cpp -- "exterior lock" statistics of long reverse-and-add orbits.
// For each step t record the lowest W cells of the (symmetric) pair word and gam.  For K=1..KM and period p=1..PM find the longest run of
// consecutive steps t with  P_i(t) == P_i(t-p) for i<K  (bottom K cells time-periodic with period p), plus the number of runs >= 20/50/100.
// Same analysis on a row-shuffled copy gives the null.  usage: lock BASE SEEDLEN SEED T [KM=8] [PM=12]   (seed digits random, resampled until no palindrome in 400 steps)
#include <bits/stdc++.h>
using namespace std;
typedef vector<uint8_t> V;
static int b;
static vector<uint8_t> CI;  // carry INTO cell i of the last step
static void step(V& d, vector<int>& P, int& gam) {
  int n = d.size(); P.resize(n);
  for (int i = 0; i < n; i++) P[i] = d[i] + d[n - 1 - i];
  int c = 0; CI.assign(n + 1, 0);
  for (int i = 0; i < n; i++) { CI[i] = c; int v = P[i] + c; if (v >= b) { d[i] = v - b; c = 1; } else { d[i] = v; c = 0; } }
  CI[n] = c;
  gam = c; if (c) d.push_back(1);
}
static bool ispal(const V& d) { int n = d.size(); for (int i = 0; i < n / 2; i++) if (d[i] != d[n - 1 - i]) return false; return true; }
struct Res { int L[16][33]; int n20[16][33], n50[16][33], n100[16][33]; int S[16][33]; };
static void analyse(const vector<array<int,16>>& rows, int KM, int PM, Res& R) {
  int T = rows.size();
  for (int K = 1; K <= KM; K++) for (int p = 1; p <= PM; p++) {
    int cur = 0, best = 0, a = 0, bb = 0, c = 0, bs = 0;
    for (int t = p; t < T; t++) {
      bool eq = true; for (int i = 0; i < K; i++) if (rows[t][i] != rows[t - p][i]) { eq = false; break; }
      if (eq) cur++; else { if (cur >= 20) a++; if (cur >= 50) bb++; if (cur >= 100) c++; if (cur > best) { best = cur; bs = t - cur - p; } cur = 0; }
    }
    if (cur > best) { best = cur; bs = T - cur - p; } if (cur >= 20) a++; if (cur >= 50) bb++; if (cur >= 100) c++;
    R.L[K][p] = best + p; R.S[K][p] = bs; R.n20[K][p] = a; R.n50[K][p] = bb; R.n100[K][p] = c;
  }
}
int main(int argc, char** argv) {
  b = atoi(argv[1]); string slarg = argv[2]; int SL = atoi(argv[2]); unsigned long long seed = atoll(argv[3]); int T = atoi(argv[4]);
  bool named = (slarg[0] == 'n');  // "n196": decimal integer 196 as seed
  V dseed;
  if (named) { string dec = slarg.substr(1); vector<int> dd; for (char c : dec) dd.push_back(c - '0');
    while (!dd.empty()) { int rem = 0; vector<int> q; for (int x : dd) { int cur = rem * 10 + x; int qq = cur / b; rem = cur % b; if (!q.empty() || qq) q.push_back(qq); } dseed.push_back(rem); dd = q; } SL = dseed.size(); }
  int KM = argc > 5 ? atoi(argv[5]) : 8, PM = argc > 6 ? atoi(argv[6]) : 12; if (KM > 15) KM = 15; if (PM > 32) PM = 32;
  mt19937_64 rng(seed * 1000003ULL + b);
  V d; vector<int> P; int gam;
  vector<array<int,16>> rows; rows.reserve(T); vector<int> gams; gams.reserve(T); vector<array<uint8_t,16>> fl; fl.reserve(T); vector<array<uint8_t,2>> e3; e3.reserve(T);
  if (named) d = dseed;
  else for (int attempt = 0; attempt < 1000; attempt++) {
    d.assign(SL, 0); for (int i = 0; i < SL; i++) d[i] = rng() % b; if (d[SL - 1] == 0) d[SL - 1] = 1;
    V e = d; bool pal = false; for (int t = 0; t < 400; t++) { if (ispal(e)) { pal = true; break; } step(e, P, gam); }
    if (!pal) break;
  }
  bool pal = false; int steps = 0;
  for (int t = 0; t < T; t++) {
    if (ispal(d)) { pal = true; break; }
    step(d, P, gam);   // P is the pair word of the current number
    array<int,16> r; r.fill(0); for (int i = 0; i < 16 && i < (int)P.size(); i++) r[i] = P[i];
    rows.push_back(r); gams.push_back(gam); steps++;
    { array<uint8_t,16> f; f.fill(0); int n = (int)CI.size() - 1; for (int K = 1; K <= 8 && 2 * K < n; K++) { int e1 = CI[K], e2 = CI[n - K]; f[K] = (e1 != e2); } fl.push_back(f); array<uint8_t,2> q{0,0}; if (n > 8) { q[0] = CI[3]; q[1] = CI[n - 3]; } e3.push_back(q); }
  }
  Res R, S; memset(&R, 0, sizeof R); memset(&S, 0, sizeof S);
  analyse(rows, KM, PM, R);
  vector<array<int,16>> sh = rows; shuffle(sh.begin(), sh.end(), rng); analyse(sh, KM, PM, S);
  // gam alternating stretch (p=2) and longest p-periodic stretch of gam stream for p<=PM
  int gbest[33]; for (int p = 1; p <= PM; p++) { int cur = 0, best = 0; for (int t = p; t < steps; t++) { if (gams[t] == gams[t - p]) cur++; else { best = max(best, cur); cur = 0; } } gbest[p] = max(best, cur) + p; }
  double dens = 0; for (int x : gams) dens += x; dens /= max(1, steps);
  printf("base %d seedlen %d seed %llu steps %d pal %d finaldigits %zu gamdens %.3f\n", b, SL, seed, steps, (int)pal, d.size(), dens);
  for (int K = 1; K <= KM; K++) {
    int bp = 1; for (int p = 1; p <= PM; p++) if (R.L[K][p] > R.L[K][bp]) bp = p;
    int sp = 1; for (int p = 1; p <= PM; p++) if (S.L[K][p] > S.L[K][sp]) sp = p;
    printf(" K=%d best p=%d L=%d  runs>=20/50/100 at best p: %d/%d/%d   | shuffled max L=%d\n", K, bp, R.L[K][bp], R.n20[K][bp], R.n50[K][bp], R.n100[K][bp], S.L[K][sp]);
  }
  printf(" gam stream longest p-periodic stretch (p=1..%d):", PM); for (int p = 1; p <= PM; p++) printf(" %d", gbest[p]); printf("\n");
  // full table K x p of longest locks, compact
  { // print the locked frame (first 2p rows after the start) for the best p of K=2,3,4
    for (int K = 2; K <= 4 && K <= KM; K++) { int bp = 1; for (int p = 1; p <= PM; p++) if (R.L[K][p] > R.L[K][bp]) bp = p; if (R.L[K][bp] < 20) continue;
      int st = R.S[K][bp]; printf(" frame K=%d p=%d start t=%d (low 8 cells | gam), rows t..t+%d:\n", K, bp, st, 2 * bp - 1);
      for (int r = st; r < st + 2 * bp && r < steps; r++) { printf("   "); for (int i = 0; i < 8; i++) printf("%d ", rows[r][i]); printf("| gam %d  e1(3)=%d e2(3)=%d\n", gams[r], (int)e3[r][0], (int)e3[r][1]); } } }
  { printf(" flip e1!=e2 at K bottom cells: K: frac, longest run of flips(1), longest run of non-flips(0), longest alternating-in-time (f_t = 1-f_{t-1})\n");
    for (int K = 1; K <= 8; K++) { long c1 = 0; int r1 = 0, r0 = 0, c1r = 0, c0r = 0, ra = 0, ca = 0; for (int t = 0; t < steps; t++) { int f = fl[t][K]; c1 += f; if (f) { c1r++; c0r = 0; } else { c0r++; c1r = 0; } r1 = max(r1, c1r); r0 = max(r0, c0r);
        if (t > 0 && f != fl[t - 1][K]) ca++; else ca = 0; ra = max(ra, ca); }
      printf("  K=%d frac %.3f run1 %d run0 %d alt %d\n", K, (double)c1 / max(1, steps), r1, r0, ra + 1); } }
  printf(" table L(K,p):\n"); for (int K = 1; K <= KM; K++) { printf("  K=%d:", K); for (int p = 1; p <= PM; p++) printf(" %d", R.L[K][p]); printf("\n"); }
}
