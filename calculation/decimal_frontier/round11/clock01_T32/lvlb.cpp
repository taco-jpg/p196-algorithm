// lvl.cpp -- round 11b: level-by-level co-reachability windows in sparse storage.
// usage: lvl B CLOCK W DIR threads caplog2 [prevW]
//   without prevW: A_W(ph) = closure of the bottom pattern under the abstract step (exactly wbuild's A_w), and
//                  BB_W(ph) = states of A_W(ph) that reach a target window inside A_W(ph) (exactly bwin's BB_w).
//   with prevW = W-1: the candidate set C(ph) = window contents whose two sub-windows of width W-1 (slots 0..W-2 at phase ph,
//                  slots 1..W-1 at phase ph+1) lie in the stored level family BB'_{W-1}; A'_W(ph) = closure of the bottom pattern
//                  under the abstract step restricted to C(ph); BB'_W(ph) = states of A'_W(ph) that reach a target window in A'_W(ph).
// Writes DIR/lb_B<B>_<CLOCK>_w<W>_ph<ph>.u64 (sorted keys of BB'_W(ph), key layout of winhash.h).
// The abstract step (FILTER_R8 section 1): per-slot rule run from ANY start value x in 0..2B-2, no closing / root condition.
// It is evaluated by subset construction over the set of running values (one DFS branch per distinct output, as wincd.h).
#include "winhash.h"
#include <chrono>
#include <set>
using namespace std;
typedef uint64_t u64;
static int B, W, L, PW = 0; static string PAT;
static vector<wh::HS*> prevT;   // previous level, one table per phase
static int wovf[64], wOVI[64], K;
static int phase;
static u64 MW, MP;   // masks W bits, PW bits
static int kp0, kp1, ovf0;  // overflow slots in sub-window [0,PW), in [1,PW]; wovf[0]

struct Exp {
  // input window
  u64 cc, cd; int cdig[16];
  // output under construction
  u64 cs, ds, rn;
  // mode 0: insert successors into tab, mark new; mode 1: test any successor in M (by slot)
  int mode; wh::HS* tab; const uint8_t* Mbits; bool hit; u64 nNew, nCut;
  inline bool inPrev(int ph, u64 c, u64 d, u64 r) const { return prevT[ph]->has(c | (d << PW) | (r << (2 * PW))); }
  void dfs(int t, uint32_t X) {
    if (hit) return;
    if (PW && t == PW) {   // prefix sub-window [0, PW) complete
      if (!inPrev(phase, cs & MP, ds & MP, rn & ((1ULL << (4 * kp0)) - 1))) { nCut++; return; }
    }
    if (t == W) {
      if (PW) { u64 r1 = (rn >> (4 * ovf0)) & ((1ULL << (4 * kp1)) - 1);
        if (!inPrev((phase + 1) % L, (cs >> 1) & MP, (ds >> 1) & MP, r1)) { nCut++; return; } }
      u64 k = cs | (ds << W) | (rn << (2 * W));
      if (mode == 0) { bool nw; tab->insert(k, &nw); if (nw) nNew++; }
      else { long long s = tab->find(k); if (s >= 0 && Mbits[s]) hit = true; }
      return;
    }
    int cin = (cc >> t) & 1, dneed = (cd >> t) & 1;
    // outputs: (d, co, r) at overflow slots, (d, co) otherwise
    uint32_t nxt[2][2][16]; uint8_t used[2][2][16]; memset(used, 0, sizeof(used));
    for (int x = 0; x <= 2 * B - 2; x++) {
      if (!((X >> x) & 1)) continue;
      for (int d = 0; d < 2; d++) {
        if ((x + d) / B != dneed) continue;
        int e = (x + cin) % B, r = (x + d) % B, co = (x + cin) / B;
        int nx = wovf[t] ? e + cdig[wOVI[t]] : e + r;
        int rk = wovf[t] ? r : 0;
        if (!used[d][co][rk]) { used[d][co][rk] = 1; nxt[d][co][rk] = 0; }
        nxt[d][co][rk] |= 1u << nx;
      }
    }
    for (int d = 0; d < 2; d++) for (int co = 0; co < 2; co++) for (int rk = 0; rk < 16; rk++) {
      if (!used[d][co][rk]) continue;
      u64 sc = cs, sd = ds, sr = rn;
      cs |= (u64)co << t; ds |= (u64)d << t; if (wovf[t]) rn |= (u64)rk << (4 * wOVI[t]);
      dfs(t + 1, nxt[d][co][rk]);
      cs = sc; ds = sd; rn = sr;
      if (hit) return;
    }
  }
  void run(u64 key) {
    cc = key & MW; cd = (key >> W) & MW; u64 rv = key >> (2 * W);
    for (int j = 0; j < K; j++) cdig[j] = (rv >> (4 * j)) & 15;
    cs = ds = rn = 0; hit = false; dfs(0, (1u << (2 * B - 1)) - 1);
  }
};

