#!/usr/bin/env python3
"""No sound guard on the inner carry can come from residues / width / outer digits.

Claim checked (COMPUTED): for every word w of the forward closure F_k, every inner carry
e in {0,1}, every residue r mod 99 with r = 0 mod 11 (196's orbit is = 0 mod 11 from t = 3),
and every width class l mod 12, there is an actual positive integer n with
    k-column projection of n          = w
    actual inner carry c_{L-k}(n)     = e
    n mod 99                          = r
    (number of digits of n) mod 12    = l .
Hence no rule "features(n) = (w, r, l) => c_{L-k}(n) in G" with G != {0,1} is true of
integers, so any carry guard would need information about the middle digits.

Construction (checked by exact integer arithmetic below, not trusted):
  width L = 2k + M, M >= 4 chosen with L = l (mod 12);
  outer digits: d_{L-1-i} = min(w_i, 9), d_i = w_i - d_{L-1-i}   (so d_{L-1} >= 1);
  adjacent middle columns: d_k = d_{L-1-k} = 5 (column sum 10 -> carry 1) for e = 1,
                           d_k = d_{L-1-k} = 0 (column sum 0  -> carry 0) for e = 0;
  two free consecutive middle digits at positions (k+1, k+2) set n mod 99 (100 = 1 mod 99).
Usage: realize.py F_BITSET K [SAMPLES]     (SAMPLES = 0: all words of F_k)
"""
import random
import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))
from fwdref import project, inner_carry  # noqa: E402


def build(w, e, r, l, k):
    M = 4
    while (2 * k + M) % 12 != l % 12:
        M += 1
    L = 2 * k + M
    d = [0] * L
    for i in range(k):
        hi = min(w[i], 9)
        d[L - 1 - i] = hi
        d[i] = w[i] - hi
    d[k] = d[L - 1 - k] = 5 if e == 1 else 0
    # residue: choose digits at positions k+1, k+2 (both strictly inside the middle since M >= 4)
    p = k + 1
    base = sum(d[i] * 10 ** i for i in range(L)) % 99
    weight = (pow(10, p, 99), pow(10, p + 1, 99))
    for a in range(10):
        for b in range(10):
            if (base + a * weight[0] + b * weight[1]) % 99 == r:
                d[p], d[p + 1] = a, b
                return int("".join(str(x) for x in reversed(d)))
    return None


def words_of(path, k):
    data = open(path, "rb").read()
    for byte_i, byte in enumerate(data):
        if not byte:
            continue
        for bit in range(8):
            if byte >> bit & 1:
                c = byte_i * 8 + bit
                w = []
                for _ in range(k):
                    w.append(c % 19)
                    c //= 19
                yield w


def main():
    path, k = sys.argv[1], int(sys.argv[2])
    samples = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    W = list(words_of(path, k)) if samples == 0 else None
    if W is None:
        rng = random.Random(1960 + k)
        allw = []
        # reservoir sample from the bitset
        for i, w in enumerate(words_of(path, k)):
            if len(allw) < samples:
                allw.append(w)
            else:
                j = rng.randint(0, i)
                if j < samples:
                    allw[j] = w
        W = allw
    checks = 0
    for w in W:
        for e in (0, 1):
            for r in range(0, 99, 11):
                for l in range(12):
                    n = build(w, e, r, l, k)
                    assert n is not None, (w, e, r, l)
                    assert project(n, k) == w, (w, n)
                    assert inner_carry(n, k) == e, (w, e, n)
                    assert n % 99 == r and len(str(n)) % 12 == l, (w, r, l, n)
                    checks += 1
    print(f"k={k}: {len(W)} words x 2 carries x 9 residues x 12 width classes = {checks} realizations, all exact")


if __name__ == "__main__":
    main()
