// enumscan.cpp -- enumerate ALL seeds with exactly D base-b digits, run reverse-and-add for T steps (stop at palindrome),
// flag orbits whose half pair word contains a run of the neutral coefficient b-1 of length >= FRAC*n at both T/2 and T (growing).
// usage: enumscan BASE D T FRAC [MAXPRINT]
// Output: counts (dead / alive / flagged) and the flagged seeds as integers (base-10 value) and digit lists (MSB first).
#include <bits/stdc++.h>
using namespace std;
static int b;
typedef vector<uint8_t> V;
// one step in place: d (LSB first) -> next; returns carry (gam)
static void revadd(V& d, V& P, int& gam) {
  int n = d.size(); P.resize(n);
  for (int i = 0; i < n; i++) P[i] = d[i] + d[n - 1 - i];
  int c = 0;
  for (int i = 0; i < n; i++) { int v = P[i] + c; d[i] = v % b; c = v / b; }
  gam = c; if (c) d.push_back(1);
}
static bool ispal(const V& d) { int n = d.size(); for (int i = 0; i < n / 2; i++) if (d[i] != d[n - 1 - i]) return false; return true; }
static int maxrun9(const V& d, V& P) {
  int n = d.size(); int best = 0, cur = 0; int h = (n + 1) / 2;
  for (int i = 0; i < h; i++) { int p = d[i] + d[n - 1 - i]; if (p == b - 1) { cur++; best = max(best, cur); } else cur = 0; }
  return best;
}
int main(int argc, char** argv) {
  b = atoi(argv[1]); int D = atoi(argv[2]); int T = atoi(argv[3]); double FR = atof(argv[4]); int MAXP = argc > 5 ? atoi(argv[5]) : 20;
  long dead = 0, alive = 0, flagged = 0; long total = 1; for (int i = 0; i < D - 1; i++) total *= b; total *= (b - 1);
  V d, P; vector<string> out;
  vector<int> digs(D);
  long long lo = 1; for (int i = 0; i < D - 1; i++) lo *= b; long long hi = lo * b;
  for (long long x = lo; x < hi; x++) {
    d.clear(); long long y = x; for (int i = 0; i < D; i++) { d.push_back(y % b); y /= b; }
    int gam; bool pal = false; int r1 = -1, n1 = 0;
    for (int t = 0; t <= T; t++) {
      if (ispal(d)) { pal = true; break; }
      if (t == T / 2) { r1 = maxrun9(d, P); n1 = d.size(); }
      if (t == T) break;
      revadd(d, P, gam);
    }
    if (pal) { dead++; continue; }
    alive++;
    int n2 = d.size(); int r2 = maxrun9(d, P);
    if (n1 > 0 && r1 >= FR * n1 && r2 >= FR * n2 && r2 > r1) {
      flagged++;
      if ((int)out.size() < MAXP) { string s = to_string(x) + " (digits MSB first:"; for (int i = D - 1; i >= 0; i--) s += " " + to_string((int)((x / (long long)pow(b, i)) % b)); s += ") n(T/2)=" + to_string(n1) + " run=" + to_string(r1) + " n(T)=" + to_string(n2) + " run=" + to_string(r2); out.push_back(s); }
    }
  }
  printf("base %d D %d T %d FRAC %.2f: seeds %lld dead %ld alive %ld flagged %ld\n", b, D, T, FR, hi - lo, dead, alive, flagged);
  for (auto& s : out) printf("  %s\n", s.c_str());
}
