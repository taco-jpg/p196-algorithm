"""Backward extension of delay witnesses (predecessor search).

A column-sum class K (length l, pair sums q_0..q_{h-1}, middle digit) is the set of
l-digit seeds y with y_i + y_{l-1-i} = q_i; all members share step(y) and hence the
same palindrome hits.  If some member y of K is itself an iterate, y = step(z), then
every member of z's class reaches the same palindromes one step later.

depth(K) = 0 if no member of K has a predecessor, else 1 + max depth(class(z)).
For a witness seed with delay T, a class chain of depth d gives delay T + d.

Members y that can have a predecessor must satisfy (necessary, used only to prune):
  same-length predecessor: y_i - y_{l-1-i} in {0, +-1, +-9} for every pair;
  shorter predecessor (y has a leading carry 1): y_i - y_{l-2-i} in {0,+-1,+-9}.
Predecessors of a concrete y are then solved exactly by a two-ended carry search
(validated against brute force in --selftest).

usage: python3 extend.py --selftest
       python3 extend.py max_delay_P4.tsv MIN MAX OUT.tsv [--budget SECONDS_PER_SEED]
"""
import sys, time
from functools import lru_cache

DIFF = {0, 1, -1, 9, -9}

def digits(x):  # little-endian
    return [int(c) for c in str(x)[::-1]]

def from_digits(d):
    return int("".join(map(str, d[::-1])))

def pred_classes(x):
    """All column-sum classes (l, q tuple, mid) of positive z with z + rev(z) = x."""
    e = digits(x); D = len(e); out = []
    for l in (D, D - 1):
        if l < 1: continue
        if l == D - 1 and e[D - 1] != 1: continue
        top_carry = 1 if l == D - 1 else 0
        h = l // 2
        # state: pair index i, carry into low position i (cl), required carry OUT of high position j=l-1-i (ch)
        def rec(i, cl, ch, qs):
            if i == h:
                if l % 2 == 0:
                    # carry into position h from low side must equal carry out of position h-1, which is
                    # the carry into high position h; that was guessed as ch's source: ch here = required
                    # carry out of position h-1 ... (see below)
                    if cl == ch: out.append((l, tuple(qs), 0))
                else:
                    m = h
                    for dm in range(10):
                        s = 2 * dm + cl
                        if s % 10 == e[m] and s // 10 == ch: out.append((l, tuple(qs), dm))
                return
            j = l - 1 - i
            for cj in (0, 1):  # carry into high position j
                q = e[j] + 10 * ch - cj
                if q < 0 or q > 18: continue
                if i == 0 and q < 1: continue  # leading digit of z is >= 1
                s = q + cl
                if s % 10 != e[i]: continue
                ncl = s // 10
                if j == i + 1 and l % 2 == 0 and False: pass
                # next: low position i+1 with carry ncl; high position j-1 must produce carry-out cj
                rec(i + 1, ncl, cj, qs + [q])
        if l == 1:
            for d0 in range(1, 10):
                if 2 * d0 == x: out.append((1, (), d0))
            continue
        rec(0, 0, top_carry, [])
    # fix-up for even l: when i == h the low carry cl is the carry into position h,
    # and ch is the carry into position h (= required carry out of position h-1 seen from above).
    return out

