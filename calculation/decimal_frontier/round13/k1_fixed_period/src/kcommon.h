// r12g kcommon.h -- shared lattice tables and the exact local window rule (copied from kink6.cpp, generalised to base B).
// Table format (.tbl): "P M" (base 10) or "P M B"; then g_0..g_{P-1}; then for each t: L row, UP row, DN row (M entries each),
// L = bulk lattice cell, UP = bulk ascending carry into the cell, DN = bulk descending carry into the mirror of the cell.
// State key (u128): phase ((t*M+j)*2+par) << PS | sum cell_i << (5 i);  PS = 100 for K <= 20 (kink6 format), 118 otherwise.
#pragma once
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <thread>
#include <vector>
typedef long long ll;
typedef unsigned __int128 u128;

static int P_, M_, B_ = 10, D_ = 19;  // time period, spatial period, base, number of cell values (2B-1)
static std::vector<int> G;
static std::vector<std::vector<int>> L, UP, DN;
static inline int md(int a, int m) { a %= m; return a < 0 ? a + m : a; }
static inline int PSof(int K) { return K <= 20 ? 100 : 118; }

static void load_tbl(const char* fn) {
    FILE* f = fopen(fn, "r");
    if (!f) { perror(fn); exit(1); }
    char line[256];
    if (!fgets(line, sizeof line, f)) exit(1);
    int a = 0, b = 0, c = 0;
    int n = sscanf(line, "%d %d %d", &a, &b, &c);
    P_ = a; M_ = b; if (n >= 3) B_ = c; D_ = 2 * B_ - 1;
    G.resize(P_);
    for (auto& x : G) if (fscanf(f, "%d", &x) != 1) exit(1);
    L.assign(P_, std::vector<int>(M_)); UP = L; DN = L;
    for (int t = 0; t < P_; t++) {
        for (auto& x : L[t]) if (fscanf(f, "%d", &x) != 1) exit(1);
        for (auto& x : UP[t]) if (fscanf(f, "%d", &x) != 1) exit(1);
        for (auto& x : DN[t]) if (fscanf(f, "%d", &x) != 1) exit(1);
    }
    fclose(f);
}

// one step of the K-window [c, c+K) (c = frame, j = (c - nB) mod M), lattice exact below c at time t.
// Din = descending carry into the mirror of the top window cell; dh = frame shift; topv = e-digit of cell c+K (used iff dh).
// returns ok = lattice below the new frame still exact at t+1.
static inline bool wstep(int K, int t, int j, const int* win, int Din, int dh, int topv, int* out) {
    const int Bb = B_; int g = G[t];
    int e[64], D[64], r[64];
    int up = UP[t][j];
    for (int i = 0; i < K; i++) { int s = win[i] + up; e[i] = s % Bb; up = s / Bb; }
    D[K - 1] = Din;
    for (int i = K - 1; i > 0; i--) D[i - 1] = (win[i] + D[i]) / Bb;
    for (int i = 0; i < K; i++) r[i] = (win[i] + D[i]) % Bb;
    int Dx = (win[0] + D[0]) / Bb;
    bool ok = true; int rlow1 = -1; int t1 = (t + 1) % P_;
    for (int k = 1; k <= 4 * M_; k++) {
        int col = md(j - k, M_); int Lx = L[t][col];
        if (Dx == DN[t][col]) break;
        int rx = (Lx + Dx) % Bb;
        if (k == 1) rlow1 = rx;
        int tgt = -k + g;
        if (tgt < 0) { int tc = md(j + tgt, M_); if ((L[t][tc] + UP[t][tc]) % Bb + rx != L[t1][tc]) ok = false; }
        Dx = (Lx + Dx) / Bb;
    }
    int nw[65];
    for (int i = 0; i < K + dh; i++) {
        if (i == K) { nw[i] = (g == 1) ? topv + r[K - 1] : topv; continue; }
        int src = i - g, rr;
        if (src >= 0) rr = r[src];
        else { if (rlow1 >= 0) rr = rlow1; else { int col = md(j - 1, M_); rr = (L[t][col] + DN[t][col]) % Bb; } }
        nw[i] = e[i] + rr;
    }
    if (dh) { if (nw[0] != L[t1][md(j, M_)]) ok = false; for (int i = 0; i < K; i++) out[i] = nw[i + 1]; }
    else for (int i = 0; i < K; i++) out[i] = nw[i];
    return ok;
}

