/* bitstats.c -- |F| and number of all-digit words in a k-column bitset. Usage: bitstats K BITS */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
  int K = atoi(argv[1]); uint64_t N = 1; for (int i = 0; i < K; i++) N *= 19;
  uint64_t nw = (N + 63) / 64, *F = malloc(nw * 8);
  FILE *f = fopen(argv[2], "rb"); if (!f || fread(F, 8, nw, f) != nw) return 1; fclose(f);
  uint64_t cnt = 0, dig = 0;
  for (uint64_t i = 0; i < nw; i++) cnt += __builtin_popcountll(F[i]);
  /* digit words: iterate over 10^K digit words */
  uint64_t P = 1; for (int i = 0; i < K; i++) P *= 10;
  for (uint64_t x = 0; x < P; x++) {
    uint64_t y = x, idx = 0, m = 1;
    for (int i = 0; i < K; i++) { idx += (y % 10) * m; y /= 10; m *= 19; }
    if ((F[idx >> 6] >> (idx & 63)) & 1) dig++;
  }
  printf("{\"k\": %d, \"F\": %llu, \"space\": %llu, \"digit_words_in_F\": %llu}\n", K,
         (unsigned long long)cnt, (unsigned long long)N, (unsigned long long)dig);
  return 0;
}
