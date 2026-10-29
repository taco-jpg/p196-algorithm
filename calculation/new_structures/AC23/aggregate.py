#!/usr/bin/env python3
"""Audit exact AC23 histogram totals and clock/prefix survivors (no estimates)."""
from pathlib import Path
from collections import Counter
import re
ROOT=Path(__file__).resolve().parent
SPACE=19**5
hist=Counter();rankseen={};prefix=clock=0
files=sorted(ROOT.glob('full_u??.tsv'))
if not files: files=[ROOT/'hist_all.tsv']
for f in files:
 lines=f.read_text().splitlines()
 for line in lines[1:]:
  if not line.startswith('U_RANK_1BASED='):continue
  v=dict(re.findall(r'([A-Z_1-9]+)=([^\s]+)',line))
  rank=int(v['U_RANK_1BASED']);assert rank not in rankseen,(rank,f)
  h={int(a):int(b)for a,b in re.findall(r'(-?\d+):(\d+)',line)}
  assert sum(h.values())==int(v['CLOCK'])-int(v['PREFIX'])==(19**5-int(v['PREFIX'])),(f,h)
  rankseen[rank]=h;prefix+=int(v['PREFIX']);clock+=int(v['CLOCK']);hist.update(h)
print('ranks',sorted(rankseen),'complete',len(rankseen))
print('checked',len(rankseen)*SPACE,'clock',clock,'prefix_survivors',prefix)
print('aggregate_hist',dict(sorted(hist.items())))
for rank,h in sorted(rankseen.items()):
 print('rank',rank,'max_first_mismatch',max(h),'at_cut_offset',max(h)-160,'distribution',dict(sorted(h.items())))
if len(rankseen)==30:
 assert clock==30*SPACE==74282970
 assert sum(hist.values())==clock-prefix
 assert prefix==0
 print('EXHAUSTED ALL-30 PHASE2 J5 NECESSARY W9 ENDPOINT GATE; NOT AN ALL-TIME LYCHREL CERTIFICATE')
