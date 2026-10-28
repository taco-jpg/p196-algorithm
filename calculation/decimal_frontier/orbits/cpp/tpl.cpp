// tpl.cpp -- clean template-lifetime tool.  Exact C++ mirror of neutral_band_search.py (norm, step incl. hyp, trim).
// usage:
//   tpl eval  BASE MAXSTEPS < file   (lines: nB B... nC C...)   -> prints "kind t reason cyclen sumgam gain" per line (kind 0 break,1 cycle,2 grow,3 long)
//   tpl rand  BASE N SEED LB LC [MAXSTEPS]       random templates (B random 1..LB cells, C symmetric 0..LC cells; cells = sum of two digits)
//   tpl climb BASE RESTARTS SEED LB LC EVALS [MAXSTEPS]   hill climbing on lifetime
// All words LSB first, entries 0..2(b-1).  Output: lifetime histogram (with break reasons) + best templates.
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> W;
static int b;
static uint64_t rs[2];
static inline uint64_t rnd() { uint64_t s1 = rs[0], s0 = rs[1]; rs[0] = s0; s1 ^= s1 << 23; rs[1] = s1 ^ s0 ^ (s1 >> 18) ^ (s0 >> 5); return rs[1] + s0; }
static inline int rn(int n) { return (int)(rnd() % (uint64_t)n); }

static int normw(const W& w, int c, W& out) { out.resize(w.size()); for (size_t i = 0; i < w.size(); i++) { int v = w[i] + c; out[i] = v % b; c = v / b; } return c; }
// reason: 1 e1==e2==0, 2 e1==e2==1, 3 other hyp failure (coefficient bound / leading zero)
static bool stepf(const W& B, const W& C, W& B2, W& C2, int& u, int& v, int& gm, int& reason) {
  for (int x : B) if (x > 2 * (b - 1)) { reason = 3; return false; }
  for (int x : C) if (x > 2 * (b - 1)) { reason = 3; return false; }
  if (!B.empty() && B[0] == 0) { reason = 3; return false; }
  static W DB, DC, DR, Br;
  int e1 = normw(B, 0, DB);
  int e2 = normw(C, e1, DC);
  if (e1 == e2) { reason = e1 ? 2 : 1; return false; }
  Br.assign(B.rbegin(), B.rend());
  gm = normw(Br, e2, DR);
  size_t nb = B.size(), nc = C.size();
  if (gm == 0) {
    B2.resize(nb); for (size_t i = 0; i < nb; i++) B2[i] = DB[i] + DR[nb - 1 - i];
    C2.resize(nc); for (size_t i = 0; i < nc; i++) C2[i] = DC[i] + DC[nc - 1 - i];
  } else {
    int xd = (b - 1) * (1 - e1), yd = (b - 1) * (1 - e2);
    B2.resize(nb + 1); for (size_t i = 0; i <= nb; i++) { int a = (i < nb) ? DB[i] : xd; int c2 = (i == 0) ? 1 : DR[nb - i]; B2[i] = a + c2; }
    C2.resize(nc + 1); for (size_t i = 0; i <= nc; i++) { int a = (i < nc) ? DC[i] : yd; int c2 = (i == 0) ? yd : DC[nc - i]; C2[i] = a + c2; }
  }
  u = 0; while (!B2.empty() && B2.back() == b - 1) { B2.pop_back(); u++; }
  v = 0; { size_t lo = 0, hi = C2.size(); while (hi - lo >= 2 && C2[lo] == b - 1 && C2[hi - 1] == b - 1) { lo++; hi--; v++; }
           if (lo) { C2.erase(C2.begin(), C2.begin() + lo); C2.resize(hi - lo); } }
  return true;
}
struct Res { int kind = 3; int t = 0; int reason = 0; int cyclen = 0, sumgam = 0, gain = 0; W cB, cC; };
static string key(const W& B, const W& C) { string s; for (int x : B) s.push_back((char)x); s.push_back((char)127); for (int x : C) s.push_back((char)x); return s; }
static Res run(W B, W C, int maxsteps, int maxlen = 400) {
  Res r; W B2, C2; int u, v, gm, reason = 0;
  unordered_map<string, int> seen; vector<int> gams, gains;
  for (int t = 0; t < maxsteps; t++) {
    string k = key(B, C);
    auto it = seen.find(k);
    if (it != seen.end()) { r.kind = 1; r.t = t; r.cyclen = t - it->second; int sg = 0, gn = 0; for (int j = it->second; j < t; j++) { sg += gams[j]; gn += gains[j]; } r.sumgam = sg; r.gain = gn; r.cB = B; r.cC = C; return r; }
    seen[k] = t;
    if (!stepf(B, C, B2, C2, u, v, gm, reason)) { r.kind = 0; r.t = t; r.reason = reason; return r; }
    gams.push_back(gm); gains.push_back(u + v);
    B.swap(B2); C.swap(C2);
    if ((int)(B.size() + C.size()) > maxlen) { r.kind = 2; r.t = t; return r; }
  }
  r.kind = 3; r.t = maxsteps; return r;
}
static string str(const W& w) { string s = "["; for (size_t i = 0; i < w.size(); i++) { if (i) s += ","; s += to_string(w[i]); } return s + "]"; }

