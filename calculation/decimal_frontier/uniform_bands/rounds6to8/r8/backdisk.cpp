// backdisk.cpp -- round 7: backward cone (reverse reachability) on the graph of reachdisk.cpp. Same keys, step relation, bottom
// interface, root rule and ROT quotient; the state set is explored from the TARGET keys through predecessors, with the same
// external-memory buckets, generations and manifest. Answer: REACHABLE (the bottom interface reaches a target, with the height) or
// UNREACHABLE (COMPLETE: the reverse frontier is empty). See DESIGN_R7.md.
// usage: [THREADS=n] [ROT=1] [PB=bits] ./backdisk B T CLOCK WORKDIR cap min_free_fraction SPEC...    |   ./backdisk TEST B T CLOCK N seed
#include <random>
#include <unordered_set>
#include <deque>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <cstdarg>
#include <string>
#include <vector>
#include <array>
#include <set>
#include <mutex>
#include <thread>
#include <atomic>
#include <chrono>
#include <algorithm>
#include <memory>
#include <cerrno>
#include <sys/resource.h>
#include <sys/statvfs.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
using namespace std;
typedef uint64_t u64; typedef unsigned __int128 u128;

static int B, T, NOV = 0; static int MODE = 0;  // 0 ALL, 2 WIRE
static int ovf[64], OVI[64]; static u64 MASK; static int NBITS;
static bool ROT = false; static int ROTP = 0, ROTN = 1, ROTK = 0;
static int PBITS = 10, PB = 1024;
static u64 CAP = 4000000000ULL; static double FREE_MIN = 0.15;
static string WORK; static int NTH = 1;

static void outf(const char* fmt, ...) {
  char buf[1024]; va_list ap; va_start(ap, fmt); vsnprintf(buf, sizeof(buf), fmt, ap); va_end(ap);
  fputs(buf, stdout); fflush(stdout);
}

