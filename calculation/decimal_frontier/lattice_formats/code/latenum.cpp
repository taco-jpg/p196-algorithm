// latenum: enumerate SELF-MIRROR absorbing lattices (spatial period m | S, palindromic necklace, axis moving with the overflow stream)
// as periodic orbits of the cyclic row map Phi_g on [0,2b-2]^m, then test each against the position automaton and the start state.
// usage: latenum b g m [-nocone] [-bcap N] [-all]
#include "solve.h"
static int B2;
// next row for cyclic row r (length m), gam flag; returns false if row is neutral (all b-1)
static bool phi(const int* r, int m, int gam, int* out, int* Aout = nullptr, int* Dout = nullptr) {
  int i0 = -1; for (int i = 0; i < m; i++) if (r[i] != b - 1) { i0 = i; break; }
  if (i0 < 0) return false;
  int A[64], D[64];  // A[i] carry into i from below; D[i] carry into i from above
  // ascending: carry out of i0 independent of carry-in
  A[(i0 + 1) % m] = r[i0] >= b ? 1 : 0;
  for (int s = 1; s < m; s++) { int i = (i0 + s) % m, j = (i0 + s + 1) % m; A[j] = (r[i] + A[i]) / b; }
  // now A[i0] set by wrap (j==i0 at s=m-1): consistent
  // descending: carry out of i0 (downwards) independent of carry-in: D[i0-1] = [r[i0]>=b]
  D[(i0 - 1 + m) % m] = r[i0] >= b ? 1 : 0;
  for (int s = 1; s < m; s++) { int i = ((i0 - s) % m + m) % m, j = ((i0 - s - 1) % m + m) % m; D[j] = (r[i] + D[i]) / b; }
  int e[64], f[64];
  for (int i = 0; i < m; i++) { e[i] = (r[i] + A[i]) % b; f[i] = (r[i] + D[i]) % b; }
  for (int i = 0; i < m; i++) out[i] = gam ? e[i] + f[(i - 1 + m) % m] : e[i] + f[i];
  if (Aout) for (int i = 0; i < m; i++) { Aout[i] = A[i]; Dout[i] = D[i]; }
  return true;
}
static FILE* dumpf = nullptr;
static long enumerate(const string& gs, int m, bool cone, size_t BCAP, bool quiet, int& nGenuine, int& nHit, int& nUndec) {
  p = gs.size(); nGenuine = nHit = nUndec = 0;
  g.assign(p, 0); Gidx.clear(); for (int t = 0; t < p; t++) { g[t] = gs[t] == '1'; if (g[t]) Gidx.push_back(t); } ng = Gidx.size();
  if (ng % m != 0) { return 0; }
  int Gc[64]; Gc[0] = 0; for (int t = 0; t < p; t++) Gc[t + 1] = Gc[t] + g[t];
  long found = 0, tested = 0; int top = 2 * b - 1;
  vector<vector<vector<int>>> lattices;   // for output
  set<vector<int>> seen0;
  for (int al = 0; al < m; al++) {
    // orbit representatives of i -> (al - i) mod m
    vector<int> reps, partner(m);
    for (int i = 0; i < m; i++) { partner[i] = ((al - i) % m + m) % m; }
    for (int i = 0; i < m; i++) if (i <= partner[i]) reps.push_back(i);
    int nf = reps.size(); vector<int> val(nf, 0);
    while (true) {
      int r0[64]; for (int q = 0; q < nf; q++) { r0[reps[q]] = val[q]; r0[partner[reps[q]]] = val[q]; }
      tested++;
      // evolve
      int cur[64], nxt[64]; memcpy(cur, r0, sizeof(int) * m); bool ok = true;
      for (int t = 0; t < p && ok; t++) { if (!phi(cur, m, g[t], nxt)) { ok = false; break; } memcpy(cur, nxt, sizeof(int) * m); }
      if (ok && memcmp(cur, r0, sizeof(int) * m) == 0) {
        // exact lattice found; rows t=0..p-1
        vector<vector<int>> rows(p, vector<int>(m));
        memcpy(cur, r0, sizeof(int) * m);
        for (int t = 0; t < p; t++) { for (int i = 0; i < m; i++) rows[t][i] = cur[i]; phi(cur, m, g[t], nxt); memcpy(cur, nxt, sizeof(int) * m); }
        // canonical under translation of positions? lattice anchored => keep; dedupe on row0 string + minimal period
        vector<int> key(r0, r0 + m); key.push_back(-1); for (int t = 0; t < p; t++) for (int i = 0; i < m; i++) key.push_back(rows[t][i]);
        if (!seen0.count(key)) {
          seen0.insert(key); found++;
          // minimal spatial period
          int mp = m; for (int d = 1; d < m; d++) if (m % d == 0) { bool per = true; for (int t = 0; t < p && per; t++) for (int i = 0; i < m && per; i++) if (rows[t][i] != rows[t][(i + d) % m]) per = false; if (per) { mp = d; break; } }
          // column (time) vectors per position: x^{(k)}_t = rows[t][k]
          if (mp == m) nGenuine++;
          if (!quiet) { printf("LATTICE b=%d g=%s m=%d minper=%d alpha=%d rows:", b, gs.c_str(), m, mp, al);
          for (int t = 0; t < p; t++) { printf(" ["); for (int i = 0; i < m; i++) printf("%d%s", rows[t][i], i + 1 < m ? "," : ""); printf("]"); }
          printf("\n"); }
          // build position-automaton states for positions 0..m-1 and validate cycle
          vector<Key> states(m);
          for (int k = 0; k < m; k++) {
            u64 L = 0, H = 0; int Y[64];
            for (int t = 0; t < p; t++) { int A[64], D[64], tmp[64]; phi(rows[t].data(), m, g[t], tmp, A, D); L |= (u64)A[k] << t; int x = rows[t][k]; H |= (u64)((x + D[k]) / b) << t; }
            for (int i = 0; i < ng; i++) { int t = Gidx[i]; int A[64], D[64], tmp[64]; phi(rows[t].data(), m, 1, tmp, A, D); int km = (k - 1 + m) % m; Y[i] = (rows[t][km] + D[km]) % b; }
            states[k] = pack(L, H, Y);
          }
          if (dumpf && mp == m) { fprintf(dumpf, "LAT %d %zu\n", m, (size_t)states.size()); for (int k = 0; k < m; k++) { u64 L, H; int Y[64]; unpack(states[k], L, H, Y); fprintf(dumpf, "%llu %llu", (unsigned long long)L, (unsigned long long)H); for (int i = 0; i < ng; i++) fprintf(dumpf, " %d", Y[i]); fprintf(dumpf, "\n"); } fprintf(dumpf, "ROWS"); for (int t = 0; t < p; t++) for (int i = 0; i < m; i++) fprintf(dumpf, " %d", rows[t][i]); fprintf(dumpf, "\n"); }
          bool valid = true;
          for (int k = 0; k < m && valid; k++) {
            u64 L, H; int Y[64]; unpack(states[k], L, H, Y); bool got = false; const Key& want = states[(k + 1) % m];
            transitions(L, H, Y, false, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { if (pack(L2, H2, Y2) == want) { bool same = true; for (int t = 0; t < p; t++) if (xs[t] != rows[t][k]) same = false; if (same) got = true; } });
            if (!got) valid = false;
          }
          if (!quiet) printf("  automaton-cycle-valid=%d\n", (int)valid);
          if (valid && cone) {
            // multi-target backward cone
            u64 Hst = 0; for (int t = 0; t < p; t++) Hst |= (u64)g[t] << t; int Y0[64]; for (int i = 0; i < ng; i++) Y0[i] = 1;
            vector<Key> startSucc; transitions(0, Hst, Y0, true, [&](u64 L2, u64 H2, int* Y2, int* xs, int* hn) { startSucc.push_back(pack(L2, H2, Y2)); });
            unordered_map<Key, int, KH> seenB; vector<Key> keys; for (int k = 0; k < m; k++) if (!seenB.count(states[k])) { seenB[states[k]] = keys.size(); keys.push_back(states[k]); }
            size_t fb = 0, fe = keys.size(); int d = 0; bool hit = false, capped = false;
            while (fb < fe && !hit && !capped) {
              d++;
              for (size_t i = fb; i < fe && !capped; i++) { u64 L, H; int Y[64]; unpack(keys[i], L, H, Y); preds(L, H, Y, [&](u64 L1, u64 H1, int* Y1) { Key kk = pack(L1, H1, Y1); if (seenB.count(kk)) return; if (keys.size() >= BCAP) { capped = true; return; } seenB[kk] = keys.size(); keys.push_back(kk); }); }
              for (auto& s : startSucc) if (seenB.count(s)) hit = true;
              fb = fe; fe = keys.size();
            }
            if (mp == m) { if (hit) nHit++; else if (capped) nUndec++; }
            if (!quiet) printf("  backward-cone: %s cone=%zu depth=%d\n", hit ? "HIT(start reaches lattice)" : (capped ? "CAPPED" : "CLOSED(no hit)"), keys.size(), d);
          }
        }
      }
      // odometer
      int q = 0; while (q < nf) { if (++val[q] < top) break; val[q] = 0; q++; } if (q == nf) break;
    }
  }
  if (!quiet) printf("DONE b=%d g=%s m=%d S=%d tested=%ld lattices=%ld\n", b, gs.c_str(), m, ng, tested, found);
  return found;
}
#include "dfa.h"
int main(int argc, char** argv) {
  b = atoi(argv[1]); ydig = 1; while ((1 << ydig) < b) ydig++;
  bool cone = true, quiet = false; size_t BCAP = 300000; int mmin = 2, mmax = 64;
  string mode = argv[2];
  for (int i = 3; i < argc; i++) { string a = argv[i]; if (a == "-nocone") cone = false; else if (a == "-bcap") BCAP = strtoull(argv[++i], 0, 10); else if (a == "-q") quiet = true; else if (a == "-mmin") mmin = atoi(argv[++i]); else if (a == "-mmax") mmax = atoi(argv[++i]); }
  if (mode == "word") { string gs = argv[3]; int m = atoi(argv[4]); for (int i = 5; i < argc; i++) { string a = argv[i]; if (a == "-nocone") cone = false; else if (a == "-bcap") BCAP = strtoull(argv[++i], 0, 10); else if (a == "-dump") dumpf = fopen(argv[++i], "a"); } int a1, a2, a3; enumerate(gs, m, cone, BCAP, false, a1, a2, a3); return 0; }
  // scan: latenum b scan pmin pmax [-mmax M] [-nocone] [-q]
  int pmin = atoi(argv[3]), pmax = atoi(argv[4]);
  for (int i = 5; i < argc; i++) { string a = argv[i]; if (a == "-nocone") cone = false; else if (a == "-bcap") BCAP = strtoull(argv[++i], 0, 10); else if (a == "-q") quiet = true; else if (a == "-mmin") mmin = atoi(argv[++i]); else if (a == "-mmax") mmax = atoi(argv[++i]); }
  Dfa dfa(b);
  for (int pp = pmin; pp <= pmax; pp++) {
    p = pp; vector<u64> streams = dfa.gen(pp, false); long wl = 0, gl = 0; auto t0 = chrono::steady_clock::now();
    for (u64 gm : streams) {
      string gs; for (int t = 0; t < pp; t++) gs += char('0' + ((gm >> t) & 1));
      int Sx = __builtin_popcountll(gm); p = pp;
      for (int m = mmin; m <= mmax && m <= Sx; m++) { if (Sx % m) continue; int ngq, nh, nu; long f = enumerate(gs, m, cone, BCAP, true, ngq, nh, nu); if (ngq) { wl++; gl += ngq; printf("SCANHIT p=%d g=%s S=%d m=%d genuine_lattices=%d reach_hit=%d undecided=%d\n", pp, gs.c_str(), Sx, m, ngq, nh, nu); fflush(stdout); } }
    }
    double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    printf("SCANSUM b=%d p=%d words=%zu words_with_genuine_lattice(m in [%d,%d])=%ld lattices=%ld time=%.1fs\n", b, pp, streams.size(), mmin, mmax, wl, gl, el); fflush(stdout);
  }
}
