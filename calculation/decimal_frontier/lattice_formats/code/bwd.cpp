#include "bwd_common.h"
int main(int argc, char** argv) {
  b = atoi(argv[1]); p = atoi(argv[2]); string gs = argv[3]; int phase = atoi(argv[4]); int ua = atoi(argv[5]), ub = atoi(argv[6]); // u values: "low" ua at phase-even times, ub otherwise
  unsigned long long CAP = 5000000ULL; int maxd = 200;
  for (int i = 7; i < argc; i++) { string a = argv[i]; if (a == "-cap") CAP = strtoull(argv[++i], 0, 10); else if (a == "-maxd") maxd = atoi(argv[++i]); }
  ydig = 1; while ((1 << ydig) < b) ydig++;
  g.assign(p, 0); Gidx.clear(); for (int t = 0; t < p; t++) { g[t] = gs[t] == '1'; if (g[t]) Gidx.push_back(t); } ng = Gidx.size();
  // uniform state: column u_t = ua if (t+phase)%2==0 else ub ; L=H=[u>=b]; Y=(u+hn)%b
  u64 Ls = 0, Hs = 0; int Yt[64]; int u[64];
  for (int t = 0; t < p; t++) { u[t] = ((t + phase) % 2 == 0) ? ua : ub; int c = u[t] >= b; Ls |= (u64)c << t; Hs |= (u64)c << t; }
  for (int i = 0; i < ng; i++) { int t = Gidx[i]; Yt[i] = (u[t] + ((Hs >> t) & 1)) % b; }
  Key target = pack(Ls, Hs, Yt);
  // check self-loop via forward transitions
  { bool self = false; transitions(Ls, Hs, Yt, false, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { if (pack(L2, H2, Y2) == target) self = true; }); printf("uniform self-loop: %d\n", (int)self); if (!self) return 1; }
  u64 Hst = 0; for (int t = 0; t < p; t++) Hst |= (u64)g[t] << t; int Y0[64]; for (int i = 0; i < ng; i++) Y0[i] = 1;
  Key start = pack(0, Hst, Y0);
  // successors of start (first=true)
  unordered_map<Key, int, KH> seen; seen[target] = 0; vector<Key> frontier{target};
  vector<Key> startSucc; transitions(0, Hst, Y0, true, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { startSucc.push_back(pack(L2, H2, Y2)); });
  printf("start successors: %zu\n", startSucc.size());
  for (int d = 1; d <= maxd; d++) {
    vector<Key> nxt;
    bool capped = false;
    for (auto& k : frontier) {
      u64 L, H; int Y[64]; unpack(k, L, H, Y);
      auto em = [&](u64 L1, u64 H1, int* Y1) { Key kk = pack(L1, H1, Y1); if (seen.count(kk)) return; if (seen.size() >= CAP) { capped = true; return; } seen[kk] = d; nxt.push_back(kk); };
      preds(L, H, Y, em);
      if (capped) break;
    }
    bool hit = false; for (auto& s : startSucc) if (seen.count(s)) hit = true;
    printf("depth %d new=%zu total=%zu startHit=%d%s\n", d, nxt.size(), seen.size(), (int)hit, capped ? " CAPPED" : ""); fflush(stdout);
    if (hit || capped || nxt.empty()) break;
    frontier.swap(nxt);
  }
}
