#!/usr/bin/env python3
"""Write 9-wire tables for kink6 / wirebudget: a wire carrying a fixed carry stream is a period-1 'lattice' of 9s
whose upward carry is the stream bit and whose downward carry is its complement (c + d = 1 keeps every 9)."""
def tbl(fn, clock, s):
    p = len(clock); assert len(s) == p
    with open(fn, 'w') as f:
        f.write(f'{p} 1\n' + ' '.join(clock) + '\n')
        for t in range(p):
            f.write('9\n' + s[t] + '\n' + str(1 - int(s[t])) + '\n')
# known decimal neutral-band exteriors (repo census EXTERIOR.md; re-derived by up4): p11 and the three p12 streams (p22 = p11 twice)
tbl('wire_p11.tbl', '00001110001', '00111010011')
for i, s in enumerate(['101101010010', '001010110101', '010100101011']):
    tbl(f'wire_p12_{i}.tbl', '0001' * 3, s)
# positive control: clock 0001 and the carry stream of the known 16-step centre loop C_B=(8,4,17,17,4,8)
tbl('wire_ctrl.tbl', '1000' * 4, '1000100001110111')
print('wrote wire_p11.tbl wire_p12_0..2.tbl wire_ctrl.tbl')
