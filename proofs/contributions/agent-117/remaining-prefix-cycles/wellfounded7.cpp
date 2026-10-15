// Agent #117: the well-founded part of the seven-column backward relation.
//
// Every seven-column long state s = (s_0..s_6), 1 <= s_0 <= 18, 0 <= s_i <= 18, has at
// most two forward images (free inner carry).  A state is BOUNDED if its backward closure
// is finite and acyclic; then rank(p) = 0 if p has no predecessor, else 1 + max rank of
// its predecessors.  Kahn's algorithm over the whole state space (846,207,882 long states
// plus the 10,467 complete short words of width 1..6 with their exact map F) computes the
// bounded part and all ranks at once.  A prefix class (3..7 leading palindrome digits)
// closes at seven columns iff every initial row of the class is bounded; the bound is
// 1 + max rank (the extra 1 is the final carry-free step onto the palindrome).
//
// Output: ranks.bin (uint8 per long state, 255 = unbounded) and a text report.
// Build: g++ -O3 -std=c++17 -o wellfounded7 wellfounded7.cpp ; needs ~2.6 GB RAM.
// Other widths: g++ -O3 -std=c++17 -DK=4 -o wellfounded4 wellfounded7.cpp (K = 4, 5, 6).
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <vector>
#include <map>
#include <array>
#include <algorithm>
#include <string>

#ifndef K
#define K 7
#endif
typedef std::array<int, K> Word;
static constexpr uint64_t pow19(int n) { return n == 0 ? 1ULL : 19ULL * pow19(n - 1); }
static const uint64_t NLONG = 18ULL * pow19(K - 1);  // 846,207,882 for K = 7

static inline uint64_t enc(const int* s) {   // s_0 in 1..18, s_i in 0..18
  uint64_t idx = 0;
  for (int i = K - 1; i >= 1; --i) idx = idx * 19 + s[i];
  return idx * 18 + (s[0] - 1);
}
static inline void dec(uint64_t idx, int* s) {
  s[0] = (int)(idx % 18) + 1; idx /= 18;
  for (int i = 1; i < K; ++i) { s[i] = (int)(idx % 19); idx /= 19; }
}
// forward images of a long state; returns number of distinct images (1 or 2)
static inline int forward(const int* s, uint64_t out[2]) {
  int low[K]; int c = 0;
  for (int i = 0; i < K; ++i) { int v = s[i] + c; low[i] = v % 10; c = v / 10; }
  int n = 0;
  for (int e = 0; e < 2; ++e) {
    int high[K]; int h = e;
    for (int i = K - 1; i >= 0; --i) { int v = s[i] + h; high[i] = v % 10; h = v / 10; }
    int p[K];
    if (h) { p[0] = 1 + low[0]; for (int i = 1; i < K; ++i) p[i] = low[i] + high[i - 1]; }
    else { for (int i = 0; i < K; ++i) p[i] = low[i] + high[i]; }
    uint64_t id = enc(p);
    if (n == 0 || out[0] != id) out[n++] = id;
  }
  return n;
}
// exact map F on a complete word (any width <= 7); returns output word and width
static int Fexact(const std::vector<int>& s, std::vector<int>& out) {
  std::vector<int> d; int c = 0;
  for (int v : s) { int t = v + c; d.push_back(t % 10); c = t / 10; }
  if (c) d.push_back(c);
  int L = (int)d.size(); out.assign(L, 0);
  for (int i = 0; i < L; ++i) out[i] = d[i] + d[L - 1 - i];
  return L;
}

