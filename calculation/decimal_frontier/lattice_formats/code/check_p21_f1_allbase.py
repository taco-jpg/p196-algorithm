#!/usr/bin/env python3
"""Independent Boolean ring-DP over actual pair coefficients 1..2b-2.
No use of residue formula, affine coefficients, or analytic carry reconstruction.
"""
G='001001010101001010101'

def ring_starts(b):
    n=2*b-1
    # Bit q in reachable[x] indicates the finite-state walk began at q.
    reachable=[0]*n
    for q in range(1,b):reachable[q]=1<<q
    for gg in G:
        output=[0]*n
        for q,oldstarts in enumerate(reachable):
            if not oldstarts:continue
            for higher_carry in (0,1):
                if (q+higher_carry)//b!=int(gg):continue
                val=(q%b)+(1 if gg=='1' else (q+higher_carry)%b)
                if 1<=val<=2*b-2:output[val]|=oldstarts
        reachable=output
    return [q for q in range(1,n) if (reachable[q]>>q)&1]

def verify():
    for b in range(2,589):
        found=ring_starts(b)
        expected=0 if b<4 else(2 if b==586 else 1)
        assert len(found)==expected,(b,found,expected)
    controls={2:[],3:[],4:[1],9:[2],10:[3],13:[4],16:[5],17:[5],
              585:[216],586:[216,217],587:[217],588:[217],1171:[433,434],10000:[3709]}
    for b,expected in controls.items():
        assert ring_starts(b)==expected,(b,ring_starts(b),expected)
    print('INDEPENDENT DP PASS: exhaustive 2b-state closed-walk test for b=2..588')
    print('PASS boundary and large-base controls b=585,586,587,588,1171,10000')
    print('No numerical cutoff is used in the analytic all-b proof; only residue representatives')

if __name__=='__main__':verify()
