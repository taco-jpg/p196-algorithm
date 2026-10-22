// entry.cpp — shortest entry walks from a fixed cycle to target words, in Agent117 witness format.
//
//   entry K DATADIR CYCLEFILE PREFIXFILE OUT.tsv
// CYCLEFILE: the cycle in forward order, one line per word: "q_0 ... q_{K-1} e" (e = carry used
//            from this word to the next).
// PREFIXFILE: one line per target: "label d_1 ... d_m" (a digit prefix). The long initial words
//            of the prefix at width K are prefix ++ every string of K-m decimal digits.
// Multi-source BFS FORWARD from the cycle words inside I_K (inf_K.bits). For each prefix, picks the
// initial word in I_K with the smallest BFS distance and outputs the backward walk
//   p0 <- s_1 <- s_2 <- ... <- s_m = z   (z on the cycle),  forwardPrefix(s_{j+1}, e_{j+1}) = s_j,
// packed as Agent117.unpack expects: n = 2 * code + e, code little-endian base 19.
// Output columns: label  p0_code  depth  z_code  packed_entry(comma separated)  n_initial_in_I
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <sstream>
#include <fstream>
#include <string>
#include <vector>

typedef uint32_t u32;
typedef uint64_t u64;
static int K;
static u64 P19[10];
static inline void decode(u64 c, int* q) { for (int i = 0; i < K; i++) { q[i] = (int)(c % 19); c /= 19; } }
static inline u64 encode(const int* q) { u64 c = 0; for (int i = K - 1; i >= 0; i--) c = c * 19 + (u64)q[i]; return c; }
static inline u64 fwd(u64 c, int e) {
    int q[10], lo[10], hi[10], p[10];
    decode(c, q);
    int cc = 0;
    for (int i = 0; i < K; i++) { int t = q[i] + cc; lo[i] = t % 10; cc = t / 10; }
    int h = e;
    for (int i = K - 1; i >= 0; i--) { int t = q[i] + h; hi[i] = t % 10; h = t / 10; }
    if (h == 0) { for (int i = 0; i < K; i++) p[i] = lo[i] + hi[i]; }
    else { p[0] = lo[0] + 1; for (int i = 1; i < K; i++) p[i] = lo[i] + hi[i - 1]; }
    return encode(p);
}
static std::vector<u64> bits;
static std::vector<u32> br;
static inline bool inI(u64 c) { return (bits[c >> 6] >> (c & 63)) & 1; }
static inline u32 rk(u64 c) { return br[c >> 6] + (u32)__builtin_popcountll(bits[c >> 6] & ((1ULL << (c & 63)) - 1)); }

