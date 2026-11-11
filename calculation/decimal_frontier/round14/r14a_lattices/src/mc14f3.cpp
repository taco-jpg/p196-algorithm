// mc14f.cpp (r14a): family-wide all-period closure over interface-graph edges.
// State = (t mod 8, par, e, w): w = K-window, e = edge (I, v) of the family: I = interface of the columns below the frame, v = the column at the frame (pending).
// Input: family file produced by famexport.py: "nE" then per edge: I J tag v[8] c[8] xb[8] A[8].
//   c[t] = forward carry into the window bottom; xb[t] = value of the column just below the frame at time t (only used when g_t = 1);
//   A[t] = mask of admissible carries b0 leaving the window bottom (bit h: carry h allowed).
// Rule (R_K^F, top relaxation, like mc13c rk_succ with lattice tables replaced by interface data):
//   e_i, a: ascending carries from a_0 = c[t]; r_i: descending with Din in {0,1}; b_out leaves cell 0; need A[t] >> b_out & 1.
//   g_t = 0: w'_i = e_i + r_i.  g_t = 1, par = 1 (no shift): w'_0 = e_0 + hi, w'_i = e_i + r_{i-1}.  g_t = 1, par = 0 (frame shift): leaving cell e_0 + hi must equal v(t+1);
//   w'_i = e_{i+1} + r_i, top cell = topv + r_{K-1}, topv free in 0..9, and the edge moves to any out-edge of J.
//   hi = (xb[t] + b_out) mod 10.  accepting: w_0 != v(t).
// Exact fold step: as mc13c exact_step with Din = a_h (par = 0) or a_{h-1} (par = 1).
#include <mach/mach.h>
#include <sys/resource.h>
#include <unistd.h>
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
#include <string>
#include <thread>
#include <vector>
using namespace std;
typedef uint8_t u8;
typedef uint32_t u32;
typedef uint64_t u64;
#define MAXK 256
static const int TP = 8, BASE = 10, BS = 19;
static const int GG[8] = {1, 0, 1, 0, 1, 0, 1, 0};

static double rss_gb() {
  mach_task_basic_info info;
  mach_msg_type_number_t count = MACH_TASK_BASIC_INFO_COUNT;
  if (task_info(mach_task_self(), MACH_TASK_BASIC_INFO, (task_info_t)&info, &count) != KERN_SUCCESS) return -1;
  return (double)info.resident_size / (1024.0 * 1024.0 * 1024.0);
}
static double peak_gb = 0;
static void start_watchdog() {
  const char *a = getenv("R14_RSS_GB");
  const char *b = getenv("R14_SEC");
  double cap = a ? atof(a) : 30.0;
  double sec = b ? atof(b) : 1e12;
  auto t0 = chrono::steady_clock::now();
  thread([cap, sec, t0]() {
    for (;;) {
      this_thread::sleep_for(chrono::seconds(2));
      double r = rss_gb();
      if (r > peak_gb) peak_gb = r;
      double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
      if (r > cap) {
        printf("# BUDGET RSS cap hit: rss %.1f GB > cap %.1f GB at %.0f s: UNDECIDED\n", r, cap, el);
        fflush(stdout);
        _exit(9);
      }
      if (el > sec) {
        printf("# BUDGET time cap hit: %.0f s, rss %.1f GB: UNDECIDED\n", el, r);
        fflush(stdout);
        _exit(10);
      }
    }
  }).detach();
}
static void die(const char *s) {
  fprintf(stderr, "FATAL %s\n", s);
  exit(3);
}

struct Edge {
  int I, J, tag;
  u8 v[8], c[8], xb[8], A[8];
  int rinv, comp;  // image edges under R^{-1} and C (-1 if not available)
  vector<int> nxt;
};
static vector<Edge> ED;
static int nE, nL;
static bool useCarve = false;  // keep only SCCs that contain a layer with tag 0
static int TM = 8;  // slices = time mod TM (canonical representatives may shift time by the group's time rotation)
static int phaseClass = 0;  // 0 = all (t,par), 1 = class A, 2 = class B
static inline bool inClass(int t, int par) {
  static const int A[8] = {0, 1, 1, 0, 0, 1, 1, 0};  // class A: par = A[t]
  bool a = (par == A[t]);
  return phaseClass == 0 ? true : (phaseClass == 1 ? a : !a);
}

