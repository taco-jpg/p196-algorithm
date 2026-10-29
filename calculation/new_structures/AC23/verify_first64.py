#!/usr/bin/env python3
"""1920 literal Python bigint orbits versus the independent C++ bitplanes."""
import re
from pathlib import Path
from collections import Counter
from verify import check
p=Path(__file__).with_name('first64_even.tsv')
lines=p.read_text().splitlines();assert lines[0]=='phase=2 centre=2 start=0 count=64'
assert len(lines)==31
for ui,line in enumerate(lines[1:]):
 assert f'U_RANK_1BASED={ui+1} ' in line
 want={int(a):int(b) for a,b in re.findall(r'(\d+):(\d+)',line)}
 got=Counter(check(code,ui,2,14,100)[0] for code in range(64))
 assert got==want,(ui,got,want)
print('PASS independent Python bigint: 1920 genuine 120-step orbits, all 30 rank-first64 histograms match compiled bitplanes')
