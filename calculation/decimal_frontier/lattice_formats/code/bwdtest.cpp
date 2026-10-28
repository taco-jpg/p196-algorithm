#include "bwd_common.h"
#include <random>
// differential test: forward edges S->T must be found by preds(T); preds(T) must all be forward-valid.
int main(int argc, char** argv) {
  b = atoi(argv[1]); p = atoi(argv[2]); string gs = argv[3]; int nsamp = atoi(argv[4]); unsigned long long CAP = 200000;
  ydig = 1; while ((1 << ydig) < b) ydig++;
  g.assign(p, 0); Gidx.clear(); for (int t = 0; t < p; t++) { g[t] = gs[t] == '1'; if (g[t]) Gidx.push_back(t); } ng = Gidx.size();
  u64 Hst = 0; for (int t = 0; t < p; t++) Hst |= (u64)g[t] << t; int Y0[64]; for (int i = 0; i < ng; i++) Y0[i] = 1;
  Key start = pack(0, Hst, Y0);
  unordered_map<Key, int, KH> id; vector<Key> keys; id[start] = 0; keys.push_back(start);
  for (size_t i = 0; i < keys.size() && keys.size() < CAP; i++) {
    u64 L, H; int Y[64]; unpack(keys[i], L, H, Y);
    transitions(L, H, Y, i == 0, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { Key k = pack(L2, H2, Y2); if (!id.count(k) && keys.size() < CAP) { id[k] = keys.size(); keys.push_back(k); } });
  }
  printf("forward states %zu\n", keys.size());
  mt19937_64 rng(12345); long edges = 0, missing = 0, bad = 0, predtotal = 0;
  for (int s = 1; s < nsamp; s++) {
    size_t i = 1 + rng() % (keys.size() - 1);
    u64 L, H; int Y[64]; unpack(keys[i], L, H, Y);
    set<Key, bool(*)(const Key&, const Key&)> succ([](const Key& a, const Key& b2) { return memcmp(a.w, b2.w, sizeof a.w) < 0; });
    transitions(L, H, Y, false, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { succ.insert(pack(L2, H2, Y2)); });
    for (auto& T : succ) {
      edges++;
      u64 L2, H2; int Y2[64]; unpack(T, L2, H2, Y2); bool found = false; long np = 0;
      preds(L2, H2, Y2, [&](u64 L1, u64 H1, int* Y1) { np++; if (pack(L1, H1, Y1) == keys[i]) found = true;
         // soundness: T in succ(pred)
         bool ok = false; transitions(L1, H1, Y1, false, [&](u64 La, u64 Ha, int* Ya, int* xs, int* hn) { if (pack(La, Ha, Ya) == T) ok = true; }); if (!ok) bad++; });
      predtotal += np; if (!found) missing++;
    }
  }
  printf("edges=%ld missing=%ld unsound=%ld avg_preds=%.2f\n", edges, missing, bad, edges ? (double)predtotal / edges : 0.0);
}
