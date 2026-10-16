"""Exact spatial target for the uniform16/14/10/2/4/8 bulk.

The target represents alternating N,O steps, grouped into length-two
segments.  Arbitrary-width backward reachability is complete only when its
queue exhausts. In particular no larger capped result implies exclusion.
"""
import json
from pathlib import Path
from continuation_theory_graph import half
from continuation_theory_multigrowth import backwards

def target(segments):
    assert segments%3==0
    return tuple([8,5,2]*(segments//3)),tuple([3,1,0]*(segments//3)),tuple([3,1,0]*(segments//3))

def verify_selfloop(segments):
    ls,lc,rc=target(segments)
    right=ls[0]
    outputs=[]
    for j in range(segments):
        next_left=ls[(j+1)%segments]
        expected=(next_left,next_left,lc[j],rc[j])
        assert expected in half(10,'E',ls[j],right,lc[j],rc[j],2)
        outputs.append(next_left)
        right=next_left
    assert right==ls[0]
    assert tuple(outputs[-1:]+outputs[:-1])==ls
    return True

if __name__=='__main__':
    rows=[]
    for segments in (3,12,36):
        row=backwards(10,[2]*segments,target(segments),maxstates=20000,seconds=3)
        row['target_selfloop_direct']=verify_selfloop(segments)
        row['target_digit_pair']=[8,8]
        rows.append(row)
        print(json.dumps(row),flush=True)
        Path('persist_block_uniform16_backward_results.json').write_text(json.dumps(rows,indent=2))
