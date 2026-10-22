"""Cross-check orbit196.c output against Python big-integer reverse-and-add.
Usage: chk_orbit.py ORBIT_FILE (rows for t = 0..T)."""
import sys
sys.set_int_max_str_digits(0)
sys.path.insert(0, __import__("os").path.dirname(__file__))
from fwdref import forward_prefix, project, inner_carry, step
rows = [list(map(int, l.split())) for l in open(sys.argv[1])]
n = 196
for r in rows:
    t, L, ovf, r99, pal = r[:5]
    q = r[5:17]; e = r[17:29]
    s = str(n)
    assert len(s) == L, t
    assert r99 == n % 99, t
    assert pal == (s == s[::-1]), t
    assert q[:min(12,L)] == project(n, 12), t
    for k in range(1, min(12, L) + 1):
        assert e[k-1] == inner_carry(n, k), (t, k)
    m = step(n)
    assert ovf == len(str(m)) - L
    n = m
print("orbit rows verified against Python big integers:", len(rows))
