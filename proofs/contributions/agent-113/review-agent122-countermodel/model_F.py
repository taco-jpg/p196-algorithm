"""Independent numerical model of Agent122's countermap F with ell(a)=a.
Checks concrete clauses on small inputs; not a proof."""
import sys
def rev(n): return int(str(n)[::-1])
def T(n): return n + rev(n)
def pal(n): s = str(n); return s == s[::-1]
def B(n): return pal(T(n))
def node(a, j): return 10**(a+j) + 10*a + 9
def terminal(a, k): return 10**(a+k+1) + 2
ell = lambda a: a
def node_of(n):
    s = str(n); L = len(s)
    # node(a,j) has width a+j+1, leading 1, then zeros, then the two-digit tail 10a+9 (a>=3)
    for a in range(3, L):
        j = L - 1 - a
        if j >= 0 and j <= ell(a) and node(a, j) == n: return (a, j)
    return None
def F(n):
    if B(n): return T(n)
    p = node_of(n)
    if p:
        a, j = p
        return node(a, j+1) if j < ell(a) else terminal(a, ell(a))
    L = len(str(n))
    return 19 if L == 1 else 109 if L == 2 else node(L, 0)
fails = 0
N = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
for n in range(1, N):
    f = F(n)
    if B(n) and f != T(n): fails += 1
    if pal(f) != B(n): fails += 1
    if not (n < f < 11*n): fails += 1
    w, wf = len(str(n)), len(str(f))
    if not (w <= wf <= w+1): fails += 1
    if not B(n) and wf != w+1: fails += 1
# exact first-hit from node(a,0) is ell(a)+2, and 5-step width floor
for a in range(3, 12):
    x, t = node(a, 0), 0
    seen = []
    while True:
        seen.append(x)
        if pal(x): break
        x = F(x); t += 1
    if t != ell(a) + 2: fails += 1; print("first-hit mismatch", a, t)
    # width floor: width(F^t n) >= width(n) + t//5
    for tt, y in enumerate(seen):
        if len(str(y)) < len(str(seen[0])) + tt // 5: fails += 1
    # true upper clock violated at t=4 for a>=4 (countermap), holds for real orbit
    if a >= 4:
        y = node(a, 0)
        for _ in range(4): y = F(y)
        z = node(a, 0)
        for _ in range(4): z = T(z)
        if not (2*len(str(y)) > 2*len(str(node(a,0))) + 7): fails += 1
        if not (2*len(str(z)) <= 2*len(str(node(a,0))) + 7): fails += 1
# every positive seed terminates (sampled)
for n in range(1, 20000):
    x, t = F(n), 1
    while not pal(x) and t < 400: x = F(x); t += 1
    if not pal(x): fails += 1; print("no termination", n)
print("N", N, "failures", fails)
