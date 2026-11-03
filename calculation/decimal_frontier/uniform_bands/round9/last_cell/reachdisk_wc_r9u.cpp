// reachdisk.cpp -- external-memory version of reachmt.cpp (round 6). Same graph, same targets, same output lines; the visited
// set lives on disk as sorted files per hash bucket, so RAM does not bound the number of states. See DESIGN_R6.md.
// usage: [THREADS=n] [ROT=1] [PB=bits] ./reachdisk B T CLOCK ALL|WIRE WORKDIR [cap] [min_free_fraction]
//   WORKDIR holds scratch and the manifest; re-running with the same arguments resumes from the last finished height.
// Output lines as reachmt: "TARGET band[..] phase p REACHED at height H (BAND='..' PH=p)", "NEW STREAM at height H: ..",
//   "RESULT COMPLETE|EMPTY|TOO_BIG|MAXDEPTH ..".
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
#include <unordered_set>
#include <deque>
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
static atomic<u64> nAccept{0}; static mutex outMx; static set<u64> streams;
static void checkNew(u64 c, u64 d, u128 r, int height) {
  if (c == d) for (Target* g : targets) if (g->c == c && g->r == r) {
    nAccept++;
    int expect = -1;
    if (g->h.compare_exchange_strong(expect, height)) {
      lock_guard<mutex> lk(outMx);
      outf("  TARGET %s phase %d REACHED at height %d  (BAND='%s' PH=%d)\n", g->name.c_str(), g->ph, height, g->spec.c_str(), g->ph);
    }
  }
  if (MODE == 2 || MODE == 0) {
    if (((~c) & MASK) == d) {
      for (int t = 0; t < T; t++) if (ovf[t] && (int)((r >> (4 * OVI[t])) & 15) != (B - 1) * (int)((c >> t) & 1)) return;
      nAccept++;
      lock_guard<mutex> lk(outMx);
      if (!streams.count(c)) {
        streams.insert(c); string s; for (int t = 0; t < T; t++) s += (char)('0' + ((c >> t) & 1));
        outf("  NEW STREAM at height %d: %s\n", height, s.c_str());
      }
    }
  }
}

