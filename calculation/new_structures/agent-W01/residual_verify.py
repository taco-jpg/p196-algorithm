#!/usr/bin/env python3
"""Independent expected-output auditor, including a wrong-shift negative control."""
import csv
import pathlib
import re
import sys
p=pathlib.Path(sys.argv[1]); primary=(p/'primary.log').read_text()
m=re.search(r'W01_RESIDUAL (.*)',primary)
assert m,'no primary result'
a={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',m.group(1))}
expected={'first':2154,'stable_front_count':17759,'stable_window_count':17177,
 'stable_physical_residual_count':17177,'first_physical_failure':2242,
 'last_physical_failure':2835,'first_front_failure':-1,'last_front_failure':-1,
 'first_window_failure':2242,'last_window_failure':2835}
for k,v in expected.items():assert a.get(k)==v,(k,a.get(k),v)
rows=list(csv.DictReader((p/'residual.csv').open()))
assert len(rows)==259 and rows[0]['t']=='0' and rows[-1]['t']=='20000'
assert rows[-1]['res_lo']=='3459' and rows[-1]['res_hi']=='16999'
assert rows[-1]['res_cnt']=='13018' and rows[-1]['res_l1']=='112648'
assert 'W01_SCATTER_GMP_PASS first=2154 last_failure=2835 stable_windows=3165' in (p/'gmp.log').read_text()
assert 'BAD_GMP_RESIDUAL t=2836 first=7359 old=7379' in (p/'negative.log').read_text()
print('W01_RESIDUAL_VERIFIED 17165 consecutive translating physical-residual windows and 3165 GMP windows')
