// W7: exhaustive survival profile of centre-windows of width w (all 19^w initial windows, pruned DFS, bottom-up).
// usage: surv lat.txt w olo ohi Hleaf [Hin]
// For every initial window (at t=0, n = 400+o) simulate the exact window dynamics until the non-lattice region exceeds w
// (lifetime = steps survived) or up to Hleaf steps; periodic windows (state repeats at a multiple of 80 steps) reported.
#include "win.h"
#include <map>
#include <unordered_set>
typedef unsigned long long u64;
Lat L; int w, K, M = 12, Hleaf, Hin; long n0; int olo, ohi, o; int t0 = 0; bool dump = false;
long long nodes = 0, leaves = 0, cycles = 0; long long lifehist[2000]; int maxlife = 0;
vector<long long> lvl;
int cells[64];
int bestcells[64];
static u64 hashwin(const int* P, int t) { u64 h = 1469598103934665603ULL ^ (u64)t; for (int i = K - w; i < K; i++) { h ^= (u64)(P[i] + 1); h *= 1099511628211ULL; } return h; }

// ternary prefix simulation; returns false if pruned
bool sim_prefix(int j) {
  int P[130], Pn[130]; int fz = K - w;
  for (int i = 0; i < fz; i++) P[i] = L.cell(t0, (n0 + 1) / 2 - K + i);
  for (int i = 0; i < w; i++) P[fz + i] = (i < j) ? cells[i] : X;
  long n = n0; int t = t0;
  for (int s = 0; s < Hin; s++) {
    int dh; if (win_step(L, P, t, n, K, w, Pn, &dh)) return false;
    memcpy(P, Pn, sizeof(int) * K); n += L.gam[t % L.p]; t = (t + 1) % L.p;
    if (P[fz] == X) break;
  }
  return true;
}
// full simulation; returns lifetime
int sim_full(bool& cyc) {
  int P[130], Pn[130]; int fz = K - w;
  for (int i = 0; i < fz; i++) P[i] = L.cell(t0, (n0 + 1) / 2 - K + i);
  for (int i = 0; i < w; i++) P[fz + i] = cells[i];
  long n = n0; int t = t0; cyc = false;
  unordered_set<u64> seen;
  for (int s = 0; s < Hleaf; s++) {
    if (s % 80 == 0) { u64 h = hashwin(P, t); if (!seen.insert(h).second) { cyc = true; return s; } }
    int dh; if (win_step(L, P, t, n, K, w, Pn, &dh)) return s;
    memcpy(P, Pn, sizeof(int) * K); n += L.gam[t % L.p]; t = (t + 1) % L.p;
  }
  return Hleaf;
}
void dfs(int j) {
  nodes++; lvl[j]++;
  if (j == w) {
    // odd n: middle cell (top cell) must be even
    leaves++;
    bool cyc; int life = sim_full(cyc);
    lifehist[life < 1999 ? life : 1999]++;
    if (life > maxlife) { maxlife = life; memcpy(bestcells, cells, sizeof(int) * w); }
    if (dump) { printf("LEAF t0=%d o=%d life=%d cells:", t0, o, life); for (int i = 0; i < w; i++) printf(" %d", cells[i]); printf("\n"); }
    if (cyc) { cycles++; printf("CYCLE o=%d cells:", o); for (int i = 0; i < w; i++) printf(" %d", cells[i]); printf("\n"); fflush(stdout); }
    return;
  }
  for (int d = 0; d <= 18; d++) {
    if (j == w - 1 && (n0 & 1) && (d & 1)) continue;
    cells[j] = d;
    if (!sim_prefix(j + 1)) continue;
    dfs(j + 1);
  }
}
int main(int argc, char** argv) {
  if (!L.load(argv[1])) { fprintf(stderr, "load fail\n"); return 1; }
  w = atoi(argv[2]); olo = atoi(argv[3]); ohi = atoi(argv[4]); Hleaf = atoi(argv[5]); Hin = argc > 6 ? atoi(argv[6]) : 4 * w + 20; if (argc > 7) t0 = atoi(argv[7]); if (argc > 8) dump = atoi(argv[8]);
  K = w + M; lvl.assign(w + 2, 0);
  for (o = olo; o < ohi; o++) {
    n0 = 400 + o;
    long long n_before = nodes, l_before = leaves;
    memset(lifehist, 0, sizeof(lifehist)); maxlife = 0;
    dfs(0);
    printf("w=%d o=%d nodes=%lld leaves=%lld maxlife=%d best:", w, o, nodes - n_before, leaves - l_before, maxlife);
    for (int i = 0; i < w; i++) printf(" %d", bestcells[i]);
    printf("\n  lifetime counts (>=): ");
    long long cum = 0; vector<long long> ge(2001, 0);
    for (int s = 1999; s >= 0; s--) { cum += lifehist[s]; ge[s] = cum; }
    int marks[] = {1, 2, 4, 8, 12, 16, 24, 32, 40, 48, 64, 80, 96, 128, 160, 240, 320, 400};
    for (int mk : marks) if (mk <= Hleaf) printf("%d:%lld ", mk, ge[mk]);
    printf("\n"); fflush(stdout);
  }
  printf("TOTAL w=%d nodes=%lld leaves=%lld cycles=%lld levels:", w, nodes, leaves, cycles);
  for (int j = 0; j <= w; j++) printf(" %lld", lvl[j]); printf("\n");
}
