// scc.cpp — strongly connected components of the forward k-column abstraction restricted to
// the infinite-rank set I_k (inf_K.bits from `kcol global`). I_k is forward-closed, and every
// node on a cycle lies in I_k, so the nontrivial SCCs found here are ALL cycles of the abstraction.
//
//   scc K DATADIR            writes DATADIR/scc_K.u32 (SCC id per I_k node, in code order),
//                            DATADIR/core_K.tsv (one line per nontrivial SCC: id size edges
//                            period girth(exact|sampled) carry/overflow usage, representative word),
//                            prints a summary.
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <numeric>
#include <string>
#include <vector>

typedef uint32_t u32;
typedef uint64_t u64;
static int K;
static u64 P19[10];

static inline void decode(u64 c, int* q) { for (int i = 0; i < K; i++) { q[i] = (int)(c % 19); c /= 19; } }
static inline u64 encode(const int* q) { u64 c = 0; for (int i = K - 1; i >= 0; i--) c = c * 19 + (u64)q[i]; return c; }
// returns code; *ov = 1 iff the outer carry is 1 (the width grows by one digit)
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
static std::vector<u32> blockrank;
static inline bool inI(u64 c) { return (bits[c >> 6] >> (c & 63)) & 1; }
static inline u32 rankI(u64 c) {
    return blockrank[c >> 6] + (u32)__builtin_popcountll(bits[c >> 6] & ((1ULL << (c & 63)) - 1));
}

