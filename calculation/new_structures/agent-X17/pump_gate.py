#!/usr/bin/env python3
"""Exact 256-mask branch of the t=108 folded-pump control by the t=107 carry gate."""
import csv,sys
sys.set_int_max_str_digits(0)
from pathlib import Path
from pump_fold import initial,fold,st

def main(out,charge_file,n=2001):
    with open(charge_file,newline='') as f:
        charge={int(r['mask']):int(r['differential_carry']) for r in csv.DictReader(f)}
    assert len(charge)==256
    rows=[]
    j=61
    for m in range(256):
        a,b=initial(n,m),initial(n+16,m)
        for t in range(108):a,b=st(a),st(b)
        small,ca=fold(a); large,cb=fold(b)
        assert ca==cb and len(large)==len(small)+8
        assert small==large[:j]+large[j+8:], (n,m)
        band=''.join(''.join(z) for z in large[j:j+8])
        assert band==('09'*8 if charge[m]==0 else '00'*8), (n,m,charge[m],band)
        rows.append((m,charge[m],band))
    assert sum(z[1] for z in rows)==170
    with open(out,'w',newline='') as f:
        w=csv.writer(f);w.writerow(['mask','incoming_differential_carry','eight_folded_pair_band_at_t108']);w.writerows(rows)
    print('PASS: 256 real decimal replays; t108 folded-pump block 09^8 for 86 safe, 00^8 for 170 charged')
if __name__=='__main__':main(sys.argv[1],sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 2001)
