// Iterate reverse-and-add from 196 and print, at requested times t, the
// width L and the first 10 column sums q_i = d_i + d_{L-1-i} (units end first).
// Usage: orbit196 t1 t2 ... (increasing)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char **argv) {
  long maxT = atol(argv[argc - 1]);
  long cap = maxT / 2 + 64;
  unsigned char *d = calloc(cap, 1), *e = calloc(cap, 1);
  long L = 3;
  d[0] = 6; d[1] = 9; d[2] = 1;  // 196, units first
  int ai = 1;
  for (long t = 0; t <= maxT; t++) {
    while (ai < argc && atol(argv[ai]) == t) {
      int pal = 1;
      for (long i = 0; i < L / 2; i++) if (d[i] != d[L - 1 - i]) { pal = 0; break; }
      printf("t=%ld L=%ld pal=%d q=", t, L, pal);
      for (int i = 0; i < 10 && i < L; i++) printf(i ? ",%d" : "%d", d[i] + d[L - 1 - i]);
      printf("\n");
      ai++;
    }
    if (t == maxT) break;
    int c = 0;
    for (long i = 0; i < L; i++) {
      int s = d[i] + d[L - 1 - i] + c;
      e[i] = (unsigned char)(s % 10);
      c = s / 10;
    }
    if (c) e[L++] = 1;
    unsigned char *tmp = d; d = e; e = tmp;
  }
  return 0;
}
