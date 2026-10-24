"""Parse the combined three-digit exclusion table of RESULTS.md into three_digit_marks.json.
usage: python3 parse_marks.py RESULTS.md OUT.json
Marks: C two-digit core, K single-prefix kernels, S 33 classes, F forward-invariant list,
x Agent117RemainingCycles (method provably fails), . open."""
import re, json, sys
lines = open(sys.argv[1]).read().split('\n')
start = [i for i, l in enumerate(lines) if l.startswith('## Excluded palindrome prefixes')][0]
marks = {}
for l in lines[start:start + 120]:
    m = re.match(r'\| \*\*(\d\d)\*\* \|(.*)\|\s*$', l)
    if m:
        for d, c in enumerate(c.strip() for c in m.group(2).split('|')):
            marks[m.group(1) + str(d)] = c
assert len(marks) == 900, len(marks)
json.dump(marks, open(sys.argv[2], 'w'))
from collections import Counter
print(Counter(marks.values()))