static void read_family(const char *fn) {
  FILE *f = fopen(fn, "r");
  if (!f) die("open family");
  if (fscanf(f, "%d", &nE) != 1) die("hdr");
  ED.resize(nE);
  for (int e = 0; e < nE; e++) {
    Edge &E = ED[e];
    int x;
    if (fscanf(f, "%d %d %d %d %d", &E.I, &E.J, &E.tag, &E.rinv, &E.comp) != 5) die("edge hdr");
    for (int t = 0; t < 8; t++) { if (fscanf(f, "%d", &x) != 1) die("v"); E.v[t] = (u8)x; }
    for (int t = 0; t < 8; t++) { if (fscanf(f, "%d", &x) != 1) die("c"); E.c[t] = (u8)x; }
    for (int t = 0; t < 8; t++) { if (fscanf(f, "%d", &x) != 1) die("xb"); E.xb[t] = (u8)x; }
    for (int t = 0; t < 8; t++) { if (fscanf(f, "%d", &x) != 1) die("A"); E.A[t] = (u8)x; }
  }
  fclose(f);
  for (int e = 0; e < nE; e++) {
    for (int e2 = 0; e2 < nE; e2++)
      if (ED[e2].I == ED[e].J) ED[e].nxt.push_back(e2);
    if (ED[e].nxt.empty() || ED[e].nxt.size() > 2) die("out-degree not 1..2");
  }
  nL = nE * 16;
}

static inline int layerid(int e, int t, int par) { return e * 16 + t * 2 + par; }
// symmetry: group elements g = (r, c): r in Rset (time shift by 2r), c complement.  Action on layers:
//   g(e,t,par) = (Rinv^r(C^c e), t + 2r, par); on windows: complement if c.
static int useSym = 0;
struct GEl { int r, c; };
static vector<GEl> group;
static vector<int> canonL;                 // canonical layer of a layer
static vector<array<u8, 2>> canonFlags;    // for each layer: [nflags, flagmask] (bit f set if element with complement flag f maps the layer to its canonical layer)
static inline int layer_image(int l, const GEl &g) {
  int e = l >> 4, t = (l >> 1) & 7, par = l & 1;
  if (g.c) { e = ED[e].comp; if (e < 0) return -1; }
  for (int k = 0; k < g.r; k++) { e = ED[e].rinv; if (e < 0) return -1; }
  return layerid(e, (t + 2 * g.r) % 8, par);
}
static void setup_symmetry() {
  int phaseClassLocal = (phaseClass ? 1 : 0);
  vector<int> rs;
  if (phaseClassLocal) rs = {0, 2}; else rs = {0, 1, 2, 3};
  // candidate elements; keep the subgroup preserving the family
  group.clear();
  for (int r : rs)
    for (int c = 0; c < 2; c++) {
      GEl g{r, c};
      bool ok = true;
      for (int l = 0; l < nL && ok; l++)
        if (layer_image(l, g) < 0) ok = false;
      if (ok) group.push_back(g);
    }
  { int r_any_odd = 0, r_any_nz = 0; for (const GEl &g : group) { if (g.r % 2) r_any_odd = 1; if (g.r) r_any_nz = 1; } TM = r_any_odd ? 2 : (r_any_nz ? 4 : 8); }
  printf("# symmetry group elements kept: %zu, slice modulus TM=%d\n", group.size(), TM);
  canonL.assign(nL, 0);
  canonFlags.assign(nL, {0, 0});
  for (int l = 0; l < nL; l++) {
    int best = l;
    for (const GEl &g : group) { int im = layer_image(l, g); if (im < best) best = im; }
    canonL[l] = best;
    u8 mask = 0;
    for (const GEl &g : group) if (layer_image(l, g) == best) mask |= (1 << g.c);
    canonFlags[l][1] = mask;
  }
}
// canonical window (K cells) for an actual layer l: lexicographic min over allowed complement flags
static inline void canon_window(int l, const u8 *w, int K, u8 *cw) {
  u8 mask = canonFlags[l][1];
  if (mask == 1) { memcpy(cw, w, K); return; }
  if (mask == 2) { for (int i = 0; i < K; i++) cw[i] = (u8)(18 - w[i]); return; }
  // both flags allowed: take the lexicographically smaller of w and its complement
  bool useComp = false;
  for (int i = 0; i < K; i++) {
    int a = w[i], b = 18 - w[i];
    if (a < b) { useComp = false; break; }
    if (a > b) { useComp = true; break; }
  }
  if (useComp) { for (int i = 0; i < K; i++) cw[i] = (u8)(18 - w[i]); }
  else memcpy(cw, w, K);
}

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

static int NTH = 8;
static void pfor(size_t n, const function<void(size_t)> &f) {
  atomic<size_t> nxt(0);
  vector<thread> th;
  for (int i = 0; i < NTH; i++)
    th.emplace_back([&]() {
      for (;;) {
        size_t k = nxt.fetch_add(1);
        if (k >= n) break;
        f(k);
      }
    });
  for (auto &x : th) x.join();
}

struct LG {
  vector<u32> alive;     // candidate ids, sorted
  int m = 0;             // number of successor slots
  int nl[2];             // next layers (canonical if useSym)
  int actual[2];         // actual next layers
  vector<u32> off[2];    // size alive.size()+1
  vector<u32> dst[2];    // edges (target candidate id, later target index)
};