int main(int argc, char** argv) {
    P19[0] = 1; for (int i = 1; i < 10; i++) P19[i] = P19[i - 1] * 19;
    K = atoi(argv[1]);
    std::string dir = argv[2];
    u64 N = P19[K];
    bits.assign((N + 63) / 64, 0);
    {
        std::string path = dir + "/inf_" + std::to_string(K) + ".bits";
        FILE* f = fopen(path.c_str(), "rb");
        if (!f) { perror(path.c_str()); return 1; }
        if (fread(bits.data(), 8, bits.size(), f) != bits.size()) { fprintf(stderr, "short read\n"); return 1; }
        fclose(f);
    }
    blockrank.assign(bits.size() + 1, 0);
    for (size_t i = 0; i < bits.size(); i++) blockrank[i + 1] = blockrank[i] + __builtin_popcountll(bits[i]);
    u32 M = blockrank[bits.size()];
    std::vector<u32> codes(M);
    { u32 j = 0; for (u64 c = 0; c < N; c++) if (inI(c)) codes[j++] = (u32)c; }
    fprintf(stderr, "[k=%d] |I|=%u\n", K, M);

    // successors as indices (2 per node, may coincide)
    auto succ = [&](u32 v, int e, int* ov) -> u32 {
        u64 t = fwd(codes[v], e, ov);
        if (!inI(t)) { fprintf(stderr, "BUG: I not forward closed\n"); exit(2); }
        return rankI(t);
    };

    // iterative Tarjan
    const u32 UNV = 0xFFFFFFFFu;
    std::vector<u32> idx(M, UNV), low(M), comp(M, UNV);
    std::vector<uint8_t> onst(M, 0);
    std::vector<u32> st;
    struct Fr { u32 v; int e; };
    std::vector<Fr> cs;
    u32 counter = 0, ncomp = 0;
    for (u32 r = 0; r < M; r++) {
        if (idx[r] != UNV) continue;
        cs.push_back({r, 0});
        idx[r] = low[r] = counter++; st.push_back(r); onst[r] = 1;
        while (!cs.empty()) {
            Fr& fr = cs.back();
            u32 v = fr.v;
            if (fr.e < 2) {
                int e = fr.e++; int ov;
                u32 w = succ(v, e, &ov);
                if (idx[w] == UNV) {
                    idx[w] = low[w] = counter++; st.push_back(w); onst[w] = 1;
                    cs.push_back({w, 0});
                } else if (onst[w]) {
                    if (idx[w] < low[v]) low[v] = idx[w];
                }
            } else {
                if (low[v] == idx[v]) {
                    u32 w;
                    do { w = st.back(); st.pop_back(); onst[w] = 0; comp[w] = ncomp; } while (w != v);
                    ncomp++;
                }
                cs.pop_back();
                if (!cs.empty()) { u32 u = cs.back().v; if (low[v] < low[u]) low[u] = low[v]; }
            }
        }
    }
    fprintf(stderr, "[k=%d] SCCs: %u\n", K, ncomp);
    { std::vector<u32>().swap(idx); std::vector<u32>().swap(low); std::vector<uint8_t>().swap(onst); }

    // sizes, nontriviality
    std::vector<u32> size(ncomp, 0);
    for (u32 v = 0; v < M; v++) size[comp[v]]++;
    std::vector<uint8_t> nontriv(ncomp, 0);
    for (u32 c = 0; c < ncomp; c++) if (size[c] > 1) nontriv[c] = 1;
    for (u32 v = 0; v < M; v++) {
        int ov;
        for (int e = 0; e < 2; e++) if (succ(v, e, &ov) == v) nontriv[comp[v]] = 1;
    }
    // members of nontrivial components
    std::vector<u32> order(M);
    std::iota(order.begin(), order.end(), 0);
    std::stable_sort(order.begin(), order.end(), [&](u32 a, u32 b) { return comp[a] < comp[b]; });
    std::vector<u32> start(ncomp + 1, 0);
    for (u32 c = 0; c < ncomp; c++) start[c + 1] = start[c] + size[c];
    std::vector<u32> local(M, 0);
    for (u32 c = 0; c < ncomp; c++) for (u32 j = start[c]; j < start[c + 1]; j++) local[order[j]] = j - start[c];

    std::string tpath = dir + "/core_" + std::to_string(K) + ".tsv";
    FILE* tf = fopen(tpath.c_str(), "w");
    fprintf(tf, "scc\tsize\tintra_edges\tperiod\tgirth\tgirth_kind\tedges_e0\tedges_e1\tedges_overflow\tmin_word\n");
    u64 coresize = 0; u32 nnt = 0;
    std::vector<u32> big;
    std::vector<int> lvl, dist;
    std::vector<u32> q;
    for (u32 c = 0; c < ncomp; c++) {
        if (!nontriv[c]) continue;
        nnt++; coresize += size[c];
        u32 n = size[c];
        // edges, carry usage, period via BFS levels from the first member
        u64 ne = 0, ne0 = 0, ne1 = 0, nov = 0;
        lvl.assign(n, -1);
        u32 root = order[start[c]];
        lvl[local[root]] = 0; q.clear(); q.push_back(root);
        long long g = 0;
        for (size_t h = 0; h < q.size(); h++) {
            u32 v = q[h];
            int ovs[2]; u32 ws[2] = {succ(v, 0, &ovs[0]), succ(v, 1, &ovs[1])};
            for (int e = 0; e < 2; e++) {
                u32 w = ws[e]; int ov = ovs[e];
                if (e == 1 && ws[1] == ws[0]) continue;  // same edge for both carries: count once
                if (comp[w] != c) continue;
                ne++; (e ? ne1 : ne0)++; nov += ov;
                if (lvl[local[w]] < 0) { lvl[local[w]] = lvl[local[v]] + 1; q.push_back(w); }
                else { long long d = (long long)lvl[local[v]] + 1 - lvl[local[w]]; if (d < 0) d = -d; g = std::gcd(g, d); }
            }
        }
        // girth: BFS from every member (exact) if small, else from 64 sampled members
        u32 girth = UNV; const char* kind = "exact";
        std::vector<u32> sources;
        if (n <= 3000) { for (u32 j = start[c]; j < start[c + 1]; j++) sources.push_back(order[j]); }
        else { kind = "sampled64"; for (int t = 0; t < 64; t++) sources.push_back(order[start[c] + (u32)(((u64)t * 2654435761u) % n)]); }
        for (u32 s : sources) {
            dist.assign(n, -1);
            q.clear(); q.push_back(s); dist[local[s]] = 0;
            bool done = false;
            for (size_t h = 0; h < q.size() && !done; h++) {
                u32 v = q[h];
                if ((u32)dist[local[v]] + 1 >= girth) break;
                for (int e = 0; e < 2; e++) {
                    int ov; u32 w = succ(v, e, &ov);
                    if (comp[w] != c) continue;
                    if (w == s) { girth = std::min(girth, (u32)dist[local[v]] + 1); done = true; break; }
                    if (dist[local[w]] < 0) { dist[local[w]] = dist[local[v]] + 1; q.push_back(w); }
                }
            }
        }
        u32 mn = codes[order[start[c]]];
        for (u32 j = start[c]; j < start[c + 1]; j++) mn = std::min(mn, codes[order[j]]);
        int w[10]; decode(mn, w);
        fprintf(tf, "%u\t%u\t%llu\t%lld\t%u\t%s\t%llu\t%llu\t%llu\t[", c, n, (unsigned long long)ne, g, girth, kind,
                (unsigned long long)ne0, (unsigned long long)ne1, (unsigned long long)nov);
        for (int i = 0; i < K; i++) fprintf(tf, "%s%d", i ? "," : "", w[i]);
        fprintf(tf, "]\n");
    }
    fclose(tf);
    std::string spath = dir + "/scc_" + std::to_string(K) + ".u32";
    FILE* sf = fopen(spath.c_str(), "wb"); fwrite(comp.data(), 4, M, sf); fclose(sf);
    std::vector<u32> sz;
    for (u32 c = 0; c < ncomp; c++) if (nontriv[c]) sz.push_back(size[c]);
    std::sort(sz.rbegin(), sz.rend());
    printf("k=%d |I|=%u sccs=%u nontrivial=%u core_nodes=%llu largest:", K, M, ncomp, nnt, (unsigned long long)coresize);
    for (size_t i = 0; i < sz.size() && i < 10; i++) printf(" %u", sz[i]);
    printf("\n");
    return 0;
}
