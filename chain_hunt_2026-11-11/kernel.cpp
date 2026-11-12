// Robust-exterior safety game on pair sums. State: pair sums s_0..s_{k-1} of the outer k columns (19^k states).
// Each step the unknown interior contributes one carry bit delta into column k-1. A state is safe if for BOTH
// values of delta the next outer block is not palindromic and the next state is safe. A nonempty safe set would
// prove that every number with such an outer block never becomes a palindrome, whatever its interior is.
// usage: kernel K
#include <bits/stdc++.h>
using namespace std;
int K; uint64_t N;
static inline void step(const int* s, int delta, bool& bad, uint64_t& nxt) {
    int d[16], c[16], a[16], b[16];
    d[K - 1] = delta; for (int i = K - 1; i >= 1; i--) d[i - 1] = (s[i] + d[i] >= 10) ? 1 : 0; int g = (s[0] + d[0] >= 10) ? 1 : 0;
    c[0] = 0; for (int i = 0; i + 1 < K; i++) c[i + 1] = (s[i] + c[i] >= 10) ? 1 : 0;
    for (int i = 0; i < K; i++) a[i] = (s[i] + c[i]) % 10;
    if (g == 0) { for (int i = 0; i < K; i++) b[i] = (s[i] + d[i]) % 10; } else { b[0] = 1; for (int i = 0; i + 1 < K; i++) b[i + 1] = (s[i] + d[i]) % 10; }
    bad = true; for (int i = 0; i < K; i++) if (a[i] != b[i]) { bad = false; break; }
    uint64_t x = 0; for (int i = K - 1; i >= 0; i--) x = x * 19 + (a[i] + b[i]); nxt = x;
}
int main(int argc, char** argv) {
    K = atoi(argv[1]); N = 1; for (int i = 0; i < K; i++) N *= 19;
    vector<uint32_t> succ(2 * N); vector<uint8_t> alive(N, 1);
    uint64_t nbadEdges = 0;
    for (uint64_t x = 0; x < N; x++) { int s[16]; uint64_t z = x; for (int i = 0; i < K; i++) { s[i] = z % 19; z /= 19; }
        for (int dl = 0; dl < 2; dl++) { bool bad; uint64_t nx; step(s, dl, bad, nx); if (bad) { succ[2 * x + dl] = 0xffffffffu; nbadEdges++; } else succ[2 * x + dl] = (uint32_t)nx; } }
    // worklist removal using reverse edges (CSR)
    vector<uint32_t> indeg(N + 1, 0); for (uint64_t e = 0; e < 2 * N; e++) if (succ[e] != 0xffffffffu) indeg[succ[e] + 1]++;
    vector<uint64_t> off(N + 1, 0); for (uint64_t x = 0; x < N; x++) off[x + 1] = off[x] + indeg[x + 1];
    vector<uint32_t> rev(off[N]); { vector<uint64_t> fill(off.begin(), off.end() - 1); for (uint64_t e = 0; e < 2 * N; e++) if (succ[e] != 0xffffffffu) rev[fill[succ[e]]++] = (uint32_t)(e / 2); }
    vector<uint32_t> work; for (uint64_t x = 0; x < N; x++) if (succ[2 * x] == 0xffffffffu || succ[2 * x + 1] == 0xffffffffu) { alive[x] = 0; work.push_back((uint32_t)x); }
    uint64_t killed = work.size();
    while (!work.empty()) { uint32_t y = work.back(); work.pop_back(); for (uint64_t e = off[y]; e < off[y + 1]; e++) { uint32_t x = rev[e]; if (alive[x]) { alive[x] = 0; killed++; work.push_back(x); } } }
    uint64_t safe = N - killed; uint64_t safeTop = 0; for (uint64_t x = 0; x < N; x++) if (alive[x] && (x % 19) >= 1) safeTop++;
    printf("k=%d: states=%llu  fatal edges=%llu  SAFE states=%llu (with nonzero outer pair sum: %llu)\n", K, (unsigned long long)N, (unsigned long long)nbadEdges, (unsigned long long)safe, (unsigned long long)safeTop);
    if (safe > 0) { int shown = 0; for (uint64_t x = 0; x < N && shown < 10; x++) if (alive[x]) { uint64_t z = x; printf("   safe pair-sum block:"); for (int i = 0; i < K; i++) { printf(" %llu", (unsigned long long)(z % 19)); z /= 19; } printf("\n"); shown++; } }
    return 0;
}
