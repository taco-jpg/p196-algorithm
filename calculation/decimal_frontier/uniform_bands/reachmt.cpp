// reachmt.cpp -- multi-threaded, memory-compact version of reach.cpp (same graph, same answers; decision only).
// A fit is reconstructed afterwards with ./reach (single-threaded, keeps parent pointers): BAND='c:r,..' PH=p ./reach ...
//
// Exact reachability over periodic left-end interfaces of ANY height (model: see reach.cpp). The reachable set depends
// only on (B, T, CLOCK), so one run checks every target at once:
//   ALL : every uniform absorbing band of base B (cycles of v -> 2((v+c) mod B), c=[v>=B], v != B-1) whose period
//         divides T, in every phase, AND the 9-wire condition (every stream).   <- use this
//   BAND: one band given by env BAND='c:r,...' and PH (stops at the first fit)
//   WIRE: 9-wire streams only
// Interfaces are packed into W 64-bit words (2T + 4*overflows bits); visited set = sharded open-addressing hash table.
// usage: [THREADS=n] ./reachmt B T CLOCK ALL|BAND|WIRE [cap] [maxdepth]
//        ./reachmt BATCH B ALL|WIRE cap  < lines "T CLOCK"
//        ./reachmt SWEEP B TMIN TMAX cap SHARD NSHARDS   every binary Lyndon word w (one clock per rotation class) and
//              every T = k|w| in [TMIN,TMAX], words with index = SHARD mod NSHARDS; prints only non-EMPTY tasks and a
//              per-T summary; ends with "SWEEP DONE".
// Output: "TARGET band[..] phase p REACHED at height H (BAND='..' PH=p)", "NEW STREAM at height H: ..",
//   "RESULT COMPLETE|EMPTY|TOO_BIG|MAXDEPTH|FIT ..".
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <cstdarg>
#include <string>
#include <vector>
#include <array>
#include <set>
#include <map>
#include <mutex>
#include <thread>
#include <atomic>
#include <chrono>
#include <algorithm>
#include <memory>
#include <iostream>
#include <sys/resource.h>
using namespace std;
typedef uint64_t u64; typedef unsigned __int128 u128;

static int B, T, NOV = 0; static int MODE = 0;  // 0 ALL, 1 BAND, 2 WIRE
static bool QUIET = false, BUFFER = false; static string OUTBUF;
static int ovf[64], OVI[64]; static u64 MASK; static int NBITS;
static int SB = 12, NS = 1 << 12;
// ROT=1: store one interface per orbit of the time shift by the clock period p (the root is fixed by it and the cell rule
// commutes with it, so the reachable set is a union of orbits; every target set used here is closed under the shift).
static bool ROT = false; static int ROTP = 0, ROTN = 1, ROTK = 0;

static void outf(const char* fmt, ...) {
  char buf[1024]; va_list ap; va_start(ap, fmt); vsnprintf(buf, sizeof(buf), fmt, ap); va_end(ap);
  if (BUFFER) OUTBUF += buf; else { fputs(buf, stdout); fflush(stdout); }
}

