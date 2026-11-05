// r11c census: AC46 two-inlet central cone, single-pass implementation, threaded.
// For each U (30) and each admissible palindromic C of length L, evolve
// S0 = U^K ++ C ++ rev(U^K) for 120 steps under the forced clock (1000)^30,
// keeping only the central part that is identical for both unknown carry
// inlets (sound for every outer context, see AC46 REPORT).  Report the first
// mismatch radius against U^(K+5) ++ C ++ rev(U^(K+5)).
// Survivors (no mismatch anywhere in the protected core) are rerun with K=100.
#include <algorithm>
#include <atomic>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <mutex>
#include <thread>
#include <vector>
#include <map>
#include <array>
#include <string>
using V = std::vector<uint8_t>;
static const uint8_t MOD10[20]={0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9};
static const uint8_t DIV10[20]={0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1};

// returns min mismatch radius, -1 = survivor (core fully matches), -2 = core too small
static int run(const uint8_t *u, const V &c, int K, int *coreOut) {
  int m = (int)c.size();
  V s; s.reserve(6 * K + m + 8);
  for (int i = 0; i < K; i++) for (int j = 0; j < 3; j++) s.push_back(u[j]);
  s.insert(s.end(), c.begin(), c.end());
  for (int i = 0; i < K; i++) for (int j = 2; j >= 0; j--) s.push_back(u[j]);
  V d(s.size()), r(s.size());
  for (int t = 0; t < 120; t++) {
    int g = (t % 4 == 0);
    int M = (int)s.size();
    int cc = 0, p9 = -1;
    for (int i = 0; i < M; i++) if (s[i] != 9) { p9 = i; break; }
    for (int i = 0; i < M; i++) {
      int z = s[i] + cc; d[i] = MOD10[z]; cc = DIV10[z];
    }
    if (p9 < 0) return -2;
    int n = M - g;
    int trim = std::max(0, p9 - g + 1);
    int outn = n - 2 * trim;
    if (outn <= m + 2) return -2;
    for (int j = 0; j < outn; j++) {
      int jj = j + trim;
      r[j] = d[g + jj] + d[M - 1 - jj];
    }
    s.assign(r.begin(), r.begin() + outn);
  }
  int S = (int)s.size();
  if (coreOut) *coreOut = S;
  if ((S - m) % 2) return -3;
  int a = (S - m) / 2;
  int best = 1 << 30;
  for (int j = 0; j < S; j++) {
    int p = j - a, want, rad;
    if (p < 0) { want = u[((p % 3) + 3) % 3]; rad = -p; }
    else if (p < m) { want = c[p]; rad = 0; }
    else { want = u[2 - ((p - m) % 3)]; rad = p - m + 1; }
    if (s[j] != want) best = std::min(best, rad);
  }
  return best == (1 << 30) ? -1 : best;
}

int main(int argc, char **argv) {
  int L = atoi(argv[1]);
  int nth = argc > 2 ? atoi(argv[2]) : 6;
  int K = argc > 3 ? atoi(argv[3]) : 50;
  std::vector<std::array<uint8_t, 3>> us;
  for (int a = 0; a <= 18; a += 2) {
    uint8_t q[3] = {9, (uint8_t)a, (uint8_t)(18 - a)};
    for (int rot = 0; rot < 3; rot++) us.push_back({q[rot], q[(rot + 1) % 3], q[(rot + 2) % 3]});
  }
  int half = (L + 1) / 2;
  long long nc = 1; for (int j = 0; j < half; j++) nc *= 19;
  long long total = (long long)us.size() * nc;
  std::atomic<long long> next(0);
  const long long CH = 4096;
  std::mutex mu;
  std::map<int, long long> hist; long long cases = 0, retries = 0; int minCore = 1 << 30;
  std::vector<std::string> surv;
  auto worker = [&]() {
    std::map<int, long long> h; long long ct = 0, rt = 0; int mc = 1 << 30;
    V c(L);
    while (true) {
      long long st = next.fetch_add(CH);
      if (st >= total) break;
      long long en = std::min(total, st + CH);
      for (long long id = st; id < en; id++) {
        int ui = id / nc; long long code = id % nc, v = code;
        for (int j = 0; j < half; j++) { int x = v % 19; v /= 19; c[j] = c[L - 1 - j] = x; }
        if (L % 2 && (c[half - 1] & 1)) continue;
        int core = 0;
        int res = run(us[ui].data(), c, K, &core);
        if (res < 0 && K < 100) { rt++; res = run(us[ui].data(), c, 100, &core); }
        if (res == -1) {
          std::lock_guard<std::mutex> lk(mu);
          char buf[512]; int o = snprintf(buf, sizeof buf, "SURVIVOR U=%d,%d,%d C=", us[ui][0], us[ui][1], us[ui][2]);
          for (int x : c) o += snprintf(buf + o, sizeof buf - o, "%d,", x);
          surv.push_back(buf); fprintf(stderr, "%s\n", buf);
        }
        h[res]++; ct++; mc = std::min(mc, core);
      }
    }
    std::lock_guard<std::mutex> lk(mu);
    for (auto [k, n] : h) hist[k] += n; cases += ct; retries += rt; minCore = std::min(minCore, mc);
  };
  std::vector<std::thread> th; for (int i = 0; i < nth; i++) th.emplace_back(worker);
  for (auto &t : th) t.join();
  printf("length=%d cases=%lld K=%d retriesK100=%lld min_core=%d hist=", L, cases, K, retries, minCore);
  for (auto [k, n] : hist) printf("%d:%lld,", k, n);
  printf(" survivors=%lld\n", hist.count(-1) ? hist[-1] : 0LL);
  for (auto &s : surv) printf("%s\n", s.c_str());
  return 0;
}
