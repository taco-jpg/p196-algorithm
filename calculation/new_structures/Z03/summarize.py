#!/usr/bin/env python3
"""Aggregate the nine exact J5 shards and enforce the recorded census totals."""
from pathlib import Path
import argparse, re

NJ = 19**5
RANGES = [(0,1_000_000),(1_000_000,2_000_000),(2_000_000,NJ)]
UWORDS = {3:(2,9,16),15:(9,8,10),27:(16,2,9)}
EXPECTED = {
  3: {-25:28027,-24:58546,-23:1158088,-22:986488,-21:114538,-20:112384,-19:8213,-18:8228,-16:752,-15:602,-14:146,-13:83,-11:4},
  15:{-25:28099,-24:58715,-23:1160301,-22:983932,-21:113881,-20:112985,-19:8257,-18:8167,-16:1042,-15:589,-14:84,-13:35,-12:12},
  27:{-25:27532,-24:58318,-23:1163142,-22:981732,-21:113477,-20:113686,-19:8046,-18:8766,-16:793,-15:388,-14:103,-13:110,-12:6},
}
def parse(path):
    lines=path.read_text().splitlines()
    meta=next((x for x in lines if x.startswith('U_RANK=')),None)
    histline=next((x for x in lines if x.startswith('endpoint_first_mismatch_by_offset_from_W9_cut:') or x.startswith('endpoint_mismatch_by_local_i:')),None)
    if meta is None or histline is None: raise ValueError(f'missing result rows in {path}')
    rank=int(re.search(r'U_RANK=(\d+)',meta).group(1))
    U=tuple(map(int,re.search(r'U=(\d+),(\d+),(\d+)',meta).groups()))
    total=int(re.search(r'total=(\d+)',meta).group(1))
    endpoint=int(re.search(r'endpoint_W9=(\d+)',meta).group(1))
    strict=int(re.search(r'strict_W9=(\d+)',meta).group(1))
    rr=re.search(r'range=\[(\d+),(\d+)\)',meta)
    if rr: start,end=map(int,rr.groups())
    else:
        # Compatibility with the first locally run build, whose shard bounds were encoded in filenames.
        m=re.search(r'u(\d+)_(0_1m|1m_2m|2m_end)\.tsv$',path.name)
        if not m: raise ValueError(f'cannot recover shard bounds from {path.name}')
        start,end={'0_1m':(0,1_000_000),'1m_2m':(1_000_000,2_000_000),'2m_end':(2_000_000,NJ)}[m.group(2)]
    raw=histline.split(':',1)[1].strip().split(); hist={}
    local=histline.startswith('endpoint_mismatch_by_local_i:')
    for tok in raw:
        i,n=map(int,tok.split(':'))
        off=i-108 if local else i
        if n: hist[off]=hist.get(off,0)+n
    return rank,U,start,end,total,endpoint,strict,hist

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input-dir',default='/tmp/z03');ap.add_argument('--output',default='calculation/new_structures/Z03/census_summary.tsv');args=ap.parse_args()
    root=Path(args.input_dir); allrows=[]
    for rank in UWORDS:
        shard=[]
        for name in (f'u{rank}_0_1m.tsv',f'u{rank}_1m_2m.tsv',f'u{rank}_2m_end.tsv'):
            row=parse(root/name);shard.append(row)
        bounds=[(r[2],r[3]) for r in shard]
        assert bounds==RANGES,(rank,bounds)
        assert all(r[0]==rank and r[1]==UWORDS[rank] for r in shard)
        assert sum(r[4] for r in shard)==NJ
        assert sum(r[5] for r in shard)==0 and sum(r[6] for r in shard)==0
        agg={}
        for r in shard:
            for off,n in r[7].items():agg[off]=agg.get(off,0)+n
        assert agg==EXPECTED[rank],(rank,agg,EXPECTED[rank])
        assert sum(agg.values())==NJ
        assert all(-25<=off<=-11 for off in agg)
        for off,n in sorted(agg.items()):allrows.append((rank,','.join(map(str,UWORDS[rank])),NJ,0,0,off,n))
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w') as f:
        f.write('# EXHAUSTED-NONE; exact phase-0 J5 endpoint-W9 census; histogram is first mismatch offset from W9|J cut.\n')
        f.write('U_RANK\tU\tJ_WORDS\tENDPOINT_W9\tSTRICT_W9\tFIRST_MISMATCH_OFFSET\tCOUNT\n')
        for row in allrows:f.write('\t'.join(map(str,row))+'\n')
    print(f'PASS: 9 contiguous shards cover {3*NJ:,} (U,J) pairs; endpoint W9 restorations=0; strict-W9 survivors=0; summary={out}')
if __name__=='__main__':main()
