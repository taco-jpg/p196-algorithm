// life.cpp -- lifetime of single-band templates (B,C) under the exact Agent120 step (mirror of neutral_band_search.py).
// usage: life BASE MODE(rand|climb) N_OR_RESTARTS SEED LBMAX LCMAX [EVALS_PER_RESTART] [MAXSTEPS]
// Words are LSB-first coefficient vectors.  step(): nextB/nextC + trim, hyp check.  Outcomes: break(t), cycle, grow, long.
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> W;
static int b;
static uint64_t rs[2];
static inline uint64_t rnd() { uint64_t s1 = rs[0], s0 = rs[1]; rs[0] = s0; s1 ^= s1 << 23; rs[1] = s1 ^ s0 ^ (s1 >> 18) ^ (s0 >> 5); return rs[1] + s0; }
static inline int rint(int n) { return (int)(rnd() % (uint64_t)n); }

static int norm(const W& w, int c, W& out) { out.resize(w.size()); for (size_t i = 0; i < w.size(); i++) { int v = w[i] + c; out[i] = v % b; c = v / b; } return c; }
struct Step { bool ok; int reason; W B2, C2; int u, v, gam; };
// reason: 1 = e1==e2==0, 2 = e1==e2==1, 3 = other hyp failure
static bool hypfail(const W& B, const W& C, int& reason) {
  for (int v : B) if (v > 2 * (b - 1)) { reason = 3; return true; }
  for (int v : C) if (v > 2 * (b - 1)) { reason = 3; return true; }
  if (!B.empty() && B[0] == 0) { reason = 3; return true; }
  return false;
}
static bool step(const W& B, const W& C, W& B2, W& C2, int& u, int& v, int& gm, int& reason) {
  if (hypfail(B, C, reason)) return false;
  static W DB, DC, DR, Br;
  int e1 = norm(B, 0, DB);
  int e2 = norm(C, e1, DC);
  if (e1 == e2) { reason = e1 ? 2 : 1; return false; }
  Br.assign(B.rbegin(), B.rend());
  int g = norm(Br, e2, DR);
  gm = g;
  size_t nb = B.size();
  if (g == 0) { B2.resize(nb); for (size_t i = 0; i < nb; i++) B2[i] = DB[i] + DR[nb - 1 - i]; }
  else { int xd = (b - 1) * (1 - e1); B2.resize(nb + 1); for (size_t i = 0; i < nb; i++) B2[i] = DB[i] + (i == 0 ? 0 : 0); 
         // nextB = zw(DB + [xd], [1] + reverse(DR)):  position i<nb: DB[i] + ([1]+rev(DR))[i]; position nb: xd + rev(DR)[nb-1]
         for (size_t i = 0; i <= nb; i++) { int a = (i < nb) ? DB[i] : xd; int c2 = (i == 0) ? 1 : DR[nb - i]; B2[i] = a + c2; } }
  size_t nc = C.size();
  if (g == 0) { C2.resize(nc); for (size_t i = 0; i < nc; i++) C2[i] = DC[i] + DC[nc - 1 - i]; }
  else { int yd = (b - 1) * (1 - e2); C2.resize(nc + 1);
         for (size_t i = 0; i <= nc; i++) { int a = (i < nc) ? DC[i] : yd; int c2 = (i == 0) ? yd : DC[nc - i]; C2[i] = a + c2; } }
  u = 0; while (!B2.empty() && B2.back() == b - 1) { B2.pop_back(); u++; }
  v = 0; { size_t lo = 0, hi = C2.size(); while (hi - lo >= 2 && C2[lo] == b - 1 && C2[hi - 1] == b - 1) { lo++; hi--; v++; }
           if (lo) { C2.erase(C2.begin(), C2.begin() + lo); C2.resize(hi - lo); } }
  return true;
}
struct Res { int kind; int t; int reason; int sumgam, gain, cyclen; };  // kind 0 break,1 cycle,2 grow,3 long
static Res run(W B, W C, int maxsteps, int maxlen = 400) {
  W B2, C2, sB, sC; int u, v, gm, reason = 0; int saved = -1; int nextsave = 1;
  Res r{3, maxsteps, 0, 0, 0, 0};
  vector<int> gams, gains;
  for (int t = 0; t < maxsteps; t++) {
    if (!step(B, C, B2, C2, u, v, gm, reason)) { r.kind = 0; r.t = t; r.reason = reason; return r; }
    gams.push_back(gm); gains.push_back(u + v);
    B.swap(B2); C.swap(C2);
    if ((int)(B.size() + C.size()) > maxlen) { r.kind = 2; r.t = t; return r; }
    if (saved >= 0 && B == sB && C == sC) { r.kind = 1; r.t = t; r.cyclen = t - saved; int sg = 0, gn = 0; for (int k = saved; k < t; k++) { sg += gams[k]; gn += gains[k]; } r.sumgam = sg; r.gain = gn; return r; }
    if (t + 1 == nextsave) { sB = B; sC = C; saved = t + 1; nextsave *= 2; }
  }
  return r;
}
static string str(const W& w) { string s = "["; for (size_t i = 0; i < w.size(); i++) { if (i) s += ","; s += to_string(w[i]); } return s + "]"; }
static int score(const Res& r, int maxsteps) { if (r.kind == 0) return r.t; return maxsteps + 1000 * (r.kind == 1); }
static W randB(int LB) { int l = 1 + rint(LB); W B(l); for (int i = 0; i < l; i++) B[i] = rint(b) + rint(b); if (B[0] == 0) B[0] = 1 + rint(2 * b - 2); return B; }
static W randC(int LC) { int l = rint(LC + 1); W C(l); for (int i = 0; i < (l + 1) / 2; i++) { int v = (i == l - 1 - i) ? 2 * rint(b) : rint(b) + rint(b); C[i] = v; C[l - 1 - i] = v; } return C; }
static void mutate(W& B, W& C, int LB, int LC) {
  int m = rint(8);
  if (m <= 2 && !B.empty()) { int i = rint(B.size()); B[i] = (rint(2) ? rint(b) + rint(b) : rint(2 * b - 1)); if (i == 0 && B[0] == 0) B[0] = 1; }
  else if (m <= 4 && !C.empty()) { int l = C.size(); int i = rint((l + 1) / 2); int v = (i == l - 1 - i) ? 2 * rint(b) : rint(2 * b - 1); if (rint(3) == 0) v = (b - 1); C[i] = v; C[l - 1 - i] = v; }
  else if (m == 5) { if ((int)B.size() < LB && rint(2)) B.push_back(rint(b) + rint(b)); else if (B.size() > 1) B.pop_back(); }
  else if (m == 6) { int l = C.size(); if (l + 2 <= LC && rint(2)) { int pos = l / 2; int v = rint(b) + rint(b); C.insert(C.begin() + pos, v); C.insert(C.begin() + pos, v); if (l % 2 == 1) {} } else if (l >= 2) { int pos = l / 2; C.erase(C.begin() + pos - 1, C.begin() + pos + (l % 2 ? 2 : 1)); } }
  else { if (!B.empty()) { int i = rint(B.size()); B[i] = (B[i] + (rint(2) ? 1 : 2 * b - 2)) % (2 * b - 1); if (i == 0 && B[0] == 0) B[0] = 1; } }
  // keep C symmetric (fix up after structural moves)
  int l = C.size(); for (int i = 0; i < l / 2; i++) C[l - 1 - i] = C[i];
}
int main(int argc, char** argv) {
  b = atoi(argv[1]); string mode = argv[2]; long N = atol(argv[3]); uint64_t seed = atoll(argv[4]);
  int LB = atoi(argv[5]), LC = atoi(argv[6]); long EV = argc > 7 ? atol(argv[7]) : 20000; int MAXS = argc > 8 ? atoi(argv[8]) : 600;
  rs[0] = seed * 0x9E3779B97F4A7C15ULL + 12345; rs[1] = seed ^ 0xD1B54A32D192ED03ULL; for (int i = 0; i < 20; i++) rnd();
  if (mode == "eval") {
    int nb, nc; while (scanf("%d", &nb) == 1) { W B(nb), C; for (int i = 0; i < nb; i++) scanf("%d", &B[i]); scanf("%d", &nc); C.resize(nc); for (int i = 0; i < nc; i++) scanf("%d", &C[i]);
      Res r = run(B, C, MAXS); printf("%d %d %d %d %d %d\n", r.kind, r.t, r.reason, r.cyclen, r.sumgam, r.gain); }
    return 0; }
  map<int, long> hist; map<int, array<long, 4>> hr; long cyc = 0, grow = 0, lng = 0;
  vector<pair<int, string>> top;
  auto record = [&](const Res& r, const W& B, const W& C) {
    if (r.kind == 0) { hist[r.t]++; hr[r.t][r.reason]++; }
    else if (r.kind == 1) cyc++; else if (r.kind == 2) grow++; else lng++;
    int sc = score(r, MAXS);
    string s = str(B) + " " + str(C) + " kind=" + to_string(r.kind) + " t=" + to_string(r.t) + " reason=" + to_string(r.reason) + " cyclen=" + to_string(r.cyclen) + " sumgam=" + to_string(r.sumgam) + " gain=" + to_string(r.gain);
    top.push_back({sc, s});
    if (top.size() > 400) { sort(top.begin(), top.end(), [](auto& a, auto& c) { return a.first > c.first; }); top.resize(100); }
  };
  if (mode == "rand") {
    for (long i = 0; i < N; i++) { W B = randB(LB), C = randC(LC); Res r = run(B, C, MAXS); record(r, B, C); }
  } else {
    for (long rs_ = 0; rs_ < N; rs_++) {
      W B = randB(LB), C = randC(LC); Res r = run(B, C, MAXS); int cur = score(r, MAXS); int best = cur; long stag = 0;
      W bB = B, bC = C; Res bR = r;
      for (long e = 0; e < EV; e++) {
        W B2 = B, C2 = C; mutate(B2, C2, LB, LC); int nm = 1 + (rint(3) == 0 ? rint(3) : 0); for (int k = 1; k < nm; k++) mutate(B2, C2, LB, LC);
        Res r2 = run(B2, C2, MAXS); int s2 = score(r2, MAXS);
        if (s2 >= cur) { if (s2 > cur) stag = 0; else stag++; B = B2; C = C2; cur = s2; r = r2; if (s2 > best) { best = s2; bB = B; bC = C; bR = r2; } }
        else stag++;
        if (stag > EV / 4) break;
        if (r2.kind >= 1) break;   // found cycle/grow/long
      }
      record(bR, bB, bC);
    }
  }
  sort(top.begin(), top.end(), [](auto& a, auto& c) { return a.first > c.first; });
  printf("# base=%d mode=%s N=%ld LB=%d LC=%d maxsteps=%d\n", b, mode.c_str(), N, LB, LC, MAXS);
  printf("# cycles=%ld grow=%ld long=%ld\n", cyc, grow, lng);
  printf("# hist t count (reason1 e1=e2=0, reason2 e1=e2=1, reason3 other)\n");
  for (auto& kv : hist) printf("H %d %ld %ld %ld %ld\n", kv.first, kv.second, hr[kv.first][1], hr[kv.first][2], hr[kv.first][3]);
  int shown = 0; set<string> seen;
  for (auto& p : top) { if (seen.count(p.second)) continue; seen.insert(p.second); printf("T %d %s\n", p.first, p.second.c_str()); if (++shown >= 40) break; }
}
