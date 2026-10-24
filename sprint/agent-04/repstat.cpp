// repstat.cpp — do realized closed walks come before palindromes?
//
//   repstat SEED_LO SEED_HI STEPS KMIN KMAX
// Per width k: number of seeds whose orbit (t <= STEPS) repeats an outer k-word (first repetition
// t1 < t2), how many of those meet a palindrome at some T > t2, and how many meet no palindrome at
// any T in [1, STEPS]. Also the number of seeds meeting no palindrome at all.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

typedef uint64_t u64;

int main(int argc, char** argv) {
    u64 lo = strtoull(argv[1], 0, 10), hi = strtoull(argv[2], 0, 10);
    int STEPS = atoi(argv[3]), KMIN = atoi(argv[4]), KMAX = atoi(argv[5]);
    const int H = 1024;
    std::vector<u64> key((KMAX + 1) * H);
    std::vector<int> gen((KMAX + 1) * H, -1);
    std::vector<u64> rep(KMAX + 1, 0), rep_pal_after(KMAX + 1, 0), rep_no_pal(KMAX + 1, 0);
    u64 no_pal_seeds = 0;
    std::vector<u64> last_pal_after(STEPS + 2, 0);   // seeds whose last palindrome time is >= tau
    std::vector<std::vector<u64>> t2hist(KMAX + 1, std::vector<u64>(STEPS + 2, 0));
    std::vector<uint8_t> d, tmp;
    int g = 0;
    for (u64 s = lo; s < hi; s++, g++) {
        d.clear(); { u64 x = s; while (x) { d.push_back((uint8_t)(x % 10)); x /= 10; } }
        int t2[16]; bool palafter[16];
        for (int k = 0; k < 16; k++) { t2[k] = -1; palafter[k] = false; }
        bool anypal = false; int lastpal = 0;
        for (int t = 0; t <= STEPS; t++) {
            int L = (int)d.size();
            if (t >= 1) {
                bool pal = true;
                for (int i = 0; i < L / 2; i++) if (d[i] != d[L - 1 - i]) { pal = false; break; }
                if (pal) {
                    anypal = true; lastpal = t;
                    for (int k = KMIN; k <= KMAX; k++) if (t2[k] >= 0 && t > t2[k]) palafter[k] = true;
                }
            }
            for (int k = KMIN; k <= KMAX; k++) {
                if (L < k || t2[k] >= 0) continue;
                u64 c = 0;
                for (int i = k - 1; i >= 0; i--) c = c * 19 + (u64)(d[i] + d[L - 1 - i]);
                u64 h = (c * 0x9E3779B97F4A7C15ULL) >> 54;
                int base = k * H;
                while (true) {
                    int slot = base + (int)h;
                    if (gen[slot] != g) { gen[slot] = g; key[slot] = c; break; }
                    if (key[slot] == c) { t2[k] = t; break; }
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
        if (!anypal) no_pal_seeds++;
        for (int tau = 0; tau <= lastpal; tau++) last_pal_after[tau]++;  // palindrome at some T >= tau
        for (int k = KMIN; k <= KMAX; k++) if (t2[k] >= 0) t2hist[k][t2[k]]++;
        for (int k = KMIN; k <= KMAX; k++) if (t2[k] >= 0) {
            rep[k]++;
            if (palafter[k]) rep_pal_after[k]++;
            if (!anypal) rep_no_pal[k]++;
        }
    }
    printf("seeds [%llu,%llu) steps %d: seeds meeting no palindrome at t in [1,%d]: %llu\n",
           (unsigned long long)lo, (unsigned long long)hi, STEPS, STEPS, (unsigned long long)no_pal_seeds);
    for (int k = KMIN; k <= KMAX; k++)
        printf("k=%d: seeds with a repeated k-word %llu | of these, meeting a palindrome after the repetition %llu | meeting no palindrome at all %llu\n",
               k, (unsigned long long)rep[k], (unsigned long long)rep_pal_after[k], (unsigned long long)rep_no_pal[k]);
    for (int k = KMIN; k <= KMAX; k++) {
        u64 tot = 0; for (int t = 0; t <= STEPS; t++) tot += t2hist[k][t];
        if (!tot) continue;
        u64 acc = 0; int med = -1, mn = -1;
        for (int t = 0; t <= STEPS; t++) { if (t2hist[k][t] && mn < 0) mn = t; acc += t2hist[k][t]; if (med < 0 && 2 * acc >= tot) med = t; }
        // baseline: expected number of the repeating seeds that would meet a palindrome after t2
        // if they behaved like a random seed of the whole range (fraction of all seeds with a palindrome at T > t2)
        double expect = 0;
        for (int t = 0; t <= STEPS; t++) if (t2hist[k][t]) expect += (double)t2hist[k][t] * (double)last_pal_after[t + 1] / (double)(hi - lo);
        printf("k=%d: first-repetition time t2: min %d, median %d; baseline expectation of seeds meeting a palindrome after t2: %.1f\n", k, mn, med, expect);
    }
    for (int tau : {50, 100, 150, 200, 250})
        if (tau <= STEPS) printf("seeds meeting a palindrome at some T >= %d: %llu\n", tau, (unsigned long long)last_pal_after[tau]);
    return 0;
}
