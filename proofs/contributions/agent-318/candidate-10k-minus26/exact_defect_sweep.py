def reverse10(n: int) -> int:
    return int(str(n)[::-1])

def step(n: int) -> int:
    return n + reverse10(n)

def palindrome(n: int) -> bool:
    s = str(n)
    return s == s[::-1]

def first_palindrome(seed: int, cap: int):
    n = seed
    for t in range(cap + 1):
        if palindrome(n):
            return t
        n = step(n)
    return None

def survivors(c_max=5000, k_lo=4, k_hi=8, cap=1000):
    out=[]
    for c in range(1,c_max):
        if all(first_palindrome(10**k-c,cap) is None for k in range(k_lo,k_hi+1)):
            out.append(c)
    return out

if __name__ == "__main__":
    s=survivors()
    print("c<5000, k=4..8, cap=1000:", s)
    for c in s:
        vals=[first_palindrome(10**k-c,3000) for k in range(4,13)]
        print(c, vals)