template <int W> struct Key { u64 w[W]; };
template <int W> static inline bool keq(const Key<W>& a, const Key<W>& b) { for (int i = 0; i < W; i++) if (a.w[i] != b.w[i]) return false; return true; }
template <int W> static inline bool kempty(const Key<W>& a) { for (int i = 0; i < W; i++) if (a.w[i] != ~0ULL) return false; return true; }
template <int W> static inline u64 khash(const Key<W>& k) {
  u64 h = 0x9E3779B97F4A7C15ULL;
  for (int i = 0; i < W; i++) { h ^= k.w[i] + 0x632BE59BD9B4E019ULL + (h << 6) + (h >> 2); h *= 0xBF58476D1CE4E5B9ULL; h ^= h >> 31; }
  h *= 0x94D049BB133111EBULL; h ^= h >> 29; return h;
}
static inline void setbits(u64* w, int pos, int len, u64 v) {  // len <= 64, v < 2^len
  int q = pos >> 6, o = pos & 63; w[q] |= v << o; if (o && o + len > 64) w[q + 1] |= v >> (64 - o);
}
static inline u64 getbits(const u64* w, int pos, int len) {
  int q = pos >> 6, o = pos & 63; u64 v = w[q] >> o; if (o && o + len > 64) v |= w[q + 1] << (64 - o);
  return len == 64 ? v : (v & ((1ULL << len) - 1));
}
template <int W> static inline Key<W> pack(u64 c, u64 d, u128 r) {
  Key<W> k; u64 tmp[W + 2]; memset(tmp, 0, sizeof(tmp));
  setbits(tmp, 0, T, c); setbits(tmp, T, T, d);
  int rb = 4 * NOV; setbits(tmp, 2 * T, min(rb, 64), (u64)r); if (rb > 64) setbits(tmp, 2 * T + 64, rb - 64, (u64)(r >> 64));
  memcpy(k.w, tmp, sizeof(k.w)); return k;
}
template <int W> static inline void unpack(const Key<W>& k, u64& c, u64& d, u128& r) {
  u64 tmp[W + 2]; memcpy(tmp, k.w, sizeof(k.w)); tmp[W] = tmp[W + 1] = 0;
  c = getbits(tmp, 0, T); d = getbits(tmp, T, T); int rb = 4 * NOV;
  r = getbits(tmp, 2 * T, min(rb, 64)); if (rb > 64) r |= (u128)getbits(tmp, 2 * T + 64, rb - 64) << 64;
}

template <int W> static inline bool kless(const Key<W>& a, const Key<W>& b) { for (int i = W - 1; i >= 0; i--) if (a.w[i] != b.w[i]) return a.w[i] < b.w[i]; return false; }
template <int W> static inline Key<W> canon(u64 c, u64 d, u128 r) {
  Key<W> best = pack<W>(c, d, r);
  u128 rmask = (4 * NOV >= 128) ? ~(u128)0 : (((u128)1 << (4 * NOV)) - 1);
  for (int s = 1; s < ROTN; s++) {
    int sh = s * ROTP, rs = 4 * s * ROTK;
    u64 c2 = ((c >> sh) | (c << (T - sh))) & MASK, d2 = ((d >> sh) | (d << (T - sh))) & MASK;
    u128 r2 = rs ? (((r >> rs) | (r << (4 * NOV - rs))) & rmask) : r;
    Key<W> k = pack<W>(c2, d2, r2); if (kless(k, best)) best = k;
  }
  return best;
}

// ---- targets
struct Target { u64 c; u128 r; string name; string spec; int ph; atomic<int> h{-1}; };
static vector<Target*> targets; static bool checkWire = false;
static void addBand(const vector<int>& vals, int ph) {  // vals: band values over its period
  int q = vals.size(); Target* g = new Target(); g->c = 0; g->r = 0; g->ph = ph;
  for (int t = 0; t < T; t++) {
    int v = vals[(t + ph) % q], cv = v >= B ? 1 : 0, rv = (v + cv) % B;
    g->c |= (u64)cv << t; if (ovf[t]) g->r |= (u128)rv << (4 * OVI[t]);
  }
  g->name = "band["; g->spec = "";
  for (int i = 0; i < q; i++) { int v = vals[i], cv = v >= B ? 1 : 0; g->name += to_string(v) + (i + 1 < q ? "," : "]"); g->spec += to_string(cv) + ":" + to_string((v + cv) % B) + (i + 1 < q ? "," : ""); }
  targets.push_back(g);
}
static vector<vector<int>> uniformCycles() {  // cycles of v -> 2((v + [v>=B]) mod B) avoiding the neutral value B-1
  vector<vector<int>> cyc; set<int> seenMin;
  auto f = [](int v) { int c = v >= B ? 1 : 0; return 2 * ((v + c) % B); };
  for (int v0 = 0; v0 <= 2 * B - 2; v0++) {
    int v = v0; for (int i = 0; i < 4 * B; i++) v = f(v);  // land on the cycle
    vector<int> cy; int u = v; bool bad = false;
    do { if (u == B - 1) bad = true; cy.push_back(u); u = f(u); } while (u != v && (int)cy.size() <= 2 * B);
    if (bad || u != v) continue;
    int mn = *min_element(cy.begin(), cy.end()); if (seenMin.count(mn)) continue; seenMin.insert(mn);
    rotate(cy.begin(), find(cy.begin(), cy.end(), mn), cy.end()); cyc.push_back(cy);
  }
  return cyc;
}
static atomic<u64> nAccept{0}; static mutex outMx; static atomic<bool> stopFit{false}; static set<u64> streams;
static void checkNew(u64 c, u64 d, u128 r, int height) {
  if (c == d) for (Target* g : targets) if (g->c == c && g->r == r) {
    nAccept++;
    int expect = -1;
    if (g->h.compare_exchange_strong(expect, height)) {
      lock_guard<mutex> lk(outMx);
      outf("  TARGET %s phase %d REACHED at height %d  (BAND='%s' PH=%d)\n", g->name.c_str(), g->ph, height, g->spec.c_str(), g->ph);
    }
    if (MODE == 1) stopFit = true;
  }
  if (checkWire && ((~c) & MASK) == d) {
    for (int t = 0; t < T; t++) if (ovf[t] && (int)((r >> (4 * OVI[t])) & 15) != (B - 1) * (int)((c >> t) & 1)) return;
    nAccept++;
    lock_guard<mutex> lk(outMx);
    if (!streams.count(c)) {
      streams.insert(c); string s; for (int t = 0; t < T; t++) s += (char)('0' + ((c >> t) & 1));
      outf("  NEW STREAM at height %d: %s\n", height, s.c_str());
    }
  }
}