int main(int argc, char** argv) {
    P19[0] = 1; for (int i = 1; i < 10; i++) P19[i] = P19[i - 1] * 19;
    K = atoi(argv[1]);
    std::string dir = argv[2];
    u64 N = P19[K];
    bits.assign((N + 63) / 64, 0);
    {
        std::string p = dir + "/inf_" + std::to_string(K) + ".bits";
        FILE* f = fopen(p.c_str(), "rb");
        if (!f || fread(bits.data(), 8, bits.size(), f) != bits.size()) { fprintf(stderr, "read fail\n"); return 1; }
        fclose(f);
    }
    br.assign(bits.size() + 1, 0);
    for (size_t i = 0; i < bits.size(); i++) br[i + 1] = br[i] + __builtin_popcountll(bits[i]);
    u32 M = br[bits.size()];
    std::vector<u32> codes(M);
    { u32 j = 0; for (u64 c = 0; c < N; c++) if (inI(c)) codes[j++] = (u32)c; }
    // read cycle
    std::vector<u64> cyc; std::vector<int> cyce;
    {
        std::ifstream in(argv[3]); std::string line;
        while (std::getline(in, line)) {
            std::istringstream ss(line); int q[10]; int e;
            for (int i = 0; i < K; i++) ss >> q[i];
            if (!(ss >> e)) continue;
            cyc.push_back(encode(q)); cyce.push_back(e);
        }
        for (size_t i = 0; i < cyc.size(); i++)
            if (fwd(cyc[i], cyce[i]) != cyc[(i + 1) % cyc.size()] || !inI(cyc[i])) { fprintf(stderr, "bad cycle at %zu\n", i); return 1; }
    }
    // BFS forward from cycle nodes
    const u32 UNV = 0xFFFFFFFFu;
    std::vector<u32> par(M, UNV);
    std::vector<uint16_t> dist(M, 0xFFFF);
    std::vector<uint8_t> pe(M, 0);
    std::vector<u32> q;
    for (u64 c : cyc) { u32 v = rk(c); if (dist[v] == 0xFFFF) { dist[v] = 0; q.push_back(v); } }
    for (size_t h = 0; h < q.size(); h++) {
        u32 v = q[h];
        for (int e = 0; e < 2; e++) {
            u64 w = fwd(codes[v], e);
            u32 wi = rk(w);
            if (dist[wi] == 0xFFFF) { dist[wi] = dist[v] + 1; par[wi] = v; pe[wi] = (uint8_t)e; q.push_back(wi); }
        }
    }
    int ecc = 0; for (u32 v = 0; v < M; v++) if (dist[v] != 0xFFFF && dist[v] > ecc) ecc = dist[v];
    fprintf(stderr, "BFS reached %zu of %u words of I_%d; eccentricity of the cycle = %d\n", q.size(), M, K, ecc);
    FILE* out = fopen(argv[5], "w");
    fprintf(out, "label\tp0_code\tdepth\tz_code\tpacked_entry\tn_initial_in_I\n");
    std::ifstream in(argv[4]); std::string line;
    while (std::getline(in, line)) {
        std::istringstream ss(line); std::string label; ss >> label;
        std::vector<int> dg; int x; while (ss >> x) dg.push_back(x);
        int m = (int)dg.size();
        u64 ntail = 1; for (int i = m; i < K; i++) ntail *= 10;
        u64 bestc = 0; int bestd = 1 << 30; u64 nin = 0;
        for (u64 t = 0; t < ntail; t++) {
            int w[10]; for (int i = 0; i < m; i++) w[i] = dg[i];
            u64 y = t; for (int i = m; i < K; i++) { w[i] = (int)(y % 10); y /= 10; }
            u64 c = encode(w);
            if (!inI(c)) continue;
            nin++;
            int dd = dist[rk(c)];
            if (dd < bestd || (dd == bestd && c < bestc)) { bestd = dd; bestc = c; }
        }
        if (!nin) { fprintf(out, "%s\tNONE\t-\t-\t-\t0\n", label.c_str()); continue; }
        // backward walk from p0 to the cycle
        std::string packed; u32 v = rk(bestc); u64 zc = bestc;
        while (dist[v] != 0) {
            u32 p = par[v]; int e = pe[v];
            if (fwd(codes[p], e) != codes[v]) { fprintf(stderr, "BUG\n"); return 1; }
            if (!packed.empty()) packed += ",";
            packed += std::to_string(2 * (u64)codes[p] + (u64)e);
            v = p; zc = codes[p];
        }
        {   // continue backward along the cycle to its first word, so that every walk ends at cyc[0]
            size_t i = 0; while (cyc[i] != zc) i++;
            while (i != 0) {
                i--;
                if (!packed.empty()) packed += ",";
                packed += std::to_string(2 * cyc[i] + (u64)cyce[i]);
                bestd += 0;
            }
            zc = cyc[0];
        }
        fprintf(out, "%s\t%llu\t%d\t%llu\t%s\t%llu\n", label.c_str(), (unsigned long long)bestc, bestd,
                (unsigned long long)zc, packed.c_str(), (unsigned long long)nin);
    }
    fclose(out);
    return 0;
}