struct NI { int m; int nl[2]; int actual[2]; };
static vector<NI> nextInfo;
static vector<vector<array<int, 2>>> incoming;
// One-step data of a window at layer (e,t,par).
struct StepCtx {
  int e, t, par, g, dh, tn, parn;
};
static inline StepCtx ctx_of(int l) {
  StepCtx c;
  c.e = l >> 4;
  c.t = (l >> 1) & 7;
  c.par = l & 1;
  c.g = GG[c.t];
  c.dh = (c.g == 1 && c.par == 0);
  c.tn = (c.t + 1) & 7;
  c.parn = c.par ^ c.g;
  return c;
}

// exact fold step F_K (returns false when the carry leaving the window is inadmissible or the leaving cell mismatches).  Next layer(s) are given by the caller.
static inline bool exact_step(int l, const u8 *w, int K, u8 *nw) {
  const StepCtx c = ctx_of(l);
  const Edge &E = ED[c.e];
  int e[MAXK], r[MAXK], a = E.c[c.t], topin = 0;
  for (int i = 0; i < K; i++) {
    if (i == K - 1) topin = a;
    int s = w[i] + a;
    e[i] = s % BASE;
    a = (s >= BASE);
  }
  int Din = (c.par == 0) ? a : topin;
  int b = Din;
  for (int i = K - 1; i >= 0; i--) {
    int s = w[i] + b;
    r[i] = s % BASE;
    b = (s >= BASE);
  }
  if (!((E.A[c.t] >> b) & 1)) return false;
  int hi = c.g ? (E.xb[c.t] + b) % BASE : 0;
  if (c.dh) {
    if (e[0] + hi != E.v[c.tn]) return false;
    for (int i = 0; i < K - 1; i++) nw[i] = (u8)(e[i + 1] + r[i]);
    nw[K - 1] = (u8)(2 * r[K - 1]);
  } else if (c.g == 0) {
    for (int i = 0; i < K; i++) nw[i] = (u8)(e[i] + r[i]);
  } else {
    int prev = hi;
    for (int i = 0; i < K; i++) {
      nw[i] = (u8)(e[i] + prev);
      prev = r[i];
    }
  }
  return true;
}

static void setup_next() {
  nextInfo.assign(nL, NI());
  incoming.assign(nL, {});
  for (int l = 0; l < nL; l++) {
    StepCtx c = ctx_of(l);
    NI &x = nextInfo[l];
    const Edge &E = ED[c.e];
    x.m = c.dh ? (int)E.nxt.size() : 1;
    for (int s = 0; s < x.m; s++) {
      int e2 = c.dh ? E.nxt[s] : c.e;
      int actual = layerid(e2, c.tn, c.parn);
      x.actual[s] = actual;
      x.nl[s] = useSym ? canonL[actual] : actual;
    }
  }
  for (int l = 0; l < nL; l++) {
    const NI &x = nextInfo[l];
    for (int s = 0; s < x.m; s++) incoming[x.nl[s]].push_back({l, s});
  }
}


