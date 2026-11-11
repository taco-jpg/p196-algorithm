// mc13b.cpp -- main-session independent computation of E_acc(K,T) for the period-8 lattices.
// Rule written from the mathematical definitions (depth / F_K / R_K of r12g sections 1-2);
// shares no code with kcommon.h, indep.cpp or klib.  Lattice read from a file produced from
// lattice_formats/p8_scc.txt by mklat13.py.
//
//   mc13b selftest LATFILE SEED COUNT           genuine big-number addition versus F_K and R_K
//   mc13b run LATFILE ORBIT KMAX THREADS [PRINT] E_acc(K,Lo) level by level
#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <functional>
#include <numeric>
#include <random>
#include <string>
#include <thread>
#include <vector>
using namespace std;
typedef uint8_t u8;
typedef uint32_t u32;
typedef uint64_t u64;

static int BASE, tp, nB, m, BS;
static vector<int> clk;
static vector<vector<int>> Bt, W, UP, DN, EE;
static vector<vector<array<int, 2>>> BOK, RB1;

static void die(const char *s) {
  fprintf(stderr, "FATAL %s\n", s);
  exit(3);
}
static inline int md(int a, int b) { return ((a % b) + b) % b; }

static void read_lat(const char *fn) {
  FILE *f = fopen(fn, "r");
  if (!f) die("open");
  if (fscanf(f, "%d %d %d %d", &BASE, &tp, &nB, &m) != 4) die("hdr");
  clk.resize(tp);
  for (int &x : clk)
    if (fscanf(f, "%d", &x) != 1) die("clk");
  Bt.assign(tp, vector<int>(nB));
  W.assign(tp, vector<int>(m));
  for (int t = 0; t < tp; t++)
    for (int x = 0; x < nB; x++)
      if (fscanf(f, "%d", &Bt[t][x]) != 1) die("B");
  for (int t = 0; t < tp; t++)
    for (int x = 0; x < m; x++)
      if (fscanf(f, "%d", &W[t][x]) != 1) die("W");
  fclose(f);
  BS = 2 * BASE - 1;
}

static void prep() {
  UP.assign(tp, vector<int>(m));
  DN = UP;
  EE = UP;
  for (int t = 0; t < tp; t++) {
    int res[2];
    for (int st = 0; st < 2; st++) {
      int a = st;
      for (int x = 0; x < 4 * m; x++) a = (W[t][x % m] + a >= BASE);
      res[st] = a;
    }
    if (res[0] != res[1]) die("UP not unique");
    int a = res[0];
    for (int x = 0; x < m; x++) {
      UP[t][x] = a;
      EE[t][x] = (W[t][x] + a) % BASE;
      a = (W[t][x] + a >= BASE);
    }
    if (a != res[0]) die("UP not periodic");
    // descending: b_{x-1} = [W[x] + b_x >= BASE], with b_x the carry into the mirror of column x
    for (int st = 0; st < 2; st++) {
      int b = st;
      for (int i = 0; i < 4 * m; i++) {
        int x = m - 1 - (i % m);
        b = (W[t][x] + b >= BASE);
      }
      res[st] = b;
    }
    if (res[0] != res[1]) die("DN not unique");
    int b = res[0];
    for (int x = m - 1; x >= 0; x--) {
      DN[t][x] = b;
      b = (W[t][x] + b >= BASE);
    }
    if (b != res[0]) die("DN not periodic");
  }
  // the bulk must be an exact solution with overflow clk
  for (int t = 0; t < tp; t++) {
    int g = clk[t], tn = (t + 1) % tp;
    for (int x = 0; x < m; x++) {
      int y = md(x - g, m);
      int rv = (W[t][y] + DN[t][y]) % BASE;
      if (W[tn][x] != EE[t][x] + rv) die("lattice is not a solution");
    }
  }
  // what happens below the window when the descending carry leaving the window bottom is bb
  BOK.assign(tp, vector<array<int, 2>>(m));
  RB1 = BOK;
  const int LIM = 3 * m;
  for (int t = 0; t < tp; t++) {
    int g = clk[t], tn = (t + 1) % tp;
    for (int j = 0; j < m; j++)
      for (int bb = 0; bb < 2; bb++) {
        vector<int> rr(LIM + 3);
        int b = bb;
        for (int l = 1; l <= LIM + 2; l++) {
          int col = md(j - l, m);
          int s = W[t][col] + b;
          rr[l] = s % BASE;
          b = (s >= BASE);
        }
        bool ok = true;
        for (int l = 1; l <= LIM; l++) {
          int coly = md(j - l, m);
          int val = EE[t][coly] + rr[g ? l + 1 : l];
          if (val != W[tn][coly]) ok = false;
        }
        BOK[t][j][bb] = ok;
        RB1[t][j][bb] = rr[1];
      }
  }
}

