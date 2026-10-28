// bauto5: exact position-automaton census of periodic-lattice exterior cycles (any base b <= 32, p <= 60).
// Same transition system as bauto3 (validated against the repo's bauto for neutral bands), but
//  * 192-bit state keys,
//  * streams generated from the exact regular language of the position-0 counter (small DFA, backward-pruned),
//  * for each nontrivial SCC the globally shortest cycle length (if <= S = #ones) is reported (SCCMIN) for the self-mirror lattice test.
// usage: bauto5 b pmin pmax [-cap N] [-maxscc k] [-g stream] [-dens4] [-v]
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <array>
#include <string>
#include <map>
#include <set>
#include <unordered_map>
#include <algorithm>
#include <chrono>
using namespace std;
typedef uint64_t u64;
struct Key {
  u64 w[5];
  Key() { for (int i = 0; i < 5; i++) w[i] = 0; }
  bool operator==(const Key& o) const { for (int i = 0; i < 5; i++) if (w[i] != o.w[i]) return false; return true; }
};
static inline void kput(Key& k, int pos, int nb, u64 v) { for (int i = 0; i < nb; i++) { int q = pos + i; if ((v >> i) & 1) k.w[q >> 6] |= 1ULL << (q & 63); } }
static inline u64 kget(const Key& k, int pos, int nb) { u64 v = 0; for (int i = 0; i < nb; i++) { int q = pos + i; v |= ((k.w[q >> 6] >> (q & 63)) & 1ULL) << i; } return v; }
struct KH { size_t operator()(const Key& k) const { u64 h = 0x9E3779B97F4A7C15ULL; for (int i = 0; i < 5; i++) { h ^= k.w[i] + 0x9E3779B97F4A7C15ULL + (h << 6) + (h >> 2); h *= 0xC2B2AE3D27D4EB4FULL; } return (size_t)(h ^ (h >> 31)); } };
int b, p, ydig, ng;
vector<int> g, Gidx;
static inline u64 mask_p() { return p >= 64 ? ~0ULL : ((1ULL << p) - 1); }
static inline Key pack(u64 L, u64 H, const int* Y) { Key k; kput(k, 0, p, L); kput(k, p, p, H); int sh = 2 * p; for (int i = 0; i < ng; i++) { kput(k, sh, ydig, (u64)Y[i]); sh += ydig; } return k; }
static inline void unpack(const Key& k, u64& L, u64& H, int* Y) { L = kget(k, 0, p); H = kget(k, p, p); int sh = 2 * p; for (int i = 0; i < ng; i++) { Y[i] = (int)kget(k, sh, ydig); sh += ydig; } }

template <class F> void transitions(u64 L, u64 H, const int* Y, bool first, F emit) {
  int yi[64]; { int c = 0; for (int t = 0; t < p; t++) yi[t] = g[t] ? c++ : -1; }
  for (int x0 = (first ? 1 : 0); x0 <= 2 * b - 2; x0++) {
    int xs[64]; int hn[64];
    struct Fr { int t; int x; int ch; };
    vector<Fr> st; st.push_back({0, x0, 0}); xs[0] = x0;
    while (!st.empty()) {
      Fr& f = st.back();
      if (f.t == p) {
        if (f.x == x0) {
          u64 L2 = 0, H2 = 0; int Y2[64];
          for (int t = 0; t < p; t++) { L2 |= (u64)((xs[t] + ((L >> t) & 1)) / b) << t; H2 |= (u64)hn[t] << t; }
          for (int i = 0; i < ng; i++) { int t = Gidx[i]; Y2[i] = (xs[t] + hn[t]) % b; }
          emit(L2, H2, Y2, xs, hn);
        }
        st.pop_back(); continue;
      }
      if (f.ch >= 2) { st.pop_back(); continue; }
      int c = f.ch++; int t = f.t, x = f.x;
      if (first && x == 0) continue;
      if ((x + c) / b != (int)((H >> t) & 1)) continue;
      int nx = (x + (int)((L >> t) & 1)) % b + (g[t] ? Y[yi[t]] : (x + c) % b);
      xs[t] = x; hn[t] = c;
      if (t + 1 < p) { xs[t + 1] = nx; st.push_back({t + 1, nx, 0}); }
      else {
        if (nx == x0) {
          u64 L2 = 0, H2 = 0; int Y2[64];
          for (int tt = 0; tt < p; tt++) { L2 |= (u64)((xs[tt] + ((L >> tt) & 1)) / b) << tt; H2 |= (u64)hn[tt] << tt; }
          for (int i = 0; i < ng; i++) { int tt = Gidx[i]; Y2[i] = (xs[tt] + hn[tt]) % b; }
          emit(L2, H2, Y2, xs, hn);
        }
      }
    }
  }
}


// ---------------- backward co-reachability from uniform band state ----------------
// preds(T): all states (L,H,Y) with a column x such that transition -> T.
template <class F> void preds(u64 L2, u64 H2, const int* Y2, F emit) {
  int yi[64]; { int c = 0; for (int t = 0; t < p; t++) yi[t] = g[t] ? c++ : -1; }
  int xs[64], Ls[64], Ys[64];
  // recursive lambda via explicit std::function-free recursion
  struct Rec {
    u64 L2, H2; const int* Y2; int* xs; int* Ls; int* Ys; int* yi; F* emit; int x0;
    void go(int t) {
      int x = xs[t];
      int hn = (H2 >> t) & 1, l2 = (L2 >> t) & 1;
      for (int Lt = 0; Lt < 2; Lt++) {
        if ((x + Lt) / b != l2) continue;
        if (g[t] && (x + hn) % b != Y2[yi[t]]) continue;
        Ls[t] = Lt;
        int base = (x + Lt) % b;
        if (!g[t]) {
          int nx = base + (x + hn) % b; Ys[t] = -1;
          if (t + 1 == p) { if (nx == x0) fin(); } else { xs[t + 1] = nx; go(t + 1); }
        } else {
          for (int y = 0; y < b; y++) {
            int nx = base + y; Ys[t] = y;
            if (t + 1 == p) { if (nx == x0) fin(); } else { if (nx > 2 * b - 2) continue; xs[t + 1] = nx; go(t + 1); }
          }
        }
      }
    }
    void fin() {
      u64 L = 0, H = 0; int Y[64];
      for (int t = 0; t < p; t++) { L |= (u64)Ls[t] << t; int hn = (H2 >> t) & 1; H |= (u64)((xs[t] + hn) / b) << t; }
      for (int i = 0; i < ng; i++) Y[i] = Ys[Gidx[i]];
      (*emit)(L, H, Y);
    }
  };
  Rec r{L2, H2, Y2, xs, Ls, Ys, yi, nullptr, 0};
  F* ep = &emit; r.emit = ep;
  for (int x0 = 0; x0 <= 2 * b - 2; x0++) { r.x0 = x0; xs[0] = x0; r.go(0); }
}

