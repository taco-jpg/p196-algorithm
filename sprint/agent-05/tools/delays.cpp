// P196 sprint agent 05 -- delay-witness search (all palindrome hits).
//
// The Agent124 ancestry bound for a prefix `pre` says: for all A > 0 and t,
// if orbit(A,t) is a palindrome beginning with `pre` then t <= bound + 1.
// So EVERY (A, t) with orbit(A,t) a palindrome is a lower-bound witness for the
// prefixes of that palindrome -- first hits and later hits alike.
// This program records, per 3/4/5-digit palindrome prefix, the largest t found.
//
// Seeds are enumerated by column-sum classes: for an l-digit seed (d_0 = units),
// step(A) depends only on q_i = d_i + d_{l-1-i} (i < l/2) and the middle digit
// for odd l.  Each class is iterated once from N1 = step(A); a hit at step s of
// N1 is a hit at time s+1 of every seed in the class.  The witness written out
// is the smallest seed of the class.
//
// Horizon: an orbit is followed while its iterates have at most D digits (and
// at most M steps).  A palindrome is counted only if it has <= D digits.  The
// horizon depends only on the number, not on the time it was reached, which
// makes the optional memo exact: the hits after a number x are a function of x.
//
// Memo (--memo B): "distinguished" iterates (hash has B low zero bits) are
// stored in a lock-free table with the list of later hits (offset, palindrome
// top digits, width).  A later orbit reaching a stored iterate copies the list
// and stops.  Validated against the no-memo path (see REPORT.md).
//
// Modes:
//   exhaust L1 L2 OUT [opts]          all classes of lengths L1..L2
//   sample  L COUNT RNGSEED OUT [opts] random classes of length L (uniform over classes)
//   seeds   FILE OUT [opts]           explicit seeds, one per line
// opts: --D <digits=200> --M <steps=5000> --memo <bits> --table <log2 slots=26>
//
// Output lines: "P<len> <prefix> <maxdelay> <seed> <palwidth>", summary lines '#'.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <atomic>
#include <algorithm>
#include <chrono>
#include <fstream>
#ifdef _OPENMP
#include <omp.h>
#endif

static const int MAXD = 4096;

struct Best { int delay = -1; int width = 0; std::string seed; };

struct Tables {
    std::vector<Best> p3, p4, p5;
    std::vector<uint64_t> hist;   // first-hit time histogram (classes)
    uint64_t classes = 0, nohit = 0, hits = 0, memo_lookups = 0, memo_found = 0, steps = 0, mcap = 0;
    Tables() : p3(1000), p4(10000), p5(100000), hist(8192, 0) {}
    static bool better(const Best& b, const Best& a) {
        if (b.delay != a.delay) return b.delay > a.delay;
        if (b.delay < 0) return false;
        if (b.seed.size() != a.seed.size()) return b.seed.size() < a.seed.size();
        return b.seed < a.seed;
    }
    void merge(const Tables& o) {
        auto mg = [](std::vector<Best>& a, const std::vector<Best>& b) {
            for (size_t i = 0; i < a.size(); i++) if (better(b[i], a[i])) a[i] = b[i];
        };
        mg(p3, o.p3); mg(p4, o.p4); mg(p5, o.p5);
        for (size_t i = 0; i < hist.size(); i++) hist[i] += o.hist[i];
        classes += o.classes; nohit += o.nohit; hits += o.hits;
        memo_lookups += o.memo_lookups; memo_found += o.memo_found; steps += o.steps; mcap += o.mcap;
    }
};

// A hit: time (or offset), palindrome width, top min(5,width) digits as an integer.
struct Hit { uint32_t t; uint32_t width; uint32_t top; };

static inline int rev_add(const uint8_t* a, int n, uint8_t* b) {
    int c = 0;
    for (int i = 0; i < n; i++) {
        int s = a[i] + a[n - 1 - i] + c;
        c = s >= 10;
        b[i] = (uint8_t)(s - 10 * c);
    }
    if (c) { b[n] = 1; return n + 1; }
    return n;
}
static inline bool is_pal(const uint8_t* a, int n) {
    for (int i = 0, j = n - 1; i < j; i++, j--) if (a[i] != a[j]) return false;
    return true;
}
static inline uint32_t top_digits(const uint8_t* a, int n) {
    uint32_t v = 0; int k = n < 5 ? n : 5;
    for (int i = 0; i < k; i++) v = v * 10 + a[n - 1 - i];
    return v;
}