// candidates of layer l: at the first time slice (tau == 0) all (parent, v); at later slices the targets coming from the previous slice.
static void gen_layer2(int l, int K, const vector<Lay> &P, vector<LG> &GG, int tau) {
  const StepCtx c = ctx_of(l);
  const Edge &E = ED[c.e];
  const int Kp = K - 1;
  LG &G = GG[l];
  const NI &ni = nextInfo[l];
  G.m = ni.m;
  for (int s = 0; s < G.m; s++) {
    G.nl[s] = ni.nl[s];
    G.actual[s] = ni.actual[s];
    G.off[s].clear();
    G.off[s].push_back(0);
    G.dst[s].clear();
  }
  G.alive.clear();
  const Lay &PL = P[l];
  if (tau == 0) {
    if (PL.n) {
      G.alive.resize((size_t)PL.n * BS);
      iota(G.alive.begin(), G.alive.end(), 0u);
    }
  } else {
    vector<u32> all;
    for (const auto &pr : incoming[l]) {
      const LG &S = GG[pr[0]];
      if (pr[1] < S.m) all.insert(all.end(), S.dst[pr[1]].begin(), S.dst[pr[1]].end());
    }
    sort(all.begin(), all.end());
    all.erase(unique(all.begin(), all.end()), all.end());
    G.alive = std::move(all);
  }
  if (G.alive.empty()) return;
  u8 w[MAXK], nw[MAXK];
  int ee[MAXK], r[MAXK];
  vector<u32> tg[2];
  for (size_t ci = 0; ci < G.alive.size(); ci++) {
    u32 id = G.alive[ci], p = id / BS;
    int v = id % BS;
    if (Kp) memcpy(w, &PL.cells[(size_t)p * Kp], Kp);
    w[Kp] = (u8)v;
    int a = E.c[c.t];
    for (int i = 0; i < K; i++) {
      int s = w[i] + a;
      ee[i] = s % BASE;
      a = (s >= BASE);
    }
    tg[0].clear();
    tg[1].clear();
    for (int Din = 0; Din < 2; Din++) {
      int b = Din;
      for (int i = K - 1; i >= 0; i--) {
        int s = w[i] + b;
        r[i] = s % BASE;
        b = (s >= BASE);
      }
      if (!((E.A[c.t] >> b) & 1)) continue;
      int hi = c.g ? (E.xb[c.t] + b) % BASE : 0;
      u8 tops[16];
      int nt;
      if (c.dh) {
        if (ee[0] + hi != E.v[c.tn]) continue;
        for (int i = 0; i < K - 1; i++) nw[i] = (u8)(ee[i + 1] + r[i]);
        for (int q = 0; q < BASE; q++) tops[q] = (u8)(q + r[K - 1]);
        nt = BASE;
      } else if (c.g == 0) {
        for (int i = 0; i < K - 1; i++) nw[i] = (u8)(ee[i] + r[i]);
        tops[0] = (u8)(ee[K - 1] + r[K - 1]);
        nt = 1;
      } else {
        int prev = hi;
        for (int i = 0; i < K; i++) {
          int val = ee[i] + prev;
          prev = r[i];
          if (i < K - 1)
            nw[i] = (u8)val;
          else
            tops[0] = (u8)val;
        }
        nt = 1;
      }
      for (int s = 0; s < G.m; s++) {
        const Lay &PN = P[G.nl[s]];
        if (!useSym) {
          long q = (Kp == 0) ? (PN.n ? 0 : -1) : lookup(PN, nw, Kp);
          if (q < 0) continue;
          for (int z = 0; z < nt; z++) tg[s].push_back((u32)q * BS + tops[z]);
        } else {
          u8 full[MAXK], cw[MAXK];
          if (Kp) memcpy(full, nw, Kp);
          for (int z = 0; z < nt; z++) {
            full[Kp] = tops[z];
            canon_window(G.actual[s], full, K, cw);
            long q = (Kp == 0) ? (PN.n ? 0 : -1) : lookup(PN, cw, Kp);
            if (q < 0) continue;
            tg[s].push_back((u32)q * BS + cw[Kp]);
          }
        }
      }
    }
    for (int s = 0; s < G.m; s++) {
      sort(tg[s].begin(), tg[s].end());
      tg[s].erase(unique(tg[s].begin(), tg[s].end()), tg[s].end());
      G.dst[s].insert(G.dst[s].end(), tg[s].begin(), tg[s].end());
      G.off[s].push_back((u32)G.dst[s].size());
    }
  }
}

