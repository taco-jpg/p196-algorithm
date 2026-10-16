"""Independent exact ancestry-depth DP for the thirteen-prefix claim.

H(P) = max{t : exists A > 0, T^t(A) = P},  T(n) = n + int(str(n)[::-1]).
Because T(n) > n, processing n in increasing order finalises depth[n]
before n is used.  Usage: python3 -I dp_depth.py [limit]
"""
import sys, time

BOUNDS = {"10": 1, "20": 2, "32": 2, "40": 3, "41": 3, "60": 3, "64": 3,
          "76": 3, "80": 4, "81": 4, "82": 4, "83": 4, "65": 6}


def main(limit):
    t0 = time.time()
    depth = bytearray(limit)
    best = {k: (-1, None) for k in BOUNDS}
    count = {k: 0 for k in BOUNDS}
    hist = {k: {} for k in BOUNDS}
    violations = []
    for n in range(1, limit):
        s = str(n)
        r = s[::-1]
        if s == r and len(s) >= 2:
            ab = s[:2]
            if ab in BOUNDS:
                d = depth[n]
                count[ab] += 1
                hist[ab][d] = hist[ab].get(d, 0) + 1
                if d > best[ab][0]:
                    best[ab] = (d, n)
                if d > BOUNDS[ab]:
                    violations.append((ab, n, d))
        v = n + int(r)
        if v < limit:
            dn = depth[n] + 1
            if dn > depth[v]:
                depth[v] = dn
    dt = time.time() - t0
    print(f"limit={limit}  elapsed={dt:.1f}s")
    print("prefix bound  #palindromes  maxDepth  firstArgmax  depthHistogram")
    for ab in BOUNDS:
        d, n = best[ab]
        h = dict(sorted(hist[ab].items()))
        print(f"  {ab}    {BOUNDS[ab]}   {count[ab]:>10}   {d:>6}   {n}   {h}")
    print("total palindromes in the 13 classes:", sum(count.values()))
    print("violations (depth > bound):", violations[:20], "count", len(violations))
    print("global max depth of any n < limit:", max(depth))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 7)
