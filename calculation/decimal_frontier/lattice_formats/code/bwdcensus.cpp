// bwdcensus: for every overflow necklace of period p (position-0 language DFA), decide whether a UNIFORM absorbing band
// (loops of k -> 2*((k+[k>=b])%b), k != b-1) is reachable from the start state of the position automaton.
// usage: bwdcensus b pmin pmax [-f1cap N] [-bcap N] [-g stream] [-v] [-und file]
#include "solve.h"
#include "dfa.h"
int main(int argc, char** argv) {
  b = atoi(argv[1]); int pmin = atoi(argv[2]), pmax = atoi(argv[3]);
  size_t F1 = 5000, B = 20000; string gfix, undfile, dumpw; bool v = false; int part_i = 0, part_n = 1; bool genonly = false;
  for (int i = 4; i < argc; i++) { string a = argv[i]; if (a == "-f1cap") F1 = strtoull(argv[++i], 0, 10); else if (a == "-bcap") B = strtoull(argv[++i], 0, 10); else if (a == "-g") gfix = argv[++i]; else if (a == "-v") v = true; else if (a == "-und") undfile = argv[++i]; else if (a == "-dumpw") dumpw = argv[++i]; else if (a == "-genonly") genonly = true; else if (a == "-part") { part_i = atoi(argv[++i]); part_n = atoi(argv[++i]); } }
  ydig = 1; while ((1 << ydig) < b) ydig++;
  Loops loops = make_loops();
  fprintf(stderr, "b=%d loops:", b); for (auto& l : loops.v) { fprintf(stderr, " {"); for (int x : l) fprintf(stderr, "%d ", x); fprintf(stderr, "}"); } fprintf(stderr, "\n");
  Dfa* dfa = nullptr; if (gfix.empty()) dfa = new Dfa(b);
  FILE* uf = undfile.empty() ? nullptr : fopen(undfile.c_str(), "a");
  FILE* wf = dumpw.empty() ? nullptr : fopen(dumpw.c_str(), "a");
  for (p = pmin; p <= pmax; p++) {
    vector<u64> streams;
    if (!gfix.empty()) { if ((int)gfix.size() != p) continue; u64 gv = 0; for (int t = 0; t < p; t++) if (gfix[t] == '1') gv |= 1ULL << t; streams.push_back(gv); }
    else streams = dfa->gen(p, false);
    long nst = streams.size(), nskip = 0, ndead = 0, nfc = 0, nbc = 0, nund = 0, nhitw = 0, targets = 0, undt = 0, hitt = 0; size_t maxf = 0, maxc = 0; int maxd = 0;
    auto t0 = chrono::steady_clock::now();
    long sidx = -1;
    for (u64 gm : streams) {
      sidx++; if (sidx % part_n != part_i) continue;
      int ngc = __builtin_popcountll(gm); if (2 * p + ydig * ngc > 319) { nskip++; continue; }
      if (wf) { string gs; for (int t = 0; t < p; t++) gs += char('0' + ((gm >> t) & 1)); fprintf(wf, "%s\n", gs.c_str()); fflush(wf); }
      if (genonly) continue;
      SolveRes R = solve_stream(gm, loops, F1, B, v);
      if (R.startdead) { ndead++; continue; }
      targets += R.targets; maxf = max(maxf, R.fstates); maxc = max(maxc, R.maxcone); maxd = max(maxd, R.maxdepth);
      if (R.hits) { nhitw++; hitt += R.hits; printf("%s", R.hitlines.c_str()); }
      if (R.undecided) { nund++; undt += R.undecided; printf("%s", R.undeclines.c_str()); if (uf) { string gs; for (int t = 0; t < p; t++) gs += char('0' + ((gm >> t) & 1)); fprintf(uf, "%s\n", gs.c_str()); fflush(uf); } }
      else if (R.fclosed) nfc++; else nbc++;
      fflush(stdout);
    }
    double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    printf("SUMMARY b=%d p=%d words=%ld startdead=%ld targets=%ld words_hit=%ld hit_targets=%ld words_undecided=%ld undecided_targets=%ld decided_by_fwd_closure=%ld decided_by_bwd_cone=%ld skipped=%ld maxfwd=%zu maxcone=%zu maxbdepth=%d time=%.1fs\n", b, p, nst, ndead, targets, nhitw, hitt, nund, undt, nfc, nbc, nskip, maxf, maxc, maxd, el);
    fflush(stdout);
  }
}
