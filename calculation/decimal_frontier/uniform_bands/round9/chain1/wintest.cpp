// wintest.cpp -- round 9: which alignments of a periodic 9-wire stream (c = word, d = complement, r = (B-1) c at overflow slots)
// have every window inside the winbits sets. An alignment with a window outside its phase set is unreachable for EVERY period T
// (window abstraction, T-independent). Phases whose file is missing are skipped (treated as "inside": sound, less pruning).
// usage: wintest B CLOCK w PREFIX WORD...
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>
using namespace std; typedef uint64_t u64;
int main(int argc, char** argv) {
  int B = atoi(argv[1]); string pat = argv[2]; int w = atoi(argv[3]); string pre = argv[4]; int P = pat.size();
  vector<vector<u64>> S(P); vector<int> nvp(P), have(P, 0);
  for (int ph = 0; ph < P; ph++) {
    int nv = 0; for (int t = 0; t < w; t++) if (pat[(ph + t) % P] == '1') nv++; nvp[ph] = nv;
    u64 U = 1ULL << (2 * w); for (int j = 0; j < nv; j++) U *= B; u64 NW = (U + 63) / 64;
    string fn = pre + "_ph" + to_string(ph) + ".bin"; FILE* f = fopen(fn.c_str(), "rb"); if (!f) { printf("phase %d: no file, skipped\n", ph); continue; }
    char hdr[64], want[64]; memset(want, 0, 64); snprintf(want, 64, "WINBITS1 %d %d %d %s", B, w, nv, pat.c_str());
    if (fread(hdr, 1, 64, f) != 64 || memcmp(hdr, want, 64)) { printf("bad header %s\n", fn.c_str()); return 2; }
    S[ph].resize(NW); if (fread(S[ph].data(), 8, NW, f) != NW) { printf("short %s\n", fn.c_str()); return 2; } fclose(f); have[ph] = 1;
  }
  for (int a = 5; a < argc; a++) {
    string word = argv[a]; int L = word.size(); int per = L; // test every alignment o of the word against the clock (slot s has clock phase s mod P)
    int lcm = L; while (lcm % P) lcm += L;
    for (int o = 0; o < L; o++) {
      int bad = -1, badph = -1;
      for (int s = 0; s < lcm && bad < 0; s++) {          // window starting at slot s
        int ph = s % P; if (!have[ph]) continue;
        u64 c = 0, d = 0, rn = 0; vector<int> rd;
        for (int t = 0; t < w; t++) { int bit = word[(o + s + t) % L] - '0'; c |= (u64)bit << t; d |= (u64)(1 - bit) << t; if (pat[(s + t) % P] == '1') rd.push_back((B - 1) * bit); }
        for (int j = (int)rd.size() - 1; j >= 0; j--) rn = rn * B + rd[j];
        u64 idx = c | (d << w) | (rn << (2 * w));
        if (!((S[ph][idx >> 6] >> (idx & 63)) & 1)) { bad = s; badph = ph; }
      }
      printf("word %s alignment %d: %s", word.c_str(), o, bad < 0 ? "all windows IN (not excluded)\n" : "EXCLUDED");
      if (bad >= 0) printf(" (window at slot %d, phase %d)\n", bad, badph);
    }
  }
  return 0;
}
