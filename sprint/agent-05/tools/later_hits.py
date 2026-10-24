"""How many per-prefix maxima come from a palindrome that is NOT the seed's first palindrome.

usage: python3 later_hits.py max_delay_P4.tsv

A search that stops at the first palindrome of each orbit would miss these;
the Agent124 ancestry bound constrains every t with orbit(A,t) a palindrome.
"""
import sys
n = later = 0; ex = []
for line in open(sys.argv[1]):
    if line.startswith("prefix"): continue
    p, t, s = line.split("\t")[:3]; t, s = int(t), int(s)
    x = s; first = None
    for k in range(1, t + 1):
        x += int(str(x)[::-1]); z = str(x)
        if z == z[::-1]: first = k; break
    n += 1
    if first is not None and first < t:
        later += 1
        if len(ex) < 5 or t > ex[-1][1]: ex.append((p, t, s, first)); ex = sorted(ex, key=lambda e: -e[1])[:5]
print(f"{later} of {n} per-prefix maxima are later (non-first) palindrome hits")
print("largest examples (prefix, delay, seed, first palindrome time):", ex)
