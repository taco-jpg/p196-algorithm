#!/usr/bin/env python3
"""Bounded diagnostic only; this is not a proof of the universal theorem."""
def is_palindrome(n):
    s = str(n)
    return s == s[::-1]

def check_witness(L, k):
    n = 1 + 2 * 10 ** (k - 1)
    if k > L:
        return n >= 10 ** L and n < 10 ** k
    i, j = L - k, k - 1
    di, dj = (n // 10**i) % 10, (n // 10**j) % 10
    return (2*k > L+1 and i < j and L-1-i == j
            and di != dj and n % 10 != 0)

def main():
    finite_cases = []
    for L in range(1, 6):
        pals = [n for n in range(10**(L-1), 10**L) if is_palindrome(n)]
        for k in range(1, L+2):
            target = {n % 10**k for n in range(1, 10**k) if n % 10}
            realized = {p % 10**k for p in pals}
            universal = target <= realized
            candidate = 2*k <= L+1
            finite_cases.append((L, k, universal, candidate, len(target-realized)))
    assert len(finite_cases) == 20
    assert all(u == c for _, _, u, c, _ in finite_cases)
    witness_cases = [(L,k) for L in range(1,12) for k in range(1,15)
                     if 2*k > L+1]
    assert len(witness_cases) == 118
    assert all(check_witness(L,k) for L,k in witness_cases)
    print("bounded cases:", len(finite_cases))
    print("candidate/finite-enumeration agreements:",
          sum(u == c for _,_,u,c,_ in finite_cases))
    print("proposed converse witness checks:", len(witness_cases))
    print("all witness checks passed: True")
    print("STATUS: diagnostic only; not a formal proof")

if __name__ == "__main__":
    main()
