#!/usr/bin/env python3
"""All-length palindrome preimage for folded reverse-add pairwords.

No finite-horizon simulations: all-length claims use a finite product graph.
"""
from collections import deque
from itertools import product

class DFA:
    def __init__(self, arcs, ends):
        self.arcs, self.ends = arcs, ends

def arcs(b, gam, state, p):
    lo_c, upper_out, prev_upper = state
    low = (p + lo_c) % b
    next_low_c = (p + lo_c) // b
    for upper_in in (0, 1):
        if (p + upper_in) // b != upper_out:
            continue
        high = (p + upper_in) % b
        if gam == 0 and low != high:
            continue
        if gam == 1 and low != (1 if prev_upper < 0 else prev_upper):
            continue
        yield (next_low_c, upper_in, high)

def terminal(b, gam, state, middle):
    lo_c, upper_out, prev_upper = state
    if middle is None:
        return lo_c == upper_out
    if middle % 2 or (middle + lo_c) // b != upper_out:
        return False
    mid_digit = (middle + lo_c) % b
    return gam == 0 or mid_digit == (1 if prev_upper < 0 else prev_upper)

def palindrome_preimage_witness(b, source):
    """Return one input fold whose normalized value is palindromic, or None.

    The finite search is exact for all fold lengths; a source DFA is expected
    to admit only valid positive pairwords (first pair nonzero and centre even).
    """
    for gam in (0, 1):
        start = (0, (0, gam, -1))
        queue = deque([start])
        previous = {start: None}
        while queue:
            q, carry = queue.popleft()
            for mid in source.ends.get(q, ()):
                if q == 0 and mid == 0: # reject zero as an integer
                    continue
                if terminal(b, gam, carry, mid):
                    word = []
                    cur = (q, carry)
                    while previous[cur] is not None:
                        old, symbol = previous[cur]
                        word.append(symbol)
                        cur = old
                    word.reverse()
                    return (gam, tuple(word), mid)
            for symbol, q2 in source.arcs.get(q, {}).items():
                if q == 0 and symbol == 0:
                    continue
                for carry2 in arcs(b, gam, carry, symbol):
                    target = (q2, carry2)
                    if target not in previous:
                        previous[target] = ((q, carry), symbol)
                        queue.append(target)
    return None

def normalize(P, b):
    d, carry = [], 0
    for p in P:
        x = p + carry
        d.append(x % b)
        carry = x // b
    if carry:
        d.append(carry)
    return d

def singleton(half, middle):
    return DFA({i: {s:i+1} for i,s in enumerate(half)}, {len(half):{middle}})

def decimal_family_dfa():
    # Full P_m = [2,4,12] + [0]*m + [12,4,2], m >= 1.
    # Fold = [2,4,12,0^k] with odd centre 0 at k>=0;
    # for even length, centre None at k>=1.
    return DFA({0:{2:1}, 1:{4:2}, 2:{12:3}, 3:{0:4}, 4:{0:4}},
               {3:{0}, 4:{None,0}})

def control_pal_family():
    # Positive control, all P_m=[2]+[0]^m+[2] normalize to palindromes.
    return DFA({0:{2:1},1:{0:2},2:{0:2}},{1:{0},2:{None,0}})

def test():
    count = 0
    for b in (2,3,4,10,13):
        for n in range(1,7):
            for h in product(range(2*b-1), repeat=n//2):
                if h and h[0] == 0:
                    continue
                centres = range(0,2*b-1,2) if n%2 else (None,)
                for centre in centres:
                    if not h and centre == 0:
                        continue
                    P = list(h) + ([] if centre is None else [centre]) + list(h[::-1])
                    digits = normalize(P,b)
                    expected = digits == digits[::-1]
                    computed = palindrome_preimage_witness(b,singleton(h,centre)) is not None
                    assert expected == computed, (b,n,h,centre,expected,computed)
                    count += 1
    assert palindrome_preimage_witness(10,decimal_family_dfa()) is None
    assert palindrome_preimage_witness(10,control_pal_family()) is not None
    for m in range(1,21):  # independent oracle spot checks, NOT a horizon proof
        seed = 2*10**(m+5) + 4*10**(m+4) + 6*10**(m+3) + 600
        digs = str(seed)
        nxt = seed + int(digs[::-1])
        expected = 2*10**(m+5) + 5*10**(m+4) + 2*10**(m+3) + 10**3 + 2*10**2 + 4*10 + 2
        assert nxt == expected
        assert str(nxt) != str(nxt)[::-1]
    print("PASS", count, "exhaustive singleton arithmetic checks")
    print("PASS decimal infinite regular family all-length palindrome preimage EMPTY")
    print("PASS positive palindrome-preimage family and decimal seed arithmetic controls")

if __name__ == "__main__":
    test()