int main(int argc, char** argv) {
  if (argc < 7) { fprintf(stderr, "usage: lvl B CLOCK W DIR threads caplog2 [prevW]\n"); return 2; }
  B = atoi(argv[1]); PAT = argv[2]; W = atoi(argv[3]); string dir = argv[4]; int nth = atoi(argv[5]); int caplog = atoi(argv[6]);
  if (argc > 7) PW = atoi(argv[7]);
  L = PAT.size(); MW = (1ULL << W) - 1;
  if (PW && PW != W - 1) { fprintf(stderr, "prevW must be W-1\n"); return 2; }
  if (PW) { MP = (1ULL << PW) - 1; prevT.assign(L, nullptr);
    for (int ph = 0; ph < L; ph++) { prevT[ph] = new wh::HS(); if (!wh::loadFile(wh::lname(dir, B, PAT, PW, ph), *prevT[ph], nth)) return 2;
      printf("prev level w=%d ph=%d: %llu windows\n", PW, ph, (unsigned long long)prevT[ph]->n.load()); fflush(stdout); } }
  vector<int> phs; for (int i = 8; i < argc; i++) phs.push_back(atoi(argv[i])); if (phs.empty()) for (int p = 0; p < L; p++) phs.push_back(p);
  for (int ph : phs) {
    auto t0 = chrono::steady_clock::now();
    string out = wh::lname(dir, B, PAT, W, ph);
    { struct stat st; if (stat(out.c_str(), &st) == 0) { printf("w=%d ph=%d exists, skipped\n", W, ph); continue; } }
    phase = ph; K = 0; for (int t = 0; t < W; t++) { wovf[t] = PAT[(ph + t) % L] - '0'; wOVI[t] = wovf[t] ? K++ : -1; }
    if (2 * W + 4 * K > 64) { fprintf(stderr, "key too wide\n"); return 2; }
    ovf0 = wovf[0]; kp0 = 0; kp1 = 0; if (PW) { for (int t = 0; t < PW; t++) kp0 += wovf[t]; for (int t = 1; t <= PW; t++) kp1 += wovf[t]; }
    wh::HS tab; tab.init(1ULL << caplog, nth);
    // seed: bottom pattern c = 0, d = overflow mask, r = 1 at overflow slots
    u64 bd = 0, br = 0; for (int t = 0; t < W; t++) if (wovf[t]) { bd |= 1ULL << t; br |= 1ULL << (4 * wOVI[t]); }
    // r11b lvlb: AIN=dir loads the stored forward closure A'_W(ph) (written by lvl2 with NOBWD=1) instead of recomputing it;
    // only the backward fixpoint (co-reachability inside A'_W(ph)) is run. Result identical to lvl2 without NOBWD.
    const char* ain = getenv("AIN");
    if (ain) { string fn = wh::lname(ain, B, PAT, W, ph); int fd = open(fn.c_str(), O_RDONLY); if (fd < 0) { fprintf(stderr, "missing %s\n", fn.c_str()); return 2; }
      struct stat st; fstat(fd, &st); u64 n = st.st_size / 8; const u64* p = (const u64*)mmap(nullptr, n * 8, PROT_READ, MAP_SHARED, fd, 0); close(fd);
      vector<thread> th; for (int i = 0; i < nth; i++) th.emplace_back([&, i]() { bool nw; for (u64 j = n * i / nth; j < n * (i + 1) / nth; j++) tab.insert(p[j], &nw); });
      for (auto& x : th) x.join(); munmap((void*)p, n * 8);
      printf("loaded A' w=%d ph=%d from %s: %llu windows\n", W, ph, fn.c_str(), (unsigned long long)tab.n.load()); fflush(stdout);
    } else
    { bool nw; tab.insert(0 | (bd << W) | (br << (2 * W)), &nw); }
    uint8_t* flag = (uint8_t*)mmap(nullptr, tab.cap, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0);   // zeroed
    // forward closure: chaotic sweeps over the table (a key inserted behind the sweep pointer is picked up by the next sweep)
    int sweep = 0; u64 cutTot = 0;
    while (!ain) {
      atomic<u64> next{0}, expanded{0}, cut{0}; const u64 CH = 1 << 14;
      auto work = [&]() {
        Exp ex; ex.mode = 0; ex.tab = &tab; ex.nNew = 0; ex.nCut = 0; u64 loc = 0;
        while (true) { u64 a = next.fetch_add(CH); if (a >= tab.cap) break; u64 bnd = min(tab.cap, a + CH);
          for (u64 i = a; i < bnd; i++) { u64 k = __atomic_load_n(&tab.a[i], __ATOMIC_RELAXED); if (k == wh::EMPTY || flag[i]) continue; flag[i] = 1; ex.run(k); loc++; } }
        expanded.fetch_add(loc); cut.fetch_add(ex.nCut); };
      vector<thread> th; for (int i = 0; i < nth; i++) th.emplace_back(work); for (auto& x : th) x.join();
      sweep++; cutTot += cut;
      printf("  [%.0fs] w=%d ph=%d fwd sweep %d: expanded %llu, |A'| %llu, cut by prev level %llu\n", chrono::duration<double>(chrono::steady_clock::now() - t0).count(), W, ph, sweep, (unsigned long long)expanded.load(), (unsigned long long)tab.n.load(), (unsigned long long)cut.load()); fflush(stdout);
      if (expanded.load() == 0) break;
    }
    u64 nA = tab.n.load();
    // r11b NOBWD=1: keep the whole forward closure A'_W(ph) (a superset of BB'_W(ph); still sound as a filter and as the prev level,
    // FINAL.md section 2), i.e. skip the backward fixpoint. All slots of A' are flagged (expanded) at this point.
    bool noBwd = getenv("NOBWD") && atoi(getenv("NOBWD"));
    u64 nt = 0;
    u64 nB = 0; int bs = 0;
    if (!noBwd) {
    memset(flag, 0, tab.cap);
    auto mark = [&](u64 k) { long long s = tab.find(k); if (s >= 0 && !flag[s]) { flag[s] = 1; nt++; } };
    // r11b target classes (env): NOBAND=1 drops band targets, NOWIRE=1 drops wire targets, WAVOID=<0/1 string u> keeps only the
    // wire target windows whose c-part (slot t = bit t) does not contain u as a substring (FINAL.md section 4).
    bool noBand = getenv("NOBAND") && atoi(getenv("NOBAND")), noWire = getenv("NOWIRE") && atoi(getenv("NOWIRE"));
    string av = getenv("WAVOID") ? getenv("WAVOID") : ""; u64 avb = 0; for (size_t i = 0; i < av.size(); i++) if (av[i] == '1') avb |= 1ULL << i;
    auto avoids = [&](u64 c) { int m = av.size(); if (!m) return true; for (int s = 0; s + m <= W; s++) if (((c >> s) & ((1ULL << m) - 1)) == avb) return false; return true; };
    if (!noWire) for (u64 c = 0; c <= MW; c++) { if (!avoids(c)) continue; u64 d = (~c) & MW, rn = 0; for (int t = 0; t < W; t++) if (wovf[t]) rn |= (u64)((B - 1) * ((c >> t) & 1)) << (4 * wOVI[t]); mark(c | (d << W) | (rn << (2 * W))); }
    if (!noBand) { auto f = [&](int v) { int c = v >= B; return 2 * ((v + c) % B); };
      for (int v0 = 0; v0 <= 2 * B - 2; v0++) { int v = v0; for (int i = 0; i < 4 * B; i++) v = f(v);
        vector<int> cy; int u = v; do { cy.push_back(u); u = f(u); } while (u != v && (int)cy.size() <= 2 * B);
        if (u != v) continue; bool bad = false; for (int z : cy) if (z == B - 1) bad = true; if (bad) continue;
        for (int o = 0; o < (int)cy.size(); o++) { u64 c = 0, rn = 0; for (int t = 0; t < W; t++) { int z = cy[(t + o) % cy.size()], cv = z >= B; c |= (u64)cv << t; if (wovf[t]) rn |= (u64)((z + cv) % B) << (4 * wOVI[t]); }
          mark(c | (c << W) | (rn << (2 * W))); } } }
    // backward fixpoint inside A'
    nB = nt;
    while (true) {
      atomic<u64> next{0}, added{0}; const u64 CH = 1 << 14;
      auto work = [&]() { Exp ex; ex.mode = 1; ex.tab = &tab; ex.Mbits = flag; ex.nCut = 0; u64 loc = 0;
        while (true) { u64 a = next.fetch_add(CH); if (a >= tab.cap) break; u64 bnd = min(tab.cap, a + CH);
          for (u64 i = a; i < bnd; i++) { u64 k = tab.a[i]; if (k == wh::EMPTY || __atomic_load_n(&flag[i], __ATOMIC_RELAXED)) continue;
            ex.run(k); if (ex.hit) { __atomic_store_n(&flag[i], 1, __ATOMIC_RELAXED); loc++; } } }
        added.fetch_add(loc); };
      vector<thread> th; for (int i = 0; i < nth; i++) th.emplace_back(work); for (auto& x : th) x.join();
      bs++; nB += added; printf("  [%.0fs] w=%d ph=%d bwd sweep %d: +%llu\n", chrono::duration<double>(chrono::steady_clock::now() - t0).count(), W, ph, bs, (unsigned long long)added.load()); fflush(stdout);
      if (added.load() == 0) break;
    }
    } else nB = nA;
    // write sorted BB' (or A' with NOBWD)
    vector<u64> v; v.reserve(nB); for (u64 i = 0; i < tab.cap; i++) if (tab.a[i] != wh::EMPTY && flag[i]) v.push_back(tab.a[i]);
    sort(v.begin(), v.end());
    { FILE* f = fopen((out + ".tmp").c_str(), "wb"); if (!f || (v.size() && fwrite(v.data(), 8, v.size(), f) != v.size())) { fprintf(stderr, "write failed\n"); return 3; } fclose(f); rename((out + ".tmp").c_str(), out.c_str()); }
    double s = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    printf("LEVEL B=%d clock=%s w=%d ph=%d k=%d prev=%d: |A'|=%llu targets=%llu |BB'|=%llu (%.1f%%) fwd sweeps %d bwd sweeps %d, %.1f s\n",
           B, PAT.c_str(), W, ph, K, PW, (unsigned long long)nA, (unsigned long long)nt, (unsigned long long)v.size(), nA ? 100.0 * v.size() / nA : 0.0, sweep, bs, s); fflush(stdout);
    munmap(flag, tab.cap); tab.release();
  }
  return 0;
}