// exact (fold) step of the top K-window [h-K, h): Din and the ghost are determined by the window itself.
static inline bool exact_step(int K, int t, int j, int par, const int* w, int* nw) {
    int a = UP[t][j], aK1 = 0;
    for (int i = 0; i < K; i++) { if (i == K - 1) aK1 = a; a = (w[i] + a) / B_; }
    int Din = (par == 0) ? a : aK1;          // n even: carry into position h; n odd: carry into the middle cell
    int ghost = (w[K - 1] + Din) % B_;
    int g = G[t]; int dh = (g == 1 && par == 0);
    return wstep(K, t, j, w, Din, dh, ghost, nw);
}
static inline void next_phase(int t, int j, int par, int& t2, int& j2, int& p2) {
    int g = G[t]; int dh = (g == 1 && par == 0);
    t2 = (t + 1) % P_; j2 = (j + dh) % M_; p2 = (par + g) % 2;
}
static inline unsigned phase_id(int t, int j, int par) { return (unsigned)((t * M_ + j) * 2 + par); }
static inline void phase_dec(unsigned ph, int& t, int& j, int& par) { par = ph % 2; ph /= 2; j = ph % M_; t = ph / M_; }
static inline u128 enc_cells(const int* w, int K) { u128 k = 0; for (int i = 0; i < K; i++) k |= (u128)w[i] << (5 * i); return k; }
static inline void dec_cells(u128 k, int* w, int K) { for (int i = 0; i < K; i++) w[i] = (int)((k >> (5 * i)) & 31); }
static inline u128 enc(int t, int j, int par, const int* w, int K, int PS) { return ((u128)phase_id(t, j, par) << PS) | enc_cells(w, K); }
static inline uint64_t mix64(uint64_t x) {
    x += 0x9E3779B97F4A7C15ULL; x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ULL; x = (x ^ (x >> 27)) * 0x94D049BB133111EBULL; return x ^ (x >> 31);
}
static inline uint64_t hkey(u128 k) { return mix64((uint64_t)k ^ mix64((uint64_t)(k >> 64))); }
static double now_s() { return std::chrono::duration<double>(std::chrono::steady_clock::now().time_since_epoch()).count(); }

// sorted key array with an open-addressing index (uint32 slots, 0 = empty); find() returns the position or -1.
struct KeyIndex {
    std::vector<u128> keys; std::vector<uint32_t> slot; uint64_t mask = 0;
    void build() {
        uint64_t n = keys.size(), cap = 1; while (cap < 2 * n + 16) cap <<= 1;
        slot.assign(cap, 0); mask = cap - 1;
        for (uint64_t i = 0; i < n; i++) {
            uint64_t h = hkey(keys[i]) & mask;
            while (slot[h]) h = (h + 1) & mask;
            slot[h] = (uint32_t)(i + 1);
        }
    }
    inline ll find(u128 k) const {
        uint64_t h = hkey(k) & mask;
        while (true) { uint32_t s = slot[h]; if (!s) return -1; if (keys[s - 1] == k) return (ll)(s - 1); h = (h + 1) & mask; }
    }
};
static std::vector<u128> read_keys(const char* fn) {
    FILE* f = fopen(fn, "rb"); if (!f) { perror(fn); exit(1); }
    fseek(f, 0, SEEK_END); long sz = ftell(f); fseek(f, 0, SEEK_SET);
    std::vector<u128> v(sz / 16);
    if (!v.empty() && fread(v.data(), 16, v.size(), f) != v.size()) { fprintf(stderr, "short read %s\n", fn); exit(1); }
    fclose(f); return v;
}
// parallel sort + unique of u128 vectors (merge sort over T chunks)
static void psort_unique(std::vector<u128>& v, int T) {
    size_t n = v.size();
    if (n < (1u << 20) || T <= 1) { std::sort(v.begin(), v.end()); v.erase(std::unique(v.begin(), v.end()), v.end()); return; }
    std::vector<size_t> b(T + 1); for (int i = 0; i <= T; i++) b[i] = n * i / T;
    { std::vector<std::thread> th; for (int i = 0; i < T; i++) th.emplace_back([&, i] { std::sort(v.begin() + b[i], v.begin() + b[i + 1]); }); for (auto& x : th) x.join(); }
    for (int w = 1; w < T; w *= 2) {
        std::vector<std::thread> th;
        for (int i = 0; i + w < T; i += 2 * w) {
            size_t lo = b[i], mid = b[i + w], hi = b[std::min(i + 2 * w, T)];
            th.emplace_back([&, lo, mid, hi] { std::inplace_merge(v.begin() + lo, v.begin() + mid, v.begin() + hi); });
        }
        for (auto& x : th) x.join();
    }
    v.erase(std::unique(v.begin(), v.end()), v.end());
}