template <int W> struct Key { u64 w[W]; };
template <int W> static inline bool keq(const Key<W>& a, const Key<W>& b) { for (int i = 0; i < W; i++) if (a.w[i] != b.w[i]) return false; return true; }
template <int W> static inline u64 khash(const Key<W>& k) {
  u64 h = 0x9E3779B97F4A7C15ULL;
  for (int i = 0; i < W; i++) { h ^= k.w[i] + 0x632BE59BD9B4E019ULL + (h << 6) + (h >> 2); h *= 0xBF58476D1CE4E5B9ULL; h ^= h >> 31; }
  h *= 0x94D049BB133111EBULL; h ^= h >> 29; return h;
}
static inline void setbits(u64* w, int pos, int len, u64 v) {
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

// ---- targets (identical to reachmt)
struct Target { u64 c; u128 r; string name; string spec; int ph; atomic<int> h{-1}; };
static vector<Target*> targets;
static void addBand(const vector<int>& vals, int ph) {
  int q = vals.size(); Target* g = new Target(); g->c = 0; g->r = 0; g->ph = ph;
  for (int t = 0; t < T; t++) {
    int v = vals[(t + ph) % q], cv = v >= B ? 1 : 0, rv = (v + cv) % B;
    g->c |= (u64)cv << t; if (ovf[t]) g->r |= (u128)rv << (4 * OVI[t]);
  }
  g->name = "band["; g->spec = "";
  for (int i = 0; i < q; i++) { int v = vals[i], cv = v >= B ? 1 : 0; g->name += to_string(v) + (i + 1 < q ? "," : "]"); g->spec += to_string(cv) + ":" + to_string((v + cv) % B) + (i + 1 < q ? "," : ""); }
  targets.push_back(g);
}
static vector<vector<int>> uniformCycles() {
  vector<vector<int>> cyc; set<int> seenMin;
  auto f = [](int v) { int c = v >= B ? 1 : 0; return 2 * ((v + c) % B); };
  for (int v0 = 0; v0 <= 2 * B - 2; v0++) {
    int v = v0; for (int i = 0; i < 4 * B; i++) v = f(v);
    vector<int> cy; int u = v; bool bad = false;
    do { if (u == B - 1) bad = true; cy.push_back(u); u = f(u); } while (u != v && (int)cy.size() <= 2 * B);
    if (bad || u != v) continue;
    int mn = *min_element(cy.begin(), cy.end()); if (seenMin.count(mn)) continue; seenMin.insert(mn);
    rotate(cy.begin(), find(cy.begin(), cy.end(), mn), cy.end()); cyc.push_back(cy);
  }
  return cyc;
}
// ---- disk visited set: per bucket base_b.bin (sorted unique) + delta_b.bin (sorted unique, disjoint from base)
template <int W> struct Disk {
  vector<FILE*> cand; vector<unique_ptr<mutex>> mx;
  Disk() : cand(PB, nullptr) { for (int i = 0; i < PB; i++) mx.emplace_back(new mutex()); }
};
static string P(const string& name) { return WORK + "/" + name; }
static string candPath(int b) { return P("cand_" + to_string(b) + ".bin"); }
static string frontPath(int h, int b) { return P("front_" + to_string(h) + "_" + to_string(b) + ".bin"); }
static string basePath(int b, int g) { return P("base_" + to_string(b) + "_" + to_string(g) + ".bin"); }
static string deltaPath(int b, int g) { return P("delta_" + to_string(b) + "_" + to_string(g) + ".bin"); }
// per-bucket committed state; only the manifest makes a generation current (a crash leaves unreferenced files behind)
struct BState { int baseGen = 0, deltaGen = 0; u64 baseCnt = 0, deltaCnt = 0; };
static u64 fsize(const string& p) { struct stat st; return stat(p.c_str(), &st) == 0 ? (u64)st.st_size : 0; }

template <int W> struct Reader {  // buffered sequential reader of sorted keys; a missing file is empty
  FILE* f = nullptr; vector<Key<W>> buf; size_t pos = 0, n = 0;
  explicit Reader(const string& path, size_t cap = (1u << 18)) : buf(cap) { f = fopen(path.c_str(), "rb"); }
  ~Reader() { if (f) fclose(f); }
  bool peek(Key<W>& k) {
    if (pos == n) { if (!f) return false; n = fread(buf.data(), sizeof(Key<W>), buf.size(), f); pos = 0; if (n == 0) return false; }
    k = buf[pos]; return true;
  }
  void adv() { pos++; }
};
template <int W> static void writeAll(const string& path, const vector<Key<W>>& v) {
  FILE* f = fopen(path.c_str(), "wb"); if (!f) { outf("RESULT TOO_BIG: cannot write %s\n", path.c_str()); exit(4); }
  if (!v.empty() && fwrite(v.data(), sizeof(Key<W>), v.size(), f) != v.size()) { outf("RESULT TOO_BIG: write failed (disk full?)\n"); exit(4); }
  fclose(f);
}
template <int W> static vector<Key<W>> readAll(const string& path) {
  vector<Key<W>> v; u64 n = fsize(path) / sizeof(Key<W>); v.resize(n);
  if (!n) return v;
  FILE* f = fopen(path.c_str(), "rb"); if (!f) return vector<Key<W>>();
  size_t got = fread(v.data(), sizeof(Key<W>), n, f); fclose(f); v.resize(got); return v;
}
// U := U minus the keys of the sorted file `path` (two-pointer streaming pass; U sorted unique)
template <int W> static void subtractFile(vector<Key<W>>& U, const string& path) {
  Reader<W> r(path); Key<W> k; size_t i = 0, w = 0;
  while (r.peek(k)) {
    r.adv();
    while (i < U.size() && kless(U[i], k)) U[w++] = U[i++];
    if (i < U.size() && keq(U[i], k)) i++;
  }
  while (i < U.size()) U[w++] = U[i++];
  U.resize(w);
}
// out := sorted union of two disjoint sorted files (either may be missing)
template <int W> static u64 mergeFiles(const string& a, const string& b, const string& out) {
  Reader<W> ra(a), rb(b); FILE* o = fopen(out.c_str(), "wb"); if (!o) { outf("RESULT TOO_BIG: cannot write %s\n", out.c_str()); exit(4); }
  vector<Key<W>> ob(1u << 16); size_t on = 0; u64 cnt = 0;
  auto flush = [&]() { if (on && fwrite(ob.data(), sizeof(Key<W>), on, o) != on) { outf("RESULT TOO_BIG: write failed (disk full?)\n"); exit(4); } cnt += on; on = 0; };
  Key<W> ka, kb; bool ha = ra.peek(ka), hb = rb.peek(kb);
  while (ha || hb) {
    if (ha && (!hb || kless(ka, kb))) { ob[on++] = ka; ra.adv(); ha = ra.peek(ka); }
    else { ob[on++] = kb; rb.adv(); hb = rb.peek(kb); }
    if (on == ob.size()) flush();
  }
  flush(); fclose(o); return cnt;
}

// ---- expansion (identical to reachmt) with leaves sent to the bucket writers
template <int W> struct Writer {
  Disk<W>* D; vector<vector<Key<W>>> buf;
  explicit Writer(Disk<W>* d) : D(d), buf(PB) {}
  void put(const Key<W>& k) {
    u64 b = khash(k) >> (64 - PBITS); auto& v = buf[b]; v.push_back(k);
    if (v.size() >= 512) flush(b);
  }
  void flush(u64 b) {
    auto& v = buf[b]; if (v.empty()) return;
    lock_guard<mutex> g(*D->mx[b]);
    if (fwrite(v.data(), sizeof(Key<W>), v.size(), D->cand[b]) != v.size()) { outf("RESULT TOO_BIG: write failed (disk full?)\n"); exit(4); }
    v.clear();
  }
  void flushAll() { for (u64 b = 0; b < (u64)PB; b++) flush(b); }
};

// ---- round 7: backward cone. Same graph as reachdisk (same keys, same step relation, same bottom interface, same root rule,
// same ROT quotient); here we enumerate PREDECESSORS. Layer 1 = the target keys, layer h = predecessors of layer h-1 not seen.
struct TKey { u64 c, d; u128 r; };
static vector<TKey> tkeys; static string SPEC;
static u64 BOTD = 0; static u128 BOTR = 0;   // the bottom interface: c = 0, d = overflow mask, r = 1 at every overflow
static int CLKP = 1;                          // smallest period of the clock word
static atomic<int> hitHeight{-1};

// ---- optional sound pruning (env WIN=w): window abstraction, see window.cpp. For every clock phase ph, WSETS[ph] holds every window content
// (c, d and r at the overflow slots; w slots starting at a slot s with s mod clock length = ph) that ANY reachable interface of ANY period T
// can have: the closure of the bottom pattern under the abstract step with an unknown running value at the window start. A state with a window
// outside its set is not reachable from the bottom, so predecessors failing it can be dropped without changing the answer.
static int WW = 0, WLEN = 1; static int wNOVp[64];
struct WH { size_t operator()(const u128& k) const { u64 a = (u64)k, b = (u64)(k >> 64); u64 h = a * 0x9E3779B97F4A7C15ULL ^ (b + 0x632BE59BD9B4E019ULL) * 0xBF58476D1CE4E5B9ULL; h ^= h >> 31; return h; } };
static vector<unordered_set<u128, WH>> WSETS; static int wpre[70];   // wpre[t] = overflow slots before slot t
static inline u128 wkey(u64 c, u64 d, u128 r) { return (u128)c | ((u128)d << WW) | (r << (2 * WW)); }
struct WExp {
  int wovf[64], wOVI[64];
  u64 cc, cd; u128 cr; u64 cs, ds; u128 rs; vector<u128>* out;
  void dfs(int t, int x) {
    if (t == WW) { out->push_back(wkey(cs, ds, rs)); return; }
    int cin = (cc >> t) & 1, dneed = (cd >> t) & 1;
    for (int d = 0; d < 2; d++) {
      if ((x + d) / B != dneed) continue;
      int e = (x + cin) % B, r = (x + d) % B, co = (x + cin) / B;
      int nx = wovf[t] ? e + (int)((cr >> (4 * wOVI[t])) & 15) : e + r;
      u64 sc = cs, sd = ds; u128 sr = rs;
      cs |= (u64)co << t; ds |= (u64)d << t; if (wovf[t]) rs |= (u128)r << (4 * wOVI[t]);
      dfs(t + 1, nx);
      cs = sc; ds = sd; rs = sr;
    }
  }
};
static void buildWindowSet(const string& pat, int w) {
  WW = w; WLEN = pat.size(); WSETS.assign(WLEN, unordered_set<u128, WH>());
  for (int t = 0; t < 69; t++) wpre[t] = 0;
  { int c = 0; for (int t = 0; t < 69; t++) { wpre[t] = c; if (pat[t % pat.size()] == '1') c++; } }
  for (int ph = 0; ph < WLEN; ph++) {
    WExp ex; int nv = 0;
    for (int t = 0; t < w; t++) { ex.wovf[t] = pat[(ph + t) % pat.size()] - '0'; ex.wOVI[t] = -1; if (ex.wovf[t]) ex.wOVI[t] = nv++; }
    wNOVp[ph] = nv;
    u64 bd = 0; u128 br = 0; for (int t = 0; t < w; t++) if (ex.wovf[t]) { bd |= 1ULL << t; br |= (u128)1 << (4 * ex.wOVI[t]); }
    auto& S = WSETS[ph]; deque<u128> q; u128 b0 = wkey(0, bd, br); S.insert(b0); q.push_back(b0); vector<u128> succ; u64 m = (1ULL << w) - 1;
    while (!q.empty()) {
      u128 k = q.front(); q.pop_front(); succ.clear(); ex.out = &succ;
      ex.cc = (u64)k & m; ex.cd = (u64)(k >> w) & m; ex.cr = k >> (2 * w);
      for (int x0 = 0; x0 <= 2 * B - 2; x0++) { ex.cs = ex.ds = 0; ex.rs = 0; ex.dfs(0, x0); }
      for (u128 s2 : succ) if (S.insert(s2).second) q.push_back(s2);
    }
    outf("window filter: w=%d phase %d: %zu abstract states\n", w, ph, S.size());
  }
}
// is the window of c,d,r that ends just before slot t1 (t1 slots decided so far) in its phase set?
static inline bool winOK(u64 c, u64 d, u128 r, int t1) {
  if (!WW || t1 < WW) return true;
  int s0 = t1 - WW, ph = s0 % WLEN; u64 m = (1ULL << WW) - 1;
  int nv = wNOVp[ph];
  u128 rr = (r >> (4 * wpre[s0])) & ((nv * 4 >= 128) ? ~(u128)0 : (((u128)1 << (4 * nv)) - 1));
  return WSETS[ph].count(wkey((c >> s0) & m, (d >> s0) & m, rr)) > 0;
}

static void addStream(const string& bits) {   // the stream and its shifts by multiples of the clock period (closed target set)
  if ((int)bits.size() != T) { fprintf(stderr, "stream length %zu != T=%d\n", bits.size(), T); exit(2); }
  set<u64> seen;
  for (int s = 0; s < T / CLKP; s++) {
    u64 c = 0; for (int t = 0; t < T; t++) if (bits[(t + s * CLKP) % T] == '1') c |= 1ULL << t;
    if (!seen.insert(c).second) continue;
    u64 d = (~c) & MASK; u128 r = 0;
    for (int t = 0; t < T; t++) if (ovf[t]) r |= (u128)((B - 1) * (int)((c >> t) & 1)) << (4 * OVI[t]);
    tkeys.push_back({c, d, r});
  }
}

static bool ALLSTREAMS = false;
// every 9-wire interface (d = complement of c, r = (B-1) c at the overflow slots) whose windows are all inside the window sets (pruned while it is built)
static void enumStreams(int t, u64 c, u128 r) {
  if (t == T) { tkeys.push_back({c, (~c) & MASK, r}); return; }
  for (int b = 0; b < 2; b++) {
    u64 c2 = c | ((u64)b << t); u128 r2 = r; if (ovf[t]) r2 |= (u128)((B - 1) * b) << (4 * OVI[t]);
    u64 dm = (t + 1 >= 64) ? ~0ULL : ((1ULL << (t + 1)) - 1);
    if (winOK(c2, (~c2) & dm, r2, t + 1)) enumStreams(t + 1, c2, r2);
  }
}

template <int W> struct PredExp {
  Writer<W>* wr = nullptr; int height = 0;    // height = the height a bottom hit would have (1 + distance of the expanded state)
  vector<TKey>* out = nullptr; bool* rootHit = nullptr;   // test mode: collect raw predecessors instead of writing
  u64 cs, ds; u128 rs;
  int co[64], dt[64], rn[64]; uint32_t G[65][32];
  u64 cc, cd; u128 cr; int x0;
  bool prep() {
    for (int t = 0; t < T; t++) {
      co[t] = (cs >> t) & 1; dt[t] = (ds >> t) & 1; rn[t] = ovf[t] ? (int)((rs >> (4 * OVI[t])) & 15) : 0;
      if (ovf[t] && rn[t] >= B) return false;
    }
    int NX = 2 * B - 1;
    for (int x = 0; x < NX; x++) G[T][x] = 1u << x;
    for (int t = T - 1; t >= 0; t--) for (int x = 0; x < NX; x++) {
      int xd = x + dt[t], r_ = xd % B; uint32_t m = 0;
      if (!(ovf[t] && r_ != rn[t])) for (int cin = 0; cin < 2; cin++) {
        if ((x + cin) / B != co[t]) continue;
        int e = (x + cin) % B;
        if (ovf[t]) { for (int cr_ = 0; cr_ < B; cr_++) m |= G[t + 1][e + cr_]; } else m |= G[t + 1][e + r_];
      }
      G[t][x] = m;
    }
    return true;
  }
  void leaf(bool ok) {
    bool bottom = (cc == 0 && cd == BOTD && cr == BOTR);
    if (out) { out->push_back({cc, cd, cr}); if (bottom && ok && rootHit) *rootHit = true; return; }
    if (bottom && ok) { int e = -1; hitHeight.compare_exchange_strong(e, height); }
    Key<W> k = ROT ? canon<W>(cc, cd, cr) : pack<W>(cc, cd, cr);
    wr->put(k);
  }
  void dfs(int t, int x, bool ok) {
    if (t == T) { leaf(ok); return; }
    if (x == 0) ok = false;                   // a root edge needs x_t >= 1 for every t (x_0 = x0 >= 1)
    int xd = x + dt[t], cdv = xd / B, r_ = xd % B;
    if (ovf[t] && r_ != rn[t]) return;
    u64 sc = cc, sd = cd; u128 sr = cr;
    for (int cin = 0; cin < 2; cin++) {
      if ((x + cin) / B != co[t]) continue;
      int e = (x + cin) % B;
      cc = sc | ((u64)cin << t); cd = sd | ((u64)cdv << t);
      if (ovf[t]) {
        for (int cr_ = 0; cr_ < B; cr_++) {
          int nx = e + cr_; if (!((G[t + 1][nx] >> x0) & 1)) continue;
          cr = sr | ((u128)cr_ << (4 * OVI[t])); if (winOK(cc, cd, cr, t + 1)) dfs(t + 1, nx, ok);
        }
      } else {
        int nx = e + r_; if (!((G[t + 1][nx] >> x0) & 1)) continue;
        if (winOK(cc, cd, cr, t + 1)) dfs(t + 1, nx, ok);
      }
    }
    cc = sc; cd = sd; cr = sr;
  }
  void expand(u64 c, u64 d, u128 r) {
    cs = c; ds = d; rs = r; if (!prep()) return;
    for (x0 = 0; x0 <= 2 * B - 2; x0++) {
      if (!((G[0][x0] >> x0) & 1)) continue;
      cc = cd = 0; cr = 0; dfs(0, x0, true);
    }
  }
};

// forward successors (same as reachdisk's Expander), collected raw; used by the self test only
struct FwdExp {
  u64 cc, cd; u128 cr; int x0; bool root; u64 cs, ds; u128 rs; vector<TKey>* out;
  void dfs(int t, int x) {
    if (t == T) { if (x == x0) out->push_back({cs, ds, rs}); return; }
    if (root && x == 0) return;
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
  void expand(const TKey& k, bool isRoot, vector<TKey>& o) {
    cc = k.c; cd = k.d; cr = k.r; root = isRoot; out = &o;
    for (x0 = isRoot ? 1 : 0; x0 <= 2 * B - 2; x0++) { cs = ds = 0; rs = 0; dfs(0, x0); }
  }
};
static bool keyEq(const TKey& a, const TKey& b) { return a.c == b.c && a.d == b.d && a.r == b.r; }
// self test: random forward edges must have their source among the predecessors, and random predecessors must step forward
// back to the target. Edges leaving the bottom interface use the root rule; the root edge shows up as rootHit.
static int selfTest(long N, unsigned long long seed) {
  mt19937_64 rng(seed); FwdExp fx; PredExp<1> px; vector<TKey> succ, preds, fs;
  TKey bottom{0, BOTD, BOTR}; TKey cur = bottom; bool atBottom = true;
  long edges = 0, bad = 0, predChecked = 0, steps = 0;
  while (edges < N && steps < 50 * N) {
    steps++;
    succ.clear(); fx.expand(cur, atBottom, succ);
    if (succ.empty() || rng() % 300 == 0) { cur = bottom; atBottom = true; continue; }
    TKey nx = succ[rng() % succ.size()];
    preds.clear(); bool rootHit = false; px.out = &preds; px.rootHit = &rootHit; px.expand(nx.c, nx.d, nx.r);
    edges++;
    bool found = false;
    if (atBottom) found = rootHit; else for (const TKey& p : preds) if (keyEq(p, cur)) { found = true; break; }
    if (!found) { bad++; if (bad < 5) fprintf(stderr, "MISSING forward edge in predecessor set (edge %ld)\n", edges); }
    if (!preds.empty()) {
      TKey p = preds[rng() % preds.size()]; fs.clear(); fx.expand(p, false, fs); predChecked++;
      bool ok = false; for (const TKey& s : fs) if (keyEq(s, nx)) { ok = true; break; }
      if (!ok) { bad++; if (bad < 5) fprintf(stderr, "predecessor does not step forward to the target (edge %ld)\n", edges); }
    }
    if (WW) for (int s0 = 0; s0 + WW <= T; s0++) if (!winOK(nx.c, nx.d, nx.r, s0 + WW)) { bad++; if (bad < 5) fprintf(stderr, "reachable state outside the window set\n"); }
    cur = nx; atBottom = false;
  }
  outf("SELFTEST forward edges checked %ld, predecessors checked %ld, mismatches %ld -> %s\n", edges, predChecked, bad, bad ? "FAIL" : "PASS");
  return bad ? 1 : 0;
}

// ---- manifest: parameters + target spec, last finished layer, per-bucket generations
struct Manifest { int layer = 0; u64 visited = 0; };
static string manifestSig(int W) {
  string s = "B=" + to_string(B) + " T=" + to_string(T) + " nov=" + to_string(NOV) + " W=" + to_string(W) +
             " rot=" + to_string(ROT) + " rotp=" + to_string(ROTP) + " rotn=" + to_string(ROTN) + " rotk=" + to_string(ROTK) + " pb=" + to_string(PB) + " ";
  for (int t = 0; t < T; t++) s += ovf[t] ? '1' : '0';
  return s + " spec=" + SPEC;
}
static void writeManifest(int W, int layer, u64 visited, const vector<BState>& bs) {
  string tmp = P("manifest.tmp"), fin = P("manifest.txt");
  FILE* f = fopen(tmp.c_str(), "w"); if (!f) exit(4);
  fprintf(f, "sig %s\nlayer %d\nvisited %llu\n", manifestSig(W).c_str(), layer, (unsigned long long)visited);
  for (size_t b = 0; b < bs.size(); b++) fprintf(f, "bk %zu %d %d %llu %llu\n", b, bs[b].baseGen, bs[b].deltaGen, (unsigned long long)bs[b].baseCnt, (unsigned long long)bs[b].deltaCnt);
  fclose(f); rename(tmp.c_str(), fin.c_str());
}
static bool readManifest(int W, Manifest& m, vector<BState>& bs) {
  FILE* f = fopen(P("manifest.txt").c_str(), "r"); if (!f) return false;
  char line[8192]; bool sigok = false;
  while (fgets(line, sizeof line, f)) {
    if (!strncmp(line, "sig ", 4)) { string s(line + 4); while (!s.empty() && s.back() == '\n') s.pop_back(); sigok = (s == manifestSig(W)); if (!sigok) { fclose(f); outf("RESULT BADTASK: manifest signature differs in %s\n", WORK.c_str()); exit(5); } }
    else if (!strncmp(line, "layer ", 6)) m.layer = atoi(line + 6);
    else if (!strncmp(line, "visited ", 8)) m.visited = strtoull(line + 8, 0, 10);
    else if (!strncmp(line, "bk ", 3)) { size_t b; BState st; unsigned long long bc, dc; if (sscanf(line + 3, "%zu %d %d %llu %llu", &b, &st.baseGen, &st.deltaGen, &bc, &dc) == 5 && b < bs.size()) { st.baseCnt = bc; st.deltaCnt = dc; bs[b] = st; } }
  }
  fclose(f); return sigok;
}
static void cleanScratch() {
  DIR* d = opendir(WORK.c_str()); if (!d) return;
  while (struct dirent* e = readdir(d)) {
    string n = e->d_name;
    if (n.rfind("base_", 0) == 0 || n.rfind("delta_", 0) == 0 || n.rfind("front_", 0) == 0 || n.rfind("cand_", 0) == 0) remove(P(n).c_str());
  }
  closedir(d);
}
static double rssGB() { struct rusage ru; getrusage(RUSAGE_SELF, &ru); return ru.ru_maxrss / 1e9; }
static double freeFrac() {
  struct statvfs sv; if (statvfs(WORK.c_str(), &sv) != 0) return 0;
  return (double)sv.f_bavail / (double)sv.f_blocks;
}

template <int W> static int run(int nth) {
  auto t0 = chrono::steady_clock::now();
  Disk<W>* D = new Disk<W>(); unique_ptr<Disk<W>> dp(D);
  vector<BState> bs(PB);
  Manifest man; bool resume = readManifest(W, man, bs);
  int L = resume ? man.layer : 0;
  if (!resume) cleanScratch();
  u64 V = 0; for (const BState& x : bs) V += x.baseCnt + x.deltaCnt;
  if (resume) outf("RESUME from layer %d (visited %llu)\n", L, (unsigned long long)V);
  int res = -1; int finalH = 0;
  while (res < 0) {
    int h = L + 1;                       // layer h holds the states at distance h-1 from the target set
    vector<BState> prev = bs;
    auto tg = chrono::steady_clock::now();
    for (int b = 0; b < PB; b++) { D->cand[b] = fopen(candPath(b).c_str(), "wb"); if (!D->cand[b]) { outf("RESULT TOO_BIG: cannot open cand\n"); return 2; } }
    if (L == 0) {
      Writer<W> wr(D);
      for (const TKey& k : tkeys) wr.put(ROT ? canon<W>(k.c, k.d, k.r) : pack<W>(k.c, k.d, k.r));
      wr.flushAll();
    } else {
      atomic<int> nb{0}; atomic<bool> guardTrip{false};
      auto work = [&]() {
        Writer<W> wr(D); PredExp<W> ex; ex.wr = &wr; ex.height = h - 1;   // distance of the expanded state is h-2; the root edge adds 1
        while (true) {
          if (guardTrip) break;
          if (freeFrac() < FREE_MIN) { guardTrip = true; break; }   // candidates of one layer can be far larger than the cone so far
          int b = nb.fetch_add(1); if (b >= PB) break;
          Reader<W> r(frontPath(L, b)); Key<W> k;
          while (r.peek(k)) { r.adv(); u64 c, d; u128 rr; unpack(k, c, d, rr); ex.expand(c, d, rr); }
        }
        wr.flushAll();
      };
      vector<thread> th; for (int i = 0; i < nth; i++) th.emplace_back(work); for (auto& x : th) x.join();
      if (guardTrip) {
        for (int b = 0; b < PB; b++) { fclose(D->cand[b]); D->cand[b] = nullptr; remove(candPath(b).c_str()); }
        outf("RESULT TOO_BIG at layer %d: disk guard while generating candidates, free %.1f%% < %.0f%% (UNDECIDED)\n", h, 100 * freeFrac(), 100 * FREE_MIN);
        return 2;
      }
    }
    for (int b = 0; b < PB; b++) { fclose(D->cand[b]); D->cand[b] = nullptr; }
    double tgen = chrono::duration<double>(chrono::steady_clock::now() - tg).count();
    if (hitHeight >= 0) {
      for (int b = 0; b < PB; b++) remove(candPath(b).c_str());
      res = 3; finalH = hitHeight; break;
    }
    auto tm = chrono::steady_clock::now();
    vector<u64> newCnt(PB, 0);
    atomic<int> nb2{0};
    auto merge = [&]() {
      while (true) {
        int b = nb2.fetch_add(1); if (b >= PB) break;
        vector<Key<W>> U = readAll<W>(candPath(b));
        remove(candPath(b).c_str());
        sort(U.begin(), U.end(), kless<W>);
        U.erase(unique(U.begin(), U.end(), keq<W>), U.end());
        const BState cur0 = prev[b];
        subtractFile(U, basePath(b, cur0.baseGen)); subtractFile(U, deltaPath(b, cur0.deltaGen));
        newCnt[b] = U.size();
        writeAll<W>(frontPath(h, b), U);
        BState cur = cur0;
        if (!U.empty()) {
          cur.deltaCnt = mergeFiles<W>(deltaPath(b, cur0.deltaGen), frontPath(h, b), deltaPath(b, h)); cur.deltaGen = h;
          if (cur.deltaCnt * 4 > cur.baseCnt) {
            cur.baseCnt = mergeFiles<W>(basePath(b, cur0.baseGen), deltaPath(b, h), basePath(b, h)); cur.baseGen = h;
            cur.deltaCnt = 0; remove(deltaPath(b, h).c_str());
          }
        }
        bs[b] = cur;
      }
    };
    { vector<thread> th; for (int i = 0; i < nth; i++) th.emplace_back(merge); for (auto& x : th) x.join(); }
    double tmerge = chrono::duration<double>(chrono::steady_clock::now() - tm).count();
    u64 nnew = 0; for (u64 x : newCnt) nnew += x;
    V = 0; for (const BState& x : bs) V += x.baseCnt + x.deltaCnt;
    double secs = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    outf("layer %d (distance %d): %llu new, %llu visited, %.1f s (gen %.1f, merge %.1f), maxrss %.2f GB, disk free %.1f%%\n", h, h - 1, (unsigned long long)nnew,
         (unsigned long long)V, secs, tgen, tmerge, rssGB(), 100 * freeFrac());
    if (nnew == 0) { res = 1; finalH = h; break; }
    L = h;
    writeManifest(W, L, V, bs);
    for (int b = 0; b < PB; b++) {
      if (prev[b].baseGen != bs[b].baseGen) remove(basePath(b, prev[b].baseGen).c_str());
      if (prev[b].deltaGen != bs[b].deltaGen) remove(deltaPath(b, prev[b].deltaGen).c_str());
      if (h >= 2) remove(frontPath(h - 1, b).c_str());
    }
    if (V > CAP) { outf("RESULT TOO_BIG at layer %d: %llu states in the cone (cap %llu) (UNDECIDED)\n", h, (unsigned long long)V, (unsigned long long)CAP); res = 2; finalH = h; break; }
    if (freeFrac() < FREE_MIN) { outf("RESULT TOO_BIG at layer %d: disk guard, free %.1f%% < %.0f%% (UNDECIDED)\n", h, 100 * freeFrac(), 100 * FREE_MIN); res = 2; finalH = h; break; }
    if (rssGB() > 200) { outf("RESULT TOO_BIG at layer %d: RSS %.1f GB above 200 GB (UNDECIDED)\n", h, rssGB()); res = 2; finalH = h; break; }
  }
  double secs = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
  if (res == 3) outf("RESULT REACHABLE: the bottom interface reaches a target at height %d (reverse distance %d); %.1f s; maxrss %.2f GB\n", finalH, finalH - 1, secs, rssGB());
  else if (res == 1) outf("RESULT UNREACHABLE (COMPLETE): reverse frontier empty after layer %d; %llu states in the backward cone%s; targets %zu; %.1f s; maxrss %.2f GB\n",
                          finalH, (unsigned long long)V, ROTN > 1 ? " (orbits under the clock shift)" : "", tkeys.size(), secs, rssGB());
  return res;
}

static int setupTask(int T_, const string& pat, const vector<string>& specs) {
  T = T_; NOV = 0;
  if (B > 15 || B < 2 || T > 64 || T < 1 || pat.empty()) { fprintf(stderr, "need 2<=B<=15, 1<=T<=64\n"); return -1; }
  MASK = (T == 64) ? ~0ULL : ((1ULL << T) - 1);
  for (int t = 0; t < T; t++) { ovf[t] = pat[t % pat.size()] - '0'; OVI[t] = -1; if (ovf[t]) OVI[t] = NOV++; }
  if (NOV == 0 || NOV > 32) { fprintf(stderr, "need 1..32 overflow steps per period\n"); return -1; }
  BOTD = 0; BOTR = 0; for (int t = 0; t < T; t++) if (ovf[t]) { BOTD |= 1ULL << t; BOTR |= (u128)1 << (4 * OVI[t]); }
  int p0 = pat.size(); for (int d = 1; d <= (int)pat.size(); d++) if (pat.size() % d == 0) { bool ok = true; for (size_t i = d; i < pat.size(); i++) if (pat[i] != pat[i - d]) { ok = false; break; } if (ok) { p0 = d; break; } }
  CLKP = (T % p0 == 0) ? p0 : T;
  ROT = getenv("ROT") && atoi(getenv("ROT")); ROTP = T; ROTN = 1; ROTK = NOV;
  if (ROT && T % p0 == 0) { ROTP = p0; ROTN = T / p0; ROTK = NOV / ROTN; }
  SPEC = ""; for (const string& s : specs) SPEC += (SPEC.empty() ? "" : ";") + s;
  for (const string& s : specs) {
    if (s == "bands") { for (auto& cy : uniformCycles()) if (T % (int)cy.size() == 0) for (int ph = 0; ph < (int)cy.size(); ph++) addBand(cy, ph); }
    else if (s.rfind("band:", 0) == 0) {            // band:v1,v2,..:phase
      size_t c2 = s.rfind(':'); vector<int> vals; string lst = s.substr(5, c2 - 5); size_t i = 0;
      while (i < lst.size()) { size_t j = lst.find(',', i); if (j == string::npos) j = lst.size(); vals.push_back(atoi(lst.substr(i, j - i).c_str())); i = j + 1; }
      addBand(vals, atoi(s.c_str() + c2 + 1));
    }
    else if (s.rfind("cut:", 0) == 0) {            // cut:L:H:y0,y1,..  one lattice cut key (c = L, d = H, r = digits at the overflow slots in order)
      size_t a = s.find(':', 4), bq = s.find(':', a + 1); u64 Lc = strtoull(s.substr(4, a - 4).c_str(), 0, 10), Hc = strtoull(s.substr(a + 1, bq - a - 1).c_str(), 0, 10);
      u128 r = 0; int j = 0; size_t i = bq + 1;
      while (i <= s.size() && j < NOV) { size_t k2 = s.find(',', i); if (k2 == string::npos) k2 = s.size(); r |= (u128)atoi(s.substr(i, k2 - i).c_str()) << (4 * j); j++; i = k2 + 1; }
      if (j != NOV) { fprintf(stderr, "cut needs %d digits\n", NOV); return -1; }
      tkeys.push_back({Lc & MASK, Hc & MASK, r});
    }
    else if (s.rfind("cutfile:", 0) == 0) {         // cutfile:PATH  lines "L H y0,y1,.." (decimal)
      FILE* cf = fopen(s.c_str() + 8, "r"); if (!cf) { fprintf(stderr, "cannot open %s\n", s.c_str() + 8); return -1; }
      char ln[4096]; size_t nread = 0;
      while (fgets(ln, sizeof ln, cf)) {
        char* p1 = ln; u64 Lc = strtoull(p1, &p1, 10), Hc = strtoull(p1, &p1, 10); u128 r = 0; int j = 0;
        while (*p1 && j < NOV) { while (*p1 == ' ' || *p1 == ',') p1++; if (!*p1 || *p1 == '\n') break; r |= (u128)strtol(p1, &p1, 10) << (4 * j); j++; }
        if (j != NOV) { fprintf(stderr, "cutfile line needs %d digits\n", NOV); return -1; }
        tkeys.push_back({Lc & MASK, Hc & MASK, r}); nread++;
      }
      fclose(cf); outf("cutfile: %zu cut keys read\n", nread);
    }
    else if (s == "allstreams") ALLSTREAMS = true;
    else if (s.rfind("stream:", 0) == 0) addStream(s.substr(7));
    else { fprintf(stderr, "unknown target spec %s\n", s.c_str()); return -1; }
  }
  for (Target* g : targets) tkeys.push_back({g->c, g->c, g->r});
  if (tkeys.empty() && !ALLSTREAMS) { fprintf(stderr, "no targets\n"); return -1; }
  NBITS = 2 * T + 4 * NOV; return (NBITS + 63) / 64;
}

int main(int argc, char** argv) {
  struct rlimit rl; getrlimit(RLIMIT_NOFILE, &rl); rl.rlim_cur = min<rlim_t>(rl.rlim_max, 8192); setrlimit(RLIMIT_NOFILE, &rl);
  if (argc >= 7 && string(argv[1]) == "TEST") {      // backdisk TEST B T CLOCK N seed
    B = atoi(argv[2]); string pat = argv[4]; vector<string> sp = {"bands"};
    int W = setupTask(atoi(argv[3]), pat, sp); if (W < 0) return 2;
    if (getenv("WIN") && atoi(getenv("WIN"))) buildWindowSet(pat, atoi(getenv("WIN")));
    return selfTest(atol(argv[5]), strtoull(argv[6], 0, 10));
  }
  if (argc < 7) { fprintf(stderr, "usage: [THREADS=n] [ROT=1] [PB=bits] backdisk B T CLOCK WORKDIR cap min_free_fraction SPEC...\n  SPEC: bands | band:v1,v2,..:phase | stream:BITS (with all clock shifts)\n  or: backdisk TEST B T CLOCK N seed\n"); return 2; }
  NTH = getenv("THREADS") ? atoi(getenv("THREADS")) : 8; if (NTH < 1) NTH = 1;
  if (getenv("PB")) PBITS = atoi(getenv("PB")); PB = 1 << PBITS;
  B = atoi(argv[1]); string pat = argv[3]; WORK = argv[4];
  CAP = strtoull(argv[5], 0, 10); FREE_MIN = atof(argv[6]);
  vector<string> specs; for (int i = 7; i < argc; i++) specs.push_back(argv[i]);
  int W = setupTask(atoi(argv[2]), pat, specs); if (W < 0) return 2;
  if (getenv("WIN") && atoi(getenv("WIN"))) {
    buildWindowSet(pat, atoi(getenv("WIN"))); SPEC += ";WIN=" + to_string(WW);
    if (ALLSTREAMS) { size_t n0 = tkeys.size(); enumStreams(0, 0, 0); outf("allstreams: %zu 9-wire keys survive the windows\n", tkeys.size() - n0); }
    size_t before = tkeys.size(); vector<TKey> keep;
    for (const TKey& k : tkeys) { bool ok = true; for (int s0 = 0; s0 + WW <= T; s0++) if (!winOK(k.c, k.d, k.r, s0 + WW)) { ok = false; break; } if (ok) keep.push_back(k); }
    tkeys = keep; outf("window filter: %zu of %zu target keys survive\n", tkeys.size(), before);
    if (tkeys.empty()) { outf("RESULT UNREACHABLE (COMPLETE): every target key has a window outside the abstract reachable set (window abstraction w=%d, sound for every T)\n", WW); return 0; }
  }
  if (ALLSTREAMS && !WW) { if (T > 28) { fprintf(stderr, "allstreams without WIN needs T <= 28\n"); return 2; } enumStreams(0, 0, 0); outf("allstreams: %zu 9-wire keys\n", tkeys.size()); }
  if (tkeys.empty()) { outf("RESULT UNREACHABLE (COMPLETE): no target key\n"); return 0; }
  if (mkdir(WORK.c_str(), 0755) != 0 && errno != EEXIST) { fprintf(stderr, "cannot create %s\n", WORK.c_str()); return 2; }
  outf("backdisk B=%d T=%d clock=%s cap=%llu threads=%d keybits=%d words=%d rot=%d(p=%d) buckets=%d workdir=%s targets=%zu spec=%s\n", B, T, pat.c_str(),
       (unsigned long long)CAP, NTH, NBITS, W, ROTN, ROTP, PB, WORK.c_str(), tkeys.size(), SPEC.c_str());
  switch (W) { case 1: run<1>(NTH); break; case 2: run<2>(NTH); break; case 3: run<3>(NTH); break; default: run<4>(NTH); break; }
  return 0;
}
