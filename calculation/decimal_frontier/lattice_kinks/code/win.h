// W7: exact window (centre-frame) update for the decimal lattice exterior.  Own implementation.
// Lower half of the palindromic pair word, buffer of K cells ending at the centre: positions h-K .. h-1, h=ceil(n/2).
// Cells i < K-w are "frozen" (must equal the lattice), cells i >= K-w are the free window (width w).
// X = -1 means unknown (ternary simulation used for pruning in DFS).
#pragma once
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <cstdint>
using namespace std;
static const int X = -1;
struct Lat {
  int p, nB, m, b; vector<int> gam; vector<vector<int>> W, cup, B;
  bool load(const char* fn) {
    FILE* f = fopen(fn, "r"); if (!f) return false;
    if (fscanf(f, "%d %d %d %d", &p, &nB, &m, &b) != 4) return false;
    gam.resize(p); for (int t = 0; t < p; t++) if (fscanf(f, "%d", &gam[t]) != 1) return false;
    W.assign(p, vector<int>(m)); cup.assign(p, vector<int>(m)); B.assign(p, vector<int>(nB));
    for (int t = 0; t < p; t++) for (int j = 0; j < m; j++) if (fscanf(f, "%d", &W[t][j]) != 1) return false;
    for (int t = 0; t < p; t++) for (int j = 0; j < m; j++) if (fscanf(f, "%d", &cup[t][j]) != 1) return false;
    for (int t = 0; t < p; t++) for (int k = 0; k < nB; k++) if (fscanf(f, "%d", &B[t][k]) != 1) { B[t][k] = 0; }
    fclose(f); return true;
  }
  inline int cell(int t, long x) const { return W[t % p][(int)((((x - nB) % m) + m) % m)]; }
  inline int cupAt(int t, long x) const { return cup[t % p][(int)((((x - nB) % m) + m) % m)]; }
  // (ascending carry INTO position x)
};

// one step on K cells.  P: K cells (positions h-K..h-1).  t: time phase (mod p), n: length (long).
// Returns: 0 ok, 1 = a KNOWN frozen cell mismatches the lattice (escape / prune).
// Pn: new buffer (positions h'-K .. h'-1); frozen cells forced to lattice (assume survival) when X.
// dh = h' - h.
static inline int win_step(const Lat& L, const int* P, int t, long n, int K, int w, int* Pn, int* dh_out, bool assume = true) {
  const int bb = 10;
  long h = (n + 1) / 2;
  int g = L.gam[t % L.p];
  bool odd = (n & 1);
  int cu[130], Oup[130], D[130], Odn[130];
  cu[0] = L.cupAt(t, h - K);
  for (int i = 0; i < K; i++) {
    int pv = P[i];
    if (pv != X && cu[i] != X) { int s = pv + cu[i]; cu[i + 1] = s >= bb; Oup[i] = s - bb * cu[i + 1]; }
    else {
      Oup[i] = X;
      if (pv == X) cu[i + 1] = X; else cu[i + 1] = (pv >= bb) ? 1 : ((pv <= bb - 2) ? 0 : X);
    }
  }
  int top;
  if (odd) { D[K - 1] = cu[K - 1]; Odn[K - 1] = Oup[K - 1]; D[K - 2] = cu[K]; top = K - 2; }
  else { D[K - 1] = cu[K]; top = K - 1; }
  if (!odd) {
    Odn[K - 1] = (P[K - 1] != X && D[K - 1] != X) ? (P[K - 1] + D[K - 1]) % bb : X;
  }
  // descending chain: D[i] = carry into mirror(i) = [P[i+1] + D[i+1] >= 10]
  for (int i = top; i >= 0; i--) {
    if (i < top) {
      int pv = P[i + 1];
      if (pv == X) D[i] = X; else if (pv >= bb) D[i] = 1; else if (pv <= bb - 2) D[i] = 0; else D[i] = D[i + 1];
    }
    Odn[i] = (P[i] != X && D[i] != X) ? (P[i] + D[i]) % bb : X;
  }
  // careful: when odd, the chain at i=top uses D[top] = cu[K] (set above), when even uses D[K-1] (set above)
  long n2 = n + g; long h2 = (n2 + 1) / 2; int dh = (int)(h2 - h); *dh_out = dh;
  int nt = (t + 1) % L.p;
  int fz = K - w;
  for (int i2 = 0; i2 < K; i2++) {
    int val;
    if (i2 < 2) { Pn[i2] = L.cell(nt, h2 - K + i2); continue; }
    int i = i2 + dh; int up, part;
    if (g == 0) { up = Oup[i]; part = (odd && i == K - 1) ? Oup[i] : Odn[i]; }
    else { up = (i <= K - 1) ? Oup[i] : Odn[K - 1]; part = Odn[i - 1]; }
    val = (up == X || part == X) ? X : up + part;
    if (i2 < fz) {
      int lv = L.cell(nt, h2 - K + i2);
      if (val != X && val != lv) return 1;
      Pn[i2] = lv;   // assume survival
    } else Pn[i2] = val;
  }
  return 0;
}
