// bidir: bidirectional (meet-in-the-middle) search start -> uniform band state S*(loop,phase) in the position automaton.
// usage: bidir b p g loopIndexOrValue phase [-cap N] [-maxl L]   (loop given by its first element value l0 as printed by bwdcensus)
#include "bwd_common.h"
int main(int argc, char** argv) {
  b = atoi(argv[1]); p = atoi(argv[2]); string gs = argv[3]; int l0 = atoi(argv[4]); int ph = atoi(argv[5]);
  size_t CAP = 6000000; int maxl = 400;
  for (int i = 6; i < argc; i++) { string a = argv[i]; if (a == "-cap") CAP = strtoull(argv[++i], 0, 10); else if (a == "-maxl") maxl = atoi(argv[++i]); }
  ydig = 1; while ((1 << ydig) < b) ydig++;
  g.assign(p, 0); Gidx.clear(); for (int t = 0; t < p; t++) { g[t] = gs[t] == '1'; if (g[t]) Gidx.push_back(t); } ng = Gidx.size();
  vector<int> nxt(2 * b - 1, -1); for (int k = 0; k <= 2 * b - 2; k++) if (k != b - 1) { int c = k >= b; nxt[k] = 2 * ((k + c) % b); }
  vector<int> lp; { int x = l0; do { lp.push_back(x); x = nxt[x]; } while (x != l0 && lp.size() < 100); }
  int ell = lp.size(); if (p % ell) { printf("loop length %d does not divide p\n", ell); return 1; }
  int u[64]; u64 Ls = 0, Hs = 0; int Yt[64];
  for (int t = 0; t < p; t++) { u[t] = lp[(t + ph) % ell]; int c = u[t] >= b; Ls |= (u64)c << t; Hs |= (u64)c << t; }
  for (int i = 0; i < ng; i++) { int t = Gidx[i]; Yt[i] = (u[t] + ((Hs >> t) & 1)) % b; }
  Key target = pack(Ls, Hs, Yt);
  u64 Hst = 0; for (int t = 0; t < p; t++) Hst |= (u64)g[t] << t; int Y0[64]; for (int i = 0; i < ng; i++) Y0[i] = 1;
  Key start = pack(0, Hst, Y0);
  // forward structures
  unordered_map<Key, int, KH> fid, bid; vector<Key> fk, bk; vector<int> fpar, bchild;
  fid[start] = 0; fk.push_back(start); fpar.push_back(-1);
  bid[target] = 0; bk.push_back(target); bchild.push_back(-1);
  size_t ff = 0, fe = 1, bf = 0, be = 1; int fl = 0, bl = 0; int meetF = -1, meetB = -1;
  // check trivial: start==target no
  while (meetF < 0 && (fl + bl) < maxl) {
    bool fwdSide = (fe - ff) <= (be - bf);
    if (fe == ff && be == bf) break;
    if ((fwdSide && fe == ff)) fwdSide = false; if ((!fwdSide && be == bf)) fwdSide = true;
    if (fwdSide) {
      fl++; size_t s0 = ff, s1 = fe; ff = fe;
      for (size_t i = s0; i < s1 && meetF < 0; i++) {
        u64 L, H; int Y[64]; unpack(fk[i], L, H, Y);
        transitions(L, H, Y, i == 0, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { if (meetF >= 0) return; Key k = pack(L2, H2, Y2); if (fid.count(k)) return; if (fk.size() >= CAP) return; int id = fk.size(); fid[k] = id; fk.push_back(k); fpar.push_back((int)i); auto it = bid.find(k); if (it != bid.end()) { meetF = id; meetB = it->second; } });
      }
      fe = fk.size();
    } else {
      bl++; size_t s0 = bf, s1 = be; bf = be;
      for (size_t i = s0; i < s1 && meetF < 0; i++) {
        u64 L, H; int Y[64]; unpack(bk[i], L, H, Y);
        preds(L, H, Y, [&](u64 L1, u64 H1, int* Y1) { if (meetF >= 0) return; Key k = pack(L1, H1, Y1); if (bid.count(k)) return; if (bk.size() >= CAP) return; int id = bk.size(); bid[k] = id; bk.push_back(k); bchild.push_back((int)i); auto it = fid.find(k); if (it != fid.end()) { meetF = it->second; meetB = id; } });
      }
      be = bk.size();
    }
    if (((fl + bl) % 4) == 0 || meetF >= 0) { printf("fl=%d bl=%d F=%zu B=%zu%s\n", fl, bl, fk.size(), bk.size(), meetF >= 0 ? " MEET" : ""); fflush(stdout); }
    if (fk.size() >= CAP && bk.size() >= CAP) { printf("both capped\n"); break; }
  }
  if (meetF < 0) { printf("NO MEET fl=%d bl=%d F=%zu B=%zu fclosed=%d bclosed=%d\n", fl, bl, fk.size(), bk.size(), (int)(fe == ff), (int)(be == bf)); return 2; }
  // path: start -> ... -> fk[meetF] ; fk[meetF] == bk[meetB] -> bchild chain -> target
  vector<Key> chain; { int v = meetF; vector<Key> tmp; while (v != -1) { tmp.push_back(fk[v]); v = fpar[v]; } reverse(tmp.begin(), tmp.end()); chain = tmp; }
  { int v = bchild[meetB]; while (v != -1) { chain.push_back(bk[v]); v = bchild[v]; } }
  auto colsOf = [&](const Key& a, const Key& bb, bool first) { u64 L, H; int Y[64]; unpack(a, L, H, Y); vector<int> xf; bool got = false; transitions(L, H, Y, first, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { if (got) return; if (pack(L2, H2, Y2) == bb) { got = true; xf.assign(xs, xs + p); } }); return xf; };
  string path;
  for (size_t i = 0; i + 1 < chain.size(); i++) { vector<int> xf = colsOf(chain[i], chain[i + 1], i == 0); if (xf.empty()) { printf("ERROR no edge at %zu\n", i); return 3; } path += "["; for (int t = 0; t < p; t++) { path += to_string(xf[t]); if (t + 1 < p) path += ","; } path += "]"; }
  string cyc = "["; for (int t = 0; t < p; t++) { cyc += to_string(u[t]); if (t + 1 < p) cyc += ","; } cyc += "]";
  printf("SCC p=%d g=%s size=1 cyclen=1 depth=%zu path=%s cyc=%s loop0=%d ph=%d\n", p, gs.c_str(), chain.size() - 1, path.c_str(), cyc.c_str(), l0, ph);
}