// ---- visited set
template <int W> struct Shard { mutex m; Key<W>* keys = nullptr; u64 cap = 0, cnt = 0; };
template <int W> struct Table {
  vector<Shard<W>> sh; atomic<u64> total{0};
  Table() : sh(NS) { for (auto& s : sh) { s.cap = 64; s.keys = (Key<W>*)malloc(sizeof(Key<W>) * s.cap); memset(s.keys, 0xFF, sizeof(Key<W>) * s.cap); } }
  ~Table() { for (auto& s : sh) free(s.keys); }
  void grow(Shard<W>& s) {
    u64 nc = s.cap * 2; Key<W>* nk = (Key<W>*)malloc(sizeof(Key<W>) * nc);
    if (!nk) { fprintf(stderr, "out of memory\n"); printf("RESULT TOO_BIG: out of memory\n"); exit(3); }
    memset(nk, 0xFF, sizeof(Key<W>) * nc);
    for (u64 i = 0; i < s.cap; i++) if (!kempty(s.keys[i])) { u64 j = khash(s.keys[i]) & (nc - 1); while (!kempty(nk[j])) j = (j + 1) & (nc - 1); nk[j] = s.keys[i]; }
    free(s.keys); s.keys = nk; s.cap = nc;
  }
  bool insert(const Key<W>& k) {  // true if new
    u64 h = khash(k); Shard<W>& s = sh[h >> (64 - SB)];
    lock_guard<mutex> g(s.m);
    if ((s.cnt + 1) * 4 > s.cap * 3) grow(s);
    u64 j = h & (s.cap - 1);
    while (true) {
      if (kempty(s.keys[j])) { s.keys[j] = k; s.cnt++; total++; return true; }
      if (keq(s.keys[j], k)) return false;
      j = (j + 1) & (s.cap - 1);
    }
  }
};

template <int W> struct Expander {
  Table<W>* tab; vector<Key<W>>* out; int height;
  u64 cc, cd; u128 cr; int x0; bool root; u64 cs, ds; u128 rs;
  void leaf() {
    Key<W> k = ROT ? canon<W>(cs, ds, rs) : pack<W>(cs, ds, rs);
    if (!tab->insert(k)) return;
    out->push_back(k);
    checkNew(cs, ds, rs, height);
  }
  void dfs(int t, int x) {
    if (t == T) { if (x == x0) leaf(); return; }
    if (root && x == 0) return;  // cell 0 contains the leading digit: >= 1 at all times
    int cin = (cc >> t) & 1, dneed = (cd >> t) & 1;
    for (int d = 0; d < 2; d++) {
      if ((x + d) / B != dneed) continue;
      int e = (x + cin) % B, r = (x + d) % B, co = (x + cin) / B;
      int nx = ovf[t] ? e + (int)((cr >> (4 * OVI[t])) & 15) : e + r;
      u64 sc = cs, sd = ds; u128 sr = rs;
      cs |= (u64)co << t; ds |= (u64)d << t; if (ovf[t]) rs |= (u128)r << (4 * OVI[t]);
      dfs(t + 1, nx);
      cs = sc; ds = sd; rs = sr;
    }
  }
  void expand(u64 c, u64 d, u128 r, bool isRoot) {
    cc = c; cd = d; cr = r; root = isRoot;
    for (x0 = isRoot ? 1 : 0; x0 <= 2 * B - 2; x0++) { cs = ds = 0; rs = 0; dfs(0, x0); }
  }
};

