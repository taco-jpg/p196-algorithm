// winhash.h -- round 11b: sparse (hash-set) storage of window families, so that windows wider than 10 fit in memory.
// Window key (width W, phase ph, k = number of overflow slots in the window):  c (W bits) | d (W bits) << W | rn << 2W,
// rn = sum_j r_j << 4j (nibble j = digit at the j-th overflow slot of the window). Needs 2W + 4k <= 64.
// The families stored here are the LEVEL sets BB'_W(ph) of lvl.cpp (see FINAL.md section 2 for the soundness proof).
#pragma once
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <atomic>
#include <thread>
#include <algorithm>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

namespace wh {
typedef uint64_t u64; typedef unsigned __int128 u128;
static const u64 EMPTY = ~0ULL;
static inline u64 mix(u64 k) { k ^= k >> 33; k *= 0xff51afd7ed558ccdULL; k ^= k >> 33; k *= 0xc4ceb9fe1a85ec53ULL; k ^= k >> 33; return k; }

// open addressing, linear probing, fixed capacity (power of two); concurrent insert by CAS
struct HS {
  u64* a = nullptr; u64 cap = 0, mask = 0; std::atomic<u64> n{0};
  void init(u64 capacity, int nth) {
    cap = 1; while (cap < capacity) cap <<= 1; mask = cap - 1;
    a = (u64*)mmap(nullptr, cap * 8, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0);
    if (a == MAP_FAILED) { fprintf(stderr, "mmap %llu slots failed\n", (unsigned long long)cap); exit(3); }
    std::vector<std::thread> th; for (int i = 0; i < nth; i++) th.emplace_back([&, i]() { u64 lo = cap * i / nth, hi = cap * (i + 1) / nth; for (u64 j = lo; j < hi; j++) a[j] = EMPTY; });
    for (auto& x : th) x.join();
    n = 0;
  }
  void release() { if (a) munmap(a, cap * 8); a = nullptr; cap = 0; n = 0; }
  // returns slot; *isNew set if inserted now
  inline u64 insert(u64 k, bool* isNew) {
    u64 i = mix(k) & mask;
    while (true) {
      u64 v = __atomic_load_n(&a[i], __ATOMIC_RELAXED);
      if (v == k) { *isNew = false; return i; }
      if (v == EMPTY) {
        u64 exp = EMPTY;
        if (__atomic_compare_exchange_n(&a[i], &exp, k, false, __ATOMIC_RELAXED, __ATOMIC_RELAXED)) {
          u64 m = n.fetch_add(1, std::memory_order_relaxed) + 1;
          if (m > cap / 10 * 8) { fprintf(stderr, "hash table overfull (%llu of %llu): raise capacity\n", (unsigned long long)m, (unsigned long long)cap); fflush(stderr); exit(7); }
          *isNew = true; return i;
        }
        if (exp == k) { *isNew = false; return i; }
        continue;  // someone else took this slot with another key: re-read it
      }
      i = (i + 1) & mask;
    }
  }
  inline long long find(u64 k) const {
    u64 i = mix(k) & mask;
    while (true) { u64 v = a[i]; if (v == k) return (long long)i; if (v == EMPTY) return -1; i = (i + 1) & mask; }
  }
  inline bool has(u64 k) const { return find(k) >= 0; }
};

static inline std::string lname(const std::string& dir, int B, const std::string& pat, int w, int ph) {
  return dir + "/lb_B" + std::to_string(B) + "_" + pat + "_w" + std::to_string(w) + "_ph" + std::to_string(ph) + ".u64";
}
// load a sorted key file into a fresh table (load factor <= 1/2)
static bool loadFile(const std::string& fn, HS& h, int nth) {
  int fd = open(fn.c_str(), O_RDONLY); if (fd < 0) { fprintf(stderr, "missing %s\n", fn.c_str()); return false; }
  struct stat st; fstat(fd, &st); u64 n = st.st_size / 8;
  const u64* p = n ? (const u64*)mmap(nullptr, n * 8, PROT_READ, MAP_SHARED, fd, 0) : nullptr; close(fd);
  if (n && p == (const u64*)MAP_FAILED) return false;
  h.init(std::max<u64>(2 * n + 16, 1024), nth);
  std::vector<std::thread> th; for (int i = 0; i < nth; i++) th.emplace_back([&, i]() { bool nw; for (u64 j = n * i / nth; j < n * (i + 1) / nth; j++) h.insert(p[j], &nw); });
  for (auto& x : th) x.join();
  if (n) munmap((void*)p, n * 8);
  return true;
}

// r11b: read-only sorted-array family (the key file mmap'ed as is, 8 B per key, page cache shared between processes) with a
// bucket index on the top IB bits of the key range; membership by binary search inside one bucket.
struct SA {
  const u64* p = nullptr; u64 n = 0; int sh = 0; std::vector<uint32_t> idx; static const int IB = 26;
  bool open_(const std::string& fn) {
    int fd = ::open(fn.c_str(), O_RDONLY); if (fd < 0) { fprintf(stderr, "missing %s\n", fn.c_str()); return false; }
    struct stat st; fstat(fd, &st); n = st.st_size / 8;
    if (n) { p = (const u64*)mmap(nullptr, n * 8, PROT_READ, MAP_SHARED, fd, 0); if (p == (const u64*)MAP_FAILED) { close(fd); return false; } }
    close(fd);
    if (n >= 0xffffffffULL) { fprintf(stderr, "SA: too many keys\n"); return false; }
    u64 mx = n ? p[n - 1] : 0; int bits = 64 - (mx ? __builtin_clzll(mx) : 63); sh = bits > IB ? bits - IB : 0;
    u64 nb = (mx >> sh) + 2; idx.assign(nb + 1, 0);
    for (u64 i = 0; i < n; i++) idx[(p[i] >> sh) + 1]++;
    for (u64 b = 1; b <= nb; b++) idx[b] += idx[b - 1];
    for (u64 i = 1; i < n; i++) if (p[i] <= p[i - 1]) { fprintf(stderr, "SA: %s not sorted unique\n", fn.c_str()); return false; }
    return true;
  }
  inline bool has(u64 k) const {
    u64 b = k >> sh; if (b + 1 >= idx.size()) return false;
    const u64* lo = p + idx[b]; const u64* hi = p + idx[b + 1];
    const u64* q = std::lower_bound(lo, hi, k); return q != hi && *q == k;
  }
};
// ---- consumer side: the level family BB'_HW(ph), ph = 0..L-1, tested on T-periodic interfaces (c, d, r nibble-packed per overflow index)
static int HW = 0, HL = 1, HT = 0, HNOV = 0; static u64 HTMASK = 0;
static int hpre[256];   // overflow slots before slot t (pattern repeated)
static std::vector<SA*> tabs;
static bool load(const std::string& dir, int B, const std::string& pat, int w, int T, int nov, int nth) {
  HW = w; HL = pat.size(); HT = T; HNOV = nov; HTMASK = (T == 64) ? ~0ULL : ((1ULL << T) - 1);
  { int c = 0; for (int t = 0; t < 256; t++) { hpre[t] = c; if (pat[t % pat.size()] == '1') c++; } }
  if (T % HL) { fprintf(stderr, "winhash: T %% L != 0\n"); return false; }
  tabs.assign(HL, nullptr);
  (void)nth;
  for (int ph = 0; ph < HL; ph++) { tabs[ph] = new SA(); if (!tabs[ph]->open_(lname(dir, B, pat, w, ph))) return false;
    fprintf(stdout, "winhash: mapped w=%d ph=%d: %llu windows (sorted array)\n", w, ph, (unsigned long long)tabs[ph]->n); fflush(stdout); }
  return true;
}
static inline u64 key(u64 cw, u64 dw, u64 rn) { return cw | (dw << HW) | (rn << (2 * HW)); }
static inline int kOf(int s0) { return hpre[s0 + HW] - hpre[s0]; }
// non-wrapping window at s0 (s0 + HW <= T)
static inline bool winAt(u64 c, u64 d, u128 r, int s0) {
  u64 m = (1ULL << HW) - 1; int k = kOf(s0);
  u64 rn = (u64)(r >> (4 * hpre[s0])) & ((k >= 16) ? ~0ULL : ((1ULL << (4 * k)) - 1));
  return tabs[s0 % HL]->has(key((c >> s0) & m, (d >> s0) & m, rn));
}
// wrapped window at s0 (T - HW < s0 < T): rotate so that s0 becomes slot 0
static inline bool winWrapAt(u64 c, u64 d, u128 r, int s0) {
  u64 c2 = ((c >> s0) | (c << (HT - s0))) & HTMASK, d2 = ((d >> s0) | (d << (HT - s0))) & HTMASK;
  int q = HNOV ? hpre[s0] % HNOV : 0; int rb = 4 * HNOV; u128 rmask = (rb >= 128) ? ~(u128)0 : (((u128)1 << rb) - 1);
  u128 r2 = q ? (((r >> (4 * q)) | (r << (rb - 4 * q))) & rmask) : r;
  u64 m = (1ULL << HW) - 1; int k = kOf(s0);
  u64 rn = (u64)r2 & ((k >= 16) ? ~0ULL : ((1ULL << (4 * k)) - 1));
  return tabs[s0 % HL]->has(key(c2 & m, d2 & m, rn));
}
static inline bool allInB(u64 c, u64 d, u128 r) {
  for (int s0 = 0; s0 + HW <= HT; s0++) if (!winAt(c, d, r, s0)) return false;
  for (int s0 = HT - HW + 1; s0 < HT; s0++) if (!winWrapAt(c, d, r, s0)) return false;
  return true;
}
}  // namespace wh
