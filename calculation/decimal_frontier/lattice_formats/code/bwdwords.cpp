// bwdwords: read overflow words (one per line, any length) from stdin or file; decide uniform-band reachability per word.
// usage: bwdwords b [-f1cap N] [-bcap N] [-v] < words
#include "solve.h"
int main(int argc, char** argv) {
  b = atoi(argv[1]); size_t F1 = 5000, B = 20000; bool v = false;
  for (int i = 2; i < argc; i++) { string a = argv[i]; if (a == "-f1cap") F1 = strtoull(argv[++i], 0, 10); else if (a == "-bcap") B = strtoull(argv[++i], 0, 10); else if (a == "-v") v = true; }
  ydig = 1; while ((1 << ydig) < b) ydig++;
  Loops loops = make_loops();
  string w; long nw = 0, nundec = 0, nhit = 0, ndead = 0, nfwd = 0, nbwd = 0, nskip = 0; size_t maxf = 0, maxc = 0;
  while (cin >> w) {
    p = w.size(); u64 gm = 0; for (int t = 0; t < p; t++) if (w[t] == '1') gm |= 1ULL << t;
    int ngc = __builtin_popcountll(gm); if (2 * p + ydig * ngc > 319) { nskip++; printf("SKIP p=%d g=%s\n", p, w.c_str()); continue; }
    SolveRes R = solve_stream(gm, loops, F1, B, v); nw++;
    if (R.startdead) { ndead++; continue; }
    maxf = max(maxf, R.fstates); maxc = max(maxc, R.maxcone);
    if (R.hits) { nhit++; printf("%s", R.hitlines.c_str()); }
    if (R.undecided) { nundec++; printf("%s", R.undeclines.c_str()); }
    if (R.fclosed) nfwd++; else if (!R.undecided) nbwd++;
    fflush(stdout);
  }
  printf("WORDS n=%ld startdead=%ld words_with_hit=%ld words_undecided=%ld decided_by_forward_closure=%ld decided_by_backward_cone=%ld skipped=%ld maxfwd=%zu maxcone=%zu\n", nw, ndead, nhit, nundec, nfwd, nbwd, nskip, maxf, maxc);
}
