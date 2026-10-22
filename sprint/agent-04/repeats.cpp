// repeats.cpp — realized closed walks of the k-column abstraction along ONE orbit.
//
//   repeats SEED STEPS KMIN KMAX
// Follows orbit(SEED, t), t <= STEPS. For each width k (<= 13) and every t with width >= k,
// looks up the last time the same outer k-column word occurred. Reports per k: number of times
// t at which word_t had occurred before, the first such repetition (t1, t2), the shortest gap
// t2 - t1 over the whole orbit (with its t1), and the palindromes met (time, first digits).
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <unordered_map>
#include <vector>

typedef uint64_t u64;

int main(int argc, char** argv) {
    std::string seed = argv[1];
    int STEPS = atoi(argv[2]), KMIN = atoi(argv[3]), KMAX = atoi(argv[4]);
    std::vector<uint8_t> d, tmp;
    for (int i = (int)seed.size() - 1; i >= 0; i--) d.push_back((uint8_t)(seed[i] - '0'));
    std::vector<std::unordered_map<u64, int>> last(KMAX + 1);
    std::vector<long long> nrep(KMAX + 1, 0);
    std::vector<int> f1(KMAX + 1, -1), f2(KMAX + 1, -1), mg(KMAX + 1, 1 << 30), mgt(KMAX + 1, -1);
    int npal = 0;
    for (int t = 0; t <= STEPS; t++) {
        int L = (int)d.size();
        bool pal = true;
        for (int i = 0; i < L / 2; i++) if (d[i] != d[L - 1 - i]) { pal = false; break; }
        if (pal && t >= 1) {
            npal++;
            if (npal <= 20) {
                printf("palindrome at t=%d width %d starts ", t, L);
                for (int i = 0; i < 6 && i < L; i++) printf("%d", d[L - 1 - i]);
                printf("\n");
            }
        }
        for (int k = KMIN; k <= KMAX; k++) {
            if (L < k) continue;
            u64 c = 0;
            for (int i = k - 1; i >= 0; i--) c = c * 19 + (u64)(d[i] + d[L - 1 - i]);
            auto it = last[k].find(c);
            if (it != last[k].end()) {
                nrep[k]++;
                if (f1[k] < 0) { f1[k] = it->second; f2[k] = t; }
                if (t - it->second < mg[k]) { mg[k] = t - it->second; mgt[k] = it->second; }
                it->second = t;
            } else last[k][c] = t;
        }
        if (t == STEPS) break;
        tmp.resize(L + 1);
        int cc = 0;
        for (int i = 0; i < L; i++) { int x = d[i] + d[L - 1 - i] + cc; tmp[i] = (uint8_t)(x % 10); cc = x / 10; }
        if (cc) { tmp[L] = 1; d.assign(tmp.begin(), tmp.begin() + L + 1); }
        else d.assign(tmp.begin(), tmp.begin() + L);
    }
    printf("seed %s, steps %d, final width %zu, palindromes met (t>=1): %d\n", seed.c_str(), STEPS, d.size(), npal);
    for (int k = KMIN; k <= KMAX; k++)
        printf("k=%d: distinct words %zu, repeated visits %lld, first repetition t1=%d t2=%d, shortest gap %s (from t=%d)\n",
               k, last[k].size(), nrep[k], f1[k], f2[k], mgt[k] < 0 ? "none" : std::to_string(mg[k]).c_str(), mgt[k]);
    return 0;
}
