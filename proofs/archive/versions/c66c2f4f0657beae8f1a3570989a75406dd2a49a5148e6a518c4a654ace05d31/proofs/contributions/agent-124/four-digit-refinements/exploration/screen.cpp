// Untrusted exploratory screener (Agent #124): for three-digit prefixes abc,
// compute the backward closure of all width-k initial words under the exact
// complete prefix inverse (Agent #104's prefixPredecessors relation, mirrored
// from verify_certificates.py) plus exact short-source edges, detecting cycles
// with an iterative DFS and memoizing ranks (longest backward path) globally.
// A prefix is CERTIFIABLE at width k iff its closure is finite and acyclic;
// then bound = 1 + max rank over its initial words.  CYCLE means the width-k
// abstraction cannot certify that prefix (it does NOT show an unbounded
// ancestry); CAP means unknown.
//
// Usage: screen K CAP < prefixes.txt   (one prefix per line, e.g. 739)
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
#include <algorithm>
using namespace std;
typedef uint64_t u64;

static int K;
// word code: base-19 digits with leading marker 1 (same as Lean wordCode)
static inline u64 push(u64 c, int d) { return c * 19 + d; }
static inline int wlen(u64 c) { int n = 0; while (c >= 19) { c /= 19; n++; } return n; }
static void decode(u64 c, vector<int>& w) {
  w.clear();
  while (c >= 19) { w.push_back(int(c % 19)); c /= 19; }
  reverse(w.begin(), w.end());
}
static u64 encode(const vector<int>& w) { u64 c = 1; for (int d : w) c = push(c, d); return c; }

struct Loc { int s, xx, yy; };
static vector<Loc> LOCAL[19][2][2];

// complete prefix inverse (no-overflow branch + overflow branch)
static void prefixPred(const vector<int>& p, vector<u64>& out) {
  struct St { u64 c; int x, y; };
  vector<St> a{{1, 0, 0}}, b;
  for (size_t i = 0; i < p.size(); i++) {
    b.clear();
    for (auto& z : a)
      for (auto& v : LOCAL[p[i]][z.x][z.y])
        if (i || v.s > 0) b.push_back({push(z.c, v.s), v.xx, v.yy});
    a.swap(b);
    if (a.empty()) break;
  }
  for (auto& z : a) out.push_back(z.c);
  if (p[0] > 10 || p[0] == 0) return;
  int first = p[0] <= 9 ? p[0] + 9 : 9;
  struct St2 { u64 c; int last, x, y; };
  vector<St2> A{{push(1, first), first, first / 10, 1}}, B;
  for (size_t i = 1; i < p.size(); i++) {
    B.clear();
    for (auto& z : A)
      for (int yy = 0; yy < 2; yy++) {
        if ((z.last + yy) / 10 != z.y) continue;
        int d = p[i] - z.last - yy + 10 * z.y;
        if (d < 0 || d > 9) continue;
        for (int xx = 0; xx < 2; xx++) {
          int s = d + 10 * xx - z.x;
          if (s >= 0 && s <= 18) B.push_back({push(z.c, s), s, xx, yy});
        }
      }
    A.swap(B);
    if (A.empty()) break;
  }
  for (auto& z : A) {
    int s = z.last;
    if (s / 10 == z.y || (s + 1) / 10 == z.y) out.push_back(z.c);
  }
}

// exact next state of a full short word (as Lean nextWord)
static void nextFull(const vector<int>& s, vector<int>& out) {
  vector<int> d; int carry = 0;
  for (int u : s) { int t = u + carry; d.push_back(t % 10); carry = t / 10; }
  if (carry) d.push_back(carry);
  int n = d.size(); out.assign(n, 0);
  for (int i = 0; i < n; i++) out[i] = d[i] + d[n - 1 - i];
}

static unordered_map<u64, vector<u64>> SHORTBACK;  // image code -> short sources
static void genShort(int n, vector<int>& half, int pos) {
  int h = (n + 1) / 2;
  if (pos == h) {
    vector<int> w(n);
    for (int i = 0; i < n; i++) w[i] = half[min(i, n - 1 - i)];
    if (w[0] == 0) return;
    if (n % 2 == 1 && w[n / 2] % 2) return;
    vector<int> img; nextFull(w, img);
    SHORTBACK[encode(img)].push_back(encode(w));
    return;
  }
  for (int v = 0; v < 19; v++) { half[pos] = v; genShort(n, half, pos + 1); }
}

