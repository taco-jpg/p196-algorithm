"""Independent re-verification of every row of the max-delay tables (Python big ints).

usage: python3 verify_tables.py DATA_DIR

For each row (prefix, delay t, seed): recompute orbit(seed, t), check it is a
palindrome, that it starts with the prefix, and that its width matches the table.
This is the check the reported numbers rely on: the search itself (class
reduction, memo, hashing) only proposes witnesses.
"""
import sys, gzip, os

def opener(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path)

bad = 0
for L in (3, 4, 5):
    path = os.path.join(sys.argv[1], f"max_delay_P{L}.tsv")
    if not os.path.exists(path): path += ".gz"
    n = 0
    cache = {}
    for line in opener(path):
        if line.startswith("prefix"): continue
        p, t, s, w = line.rstrip("\n").split("\t")[:4]
        t, s, w = int(t), int(s), int(w)
        key = (s, t)
        if key not in cache:
            x = s
            for _ in range(t): x += int(str(x)[::-1])
            cache[key] = str(x)
        x = cache[key]
        ok = x == x[::-1] and x.startswith(p) and len(x) == w and len(p) == L
        if not ok:
            bad += 1; print("BAD ROW", L, p, t, s, w)
        n += 1
    print(f"P{L}: {n} rows re-verified")
print("ALL ROWS VERIFIED" if bad == 0 else f"{bad} BAD ROWS")
sys.exit(1 if bad else 0)
