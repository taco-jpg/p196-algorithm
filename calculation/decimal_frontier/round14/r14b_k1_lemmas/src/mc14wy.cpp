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

static bool WIRE = false;
static bool NO9 = false;
static int FORB = -1;
static void prep() {
  UP.assign(tp, vector<int>(m));
  DN = UP;
  EE = UP;
  // wire mode (round 14): the bulk is an all-(b-1) column; its carries are the streams of the head.  The carry leaving the window must be
  // the complement of the forward stream, otherwise the wire cells do not stay (b-1).
  WIRE = true;
  for (int t = 0; t < tp; t++)
    for (int x = 0; x < m; x++)
      if (W[t][x] != BASE - 1) WIRE = false;
  if (WIRE) {
    if (m != 1) die("wire needs m = 1");
    BOK.assign(tp, vector<array<int, 2>>(m));
    RB1 = BOK;
    for (int t = 0; t < tp; t++) {
      int a = 0;
      for (int x = 0; x < nB; x++) a = (Bt[t][x] + a >= BASE);
      UP[t][0] = a;
      EE[t][0] = (BASE - 1 + a) % BASE;
      DN[t][0] = 1 - a;
      for (int bb = 0; bb < 2; bb++) {
        BOK[t][0][bb] = (bb == 1 - a);
        RB1[t][0][bb] = (BASE - 1 + bb) % BASE;
      }
    }
    return;
  }
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

struct Phase {
  int t, j, par;
};

static vector<vector<Phase>> all_orbits() {
  int tot = tp * m * 2;
  vector<char> seen(tot, 0);
  vector<vector<Phase>> out;
  for (int id = 0; id < tot; id++) {
    if (seen[id]) continue;
    vector<Phase> o;
    int cur = id;
    while (!seen[cur]) {
      seen[cur] = 1;
      int par = cur & 1, rest = cur >> 1, t = rest / m, j = rest % m;
      o.push_back({t, j, par});
      int g = clk[t], dh = (g == 1 && par == 0);
      int t2 = (t + 1) % tp, j2 = (j + dh) % m, par2 = (par + g) % 2;
      cur = ((t2 * m + j2) * 2) + par2;
    }
    if (cur != id) die("nu not a permutation");
    out.push_back(o);
  }
  return out;
}

// All R_K successors of (ph,w).  For each admissible descending carry Din entering from above:
// head = first K-1 new cells, tops[0..nt) = possible new top cell values.
template <class CB>
static inline void rk_succ(const Phase &ph, const u8 *w, int K, CB &&cb) {
  const int t = ph.t, j = ph.j, par = ph.par, g = clk[t], dh = (g == 1 && par == 0), tn = (t + 1) % tp;
  int e[64], r[64], a = UP[t][j];
  for (int i = 0; i < K; i++) {
    int s = w[i] + a;
    e[i] = s % BASE;
    a = (s >= BASE);
  }
  u8 nw[64], tops[32];
  for (int Din = 0; Din < 2; Din++) {
    int b = Din;
    for (int i = K - 1; i >= 0; i--) {
      int s = w[i] + b;
      r[i] = s % BASE;
      b = (s >= BASE);
    }
    if (!BOK[t][j][b]) continue;
    int rb1 = RB1[t][j][b];
    if (dh) {
      if (e[0] + rb1 != W[tn][j]) continue;  // column c leaves the window and must be lattice
      for (int i = 0; i < K - 1; i++) nw[i] = (u8)(e[i + 1] + r[i]);
      for (int v = 0; v < BASE; v++) tops[v] = (u8)(v + r[K - 1]);
      cb(nw, tops, BASE);
    } else if (g == 0) {
      for (int i = 0; i < K - 1; i++) nw[i] = (u8)(e[i] + r[i]);
      tops[0] = (u8)(e[K - 1] + r[K - 1]);
      cb(nw, tops, 1);
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
      cb(nw, tops, 1);
    }
  }
}

// exact fold map F_K: window = top K folded columns
static inline bool exact_step(const Phase &ph, const u8 *w, int K, u8 *nw) {
  const int t = ph.t, j = ph.j, par = ph.par, g = clk[t], dh = (g == 1 && par == 0), tn = (t + 1) % tp;
  int e[64], r[64], a = UP[t][j], topin = 0;
  for (int i = 0; i < K; i++) {
    if (i == K - 1) topin = a;
    int s = w[i] + a;
    e[i] = s % BASE;
    a = (s >= BASE);
  }
  int Din = (par == 0) ? a : topin;
  int b = Din;
  for (int i = K - 1; i >= 0; i--) {
    int s = w[i] + b;
    r[i] = s % BASE;
    b = (s >= BASE);
  }
  if (!BOK[t][j][b]) return false;
  int rb1 = RB1[t][j][b];
  if (dh) {
    if (e[0] + rb1 != W[tn][j]) return false;
    for (int i = 0; i < K - 1; i++) nw[i] = (u8)(e[i + 1] + r[i]);
    nw[K - 1] = (u8)(2 * r[K - 1]);
  } else if (g == 0) {
    for (int i = 0; i < K; i++) nw[i] = (u8)(e[i] + r[i]);
  } else {
    int prev = rb1;
    for (int i = 0; i < K; i++) {
      nw[i] = (u8)(e[i] + prev);
      prev = r[i];
    }
  }
  return true;
}

// ---------------------------------------------------------------- selftest by plain addition
static inline int LL(int t, int x) { return x < nB ? Bt[t][x] : W[t][(x - nB) % m]; }

static void selftest(u64 seed, long count) {
  mt19937_64 rng(seed);
  long defined = 0, undefined = 0, rk = 0, shifts = 0;
  for (long it = 0; it < count; it++) {
    int t = rng() % tp, par = rng() % 2, j = rng() % m, D = 1 + rng() % 16;
    int c = nB + 3 * m + j + m * (rng() % 3);
    int h = c + D, n = 2 * h - par;
    vector<int> P(h);
    for (int x = 0; x < c; x++) P[x] = LL(t, x);
    int mode = rng() % 4;
    for (int i = 0; i < D; i++) {
      // mode 0: random window; others: lattice-like window with few changes, so that many steps are defined
      if (mode == 0)
        P[c + i] = rng() % BS;
      else
        P[c + i] = (rng() % 5 == 0) ? (int)(rng() % BS) : W[t][(j + i) % m];
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
      int s = d[i] + d[n - 1 - i] + carry;
      res[i] = s % BASE;
      carry = (s >= BASE);
    }
    res[n] = carry;
    int n2 = n + carry, gam = carry;
    if (gam != clk[t]) {
      if (!WIRE) die("selftest: overflow differs from clock");
      Phase ph0{t, j, par};
      u8 w0[64], nw0[64];
      for (int i = 0; i < D; i++) w0[i] = (u8)P[c + i];
      if (exact_step(ph0, w0, D, nw0)) die("selftest: F_K defined although the genuine overflow differs from the clock");
      undefined++;
      continue;
    }
    int h2 = (n2 + 1) / 2, c2 = h2 - D;
    int tn = (t + 1) % tp;
    vector<int> P2(h2);
    for (int x = 0; x < h2; x++) P2[x] = res[x] + res[n2 - 1 - x];
    bool genuine = true;
    for (int x = 0; x < c2; x++)
      if (P2[x] != LL(tn, x)) genuine = false;
    int dh = (clk[t] == 1 && par == 0);
    if (c2 != c + dh) die("selftest: frame motion");
    Phase ph{t, j, par};
    u8 w[64], nw[64];
    for (int i = 0; i < D; i++) w[i] = (u8)P[c + i];
    bool mine = exact_step(ph, w, D, nw);
    if (mine != genuine) {
      fprintf(stderr, "t=%d j=%d par=%d D=%d genuine=%d mine=%d\n", t, j, par, D, (int)genuine, (int)mine);
      die("selftest: F_K defined/undefined differs");
    }
    if (genuine) {
      defined++;
      if (dh) shifts++;
      for (int i = 0; i < D; i++)
        if (nw[i] != P2[c2 + i]) die("selftest: F_K window differs");
      for (int K = 1; K <= D; K++) {
        bool found = false;
        rk_succ(ph, w, K, [&](const u8 *head, const u8 *tops, int nt) {
          bool same = true;
          for (int i = 0; i < K - 1; i++)
            if (head[i] != P2[c2 + i]) same = false;
          if (!same) return;
          for (int z = 0; z < nt; z++)
            if (tops[z] == P2[c2 + K - 1]) found = true;
        });
        if (!found) die("selftest: genuine successor not an R_K edge");
        rk++;
      }
    } else
      undefined++;
  }
  printf("selftest PASS: %ld tests, F_K defined %ld (frame shifts %ld), undefined %ld, R_K containment checks %ld\n",
         count, defined, shifts, undefined, rk);
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

static void run_level_chain(int orbitIdx, int Kmax, int nth, int printExact, int sccMode = 0) {
  auto orbits = all_orbits();
  if (orbitIdx >= (int)orbits.size()) die("orbit index");
  const vector<Phase> &ph = orbits[orbitIdx];
  const int T = (int)ph.size();
  printf("# base %d tp %d nB %d m %d  orbits %zu  orbit %d  T=%d  first phase (t=%d,j=%d,par=%d)\n", BASE, tp, nB, m,
         orbits.size(), orbitIdx, T, ph[0].t, ph[0].j, ph[0].par);
  vector<Lay> P(T);
  for (auto &L : P) L.n = 1;
  for (int K = 1; K <= Kmax; K++) {
    auto t0 = chrono::steady_clock::now();
    const int Kp = K - 1;
    pfor(T, nth, [&](size_t a, size_t b, int) {
      for (size_t l = a; l < b; l++)
        if (Kp > 0) build_ht(P[l], Kp);
    });
    int anchor = 0;
    for (int l = 0; l < T; l++)
      if (P[l].n < P[anchor].n) anchor = l;
    vector<vector<u32>> alive(T), off(T), dst(T);
    if ((u64)P[anchor].n * BS >= 0xFFFFFFF0ULL) die("too many candidates");
    alive[0].resize(P[anchor].n * BS);
    iota(alive[0].begin(), alive[0].end(), 0u);
    for (int r = 0; r < T; r++) {
      const int l = (anchor + r) % T, l2 = (anchor + r + 1) % T;
      const Lay &PL = P[l], &PN = P[l2];
      const Phase &PH = ph[l];
      const size_t nn = alive[r].size();
      vector<vector<u32>> partS(nth), partC(nth);
      vector<size_t> partA(nth, 0), partB(nth, 0);
      pfor(nn, nth, [&](size_t a, size_t b, int id) {
        partA[id] = a;
        partB[id] = b;
        auto &S = partS[id];
        auto &C = partC[id];
        u8 w[64];
        for (size_t i = a; i < b; i++) {
          u32 idx = alive[r][i], pi = idx / BS, v = idx % BS;
          if (Kp) memcpy(w, &PL.cells[(size_t)pi * Kp], Kp);
          w[Kp] = (u8)v;
          size_t c0 = S.size();
          rk_succ(PH, w, K, [&](const u8 *head, const u8 *tops, int nt) {
            if (NO9) {
              // reject off-lattice 9-cells in the new window (head cells)
              const Phase &P2 = ph[l2];
              for (int i = 0; i < K - 1; i++) if (head[i] == (FORB>=0?FORB:BASE - 1) && W[P2.t][(P2.j + i) % m] != head[i]) return;
            }
            long q = (Kp == 0) ? (PN.n ? 0 : -1) : lookup(PN, head, Kp);
            if (q < 0) return;
            for (int z = 0; z < nt; z++) {
              if (NO9) { const Phase &P2 = ph[l2]; if (tops[z] == (FORB>=0?FORB:BASE - 1) && W[P2.t][(P2.j + K - 1) % m] != tops[z]) continue; }
              S.push_back((u32)q * BS + tops[z]);
            }
          });
          sort(S.begin() + c0, S.end());
          S.erase(unique(S.begin() + c0, S.end()), S.end());
          C.push_back((u32)(S.size() - c0));
        }
      });
      off[r].resize(nn + 1);
      size_t total = 0;
      for (int id = 0; id < nth; id++) total += partS[id].size();
      dst[r].resize(total);
      size_t posE = 0, posN = 0;
      off[r][0] = 0;
      if (total > 0xFFFFFFF0ULL) die("too many edges");
      for (int id = 0; id < nth; id++) {
        if (!partS[id].empty()) memcpy(&dst[r][posE], partS[id].data(), partS[id].size() * sizeof(u32));
        for (u32 c : partC[id]) {
          off[r][posN + 1] = off[r][posN] + c;
          posN++;
        }
        posE += partS[id].size();
        vector<u32>().swap(partS[id]);
        vector<u32>().swap(partC[id]);
      }
      if (posN != nn) die("internal: node count");
      vector<u32> *target;
      vector<u32> tmp;
      if (r + 1 < T) {
        tmp = dst[r];
        sort(tmp.begin(), tmp.end());
        tmp.erase(unique(tmp.begin(), tmp.end()), tmp.end());
        alive[r + 1] = std::move(tmp);
        target = &alive[r + 1];
      } else
        target = &alive[0];
      // successor id -> position in target layer; edges into nodes absent from layer 0 are dropped
      vector<u32> newoff(nn + 1, 0), newdst;
      newdst.reserve(dst[r].size());
      for (size_t u = 0; u < nn; u++) {
        for (u32 e = off[r][u]; e < off[r][u + 1]; e++) {
          auto it = lower_bound(target->begin(), target->end(), dst[r][e]);
          if (it != target->end() && *it == dst[r][e]) newdst.push_back((u32)(it - target->begin()));
        }
        newoff[u + 1] = (u32)newdst.size();
      }
      off[r] = std::move(newoff);
      dst[r] = std::move(newdst);
    }
    // remember the candidate ids before compressing: alive[r] holds them; compress keeps them in step.
    for (int round = 0; round < 60; round++) {
      vector<vector<char>> keep(T);
      for (int r = 0; r < T; r++) keep[r].assign(alive[r].size(), 1);
      for (int r = T - 1; r >= 0; r--) {
        int nx = (r + 1) % T;
        for (size_t u = 0; u < alive[r].size(); u++) {
          char ok = 0;
          for (u32 e = off[r][u]; e < off[r][u + 1]; e++)
            if (keep[nx][dst[r][e]]) {
              ok = 1;
              break;
            }
          keep[r][u] = ok;
        }
      }
      for (int r = 0; r < T; r++) {
        int nx = (r + 1) % T;
        vector<char> has(alive[nx].size(), 0);
        for (size_t u = 0; u < alive[r].size(); u++)
          if (keep[r][u])
            for (u32 e = off[r][u]; e < off[r][u + 1]; e++) has[dst[r][e]] = 1;
        for (size_t v = 0; v < has.size(); v++)
          if (!has[v]) keep[nx][v] = 0;
      }
      bool changed = false;
      vector<vector<u32>> mp(T);
      for (int r = 0; r < T; r++) {
        mp[r].assign(alive[r].size(), EMPTYS);
        u32 c = 0;
        for (size_t u = 0; u < alive[r].size(); u++)
          if (keep[r][u])
            mp[r][u] = c++;
          else
            changed = true;
      }
      if (!changed) break;
      for (int r = 0; r < T; r++) {
        int nx = (r + 1) % T;
        vector<u32> na, no(1, 0), nd;
        for (size_t u = 0; u < alive[r].size(); u++)
          if (keep[r][u]) {
            na.push_back(alive[r][u]);
            for (u32 e = off[r][u]; e < off[r][u + 1]; e++)
              if (keep[nx][dst[r][e]]) nd.push_back(mp[nx][dst[r][e]]);
            no.push_back((u32)nd.size());
          }
        alive[r] = std::move(na);
        off[r] = std::move(no);
        dst[r] = std::move(nd);
      }
    }
    // accepting flags
    vector<vector<char>> acc(T);
    vector<u64> base0(T + 1, 0);
    for (int r = 0; r < T; r++) {
      base0[r + 1] = base0[r] + alive[r].size();
      int l = (anchor + r) % T;
      const Phase &PH = ph[l];
      acc[r].resize(alive[r].size());
      for (size_t u = 0; u < alive[r].size(); u++) {
        u32 idx = alive[r][u], pi = idx / BS, v = idx % BS;
        int w0 = (Kp == 0) ? (int)v : P[l].cells[(size_t)pi * Kp];
        acc[r][u] = (w0 != W[PH.t][PH.j]);
      }
    }
    const u64 Ntot = base0[T];
    const size_t N0 = alive[0].size();
    vector<u8> inE(Ntot, 0);
    atomic<size_t> nextBatch(0);
    const size_t nb = (N0 + 63) / 64;
    if (!sccMode) {
      vector<thread> th;
      for (int id = 0; id < nth; id++)
        th.emplace_back([&]() {
          vector<u64> F0(Ntot, 0), F1(Ntot, 0), B0(Ntot, 0), B1(Ntot, 0);
          vector<vector<u32>> fr(T);
          for (;;) {
            size_t bi = nextBatch.fetch_add(1);
            if (bi >= nb) break;
            size_t lo = bi * 64, hi = min(N0, lo + 64);
            for (auto &x : fr) x.clear();
            for (size_t i = lo; i < hi; i++) {
              fr[0].push_back((u32)i);
              if (acc[0][i])
                F1[i] = 1ULL << (i - lo);
              else
                F0[i] = 1ULL << (i - lo);
            }
            for (int r = 0; r + 1 < T; r++) {
              const u64 b0 = base0[r], b1 = base0[r + 1];
              for (u32 u : fr[r]) {
                u64 f0 = F0[b0 + u], f1 = F1[b0 + u];
                for (u32 e = off[r][u]; e < off[r][u + 1]; e++) {
                  u32 v = dst[r][e];
                  u64 ix = b1 + v;
                  if (F0[ix] == 0 && F1[ix] == 0) fr[r + 1].push_back(v);
                  if (acc[r + 1][v])
                    F1[ix] |= (f0 | f1);
                  else {
                    F0[ix] |= f0;
                    F1[ix] |= f1;
                  }
                }
              }
            }
            for (int r = T - 1; r >= 0; r--) {
              const u64 bb0 = base0[r];
              for (u32 u : fr[r]) {
                u64 ix = bb0 + u, b0v = 0, b1v = 0;
                const bool au = acc[r][u];
                for (u32 e = off[r][u]; e < off[r][u + 1]; e++) {
                  u32 v = dst[r][e];
                  if (r == T - 1) {
                    if (v >= lo && v < hi) {
                      u64 bit = 1ULL << (v - lo);
                      if (au)
                        b1v |= bit;
                      else
                        b0v |= bit;
                    }
                  } else {
                    u64 jx = base0[r + 1] + v;
                    if (au)
                      b1v |= (B0[jx] | B1[jx]);
                    else {
                      b0v |= B0[jx];
                      b1v |= B1[jx];
                    }
                  }
                }
                B0[ix] = b0v;
                B1[ix] = b1v;
                u64 mm = (F1[ix] & (b0v | b1v)) | (F0[ix] & b1v);
                if (mm) __atomic_store_n(&inE[ix], (u8)1, __ATOMIC_RELAXED);
              }
            }
            for (int r = 0; r < T; r++)
              for (u32 u : fr[r]) {
                u64 ix = base0[r] + u;
                F0[ix] = F1[ix] = B0[ix] = B1[ix] = 0;
              }
          }
        });
      for (auto &x : th) x.join();
    }
    if (sccMode) {
      // all periods at once: a state lies on a closed walk through an accepting state iff its SCC contains one
      const u32 UNV = 0xFFFFFFFFu;
      if (Ntot >= 0xFFFFFFF0ULL) die("too many nodes for Tarjan");
      vector<u32> order(Ntot, UNV), low(Ntot, 0);
      vector<u8> onst(Ntot, 0), accG(Ntot, 0);
      for (int r = 0; r < T; r++)
        for (size_t u = 0; u < alive[r].size(); u++) accG[base0[r] + u] = (u8)acc[r][u];
      vector<u32> st;
      struct Fr {
        u32 id, e, eend;
        int r;
      };
      vector<Fr> stk;
      u32 counter = 0;
      for (int r0 = 0; r0 < T; r0++)
        for (u32 u0 = 0; u0 < alive[r0].size(); u0++) {
          u32 root = (u32)(base0[r0] + u0);
          if (order[root] != UNV) continue;
          order[root] = low[root] = counter++;
          st.push_back(root);
          onst[root] = 1;
          stk.push_back({root, off[r0][u0], off[r0][u0 + 1], r0});
          while (!stk.empty()) {
            Fr &f = stk.back();
            if (f.e < f.eend) {
              u32 v = dst[f.r][f.e++];
              int r2 = (f.r + 1) % T;
              u32 id2 = (u32)(base0[r2] + v);
              if (order[id2] == UNV) {
                order[id2] = low[id2] = counter++;
                st.push_back(id2);
                onst[id2] = 1;
                stk.push_back({id2, off[r2][v], off[r2][v + 1], r2});
              } else if (onst[id2]) {
                low[f.id] = min(low[f.id], order[id2]);
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
                bool hasAcc = false;
                for (size_t i = start; i < st.size(); i++) {
                  if (accG[st[i]]) hasAcc = true;
                  onst[st[i]] = 0;
                }
                if (hasAcc && st.size() - start >= 2)
                  for (size_t i = start; i < st.size(); i++) inE[st[i]] = 1;
                st.resize(start);
              }
            }
          }
        }
    }
    vector<Lay> New(T);
    u64 total = 0, naccept = 0, parents = 0;
    for (int r = 0; r < T; r++) {
      int l = (anchor + r) % T;
      Lay &L = New[l];
      u32 lastp = EMPTYS;
      for (size_t u = 0; u < alive[r].size(); u++)
        if (inE[base0[r] + u]) {
          u32 idx = alive[r][u], pi = idx / BS, v = idx % BS;
          if (Kp) L.cells.insert(L.cells.end(), P[l].cells.begin() + (size_t)pi * Kp, P[l].cells.begin() + (size_t)(pi + 1) * Kp);
          L.cells.push_back((u8)v);
          L.n++;
          total++;
          if (acc[r][u]) naccept++;
          if (pi != lastp) {
            parents++;
            lastp = pi;
          }
        }
    }
    vector<vector<u32>>().swap(alive);
    vector<vector<u32>>().swap(off);
    vector<vector<u32>>().swap(dst);
    vector<Lay>().swap(P);
    // exact fold orbits inside E_acc(K,T)
    u64 exact = 0;
    if (total) {
      pfor(T, nth, [&](size_t a, size_t b, int) {
        for (size_t l = a; l < b; l++) build_ht(New[l], K);
      });
      const Lay &AL = New[anchor];
      atomic<u64> ex(0);
      if (sccMode) {
        // periodic orbits of F_K of any period inside the set: functional graph of the one-lap return map on the anchor layer
        vector<long> ret(AL.n, -1);
        pfor(AL.n, nth, [&](size_t a, size_t b, int) {
          u8 cur[64], nxt[64];
          for (size_t i = a; i < b; i++) {
            memcpy(cur, &AL.cells[i * K], K);
            int l = anchor;
            bool ok = true;
            long q = -1;
            for (int s = 0; s < T; s++) {
              if (!exact_step(ph[l], cur, K, nxt)) {
                ok = false;
                break;
              }
              l = (l + 1) % T;
              q = lookup(New[l], nxt, K);
              if (q < 0) {
                ok = false;
                break;
              }
              memcpy(cur, nxt, K);
            }
            ret[i] = ok ? q : -1;
          }
        });
        vector<u8> col(AL.n, 0);
        u64 pts = 0;
        for (size_t i = 0; i < AL.n; i++) {
          if (col[i]) continue;
          vector<long> path;
          long x = (long)i;
          while (x >= 0 && col[x] == 0) {
            col[x] = 1;
            path.push_back(x);
            x = ret[x];
          }
          if (x >= 0 && col[x] == 1) {
            size_t z = 0;
            while (path[z] != x) z++;
            pts += path.size() - z;
            string s;
            for (int q = 0; q < K; q++) s += to_string((int)AL.cells[(size_t)x * K + q]) + " ";
            printf("# PERIODIC exact orbit K=%d laps=%zu period=%zu anchor phase (t=%d,j=%d,par=%d): %s\n", K, path.size() - z, (path.size() - z) * (size_t)T, ph[anchor].t, ph[anchor].j, ph[anchor].par, s.c_str());
          }
          for (long p : path) col[p] = 2;
        }
        ex = pts;
      } else
      pfor(AL.n, nth, [&](size_t a, size_t b, int) {
        u8 cur[64], nxt[64];
        for (size_t i = a; i < b; i++) {
          memcpy(cur, &AL.cells[i * K], K);
          int l = anchor;
          bool ok = true;
          for (int s = 0; s < T; s++) {
            if (!exact_step(ph[l], cur, K, nxt)) {
              ok = false;
              break;
            }
            l = (l + 1) % T;
            if (lookup(New[l], nxt, K) < 0) {
              ok = false;
              break;
            }
            memcpy(cur, nxt, K);
          }
          if (ok && memcmp(cur, &AL.cells[i * K], K) == 0) {
            ex++;
            if (printExact) {
              string s;
              for (int q = 0; q < K; q++) s += to_string((int)cur[q]) + " ";
              printf("# exact orbit K=%d anchor phase (t=%d,j=%d,par=%d): %s\n", K, ph[anchor].t, ph[anchor].j, ph[anchor].par, s.c_str());
            }
          }
        }
      });
      exact = ex.load();
    }
    double sec = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    printf("K %d Eacc %llu accepting %llu parents %llu exact %llu nodes %llu time %.1f\n", K, (unsigned long long)total,
           (unsigned long long)naccept, (unsigned long long)parents, (unsigned long long)exact, (unsigned long long)Ntot, sec);
    fflush(stdout);
    { const char *dd=getenv("DUMPDIR"); if(dd && total){ char fn[512]; snprintf(fn,sizeof fn,"%s/K%d.bin",dd,K); FILE*fo=fopen(fn,"wb"); int hdr[2]={T,K}; fwrite(hdr,sizeof(int),2,fo); for(int l=0;l<T;l++){ int rec[4]={ph[l].t,ph[l].j,ph[l].par,(int)New[l].n}; fwrite(rec,sizeof(int),4,fo); fwrite(New[l].cells.data(),1,(size_t)New[l].n*K,fo);} fclose(fo);} }
    P = std::move(New);
    if (total == 0) {
      printf("EMPTY at K=%d\n", K);
      fflush(stdout);
      break;
    }
  }
}

int main(int argc, char **argv) {
  if (argc < 3) die("usage");
  string mode = argv[1];
  read_lat(argv[2]);
  prep();
  if (getenv("NO9")) NO9 = true;
  if (getenv("FORB")) { FORB = atoi(getenv("FORB")); NO9 = true; }
  if (mode == "selftest") {
    selftest(strtoull(argv[3], 0, 10), atol(argv[4]));
  } else if (mode == "run") {
    run_level_chain(atoi(argv[3]), atoi(argv[4]), atoi(argv[5]), argc > 6 ? atoi(argv[6]) : 0);
  } else if (mode == "runscc") {
    run_level_chain(atoi(argv[3]), atoi(argv[4]), atoi(argv[5]), argc > 6 ? atoi(argv[6]) : 0, 1);
  } else if (mode == "orbits") {
    auto o = all_orbits();
    for (size_t i = 0; i < o.size(); i++)
      printf("orbit %zu length %zu first (t=%d,j=%d,par=%d)\n", i, o[i].size(), o[i][0].t, o[i][0].j, o[i][0].par);
  } else
    die("mode");
  return 0;
}
