// solve.h : per-stream decision of "is a uniform absorbing band reachable from the start state" (position automaton).
#pragma once
#include "bwd_common.h"
#include <iostream>
struct Loops { vector<vector<int>> v; };
static Loops make_loops() {
  Loops R; vector<int> nxt(2 * b - 1, -1);
  for (int k = 0; k <= 2 * b - 2; k++) if (k != b - 1) { int c = k >= b; int d = (k + c) % b; nxt[k] = 2 * d; }
  vector<int> st(2 * b - 1, 0);
  for (int k = 0; k <= 2 * b - 2; k++) { if (k == b - 1 || st[k]) continue; vector<int> path; int x = k; while (x != b - 1 && x >= 0 && st[x] == 0) { st[x] = 1; path.push_back(x); x = nxt[x]; } if (x != b - 1 && x >= 0 && st[x] == 1) { vector<int> cyc; int y = x; do { cyc.push_back(y); y = nxt[y]; } while (y != x); R.v.push_back(cyc); } for (int q : path) st[q] = 2; }
  return R;
}
struct SolveRes { int targets = 0, hits = 0, undecided = 0, fwddec = 0, bwddec = 0; bool startdead = false; bool fclosed = false; size_t fstates = 0, maxcone = 0; int maxdepth = 0; string hitlines, undeclines; };
static vector<int> colsOf(const Key& a, const Key& bb, bool first) { u64 L, H; int Y[64]; unpack(a, L, H, Y); vector<int> xf; bool got = false; transitions(L, H, Y, first, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { if (got) return; if (pack(L2, H2, Y2) == bb) { got = true; xf.assign(xs, xs + p); } }); return xf; }
// requires globals b,p,ydig set; sets g,Gidx,ng from gm (bit t = g[t])
static SolveRes solve_stream(u64 gm, const Loops& loops, size_t F1CAP, size_t BCAP, bool verbose) {
  SolveRes R;
  g.assign(p, 0); Gidx.clear(); for (int t = 0; t < p; t++) { g[t] = (gm >> t) & 1; if (g[t]) Gidx.push_back(t); } ng = Gidx.size();
  string gs; for (int t = 0; t < p; t++) gs += char('0' + g[t]);
  u64 Hst = 0; for (int t = 0; t < p; t++) Hst |= (u64)g[t] << t; int Y0[64]; for (int i = 0; i < ng; i++) Y0[i] = 1;
  Key startK = pack(0, Hst, Y0);
  vector<Key> startSucc; transitions(0, Hst, Y0, true, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { startSucc.push_back(pack(L2, H2, Y2)); });
  if (startSucc.empty()) { R.startdead = true; return R; }
  unordered_map<Key, int, KH> fid; vector<Key> fkeys; bool fcap = false;
  fid[startK] = 0; fkeys.push_back(startK);
  for (size_t i = 0; i < fkeys.size() && !fcap; i++) {
    u64 L, H; int Y[64]; unpack(fkeys[i], L, H, Y);
    transitions(L, H, Y, i == 0, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { Key k = pack(L2, H2, Y2); if (fid.count(k)) return; if (fkeys.size() >= F1CAP) { fcap = true; return; } fid[k] = fkeys.size(); fkeys.push_back(k); });
  }
  R.fclosed = !fcap; R.fstates = fkeys.size();
  for (auto& lp : loops.v) {
    int ell = lp.size(); if (p % ell) continue;
    for (int ph = 0; ph < ell; ph++) {
      int u[64]; u64 Ls = 0, Hs = 0; int Yt[64];
      for (int t = 0; t < p; t++) { u[t] = lp[(t + ph) % ell]; int c = u[t] >= b; Ls |= (u64)c << t; Hs |= (u64)c << t; }
      for (int i = 0; i < ng; i++) { int t = Gidx[i]; Yt[i] = (u[t] + ((Hs >> t) & 1)) % b; }
      Key target = pack(Ls, Hs, Yt);
      R.targets++;
      if (R.fclosed) { if (fid.count(target)) { R.hits++; R.hitlines += "HITFWD p=" + to_string(p) + " g=" + gs + " loop0=" + to_string(lp[0]) + " ph=" + to_string(ph) + "\n"; } else R.fwddec++; continue; }
      unordered_map<Key, int, KH> seen; vector<Key> keys; vector<int> child; seen[target] = 0; keys.push_back(target); child.push_back(-1);
      size_t fb = 0, fe = 1; int d = 0; bool hit = false, capped = false; int hitStart = -1;
      while (fb < fe && !hit && !capped) {
        d++;
        for (size_t i2 = fb; i2 < fe && !capped; i2++) {
          u64 L, H; int Y[64]; Key ki = keys[i2]; unpack(ki, L, H, Y);
          preds(L, H, Y, [&](u64 L1, u64 H1, int* Y1) { Key kk = pack(L1, H1, Y1); if (seen.count(kk)) return; if (keys.size() >= BCAP) { capped = true; return; } seen[kk] = keys.size(); keys.push_back(kk); child.push_back((int)i2); });
        }
        for (size_t si = 0; si < startSucc.size() && hitStart < 0; si++) { auto it = seen.find(startSucc[si]); if (it != seen.end()) hitStart = it->second; }
        if (hitStart >= 0) hit = true;
        fb = fe; fe = keys.size();
      }
      R.maxdepth = max(R.maxdepth, d); R.maxcone = max(R.maxcone, keys.size());
      if (verbose) printf("TARGET p=%d g=%s loop0=%d ph=%d %s cone=%zu depth=%d\n", p, gs.c_str(), lp[0], ph, hit ? "HIT" : (capped ? "CAPPED" : "CLOSED"), keys.size(), d);
      if (hit) {
        R.hits++;
        vector<Key> chain; { int v = hitStart; while (v != -1) { chain.push_back(keys[v]); v = child[v]; } }
        string path; vector<int> x0 = colsOf(startK, chain[0], true); path += "["; for (int t = 0; t < p; t++) { path += to_string(x0[t]); if (t + 1 < p) path += ","; } path += "]";
        for (size_t i2 = 0; i2 + 1 < chain.size(); i2++) { vector<int> xf = colsOf(chain[i2], chain[i2 + 1], false); path += "["; for (int t = 0; t < p; t++) { path += to_string(xf[t]); if (t + 1 < p) path += ","; } path += "]"; }
        string cyc = "["; for (int t = 0; t < p; t++) { cyc += to_string(u[t]); if (t + 1 < p) cyc += ","; } cyc += "]";
        R.hitlines += "SCC p=" + to_string(p) + " g=" + gs + " size=1 cyclen=1 depth=" + to_string(chain.size()) + " path=" + path + " cyc=" + cyc + " loop0=" + to_string(lp[0]) + " ph=" + to_string(ph) + "\n";
      } else if (capped) { R.undecided++; R.undeclines += "UNDECIDED p=" + to_string(p) + " g=" + gs + " loop0=" + to_string(lp[0]) + " ph=" + to_string(ph) + " bcone>=" + to_string(keys.size()) + " bdepth=" + to_string(d) + " fwd>=" + to_string(R.fstates) + "\n"; }
      else R.bwddec++;
    }
  }
  return R;
}
