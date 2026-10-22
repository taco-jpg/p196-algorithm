// cyc.cpp — shortest simple cycles of the forward k-column abstraction inside I_k (= inf_K.bits).
//
//   cyc K DATADIR MAXLEN [MAXPRINT]
// For L = 1..MAXLEN, counts simple cycles of length L (each counted once, rooted at its smallest
// word code) and stops after the first L with at least one cycle; prints up to MAXPRINT of them
// as rows "word  --e/ov-->" with e = boundary carry used and ov = 1 if the width grows.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

typedef uint32_t u32;
typedef uint64_t u64;
static int K;
static u64 P19[10];
static inline void decode(u64 c, int* q) { for (int i = 0; i < K; i++) { q[i] = (int)(c % 19); c /= 19; } }
static inline u64 encode(const int* q) { u64 c = 0; for (int i = K - 1; i >= 0; i--) c = c * 19 + (u64)q[i]; return c; }
static inline u64 fwd(u64 c, int e, int* ov) {
    int q[10], lo[10], hi[10], p[10];
    decode(c, q);
    int cc = 0;
    for (int i = 0; i < K; i++) { int t = q[i] + cc; lo[i] = t % 10; cc = t / 10; }
    int h = e;
    for (int i = K - 1; i >= 0; i--) { int t = q[i] + h; hi[i] = t % 10; h = t / 10; }
    if (h == 0) { for (int i = 0; i < K; i++) p[i] = lo[i] + hi[i]; }
    else { p[0] = lo[0] + 1; for (int i = 1; i < K; i++) p[i] = lo[i] + hi[i - 1]; }
    *ov = h;
    return encode(p);
}
static std::vector<u64> bits;
static std::vector<u32> br;
static inline bool inI(u64 c) { return (bits[c >> 6] >> (c & 63)) & 1; }
static inline u32 rk(u64 c) { return br[c >> 6] + (u32)__builtin_popcountll(bits[c >> 6] & ((1ULL << (c & 63)) - 1)); }

static std::vector<u32> codes, S0, S1;
static std::vector<uint8_t> OV;  // bit0: ov of e=0 edge, bit1: ov of e=1 edge
static int L, maxprint;
static u64 found;
static u32 path[64]; static int pe[64];
static std::vector<uint8_t> onpath;

static void print_cycle() {
    for (int i = 0; i < L; i++) {
        int q[10]; decode(codes[path[i]], q);
        printf("  [");
        for (int j = 0; j < K; j++) printf("%s%d", j ? "," : "", q[j]);
        int ov = (OV[path[i]] >> pe[i]) & 1;
        printf("] --e=%d%s-->\n", pe[i], ov ? ",overflow" : "");
    }
    printf("\n");
}
static void dfs(u32 root, int d) {
    u32 v = path[d];
    for (int e = 0; e < 2; e++) {
        u32 w = e ? S1[v] : S0[v];
        if (e == 1 && S1[v] == S0[v]) continue;
        if (d + 1 == L) {
            if (w == root) { pe[d] = e; found++; if ((int)found <= maxprint) print_cycle(); }
            continue;
        }
        if (w <= root || onpath[w]) continue;
        pe[d] = e; path[d + 1] = w; onpath[w] = 1;
        dfs(root, d + 1);
        onpath[w] = 0;
    }
}

int main(int argc, char** argv) {
    P19[0] = 1; for (int i = 1; i < 10; i++) P19[i] = P19[i - 1] * 19;
    K = atoi(argv[1]); std::string dir = argv[2]; int maxlen = atoi(argv[3]);
    maxprint = argc > 4 ? atoi(argv[4]) : 20;
    u64 N = P19[K];
    bits.assign((N + 63) / 64, 0);
    std::string path_ = dir + "/inf_" + std::to_string(K) + ".bits";
    FILE* f = fopen(path_.c_str(), "rb");
    if (!f || fread(bits.data(), 8, bits.size(), f) != bits.size()) { fprintf(stderr, "read fail\n"); return 1; }
    fclose(f);
    br.assign(bits.size() + 1, 0);
    for (size_t i = 0; i < bits.size(); i++) br[i + 1] = br[i] + __builtin_popcountll(bits[i]);
    u32 M = br[bits.size()];
    codes.resize(M); S0.resize(M); S1.resize(M); OV.resize(M); onpath.assign(M, 0);
    { u32 j = 0; for (u64 c = 0; c < N; c++) if (inI(c)) codes[j++] = (u32)c; }
    for (u32 v = 0; v < M; v++) {
        int o0, o1;
        u64 a = fwd(codes[v], 0, &o0), b = fwd(codes[v], 1, &o1);
        S0[v] = rk(a); S1[v] = rk(b); OV[v] = (uint8_t)(o0 | (o1 << 1));
    }
    for (L = 1; L <= maxlen; L++) {
        found = 0;
        for (u32 r = 0; r < M; r++) { path[0] = r; onpath[r] = 1; dfs(r, 0); onpath[r] = 0; }
        printf("k=%d length %d: %llu simple cycles\n", K, L, (unsigned long long)found);
        fflush(stdout);
        if (found) break;
    }
    return 0;
}