static double rssGB() {
  struct rusage ru; getrusage(RUSAGE_SELF, &ru);
#ifdef __APPLE__
  return ru.ru_maxrss / 1e9;
#else
  return ru.ru_maxrss / 1e6;
#endif
}

enum { R_EMPTY = 0, R_COMPLETE = 1, R_TOOBIG = 2, R_MAXDEPTH = 3, R_FIT = 4 };
template <int W> static int run(u64 cap, int maxdepth, int nth) {
  unique_ptr<Table<W>> tabp(new Table<W>()); Table<W>* tab = tabp.get();
  auto t0 = chrono::steady_clock::now();
  u64 rc = 0, rd = 0; u128 rr = 0;
  for (int t = 0; t < T; t++) if (ovf[t]) { rd |= 1ULL << t; rr |= (u128)1 << (4 * OVI[t]); }
  vector<Key<W>> frontier;
  { Expander<W> ex; ex.tab = tab; ex.out = &frontier; ex.height = 1; ex.expand(rc, rd, rr, true); }
  if (!QUIET) outf("height 1: %zu interfaces\n", frontier.size());
  if (frontier.empty()) { outf("RESULT EMPTY at height 1: no left end at all\n"); return R_EMPTY; }
  int depth = 1; int res = R_COMPLETE;
  while (!frontier.empty() && !stopFit) {
    if (depth >= maxdepth) { outf("RESULT MAXDEPTH at height %d: %llu visited, frontier %zu\n", depth, (unsigned long long)tab->total.load(), frontier.size()); res = R_MAXDEPTH; break; }
    vector<vector<Key<W>>> outs(nth); atomic<u64> nexti{0}; const u64 CHK = 64; atomic<bool> over{false};
    auto work = [&](int id) {
      Expander<W> ex; ex.tab = tab; ex.out = &outs[id]; ex.height = depth + 1;
      while (true) {
        u64 a = nexti.fetch_add(CHK); if (a >= frontier.size()) break;
        u64 b = min<u64>(a + CHK, frontier.size());
        for (u64 i = a; i < b; i++) { u64 c, d; u128 r; unpack(frontier[i], c, d, r); ex.expand(c, d, r, false); }
        if (tab->total.load() > cap) { over = true; break; }
        if (stopFit) break;
      }
    };
    if (nth == 1) work(0); else { vector<thread> th; for (int i = 0; i < nth; i++) th.emplace_back(work, i); for (auto& x : th) x.join(); }
    u64 nnew = 0; for (auto& o : outs) nnew += o.size();
    double secs = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    if (!QUIET) outf("height %d: %llu new, %llu visited, %.1f s, maxrss %.2f GB%s\n", depth + 1, (unsigned long long)nnew, (unsigned long long)tab->total.load(), secs, rssGB(), nAccept ? "  <-- accepting interfaces seen" : "");
    if (over || tab->total.load() > cap) { outf("RESULT TOO_BIG at height %d: %llu interfaces visited (cap %llu)\n", depth + 1, (unsigned long long)tab->total.load(), (unsigned long long)cap); res = R_TOOBIG; break; }
    vector<Key<W>>().swap(frontier); frontier.reserve(nnew);
    for (auto& o : outs) { frontier.insert(frontier.end(), o.begin(), o.end()); vector<Key<W>>().swap(o); }
    depth++;
  }
  int reached = 0; for (Target* g : targets) if (g->h >= 0) reached++;
  if (MODE == 1 && stopFit) { outf("RESULT FIT at height %d (reconstruct the left end with ./reach, same BAND/PH)\n", targets[0]->h.load()); return R_FIT; }
  if (res == R_COMPLETE) {
    double secs = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    outf("RESULT COMPLETE: frontier empty after height %d; %llu interfaces reachable%s; band targets reached %d of %zu; distinct wire streams %zu%s; %.1f s; maxrss %.2f GB\n",
         depth, (unsigned long long)tab->total.load(), ROTN > 1 ? " (orbits under the clock shift)" : "", reached, targets.size(), streams.size(), ROTN > 1 ? " (up to the clock shift)" : "", secs, rssGB());
  } else if (reached) outf("NOTE: band targets reached before stopping: %d\n", reached);
  return res;
}

