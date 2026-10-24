// scan.cpp — forward scan of real reverse-and-add orbits, projected to the k-column abstraction.
//
//   scan DATADIR SEED_LO SEED_HI STEPS OUT_PREFIX
// For every seed in [SEED_LO, SEED_HI) runs STEPS reverse-and-add steps (orbits continue past
// palindromes, as in the brief's forward witness scan) and, for k = 4..7 (inf_k.bits from
// `kcol global`):
//   * checks at every step with width L >= k that forwardPrefix(word_t, e_t) == word_{t+1},
//     where word_t = outer k column sums of orbit(seed, t) and e_t = the actual low-scan carry
//     into column L-k  (validation of the abstraction against real integers);
//   * records the entry time into I_k (first t with L_t >= k and word_t in I_k), relative to the
//     first time t0 with L_t >= k;  checks that I_k is never left again;
//   * records the first repeated k-word (a closed walk of the abstraction realized by the orbit).
// For every palindrome orbit(seed, T), T >= 1, with >= 4 digits: per 4-digit prefix the max T
// (and its seed), and whether the last predecessor's k-word lies in I_k.
// Outputs OUT_PREFIX.prefix.tsv and OUT_PREFIX.summary.txt.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <unordered_map>
#include <vector>

typedef uint64_t u64;
static u64 P19[10];
static std::vector<u64> bits[8];
static bool inI(int k, u64 c) { return (bits[k][c >> 6] >> (c & 63)) & 1; }

static u64 encode(const int* q, int k) { u64 c = 0; for (int i = k - 1; i >= 0; i--) c = c * 19 + (u64)q[i]; return c; }
static u64 fwd(const int* q, int K, int e) {
    int lo[10], hi[10], p[10];
    int cc = 0;
    for (int i = 0; i < K; i++) { int t = q[i] + cc; lo[i] = t % 10; cc = t / 10; }
    int h = e;
    for (int i = K - 1; i >= 0; i--) { int t = q[i] + h; hi[i] = t % 10; h = t / 10; }
    if (h == 0) { for (int i = 0; i < K; i++) p[i] = lo[i] + hi[i]; }
    else { p[0] = lo[0] + 1; for (int i = 1; i < K; i++) p[i] = lo[i] + hi[i - 1]; }
    return encode(p, K);
}

// digits little-endian: d[0] units, d[L-1] leading
struct Num { std::vector<uint8_t> d; };

static void word_of(const Num& n, int k, int* q) {
    int L = (int)n.d.size();
    for (int i = 0; i < k; i++) q[i] = n.d[i] + n.d[L - 1 - i];  // column sums, outermost first
}
// carry into column L-k from the low scan of the column sums
static int carry_into(const Num& n, int col) {
    int L = (int)n.d.size(), c = 0;
    for (int i = 0; i < col; i++) c = (n.d[i] + n.d[L - 1 - i] + c) / 10;
    return c;
}
static void step(Num& n, std::vector<uint8_t>& tmp) {
    int L = (int)n.d.size();
    tmp.resize(L + 1);
    int c = 0;
    for (int i = 0; i < L; i++) { int t = n.d[i] + n.d[L - 1 - i] + c; tmp[i] = (uint8_t)(t % 10); c = t / 10; }
    if (c) { tmp[L] = 1; n.d.assign(tmp.begin(), tmp.begin() + L + 1); }
    else n.d.assign(tmp.begin(), tmp.begin() + L);
}
static bool is_pal(const Num& n) {
    int L = (int)n.d.size();
    for (int i = 0; i < L / 2; i++) if (n.d[i] != n.d[L - 1 - i]) return false;
    return true;
}

struct PStat { int maxT = -1; u64 seed = 0; u64 hits = 0; u64 last_in_I[8] = {0}; u64 last_long[8] = {0}; };

