from typing import Callable

def reverse10(n: int) -> int:
    return int(str(n)[::-1])

def step(n: int) -> int:
    return n + reverse10(n)

def palindrome(n: int) -> bool:
    s = str(n)
    return s == s[::-1]

def seed(k: int) -> int:
    assert k >= 4
    return 10**k - 26

def iterate(k: int, t: int) -> int:
    n = seed(k)
    for _ in range(t):
        n = step(n)
    return n

def expected(k: int, t: int) -> int | None:
    if t == 0:
        return 10**k - 26
    if t == 1:
        return int("147" + "9"*(k-4) + "73")
    if t == 2 and k >= 5:
        return int("527" + "9"*(k-5) + "714")
    if t == 3 and k >= 5:
        return int("945" + "9"*(k-5) + "439")
    if t == 4 and k >= 6:
        return int("1880" + "9"*(k-6) + "8988")
    return None

def check_parametric_formulas(k_max: int = 200) -> None:
    for k in range(4, k_max + 1):
        assert iterate(k, 0) == expected(k, 0)
        assert iterate(k, 1) == expected(k, 1)
        if k >= 5:
            assert iterate(k, 2) == expected(k, 2)
            assert iterate(k, 3) == expected(k, 3)
        if k >= 6:
            assert iterate(k, 4) == expected(k, 4)

def first_palindrome(k: int, cap: int) -> int | None:
    n = seed(k)
    for t in range(cap + 1):
        if palindrome(n):
            return t
        n = step(n)
    return None

if __name__ == "__main__":
    check_parametric_formulas()
    print("exact closed forms: PASS in their stated parameter ranges, k<=200")
    for k in range(4, 13):
        print(k, first_palindrome(k, 5000))
