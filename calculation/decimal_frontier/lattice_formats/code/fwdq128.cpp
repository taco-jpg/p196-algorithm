// fwdq: forward BFS of the position automaton for a word with rotation symmetry (period q divides p), on the quotient by Z_{p/q}.
// 64-bit keys (2p + ydig*ng <= 64).  Prints level profile; optional membership test for target states (dump file) at the end.
// usage: fwdq b g q [-cap N] [-sec S] [-dump file]
#include "bwd_common.h"
#include <fstream>
#include <sstream>
typedef unsigned __int128 K64;
static int qrot, gq;   // symmetry rotation by qrot time steps ; gq = number of gam times in qrot steps
static inline K64 pk(u64 L, u64 H, const int* Y) { K64 k = (K64)L | ((K64)H << p); int sh = 2 * p; for (int i = 0; i < ng; i++) { k |= (K64)Y[i] << sh; sh += ydig; } return k; }
static inline void upk(K64 k, u64& L, u64& H, int* Y) { u64 m = (1ULL << p) - 1; L = (u64)k & m; H = (u64)(k >> p) & m; int sh = 2 * p; for (int i = 0; i < ng; i++) { Y[i] = (int)((k >> sh) & ((1u << ydig) - 1)); sh += ydig; } }
static inline u64 rotbits(u64 v, int s) { s %= p; if (!s) return v; return ((v << s) | (v >> (p - s))) & ((1ULL << p) - 1); }
static K64 canon(K64 k) {
  u64 L, H; int Y[64], Y2[64]; upk(k, L, H, Y); K64 best = k;
  for (int j = 1; j < p / qrot; j++) {
    int s = j * qrot; u64 L2 = rotbits(L, s), H2 = rotbits(H, s);
    // new time t' = t+s ; gam index of t' ; Y2[idx(t')] = Y[idx(t)]
    int sg = 0; for (int t = 0; t < s; t++) sg += g[t];   // gam times before s
    // gam times in order: Gidx; rotating by s maps gam index i -> (i + (ng - sg)) % ng  when s steps shift forward (word has period qrot so g rotation-invariant)
    for (int i = 0; i < ng; i++) Y2[(i + sg) % ng] = Y[i];
    K64 c = pk(L2, H2, Y2); if (c < best) best = c;
  }
  return best;
}
int main(int argc, char** argv) {
  b = atoi(argv[1]); string gs = argv[2]; qrot = atoi(argv[3]); p = gs.size(); size_t CAP = 3000000; double SEC = 1e18; string dump;
  for (int i = 4; i < argc; i++) { string a = argv[i]; if (a == "-cap") CAP = strtoull(argv[++i], 0, 10); else if (a == "-sec") SEC = atof(argv[++i]); else if (a == "-dump") dump = argv[++i]; }
  ydig = 1; while ((1 << ydig) < b) ydig++;
  g.assign(p, 0); Gidx.clear(); for (int t = 0; t < p; t++) { g[t] = gs[t] == '1'; if (g[t]) Gidx.push_back(t); } ng = Gidx.size();
  for (int t = 0; t < p; t++) if (g[t] != g[(t + qrot) % p]) { printf("word not %d-periodic\n", qrot); return 1; }
  if (2 * p + ydig * ng > 128) { printf("key too long\n"); return 1; }
  u64 Hst = 0; for (int t = 0; t < p; t++) Hst |= (u64)g[t] << t; int Y0[64]; for (int i = 0; i < ng; i++) Y0[i] = 1;
  K64 start = canon(pk(0, Hst, Y0));
  auto T0 = chrono::steady_clock::now(); auto el = [&]() { return chrono::duration<double>(chrono::steady_clock::now() - T0).count(); };
  vector<K64> keys; keys.reserve(CAP); size_t tsz = 1; while (tsz < CAP * 2) tsz <<= 1; vector<uint32_t> tab(tsz, 0xFFFFFFFFu); uint64_t mask = tsz - 1;
  auto hh = [&](K64 k) { uint64_t a = (uint64_t)k, c = (uint64_t)(k >> 64); uint64_t h = a * 0x9E3779B97F4A7C15ULL ^ (c + 0x7F4A7C15ULL) * 0xC2B2AE3D27D4EB4FULL; h ^= h >> 31; h *= 0x94D049BB133111EBULL; h ^= h >> 29; return h & mask; };
  auto findk = [&](K64 k) -> int { uint64_t h = hh(k); while (true) { uint32_t v = tab[h]; if (v == 0xFFFFFFFFu) return -1; if (keys[v] == k) return v; h = (h + 1) & mask; } };
  auto addk = [&](K64 k) { uint64_t h = hh(k); while (tab[h] != 0xFFFFFFFFu) h = (h + 1) & mask; tab[h] = keys.size(); keys.push_back(k); };
  addk(start); size_t fb = 0, fe = 1; int lev = 0; bool capped = false;
  while (fb < fe && !capped && el() < SEC) {
    lev++; size_t s0 = fb, s1 = fe; fb = fe;
    for (size_t i = s0; i < s1 && !capped; i++) {
      u64 L, H; int Y[64]; upk(keys[i], L, H, Y);
      transitions(L, H, Y, i == 0, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { if (capped) return; K64 k = canon(pk(L2, H2, Y2)); if (findk(k) >= 0) return; if (keys.size() >= CAP) { capped = true; return; } addk(k); });
    }
    fe = keys.size();
    printf("level %d new=%zu total=%zu t=%.0fs%s\n", lev, fe - fb, keys.size(), el(), capped ? " CAPPED" : ""); fflush(stdout);
  }
  printf("%s total=%zu levels=%d\n", (fb >= fe && !capped) ? "CLOSED" : "NOT-CLOSED", keys.size(), lev);
  if (!dump.empty() && fb >= fe && !capped) {
    ifstream f(dump); string line; int nlat = 0, reach = 0;
    while (getline(f, line)) if (line.rfind("LAT", 0) == 0) { int m; size_t ns; sscanf(line.c_str(), "LAT %d %zu", &m, &ns); bool any = false; for (int k = 0; k < m; k++) { getline(f, line); istringstream is(line); unsigned long long Lq, Hq; is >> Lq >> Hq; int Y[64]; for (int i = 0; i < ng; i++) is >> Y[i]; if (findk(canon(pk(Lq, Hq, Y))) >= 0) any = true; } getline(f, line); nlat++; if (any) { reach++; printf("LATTICE REACHABLE (index %d)\n", nlat - 1); } }
    printf("lattices=%d reachable=%d\n", nlat, reach);
  }
}
