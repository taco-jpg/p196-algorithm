#!/usr/bin/env python3
"""Exact verifier for Agent #18 finite-seed candidate 10828."""
def rev(n): return int(str(n)[::-1])
def step(n): return n + rev(n)
def pal(n):
    s = str(n)
    return s == s[::-1]

def pair_word(n):
    d = list(map(int, str(n)))
    return [a+b for a,b in zip(d, d[::-1])]

def template_match(w):
    # Agent #8/109 two-gap template, restricted to positive g,h and
    # phases c=1..17 except 9. B,A,C are arbitrary finite words;
    # C must be palindromic because the whole template is symmetric.
    L = len(w)
    for c in range(1,18):
        if c == 9: continue
        q = 18-c
        for g in range(1, L//2+1):
            if w[:g] != [c]*g or w[L-g:] != [c]*g: continue
            rem = w[g:L-g]
            for h in range(1, len(rem)//2+1):
                if rem[:h] != [q]*h or rem[-h:] != [q]*h: continue
                mid = rem[h:-h]
                for a_len in range(len(mid)//2+1):
                    A = mid[:a_len]
                    C = mid[a_len:len(mid)-a_len]
                    if C == C[::-1] and mid[len(mid)-a_len:] == A[::-1]:
                        return True, (c,g,h,a_len)
    return False, None

seed = 10828
n = seed
rows = []
for t in range(40):
    pw = pair_word(n)
    tm, witness = template_match(pw)
    rows.append((t,n,len(str(n)),pal(n),tm,witness))
    if t < 39:
        n = step(n)

first = [t for t,_,_,p,_,_ in rows if p]
assert first == [39], first
assert all(not p for t,_,_,p,_,_ in rows if t < 39)
assert all(not tm for _,_,_,_,tm,_ in rows)
for t in range(39):
    assert step(rows[t][1]) == rows[t+1][1]
print("first_palindrome_time=39")
print("nonpalindromic_prefix_through=38")
print("template_matches=0")
print("final_palindrome=", rows[-1][1])