#include "winbits.h"
#include "wincd.h"
static int WW = 0;
static atomic<u64> wrapViol{0}, cdViol{0}, cdWrapViol{0}, bPruned{0}; static bool BFILT = false;
static atomic<u64> winViol{0}, winChecked{0};
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
template <int W> struct Expander {
  Writer<W>* wr; int height;
  u64 cc, cd; u128 cr; int x0; bool root; u64 cs, ds; u128 rs;
  void leaf() {
    Key<W> k = ROT ? canon<W>(cs, ds, rs) : pack<W>(cs, ds, rs);
    checkNew(cs, ds, rs, height);
    if (WW) { winChecked++; for (int s0 = 0; s0 + WW <= T; s0++) if (!wb::winAt(cs, ds, rs, s0)) { if (winViol++ < 5) outf("WINDOW VIOLATION at height %d, start slot %d: c=%llu d=%llu\n", height, s0, (unsigned long long)cs, (unsigned long long)ds); break; }
      for (int s0 = T - WW + 1; s0 < T; s0++) if (!wb::winWrapAt(cs, ds, rs, s0)) { if (wrapViol++ < 5) outf("WRAP WINDOW VIOLATION at height %d, start slot %d: c=%llu d=%llu\n", height, s0, (unsigned long long)cs, (unsigned long long)ds); break; }
      if (wcd::CW) { int cw = wcd::CW;
        for (int s0 = 0; s0 + cw <= T; s0++) if (!wcd::winAt(cs, ds, s0)) { if (cdViol++ < 5) outf("CD WINDOW VIOLATION at height %d, start slot %d\n", height, s0); break; }
        for (int s0 = T - cw + 1; s0 < T; s0++) if (!wcd::winWrapAt(cs, ds, s0)) { if (cdWrapViol++ < 5) outf("CD WRAP WINDOW VIOLATION at height %d, start slot %d\n", height, s0); break; } } }
    if (BFILT && !wb::allInB(cs, ds, rs)) { bPruned++; return; }   // r9u: no bottom -> target path passes through this successor
    wr->put(k);
  }
  void dfs(int t, int x) {
    if (t == T) { if (x == x0) leaf(); return; }
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
  void expand(u64 c, u64 d, u128 r, bool isRoot) {
    cc = c; cd = d; cr = r; root = isRoot;
    for (x0 = isRoot ? 1 : 0; x0 <= 2 * B - 2; x0++) { cs = ds = 0; rs = 0; dfs(0, x0); }
  }
};

static double rssGB() { struct rusage ru; getrusage(RUSAGE_SELF, &ru); return ru.ru_maxrss / 1e9; }
static double freeFrac() {
  struct statvfs sv; if (statvfs(WORK.c_str(), &sv) != 0) return 0;
  return (double)sv.f_bavail / (double)sv.f_blocks;
}

// ---- manifest: parameters, last finished height, targets, streams, visited count
struct Manifest { int layer = 0; u64 visited = 0; };
static string manifestSig(int W) {
  string s = "B=" + to_string(B) + " T=" + to_string(T) + " nov=" + to_string(NOV) + " W=" + to_string(W) + " mode=" + to_string(MODE) +
             " rot=" + to_string(ROT) + " rotp=" + to_string(ROTP) + " rotn=" + to_string(ROTN) + " rotk=" + to_string(ROTK) + " pb=" + to_string(PB);
  for (int t = 0; t < T; t++) s += ovf[t] ? '1' : '0';
  return s;
}
static void writeManifest(int W, int layer, u64 visited, const vector<BState>& bs) {
  string tmp = P("manifest.tmp"), fin = P("manifest.txt");
  FILE* f = fopen(tmp.c_str(), "w"); if (!f) exit(4);
  fprintf(f, "sig %s\nlayer %d\nvisited %llu\nnacc %llu\n", manifestSig(W).c_str(), layer, (unsigned long long)visited, (unsigned long long)nAccept.load());
  for (size_t b = 0; b < bs.size(); b++) fprintf(f, "bk %zu %d %d %llu %llu\n", b, bs[b].baseGen, bs[b].deltaGen, (unsigned long long)bs[b].baseCnt, (unsigned long long)bs[b].deltaCnt);
  for (size_t i = 0; i < targets.size(); i++) fprintf(f, "target %zu %d\n", i, targets[i]->h.load());
  for (u64 s : streams) fprintf(f, "stream %llu\n", (unsigned long long)s);
  fclose(f); rename(tmp.c_str(), fin.c_str());
}
static bool readManifest(int W, Manifest& m, vector<BState>& bs) {
  FILE* f = fopen(P("manifest.txt").c_str(), "r"); if (!f) return false;
  char line[4096]; bool sigok = false;
  while (fgets(line, sizeof line, f)) {
    if (!strncmp(line, "sig ", 4)) { string s(line + 4); while (!s.empty() && s.back() == '\n') s.pop_back(); sigok = (s == manifestSig(W)); if (!sigok) { fclose(f); outf("RESULT BADTASK: manifest signature differs in %s\n", WORK.c_str()); exit(5); } }
    else if (!strncmp(line, "layer ", 6)) m.layer = atoi(line + 6);
    else if (!strncmp(line, "visited ", 8)) m.visited = strtoull(line + 8, 0, 10);
    else if (!strncmp(line, "nacc ", 5)) nAccept = strtoull(line + 5, 0, 10);
    else if (!strncmp(line, "bk ", 3)) { size_t b; BState st; unsigned long long bc, dc; if (sscanf(line + 3, "%zu %d %d %llu %llu", &b, &st.baseGen, &st.deltaGen, &bc, &dc) == 5 && b < bs.size()) { st.baseCnt = bc; st.deltaCnt = dc; bs[b] = st; } }
    else if (!strncmp(line, "target ", 7)) { size_t i; int h; if (sscanf(line + 7, "%zu %d", &i, &h) == 2 && i < targets.size()) targets[i]->h = h; }
    else if (!strncmp(line, "stream ", 7)) streams.insert(strtoull(line + 7, 0, 10));
  }
  fclose(f); return sigok;
}

// delete scratch left by an uncommitted attempt (no manifest): base/delta/front/cand files of this work directory
static void cleanScratch() {
  DIR* d = opendir(WORK.c_str()); if (!d) return;
  while (struct dirent* e = readdir(d)) {
    string n = e->d_name;
    if (n.rfind("base_", 0) == 0 || n.rfind("delta_", 0) == 0 || n.rfind("front_", 0) == 0 || n.rfind("cand_", 0) == 0) remove(P(n).c_str());
  }
  closedir(d);
}

template <int W> static int run(int nth) {
  auto t0 = chrono::steady_clock::now();
  Disk<W>* D = new Disk<W>(); unique_ptr<Disk<W>> dp(D);
  vector<BState> bs(PB);
  Manifest man; bool resume = readManifest(W, man, bs);
  int L = resume ? man.layer : 0;
  if (!resume) cleanScratch();
  u64 V = 0; for (const BState& x : bs) V += x.baseCnt + x.deltaCnt;
  if (resume) outf("RESUME from height %d (visited %llu)\n", L, (unsigned long long)V);
  int res = -1; int finalH = 0;
  while (res < 0) {
    int h = L + 1;
    vector<BState> prev = bs;  // last committed state; the new state is built next to it and committed by the manifest
    auto tg = chrono::steady_clock::now();
    // 1. candidates of height h
    for (int b = 0; b < PB; b++) { D->cand[b] = fopen(candPath(b).c_str(), "wb"); if (!D->cand[b]) { outf("RESULT TOO_BIG: cannot open cand\n"); return 2; } }
    if (L == 0) {
      Writer<W> wr(D); Expander<W> ex; ex.wr = &wr; ex.height = 1;
      u64 rc = 0, rd = 0; u128 rr = 0;
      for (int t = 0; t < T; t++) if (ovf[t]) { rd |= 1ULL << t; rr |= (u128)1 << (4 * OVI[t]); }
      ex.expand(rc, rd, rr, true); wr.flushAll();
    } else {
      atomic<int> nb{0};
      auto work = [&]() {
        Writer<W> wr(D); Expander<W> ex; ex.wr = &wr; ex.height = h;
        while (true) {
          int b = nb.fetch_add(1); if (b >= PB) break;
          Reader<W> r(frontPath(L, b)); Key<W> k;
          while (r.peek(k)) { r.adv(); u64 c, d; u128 rr; unpack(k, c, d, rr); ex.expand(c, d, rr, false); }
        }
        wr.flushAll();
      };
      vector<thread> th; for (int i = 0; i < nth; i++) th.emplace_back(work); for (auto& x : th) x.join();
    }
    for (int b = 0; b < PB; b++) { fclose(D->cand[b]); D->cand[b] = nullptr; }
    double tgen = chrono::duration<double>(chrono::steady_clock::now() - tg).count();
    // 2. per bucket: dedup, subtract committed base and delta, write the new frontier, extend delta, maybe compact
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
          if (cur.deltaCnt * 4 > cur.baseCnt) {  // compaction: base := base + delta; the new delta file is emptied
            cur.baseCnt = mergeFiles<W>(basePath(b, cur0.baseGen), deltaPath(b, h), basePath(b, h)); cur.baseGen = h;
            cur.deltaCnt = 0; remove(deltaPath(b, h).c_str());
          }
        }
        bs[b] = cur;  // bs holds the new state; prev keeps the committed one
      }
    };
    { vector<thread> th; for (int i = 0; i < nth; i++) th.emplace_back(merge); for (auto& x : th) x.join(); }
    double tmerge = chrono::duration<double>(chrono::steady_clock::now() - tm).count();
    u64 nnew = 0; for (u64 x : newCnt) nnew += x;
    V = 0; for (const BState& x : bs) V += x.baseCnt + x.deltaCnt;
    double secs = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    if (BFILT) outf("[bpruned %llu] ", (unsigned long long)bPruned.load());
    outf("height %d: %llu new, %llu visited, %.1f s (gen %.1f, merge %.1f), maxrss %.2f GB, disk free %.1f%%%s\n", h, (unsigned long long)nnew,
         (unsigned long long)V, secs, tgen, tmerge, rssGB(), 100 * freeFrac(), nAccept ? "  <-- accepting interfaces seen" : "");
    if (nnew == 0) { res = 1; finalH = h; break; }
    // commit: the manifest is the only record of the new generation; superseded files go after it is written
    L = h;
    writeManifest(W, L, V, bs);
    for (int b = 0; b < PB; b++) {
      if (prev[b].baseGen != bs[b].baseGen) remove(basePath(b, prev[b].baseGen).c_str());
      if (prev[b].deltaGen != bs[b].deltaGen) remove(deltaPath(b, prev[b].deltaGen).c_str());
      if (h >= 2) remove(frontPath(h - 1, b).c_str());
    }
    if (V > CAP) { outf("RESULT TOO_BIG at height %d: %llu interfaces visited (cap %llu)\n", h, (unsigned long long)V, (unsigned long long)CAP); res = 2; finalH = h; break; }
    if (freeFrac() < FREE_MIN) { outf("RESULT TOO_BIG at height %d: disk guard, free %.1f%% < %.0f%% (UNDECIDED)\n", h, 100 * freeFrac(), 100 * FREE_MIN); res = 2; finalH = h; break; }
    if (rssGB() > 200) { outf("RESULT TOO_BIG at height %d: RSS %.1f GB above 200 GB (UNDECIDED)\n", h, rssGB()); res = 2; finalH = h; break; }
  }
  int reached = 0; for (Target* g : targets) if (g->h >= 0) reached++;
  double secs = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
  if (res == 1) {
    outf("RESULT COMPLETE: frontier empty after height %d; %llu interfaces reachable%s; band targets reached %d of %zu; distinct wire streams %zu%s; %.1f s; maxrss %.2f GB\n",
         finalH, (unsigned long long)V, ROTN > 1 ? " (orbits under the clock shift)" : "", reached, targets.size(), streams.size(), ROTN > 1 ? " (up to the clock shift)" : "", secs, rssGB());
  } else if (reached) outf("NOTE: band targets reached before stopping: %d\n", reached);
  return res;
}