// memo: rank >= 0 done; -1 on stack; -2 cyclic/infinite
static unordered_map<u64, int> RANK;
static size_t CAP;

static void parents(u64 c, vector<u64>& ps) {
  ps.clear();
  auto it = SHORTBACK.find(c);
  if (it != SHORTBACK.end()) ps = it->second;
  vector<int> w; decode(c, w);
  if ((int)w.size() == K) prefixPred(w, ps);
}

// returns rank, -2 for cycle, -3 for cap
static int rankOf(u64 root) {
  auto f = RANK.find(root);
  if (f != RANK.end()) return f->second == -1 ? -2 : f->second;
  struct Fr { u64 c; vector<u64> ps; size_t i; int best; };
  vector<Fr> st;
  st.push_back({root, {}, 0, -1});
  parents(root, st.back().ps);
  RANK[root] = -1;
  while (!st.empty()) {
    Fr& fr = st.back();
    if (fr.i < fr.ps.size()) {
      u64 q = fr.ps[fr.i++];
      auto g = RANK.find(q);
      if (g == RANK.end()) {
        if (RANK.size() > CAP) { for (auto& x : st) RANK.erase(x.c); return -3; }
        RANK[q] = -1;
        Fr nf{q, {}, 0, -1};
        parents(q, nf.ps);
        st.push_back(std::move(nf));
        continue;
      }
      if (g->second < 0) {  // on stack (-1) or known cyclic (-2)
        for (auto& x : st) RANK[x.c] = -2;
        return -2;
      }
      fr.best = max(fr.best, g->second);
    } else {
      int r = fr.best + 1;  // best=-1 -> rank 0
      RANK[fr.c] = r;
      st.pop_back();
      if (!st.empty()) st.back().best = max(st.back().best, r);
      else return r;
    }
  }
  return -4;
}

int main(int argc, char** argv) {
  K = argc > 1 ? atoi(argv[1]) : 7;
  CAP = argc > 2 ? strtoull(argv[2], 0, 10) : 10000000;
  for (int p = 0; p < 19; p++) for (int x = 0; x < 2; x++) for (int y = 0; y < 2; y++)
    for (int s = 0; s < 19; s++) for (int yy = 0; yy < 2; yy++)
      if ((s + yy) / 10 == y && 2 * s + x + yy - 10 * ((s + x) / 10 + y) == p)
        LOCAL[p][x][y].push_back({s, (s + x) / 10, yy});
  for (int n = 1; n < K; n++) { vector<int> half((n + 1) / 2); genShort(n, half, 0); }
  string line;
  while (getline(cin, line)) {
    if (line.empty()) continue;
    int abc = stoi(line);
    int a = abc / 100, b = abc / 10 % 10, c = abc % 10;
    vector<u64> init;
    // long initial words: abc + (K-3) digits
    {
      vector<u64> cur{encode({a, b, c})};
      for (int i = 3; i < K; i++) {
        vector<u64> n; for (u64 z : cur) for (int d = 0; d < 10; d++) n.push_back(push(z, d));
        cur.swap(n);
      }
      init = cur;
    }
    // short palindromic digit targets of widths 3..K-1 with even odd center
    for (int n = 3; n < K; n++) {
      int h = (n + 1) / 2;
      vector<int> half(h);
      long tot = 1; for (int i = 0; i < h; i++) tot *= 10;
      for (long m = 0; m < tot; m++) {
        long t = m; for (int i = h - 1; i >= 0; i--) { half[i] = t % 10; t /= 10; }
        vector<int> w(n); for (int i = 0; i < n; i++) w[i] = half[min(i, n - 1 - i)];
        if (w[0] != a || w[1] != b || w[2] != c) continue;
        if (n % 2 == 1 && w[n / 2] % 2) continue;
        init.push_back(encode(w));
      }
    }
    int best = -1; string status = "CERTIFIABLE";
    for (u64 w : init) {
      int r = rankOf(w);
      if (r == -2) { status = "CYCLE"; break; }
      if (r == -3) { status = "CAP"; break; }
      best = max(best, r);
    }
    printf("{\"prefix\":%d,\"width\":%d,\"status\":\"%s\",\"bound\":%d,\"memo\":%zu}\n",
           abc, K, status.c_str(), status == "CERTIFIABLE" ? best + 1 : -1, RANK.size());
    fflush(stdout);
  }
}
