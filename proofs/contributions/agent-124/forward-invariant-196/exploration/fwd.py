import sys
sys.setrecursionlimit(10000)
def T(n): return n + int(str(n)[::-1])
def pair_word(n):
    d = [int(c) for c in str(n)][::-1]  # units first
    L = len(d)
    return [d[i] + d[L-1-i] for i in range(L)]
def forward_prefixes(s):
    k = len(s); low, carry = [], 0
    for v in s:
        carry, d = divmod(v + carry, 10); low.append(d)
    out = set()
    for inner in (0, 1):
        high, c = [0]*k, inner
        for i in range(k-1, -1, -1):
            c, high[i] = divmod(s[i] + c, 10)
        if c:
            p = (1 + low[0],) + tuple(low[i] + high[i-1] for i in range(1, k))
        else:
            p = tuple(a + b for a, b in zip(low, high))
        out.add(p)
    return out
k = int(sys.argv[1]); t0 = int(sys.argv[2])
n = 196
for _ in range(t0): n = T(n)
w0 = tuple(pair_word(n)[:k])
seen = {w0}; stack = [w0]
while stack:
    w = stack.pop()
    for p in forward_prefixes(w):
        if p not in seen:
            seen.add(p); stack.append(p)
print('k', k, 't0', t0, 'w0', w0, 'forward reachable', len(seen), 'of', 18*19**(k-1))
# which leading digit-word prefixes (digits <=9, first k entries) are reachable
digit_words = [w for w in seen if all(x <= 9 for x in w)]
print('reachable all-digit words', len(digit_words))