// ---------------------------------------------------------------- level computation
struct Lay {
  u32 n = 0;
  vector<u8> cells;
  vector<u32> ht;
  u32 mask = 0;
};
static const u32 EMPTYS = 0xFFFFFFFFu;

static inline u64 hsh(const u8 *p, int len) {
  u64 h = 0x9E3779B97F4A7C15ULL * (u64)(len + 1);
  while (len >= 8) {
    u64 v;
    memcpy(&v, p, 8);
    h = (h ^ v) * 0x100000001B3ULL;
    h ^= h >> 29;
    p += 8;
    len -= 8;
  }
  if (len) {
    u64 v = 0;
    memcpy(&v, p, len);
    h = (h ^ v) * 0x100000001B3ULL;
    h ^= h >> 29;
  }
  h *= 0x9E3779B97F4A7C15ULL;
  return h ^ (h >> 32);
}
static void build_ht(Lay &L, int len) {
  u32 cap = 16;
  while (cap < (u64)L.n * 2 + 2) cap <<= 1;
  L.ht.assign(cap, EMPTYS);
  L.mask = cap - 1;
  for (u32 i = 0; i < L.n; i++) {
    u32 h = (u32)hsh(&L.cells[(size_t)i * len], len) & L.mask;
    while (L.ht[h] != EMPTYS) h = (h + 1) & L.mask;
    L.ht[h] = i;
  }
}
static inline long lookup(const Lay &L, const u8 *key, int len) {
  if (L.n == 0) return -1;
  u32 h = (u32)hsh(key, len) & L.mask;
  for (;;) {
    u32 v = L.ht[h];
    if (v == EMPTYS) return -1;
    if (memcmp(&L.cells[(size_t)v * len], key, len) == 0) return v;
    h = (h + 1) & L.mask;
  }
}

static void pfor(size_t n, int nth, const function<void(size_t, size_t, int)> &f) {
  if (n == 0) return;
  if (nth <= 1 || n < 2000) {
    f(0, n, 0);
    return;
  }
  vector<thread> th;
  size_t step = n / nth + 1;
  for (int i = 0; i < nth; i++) {
    size_t a = min(n, step * i), b = min(n, step * (i + 1));
    th.emplace_back([&, a, b, i]() { f(a, b, i); });
  }
  for (auto &x : th) x.join();
}


// Budget frame: the window [c,c+K) may shift by one column at any step, but two shifts are at least B steps apart.
// This contains every balanced schedule floor(d t + const) with drift 0 <= d <= 1/B.  Phase = (t, j, beta), beta = steps
// still to wait before the next shift is allowed.
static int Bud;
static vector<vector<vector<int>>> TOPS0;  // [a][Din] -> possible values of the new top cell for a shift at an overflow-free step
static inline int phid(int t, int j, int beta) { return ((t * m + j) * Bud) + beta; }
static void prep_tops() {
  TOPS0.assign(2, vector<vector<int>>(2));
  for (int a = 0; a < 2; a++)
    for (int Din = 0; Din < 2; Din++) {
      vector<char> seen(2 * BS + 2, 0);
      for (int p = 0; p < BS; p++)
        for (int bp = 0; bp < 2; bp++) {
          if ((int)(p + bp >= BASE) != Din) continue;
          int e = (p + a) % BASE, r = (p + bp) % BASE;
          seen[e + r] = 1;
        }
      for (int v = 0; v < (int)seen.size(); v++)
        if (seen[v]) TOPS0[a][Din].push_back(v);
    }
}

