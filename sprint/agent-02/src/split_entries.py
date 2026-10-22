#!/usr/bin/env python3
"""Split a gen_code4 Entries module with several entries into one module per entry
(each entry check needs about 5 GB of kernel memory at width 8).
Usage: split_entries.py PATH/A124<TAG>Entries.lean   -> writes ...Entries.lean, ...Entries1.lean, ..."""
import re
import sys
path = sys.argv[1]
src = open(path).read()
m = re.search(r'(?:/-- [^\n]*-/\n)?def entries00 : List \(List Nat × Nat\) :=\n  \[(.*)\]\n', src)
items = re.findall(r'\(\[[0-9,]+\], [0-9]+\)', m.group(1))
head = src[:m.start()]
k = re.search(r'entryOK (\d+)', src).group(1)
tail = src[src.index('\nend ', m.end()):]
for i, it in enumerate(items):
    body = (f"/-- Prefix entry (digits, rank bound) number {i}. -/\n"
            f"def entries{i:02d} : List (List Nat × Nat) :=\n  [{it}]\n\n"
            f"theorem entries{i:02d}_ok : entries{i:02d}.all (entryOK {k} (R ranks)) = true := by\n  decide +kernel\n\n"
            f"theorem entries{i:02d}_le : entries{i:02d}.all (fun e => Nat.ble (e.2 + 1) 100) = true := by\n  decide +kernel\n")
    out = path if i == 0 else path.replace('Entries.lean', f'Entries{i}.lean')
    open(out, 'w').write(head + body + tail)
print(len(items), 'entries')
