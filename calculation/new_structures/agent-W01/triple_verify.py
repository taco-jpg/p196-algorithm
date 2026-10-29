#!/usr/bin/env python3
"""Independent exhaustive exact trace audit of a three-body Lychrel scattering shield.
The two input CSV files are regenerated from distinct executable seeds;
this checker does not perform the decimal reverse-add transition itself.
"""
import csv
import sys
from pathlib import Path

if len(sys.argv)!=3:raise SystemExit('usage: triple_verify.py triple.csv baseline_pair.csv')

def read(path):
    with open(path,newline='') as f:return {int(r['t']):r for r in csv.DictReader(f)}

T=read(sys.argv[1]);P=read(sys.argv[2]);
assert len(T)==18501 and min(T)==1500 and max(T)==20000,len(T)
assert len(P)==18251 and min(P)==1750 and max(P)==20000,len(P)

def u16(s):
    assert len(s)==122
    return [int(s[i:i+2],16)-36 for i in range(0,122,2)]

alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
def u64(s):
    assert len(s)==61
    return [alphabet.index(c)-18 for c in s]

expected=read(Path(__file__).with_name('triple_expected.csv'))
for t in expected:
    a,b=T[t],expected[t]
    for key in ('front','back','count','shield_front','shield_gap'):
        assert a[key]==b[key],(t,key,a[key],b[key])

first=next((t,int(r['front'])) for t,r in T.items() if int(r['front'])>=0)
assert first==(4354,9014),first
front_bad=[t for t in range(4354,19913) if int(T[t+88]['front'])!=int(T[t]['front'])-20]
assert front_bad==[4365,4368,4369],front_bad
front_checks=19912-4370+1
for t in range(4370,20001):
    assert int(T[t]['front'])==int(P[t]['front'])+2000,t

# Two-ended actual signed *digits* of the three-body residual form a moving
# period-88 particle, not merely an aligned folded coefficient sum.
tile_rows=0
for t in range(5098,19913):
    a,b=T[t],T[t+88]
    assert a['low']==b['low'] and a['high']==b['high'],t
    tile_rows+=1
assert tile_rows==14815

# Third pulse cancels the no-X YZ interaction on the entire 61-pair outgoing
# tile. Equivalently the three-body residual is exactly the negative of YZ.
# The separate XY daughter appears 2000 cells further outward; its negative
# matches the triple daughter for [-20,+35], with a *nonzero* 5-cell kink.
shielded=0; anti_checks=0; right_kink=0;min_gap=10**9
for t in range(5098,20001):
    triple=T[t];pair=P[t]
    g=int(triple['shield_gap']);min_gap=min(g,min_gap)
    assert g>=41,('screen-failure',t,g)
    aL,aH=u16(triple['low']),u16(triple['high'])
    bL,bH=u64(pair['low']),u64(pair['high'])
    for i in range(56):
        assert aL[i]==-bL[i] and aH[i]==-bH[i],(t,i-20)
        anti_checks+=2
    tail=sum(aL[i]!=-bL[i] for i in range(56,61))+sum(aH[i]!=-bH[i] for i in range(56,61))
    assert tail>0,('lost-kink',t)
    right_kink+=tail
    shielded+=1
assert int(T[5097]['shield_gap'])==40
assert shielded==14903 and min_gap==41
assert anti_checks==1669136,anti_checks

# The first physical uncancelled digit need not move monotonically in each
# step, but finite 176-step block minima grow strictly throughout this run.
mins=[]
for st in range(5098,20001,176):
    mins.append(min(int(T[t]['shield_gap']) for t in range(st,min(st+176,20001))))
assert len(mins)==85 and mins[0]==41 and mins[-1]==1004
assert min(b-a for a,b in zip(mins,mins[1:]))==4
assert all(b>a for a,b in zip(mins,mins[1:]))
# Wrong translation +1999 instead of +2000 fails at every stable checked row.
assert int(T[6000]['front'])!=int(P[6000]['front'])+1999
print('W01_TRIPLE_SCREEN_PASS real_decimal_orbits=8 steps=20000 '
      f'birth=4354@9014 front_88_checks={front_checks} '
      f'two_ended_tile_88_rows={tile_rows} tile_digit_checks={tile_rows*122} '
      f'full_physical_shield_rows={shielded} anti_XY_digit_checks={anti_checks} '
      f'nonzero_kink_mismatches={right_kink} '
      f'gap_min={min_gap} gap_end={T[20000]["shield_gap"]} '
      'all_176_block_minima_increase=1')
