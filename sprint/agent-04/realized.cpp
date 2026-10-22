// realized.cpp — prefix obstructions realized entirely by actual integer orbits.
//
//   realized SEED_LO SEED_HI STEPS KMIN KMAX OUT.tsv
// For every seed and every width k in [KMIN, KMAX] (k <= 13), follows the outer k column sums
// word_t of orbit(seed, t) for all t with width >= k, and remembers the first repetition
// word_{t1} = word_{t2} (t1 < t2). That repetition is a closed walk of the forward k-column
// abstraction realized by actual integers (forward edges use the actual carries). Whenever
// orbit(seed, T) is a palindrome (T >= 1, >= 4 digits) and t2 <= T-1, the words
// word_{t1..T-1} give an entry walk and a cycle reaching the initial word word_{T-1} of the
// palindrome's prefix: a cycle obstruction at width k, realized by a single orbit.
// Keeps, per (4-digit prefix, k) and (3-digit prefix, k), the witness with the smallest T - t1.
// Output rows: prefix  k  seed  t1  t2  T
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <tuple>
#include <vector>

typedef uint64_t u64;

struct Wit { u64 seed; int t1, t2, T; };

int main(int argc, char** argv) {
    u64 lo = strtoull(argv[1], 0, 10), hi = strtoull(argv[2], 0, 10);
    int STEPS = atoi(argv[3]), KMIN = atoi(argv[4]), KMAX = atoi(argv[5]);
    const char* out = argv[6];
    const int H = 1024;  // open-addressing table per k (STEPS < H/2)
    std::vector<u64> key((KMAX + 1) * H);
    std::vector<int> val((KMAX + 1) * H), gen((KMAX + 1) * H, -1);
    std::map<std::pair<int, int>, Wit> best;  // (prefix, k) -> witness
    std::vector<uint8_t> d, tmp;
    int g = 0;
    for (u64 s = lo; s < hi; s++, g++) {
        d.clear(); { u64 x = s; while (x) { d.push_back((uint8_t)(x % 10)); x /= 10; } }
        int t1[16], t2[16];
        for (int k = 0; k < 16; k++) t1[k] = t2[k] = -1;
        for (int t = 0; t <= STEPS; t++) {
            int L = (int)d.size();
            if (t >= 1 && L >= 4) {
                bool pal = true;
                for (int i = 0; i < L / 2; i++) if (d[i] != d[L - 1 - i]) { pal = false; break; }
                if (pal) {
                    int P4 = d[L - 1] * 1000 + d[L - 2] * 100 + d[L - 3] * 10 + d[L - 4];
                    int P3 = P4 / 10;
                    for (int k = KMIN; k <= KMAX; k++) {
                        if (t2[k] < 0 || t2[k] > t - 1) continue;
                        for (int P : {P4, P3}) {
                            auto it = best.find({P, k});
                            if (it == best.end() || t - t1[k] < it->second.T - it->second.t1)
                                best[{P, k}] = Wit{s, t1[k], t2[k], t};
                        }
                    }
                }
            }
            for (int k = KMIN; k <= KMAX; k++) {
                if (L < k || t2[k] >= 0) continue;
                u64 c = 0;
                for (int i = k - 1; i >= 0; i--) c = c * 19 + (u64)(d[i] + d[L - 1 - i]);
                u64 h = (c * 0x9E3779B97F4A7C15ULL) >> 54;  // 10 bits
                int base = k * H;
                while (true) {
                    int slot = base + (int)h;
                    if (gen[slot] != g) { gen[slot] = g; key[slot] = c; val[slot] = t; break; }
                    if (key[slot] == c) { t1[k] = val[slot]; t2[k] = t; break; }
                    h = (h + 1) & (H - 1);
                }
            }
            if (t == STEPS) break;
            tmp.resize(L + 1);
            int cc = 0;
            for (int i = 0; i < L; i++) { int x = d[i] + d[L - 1 - i] + cc; tmp[i] = (uint8_t)(x % 10); cc = x / 10; }
            if (cc) { tmp[L] = 1; d.assign(tmp.begin(), tmp.begin() + L + 1); }
            else d.assign(tmp.begin(), tmp.begin() + L);
        }
    }
    FILE* f = fopen(out, "w");
    fprintf(f, "prefix\tk\tseed\tt1\tt2\tT\n");
    for (auto& kv : best)
        fprintf(f, "%d\t%d\t%llu\t%d\t%d\t%d\n", kv.first.first, kv.first.second,
                (unsigned long long)kv.second.seed, kv.second.t1, kv.second.t2, kv.second.T);
    fclose(f);
    printf("wrote %zu witnesses to %s\n", best.size(), out);
    return 0;
}
