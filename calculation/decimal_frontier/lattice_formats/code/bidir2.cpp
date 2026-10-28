// bidir2: large-scale bidirectional BFS in the position automaton, compact 128-bit keys (2p + ydig*ng <= 128).
// start -> any state of the target lattices listed in a dump file (from latenum -dump).
// usage: bidir2 b g dumpfile [-cap N] [-sec S] [-maxl L]
#include "bwd_common.h"
#include <fstream>
#include <sstream>
typedef unsigned __int128 u128;
static inline u128 pack128(u64 L, u64 H, const int* Y) { u128 k = (u128)L | ((u128)H << p); int sh = 2 * p; for (int i = 0; i < ng; i++) { k |= (u128)Y[i] << sh; sh += ydig; } return k; }
static inline void unpack128(u128 k, u64& L, u64& H, int* Y) { u64 mk = p >= 64 ? ~0ULL : ((1ULL << p) - 1); L = (u64)k & mk; H = (u64)(k >> p) & mk; int sh = 2 * p; for (int i = 0; i < ng; i++) { Y[i] = (int)((k >> sh) & ((1u << ydig) - 1)); sh += ydig; } }
static inline uint64_t h128(u128 k) { uint64_t a = (uint64_t)k, c = (uint64_t)(k >> 64); uint64_t h = a * 0x9E3779B97F4A7C15ULL ^ (c + 0x7F4A7C15ULL) * 0xC2B2AE3D27D4EB4FULL; h ^= h >> 31; h *= 0x94D049BB133111EBULL; h ^= h >> 29; return h; }
struct Side {
  vector<u128> keys; vector<uint32_t> par; vector<uint32_t> tab; uint64_t mask; size_t cap;
  Side(size_t cap_) : cap(cap_) { uint64_t sz = 1; while (sz < cap * 2) sz <<= 1; tab.assign(sz, 0xFFFFFFFFu); mask = sz - 1; keys.reserve(cap); par.reserve(cap); }
  int find(u128 k) const { uint64_t h = h128(k) & mask; while (true) { uint32_t v = tab[h]; if (v == 0xFFFFFFFFu) return -1; if (keys[v] == k) return v; h = (h + 1) & mask; } }
  int add(u128 k, uint32_t pr) { uint64_t h = h128(k) & mask; while (tab[h] != 0xFFFFFFFFu) h = (h + 1) & mask; uint32_t id = keys.size(); keys.push_back(k); par.push_back(pr); tab[h] = id; return id; }
  bool full() const { return keys.size() >= cap; }
};
int main(int argc, char** argv) {
  b = atoi(argv[1]); string gs = argv[2]; string dump = argv[3]; p = gs.size();
  size_t CAP = 20000000; double SEC = 1e18; int maxl = 100000;
  for (int i = 4; i < argc; i++) { string a = argv[i]; if (a == "-cap") CAP = strtoull(argv[++i], 0, 10); else if (a == "-sec") SEC = atof(argv[++i]); else if (a == "-maxl") maxl = atoi(argv[++i]); }
  ydig = 1; while ((1 << ydig) < b) ydig++;
  g.assign(p, 0); Gidx.clear(); for (int t = 0; t < p; t++) { g[t] = gs[t] == '1'; if (g[t]) Gidx.push_back(t); } ng = Gidx.size();
  if (2 * p + ydig * ng > 128) { printf("key too long (%d bits)\n", 2 * p + ydig * ng); return 1; }
  auto T0 = chrono::steady_clock::now(); auto el = [&]() { return chrono::duration<double>(chrono::steady_clock::now() - T0).count(); };
  // read targets
  vector<u128> tkeys; vector<int> tlat, tpos; vector<vector<int>> latRows; vector<int> latM;
  { ifstream f(dump); string line; while (getline(f, line)) { if (line.rfind("LAT", 0) == 0) { int m; size_t ns; sscanf(line.c_str(), "LAT %d %zu", &m, &ns); int li = latM.size(); latM.push_back(m); for (int k = 0; k < m; k++) { getline(f, line); istringstream is(line); unsigned long long L, H; is >> L >> H; int Y[64]; for (int i = 0; i < ng; i++) is >> Y[i]; tkeys.push_back(pack128(L, H, Y)); tlat.push_back(li); tpos.push_back(k); } getline(f, line); istringstream is2(line); string tag; is2 >> tag; vector<int> rr; int v; while (is2 >> v) rr.push_back(v); latRows.push_back(rr); } } }
  printf("targets: %zu states from %zu lattices\n", tkeys.size(), latM.size()); fflush(stdout);
  u64 Hst = 0; for (int t = 0; t < p; t++) Hst |= (u64)g[t] << t; int Y0[64]; for (int i = 0; i < ng; i++) Y0[i] = 1;
  u128 start = pack128(0, Hst, Y0);
  Side F(CAP), B(CAP);
  F.add(start, 0xFFFFFFFFu);
  for (u128 k : tkeys) if (B.find(k) < 0) B.add(k, 0xFFFFFFFFu);
  size_t ff = 0, fe = 1, bf = 0, be = B.keys.size(); int fl = 0, bl = 0; int meetF = -1, meetB = -1; bool fdone = false, bdone = false;
  while (meetF < 0 && fl + bl < maxl && el() < SEC) {
    if (fe == ff) fdone = true; if (be == bf) bdone = true;
    if (F.full()) fdone = true; if (B.full()) bdone = true;
    if (fdone && bdone) break;
    bool fwd = !fdone && (bdone || (fe - ff) <= (be - bf));
    if (fwd) {
      fl++; size_t s0 = ff, s1 = fe; ff = fe;
      for (size_t i = s0; i < s1 && meetF < 0 && !F.full(); i++) {
        u64 L, H; int Y[64]; unpack128(F.keys[i], L, H, Y);
        transitions(L, H, Y, i == 0, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { if (meetF >= 0 || F.full()) return; u128 k = pack128(L2, H2, Y2); if (F.find(k) >= 0) return; int id = F.add(k, (uint32_t)i); int j = B.find(k); if (j >= 0) { meetF = id; meetB = j; } });
      }
      fe = F.keys.size();
    } else {
      bl++; size_t s0 = bf, s1 = be; bf = be;
      for (size_t i = s0; i < s1 && meetF < 0 && !B.full(); i++) {
        u64 L, H; int Y[64]; unpack128(B.keys[i], L, H, Y);
        preds(L, H, Y, [&](u64 L1, u64 H1, int* Y1) { if (meetF >= 0 || B.full()) return; u128 k = pack128(L1, H1, Y1); if (B.find(k) >= 0) return; int id = B.add(k, (uint32_t)i); int j = F.find(k); if (j >= 0) { meetF = j; meetB = id; } });
      }
      be = B.keys.size();
    }
    if ((fl + bl) % 2 == 0 || meetF >= 0) { printf("t=%.0fs fl=%d bl=%d F=%zu B=%zu%s\n", el(), fl, bl, F.keys.size(), B.keys.size(), meetF >= 0 ? " MEET" : ""); fflush(stdout); }
  }
  if (meetF < 0) { printf("NO MEET fl=%d bl=%d F=%zu B=%zu fdone=%d bdone=%d fclosed=%d bclosed=%d t=%.0fs\n", fl, bl, F.keys.size(), B.keys.size(), (int)fdone, (int)bdone, (int)(fe == ff), (int)(be == bf), el()); return 2; }
  // path
  vector<u128> chain; { vector<u128> tmp; uint32_t v = meetF; while (v != 0xFFFFFFFFu) { tmp.push_back(F.keys[v]); v = F.par[v]; } reverse(tmp.begin(), tmp.end()); chain = tmp; }
  uint32_t v = B.par[meetB]; uint32_t last = meetB; while (v != 0xFFFFFFFFu) { chain.push_back(B.keys[v]); last = v; v = B.par[v]; }
  // 'last' is a root target state index in B (par == none); find which lattice/pos
  u128 root = B.keys[last]; int li = -1, lp = -1; for (size_t q = 0; q < tkeys.size(); q++) if (tkeys[q] == root) { li = tlat[q]; lp = tpos[q]; break; }
  auto colsOf = [&](u128 a, u128 bb, bool first) { u64 L, H; int Y[64]; unpack128(a, L, H, Y); vector<int> xf; bool got = false; transitions(L, H, Y, first, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { if (got) return; if (pack128(L2, H2, Y2) == bb) { got = true; xf.assign(xs, xs + p); } }); return xf; };
  string path;
  for (size_t i = 0; i + 1 < chain.size(); i++) { vector<int> xf = colsOf(chain[i], chain[i + 1], i == 0); if (xf.empty()) { printf("ERROR no edge at %zu\n", i); return 3; } path += "["; for (int t = 0; t < p; t++) { path += to_string(xf[t]); if (t + 1 < p) path += ","; } path += "]"; }
  int m = latM[li]; string cyc;
  for (int k = 0; k < m; k++) { int pos = (lp + k) % m; cyc += "["; for (int t = 0; t < p; t++) { cyc += to_string(latRows[li][t * m + pos]); if (t + 1 < p) cyc += ","; } cyc += "]"; }
  printf("SCC p=%d g=%s size=%d cyclen=%d depth=%zu path=%s cyc=%s\n", p, gs.c_str(), m, m, chain.size() - 1, path.c_str(), cyc.c_str());
}
