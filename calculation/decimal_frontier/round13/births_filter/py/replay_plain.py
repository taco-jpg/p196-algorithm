#!/usr/bin/env python3
"""r12e3: independent plain-integer replay of a TOP99 hit (second check next to py/extract_hit.py + verify_ext.verify).
It does NOT import neutral_band_search or verify_ext.  The closed L-walk is read from the khxt -dump TOP99_HIT block in the same
way as extract_hit.py (start = smallest id in phase 0, follow the out-edge that stays in the block); B_t = window of the t-th
walk node with the trailing 9s removed.  Then, for every t = 0..L-1, with plain Python ints and decimal strings only:
  x_t   = the decimal number whose pair word (p_i = d_i + d_{n-1-i}, least significant first) is
          B_t + [9]*G + [c_t] + [9]*G + reverse(B_t),  c_t = 18 if the low block B_t gives no carry, else 0 (centre with e2 = 1-e1);
  y_t   = x_t + int(str(x_t)[::-1])          (one true reverse-and-add step);
  check (a) the pair word of y_t starts with B_{t+1} (indices mod L) followed by at least G-1 nines,
        (b) len(y_t) - len(x_t) == g_t (clock bit: the step overflows iff g_t = 1),
        (c) the walk closes (B_L = B_0, checked by the walk) and reports e_t = carry out of the low |B_t| digits of x_t + rev(x_t).
usage: replay_plain.py DUMP WORD L [G=8]   -> prints PLAIN-REPLAY OK / FAIL with the first mismatches."""
import sys
fn, word, L = sys.argv[1], sys.argv[2], int(sys.argv[3]); G = int(sys.argv[4]) if len(sys.argv) > 4 else 8
P = len(word); g = word * (L // P); assert len(g) == L
nodes = {}; inblock = False
for l in open(fn):
    if l.startswith('# TOP99_HIT'): inblock = True; nodes = {}; continue
    if l.startswith('#'): inblock = False; continue
    if inblock and ':' in l:
        h, xs = l.split(':'); hh = h.split()
        nodes[int(hh[0])] = (int(hh[1]), int(hh[2]), int(hh[3]), [int(v) for v in xs.split()])
start = min(i for i, n in nodes.items() if n[0] == 0); walk = [start]
for _ in range(L - 1):
    t, o0, o1, x = nodes[walk[-1]]; nxt = [o for o in (o0, o1) if o >= 0 and o in nodes]; walk.append(nxt[0])
closes = start in nodes[walk[-1]][1:3]
def trim9(x):
    x = list(x)
    while x and x[-1] == 9: x.pop()
    return x
B = [trim9(nodes[i][3]) for i in walk]
def number(pw):                                   # pair word (LSF) -> decimal string of a number with that pair word
    n = len(pw); d = [0] * n
    for i in range(n // 2): d[i] = pw[i] // 2; d[n - 1 - i] = pw[i] - pw[i] // 2
    if n % 2: assert pw[n // 2] % 2 == 0; d[n // 2] = pw[n // 2] // 2
    assert all(0 <= v <= 9 for v in d) and d[-1] != 0
    return ''.join(str(v) for v in reversed(d))  # most significant first
def pairword(s):                                  # decimal string (MSF) -> pair word (LSF)
    d = [int(c) for c in reversed(s)]; return [a + b for a, b in zip(d, reversed(d))]
fails = []; es = []
for t in range(L):
    Bt, Bn = B[t], B[(t + 1) % L]
    w = len(Bt); xs = number(Bt + [9] * G + [0] + [9] * G + Bt[::-1])
    x = int(xs); r = int(xs[::-1]); low = (x % 10 ** w + r % 10 ** w) // 10 ** w      # carry out of the low block
    c = 18 if low == 0 else 0
    xs = number(Bt + [9] * G + [c] + [9] * G + Bt[::-1]); x = int(xs); r = int(xs[::-1])
    assert (x % 10 ** w + r % 10 ** w) // 10 ** w == low
    ys = str(x + r); pw = pairword(ys); es.append(low)
    if pw[:len(Bn)] != Bn: fails.append(f't={t}: new low block {pw[:len(Bn)+2]} != B_{(t+1)%L} {Bn}')
    if pw[len(Bn):len(Bn) + G - 1] != [9] * (G - 1): fails.append(f't={t}: no band of 9s after the new block: {pw[len(Bn):len(Bn)+G]}')
    if len(ys) - len(xs) != int(g[t]): fails.append(f't={t}: length change {len(ys)-len(xs)} != g_t {g[t]}')
if not closes: fails.append('walk does not close')
print(f"walk of {L} nodes, closes={closes}, widths {sorted(set(len(b) for b in B))}, e={''.join(map(str, es))}, gap G={G}")
print('PLAIN-REPLAY', 'OK' if not fails else 'FAIL', *fails[:5])