// per-task setup; returns key words W, or -1 on bad input
static int setupTask(int T_, const string& pat, const string& mode) {
  T = T_; NOV = 0; for (Target* g : targets) delete g; targets.clear(); streams.clear(); nAccept = 0; stopFit = false;
  MODE = mode == "ALL" ? 0 : mode == "BAND" ? 1 : mode == "WIRE" ? 2 : -1;
  if (MODE < 0) { fprintf(stderr, "mode must be ALL, BAND or WIRE\n"); return -1; }
  if (B > 15 || B < 2 || T > 64 || T < 1 || pat.empty()) { fprintf(stderr, "need 2<=B<=15, 1<=T<=64\n"); return -1; }
  MASK = (T == 64) ? ~0ULL : ((1ULL << T) - 1);
  for (int t = 0; t < T; t++) { ovf[t] = pat[t % pat.size()] - '0'; OVI[t] = -1; if (ovf[t]) OVI[t] = NOV++; }
  if (NOV == 0 || NOV > 32) { fprintf(stderr, "need 1..32 overflow steps per period\n"); return -1; }
  checkWire = (MODE != 1);
  if (MODE == 0) {
    for (auto& cy : uniformCycles()) if (T % (int)cy.size() == 0) for (int ph = 0; ph < (int)cy.size(); ph++) addBand(cy, ph);
  } else if (MODE == 1) {
    string bs = getenv("BAND") ? getenv("BAND") : "1:3,0:6"; size_t p = 0; vector<int> vals;
    while (p < bs.size()) { size_t q = bs.find(',', p); if (q == string::npos) q = bs.size(); string it = bs.substr(p, q - p); int cv = it[0] - '0', rv = atoi(it.c_str() + 2); vals.push_back(rv + (B - 1) * cv); p = q + 1; }
    if (T % (int)vals.size()) { fprintf(stderr, "T must be a multiple of the band period %zu\n", vals.size()); return -1; }
    addBand(vals, getenv("PH") ? atoi(getenv("PH")) : 0);
  }
  ROT = getenv("ROT") && atoi(getenv("ROT")); ROTP = T; ROTN = 1; ROTK = NOV;
  if (ROT) {
    int p0 = pat.size(); for (int d = 1; d <= (int)pat.size(); d++) if (pat.size() % d == 0) { bool ok = true; for (size_t i = d; i < pat.size(); i++) if (pat[i] != pat[i - d]) { ok = false; break; } if (ok) { p0 = d; break; } }
    if (T % p0 == 0) { ROTP = p0; ROTN = T / p0; ROTK = NOV / ROTN; }
  }
  NBITS = 2 * T + 4 * NOV; return (NBITS + 63) / 64;
}
static int solve(int W, const string& pat, const string& mode, u64 cap, int maxdepth, int nth) {
  if (!QUIET) {
    outf("reachmt B=%d T=%d clock=%s mode=%s cap=%llu threads=%d keybits=%d words=%d rot=%d(p=%d) targets:", B, T, pat.c_str(), mode.c_str(), (unsigned long long)cap, nth, NBITS, W, ROTN, ROTP);
    for (Target* g : targets) outf(" %s/ph%d", g->name.c_str(), g->ph);
    outf("%s\n", checkWire ? " +wire" : "");
  }
  switch (W) { case 1: return run<1>(cap, maxdepth, nth); case 2: return run<2>(cap, maxdepth, nth); case 3: return run<3>(cap, maxdepth, nth); default: return run<4>(cap, maxdepth, nth); }
}

