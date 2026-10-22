"""Independent re-check of walk witnesses with the Python reference forward step.
Usage: python3 verify_walks.py K walks.tsv start_word"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ref import forward_prefix
K = int(sys.argv[1]); start = [int(x) for x in sys.argv[3].split(',')]
assert len(start) == K
n = bad = 0; prefixes = set()
for line in open(sys.argv[2]):
    p, L, tgt, bits = line.rstrip('\n').split('\t')
    s = list(start)
    for b in bits:
        s = forward_prefix(s, int(b))
    tgt = [int(x) for x in tgt.split(',')]
    ok = (s == tgt and len(bits) == int(L) and len(s) == K and all(x <= 9 for x in s)
          and s[0] >= 1 and int(''.join(map(str, s[:4]))) == int(p))
    bad += not ok; n += 1; prefixes.add(int(p))
print(f'K={K}: {n} walks, {len(prefixes)} distinct prefixes, failures={bad}')