// R_K^F successors of the candidate (p, v) at layer l: per slot, sorted unique target candidate ids
static void gen_layer(int l, int K, const vector<Lay> &P, LG &G) {
  const StepCtx c = ctx_of(l);
  const Edge &E = ED[c.e];
  const int Kp = K - 1;
  G.m = c.dh ? (int)E.nxt.size() : 1;
  for (int s = 0; s < G.m; s++) {
    int e2 = c.dh ? E.nxt[s] : c.e;
    int actual = layerid(e2, c.tn, c.parn);
    G.actual[s] = actual;
    G.nl[s] = useSym ? canonL[actual] : actual;
    G.off[s].clear();
    G.off[s].push_back(0);
    G.dst[s].clear();
  }
  G.alive.clear();
  const Lay &PL = P[l];
  if (PL.n == 0) return;
  u8 w[MAXK], nw[MAXK];
  int ee[MAXK], r[MAXK];
  vector<u32> tg[2];
  for (u32 p = 0; p < PL.n; p++) {
    if (Kp) memcpy(w, &PL.cells[(size_t)p * Kp], Kp);
    for (int v = 0; v < BS; v++) {
      w[Kp] = (u8)v;
      // ascending part
      int a = E.c[c.t];
      for (int i = 0; i < K; i++) {
        int s = w[i] + a;
        ee[i] = s % BASE;
        a = (s >= BASE);
      }
      tg[0].clear();
      tg[1].clear();
      for (int Din = 0; Din < 2; Din++) {
        int b = Din;
        for (int i = K - 1; i >= 0; i--) {
          int s = w[i] + b;
          r[i] = s % BASE;
          b = (s >= BASE);
        }
        if (!((E.A[c.t] >> b) & 1)) continue;
        int hi = c.g ? (E.xb[c.t] + b) % BASE : 0;
        u8 tops[16];
        int nt;
        if (c.dh) {
          if (ee[0] + hi != E.v[c.tn]) continue;
          for (int i = 0; i < K - 1; i++) nw[i] = (u8)(ee[i + 1] + r[i]);
          for (int q = 0; q < BASE; q++) tops[q] = (u8)(q + r[K - 1]);
          nt = BASE;
        } else if (c.g == 0) {
          for (int i = 0; i < K - 1; i++) nw[i] = (u8)(ee[i] + r[i]);
          tops[0] = (u8)(ee[K - 1] + r[K - 1]);
          nt = 1;
        } else {
          int prev = hi;
          for (int i = 0; i < K; i++) {
            int val = ee[i] + prev;
            prev = r[i];
            if (i < K - 1)
              nw[i] = (u8)val;
            else
              tops[0] = (u8)val;
          }
          nt = 1;
        }
        for (int s = 0; s < G.m; s++) {
          const Lay &PN = P[G.nl[s]];
          if (!useSym) {
            long q = (Kp == 0) ? (PN.n ? 0 : -1) : lookup(PN, nw, Kp);
            if (q < 0) continue;
            for (int z = 0; z < nt; z++) tg[s].push_back((u32)q * BS + tops[z]);
          } else {
            u8 full[MAXK], cw[MAXK];
            if (Kp) memcpy(full, nw, Kp);
            for (int z = 0; z < nt; z++) {
              full[Kp] = tops[z];
              canon_window(G.actual[s], full, K, cw);
              long q = (Kp == 0) ? (PN.n ? 0 : -1) : lookup(PN, cw, Kp);
              if (q < 0) continue;
              tg[s].push_back((u32)q * BS + cw[Kp]);
            }
          }
        }
      }
      bool any = false;
      for (int s = 0; s < G.m; s++) {
        sort(tg[s].begin(), tg[s].end());
        tg[s].erase(unique(tg[s].begin(), tg[s].end()), tg[s].end());
        if (!tg[s].empty()) any = true;
      }
      if (!any) continue;
      G.alive.push_back(p * BS + v);
      for (int s = 0; s < G.m; s++) {
        G.dst[s].insert(G.dst[s].end(), tg[s].begin(), tg[s].end());
        G.off[s].push_back((u32)G.dst[s].size());
      }
    }
  }
}