def class_members_with_possible_pred(l, q, mid):
    """Members y (digit lists) of class (l,q,mid) that pass a necessary image condition."""
    h = l // 2
    res = []
    # same-length pattern: pairs independent
    opts = []
    for i in range(h):
        o = []
        for a in range(10):
            b = q[i] - a  # a = y_i (low), b = y_{l-1-i} (high)
            if 0 <= b <= 9 and (a - b) in DIFF and not (i == 0 and b == 0):
                o.append((a, b))
        opts.append(o)
    def rec_same(i, cur):
        if i == h:
            y = [0] * l
            for k, (a, b) in enumerate(cur): y[k] = a; y[l - 1 - k] = b
            if l % 2: y[h] = mid
            res.append(tuple(y)); return
        for ab in opts[i]: rec_same(i + 1, cur + [ab])
    rec_same(0, [])
    # leading-carry pattern: y_{l-1} = 1, and y_k - y_{l-2-k} in DIFF for k < (l-1)/2
    if q and q[0] >= 1 and q[0] - 1 <= 9:
        y = [None] * l
        y[l - 1] = 1; y[0] = q[0] - 1
        if l % 2: y[h] = mid
        def rec_lead(y):
            # find first unset position from the top side
            try: j = max(k for k in range(l) if y[k] is None)
            except ValueError:
                ok = all((y[k] - y[l - 2 - k]) in DIFF for k in range(l - 1))
                if ok: res.append(tuple(y))
                return
            # j is a high position l-1-i paired (in class) with low i = l-1-j
            i = l - 1 - j
            # constraint for shorter predecessor pairs position j with l-2-j
            partner = l - 2 - j
            cands = range(10)
            if 0 <= partner < l and y[partner] is not None:
                cands = [v for v in range(10) if (y[partner] - v) in DIFF]
            for v in cands:
                w = q[i] - v if i < h else None
                if i < h:
                    if not (0 <= w <= 9): continue
                    if y[i] is not None and y[i] != w: continue
                y2 = list(y); y2[j] = v
                if i < h: y2[i] = w
                # early prune on pairs fully set
                bad = False
                for k in range(l - 1):
                    if y2[k] is not None and y2[l - 2 - k] is not None and (y2[k] - y2[l - 2 - k]) not in DIFF:
                        bad = True; break
                if not bad: rec_lead(y2)
        if l >= 2: rec_lead(y)
    return set(res)

def smallest_member(l, q, mid):
    y = [0] * l; h = l // 2
    for i in range(h):
        hi = max(q[i] - 9, 0)
        if i == 0: hi = max(hi, 1)
        y[l - 1 - i] = hi; y[i] = q[i] - hi
    if l % 2: y[h] = mid
    if l == 1: y[0] = mid
    return from_digits(y)

def class_of(x):
    d = digits(x); l = len(d); h = l // 2
    return (l, tuple(d[i] + d[l - 1 - i] for i in range(h)), d[h] if l % 2 else 0)

def extend_class(cls, deadline, memo):
    """Return (depth, deepest class) of the predecessor tree above class cls."""
    if cls in memo: return memo[cls]
    if time.time() > deadline: return (0, cls)
    best = (0, cls)
    for y in class_members_with_possible_pred(*cls):
        for pc in pred_classes(from_digits(y)):
            d, c = extend_class(pc, deadline, memo)
            if d + 1 > best[0]: best = (d + 1, c)
    memo[cls] = best
    return best

def selftest():
    import random
    rev = lambda z: int(str(z)[::-1])
    # 1. pred_classes against brute force for all x < 200000
    image = {}
    for z in range(1, 200000):
        image.setdefault(z + rev(z), set()).add(class_of(z))
    bad = 0
    for x in range(1, 200000):
        got = set(pred_classes(x))
        want = image.get(x, set())
        if got != want:
            bad += 1
            if bad < 5: print("pred mismatch", x, got, want)
    print("pred_classes mismatches below 200000:", bad)
    # 2. member filter keeps every member that is actually an image (exhaustive, l <= 5)
    images = set(image.keys())
    miss = 0
    for z in range(10, 100000):
        if z in images:
            cls = class_of(z)
            if tuple(digits(z)) not in class_members_with_possible_pred(*cls):
                miss += 1
                if miss < 5: print("filter dropped image member", z, cls)
    print("filter dropped image members below 100000:", miss)

if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        selftest(); sys.exit()
    tsv, lo, hi, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    budget = float(sys.argv[sys.argv.index("--budget") + 1]) if "--budget" in sys.argv else 20.0
    rows = []
    for line in open(tsv):
        if line.startswith("prefix"): continue
        p, t, s = line.split("\t")[:3]
        if lo <= int(t) <= hi: rows.append((p, int(t), int(s)))
    with open(out, "w") as fo:
        fo.write("prefix\told_delay\tnew_delay\tnew_seed\tseconds\n")
        for p, t, s in rows:
            t0 = time.time(); memo = {}
            d, c = extend_class(class_of(s), t0 + budget, memo)
            if d > 0:
                ns = smallest_member(*c)
                fo.write(f"{p}\t{t}\t{t + d}\t{ns}\t{time.time() - t0:.1f}\n"); fo.flush()
