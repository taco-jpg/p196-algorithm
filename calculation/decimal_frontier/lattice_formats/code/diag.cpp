#include "bwd_common.h"
// Death diagnosis: BFS from start; for every state with no successor, classify, over all x0, the failure of the DFS chain:
//  reach[t] = number of x0-chains alive at time t; types: Hfail (no c with floor((x+c)/b)==H_t), closure (chain complete, x_p != x_0).
int main(int argc, char** argv) {
  b = atoi(argv[1]); p = atoi(argv[2]); string gs = argv[3]; unsigned long long CAP = 300000;
  ydig = 1; while ((1 << ydig) < b) ydig++;
  g.assign(p, 0); Gidx.clear(); for (int t = 0; t < p; t++) { g[t] = gs[t] == '1'; if (g[t]) Gidx.push_back(t); } ng = Gidx.size();
  u64 Hst = 0; for (int t = 0; t < p; t++) Hst |= (u64)g[t] << t; int Y0[64]; for (int i = 0; i < ng; i++) Y0[i] = 1;
  Key start = pack(0, Hst, Y0);
  unordered_map<Key, int, KH> id; vector<Key> keys; vector<int> lev; id[start] = 0; keys.push_back(start); lev.push_back(0);
  vector<char> hasSucc;
  int yi[64]; { int c = 0; for (int t = 0; t < p; t++) yi[t] = g[t] ? c++ : -1; }
  long hf = 0, cf = 0, comp = 0, chains = 0; vector<long> hfT(p, 0); vector<long> alive(p + 1, 0); long dead = 0, deadlev[64] = {0};
  for (size_t i = 0; i < keys.size() && keys.size() < CAP; i++) {
    u64 L, H; int Y[64]; unpack(keys[i], L, H, Y);
    int nsucc = 0;
    transitions(L, H, Y, i == 0, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { nsucc++; Key k = pack(L2, H2, Y2); if (!id.count(k) && keys.size() < CAP) { id[k] = keys.size(); keys.push_back(k); lev.push_back(lev[i] + 1); } });
    if (nsucc == 0) {
      dead++; deadlev[min(lev[i], 63)]++;
      // diagnose chains
      for (int x0 = (i == 0 ? 1 : 0); x0 <= 2 * b - 2; x0++) {
        // explore all c-branches
        struct Fr { int t, x; };
        vector<Fr> st; st.push_back({0, x0});
        while (!st.empty()) {
          Fr f = st.back(); st.pop_back(); alive[f.t]++;
          if (f.t == p) { if (f.x != x0) cf++; else comp++; continue; }
          bool any = false;
          for (int c = 0; c < 2; c++) {
            if ((f.x + c) / b != (int)((H >> f.t) & 1)) continue; any = true;
            int nx = (f.x + (int)((L >> f.t) & 1)) % b + (g[f.t] ? Y[yi[f.t]] : (f.x + c) % b);
            st.push_back({f.t + 1, nx});
          }
          if (!any) { hf++; hfT[f.t]++; }
        }
      }
    }
  }
  printf("b=%d p=%d g=%s states=%zu dead=%ld  chains: Hfail=%ld closureFail=%ld  deadByLevel:", b, p, gs.c_str(), keys.size(), dead, hf, cf);
  for (int l = 0; l < 20; l++) if (deadlev[l]) printf(" L%d:%ld", l, deadlev[l]); printf("\n  Hfail by t:"); for (int t = 0; t < p; t++) printf(" %ld", hfT[t]); printf("\n");
}
