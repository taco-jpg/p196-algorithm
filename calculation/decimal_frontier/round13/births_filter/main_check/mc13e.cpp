// mc13e.cpp -- main-session independent check of r13c (Theorem B: births above saturated interfaces).
// Written from the definitions (R1)-(R3) of an infinite closed L-history; no code shared with r13c's khr / kh3 / python.
// Modes:
//   mc13e selftest SEED COUNT                genuine addition versus the recurrence (R1-R3)
//   mc13e if G D                             |IF(D)| and saturation height
//   mc13e births G D L                       distinct births above IF(D) and rotation classes
//   mc13e root G L KMAX                      plain tower from the root
//   mc13e towers G D L THREADS NCAP SEC KMAX [SAMPLE] all towers (one per rotation class); optional random sample size
#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <functional>
#include <map>
#include <mutex>
#include <numeric>
#include <random>
#include <string>
#include <thread>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;
typedef uint8_t u8;
typedef uint32_t u32;
typedef uint64_t u64;

static const int b = 10;
static const int BS = 19;
static vector<int> gP;
static int P;
static inline int gt(int t) { return gP[t % P]; }

static void die(const char *s) {
  fprintf(stderr, "FATAL %s\n", s);
  exit(3);
}

struct Iface {
  int per = 0;
  bool root = false;
  vector<u8> c, xb, A;  // c = ascending carry into next column, xb = previous column (only read when g=1), A = mask of allowed top bits
};

static string ikey(const Iface &I) {
  string s;
  s.reserve(3 * I.per + 1);
  s.push_back(I.root ? 'R' : 'N');
  for (int t = 0; t < I.per; t++) {
    s.push_back((char)I.c[t]);
    s.push_back((char)(gt(t) ? I.xb[t] : 0));
    s.push_back((char)I.A[t]);
  }
  return s;
}

static Iface root_iface(int per) {
  Iface I;
  I.per = per;
  I.root = true;
  I.c.assign(per, 0);
  I.xb.assign(per, 0);
  I.A.resize(per);
  for (int t = 0; t < per; t++) I.A[t] = (u8)(1 << gt(t));  // H_0(t) = g_t
  return I;
}

// digit of the next column at time t+1 for the head column value v at time t
static inline int ystep(const Iface &I, int t, int v, int h) {
  int per = I.per;
  int c = I.c[t % per];
  int H = (v + h) >= b;
  int part;
  if (gt(t)) {
    part = I.root ? 1 : (I.xb[t % per] + H) % b;
  } else
    part = (v + h) % b;
  return (v + c) % b + part;
}

// enumerate closed columns v of period D above I (I.per | D)
template <class F>
static void enum_cols(const Iface &I, int D, F &&cb) {
  // nx[t][v] : mask of possible v(t+1)
  vector<array<u32, 19>> nx(D);
  for (int t = 0; t < D; t++)
    for (int v = 0; v < BS; v++) {
      u32 mask = 0;
      if (!(I.root && v == 0))
        for (int h = 0; h < 2; h++) {
          int H = (v + h) >= b;
          if (!((I.A[t % I.per] >> H) & 1)) continue;
          mask |= 1u << ystep(I, t, v, h);
        }
      nx[t][v] = mask;
    }
  vector<u32> back(D + 1);
  vector<int> v(D + 1);
  for (int v0 = (I.root ? 1 : 0); v0 < BS; v0++) {
    back[D] = 1u << v0;
    for (int t = D - 1; t >= 0; t--) {
      u32 m = 0;
      for (int x = 0; x < BS; x++)
        if (nx[t][x] & back[t + 1]) m |= 1u << x;
      back[t] = m;
    }
    if (!((back[0] >> v0) & 1)) continue;
    v[0] = v0;
    // iterative DFS
    vector<u32> rem(D + 1);
    rem[0] = nx[0][v0] & back[1];
    int t = 0;
    while (t >= 0) {
      if (rem[t] == 0) {
        t--;
        continue;
      }
      int y = __builtin_ctz(rem[t]);
      rem[t] &= rem[t] - 1;
      if (t + 1 == D) {
        // y == v0 by construction
        v[D] = y;
        cb(v);
      } else {
        v[t + 1] = y;
        rem[t + 1] = nx[t + 1][y] & back[t + 2];
        t++;
      }
    }
  }
}

