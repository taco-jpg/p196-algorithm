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
    m = k - 4
    forms: dict[int, Callable[[int], int]] = {
        0: lambda m: 10**(m+4) - 26,
        1: lambda m: int("147" + "9"*m + "73"),
        2: lambda m: int("527" + "9"*m + "714"),
        3: lambda m: int("945" + "9"*m + "439"),
        4: lambda m: int("1880" + "9"*m + "8988"),
    }
    return forms.get(t, lambda m: None)(m)

def check_parametric_formulas(k_max: int = 200) -> None:
    for k in range(4, k_max + 1):
        for t in range(5):
            got = iterate(k, t)
            want = expected(k, t)
            assert got == want, (k, t, got, want)

def first_palindrome(k: int, cap: int) -> int | None:
    n = seed(k)
    for t in range(cap + 1):
        if palindrome(n):
            return t
        n = step(n)
    return None

if __name__ == "__main__":
    check_parametric_formulas()
    print("exact first-five-step formulas: PASS for k=4..200")
    for k in range(4, 13):
        print(k, first_palindrome(k, 5000))
