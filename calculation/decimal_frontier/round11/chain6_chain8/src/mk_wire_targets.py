#!/usr/bin/env python3
"""r11f control: target windows (winbits index, all cyclic starts incl. wrapped) of the 9-wire interface of a stream:
c = stream bits, d = complement, r = 9 at overflow slots with c = 1, 0 otherwise.  usage: mk_wire_targets.py B CLOCK w STREAM out.txt"""
import sys
B = int(sys.argv[1]); pat = sys.argv[2]; w = int(sys.argv[3]); s = sys.argv[4]; out = sys.argv[5]
T = len(s); L0 = len(pat); assert T % L0 == 0
ov = [pat[t % L0] == "1" for t in range(T)]
res = set()
for sh in range(0, T, L0):            # all clock shifts of the stream (closed target set)
    st = s[sh:] + s[:sh]
    for s0 in range(T):
        c = d = rv = 0; j = 0
        for i in range(w):
            t = (s0 + i) % T; b = int(st[t])
            c |= b << i; d |= (1 - b) << i
            if ov[t]: rv += (B - 1) * b * B ** j; j += 1
        res.add((s0 % L0, c | (d << w) | (rv << (2 * w))))
with open(out, "w") as f:
    for ph, idx in sorted(res): f.write(f"{ph} {idx}\n")
print("distinct (phase, window) pairs", len(res))