// emit(phase', head (K-1 cells), tops, ntops)
template <class CB>
static inline void budget_succ(int t, int j, int beta, const u8 *w, int K, int allowShift, int allowStay, CB &&emit) {
  const int g = clk[t], tn = (t + 1) % tp;
  int e[64], r[64], a = UP[t][j];
  for (int i = 0; i < K; i++) {
    int s_ = w[i] + a;
    e[i] = s_ % BASE;
    a = (s_ >= BASE);
  }
  u8 nw[64], tops[64];
  for (int Din = 0; Din < 2; Din++) {
    int b = Din;
    for (int i = K - 1; i >= 0; i--) {
      int s_ = w[i] + b;
      r[i] = s_ % BASE;
      b = (s_ >= BASE);
    }
    if (!BOK[t][j][b]) continue;
    const int rb1 = RB1[t][j][b];
    if (allowStay) {
      // no shift
      int ph2 = phid(tn, j, beta > 0 ? beta - 1 : 0);
      if (g == 0) {
        for (int i = 0; i < K - 1; i++) nw[i] = (u8)(e[i] + r[i]);
        tops[0] = (u8)(e[K - 1] + r[K - 1]);
      } else {
        int prev = rb1;
        for (int i = 0; i < K; i++) {
          int val = e[i] + prev;
          prev = r[i];
          if (i < K - 1)
            nw[i] = (u8)val;
          else
            tops[0] = (u8)val;
        }
      }
      emit(ph2, nw, tops, 1);
    }
    if (beta == 0 && allowShift) {
      // shift by one column: the leaving cell c must become lattice at t+1
      int leave = e[0] + (g == 1 ? rb1 : r[0]);
      if (leave == W[tn][j]) {
        int ph2 = phid(tn, (j + 1) % m, Bud - 1);
        if (g == 1) {
          for (int i = 0; i < K - 1; i++) nw[i] = (u8)(e[i + 1] + r[i]);
          for (int v = 0; v < BASE; v++) tops[v] = (u8)(v + r[K - 1]);
          emit(ph2, nw, tops, BASE);
        } else {
          for (int i = 0; i < K - 1; i++) nw[i] = (u8)(e[i + 1] + r[i + 1]);
          const auto &tv = TOPS0[a][Din];
          for (size_t z = 0; z < tv.size(); z++) tops[z] = (u8)tv[z];
          emit(ph2, nw, tops, (int)tv.size());
        }
      }
    }
  }
}


static inline int LL(int t, int x) { return x < nB ? Bt[t][x] : W[t][(x - nB) % m]; }

static void budget_selftest(u64 seed, long count) {
  prep_tops();
  mt19937_64 rng(seed);
  long stayok = 0, shiftok = 0, none = 0;
  for (long it = 0; it < count; it++) {
    int t = rng() % tp, par = rng() % 2, j = rng() % m, K = 1 + rng() % 12, D = K + 1 + rng() % 5;
    int c = nB + 3 * m + j + m * (rng() % 3);
    int h = c + D, n = 2 * h - par;
    vector<int> P(h);
    for (int x = 0; x < c; x++) P[x] = LL(t, x);
    int mode = rng() % 5;
    for (int i = 0; i < D; i++) {
      if (mode == 0)
        P[c + i] = rng() % BS;
      else if (mode == 1)
        P[c + i] = (rng() % 3 == 0) ? (int)(rng() % BS) : W[t][(j + i) % m];
      else
        P[c + i] = (rng() % 7 == 0) ? (int)(rng() % BS) : W[t][(j + i) % m];
    }
    if (par == 1) P[h - 1] = P[h - 1] / 2 * 2;
    vector<int> d(n);
    for (int x = 0; x < h - par; x++) {
      int lo = max(0, P[x] - (BASE - 1)), hi = min(P[x], BASE - 1);
      int v = lo + rng() % (hi - lo + 1);
      d[x] = v;
      d[n - 1 - x] = P[x] - v;
    }
    if (par == 1) d[h - 1] = P[h - 1] / 2;
    vector<int> res(n + 1);
    int carry = 0;
    for (int i = 0; i < n; i++) {
      int s_ = d[i] + d[n - 1 - i] + carry;
      res[i] = s_ % BASE;
      carry = (s_ >= BASE);
    }
    res[n] = carry;
    int n2 = n + carry;
    if (carry != clk[t]) die("budget selftest: overflow differs from clock");
    int h2 = (n2 + 1) / 2, tn = (t + 1) % tp;
    vector<int> P2(h2);
    for (int x = 0; x < h2; x++) P2[x] = res[x] + res[n2 - 1 - x];
    u8 w[64];
    for (int i = 0; i < K; i++) w[i] = (u8)P[c + i];
    for (int s = 0; s < 2; s++) {
      int c2 = c + s;
      if (c2 + K > h2) continue;
      bool ok = true;
      for (int x = 0; x < c2; x++)
        if (P2[x] != LL(tn, x)) ok = false;
      if (!ok) continue;
      bool found = false;
      budget_succ(t, j, 0, w, K, 1, 1, [&](int ph2, const u8 *head, const u8 *tops, int nt) {
        int rest = ph2 / Bud, j2 = rest % m;
        int isshift = (j2 == (j + 1) % m) && (m > 1);
        if (isshift != s) return;
        bool same = true;
        for (int i = 0; i < K - 1; i++)
          if (head[i] != P2[c2 + i]) same = false;
        if (!same) return;
        for (int z = 0; z < nt; z++)
          if (tops[z] == P2[c2 + K - 1]) found = true;
      });
      if (!found) {
        fprintf(stderr, "t=%d j=%d par=%d K=%d D=%d s=%d g=%d\n", t, j, par, K, D, s, clk[t]);
        die("budget selftest: genuine successor missing");
      }
      if (s == 0)
        stayok++;
      else
        shiftok++;
    }
    none++;
  }
  printf("budget selftest PASS: %ld tests, genuine stay successors found %ld, genuine shift successors found %ld\n", none, stayok, shiftok);
}

