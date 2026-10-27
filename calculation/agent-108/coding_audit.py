#!/usr/bin/env python3
"""Independent arithmetic audit of the saturated two-column exterior relation."""
from itertools import product


def local_step(q, boundary):
    """Two columns, arbitrary inward right carry; no repository imports."""
    left = [0]
    ld = []
    for x in q:
        digit, carry = (x + left[-1]) % 10, (x + left[-1]) // 10
        ld.append(digit)
        left.append(carry)
    right = [0, 0, boundary]
    rd = [0, 0]
    for j in (1, 0):
        rd[j] = (q[j] + right[j + 1]) % 10
        right[j] = (q[j] + right[j + 1]) // 10
    overflow = right[0]
    out = (ld[0] + 1, ld[1] + rd[0]) if overflow else tuple(x+y for x,y in zip(ld,rd))
    return out, overflow, tuple(left), tuple(right)


def enumerate_relation():
    paths = []
    for y in range(19):
        for bits in product(range(2), repeat=4):
            q = (10, y)
            trace = [q]
            for t, boundary in enumerate(bits):
                q, g, _, _ = local_step(q, boundary)
                if g != (t == 0) or q[0] != (1, 2, 5, 10)[t]:
                    break
                trace.append(q)
            else:
                paths.append((y, q[1], bits, tuple(trace)))
    return paths


def main():
    paths = enumerate_relation()
    # Floyd reachability is deliberately distinct from a DFS/SCC implementation.
    reach = [[False]*19 for _ in range(19)]
    for u,v,_,_ in paths:
        reach[u][v] = True
    for k in range(19):
        for i in range(19):
            for j in range(19):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
    cyclic_nodes = {i for i in range(19) if reach[i][i]}
    recurrent = {(u,v,bits,trace) for u,v,bits,trace in paths if reach[v][u]}
    expected = set()
    for a,b,c,h in product(range(2), repeat=4):
        u,v = 4+9*a+b, 4+9*b+c
        bits = (h,1,b*c,b^c)
        trace = ((10,u), (1,5+b), (2,11+2*b), (5,2+4*b+b*c), (10,v))
        expected.add((u,v,bits,trace))
    if cyclic_nodes != {4,5,13,14} or recurrent != expected:
        raise RuntimeError((cyclic_nodes,recurrent,expected))
    print(f'ALL CHECKS PASSED: raw_paths={len(paths)}, cyclic_nodes={sorted(cyclic_nodes)}, recurrent_edges={len({(u,v) for u,v,_,_ in recurrent})}, recurrent_carry_paths={len(recurrent)}')


if __name__ == '__main__':
    main()
