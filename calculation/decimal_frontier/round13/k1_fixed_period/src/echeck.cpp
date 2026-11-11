// r13b echeck: E_K file (eset2, WORDS=3) subset of a kink7 Cyc(K) file (phase << PS | cells)?  usage: echeck lat.tbl orbit K EFILE CYCFILE
#include "kcommon.h"
int main(int argc, char** argv) {
    load_tbl(argv[1]); int which = atoi(argv[2]); int K = atoi(argv[3]); const char* efn = argv[4]; const char* cfn = argv[5];
    int NPH = 2 * P_ * M_; std::vector<int> orb(NPH, -1); std::vector<int> reps; int norb = 0;
    for (int s = 0; s < NPH; s++) { if (orb[s] >= 0) continue; reps.push_back(s); int t, j, p; phase_dec(s, t, j, p); int x = s; do { orb[x] = norb; int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; x = phase_id(t, j, p); } while (x != s); norb++; }
    std::vector<std::array<int,3>> Ph; { int t, j, p; phase_dec(reps[which], t, j, p); int x = reps[which]; do { Ph.push_back({t, j, p}); int a, b, c; next_phase(t, j, p, a, b, c); t = a; j = b; p = c; x = phase_id(t, j, p); } while (x != reps[which]); }
    int PS = PSof(K);
    std::vector<u128> C = read_keys(cfn); if (!std::is_sorted(C.begin(), C.end())) { puts("Cyc not sorted"); return 1; }
    FILE* f = fopen(efn, "rb"); if (!f) { perror(efn); return 1; } int lo, wds; fread(&lo, 4, 1, f); fread(&wds, 4, 1, f);
    if (lo != (int)Ph.size() || wds != 3) { puts("bad header"); return 1; }
    uint64_t tot = 0, miss = 0;
    for (int l = 0; l < lo; l++) {
        uint64_t n; fread(&n, 8, 1, f); std::vector<uint64_t> a(3 * n); fread(a.data(), 8, 3 * n, f);
        for (uint64_t i = 0; i < n; i++) {
            u128 cells = 0; int c[64]; for (int q = 0; q < K; q++) { c[q] = (a[3 * i + q / 12] >> (5 * (q % 12))) & 31; cells |= (u128)c[q] << (5 * q); }
            u128 k = ((u128)phase_id(Ph[l][0], Ph[l][1], Ph[l][2]) << PS) | cells;
            tot++; if (!std::binary_search(C.begin(), C.end(), k)) miss++;
        }
    }
    printf("K=%d E=%llu Cyc=%llu missing-from-Cyc=%llu %s\n", K, (unsigned long long)tot, (unsigned long long)C.size(), (unsigned long long)miss, miss ? "VIOLATION" : "E subset Cyc");
    return 0;
}