// interface above column v (period D); returns false if some A' empty
static bool extend(const Iface &I, const vector<int> &v, int D, Iface &J) {
  J.per = D;
  J.root = false;
  J.c.resize(D);
  J.xb.resize(D);
  J.A.resize(D);
  for (int t = 0; t < D; t++) {
    int vt = v[t], vn = v[(t + 1) % D];
    int mask = 0;
    for (int h = 0; h < 2; h++) {
      int H = (vt + h) >= b;
      if (!((I.A[t % I.per] >> H) & 1)) continue;
      if (ystep(I, t, vt, h) == vn) mask |= 1 << h;
    }
    if (mask == 0) return false;
    J.A[t] = (u8)mask;
    J.c[t] = (u8)((vt + I.c[t % I.per]) >= b);
    J.xb[t] = (u8)(gt(t) ? vt : 0);
  }
  return true;
}

static vector<Iface> saturate(int d, int &a0) {
  vector<Iface> out;
  unordered_map<string, int> seen;
  Iface r = root_iface(d);
  seen[ikey(r)] = 0;
  out.push_back(r);
  vector<int> depth{0};
  a0 = 0;
  for (size_t i = 0; i < out.size(); i++) {
    Iface I = out[i];
    int dep = depth[i];
    enum_cols(I, d, [&](const vector<int> &v) {
      Iface J;
      if (!extend(I, v, d, J)) die("closed column with empty A'");
      string k = ikey(J);
      if (!seen.count(k)) {
        seen[k] = (int)out.size();
        out.push_back(J);
        depth.push_back(dep + 1);
        if (dep + 1 > a0) a0 = dep + 1;
      }
    });
  }
  return out;
}

static string rotkey(const Iface &I) {
  // canonical representative under time rotations by the clock period P
  string best;
  for (int rot = 0; rot < I.per; rot += P) {
    string s;
    s.reserve(3 * I.per);
    for (int t = 0; t < I.per; t++) {
      int u = (t + rot) % I.per;
      s.push_back((char)I.c[u]);
      s.push_back((char)(gt(u) ? I.xb[u] : 0));
      s.push_back((char)I.A[u]);
    }
    if (best.empty() || s < best) best = s;
  }
  return best;
}

static Iface from_rotkey(const string &s, int per) {
  Iface I;
  I.per = per;
  I.root = false;
  I.c.resize(per);
  I.xb.resize(per);
  I.A.resize(per);
  for (int t = 0; t < per; t++) {
    I.c[t] = (u8)s[3 * t];
    I.xb[t] = (u8)s[3 * t + 1];
    I.A[t] = (u8)s[3 * t + 2];
  }
  return I;
}

// ------------------------------------------------------------ tower = levels above an L-periodic interface
struct Lay {
  u32 n = 0;
  vector<u8> cells;
  vector<u32> ht;
  u32 mask = 0;
};
static const u32 EMP = 0xFFFFFFFFu;
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
  L.ht.assign(cap, EMP);
  L.mask = cap - 1;
  for (u32 i = 0; i < L.n; i++) {
    u32 h = (u32)hsh(&L.cells[(size_t)i * len], len) & L.mask;
    while (L.ht[h] != EMP) h = (h + 1) & L.mask;
    L.ht[h] = i;
  }
}
static inline long lookup(const Lay &L, const u8 *key, int len) {
  if (L.n == 0) return -1;
  u32 h = (u32)hsh(key, len) & L.mask;
  for (;;) {
    u32 v = L.ht[h];
    if (v == EMP) return -1;
    if (memcmp(&L.cells[(size_t)v * len], key, len) == 0) return v;
    h = (h + 1) & L.mask;
  }
}

struct TowerResult {
  int death = -1;  // first empty level, or -1 if capped
  int lastLevel = 0;
  u64 kept = 0;
  u64 maxNodes = 0;
};

