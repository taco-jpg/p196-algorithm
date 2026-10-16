"""Re-derive the 13 sharpness witnesses (as stated in TwoDigitMain.lean,
SharpAt a b R h k) and the first 7 orbit values of 196.  Uses an arithmetic
reversal (no string ops) independent of the DP script."""

def rev(n):
    r = 0
    while n:
        r = 10 * r + n % 10
        n //= 10
    return r

def T(n):
    return n + rev(n)

def pal(n):
    return rev(n) == n

# (a, b, R, h, k) exactly as in TwoDigitMain.lean sharp_ab
SHARP = [(1, 0, 100, 1, 1), (2, 0, 1005000, 2, 5), (3, 2, 12090, 2, 3),
         (4, 0, 1008000, 3, 5), (4, 1, 1008400, 3, 5), (6, 0, 1103090, 3, 5),
         (6, 4, 1203090, 3, 5), (6, 5, 1203290, 6, 6), (7, 6, 17590, 3, 3),
         (8, 0, 1009000, 4, 5), (8, 1, 1009200, 4, 5), (8, 2, 1006500, 4, 5),
         (8, 3, 1009400, 4, 5)]
BOUNDS = {(1, 0): 1, (2, 0): 2, (3, 2): 2, (4, 0): 3, (4, 1): 3, (6, 0): 3,
          (6, 4): 3, (6, 5): 6, (7, 6): 3, (8, 0): 4, (8, 1): 4, (8, 2): 4,
          (8, 3): 4}

ok = True
for a, b, R, h, k in SHARP:
    path = [R]
    for _ in range(h):
        path.append(T(path[-1]))
    P = path[-1]
    c1 = pal(P)
    c2 = not any(pal(x) for x in path[:-1])
    c3 = P // 10 ** k == 10 * a + b
    c4 = str(P)[:2] == f"{a}{b}"
    c5 = h == BOUNDS[(a, b)]
    good = c1 and c2 and c3 and c4 and c5 and R > 0
    ok &= good
    print(f"{a}{b}: R={R} h={h} path={path} P/10^{k}={P // 10 ** k} "
          f"pal={c1} firstPal={c2} prefixOK={c3 and c4} h==bound={c5} -> {good}")
print("1203290 % 11 =", 1203290 % 11)
orb = [196]
for _ in range(7):
    orb.append(T(orb[-1]))
print("orbit 196, t=0..7:", orb, "palindromes:", [pal(x) for x in orb])
print("ALL SHARP OK" if ok else "SHARP FAILURE")