static int setupTask(int T_, const string& pat, const string& mode) {
  T = T_; NOV = 0; for (Target* g : targets) delete g; targets.clear(); streams.clear(); nAccept = 0;
  MODE = mode == "ALL" ? 0 : mode == "WIRE" ? 2 : -1;
  if (MODE < 0) { fprintf(stderr, "mode must be ALL or WIRE\n"); return -1; }
  if (B > 15 || B < 2 || T > 64 || T < 1 || pat.empty()) { fprintf(stderr, "need 2<=B<=15, 1<=T<=64\n"); return -1; }
  MASK = (T == 64) ? ~0ULL : ((1ULL << T) - 1);
  for (int t = 0; t < T; t++) { ovf[t] = pat[t % pat.size()] - '0'; OVI[t] = -1; if (ovf[t]) OVI[t] = NOV++; }
  if (NOV == 0 || NOV > 32) { fprintf(stderr, "need 1..32 overflow steps per period\n"); return -1; }
  if (MODE == 0) for (auto& cy : uniformCycles()) if (T % (int)cy.size() == 0) for (int ph = 0; ph < (int)cy.size(); ph++) addBand(cy, ph);
  ROT = getenv("ROT") && atoi(getenv("ROT")); ROTP = T; ROTN = 1; ROTK = NOV;
  if (ROT) {
    int p0 = pat.size(); for (int d = 1; d <= (int)pat.size(); d++) if (pat.size() % d == 0) { bool ok = true; for (size_t i = d; i < pat.size(); i++) if (pat[i] != pat[i - d]) { ok = false; break; } if (ok) { p0 = d; break; } }
    if (T % p0 == 0) { ROTP = p0; ROTN = T / p0; ROTK = NOV / ROTN; }
  }
  NBITS = 2 * T + 4 * NOV; return (NBITS + 63) / 64;
}

