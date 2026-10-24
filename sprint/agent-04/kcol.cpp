// kcol.cpp — fast implementation of the k-column prefix abstraction
// (SevenColumnProjection.forwardPrefix / SevenColumn.prefixPredecessors). fwd/preds work for k <= 8;
// the global and prefixes modes store 32-bit codes and need k <= 7 (k = 7: peak 4.2 GB).
//
// Word code: little-endian base 19, q_0 (outermost column) is the lowest base-19 digit.
// This is the same packing as Agent117.unpackWord.
//
// Modes:
//   kcol global K OUTDIR
//       Over ALL words with q_0 >= 1: in-degree peeling of the forward graph.
//       Writes OUTDIR/inf_K.bits (bit set = infinite backward rank, i.e. reachable
//       forward from a cycle) and OUTDIR/rank_K.u8 (finite longest-backward-path length,
//       254 = saturated, 255 = infinite). Prints summary statistics.
//   kcol prefixes K OUTDIR
//       Uses inf_K.bits / rank_K.u8. For every 3- and 4-digit prefix, decides whether some
//       long initial word (prefix ++ decimal digits, length K) is infinite-rank ("cycle"),
//       otherwise reports the max finite rank over its initial words (the certificate bound).
//   kcol fwd K CODE E          print forwardPrefix(word(CODE), E)
//   kcol preds K CODE          print prefixPredecessors(word(CODE))
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <chrono>

typedef uint32_t u32;
typedef uint64_t u64;

static int K;
static u64 P19[10];

static inline void decode(u64 c, int* q) {
    for (int i = 0; i < K; i++) { q[i] = (int)(c % 19); c /= 19; }
}
static inline u64 encode(const int* q) {
    u64 c = 0;
    for (int i = K - 1; i >= 0; i--) c = c * 19 + (u64)q[i];
    return c;
}

// forwardPrefix (ActualPrefix.lean): low scan from column 0 with carry 0,
// high scan from column K-1 down to 0 with carry e; if outer carry != 0, shift high by a leading 1.
static inline u64 fwd_q(const int* q, int e) {
    int lo[10], hi[10], p[10];
    int c = 0;
    for (int i = 0; i < K; i++) { int t = q[i] + c; lo[i] = t % 10; c = t / 10; }
    int h = e;
    for (int i = K - 1; i >= 0; i--) { int t = q[i] + h; hi[i] = t % 10; h = t / 10; }
    if (h == 0) {
        for (int i = 0; i < K; i++) p[i] = lo[i] + hi[i];
    } else {
        p[0] = lo[0] + 1;
        for (int i = 1; i < K; i++) p[i] = lo[i] + hi[i - 1];
    }
    return encode(p);
}
static inline u64 fwd(u64 c, int e) { int q[10]; decode(c, q); return fwd_q(q, e); }

// prefixPredecessors (PrefixInverse.lean), literal recursion.
static void noov(const int* p, int i, int x, int y, int* s, std::vector<u64>& out) {
    if (i == K) { if (s[0] > 0) out.push_back(encode(s)); return; }
    int v = p[i];
    for (int a = 0; a < 19; a++)
        for (int z = 0; z < 2; z++)
            if ((a + z) / 10 == y && v == (a + x) % 10 + (a + z) % 10) {
                s[i] = a; noov(p, i + 1, (a + x) / 10, z, s, out);
            }
}
static void ovtail(const int* p, int i, int prev, int x, int y, int* s, std::vector<u64>& out) {
    if (i == K) {
        if ((prev + 0) / 10 == y || (prev + 1) / 10 == y) out.push_back(encode(s));
        return;
    }
    int v = p[i];
    for (int a = 0; a < 19; a++)
        for (int z = 0; z < 2; z++)
            if ((prev + z) / 10 == y && v == (a + x) % 10 + (prev + z) % 10) {
                s[i] = a; ovtail(p, i + 1, a, (a + x) / 10, z, s, out);
            }
}
static void preds(u64 c, std::vector<u64>& out) {
    out.clear();
    int p[10], s[10];
    decode(c, p);
    noov(p, 0, 0, 0, s, out);
    int v = p[0];
    if (0 < v && v <= 10) {
        int a = v <= 9 ? v + 9 : 9;
        s[0] = a;
        ovtail(p, 1, a, (a + 0) / 10, 1, s, out);
    }
}

