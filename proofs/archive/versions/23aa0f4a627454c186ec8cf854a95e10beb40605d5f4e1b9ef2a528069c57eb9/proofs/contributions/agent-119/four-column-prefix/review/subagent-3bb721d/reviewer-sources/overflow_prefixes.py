"""Brute force: 3-digit prefixes of palindromes (width >= 3) produced by an
overflowing step (len(T(n)) > len(n)), for 1 <= n < N.  Usage: N"""
import sys, json
N = int(sys.argv[1]); seen = {}; cnt = 0
for n in range(1, N):
    s = str(n); m = n + int(s[::-1]); t = str(m)
    if len(t) > len(s) and len(t) >= 3 and t == t[::-1]:
        cnt += 1; seen[t[:3]] = seen.get(t[:3], 0) + 1
print(json.dumps({'N': N, 'overflow_palindrome_steps': cnt, 'prefixes': dict(sorted(seen.items()))}))
