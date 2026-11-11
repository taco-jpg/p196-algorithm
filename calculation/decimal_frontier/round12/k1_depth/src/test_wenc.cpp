// r12g: round-trip and injectivity test of kfwd window packing for K = 20..30 (both paths)
#include "kcommon.h"
static inline u128 wenc(const int* w, int K_) {
    if (K_ <= 25) return enc_cells(w, K_);
    uint64_t lo = 0, hi = 0; for (int i = 14; i >= 0; i--) lo = lo * D_ + w[i]; for (int i = K_ - 1; i >= 15; i--) hi = hi * D_ + w[i];
    return ((u128)hi << 64) | lo;
}
static inline void wdec(u128 k, int* w, int K_) {
    if (K_ <= 25) { dec_cells(k, w, K_); return; }
    uint64_t lo = (uint64_t)k, hi = (uint64_t)(k >> 64);
    for (int i = 0; i < 15; i++) { w[i] = (int)(lo % D_); lo /= D_; } for (int i = 15; i < K_; i++) { w[i] = (int)(hi % D_); hi /= D_; }
}
int main() {
    uint64_t x = 88172645463325252ULL; long bad = 0, tot = 0;
    for (D_ = 17; D_ <= 19; D_ += 2) for (int K = 20; K <= 30; K++) {
        std::vector<u128> v;
        for (int r = 0; r < 200000; r++) {
            int w[64], w2[64];
            for (int i = 0; i < K; i++) { x ^= x << 13; x ^= x >> 7; x ^= x << 17; w[i] = (r % 7 == 0) ? (r / 7 + i) % D_ : (int)(x % D_); if (r % 11 == 0) w[i] = D_ - 1; }
            u128 k = wenc(w, K); wdec(k, w2, K); tot++;
            for (int i = 0; i < K; i++) if (w[i] != w2[i]) { bad++; break; }
            v.push_back(k);
        }
    }
    printf("round trips %ld, failures %ld\n", tot, bad);
}