// genome: B (cells), half H of C, odd flag + middle (digit)
struct G { W B, H; int odd = 0; int mid = 0; };
static int cell() { return rn(b) + rn(b); }
static W buildC(const G& g) { W C = g.H; if (g.odd) C.push_back(2 * g.mid); for (int i = (int)g.H.size() - 1; i >= 0; i--) C.push_back(g.H[i]); return C; }
static G randG(int LB, int LC) {
  G g; int lb = 1 + rn(LB); g.B.resize(lb); for (auto& x : g.B) x = cell(); if (g.B[0] == 0) g.B[0] = 1 + rn(2 * b - 2);
  int lc = rn(LC + 1); g.odd = lc & 1; g.H.resize(lc / 2); for (auto& x : g.H) x = cell(); g.mid = rn(b); return g;
}
static void mutate(G& g, int LB, int LC) {
  int m = rn(10);
  if (m <= 2) { int i = rn(g.B.size()); g.B[i] = rn(2) ? cell() : rn(2 * b - 1); if (i == 0 && g.B[0] == 0) g.B[0] = 1; }
  else if (m <= 4 && !g.H.empty()) { int i = rn(g.H.size()); g.H[i] = rn(2) ? cell() : rn(2 * b - 1); }
  else if (m == 5) { if ((int)g.B.size() < LB && rn(2)) g.B.push_back(cell()); else if (g.B.size() > 1) g.B.pop_back(); }
  else if (m == 6) { int lc = 2 * g.H.size() + g.odd; if (rn(2) && lc + 2 <= LC) g.H.push_back(cell()); else if (!g.H.empty()) g.H.pop_back(); }
  else if (m == 7) { if (LC >= 1) { int lc = 2 * g.H.size() + g.odd; if (g.odd) { g.odd = 0; } else if (lc + 1 <= LC) g.odd = 1; g.mid = rn(b); } }
  else if (m == 8) { int i = rn(g.B.size()); g.B[i] = (g.B[i] + (rn(2) ? 1 : 2 * b - 2)) % (2 * b - 1); if (i == 0 && g.B[0] == 0) g.B[0] = 1; }
  else { if (!g.H.empty()) { int i = rn(g.H.size()); g.H[i] = (g.H[i] + (rn(2) ? 1 : 2 * b - 2)) % (2 * b - 1); } else g.mid = rn(b); }
}
static int score(const Res& r, int maxsteps) { if (r.kind == 0) return r.t; return maxsteps + 1000 * (r.kind == 1 ? 1 : 0); }

