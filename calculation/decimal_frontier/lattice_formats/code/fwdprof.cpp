#include "bwd_common.h"
int main(int argc, char** argv) {
  b = atoi(argv[1]); p = atoi(argv[2]); string gs = argv[3]; unsigned long long CAP = atoll(argv[4]);
  ydig = 1; while ((1 << ydig) < b) ydig++;
  g.assign(p, 0); Gidx.clear(); for (int t = 0; t < p; t++) { g[t] = gs[t] == '1'; if (g[t]) Gidx.push_back(t); } ng = Gidx.size();
  u64 Hst = 0; for (int t = 0; t < p; t++) Hst |= (u64)g[t] << t; int Y0[64]; for (int i = 0; i < ng; i++) Y0[i] = 1;
  Key start = pack(0, Hst, Y0);
  unordered_map<Key, int, KH> id; vector<Key> keys; vector<int> lev; id[start] = 0; keys.push_back(start); lev.push_back(0);
  vector<long> cnt(1, 1); bool capped = false;
  for (size_t i = 0; i < keys.size() && !capped; i++) {
    u64 L, H; int Y[64]; unpack(keys[i], L, H, Y);
    transitions(L, H, Y, i == 0, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { Key k = pack(L2, H2, Y2); if (id.count(k)) return; if (keys.size() >= CAP) { capped = true; return; } id[k] = keys.size(); keys.push_back(k); int l = lev[i] + 1; lev.push_back(l); if ((int)cnt.size() <= l) cnt.push_back(0); cnt[l]++; });
  }
  printf("fwd b=%d p=%d g=%s S=%d states=%zu capped=%d prof:", b, p, gs.c_str(), ng, keys.size(), (int)capped); for (size_t l = 0; l < cnt.size(); l++) printf(" %ld", cnt[l]); printf("\n");
}