static double now() {
    return std::chrono::duration<double>(std::chrono::steady_clock::now().time_since_epoch()).count();
}

static void write_file(const std::string& path, const void* data, size_t n) {
    FILE* f = fopen(path.c_str(), "wb");
    if (!f) { perror(path.c_str()); exit(1); }
    fwrite(data, 1, n, f); fclose(f);
}
static void read_file(const std::string& path, void* data, size_t n) {
    FILE* f = fopen(path.c_str(), "rb");
    if (!f) { perror(path.c_str()); exit(1); }
    if (fread(data, 1, n, f) != n) { fprintf(stderr, "short read %s\n", path.c_str()); exit(1); }
    fclose(f);
}

static int mode_global(const std::string& outdir) {
    u64 N = P19[K];
    if (N > 0xFFFFFFFFull) { fprintf(stderr, "global mode stores 32-bit codes: K <= 7 only\n"); return 1; }
    double t0 = now();
    std::vector<uint16_t> indeg(N, 0);
    u64 valid = 0, edges = 0, maxin = 0;
    for (u64 c = 0; c < N; c++) {
        if (c % 19 == 0) continue;  // q_0 = 0 is not a state
        valid++;
        int q[10]; decode(c, q);
        u64 a = fwd_q(q, 0), b = fwd_q(q, 1);
        indeg[a]++; edges++;
        if (b != a) { indeg[b]++; edges++; }
    }
    for (u64 c = 0; c < N; c++) if (indeg[c] > maxin) maxin = indeg[c];
    fprintf(stderr, "[k=%d] indegree pass %.1fs\n", K, now() - t0);
    std::vector<uint8_t> rank(N, 255);
    std::vector<u32> cur, nxt;
    for (u64 c = 0; c < N; c++) if (c % 19 != 0 && indeg[c] == 0) cur.push_back((u32)c);
    u64 finite = 0; int r = 0;
    std::vector<u64> wave_sizes;
    while (!cur.empty()) {
        wave_sizes.push_back(cur.size());
        nxt.clear();
        for (u32 c : cur) {
            rank[c] = r > 254 ? 254 : (uint8_t)r;
            finite++;
            int q[10]; decode(c, q);
            u64 a = fwd_q(q, 0), b = fwd_q(q, 1);
            if (--indeg[a] == 0) nxt.push_back((u32)a);
            if (b != a && --indeg[b] == 0) nxt.push_back((u32)b);
        }
        std::swap(cur, nxt);
        r++;
    }
    fprintf(stderr, "[k=%d] peeling %.1fs\n", K, now() - t0);
    std::vector<u64> bits((N + 63) / 64, 0);
    u64 inf = 0;
    for (u64 c = 0; c < N; c++)
        if (c % 19 != 0 && indeg[c] > 0) { bits[c >> 6] |= 1ULL << (c & 63); inf++; }
    write_file(outdir + "/inf_" + std::to_string(K) + ".bits", bits.data(), bits.size() * 8);
    write_file(outdir + "/rank_" + std::to_string(K) + ".u8", rank.data(), N);
    printf("k=%d states(q0>=1)=%llu edges=%llu max_indegree=%llu finite=%llu infinite=%llu "
           "infinite_fraction=%.6f max_finite_rank=%d\n",
           K, (unsigned long long)valid, (unsigned long long)edges, (unsigned long long)maxin,
           (unsigned long long)finite, (unsigned long long)inf, (double)inf / (double)valid, r - 1);
    printf("k=%d wave sizes (rank: count) tail:", K);
    for (size_t i = (wave_sizes.size() > 12 ? wave_sizes.size() - 12 : 0); i < wave_sizes.size(); i++)
        printf(" %zu:%llu", i, (unsigned long long)wave_sizes[i]);
    printf("\n");
    return 0;
}

