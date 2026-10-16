#!/usr/bin/env python3
"""Agent #109 independent literal-integer control for agent102-ancestry-lean.

Written without reading Agent #102's control.py. For random positive integers,
compute actual orbits with Python big integers (n -> n + int(str(n)[::-1])),
their column-sum words q (q_i = d_i + d_{L-1-i}, i = 0 least significant), the
actual carries of the column-sum word, and check for every maximal 0/18 run
[a,b) of q:
 (i)/(iii) the set {i in [a,b) : q'_i = c} equals the `descendant` interval
     (no overflow: endpoints survive iff carry_a == h, carry_{L-b} == h;
      overflow: [a+1,b));
 (ii) a nonempty descendant is a maximal run of c in q';
 (iv) descendant length + overflow <= b-a;
and follow each tracked ancestry along the orbit, checking survival_bound
t + psi(p_t) <= 4(ell-1) + psi(p_0) and extinction by 4 ell - 3 + psi(p_0).
"""
import json, random, sys

def psi(p):
    return {1: 4, 2: 3, 3: 2, 4: 2, 5: 2, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1}.get(p, 0)

def colsum(n):
    d = [int(ch) for ch in str(n)[::-1]]
    L = len(d)
    return [d[i] + d[L - 1 - i] for i in range(L)]

def carries(q):
    """carry[i] = incoming carry into column i when evaluating sum q_i 10^i."""
    c = [0]
    for x in q:
        c.append((x + c[-1]) // 10)
    return c  # length L+1, c[L] = overflow

def maximal_runs(q, c):
    runs, i, L = [], 0, len(q)
    while i < L:
        if q[i] == c:
            j = i
            while j < L and q[j] == c: j += 1
            runs.append((i, j)); i = j
        else:
            i += 1
    return runs

def descendant(q, cr, c, a, b):
    L = len(q); h = 1 if c == 18 else 0
    if cr[L] == 0:
        return (a if cr[a] == h else a + 1, b if cr[L - b] == h else b - 1)
    return (a + 1, b)

def run_rich(rng, maxlen):
    """Random integer whose column-sum word has long 0/18 runs."""
    L = rng.randint(2, maxlen); half = (L + 1) // 2
    q = []
    while len(q) < half:
        c = rng.choice([0, 18, rng.randint(0, 18)])
        q += [c] * rng.randint(1, 8)
    q = q[:half]
    if q[0] == 0: q[0] = rng.randint(1, 18)
    if L % 2: q[-1] = 2 * (q[-1] // 2)
    d = [0] * L
    for i in range(half):
        j = L - 1 - i
        if i == j: d[i] = q[i] // 2
        else:
            hi = min(9, q[i]) if i == 0 else rng.randint(max(0, q[i] - 9), min(9, q[i]))
            d[j], d[i] = hi, q[i] - hi
    return int("".join(map(str, reversed(d))))

def main(trials=4000, seed=109, maxlen=40, steps=60):
    rng = random.Random(seed)
    nruns = nsteps = 0; max_ext = 0
    for _ in range(trials):
        if rng.random() < 0.3:
            L0 = rng.randint(1, maxlen)
            n = rng.randint(10 ** (L0 - 1), 10 ** L0 - 1)
        else:
            n = run_rich(rng, maxlen)
        q = colsum(n)
        # tracked ancestries: list of (c, a, b, t0data)
        tracked = []
        for c in (0, 18):
            for (a, b) in maximal_runs(q, c):
                tracked.append({"c": c, "ell": b - a, "psi0": psi(q[0]), "a": a, "b": b, "t": 0})
                nruns += 1
        for t in range(steps):
            cr = carries(q)
            n2 = n + int(str(n)[::-1])
            q2 = colsum(n2)
            assert len(q2) == len(q) + cr[len(q)]
            for tr in tracked:
                a, b, c = tr["a"], tr["b"], tr["c"]
                if a >= b: continue
                # tracked interval must be a maximal run of q
                assert all(q[i] == c for i in range(a, b))
                assert (a == 0 or q[a - 1] != c) and (b == len(q) or q[b] != c)
                d1, d2 = descendant(q, cr, c, a, b)
                for i in range(a, b):
                    assert (q2[i] == c) == (d1 <= i < d2), (n, c, a, b, i)
                if d1 < d2:
                    assert all(q2[i] == c for i in range(d1, d2))
                    assert (d1 == 0 or q2[d1 - 1] != c) and (d2 == len(q2) or q2[d2] != c)
                assert a <= d1 and d2 <= b and max(d2 - d1, 0) + cr[len(q)] <= b - a
                tr["a"], tr["b"], tr["t"] = d1, d2, t + 1
                if d1 < d2:
                    assert (t + 1) + psi(q2[0]) <= 4 * (tr["ell"] - 1) + tr["psi0"]
                else:
                    max_ext = max(max_ext, t + 1)
                    assert t + 1 <= 4 * tr["ell"] - 3 + tr["psi0"]
                nsteps += 1
            n, q = n2, q2
        for tr in tracked:
            assert tr["a"] >= tr["b"] or steps < 4 * tr["ell"] - 3 + tr["psi0"]
    print(json.dumps({"trials": trials, "seed": seed, "runs_tracked": nruns,
                      "run_steps_checked": nsteps, "max_extinction_time": max_ext,
                      "result": "PASS"}))

if __name__ == "__main__":
    main(*(int(x) for x in sys.argv[1:]))
