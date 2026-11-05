// wbuild.cpp -- r9u: build the bitset window sets A_w(ph) (winbits.h) for one clock word, all phases, and write them to DIR.
// usage: wbuild B CLOCK w DIR threads [ph ...]
#include "winbits.h"
#include "wincd.h"
#include <chrono>
int main(int argc, char** argv) {
  if (argc < 6) { fprintf(stderr, "usage: [CD=1] wbuild B CLOCK w DIR threads [ph...]\n"); return 2; }
  bool cd = getenv("CD") && atoi(getenv("CD"));
  int B = atoi(argv[1]); std::string pat = argv[2]; int w = atoi(argv[3]); std::string dir = argv[4]; int nth = atoi(argv[5]);
  std::vector<int> phs; for (int i = 6; i < argc; i++) phs.push_back(atoi(argv[i]));
  if (phs.empty()) for (int ph = 0; ph < (int)pat.size(); ph++) phs.push_back(ph);
  wb::initGeom(B, pat, w);
  for (int ph : phs) {
    auto t0 = std::chrono::steady_clock::now();
    std::string fn = cd ? wcd::fname(dir, B, pat, w, ph) : wb::fname(dir, B, pat, w, ph);
    struct stat st; if (stat(fn.c_str(), &st) == 0) { printf("window w=%d phase %d: exists, skipped\n", w, ph); continue; }
    wb::u64 n = cd ? wcd::buildPhase(B, pat, w, ph, nth, fn) : wb::buildPhase(B, pat, w, ph, nth, fn);
    double s = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    printf("window filter%s: w=%d phase %d: %llu abstract states (k=%d, %.1f s)\n", cd ? " (c,d only)" : "", w, ph, (unsigned long long)n, wb::wk[ph], s); fflush(stdout);
  }
  return 0;
}
