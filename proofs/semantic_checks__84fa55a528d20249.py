"""Numerical cross-checks of the semantic lemmas the chain proof relies on.

(A) tri_step: width n >= 3 -> exists e in {0,1} (the actual carry into
    column L-3) with tri(T n) = nextT(tri n, e), width(T n) = width n + topT.
    Exhaustive for 1 <= n < 10**6, plus random n of width 3..60.
(B) Lemma 1 (width_step_eq_of_small_descending): if every pair sum of T m is
    <= 9 and pair1(T m) < pair0(T m) then width(T m) = width m.
    Exhaustive for 1 <= m < LIMIT_B.
(C) The exact induction invariant `key` of Cert.ancestry_bound: if
    T^(i+1)(n) is a palindrome with one of the 13 prefixes, then
    width(n) >= 3 and tri(n) is in layer i of that prefix's certificate
    (layers decoded from the committed Lean files); in particular i < h.
    Exhaustive for 1 <= n < LIMIT_C, i up to 12.
"""
import random, re, sys, os
sys.setrecursionlimit(10000)
PKG = sys.argv[1]
LIMIT_B = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 7
LIMIT_C = int(sys.argv[3]) if len(sys.argv) > 3 else 2 * 10 ** 6

def hi2(s2, e): return (s2 + e) // 10
def hi1(s1, s2, e): return (s1 + hi2(s2, e)) // 10
def top(s0, s1, s2, e): return (s0 + hi1(s1, s2, e)) // 10
def nxt(s0, s1, s2, e):
    if top(s0, s1, s2, e) == 0:
        return (s0 % 10 + (s0 + hi1(s1, s2, e)) % 10,
                (s1 + s0 // 10) % 10 + (s1 + hi2(s2, e)) % 10,
                (s2 + (s1 + s0 // 10) // 10) % 10 + (s2 + e) % 10)
    return (s0 % 10 + 1,
            (s1 + s0 // 10) % 10 + (s0 + hi1(s1, s2, e)) % 10,
            (s2 + (s1 + s0 // 10) // 10) % 10 + (s1 + hi2(s2, e)) % 10)

def T(n): return n + int(str(n)[::-1])
def digits(n): return [int(c) for c in str(n)[::-1]]          # units first
def pairs(n):
    d = digits(n); L = len(d)
    return [d[i] + d[L - 1 - i] for i in range(L)]
def tri(n):
    p = pairs(n); return (p[0], p[1], p[2])
def carry_into(n, j):
    """actual carry entering column j when computing n + rev(n)."""
    q = pairs(n); c = 0
    for i in range(j):
        c = (q[i] + c) // 10
    return c

# (A)
badA = 0; cntA = 0
def checkA(n):
    global badA, cntA
    L = len(str(n))
    if L < 3: return
    cntA += 1
    e = carry_into(n, L - 3)
    w = tri(n); m = T(n)
    if not (e <= 1 and tri(m) == nxt(*w, e) and len(str(m)) == L + top(*w, e)):
        badA += 1
        if badA < 5: print("A-FAIL", n, e, w, tri(m))
for n in range(1, 10 ** 6):
    checkA(n)
rng = random.Random(20261015)
for _ in range(300000):
    L = rng.randint(3, 60)
    n = rng.randint(10 ** (L - 1), 10 ** L - 1)
    checkA(n)
# adversarial: long runs of 9s/0s and pair sums near 9/10 boundaries
for L in range(3, 40):
    for _ in range(3000):
        d = [rng.choice([0, 9, 9, 9, 0, 1, 8, rng.randint(0, 9)]) for _ in range(L)]
        if d[-1] == 0: d[-1] = rng.randint(1, 9)
        checkA(int("".join(map(str, reversed(d)))))
print(f"(A) tri_step checked on {cntA} numbers, failures={badA}")

# (B)
badB = 0; cntB = 0
for m in range(1, LIMIT_B):
    s = m + int(str(m)[::-1])
    st = str(s); L = len(st)
    if L < 2: continue
    # pair sums of s; small-and-descending test
    p0 = int(st[0]) + int(st[-1]); p1 = int(st[1]) + int(st[-2])
    if p1 >= p0: continue
    ok = True
    for i in range(L):
        if int(st[i]) + int(st[L - 1 - i]) > 9:
            ok = False; break
    if not ok: continue
    cntB += 1
    if L != len(str(m)):
        badB += 1
        if badB < 5: print("B-FAIL", m, s)
print(f"(B) Lemma 1 hypotheses met by {cntB} values m < {LIMIT_B}, failures={badB}")

# (C)
def decode(mask):
    out, k = set(), 0
    while mask:
        if mask & 1: out.add((k // 361, k // 19 % 19, k % 19))
        mask >>= 1; k += 1
    return out
LAYERS = {}
for name in ["10", "20", "32", "40", "41", "60", "64", "65", "76", "80", "81", "82", "83"]:
    src = open(os.path.join(PKG, f"TwoDigitCert{name}.lean")).read()
    body = re.search(r"layers := \[(.*?)\]", src, re.S).group(1)
    LAYERS[name] = [decode(int(x)) for x in re.findall(r"\d+", body)]
badC = 0; cntC = 0; maxi = {k: -1 for k in LAYERS}
for n in range(1, LIMIT_C):
    x = n
    for i in range(12):
        x = T(x)
        sx = str(x)
        if sx == sx[::-1] and sx[:2] in LAYERS:
            ab = sx[:2]; Ls = LAYERS[ab]
            cntC += 1
            maxi[ab] = max(maxi[ab], i)
            if not (len(str(n)) >= 3 and i < len(Ls) and tri(n) in Ls[i]):
                badC += 1
                if badC < 5: print("C-FAIL", n, i, x)
print(f"(C) invariant instances checked={cntC} for n < {LIMIT_C}, failures={badC}; "
      f"max layer index i reached per prefix={maxi}")
