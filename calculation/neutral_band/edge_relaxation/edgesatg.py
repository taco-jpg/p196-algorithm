#!/usr/bin/env python3
"""Edge relaxation for a 9-wire carrying a given stream, general overflow clock.
K cells of the cap sit directly on the wire (cell 0 = first non-9 cell above the wire); everything above them is free
(descending carry d[K] free every step). The stream bit s_t is the ascending carry arriving from the wire; the cap must
send d = 1 - s_t back down (wire condition c + d = 1). After T steps the cap pattern must return shifted up by `shift`
cells (the vacated cells become wire 9s).  SAT <=> a cap of the stream can drift `shift` cells per T steps.
usage: edgesatg.py clock stream T K shift_min shift_max"""
import sys, time
from pysat.solvers import Cadical153

def solve(clock, s, T, K, shift):
    g = [int(clock[t % len(clock)]) for t in range(T)]
    st = [int(s[t % len(s)]) for t in range(T)]
    nv = [0]
    def new(): nv[0] += 1; return nv[0]
    cl = []; TRUE = new(); cl.append([TRUE]); const = lambda b: TRUE if b else -TRUE
    P = [[[new() for v in range(19)] for j in range(K)] for t in range(T + 1)]
    for t in range(T + 1):
        for j in range(K):
            cl.append(P[t][j][:])
            for v in range(19):
                for u in range(v): cl.append([-P[t][j][v], -P[t][j][u]])
    for t in range(T):
        c = [const(st[t])] + [new() for j in range(K)]
        d = [new() for j in range(K)] + [new()]          # d[K] free (from above)
        dm1 = new(); cl.append([dm1] if 1 - st[t] else [-dm1])
        E = [[new() for u in range(10)] for j in range(K)]; R = [[new() for u in range(10)] for j in range(K)]
        for j in range(K):
            cl.append(E[j][:]); cl.append(R[j][:])
            for v in range(19):
                for x in (0, 1):
                    sm = v + x
                    pre = [-P[t][j][v], -c[j] if x else c[j]]
                    cl.append(pre + [E[j][sm % 10]]); cl.append(pre + [c[j + 1] if sm >= 10 else -c[j + 1]])
                    pre = [-P[t][j][v], -d[j + 1] if x else d[j + 1]]   # carry into mirror of cell j comes from cell j+1 side
                    cl.append(pre + [R[j][sm % 10]])
                    tgt = d[j]                                           # carry sent below cell j
                    cl.append(pre + [tgt if sm >= 10 else -tgt])
            # d[0] is the carry sent into the wire
        cl.append([d[0], -dm1]); cl.append([-d[0], dm1])
        rwire = 9 * st[t]
        for j in range(K):
            for x in range(10):
                if g[t]:
                    if j == 0: cl.append([-E[j][x], P[t + 1][j][x + rwire]])
                    else:
                        for y in range(10): cl.append([-E[j][x], -R[j - 1][y], P[t + 1][j][x + y]])
                else:
                    for y in range(10): cl.append([-E[j][x], -R[j][y], P[t + 1][j][x + y]])
    cl.append([-P[0][0][9]])
    for j in range(shift): cl.append([P[T][j][9]])
    for j in range(K - shift):
        for v in range(19):
            cl.append([-P[0][j][v], P[T][j + shift][v]]); cl.append([P[0][j][v], -P[T][j + shift][v]])
    sol = Cadical153(bootstrap_with=cl); t0 = time.time(); r = sol.solve(); sol.delete()
    return r, time.time() - t0

if __name__ == '__main__':
    clock, stream, T, K, s0, s1 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    res = []
    for sh in range(s0, s1 + 1):
        r, dt = solve(clock, stream, T, K, sh)
        res.append(f'{sh}:{"S" if r else "-"}')
        print(f'clock={clock} stream={stream} T={T} K={K} shift={sh}: {"SAT" if r else "UNSAT"} ({dt:.1f}s)', flush=True)
    print('SUMMARY', clock, stream, 'T', T, 'K', K, ' '.join(res))
