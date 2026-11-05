"""Cross-check of stack_uniform.py against bx: |CL_k(A)| (distinct cut words of length 12k) vs bxs -nosym state counts."""
import sys
sys.argv = [sys.argv[0]] + sys.argv[1:]
exec(open(__file__.replace('stack_crosscheck.py', 'stack_uniform.py')).read().split('# --- AT edges')[0])
NX = 2 * b - 1
for k in range(1, int(sys.argv[2]) + 1 if len(sys.argv) > 2 else 4):
    words = set()
    for x0 in range(NX):
        # DFS over 12k steps keeping label
        frontier = {(x0, ())}
        for t in range(12 * k):
            f = t % P; nf = set()
            for x, lab in frontier:
                for xn, a in A[f][x]: nf.add((xn, lab + (a,)))
            frontier = nf
        for x, lab in frontier:
            if x == x0: words.add(lab)
    print('k', k, '|CL_k(A)|', len(words))
