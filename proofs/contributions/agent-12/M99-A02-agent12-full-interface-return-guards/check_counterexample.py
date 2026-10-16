from __future__ import annotations

PREFIX = (4, 4, 0)
ALPHA = (0, 0, 0, 0, 1, 1, 1)
REQUIRED = {0: 0, 1: 0, 3: 0, 5: 0, 6: 1}
OVERFLOWS = (0, 0, 1, 0, 1, 0, 1)

def normalize(word, incoming=0):
    retained, carries = [], [incoming]
    for x in word:
        carry, digit = divmod(x + carries[-1], 10)
        retained.append(digit)
        carries.append(carry)
    return tuple(retained), tuple(carries)

def pair(word):
    return tuple(x + y for x, y in zip(word, word[::-1]))

def prefix_step(prefix, high_incoming):
    lo, _ = normalize(prefix)
    hi, carries = normalize(prefix[::-1], high_incoming)
    overflow = carries[-1]
    if overflow:
        out = (lo[0] + 1, lo[1] + hi[2], lo[2] + hi[1])
    else:
        out = (lo[0] + hi[2], lo[1] + hi[1], lo[2] + hi[0])
    return out, overflow

def core_map(h):
    states, controls = [h], []
    for t in range(7):
        digits, carries = normalize(h, ALPHA[t])
        c = carries[-1]
        controls.append(c)
        if t in REQUIRED and c != REQUIRED[t]:
            return False, t, states, controls
        if not OVERFLOWS[t]:
            h = pair(digits)
        else:
            h = list(pair(digits + (0,)))
            edge = c if t == 2 else 5 + c if t == 4 else 0
            h[0] += edge
            h[-1] += edge
            h = tuple(h)
        assert h == h[::-1] and all(0 <= x <= 18 for x in h)
        states.append(h)
    return True, None, states, controls

def realize(q):
    d = [0] * len(q)
    for i in range(len(q) // 2):
        d[i] = max(0, q[i] - 9)
        d[-1-i] = q[i] - d[i]
    if len(q) % 2:
        assert q[len(q)//2] % 2 == 0
        d[len(q)//2] = q[len(q)//2] // 2
    return int(''.join(map(str, d[::-1])))

h = (1, 3, 16, 3, 1)
q = PREFIX + h + PREFIX[::-1]
seed = realize(q)

ok1, fail1, states1, controls1 = core_map(h)
h2 = states1[-1]
ok2, fail2, states2, controls2 = core_map(h2)

assert ok1 and controls1 == [0, 0, 0, 0, 0, 0, 1]
assert h2 == (3, 5, 9, 15, 15, 9, 5, 3)
assert not ok2 and fail2 == 5
assert controls2 == [0, 0, 1, 0, 0, 1]

n = seed
values = [n]
for _ in range(14):
    n += int(str(n)[::-1])
    values.append(n)

assert values[:8] == [
    44013800000, 44014631044, 88028272088, 176055554176,
    847511104847, 1595912220595, 7546134416546, 14002278733003
]
assert not any(str(v) == str(v)[::-1] for v in values[:8])

print("PASS: first guard satisfied")
print("PASS: first returned middle:", h2)
print("PASS: second guard fails at t=5 with controls:", controls2)
print("PASS: exact seed:", seed)
print("PASS: first 14 iterates contain no palindrome")