int main(int argc, char** argv) {
    P19[0] = 1; for (int i = 1; i < 10; i++) P19[i] = P19[i - 1] * 19;
    std::string dir = argv[1];
    u64 lo = strtoull(argv[2], 0, 10), hi = strtoull(argv[3], 0, 10);
    int T = atoi(argv[4]);
    std::string out = argv[5];
    for (int k = 4; k <= 7; k++) {
        u64 N = P19[k];
        bits[k].assign((N + 63) / 64, 0);
        std::string p = dir + "/inf_" + std::to_string(k) + ".bits";
        FILE* f = fopen(p.c_str(), "rb");
        if (!f || fread(bits[k].data(), 8, bits[k].size(), f) != bits[k].size()) { fprintf(stderr, "read %s\n", p.c_str()); return 1; }
        fclose(f);
    }
    std::vector<PStat> ps(10000);
    u64 checked_edges[8] = {0}, bad_edges[8] = {0}, left_I[8] = {0};
    int max_entry_rel[8] = {0}; u64 max_entry_seed[8] = {0};
    u64 never_entered[8] = {0};
    u64 repeat_seeds[8] = {0}; int min_repeat_gap[8]; u64 min_repeat_seed[8] = {0}; int min_repeat_t[8] = {0};
    for (int k = 0; k < 8; k++) min_repeat_gap[k] = 1 << 30;
    Num n; std::vector<uint8_t> tmp;
    std::vector<std::unordered_map<u64, int>> seen(8);
    for (u64 s = lo; s < hi; s++) {
        n.d.clear(); { u64 x = s; while (x) { n.d.push_back((uint8_t)(x % 10)); x /= 10; } }
        int t0[8], entry[8]; bool inside[8]; bool rep[8];
        for (int k = 4; k <= 7; k++) { t0[k] = -1; entry[k] = -1; inside[k] = false; rep[k] = false; seen[k].clear(); }
        u64 prevw[8]; int prevq[8][10]; bool have_prev[8] = {0};
        for (int t = 0; t <= T; t++) {
            int L = (int)n.d.size();
            if (t >= 1 && L >= 4 && is_pal(n)) {
                int P = n.d[L - 1] * 1000 + n.d[L - 2] * 100 + n.d[L - 3] * 10 + n.d[L - 4];
                PStat& st = ps[P];
                st.hits++;
                if (t > st.maxT) { st.maxT = t; st.seed = s; }
                for (int k = 4; k <= 7; k++) if (have_prev[k]) {  // previous number was long at width k
                    st.last_long[k]++;
                    if (inI(k, prevw[k])) st.last_in_I[k]++;
                }
            }
            for (int k = 4; k <= 7; k++) {
                if (L < k) { have_prev[k] = false; continue; }
                int q[10]; word_of(n, k, q);
                u64 w = encode(q, k);
                if (t0[k] < 0) t0[k] = t;
                bool in = inI(k, w);
                if (in && entry[k] < 0) entry[k] = t;
                if (inside[k] && !in) left_I[k]++;
                inside[k] = inside[k] || in;
                if (!rep[k]) {
                    auto it = seen[k].find(w);
                    if (it != seen[k].end()) {
                        rep[k] = true; repeat_seeds[k]++;
                        int gap = t - it->second;
                        if (gap < min_repeat_gap[k]) { min_repeat_gap[k] = gap; min_repeat_seed[k] = s; min_repeat_t[k] = it->second; }
                    } else seen[k][w] = t;
                }
                memcpy(prevq[k], q, sizeof(q)); prevw[k] = w; have_prev[k] = true;
            }
            if (t == T) break;
            // actual carries for the edge validation of this step
            int e[8];
            for (int k = 4; k <= 7; k++) if (L >= k) e[k] = carry_into(n, L - k);
            u64 expect[8];
            for (int k = 4; k <= 7; k++) if (L >= k) { int q[10]; word_of(n, k, q); expect[k] = fwd(q, k, e[k]); }
            step(n, tmp);
            int L2 = (int)n.d.size();
            for (int k = 4; k <= 7; k++) if (L >= k && L2 >= k) {
                int q[10]; word_of(n, k, q);
                checked_edges[k]++;
                if (encode(q, k) != expect[k]) bad_edges[k]++;
            }
        }
        for (int k = 4; k <= 7; k++) {
            if (entry[k] < 0) { if (t0[k] >= 0) never_entered[k]++; continue; }
            int rel = entry[k] - t0[k];
            if (rel > max_entry_rel[k]) { max_entry_rel[k] = rel; max_entry_seed[k] = s; }
        }
    }
    std::string sp = out + ".summary.txt";
    FILE* f = fopen(sp.c_str(), "w");
    fprintf(f, "seeds [%llu, %llu), steps %d\n", (unsigned long long)lo, (unsigned long long)hi, T);
    for (int k = 4; k <= 7; k++) {
        fprintf(f, "k=%d: edges validated=%llu mismatches=%llu | left I_k after entry=%llu | "
                   "max (entry time - first long time)=%d (seed %llu) | seeds never entering I_k=%llu | "
                   "seeds with a repeated k-word=%llu, shortest realized closed walk=%d steps (seed %llu, from t=%d)\n",
                k, (unsigned long long)checked_edges[k], (unsigned long long)bad_edges[k], (unsigned long long)left_I[k],
                max_entry_rel[k], (unsigned long long)max_entry_seed[k], (unsigned long long)never_entered[k],
                (unsigned long long)repeat_seeds[k], min_repeat_gap[k], (unsigned long long)min_repeat_seed[k], min_repeat_t[k]);
    }
    fclose(f);
    std::string pp = out + ".prefix.tsv";
    f = fopen(pp.c_str(), "w");
    fprintf(f, "prefix\thits\tmax_time\tseed\tlast_pred_long_k4\tin_I4\tlong_k5\tin_I5\tlong_k6\tin_I6\tlong_k7\tin_I7\n");
    for (int P = 1000; P < 10000; P++) {
        PStat& st = ps[P];
        if (st.hits == 0) continue;
        fprintf(f, "%d\t%llu\t%d\t%llu", P, (unsigned long long)st.hits, st.maxT, (unsigned long long)st.seed);
        for (int k = 4; k <= 7; k++) fprintf(f, "\t%llu\t%llu", (unsigned long long)st.last_long[k], (unsigned long long)st.last_in_I[k]);
        fprintf(f, "\n");
    }
    fclose(f);
    printf("wrote %s and %s\n", sp.c_str(), pp.c_str());
    return 0;
}