static TowerResult run_tower(const Iface &I, int T, int kmax, u64 ncap, double seccap, bool verbose = false) {
  TowerResult R;
  auto t0 = chrono::steady_clock::now();
  vector<Lay> P_(T);
  for (auto &L : P_) L.n = 1;
  vector<int> e(kmax + 4), rd(kmax + 4);
  vector<u8> w(kmax + 4), y(kmax + 4);
  for (int K = 1; K <= kmax; K++) {
    const int Kp = K - 1;
    if (Kp > 0)
      for (int l = 0; l < T; l++) build_ht(P_[l], Kp);
    int anchor = 0;
    for (int l = 0; l < T; l++)
      if (P_[l].n < P_[anchor].n) anchor = l;
    vector<vector<u32>> alive(T), off(T), dst(T);
    if ((u64)P_[anchor].n * BS >= 0xFFFFFFF0ULL) {
      R.lastLevel = K;
      return R;
    }
    alive[0].resize(P_[anchor].n * BS);
    iota(alive[0].begin(), alive[0].end(), 0u);
    u64 nodes = 0;
    bool capped = false;
    for (int r = 0; r < T && !capped; r++) {
      const int l = (anchor + r) % T, l2 = (anchor + r + 1) % T;
      const Lay &PL = P_[l], &PN = P_[l2];
      const int g = gt(l), c0 = I.c[l % I.per], xb0 = I.xb[l % I.per], Am = I.A[l % I.per];
      vector<u32> S, C;
      S.reserve(alive[r].size() * 2);
      C.reserve(alive[r].size());
      for (u32 idx : alive[r]) {
        u32 pi = idx / BS, v = idx % BS;
        if (Kp) memcpy(w.data(), &PL.cells[(size_t)pi * Kp], Kp);
        w[Kp] = (u8)v;
        size_t c_start = S.size();
        bool skip = (I.root && Kp == 0 && v == 0);  // column 0 digits are >= 1
        if (!skip) {
          int ca = c0;
          for (int i = 0; i < K; i++) {
            int s = w[i] + ca;
            e[i] = s % b;
            ca = (s >= b);
          }
          for (int h = 0; h < 2; h++) {
            int H = h;
            for (int i = K - 1; i >= 0; i--) {
              int s = w[i] + H;
              rd[i] = s % b;
              H = (s >= b);
            }
            if (!((Am >> H) & 1)) continue;
            for (int i = 0; i < K; i++) {
              int part;
              if (g) {
                if (i == 0)
                  part = I.root ? 1 : (xb0 + H) % b;
                else
                  part = rd[i - 1];
              } else
                part = rd[i];
              y[i] = (u8)(e[i] + part);
            }
            long q = (Kp == 0) ? (PN.n ? 0 : -1) : lookup(PN, y.data(), Kp);
            if (q < 0) continue;
            S.push_back((u32)q * BS + y[K - 1]);
          }
          sort(S.begin() + c_start, S.end());
          S.erase(unique(S.begin() + c_start, S.end()), S.end());
        }
        C.push_back((u32)(S.size() - c_start));
      }
      const size_t nn = alive[r].size();
      off[r].resize(nn + 1);
      off[r][0] = 0;
      for (size_t u = 0; u < nn; u++) off[r][u + 1] = off[r][u] + C[u];
      vector<u32> *target;
      vector<u32> tmp;
      if (r + 1 < T) {
        tmp = S;
        sort(tmp.begin(), tmp.end());
        tmp.erase(unique(tmp.begin(), tmp.end()), tmp.end());
        alive[r + 1] = std::move(tmp);
        target = &alive[r + 1];
        nodes += alive[r + 1].size();
      } else
        target = &alive[0];
      vector<u32> no(nn + 1, 0), nd;
      nd.reserve(S.size());
      for (size_t u = 0; u < nn; u++) {
        for (u32 ee = off[r][u]; ee < off[r][u + 1]; ee++) {
          auto it = lower_bound(target->begin(), target->end(), S[ee]);
          if (it != target->end() && *it == S[ee]) nd.push_back((u32)(it - target->begin()));
        }
        no[u + 1] = (u32)nd.size();
      }
      off[r] = std::move(no);
      dst[r] = std::move(nd);
      if (nodes + alive[0].size() > ncap) capped = true;
    }
    if (capped) {
      R.lastLevel = K;
      R.maxNodes = max(R.maxNodes, nodes);
      return R;
    }
    // trim to the bi-infinite core
    for (int round = 0; round < 200; round++) {
      vector<vector<char>> keep(T);
      for (int r = 0; r < T; r++) keep[r].assign(alive[r].size(), 1);
      for (int r = T - 1; r >= 0; r--) {
        int nx = (r + 1) % T;
        for (size_t u = 0; u < alive[r].size(); u++) {
          char ok = 0;
          for (u32 ee = off[r][u]; ee < off[r][u + 1]; ee++)
            if (keep[nx][dst[r][ee]]) {
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
            for (u32 ee = off[r][u]; ee < off[r][u + 1]; ee++) has[dst[r][ee]] = 1;
        for (size_t v = 0; v < has.size(); v++)
          if (!has[v]) keep[nx][v] = 0;
      }
      bool changed = false;
      vector<vector<u32>> mp(T);
      for (int r = 0; r < T; r++) {
        mp[r].assign(alive[r].size(), EMP);
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
            for (u32 ee = off[r][u]; ee < off[r][u + 1]; ee++)
              if (keep[nx][dst[r][ee]]) nd.push_back(mp[nx][dst[r][ee]]);
            no.push_back((u32)nd.size());
          }
        alive[r] = std::move(na);
        off[r] = std::move(no);
        dst[r] = std::move(nd);
      }
    }
    // exact: states on a closed walk of length exactly T
    vector<u64> base0(T + 1, 0);
    for (int r = 0; r < T; r++) base0[r + 1] = base0[r] + alive[r].size();
    const u64 Ntot = base0[T];
    R.maxNodes = max(R.maxNodes, Ntot);
    vector<u8> inE(Ntot, 0);
    const size_t N0 = alive[0].size();
    if (N0 > 0 && Ntot > 0) {
      vector<u64> F(Ntot, 0), B(Ntot, 0);
      vector<vector<u32>> fr(T);
      for (size_t lo = 0; lo < N0; lo += 64) {
        size_t hi = min(N0, lo + 64);
        for (auto &x : fr) x.clear();
        for (size_t i = lo; i < hi; i++) {
          fr[0].push_back((u32)i);
          F[i] = 1ULL << (i - lo);
        }
        for (int r = 0; r + 1 < T; r++) {
          for (u32 u : fr[r]) {
            u64 f = F[base0[r] + u];
            for (u32 ee = off[r][u]; ee < off[r][u + 1]; ee++) {
              u32 v = dst[r][ee];
              u64 ix = base0[r + 1] + v;
              if (F[ix] == 0) fr[r + 1].push_back(v);
              F[ix] |= f;
            }
          }
        }
        for (int r = T - 1; r >= 0; r--) {
          for (u32 u : fr[r]) {
            u64 ix = base0[r] + u, bv = 0;
            for (u32 ee = off[r][u]; ee < off[r][u + 1]; ee++) {
              u32 v = dst[r][ee];
              if (r == T - 1) {
                if (v >= lo && v < hi) bv |= 1ULL << (v - lo);
              } else
                bv |= B[base0[r + 1] + v];
            }
            B[ix] = bv;
            if (F[ix] & bv) inE[ix] = 1;
          }
        }
        for (int r = 0; r < T; r++)
          for (u32 u : fr[r]) {
            u64 ix = base0[r] + u;
            F[ix] = B[ix] = 0;
          }
      }
    }
    vector<Lay> New(T);
    u64 total = 0;
    for (int r = 0; r < T; r++) {
      int l = (anchor + r) % T;
      Lay &L = New[l];
      for (size_t u = 0; u < alive[r].size(); u++)
        if (inE[base0[r] + u]) {
          u32 idx = alive[r][u], pi = idx / BS, v = idx % BS;
          if (Kp) L.cells.insert(L.cells.end(), P_[l].cells.begin() + (size_t)pi * Kp, P_[l].cells.begin() + (size_t)(pi + 1) * Kp);
          L.cells.push_back((u8)v);
          L.n++;
          total++;
        }
    }
    P_ = std::move(New);
    R.lastLevel = K;
    R.kept = total;
    if (verbose) {
      printf("  level %d kept %llu nodes %llu\n", K, (unsigned long long)total, (unsigned long long)Ntot);
      fflush(stdout);
    }
    if (total == 0) {
      R.death = K;
      return R;
    }
    double sec = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    if (sec > seccap) return R;
  }
  return R;
}

// genuine addition versus (R1)-(R3)
static void selftest(u64 seed, long count) {
  mt19937_64 rng(seed);
  long tests = 0;
  for (long it = 0; it < count; it++) {
    int n = 8 + rng() % 200;
    vector<int> d(n);
    for (int i = 0; i < n; i++) d[i] = rng() % 10;
    if (d[n - 1] == 0) d[n - 1] = 1;
    if (d[0] == 0) d[0] = 1;
    // pair word x_i = d_i + d_{n-1-i}
    int h = (n + 1) / 2;
    vector<int> x(n);
    for (int i = 0; i < n; i++) x[i] = d[i] + d[n - 1 - i];
    // genuine next number
    vector<int> res(n + 1);
    int carry = 0;
    for (int i = 0; i < n; i++) {
      int s = d[i] + d[n - 1 - i] + carry;
      res[i] = s % b;
      carry = (s >= b);
    }
    res[n] = carry;
    int n2 = n + carry, g = carry;
    vector<int> x2(n2);
    for (int i = 0; i < n2; i++) x2[i] = res[i] + res[n2 - 1 - i];
    // L_i ascending, H_i : carry out of the digit at mirror position n-1-i ( H_0 = overflow ), recursion downward from the middle
    vector<int> Lc(n + 2, 0), Hc(n + 2, 0);
    for (int i = 0; i < n; i++) Lc[i + 1] = (x[i] + Lc[i]) >= b;
    // H_i = carry out of position n-1-i = Lc[n-i]
    for (int i = 0; i <= n; i++) Hc[i] = Lc[n - i];
    if (Hc[0] != g) die("selftest overflow");
    for (int i = 0; i + 1 < h; i++) {
      // R1
      if (Hc[i] != (x[i] + Hc[i + 1]) / b) die("selftest R1");
      // R3
      int val = (x[i] + Lc[i]) % b + (g ? (i == 0 ? 1 : (x[i - 1] + Hc[i]) % b) : (x[i] + Hc[i + 1]) % b);
      if (val != x2[i]) die("selftest R3");
      tests++;
    }
  }
  printf("selftest PASS: %ld random numbers, %ld column checks of (R1),(R3) against genuine addition\n", count, tests);
}

int main(int argc, char **argv) {
  if (argc < 2) die("usage");
  string mode = argv[1];
  if (mode == "selftest") {
    selftest(strtoull(argv[2], 0, 10), atol(argv[3]));
    return 0;
  }
  string G = argv[2];
  P = (int)G.size();
  gP.resize(P);
  for (int i = 0; i < P; i++) gP[i] = G[i] - '0';
  if (mode == "if") {
    int d = atoi(argv[3]), a0;
    auto v = saturate(d, a0);
    printf("g=%s d=%d |IF|=%zu a0=%d\n", G.c_str(), d, v.size(), a0);
    return 0;
  }
  if (mode == "root") {
    int L = atoi(argv[3]), kmax = atoi(argv[4]);
    Iface r = root_iface(L);
    auto R = run_tower(r, L, kmax, 2000000000ULL, 1e18, true);
    printf("root tower g=%s L=%d: death level %d (last level %d, kept %llu)\n", G.c_str(), L, R.death, R.lastLevel, (unsigned long long)R.kept);
    return 0;
  }
  int d = atoi(argv[3]), L = atoi(argv[4]);
  int a0;
  auto IF = saturate(d, a0);
  printf("g=%s d=%d L=%d |IF|=%zu a0=%d\n", G.c_str(), d, L, IF.size(), a0);
  fflush(stdout);
  unordered_set<string> distinct;
  unordered_set<string> classes;
  for (const Iface &I : IF) {
    enum_cols(I, L, [&](const vector<int> &v) {
      bool dper = true;
      for (int t = 0; t < L; t++)
        if (v[t] != v[(t + d) % L]) {
          dper = false;
          break;
        }
      if (dper) return;
      Iface J;
      if (!extend(I, v, L, J)) die("closed L-column with empty A'");
      string k = ikey(J);
      if (distinct.insert(k).second) classes.insert(rotkey(J));
    });
  }
  printf("births: distinct interfaces %zu, rotation classes %zu\n", distinct.size(), classes.size());
  fflush(stdout);
  if (mode == "births") return 0;
  unordered_set<string>().swap(distinct);
  int nth = atoi(argv[5]);
  u64 ncap = strtoull(argv[6], 0, 10);
  double sec = atof(argv[7]);
  int kmax = atoi(argv[8]);
  long sample = argc > 9 ? atol(argv[9]) : 0;
  long only = argc > 10 ? atol(argv[10]) : -1;
  vector<string> list(classes.begin(), classes.end());
  sort(list.begin(), list.end());
  unordered_set<string>().swap(classes);
  if (sample > 0 && sample < (long)list.size()) {
    mt19937_64 rng(12345);
    shuffle(list.begin(), list.end(), rng);
    list.resize(sample);
  }
  if (only >= 0) {
    Iface I = from_rotkey(list[only], L);
    auto R = run_tower(I, L, kmax, ncap, sec, true);
    printf("single tower %ld: death level %d (last level %d kept %llu maxNodes %llu)\n", only, R.death, R.lastLevel, (unsigned long long)R.kept, (unsigned long long)R.maxNodes);
    return 0;
  }
  atomic<size_t> next_(0);
  mutex mu;
  map<int, long> hist;
  long done = 0, cappedN = 0;
  int maxd = 0;
  auto start = chrono::steady_clock::now();
  vector<thread> th;
  for (int i = 0; i < nth; i++)
    th.emplace_back([&]() {
      for (;;) {
        size_t k = next_.fetch_add(1);
        if (k >= list.size()) break;
        Iface I = from_rotkey(list[k], L);
        auto R = run_tower(I, L, kmax, ncap, sec);
        lock_guard<mutex> lk(mu);
        done++;
        if (R.death >= 0) {
          hist[R.death]++;
          if (R.death > maxd) maxd = R.death;
        } else {
          cappedN++;
          string pr;
          for (int t = 0; t < min(L, 8); t++) pr += to_string((int)I.xb[t]) + ",";
          printf("CAPPED k=%zu last level %d kept %llu maxNodes %llu xb(first)=%s\n", k, R.lastLevel, (unsigned long long)R.kept, (unsigned long long)R.maxNodes, pr.c_str());
          fflush(stdout);
        }
        if (done % 50000 == 0) {
          double s = chrono::duration<double>(chrono::steady_clock::now() - start).count();
          printf("progress %ld/%zu capped %ld maxdeath %d t=%.0fs\n", done, list.size(), cappedN, maxd, s);
          fflush(stdout);
        }
      }
    });
  for (auto &x : th) x.join();
  printf("towers run %ld, die %ld, capped %ld, max death level %d\n", done, done - cappedN, cappedN, maxd);
  printf("death level histogram (level:count, first 30):");
  int cnt = 0;
  for (auto &kv : hist) {
    if (cnt++ < 30) printf(" %d:%ld", kv.first, kv.second);
  }
  printf("\n");
  long tot = 0;
  for (auto &kv : hist) tot += kv.first * kv.second;
  printf("sum of death levels %ld (a fingerprint of the distribution)\n", tot);
  return 0;
}
