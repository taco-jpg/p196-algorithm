#!/usr/bin/env python3
"""Generate enrichment automata (delta tables) for fwdbfs.c, and check each one
against the actual 196 orbit (orbit196.c output) so the enriched system is sound:
for every t >= t0 the actual value E(t+1) == delta[E(t)][b_t][e_t].

Each enrichment E is a function of the actual state (number n, width L, time t,
the inner carry used on the previous step) whose update depends only on the
overflow bit b (= c_L) and the free inner carry e (= c_{L-k}) -- there is no guard.

Usage: gen_tables.py ORBIT_FILE T0 K OUTDIR
Writes OUTDIR/<name>.tbl for every enrichment and prints "name NE E0".
"""
import os
import sys


def table_lmod(m, L0):
    return m, L0 % m, [[[(E + b) % m for e in (0, 1)] for b in (0, 1)] for E in range(m)]


def r99_update(r, p):
    """n -> n + rev(n) mod 99 from (n mod 99, L mod 2).
    rev(n) = n (mod 9) ; rev(n) = (-1)^(L-1) n (mod 11)."""
    r9, r11 = r % 9, r % 11
    s9 = (2 * r9) % 9
    s11 = (r11 + (r11 if p == 1 else -r11)) % 11
    # CRT back to mod 99
    for x in range(99):
        if x % 9 == s9 and x % 11 == s11:
            return x
    raise AssertionError


def table_r99p(r0, p0):
    NE = 198
    tab = []
    for E in range(NE):
        r, p = divmod(E, 2)
        row = []
        for b in (0, 1):
            r2 = r99_update(r, p)
            p2 = p ^ b
            row.append([r2 * 2 + p2, r2 * 2 + p2])
        tab.append(row)
    return NE, r0 * 2 + p0, tab


def table_r11p(r0, p0):
    NE = 22
    tab = []
    for E in range(NE):
        r, p = divmod(E, 2)
        row = []
        for b in (0, 1):
            r2 = (r + (r if p == 1 else -r)) % 11
            row.append([r2 * 2 + (p ^ b)] * 2)
        tab.append(row)
    return NE, r0 * 2 + p0, tab


def table_r9(r0):
    return 9, r0, [[[(2 * E) % 9] * 2 for b in (0, 1)] for E in range(9)]


def table_clock(m, t0):
    return m, t0 % m, [[[(E + 1) % m] * 2 for b in (0, 1)] for E in range(m)]


def table_preve(e0):
    return 2, e0, [[[0, 1] for b in (0, 1)] for E in range(2)]


def table_prevbe(b0, e0):
    return 4, b0 * 2 + e0, [[[b * 2 + 0, b * 2 + 1] for b in (0, 1)] for E in range(4)]


def table_combo(r0, L0, e0):
    """(n mod 99, L mod 12, previous e)  -- NE = 99*12*2 = 2376"""
    NE = 99 * 12 * 2
    tab = []
    for E in range(NE):
        r, rest = divmod(E, 24)
        lm, pe = divmod(rest, 2)
        row = []
        for b in (0, 1):
            r2 = r99_update(r, lm % 2)
            l2 = (lm + b) % 12
            row.append([(r2 * 12 + l2) * 2 + e for e in (0, 1)])
        tab.append(row)
    return NE, (r0 * 12 + L0 % 12) * 2 + e0, tab


def read_orbit(path):
    rows = {}
    with open(path) as f:
        for line in f:
            a = list(map(int, line.split()))
            t = a[0]
            rows[t] = dict(t=t, L=a[1], b=a[2], r99=a[3], pal=a[4], q=a[5:17], e=a[17:29])
    return rows


def actual_E(name, row, prev, k):
    t, L, r = row["t"], row["L"], row["r99"]
    if name == "lmod2":
        return L % 2
    if name.startswith("lmod"):
        return L % int(name[4:])
    if name == "r99p":
        return r * 2 + L % 2
    if name == "r11p":
        return (r % 11) * 2 + L % 2
    if name == "r9":
        return r % 9
    if name == "clock6":
        return t % 6
    if name == "preve":
        return prev["e"][k - 1]
    if name == "prevbe":
        return prev["b"] * 2 + prev["e"][k - 1]
    if name == "combo":
        return (r * 12 + L % 12) * 2 + prev["e"][k - 1]
    raise KeyError(name)


def main():
    orbit, t0, k, outdir = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rows = read_orbit(orbit)
    R, P = rows[t0], rows[t0 - 1]
    os.makedirs(outdir, exist_ok=True)
    tables = {}
    for m in (2, 3, 4, 5, 6, 7, 8, 10, 12):
        tables[f"lmod{m}"] = table_lmod(m, R["L"])
    tables["r99p"] = table_r99p(R["r99"], R["L"] % 2)
    tables["r11p"] = table_r11p(R["r99"] % 11, R["L"] % 2)
    tables["r9"] = table_r9(R["r99"] % 9)
    tables["clock6"] = table_clock(6, t0)
    tables["preve"] = table_preve(P["e"][k - 1])
    tables["prevbe"] = table_prevbe(P["b"], P["e"][k - 1])
    tables["combo"] = table_combo(R["r99"], R["L"], P["e"][k - 1])
    tmax = max(rows)
    for name, (NE, E0, tab) in tables.items():
        # soundness along the actual orbit: E(t0) == E0 and E(t+1) == delta[E(t)][b_t][e_t]
        assert actual_E(name, R, P, k) == E0, name
        E = E0
        for t in range(t0, tmax):
            row, nxt = rows[t], rows[t + 1]
            E = tab[E][row["b"]][row["e"][k - 1]]
            assert E == actual_E(name, nxt, row, k), (name, t)
        with open(os.path.join(outdir, f"{name}.tbl"), "w") as f:
            f.write(f"{NE} {E0}\n")
            for E in range(NE):
                f.write(" ".join(str(tab[E][b][e]) for b in (0, 1) for e in (0, 1)) + "\n")
        print(name, NE, E0, f"sound on t={t0}..{tmax}")


if __name__ == "__main__":
    main()