int main(int argc, char** argv) {
  if (argc < 6) { fprintf(stderr, "usage: [THREADS=n] [ROT=1] [PB=bits] reachdisk B T CLOCK ALL|WIRE WORKDIR [cap] [min_free_fraction]\n"); return 2; }
  struct rlimit rl; getrlimit(RLIMIT_NOFILE, &rl); rl.rlim_cur = min<rlim_t>(rl.rlim_max, 8192); setrlimit(RLIMIT_NOFILE, &rl);
  NTH = getenv("THREADS") ? atoi(getenv("THREADS")) : 8; if (NTH < 1) NTH = 1;
  if (getenv("PB")) PBITS = atoi(getenv("PB")); PB = 1 << PBITS;
  B = atoi(argv[1]); string pat = argv[3]; string mode = argv[4]; WORK = argv[5];
  if (argc > 6) CAP = strtoull(argv[6], 0, 10);
  if (argc > 7) FREE_MIN = atof(argv[7]);
  int W = setupTask(atoi(argv[2]), pat, mode); if (W < 0) return 2;
  if (mkdir(WORK.c_str(), 0755) != 0 && errno != EEXIST) { fprintf(stderr, "cannot create %s\n", WORK.c_str()); return 2; }
  outf("reachdisk B=%d T=%d clock=%s mode=%s cap=%llu threads=%d keybits=%d words=%d rot=%d(p=%d) buckets=%d workdir=%s targets:", B, T, pat.c_str(), mode.c_str(),
       (unsigned long long)CAP, NTH, NBITS, W, ROTN, ROTP, PB, WORK.c_str());
  for (Target* g : targets) outf(" %s/ph%d", g->name.c_str(), g->ph);
  outf("%s\n", " +wire");
  if (getenv("WINCHECK") && atoi(getenv("WINCHECK"))) { WW = atoi(getenv("WINCHECK")); if (!wb::load(getenv("WINDIR") ? getenv("WINDIR") : ".", B, pat, WW, T, NOV)) return 2; }
  if (WW && getenv("BFILT") && atoi(getenv("BFILT"))) { if (!wb::loadB(getenv("WINDIR") ? getenv("WINDIR") : ".")) return 2; BFILT = true; outf("BFILT: forward successors with a window outside the co-reachability windows BB_w are dropped (w=%d, wrapped windows included)\n", WW); }
  if (getenv("CDW") && atoi(getenv("CDW"))) { if (!wcd::load(getenv("WINDIR") ? getenv("WINDIR") : ".", B, pat, atoi(getenv("CDW")), T)) return 2; }
  switch (W) { case 1: run<1>(NTH); break; case 2: run<2>(NTH); break; case 3: run<3>(NTH); break; default: run<4>(NTH); break; }
  if (WW) outf("WINDOW CHECK w=%d: %llu successor states checked against all windows, %llu violations (non-wrapping), %llu violations (wrapping, T-w+1..T-1)\n", WW, (unsigned long long)winChecked.load(), (unsigned long long)winViol.load(), (unsigned long long)wrapViol.load());
  if (BFILT) outf("BFILT pruned %llu successor candidates\n", (unsigned long long)bPruned.load());
  if (wcd::CW) outf("CD WINDOW CHECK w=%d: %llu violations (non-wrapping), %llu violations (wrapping)\n", wcd::CW, (unsigned long long)cdViol.load(), (unsigned long long)cdWrapViol.load());
  return 0;
}