int main(int argc, char **argv) {
  start_watchdog();
  if (argc < 4) die("usage: mc14f2 FAM KMAX THREADS [carve] [phaseClass] [sym]");
  read_family(argv[1]);
  int Kmax = atoi(argv[2]);
  NTH = atoi(argv[3]);
  if (argc > 4 && atoi(argv[4]) == 1) useCarve = true;
  if (argc > 5) phaseClass = atoi(argv[5]);
  if (argc > 6) useSym = atoi(argv[6]);
  printf("# family edges %d layers %d carve %d threads %d phaseClass %d useSym %d\n", nE, nL, (int)useCarve, NTH, phaseClass, useSym);
  if (useSym) setup_symmetry();
  setup_next();
  fflush(stdout);
  vector<Lay> P(nL);
  for (int l = 0; l < nL; l++) { int t=(l>>1)&7, par=l&1; P[l].n = inClass(t, par) ? 1 : 0; if (useSym && canonL[l] != l) P[l].n = 0; }  // level 0: one empty window at every layer of the chosen phase class (canonical layers only if useSym)
  for (int K = 1; K <= Kmax; K++) {
    auto t0 = chrono::steady_clock::now();
    const int Kp = K - 1;
    if (Kp > 0) pfor(nL, [&](size_t l) { build_ht(P[l], Kp); });
    vector<LG> G(nL);
    for (int tau = 0; tau < TM; tau++) {
      vector<int> sl;
      for (int l = 0; l < nL; l++)
        if ((((l >> 1) & 7) % TM) == tau) sl.push_back(l);
      pfor(sl.size(), [&](size_t i) { gen_layer2(sl[i], K, P, G, tau); });
    }
    u64 candTotal = 0; for (int l = 0; l < nL; l++) candTotal += G[l].alive.size();
    // remap targets to indices in the next layer's alive list; drop dead targets
    pfor(nL, [&](size_t l) {
      LG &A = G[l];
      vector<u32> no[2], nd[2];
      for (int s = 0; s < A.m; s++) {
        const vector<u32> &tgtAlive = G[A.nl[s]].alive;
        no[s].assign(A.alive.size() + 1, 0);
        nd[s].reserve(A.dst[s].size());
      }
      for (int s = 0; s < A.m; s++) {
        const vector<u32> &tgtAlive = G[A.nl[s]].alive;
        for (size_t i = 0; i < A.alive.size(); i++) {
          for (u32 q = A.off[s][i]; q < A.off[s][i + 1]; q++) {
            auto it = lower_bound(tgtAlive.begin(), tgtAlive.end(), A.dst[s][q]);
            if (it != tgtAlive.end() && *it == A.dst[s][q]) nd[s].push_back((u32)(it - tgtAlive.begin()));
          }
          no[s][i + 1] = (u32)nd[s].size();
        }
      }
      for (int s = 0; s < A.m; s++) {
        A.off[s] = std::move(no[s]);
        A.dst[s] = std::move(nd[s]);
      }
    });
    // trim to the bi-infinite core: backward sweeps by time slice (deleted nodes propagate within one pass), then forward sweeps
    vector<vector<u8>> keep(nL);
    pfor(nL, [&](size_t l) { keep[l].assign(G[l].alive.size(), 1); });
    vector<int> sliceL[8];
    for (int l = 0; l < nL; l++) if (!G[l].alive.empty()) sliceL[((l >> 1) & 7) % TM].push_back(l);
    bool changed = true;
    int rounds = 0;
    while (changed && rounds < 1000) {
      changed = false;
      rounds++;
      for (int tau = TM - 1; tau >= 0; tau--) {
        atomic<bool> ch(false);
        pfor(sliceL[tau].size(), [&](size_t ii) {
          int l = sliceL[tau][ii];
          const LG &A = G[l];
          for (size_t i = 0; i < A.alive.size(); i++)
            if (keep[l][i]) {
              bool ok = false;
              for (int s = 0; s < A.m && !ok; s++)
                for (u32 q = A.off[s][i]; q < A.off[s][i + 1]; q++)
                  if (keep[A.nl[s]][A.dst[s][q]]) {
                    ok = true;
                    break;
                  }
              if (!ok) {
                keep[l][i] = 0;
                ch = true;
              }
            }
        });
        if (ch.load()) changed = true;
      }
      for (int tau = 0; tau < TM; tau++) {
        int prev = (tau + TM - 1) % TM;
        vector<vector<u8>> has(nL);
        for (int l : sliceL[tau]) has[l].assign(G[l].alive.size(), 0);
        pfor(sliceL[prev].size(), [&](size_t ii) {
          int l = sliceL[prev][ii];
          const LG &A = G[l];
          for (size_t i = 0; i < A.alive.size(); i++)
            if (keep[l][i])
              for (int s = 0; s < A.m; s++)
                for (u32 q = A.off[s][i]; q < A.off[s][i + 1]; q++)
                  if (keep[A.nl[s]][A.dst[s][q]]) __atomic_store_n(&has[A.nl[s]][A.dst[s][q]], (u8)1, __ATOMIC_RELAXED);
        });
        atomic<bool> ch(false);
        pfor(sliceL[tau].size(), [&](size_t ii) {
          int l = sliceL[tau][ii];
          for (size_t i = 0; i < keep[l].size(); i++)
            if (keep[l][i] && !has[l][i]) {
              keep[l][i] = 0;
              ch = true;
            }
        });
        if (ch.load()) changed = true;
      }
    }
    // compress to the kept nodes: renumber, global CSR
    vector<vector<u32>> newid(nL);
    vector<u64> base(nL + 1, 0);
    for (int l = 0; l < nL; l++) {
      newid[l].assign(G[l].alive.size(), EMPTYS);
      u32 c = 0;
      for (size_t i = 0; i < G[l].alive.size(); i++)
        if (keep[l][i]) newid[l][i] = c++;
      base[l + 1] = base[l] + c;
    }
    const u64 N = base[nL];
    if (N >= 0xFFFFFF00ULL) die("too many nodes");
    vector<u32> goff(N + 1, 0);
    vector<u64> ecount(nL, 0);
    vector<vector<u32>> ids(nL);
    for (int l = 0; l < nL; l++) {
      LG &A = G[l];
      ids[l].reserve(base[l + 1] - base[l]);
      for (size_t i = 0; i < A.alive.size(); i++)
        if (keep[l][i]) {
          ids[l].push_back(A.alive[i]);
          u32 deg = 0;
          for (int s = 0; s < A.m; s++)
            for (u32 q = A.off[s][i]; q < A.off[s][i + 1]; q++)
              if (keep[A.nl[s]][A.dst[s][q]]) deg++;
          goff[base[l] + newid[l][i]] = deg;  // temporarily the degree
        }
    }
    u64 totE = 0;
    for (u64 v = 0; v < N; v++) {
      u64 d = goff[v];
      goff[v] = (u32)totE;
      totE += d;
    }
    goff[N] = (u32)totE;
    if (totE >= 0xFFFFFF00ULL) die("too many edges");
    vector<u32> gdst(totE);
    for (int l = 0; l < nL; l++) {
      LG &A = G[l];
      for (size_t i = 0; i < A.alive.size(); i++)
        if (keep[l][i]) {
          u32 pos = goff[base[l] + newid[l][i]];
          for (int s = 0; s < A.m; s++)
            for (u32 q = A.off[s][i]; q < A.off[s][i + 1]; q++) {
              int nl = A.nl[s];
              u32 tgt = A.dst[s][q];
              if (keep[nl][tgt]) gdst[pos++] = (u32)(base[nl] + newid[nl][tgt]);
            }
        }
    }
    // accepting flags (bit 1) and tag flags (bit 2) per node
    vector<u8> flag(N, 0);
    u64 nacc0 = 0;
    for (int l = 0; l < nL; l++) {
      const StepCtx c = ctx_of(l);
      const Edge &E = ED[c.e];
      for (size_t i = 0; i < ids[l].size(); i++) {
        u32 id = ids[l][i], pi = id / BS, v = id % BS;
        int w0 = (Kp == 0) ? (int)v : P[l].cells[(size_t)pi * Kp];
        u8 fl = 0;
        if (w0 != E.v[c.t]) fl |= 1;
        if (E.tag) fl |= 2;
        flag[base[l] + i] = fl;
        if (fl & 1) nacc0++;
      }
    }
    // free the per-layer graphs before Tarjan
    vector<LG>().swap(G);
    vector<vector<u8>>().swap(keep);
    vector<vector<u32>>().swap(newid);
    // Tarjan SCC (iterative)
    vector<u8> kept(N, 0);
    u64 sccs = 0, keptN = 0;
    if (N) {
      vector<u32> idx(N, 0), low(N, 0), cur(N, 0);
      vector<u8> on(N, 0);
      vector<u32> S, D;
      u32 cnt = 0;
      for (u64 root = 0; root < N; root++) {
        if (idx[root]) continue;
        cnt++;
        idx[root] = low[root] = cnt;
        cur[root] = goff[root];
        S.push_back((u32)root);
        on[root] = 1;
        D.push_back((u32)root);
        while (!D.empty()) {
          u32 v = D.back();
          if (cur[v] < goff[v + 1]) {
            u32 w = gdst[cur[v]++];
            if (!idx[w]) {
              cnt++;
              idx[w] = low[w] = cnt;
              cur[w] = goff[w];
              S.push_back(w);
              on[w] = 1;
              D.push_back(w);
            } else if (on[w]) {
              low[v] = min(low[v], idx[w]);
            }
          } else {
            D.pop_back();
            if (!D.empty()) {
              u32 u = D.back();
              low[u] = min(low[u], low[v]);
            }
            if (low[v] == idx[v]) {
              // pop the SCC
              size_t start = S.size();
              do {
                start--;
              } while (S[start] != v);
              u64 sz = S.size() - start;
              u8 orf = 0;
              u8 allf = 3;
              for (size_t q = start; q < S.size(); q++) {
                orf |= flag[S[q]];
                allf &= flag[S[q]];
                on[S[q]] = 0;
              }
              // orf bit0: contains an accepting state; allf bit1: all layers tagged
              bool keepit = (sz >= 2) && (orf & 1) && !(useCarve && (allf & 2));
              if (keepit) {
                sccs++;
                for (size_t q = start; q < S.size(); q++) kept[S[q]] = 1;
                keptN += sz;
              }
              S.resize(start);
            }
          }
        }
      }
    }
    // new level sets
    vector<Lay> New(nL);
    u64 total = 0, naccK = 0, tagged = 0, weighted = 0;
    for (int l = 0; l < nL; l++) {
      Lay &L = New[l];
      const size_t nn = ids[l].size();
      for (size_t i = 0; i < nn; i++)
        if (kept[base[l] + i]) {
          u32 id = ids[l][i], pi = id / BS, v = id % BS;
          if (Kp) L.cells.insert(L.cells.end(), P[l].cells.begin() + (size_t)pi * Kp, P[l].cells.begin() + (size_t)(pi + 1) * Kp);
          L.cells.push_back((u8)v);
          L.n++;
          total++;
          if (flag[base[l] + i] & 1) naccK++;
          if (flag[base[l] + i] & 2) tagged++;
          if (useSym) {
            // orbit size of this quotient state: |G| / #{g : g layer = layer and g window = window}
            size_t pos = L.cells.size() - K;
            bool all9 = true;
            for (int a = 0; a < K; a++) if (L.cells[pos + a] != 9) { all9 = false; break; }
            int stab = 0;
            for (const GEl &g : group)
              if (layer_image(l, g) == l && (g.c == 0 || all9)) stab++;
            weighted += group.size() / stab;
          }
        }
    }
    vector<Lay>().swap(P);
    vector<vector<u32>>().swap(ids);
    vector<u32>().swap(goff);
    vector<u32>().swap(gdst);
    vector<u8>().swap(flag);
    vector<u8>().swap(kept);
    // exact fold orbits inside the kept sets: cycle detection on the exact-step graph (per state: 1 or 2 successors at frame shifts)
    u64 exactCycles = 0;
    if (total) {
      pfor(nL, [&](size_t l) { if (New[l].n) build_ht(New[l], K); });
      vector<u64> nb(nL + 1, 0);
      for (int l = 0; l < nL; l++) nb[l + 1] = nb[l] + New[l].n;
      const u64 NN = nb[nL];
      vector<u32> ex0(NN, EMPTYS), ex1(NN, EMPTYS);
      pfor(nL, [&](size_t l) {
        const Lay &L = New[l];
        if (L.n == 0) return;
        StepCtx c = ctx_of((int)l);
        const Edge &E = ED[c.e];
        u8 nw[MAXK];
        int m = c.dh ? (int)E.nxt.size() : 1;
        int nls[2];
        for (int s = 0; s < m; s++) {
          int actual = layerid(c.dh ? E.nxt[s] : c.e, c.tn, c.parn);
          nls[s] = actual;  // actual next layer; canonicalized below if useSym
        }
        for (u32 i = 0; i < L.n; i++) {
          if (!exact_step((int)l, &L.cells[(size_t)i * K], K, nw)) continue;
          for (int s = 0; s < m; s++) {
            int actual = nls[s];
            u8 cw[MAXK];
            const u8 *key = nw;
            int nl2 = actual;
            if (useSym) { nl2 = canonL[actual]; canon_window(actual, nw, K, cw); key = cw; }
            const Lay &LN = New[nl2];
            if (LN.n == 0) continue;
            long q = lookup(LN, key, K);
            if (q >= 0) {
              u32 tgt = (u32)(nb[nl2] + q);
              if (s == 0)
                ex0[nb[l] + i] = tgt;
              else
                ex1[nb[l] + i] = tgt;
            }
          }
        }
      });
      // DFS for cycles
      vector<u8> col(NN, 0);
      vector<u32> st, par_;
      int printed = 0;
      for (u64 r0 = 0; r0 < NN; r0++) {
        if (col[r0]) continue;
        st.clear();
        par_.clear();
        st.push_back((u32)r0);
        par_.push_back(EMPTYS);
        vector<u8> slot;
        slot.push_back(0);
        col[r0] = 1;
        while (!st.empty()) {
          u32 v = st.back();
          u8 &sl = slot.back();
          u32 w = EMPTYS;
          if (sl == 0) {
            w = ex0[v];
            sl = 1;
          } else if (sl == 1) {
            w = ex1[v];
            sl = 2;
          }
          if (sl <= 2 && w != EMPTYS) {
            if (col[w] == 1) {
              // cycle found: walk the current stack for reporting
              exactCycles++;
              if (printed < 8) {
                printed++;
                size_t z = st.size();
                while (z > 0 && st[z - 1] != w) z--;
                printf("# PERIODIC exact orbit K=%d cycle nodes %zu (node ids)", K, st.size() - z + 1);
                // print the states along the cycle: layer (e,t,par) and window of the first state
                for (size_t q = z - 1; q < st.size() && q - (z - 1) < 2; q++) {
                  u32 nodeid = st[q];
                  int layer = (int)(upper_bound(nb.begin(), nb.end(), (u64)nodeid) - nb.begin()) - 1;
                  u32 idx = (u32)(nodeid - nb[layer]);
                  string sw;
                  for (int a = 0; a < K; a++) sw += to_string((int)New[layer].cells[(size_t)idx * K + a]) + " ";
                  printf(" | layer e=%d t=%d par=%d win %s", layer >> 4, (layer >> 1) & 7, layer & 1, sw.c_str());
                }
                printf("\n");
                fflush(stdout);
              }
            } else if (col[w] == 0) {
              col[w] = 1;
              st.push_back(w);
              par_.push_back(v);
              slot.push_back(0);
            }
          } else if (sl >= 2) {
            col[v] = 2;
            st.pop_back();
            par_.pop_back();
            slot.pop_back();
          }
          // note: `sl` reference may dangle after push_back; we re-read at the next iteration
        }
      }
    }
    double sec = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    printf("K %d Eacc %llu accepting %llu layers-tag1 %llu sccs %llu exact %llu nodes %llu cand %llu time %.1f rss %.1f peak %.1f rounds %d weighted %llu\n", K, (unsigned long long)total, (unsigned long long)naccK, (unsigned long long)tagged, (unsigned long long)sccs, (unsigned long long)exactCycles, (unsigned long long)N, (unsigned long long)candTotal, sec, rss_gb(), peak_gb, rounds, (unsigned long long)weighted);
    fflush(stdout);
    P = std::move(New);
    if (total == 0) {
      printf("EMPTY at K=%d\n", K);
      fflush(stdout);
      break;
    }
  }
  return 0;
}