int main(int argc, char** argv) {
  const char* outdir = argc > 1 ? argv[1] : ".";
  // ---- short words
  std::vector<std::vector<int>> shorts; std::map<std::vector<int>, int> shortIdx;
  for (int n = 1; n < K; ++n) {
    if (n == 1) { for (int v = 2; v <= 18; v += 2) { shortIdx[{v}] = (int)shorts.size(); shorts.push_back({v}); } continue; }
    int half = n / 2; std::vector<int> left(half);
    std::vector<int> cnt(half, 0);
    // enumerate left halves: left[0] in 1..18, others 0..18
    bool done = false; for (int i = 0; i < half; ++i) left[i] = (i == 0 ? 1 : 0);
    while (!done) {
      if (n % 2) {
        for (int center = 0; center <= 18; center += 2) {
          std::vector<int> w(left); w.push_back(center);
          for (int i = half - 1; i >= 0; --i) w.push_back(left[i]);
          shortIdx[w] = (int)shorts.size(); shorts.push_back(w);
        }
      } else {
        std::vector<int> w(left); for (int i = half - 1; i >= 0; --i) w.push_back(left[i]);
        shortIdx[w] = (int)shorts.size(); shorts.push_back(w);
      }
      int i = half - 1;
      while (i >= 0) { left[i]++; if (left[i] <= 18) break; left[i] = (i == 0 ? 1 : 0); i--; }
      if (i < 0) done = true;
    }
  }
  const uint64_t NSHORT = shorts.size();
  fprintf(stderr, "short words: %llu\n", (unsigned long long)NSHORT);
  const uint64_t N = NLONG + NSHORT;
  // successor of each short word: encoded as index in [0, N)
  std::vector<uint64_t> shortSucc(NSHORT);
  for (uint64_t i = 0; i < NSHORT; ++i) {
    std::vector<int> o; int L = Fexact(shorts[i], o);
    if (L == K) shortSucc[i] = enc(o.data());
    else shortSucc[i] = NLONG + shortIdx.at(o);
  }
  // ---- arrays
  std::vector<uint16_t> cnt(N, 0);
  std::vector<uint8_t> rank(N, 0);
  fprintf(stderr, "counting predecessors over %llu long states...\n", (unsigned long long)NLONG);
  for (uint64_t i = 0; i < NLONG; ++i) {
    int s[K]; dec(i, s); uint64_t o[2]; int n = forward(s, o);
    for (int j = 0; j < n; ++j) { if (cnt[o[j]] < 65535) cnt[o[j]]++; else { fprintf(stderr, "count overflow\n"); return 1; } }
    if ((i & ((1ULL << 26) - 1)) == 0) fprintf(stderr, "  %.1f%%\n", 100.0 * i / NLONG);
  }
  for (uint64_t i = 0; i < NSHORT; ++i) cnt[shortSucc[i]]++;
  // ---- Kahn
  std::vector<uint32_t> queue; queue.reserve(1 << 24);
  uint64_t processed = 0;
  for (uint64_t i = 0; i < N; ++i) if (cnt[i] == 0) queue.push_back((uint32_t)i);
  fprintf(stderr, "rank-0 states: %zu\n", queue.size());
  size_t head = 0; uint8_t maxRank = 0;
  while (head < queue.size()) {
    uint64_t i = queue[head++]; processed++;
    uint8_t r = rank[i]; if (r > maxRank) maxRank = r;
    uint64_t o[2]; int n;
    if (i < NLONG) { int s[K]; dec(i, s); n = forward(s, o); }
    else { o[0] = shortSucc[i - NLONG]; n = 1; }
    for (int j = 0; j < n; ++j) {
      uint64_t t = o[j];
      if (r + 1 > rank[t]) { if (r + 1 > 254) { fprintf(stderr, "rank overflow\n"); return 1; } rank[t] = (uint8_t)(r + 1); }
      if (--cnt[t] == 0) queue.push_back((uint32_t)t);
    }
    if (head >= (1u << 24) && head * 2 > queue.size()) { queue.erase(queue.begin(), queue.begin() + head); head = 0; }
  }
  fprintf(stderr, "bounded states: %llu (long+short), max rank %u\n", (unsigned long long)processed, maxRank);
  // mark unbounded as 255
  uint64_t boundedLong = 0;
  for (uint64_t i = 0; i < N; ++i) { if (cnt[i] != 0) rank[i] = 255; else if (i < NLONG) boundedLong++; }
  fprintf(stderr, "bounded long states: %llu\n", (unsigned long long)boundedLong);
  // ---- write ranks of long states
  {
    std::string fn = std::string(outdir) + "/ranks" + std::to_string(K) + ".bin";
    FILE* f = fopen(fn.c_str(), "wb"); fwrite(rank.data(), 1, NLONG, f); fclose(f);
  }
  // ---- compact outputs: rank of every long initial row (digits <= 9, s_0 >= 1), in
  // lexicographic order of the K digits (9*10^(K-1) bytes, 255 = unbounded), and the rank of
  // every complete short word (width < K).
  {
    std::string fn = std::string(outdir) + "/rows_rank" + std::to_string(K) + ".bin";
    FILE* f = fopen(fn.c_str(), "wb");
    uint64_t nrows = 9; for (int i = 1; i < K; ++i) nrows *= 10;
    for (uint64_t c = 0; c < nrows; ++c) {
      int s[K]; uint64_t t = c; for (int i = K - 1; i >= 1; --i) { s[i] = t % 10; t /= 10; } s[0] = (int)t + 1;
      fputc(rank[enc(s)], f);
    }
    fclose(f);
    fn = std::string(outdir) + "/short_rank" + std::to_string(K) + ".tsv";
    f = fopen(fn.c_str(), "w");
    for (uint64_t i = 0; i < NSHORT; ++i) {
      for (size_t j = 0; j < shorts[i].size(); ++j) fprintf(f, "%s%d", j ? "," : "", shorts[i][j]);
      fprintf(f, "\t%d\n", (int)rank[NLONG + i]);
    }
    fclose(f);
  }
  // ---- class report: for 3..7 leading digits
  // rows: all long states with all entries <= 9 (s_0 >= 1): 9*10^6 rows.
  // short palindrome words of width 3..6 beginning with the class digits also count.
  std::string fn = std::string(outdir) + "/classes" + std::to_string(K) + ".tsv";
  FILE* rep = fopen(fn.c_str(), "w");
  fprintf(rep, "#digits\tprefix\tclosed\tbound\trows\tbounded_rows\n");
  for (int D = 3; D <= K; ++D) {
    uint64_t nclasses = 9; for (int i = 1; i < D; ++i) nclasses *= 10;
    uint64_t closedCount = 0;
    for (uint64_t c = 0; c < nclasses; ++c) {
      int dg[7]; uint64_t t = c; for (int i = D - 1; i >= 1; --i) { dg[i] = t % 10; t /= 10; } dg[0] = (int)t + 1;
      uint64_t rows = 0, bounded = 0; int maxr = -1; bool closed = true;
      uint64_t tails = 1; for (int i = D; i < K; ++i) tails *= 10;
      for (uint64_t u = 0; u < tails; ++u) {
        int s[K]; for (int i = 0; i < D; ++i) s[i] = dg[i];
        uint64_t v = u; for (int i = K - 1; i >= D; --i) { s[i] = v % 10; v /= 10; }
        uint8_t r = rank[enc(s)]; rows++;
        if (r == 255) closed = false; else { bounded++; if (r > maxr) maxr = r; }
      }
      // short palindromes of width n in [max(3,D) .. 6] beginning with dg[0..D-1]
      for (int n = std::max(3, D); n < K; ++n) {
        int h = (n + 1) / 2; uint64_t combos = 1; for (int i = D; i < h; ++i) combos *= 10;
        for (uint64_t u = 0; u < combos; ++u) {
          std::vector<int> w(n, 0);
          for (int i = 0; i < D && i < h; ++i) w[i] = dg[i];
          uint64_t v = u; for (int i = h - 1; i >= D; --i) { w[i] = v % 10; v /= 10; }
          for (int i = 0; i < n / 2; ++i) w[n - 1 - i] = w[i];
          bool ok = true; for (int i = 0; i < D; ++i) if (w[i] != dg[i]) ok = false;
          if (!ok) continue;
          if (n % 2 && (w[n / 2] % 2)) continue;         // odd centre: no predecessor at all
          auto it = shortIdx.find(w); if (it == shortIdx.end()) continue;  // (w[0]>=1 always)
          uint8_t r = rank[NLONG + it->second]; rows++;
          if (r == 255) closed = false; else { bounded++; if (r > maxr) maxr = r; }
        }
      }
      if (closed) closedCount++;
      if (D <= 5 || closed) {
        fprintf(rep, "%d\t", D); for (int i = 0; i < D; ++i) fprintf(rep, "%d", dg[i]);
        fprintf(rep, "\t%d\t%d\t%llu\t%llu\n", closed ? 1 : 0, closed ? maxr + 1 : -1,
                (unsigned long long)rows, (unsigned long long)bounded);
      }
    }
    fprintf(stderr, "D=%d classes %llu closed %llu\n", D, (unsigned long long)nclasses, (unsigned long long)closedCount);
    fprintf(rep, "#summary\tD=%d\tclasses=%llu\tclosed=%llu\n", D, (unsigned long long)nclasses, (unsigned long long)closedCount);
  }
  fclose(rep);
  return 0;
}