// ---------------- memo table ----------------
struct Entry { std::atomic<uint64_t> k1; uint64_t k2; uint32_t off; uint32_t cnt; };
static Entry* g_tab = nullptr; static uint64_t g_mask = 0;
static Hit* g_pool = nullptr; static std::atomic<uint64_t> g_pool_used{0}; static uint64_t g_pool_cap = 0;
static std::atomic<uint64_t> g_tab_used{0};
static int g_memo_bits = -1;

static inline void hash128(const uint8_t* a, int n, uint64_t& h1, uint64_t& h2) {
    uint64_t x = 0x9E3779B97F4A7C15ULL ^ (uint64_t)n, y = 0xC2B2AE3D27D4EB4FULL + (uint64_t)n;
    int i = 0;
    for (; i + 8 <= n; i += 8) {
        uint64_t w; memcpy(&w, a + i, 8);
        x = (x ^ w) * 0xFF51AFD7ED558CCDULL; x ^= x >> 29;
        y = (y + w) * 0xC4CEB9FE1A85EC53ULL; y ^= y >> 31;
    }
    uint64_t w = 0; memcpy(&w, a + i, n - i);
    x = (x ^ w) * 0xFF51AFD7ED558CCDULL; x ^= x >> 33; x *= 0xC4CEB9FE1A85EC53ULL; x ^= x >> 29;
    y = (y + w) * 0x9E3779B97F4A7C15ULL; y ^= y >> 32; y *= 0xFF51AFD7ED558CCDULL; y ^= y >> 30;
    h1 = x | 2;  // never 0 (empty) or 1 (busy)
    h2 = y;
}
static bool memo_find(uint64_t h1, uint64_t h2, uint32_t& off, uint32_t& cnt) {
    uint64_t i = (h2 ^ (h1 >> 7)) & g_mask;
    for (uint64_t p = 0; p < 64; p++, i = (i + 1) & g_mask) {
        uint64_t k = g_tab[i].k1.load(std::memory_order_acquire);
        if (k == 0) return false;
        if (k == h1 && g_tab[i].k2 == h2) { off = g_tab[i].off; cnt = g_tab[i].cnt; return true; }
    }
    return false;
}
static void memo_insert(uint64_t h1, uint64_t h2, const Hit* hs, uint32_t cnt) {
    if (g_tab_used.load(std::memory_order_relaxed) > (g_mask + 1) / 10 * 7) return;  // full: skip
    uint64_t off = 0;
    if (cnt) {
        off = g_pool_used.fetch_add(cnt);
        if (off + cnt > g_pool_cap) return;
        memcpy(g_pool + off, hs, cnt * sizeof(Hit));
    }
    uint64_t i = (h2 ^ (h1 >> 7)) & g_mask;
    for (uint64_t p = 0; p < 64; p++, i = (i + 1) & g_mask) {
        uint64_t k = g_tab[i].k1.load(std::memory_order_acquire);
        if (k == h1 && g_tab[i].k2 == h2) return;
        if (k == 0) {
            uint64_t z = 0;
            if (g_tab[i].k1.compare_exchange_strong(z, 1, std::memory_order_acq_rel)) {
                g_tab[i].k2 = h2; g_tab[i].off = (uint32_t)off; g_tab[i].cnt = cnt;
                g_tab[i].k1.store(h1, std::memory_order_release);
                g_tab_used.fetch_add(1, std::memory_order_relaxed);
                return;
            }
        }
    }
}

// ---------------- orbit ----------------
struct Work {
    std::vector<uint8_t> A, B;
    std::vector<Hit> hits;
    std::vector<std::pair<uint64_t, uint64_t>> dpk; std::vector<uint32_t> dpt;
    std::vector<Hit> tmp;
    Work() : A(MAXD), B(MAXD) {}
};

