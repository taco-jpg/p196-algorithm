"""Exact all-period obstruction to the alternating outer9/18 branch.

This excludes only that prescribed overflow clock and outer branch.
It is not a decimal reverse-and-add termination theorem.
"""
from pathlib import Path
import json

def run():
    # At an N phase with q0=9, no overflow forces the carry from column1
    # to column0 to be0. Thus Q=q1 is0..9. N sends q0 to18. At the next O
    # phase the low incoming carry to column1 is1, and the previous high
    # digit is8+cO. These facts give the equations enumerated below.
    edges={q:set() for q in range(10)}
    cases=[]
    for Q in range(10):
        for cn in (0,1):
            if (Q+cn)//10:continue
            R=2*Q+cn
            for co in (0,1):
                if R<9 and co!=0 or R>9 and co!=1:continue
                nextQ=(R+1)%10+8+co
                cases.append(dict(Q=Q,N_inner_carry=cn,R=R,
                                  O_high_carry=co,nextQ=nextQ))
                if nextQ<=9:edges[Q].add(nextQ)
    assert {q:sorted(v) for q,v in edges.items() if v}=={0:[9],4:[8,9]}
    ranks={q:0 for q,v in edges.items() if not v}
    ranks.update({0:1,4:1})
    assert len(ranks)==10
    assert all(ranks[v]<ranks[q] for q,vs in edges.items() for v in vs)
    result=dict(status='exact_all_period_outer9_18_obstruction',
                prescribed_clock='N,O repeated',
                prescribed_outer_coefficients=[9,18],cases=cases,
                continuing_edges={q:sorted(v) for q,v in edges.items()},
                strictly_decreasing_rank=ranks,
                proof='Every continuing N/O pair follows one listed edge and strictly decreases a nonnegative rank. Therefore no infinite9/18 alternating exterior exists, regardless of temporal period or interior length.',
                scope='Only the9/18 branch of the indefinitely alternating N/O clock.',
                decimal_lychrel_existence_proved=False)
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','continuing_edges','strictly_decreasing_rank']}))

if __name__=='__main__':run()