// Long initial words of a prefix (digits d[0..m-1]) at width K: prefix ++ any K-m decimal digits.
static int mode_prefixes(const std::string& outdir) {
    u64 N = P19[K];
    std::vector<u64> bits((N + 63) / 64);
    std::vector<uint8_t> rank(N);
    read_file(outdir + "/inf_" + std::to_string(K) + ".bits", bits.data(), bits.size() * 8);
    read_file(outdir + "/rank_" + std::to_string(K) + ".u8", rank.data(), N);
    std::string path = outdir + "/prefix_status_k" + std::to_string(K) + ".tsv";
    FILE* f = fopen(path.c_str(), "w");
    fprintf(f, "prefix\tk\tstatus\tbound_or_ncycle_initial\tn_initial\n");
    for (int m = 3; m <= 4; m++) {
        if (m > K) continue;
        int lo = (m == 3) ? 100 : 1000, hi = (m == 3) ? 999 : 9999;
        int tail = K - m;
        u64 ntail = 1; for (int i = 0; i < tail; i++) ntail *= 10;
        for (int P = lo; P <= hi; P++) {
            int d[10]; int x = P;
            for (int i = m - 1; i >= 0; i--) { d[i] = x % 10; x /= 10; }
            bool leadone = (d[0] == 1);
            for (int i = 1; i < m; i++) if (d[i] > 2) leadone = false;
            if (leadone) { fprintf(f, "%d\t%d\tleadone\t-\t-\n", P, K); continue; }
            int q[10]; for (int i = 0; i < m; i++) q[i] = d[i];
            int maxr = -1; u64 ncyc = 0;
            for (u64 t = 0; t < ntail; t++) {
                u64 y = t;
                for (int i = m; i < K; i++) { q[i] = (int)(y % 10); y /= 10; }
                u64 c = encode(q);
                if ((bits[c >> 6] >> (c & 63)) & 1) ncyc++;
                else if (rank[c] > maxr) maxr = rank[c];
            }
            if (ncyc) fprintf(f, "%d\t%d\tcycle\t%llu\t%llu\n", P, K, (unsigned long long)ncyc, (unsigned long long)ntail);
            else fprintf(f, "%d\t%d\tacyclic\t%d\t%llu\n", P, K, maxr, (unsigned long long)ntail);
        }
    }
    fclose(f);
    printf("wrote %s\n", path.c_str());
    return 0;
}

static void print_word(u64 c) {
    int q[10]; decode(c, q);
    printf("[");
    for (int i = 0; i < K; i++) printf("%s%d", i ? ", " : "", q[i]);
    printf("]");
}

int main(int argc, char** argv) {
    P19[0] = 1; for (int i = 1; i < 10; i++) P19[i] = P19[i - 1] * 19;
    if (argc < 3) { fprintf(stderr, "usage: see header\n"); return 1; }
    std::string mode = argv[1];
    K = atoi(argv[2]);
    if (K < 1 || K > 8) { fprintf(stderr, "K must be 1..8\n"); return 1; }
    if (mode == "global") return mode_global(argv[3]);
    if (mode == "prefixes") return mode_prefixes(argv[3]);
    if (mode == "fwd") { u64 c = strtoull(argv[3], 0, 10); print_word(fwd(c, atoi(argv[4]))); printf("\n"); return 0; }
    if (mode == "preds") {
        std::vector<u64> out; preds(strtoull(argv[3], 0, 10), out);
        for (u64 s : out) { print_word(s); printf("\n"); }
        return 0;
    }
    fprintf(stderr, "unknown mode\n");
    return 1;
}