int main(int argc, char** argv) {
  string mode = argv[1]; b = atoi(argv[2]);
  if (mode == "eval") {
    int maxs = atoi(argv[3]); int maxlen = argc > 4 ? atoi(argv[4]) : 400; int nb, nc;
    while (scanf("%d", &nb) == 1) { W B(nb), C; for (int i = 0; i < nb; i++) if (scanf("%d", &B[i]) != 1) return 1; if (scanf("%d", &nc) != 1) return 1; C.resize(nc); for (int i = 0; i < nc; i++) if (scanf("%d", &C[i]) != 1) return 1;
      Res r = run(B, C, maxs, maxlen); printf("%d %d %d %d %d %d\n", r.kind, r.t, r.reason, r.cyclen, r.sumgam, r.gain); }
    return 0;
  }
  long N = atol(argv[3]); uint64_t seed = atoll(argv[4]); int LB = atoi(argv[5]), LC = atoi(argv[6]);
  rs[0] = seed * 0x9E3779B97F4A7C15ULL + 12345; rs[1] = seed ^ 0xD1B54A32D192ED03ULL; for (int i = 0; i < 20; i++) rnd();
  long EV = 0; int MAXS = 400;
  if (mode == "rand") { if (argc > 7) MAXS = atoi(argv[7]); }
  else { EV = atol(argv[7]); if (argc > 8) MAXS = atoi(argv[8]); }
  map<int, array<long, 4>> hist; long ncyc = 0, ngrow = 0, nlong = 0, ncert = 0;
  vector<pair<int, string>> top;
  auto record = [&](const Res& r, const G& g) {
    if (r.kind == 0) { hist[r.t][0]++; hist[r.t][r.reason]++; }
    else if (r.kind == 1) { ncyc++; if (r.sumgam <= r.gain) ncert++; } else if (r.kind == 2) ngrow++; else nlong++;
    int sc = score(r, MAXS);
    string s = "B=" + str(g.B) + " C=" + str(buildC(g)) + " kind=" + to_string(r.kind) + " t=" + to_string(r.t) + " reason=" + to_string(r.reason);
    if (r.kind == 1) s += " cyclen=" + to_string(r.cyclen) + " sumgam=" + to_string(r.sumgam) + " gain=" + to_string(r.gain) + " cycB=" + str(r.cB) + " cycC=" + str(r.cC);
    top.push_back({sc, s});
    if (top.size() > 600) { sort(top.begin(), top.end(), [](auto& a, auto& c) { return a.first > c.first; }); top.resize(150); }
  };
  if (mode == "rand") {
    for (long i = 0; i < N; i++) { G g = randG(LB, LC); Res r = run(g.B, buildC(g), MAXS); record(r, g); }
  } else {
    for (long rr = 0; rr < N; rr++) {
      G g = randG(LB, LC); Res r = run(g.B, buildC(g), MAXS); int cur = score(r, MAXS); G bestg = g; Res bestr = r; int best = cur; long stag = 0;
      for (long e = 0; e < EV; e++) {
        G g2 = g; mutate(g2, LB, LC); if (rn(3) == 0) mutate(g2, LB, LC);
        Res r2 = run(g2.B, buildC(g2), MAXS); int s2 = score(r2, MAXS);
        if (s2 >= cur) { stag = (s2 > cur) ? 0 : stag + 1; g = g2; cur = s2; if (s2 > best) { best = s2; bestg = g2; bestr = r2; } } else stag++;
        if (stag > EV / 3) break;
        if (r2.kind >= 1) break;
      }
      record(bestr, bestg);
    }
  }
  sort(top.begin(), top.end(), [](auto& a, auto& c) { return a.first > c.first; });
  printf("# base=%d mode=%s N=%ld LB=%d LC=%d maxsteps=%d EV=%ld\n", b, mode.c_str(), N, LB, LC, MAXS, EV);
  printf("# cycles=%ld (certificates %ld) grow=%ld long=%ld\n", ncyc, ncert, ngrow, nlong);
  printf("# H t count r1(e1=e2=0) r2(e1=e2=1) r3(other)\n");
  for (auto& kv : hist) printf("H %d %ld %ld %ld %ld\n", kv.first, kv.second[0], kv.second[1], kv.second[2], kv.second[3]);
  int shown = 0; set<string> seen;
  for (auto& p : top) { if (seen.count(p.second)) continue; seen.insert(p.second); printf("T %d %s\n", p.first, p.second.c_str()); if (++shown >= 25) break; }
}