int main(int argc, char** argv) {
  int nth = getenv("THREADS") ? atoi(getenv("THREADS")) : (int)thread::hardware_concurrency(); if (nth < 1) nth = 1;
  string first = argc >= 2 ? argv[1] : "";
  if (first == "BATCH") {  // reachmt BATCH B MODE cap  < lines "T CLOCK"
    if (argc < 5) { fprintf(stderr, "usage: reachmt BATCH B ALL|WIRE cap < tasks (lines: T CLOCK)\n"); return 2; }
    B = atoi(argv[2]); string mode = argv[3]; u64 cap = strtoull(argv[4], 0, 10); QUIET = true; SB = 6; NS = 1 << SB;
    int Tt; string pat;
    while (cin >> Tt >> pat) {
      int W = setupTask(Tt, pat, mode);
      printf("TASK %d %s\n", Tt, pat.c_str()); fflush(stdout);
      if (W < 0) printf("RESULT BADTASK\n"); else solve(W, pat, mode, cap, 1000000, nth);
      printf("ENDTASK\n"); fflush(stdout);
    }
    return 0;
  }
  if (first == "SWEEP") {  // reachmt SWEEP B TMIN TMAX cap SHARD NSHARDS
    if (argc < 8) { fprintf(stderr, "usage: reachmt SWEEP B TMIN TMAX cap SHARD NSHARDS\n"); return 2; }
    B = atoi(argv[2]); int tmin = atoi(argv[3]), tmax = atoi(argv[4]); u64 cap = strtoull(argv[5], 0, 10);
    long long shard = atoll(argv[6]), nsh = atoll(argv[7]); QUIET = true; BUFFER = true; SB = 6; NS = 1 << SB; nth = 1;
    map<int, array<long long, 6>> cnt;  // tasks, empty, complete, undecided, band targets, wire streams
    vector<int> w(1, -1); long long idx = 0; auto t0 = chrono::steady_clock::now();
    printf("SWEEP B=%d T=%d..%d cap=%llu shard %lld of %lld\n", B, tmin, tmax, (unsigned long long)cap, shard, nsh); fflush(stdout);
    while (!w.empty()) {  // Duval: binary Lyndon words of length <= tmax in lexicographic order
      w.back()++;
      int p = w.size();
      if ((idx++ % nsh) == shard) {
        string pat; bool any = false; for (int v : w) { pat += (char)('0' + v); any |= (v == 1); }
        if (any) for (int Tt = max(p, ((tmin + p - 1) / p) * p); Tt <= tmax; Tt += p) {
          int W = setupTask(Tt, pat, "ALL"); if (W < 0) continue;
          OUTBUF.clear(); int res = solve(W, pat, "ALL", cap, 1000000, 1);
          auto& c = cnt[Tt]; c[0]++;
          if (res == R_EMPTY) { c[1]++; continue; }
          if (res == R_COMPLETE) c[2]++; else c[3]++;
          int reached = 0; for (Target* g : targets) if (g->h >= 0) reached++;
          c[4] += reached; c[5] += streams.size();
          printf("TASK %d %s\n%sENDTASK\n", Tt, pat.c_str(), OUTBUF.c_str()); fflush(stdout);
        }
      }
      while ((int)w.size() < tmax) w.push_back(w[w.size() - p]);
      while (!w.empty() && w.back() == 1) w.pop_back();
    }
    for (auto& kv : cnt) printf("SWEEP SUMMARY T=%d tasks=%lld empty=%lld complete=%lld undecided=%lld band_targets=%lld wire_streams=%lld\n",
                                kv.first, kv.second[0], kv.second[1], kv.second[2], kv.second[3], kv.second[4], kv.second[5]);
    printf("SWEEP DONE shard %lld of %lld, %lld words scanned, %.1f s\n", shard, nsh, idx, chrono::duration<double>(chrono::steady_clock::now() - t0).count());
    return 0;
  }
  if (argc < 5) { fprintf(stderr, "usage: [THREADS=n] [BAND=.. PH=..] reachmt B T CLOCK ALL|BAND|WIRE [cap] [maxdepth]\n       reachmt BATCH B ALL|WIRE cap < tasks\n       reachmt SWEEP B TMIN TMAX cap SHARD NSHARDS\n"); return 2; }
  B = atoi(argv[1]); string pat = argv[3]; string mode = argv[4];
  u64 cap = argc > 5 ? strtoull(argv[5], 0, 10) : 4000000000ULL; int maxdepth = argc > 6 ? atoi(argv[6]) : 1000000;
  int W = setupTask(atoi(argv[2]), pat, mode); if (W < 0) return 2;
  solve(W, pat, mode, cap, maxdepth, nth);
  return 0;
}