static void run_budget(int Kmax, int nth, int driftZero) {
  prep_tops();
  const int NP = tp * m * Bud;
  printf("# budget closure base %d tp %d m %d B %d phases %d%s\n", BASE, tp, m, Bud, NP, driftZero ? " (no shifts at all)" : "");
  vector<Lay> P(NP);
  for (auto &L : P) L.n = 1;
  for (int K = 1; K <= Kmax; K++) {
    auto t0 = chrono::steady_clock::now();
    const int Kp = K - 1;
    pfor(NP, nth, [&](size_t a, size_t b, int) {
      for (size_t l = a; l < b; l++)
        if (Kp > 0) build_ht(P[l], Kp);
    });
    vector<u64> base0(NP + 1, 0);
    for (int p = 0; p < NP; p++) base0[p + 1] = base0[p] + (u64)P[p].n * BS;
    const u64 Ncand = base0[NP];
    if (Ncand >= 0xFFFFFFF0ULL) die("too many candidates");
    // adjacency
    vector<u64> off(Ncand + 1, 0);
    vector<vector<u32>> partD(nth);
    vector<vector<pair<u32, u32>>> partC(nth);
    // process phases in parallel by node ranges
    pfor(Ncand, nth, [&](size_t aa, size_t bb, int id) {
      auto &D = partD[id];
      auto &C = partC[id];
      u8 w[64];
      int ph = (int)(upper_bound(base0.begin(), base0.end(), (u64)aa) - base0.begin()) - 1;
      for (size_t node = aa; node < bb; node++) {
        while (node >= base0[ph + 1]) ph++;
        u64 idx = node - base0[ph];
        u32 pi = (u32)(idx / BS), v = (u32)(idx % BS);
        int beta = ph % Bud, rest = ph / Bud, t = rest / m, j = rest % m;
        if (Kp) memcpy(w, &P[ph].cells[(size_t)pi * Kp], Kp);
        w[Kp] = (u8)v;
        size_t c0 = D.size();
        budget_succ(t, j, beta, w, K, !driftZero, 1, [&](int ph2, const u8 *head, const u8 *tops, int nt) {
          long q = (Kp == 0) ? 0 : lookup(P[ph2], head, Kp);
          if (q < 0 || P[ph2].n == 0) return;
          for (int z = 0; z < nt; z++) D.push_back((u32)(base0[ph2] + (u64)q * BS + tops[z]));
        });
        sort(D.begin() + c0, D.end());
        D.erase(unique(D.begin() + c0, D.end()), D.end());
        C.push_back({(u32)node, (u32)(D.size() - c0)});
      }
    });
    u64 M = 0;
    for (int id = 0; id < nth; id++) M += partD[id].size();
    vector<u32> dst(M);
    {
      u64 pos = 0;
      for (int id = 0; id < nth; id++) {
        if (!partD[id].empty()) memcpy(&dst[pos], partD[id].data(), partD[id].size() * sizeof(u32));
        u64 p2 = pos;
        for (auto &pr : partC[id]) {
          off[pr.first] = p2;
          p2 += pr.second;
        }
        pos += partD[id].size();
        vector<u32>().swap(partD[id]);
        vector<pair<u32, u32>>().swap(partC[id]);
      }
      off[Ncand] = pos;
    }
    // iterative Tarjan
    const u32 UNV = 0xFFFFFFFFu;
    vector<u32> order(Ncand, UNV), low(Ncand, 0);
    vector<u8> onst(Ncand, 0), keep(Ncand, 0);
    vector<u32> st;
    struct Fr {
      u32 id;
      u64 e;
    };
    vector<Fr> stk;
    u32 counter = 0;
    auto isacc = [&](u32 node) {
      int ph = (int)(upper_bound(base0.begin(), base0.end(), (u64)node) - base0.begin()) - 1;
      u64 idx = node - base0[ph];
      u32 pi = (u32)(idx / BS), v = (u32)(idx % BS);
      int rest = ph / Bud, t = rest / m, j = rest % m;
      int w0 = (Kp == 0) ? (int)v : P[ph].cells[(size_t)pi * Kp];
      return w0 != W[t][j];
    };
    for (u64 root = 0; root < Ncand; root++) {
      if (order[root] != UNV) continue;
      order[root] = low[root] = counter++;
      st.push_back((u32)root);
      onst[root] = 1;
      stk.push_back({(u32)root, off[root]});
      while (!stk.empty()) {
        Fr &f = stk.back();
        if (f.e < off[(u64)f.id + 1]) {
          u32 v = dst[f.e++];
          if (order[v] == UNV) {
            order[v] = low[v] = counter++;
            st.push_back(v);
            onst[v] = 1;
            stk.push_back({v, off[v]});
          } else if (onst[v]) {
            low[f.id] = min(low[f.id], order[v]);
          }
        } else {
          u32 id = f.id;
          stk.pop_back();
          if (!stk.empty()) {
            u32 par = stk.back().id;
            low[par] = min(low[par], low[id]);
          }
          if (low[id] == order[id]) {
            size_t start = st.size();
            do {
              start--;
            } while (st[start] != id);
            bool hasAcc = false, big = (st.size() - start >= 2);
            for (size_t i = start; i < st.size(); i++) {
              if (!hasAcc && big && isacc(st[i])) hasAcc = true;
              onst[st[i]] = 0;
            }
            if (hasAcc)
              for (size_t i = start; i < st.size(); i++) keep[st[i]] = 1;
            st.resize(start);
          }
        }
      }
    }
    vector<Lay> New(NP);
    u64 total = 0, nacc = 0;
    for (int ph = 0; ph < NP; ph++) {
      Lay &L = New[ph];
      for (u64 node = base0[ph]; node < base0[ph + 1]; node++)
        if (keep[node]) {
          u64 idx = node - base0[ph];
          u32 pi = (u32)(idx / BS), v = (u32)(idx % BS);
          if (Kp) L.cells.insert(L.cells.end(), P[ph].cells.begin() + (size_t)pi * Kp, P[ph].cells.begin() + (size_t)(pi + 1) * Kp);
          L.cells.push_back((u8)v);
          L.n++;
          total++;
          if (isacc((u32)node)) nacc++;
        }
    }
    double sec = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    printf("K %d CycAccBudget %llu accepting %llu candidates %llu edges %llu time %.1f\n", K, (unsigned long long)total, (unsigned long long)nacc, (unsigned long long)Ncand, (unsigned long long)M, sec);
    fflush(stdout);
    P = std::move(New);
    if (total == 0) {
      printf("EMPTY at K=%d\n", K);
      fflush(stdout);
      break;
    }
  }
}

int main(int argc, char **argv) {
  if (argc < 5) die("usage: mc13d LATFILE B KMAX THREADS [zero]");
  read_lat(argv[1]);
  prep();
  Bud = atoi(argv[2]);
  if (string(argv[3]) == "selftest") {
    budget_selftest(strtoull(argv[4], 0, 10), atol(argv[5]));
    return 0;
  }
  run_budget(atoi(argv[3]), atoi(argv[4]), argc > 5 && string(argv[5]) == "zero" ? 1 : 0);
  return 0;
}