// x = A[0..n) is orbit(seed, t0).  Collect hits at times > t0 (and t0 itself if count_x).
static void run_orbit(Tables& tb, Work& w, int n, int t0, int D, int M, bool count_x) {
    w.hits.clear(); w.dpk.clear(); w.dpt.clear();
    uint8_t* a = w.A.data(); uint8_t* b = w.B.data();
    if (n > D) return;
    if (count_x && is_pal(a, n)) w.hits.push_back({(uint32_t)t0, (uint32_t)n, top_digits(a, n)});
    bool ended = false;
    for (int t = t0 + 1; t <= M; t++) {
        int m = rev_add(a, n, b);
        if (m > D) { ended = true; break; }
        n = m; std::swap(a, b); tb.steps++;
        if (is_pal(a, n)) w.hits.push_back({(uint32_t)t, (uint32_t)n, top_digits(a, n)});
        if (g_memo_bits >= 0) {
            uint64_t h1, h2; hash128(a, n, h1, h2);
            if (((h1 >> 40) & ((1ULL << g_memo_bits) - 1)) == 0) {
                tb.memo_lookups++;
                uint32_t off, cnt;
                if (memo_find(h1, h2, off, cnt)) {
                    tb.memo_found++;
                    for (uint32_t j = 0; j < cnt; j++) {
                        Hit h = g_pool[off + j];
                        if ((int)(t + h.t) <= M) w.hits.push_back({t + h.t, h.width, h.top});
                    }
                    ended = true;
                    break;
                }
                w.dpk.push_back({h1, h2}); w.dpt.push_back((uint32_t)t);
            }
        }
    }
    // M is chosen so large that it never binds before D (checked: see report); if it bound,
    // memo entries would be time-dependent, so refuse to insert in that case.
    if (!ended) { tb.mcap++; return; }   // step cap bound before the digit cap: no memo insert
    if (g_memo_bits >= 0) {
        for (size_t k = 0; k < w.dpk.size(); k++) {
            w.tmp.clear();
            for (auto& h : w.hits) if (h.t > w.dpt[k]) w.tmp.push_back({h.t - w.dpt[k], h.width, h.top});
            memo_insert(w.dpk[k].first, w.dpk[k].second, w.tmp.data(), (uint32_t)w.tmp.size());
        }
    }
}

static inline void record_hits(Tables& tb, const Work& w, const uint8_t* sd, int l) {
    if (w.hits.empty()) { tb.nohit++; return; }
    tb.hits += w.hits.size();
    uint32_t tf = w.hits[0].t; for (auto& h : w.hits) tf = std::min(tf, h.t);
    if (tf < tb.hist.size()) tb.hist[tf]++;
    std::string seed;
    for (auto& h : w.hits) {
        int T = (int)h.t, n = (int)h.width; uint32_t v = h.top;
        int k = n < 5 ? n : 5;
        auto upd = [&](Best& bb) {
            bool imp = T > bb.delay;
            if (!imp && T == bb.delay) {
                if (seed.empty()) { seed.assign(l, '0'); for (int i = 0; i < l; i++) seed[l - 1 - i] = char('0' + sd[i]); }
                imp = seed.size() < bb.seed.size() || (seed.size() == bb.seed.size() && seed < bb.seed);
            }
            if (imp) {
                if (seed.empty()) { seed.assign(l, '0'); for (int i = 0; i < l; i++) seed[l - 1 - i] = char('0' + sd[i]); }
                bb.delay = T; bb.width = n; bb.seed = seed;
            }
        };
        auto pref = [&](int len) { uint32_t x = v; for (int i = k; i > len; i--) x /= 10; return x; };
        if (n >= 3) upd(tb.p3[pref(3)]);
        if (n >= 4) upd(tb.p4[pref(4)]);
        if (n >= 5) upd(tb.p5[pref(5)]);
    }
}

