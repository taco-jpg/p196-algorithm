// runs.cpp BASE SEEDSPEC T [ratio] -- longest constant runs of the half pair word along a long orbit vs the first-order Markov expectation.
// SEEDSPEC: n<decimal>  or  r<len>:<seed>.   Output per checkpoint: t n m | for v in {0,b-1,2b-2,any}: real maxrun / Markov-1 expected maxrun
#include <bits/stdc++.h>
using namespace std;
typedef vector<uint8_t> V;
static int b;
static void step(V& d, vector<int>& P, int& gam) {
  int n = d.size(); P.resize(n);
  for (int i = 0; i < n; i++) P[i] = d[i] + d[n - 1 - i];
  int c = 0; for (int i = 0; i < n; i++) { int v = P[i] + c; if (v >= b) { d[i] = v - b; c = 1; } else { d[i] = v; c = 0; } }
  gam = c; if (c) d.push_back(1);
}
static bool ispal(const V& d) { int n = d.size(); for (int i = 0; i < n / 2; i++) if (d[i] != d[n - 1 - i]) return false; return true; }
int main(int argc, char** argv) {
  b = atoi(argv[1]); string sp = argv[2]; int T = atoi(argv[3]); double ratio = argc > 4 ? atof(argv[4]) : 1.5;
  V d;
  if (sp[0] == 'n') { vector<int> dd; for (char c : sp.substr(1)) dd.push_back(c - '0'); while (!dd.empty()) { int rem = 0; vector<int> q; for (int x : dd) { int cur = rem * 10 + x; int qq = cur / b; rem = cur % b; if (!q.empty() || qq) q.push_back(qq); } d.push_back(rem); dd = q; } }
  else { int L = atoi(sp.substr(1, sp.find(':') - 1).c_str()); unsigned long long sd = atoll(sp.substr(sp.find(':') + 1).c_str()); mt19937_64 rng(sd * 7919ULL + b); d.assign(L, 0); for (int i = 0; i < L; i++) d[i] = rng() % b; if (d[L - 1] == 0) d[L - 1] = 1; }
  vector<int> P; int gam; double nextcp = 100;
  for (int t = 0; t <= T; t++) {
    if (ispal(d)) { printf("palindrome at t=%d\n", t); break; }
    bool cp = (t >= nextcp) || t == T;
    int n = d.size();
    if (cp) { nextcp = max(nextcp * ratio, nextcp + 1);
      int m = (n + 1) / 2; vector<int> H(m); for (int i = 0; i < m; i++) H[i] = d[i] + d[n - 1 - i];
      int K = 2 * b - 1; vector<double> cnt(K, 0); vector<vector<double>> tr(K, vector<double>(K, 0));
      for (int i = 0; i < m; i++) { cnt[H[i]]++; if (i + 1 < m) tr[H[i]][H[i + 1]]++; }
      printf("t=%d n=%d m=%d |", t, n, m);
      vector<int> vs = {0, b - 1, 2 * b - 2};
      for (int v : vs) { int best = 0, cur = 0; for (int i = 0; i < m; i++) { if (H[i] == v) { cur++; best = max(best, cur); } else cur = 0; }
        double pi = cnt[v] / m, pvv = 0; double row = 0; for (int w = 0; w < K; w++) row += tr[v][w]; if (row > 0) pvv = tr[v][v] / row;
        double ex = (pvv > 0 && pvv < 1 && pi > 0) ? 1 + log(max(1e-9, m * pi * (1 - pvv))) / log(1 / pvv) : 1; if (ex < 1) ex = 1;
        printf(" v%d: %d/%.1f", v, best, ex); }
      // any constant: best over all values
      int bestany = 0; { int cur = 1; for (int i = 1; i < m; i++) { if (H[i] == H[i - 1]) { cur++; } else cur = 1; bestany = max(bestany, cur); } }
      double exany = 0; for (int v = 0; v < K; v++) { double pi = cnt[v] / m, row = 0; for (int w = 0; w < K; w++) row += tr[v][w]; double pvv = row > 0 ? tr[v][v] / row : 0; if (pvv > 0 && pvv < 1 && pi > 0) exany = max(exany, 1 + log(max(1e-9, m * pi * (1 - pvv))) / log(1 / pvv)); }
      printf(" any: %d/%.1f\n", bestany, exany); fflush(stdout);
    }
    if (t == T) break;
    step(d, P, gam);
  }
}
