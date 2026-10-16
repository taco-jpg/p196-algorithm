from fractions import Fraction

def step(n: int) -> int:
    return n + int(str(n)[::-1])

def iterate(k: int, c: int, t: int) -> int:
    n = 10**k - c
    for _ in range(t):
        n = step(n)
    return n

def affine_fit(c: int, t: int, k1: int = 20, k2: int = 21):
    y1 = iterate(k1, c, t)
    y2 = iterate(k2, c, t)
    a = Fraction(y2-y1, 10**k2-10**k1)
    b = y1-a*10**k1
    return a, b

def first_nonlinear(c: int, check_ks=(10,11,12,15,20,25), cap=80):
    for t in range(cap+1):
        a,b=affine_fit(c,t)
        if any(Fraction(iterate(k,c,t)) != a*10**k+b for k in check_ks):
            return t
    return None

if __name__ == "__main__":
    for c in (26, 1402, 4832):
        print("c", c, "first nonlinear t", first_nonlinear(c))
    print("c=26 affine coefficients through t=14:")
    for t in range(15):
        print(t, affine_fit(26,t))