static int class_first_iterate(int l, const int* q, int mid, uint8_t* seedd, uint8_t* out) {
    int h = l / 2;
    for (int i = 0; i < h; i++) {
        int hi = q[i] - 9; if (hi < 0) hi = 0;
        if (i == 0 && hi < 1) hi = 1;
        seedd[l - 1 - i] = (uint8_t)hi; seedd[i] = (uint8_t)(q[i] - hi);
    }
    if (l & 1) seedd[h] = (uint8_t)mid;
    return rev_add(seedd, l, out);
}
static uint64_t ipow(uint64_t b, int e) { uint64_t r = 1; while (e--) r *= b; return r; }
static void decode_class(int l, uint64_t id, int* q, int& mid) {
    int h = l / 2;
    if (l & 1) { mid = (int)(id % 10); id /= 10; } else mid = 0;
    for (int i = h - 1; i >= 1; i--) { q[i] = (int)(id % 19); id /= 19; }
    q[0] = (int)(id % 18) + 1;
}
static uint64_t class_count(int l) {
    if (l == 1) return 9;
    uint64_t c = 18 * ipow(19, l / 2 - 1);
    if (l & 1) c *= 10;
    return c;
}

static void write_tables(const Tables& tb, const char* out, const std::string& hdr, double secs) {
    FILE* f = fopen(out, "w");
    fprintf(f, "# %s\n# mcap %llu\n# classes %llu nohit %llu hits %llu steps %llu memo_lookups %llu memo_found %llu table_used %llu pool_used %llu seconds %.1f\n",
            hdr.c_str(), (unsigned long long)tb.mcap, (unsigned long long)tb.classes, (unsigned long long)tb.nohit,
            (unsigned long long)tb.hits, (unsigned long long)tb.steps,
            (unsigned long long)tb.memo_lookups, (unsigned long long)tb.memo_found,
            (unsigned long long)g_tab_used.load(), (unsigned long long)g_pool_used.load(), secs);
    fprintf(f, "# firsthit-hist");
    for (size_t i = 0; i < tb.hist.size(); i++) if (tb.hist[i]) fprintf(f, " %zu:%llu", i, (unsigned long long)tb.hist[i]);
    fprintf(f, "\n");
    auto dump = [&](const std::vector<Best>& v, int len, int lo) {
        for (size_t i = lo; i < v.size(); i++)
            if (v[i].delay >= 0) fprintf(f, "P%d %0*zu %d %s %d\n", len, len, i, v[i].delay, v[i].seed.c_str(), v[i].width);
    };
    dump(tb.p3, 3, 100); dump(tb.p4, 4, 1000); dump(tb.p5, 5, 10000);
    fclose(f);
}

int main(int argc, char** argv) {
    if (argc < 2) { fprintf(stderr, "usage: see source header\n"); return 2; }
    std::string mode = argv[1];
    int D = 200, M = 5000, tbits = 26;
    std::vector<std::string> pos;
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i], "--D")) D = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--M")) M = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--memo")) g_memo_bits = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--table")) tbits = atoi(argv[++i]);
        else pos.push_back(argv[i]);
    }
    if (D + 2 > MAXD) { fprintf(stderr, "D too large\n"); return 2; }
    if (g_memo_bits >= 0) {
        uint64_t slots = 1ULL << tbits; g_mask = slots - 1;
        g_tab = (Entry*)calloc(slots, sizeof(Entry));
        g_pool_cap = slots / 2; g_pool = (Hit*)malloc(g_pool_cap * sizeof(Hit));
        if (!g_tab || !g_pool) { fprintf(stderr, "alloc failed\n"); return 3; }
    }
    auto t0 = std::chrono::steady_clock::now();
    int nth = 1;
#ifdef _OPENMP
    nth = omp_get_max_threads();
#endif
    std::vector<Tables> per(nth);
    std::string hdr; const char* out = nullptr;
    std::string common = " D=" + std::to_string(D) + " M=" + std::to_string(M) + " memo=" + std::to_string(g_memo_bits);

    if (mode == "exhaust") {
        int L1 = atoi(pos[0].c_str()), L2 = atoi(pos[1].c_str()); out = pos[2].c_str();
        hdr = "exhaust L=" + pos[0] + ".." + pos[1] + common;
        for (int l = L1; l <= L2; l++) {
            uint64_t C = class_count(l);
            auto tl = std::chrono::steady_clock::now();
            #pragma omp parallel
            {
                int tid = 0;
#ifdef _OPENMP
                tid = omp_get_thread_num();
#endif
                Work w; std::vector<uint8_t> S(64); int q[32]; int mid;
                #pragma omp for schedule(dynamic, 4096)
                for (long long id = 0; id < (long long)C; id++) {
                    int n;
                    if (l == 1) { S[0] = (uint8_t)(id + 1); n = rev_add(S.data(), 1, w.A.data()); }
                    else { decode_class(l, (uint64_t)id, q, mid); n = class_first_iterate(l, q, mid, S.data(), w.A.data()); }
                    per[tid].classes++;
                    run_orbit(per[tid], w, n, 1, D, M, true);
                    record_hits(per[tid], w, S.data(), l);
                }
            }
            double s = std::chrono::duration<double>(std::chrono::steady_clock::now() - tl).count();
            fprintf(stderr, "length %d: %llu classes, %.1f s, table %llu, pool %llu\n", l, (unsigned long long)C, s,
                    (unsigned long long)g_tab_used.load(), (unsigned long long)g_pool_used.load());
        }
    } else if (mode == "sample") {
        int l = atoi(pos[0].c_str()); long long cnt = atoll(pos[1].c_str());
        uint64_t rs = strtoull(pos[2].c_str(), 0, 10); out = pos[3].c_str();
        hdr = "sample L=" + pos[0] + " count=" + pos[1] + " rng=" + pos[2] + common;
        #pragma omp parallel
        {
            int tid = 0;
#ifdef _OPENMP
            tid = omp_get_thread_num();
#endif
            Work w; std::vector<uint8_t> S(512); std::vector<int> q(512); int mid;
            #pragma omp for schedule(dynamic, 1024)
            for (long long k = 0; k < cnt; k++) {
                uint64_t z = rs * 0x9E3779B97F4A7C15ULL + (uint64_t)k * 0xBF58476D1CE4E5B9ULL + 1;
                auto nxt = [&]() { z += 0x9E3779B97F4A7C15ULL; uint64_t x = z;
                    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ULL; x = (x ^ (x >> 27)) * 0x94D049BB133111EBULL;
                    return x ^ (x >> 31); };
                int h = l / 2;
                q[0] = (int)(nxt() % 18) + 1;
                for (int i = 1; i < h; i++) q[i] = (int)(nxt() % 19);
                mid = (l & 1) ? (int)(nxt() % 10) : 0;
                int n = class_first_iterate(l, q.data(), mid, S.data(), w.A.data());
                per[tid].classes++;
                run_orbit(per[tid], w, n, 1, D, M, true);
                record_hits(per[tid], w, S.data(), l);
            }
        }
    } else if (mode == "seeds") {
        out = pos[1].c_str();
        hdr = "seeds file=" + pos[0] + common;
        std::ifstream in(pos[0]); std::string line; std::vector<std::string> seeds;
        while (std::getline(in, line)) {
            std::string s; for (char ch : line) { if (ch == '#') break; if (ch >= '0' && ch <= '9') s += ch; }
            size_t p = s.find_first_not_of('0');
            if (p != std::string::npos) seeds.push_back(s.substr(p));
        }
        #pragma omp parallel
        {
            int tid = 0;
#ifdef _OPENMP
            tid = omp_get_thread_num();
#endif
            Work w; std::vector<uint8_t> S(512);
            #pragma omp for schedule(dynamic, 1)
            for (long long k = 0; k < (long long)seeds.size(); k++) {
                const std::string& s = seeds[k]; int n = (int)s.size();
                for (int i = 0; i < n; i++) { w.A[i] = (uint8_t)(s[n - 1 - i] - '0'); S[i] = w.A[i]; }
                per[tid].classes++;
                run_orbit(per[tid], w, n, 0, D, M, false);
                record_hits(per[tid], w, S.data(), n);
            }
        }
    } else { fprintf(stderr, "unknown mode\n"); return 2; }

    Tables all; for (auto& t : per) all.merge(t);
    double secs = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    write_tables(all, out, hdr, secs);
    fprintf(stderr, "done: classes %llu nohit %llu hits %llu steps %llu lookups %llu found %llu in %.1f s\n",
            (unsigned long long)all.classes, (unsigned long long)all.nohit, (unsigned long long)all.hits,
            (unsigned long long)all.steps, (unsigned long long)all.memo_lookups, (unsigned long long)all.memo_found, secs);
    return 0;
}
