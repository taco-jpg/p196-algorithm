#!/usr/bin/env python3
"""Paper-sound signed-boundary-rewrite certificate FORMAT for 2 neutral bands.

Input blocks O0 x^g O1 u^h O2 v^h O3 y^g O4 are the exact
reverse+add output of a phase, produced by agent3_T5_two_band.py.
An elementary move preserves the represented digit word for all sufficiently
large g,h. This is not a verified Lean theorem or a decimal certificate.
"""
from dataclasses import dataclass
from random import Random
from two_band import Phase, image_blocks, valid_phase, word, val, rand_phase

@dataclass(frozen=True)
class Move:
    run: int  # 0 outer left, 1 inner left, 2 inner right, 3 outer right
    side: str # L = fixed block before run, R = fixed block after run
    delta: int # >0 extract from fixed block, <0 absorb from band


def weave(blocks,runs,offsets,g,h):
    exps=[g+offsets[0],h+offsets[1],h+offsets[2],g+offsets[3]]
    assert min(exps)>=0
    w=list(blocks[0])
    for i in range(4):
        w.extend([runs[i]]*exps[i]);w.extend(blocks[i+1])
    return tuple(w)


def apply_moves(blocks,runs,moves):
    """(new_blocks, shifts_per_run, minimum initial (g,h)) or None.

    The two copies of g/h are allowed different offsets transiently.
    A valid phase edge requires final equal shifts for paired runs.
    """
    blocks=[list(z) for z in blocks]
    off=[0]*4;minoff=[0]*4
    for move in moves:
        i,side,n=move.run,move.side,move.delta
        if i not in (0,1,2,3) or side not in ('L','R') or not isinstance(n,int):return None
        blk=i+(side=='R')
        c=runs[i]
        if n>0:
            if n>len(blocks[blk]):return None
            if side=='L':
                if blocks[blk][-n:]!=[c]*n:return None
                del blocks[blk][-n:]
            else:
                if blocks[blk][:n]!=[c]*n:return None
                del blocks[blk][:n]
        elif n<0:
            if side=='L':blocks[blk].extend([c]*(-n))
            else:blocks[blk]=[c]*(-n)+blocks[blk]
        off[i]+=n
        minoff[i]=min(minoff[i],off[i])
    return tuple(tuple(z) for z in blocks),tuple(off),(-min(minoff[0],minoff[3]),-min(minoff[1],minoff[2]))


def signed_edge(b,p,q,moves):
    if not (valid_phase(b,p) and valid_phase(b,q)):return None
    O,R,_=image_blocks(b,p)
    if R!=(q.x,q.u,q.v,q.y):return None
    outcome=apply_moves(O,R,moves)
    if outcome is None:return None
    blocks,off,need=outcome
    if blocks!=(q.A,q.B,q.M,q.D,q.E):return None
    if off[0]!=off[3] or off[1]!=off[2]:return None
    return off[0],off[1],need[0],need[1]


def signed_cycleOK(b,phases,move_traces):
    """Returns a valid seed (g0,h0) or None. Sound by induction ON PAPER.

    Requires nonnegative total gains in each band and at least one positive.
    Nonpalindromicity is witnessed by fixed mirrored-block mismatch or a nonempty unequal repeated-digit band.
    """
    p=len(phases)
    if p==0 or len(move_traces)!=p:return None
    if not all(valid_phase(b,q) for q in phases):return None
    edges=[]
    for j,q in enumerate(phases):
        out=signed_edge(b,q,phases[(j+1)%p],move_traces[j])
        if out is None:return None
        edges.append(out)
    total_g=sum(e[0] for e in edges)
    total_h=sum(e[1] for e in edges)
    if min(total_g,total_h)<0 or total_g+total_h==0:return None
    g0=h0=0;sg=sh=0
    for q,(dg,dh,ng,nh) in zip(phases,edges):
        g0=max(g0,ng-sg);h0=max(h0,nh-sh)
        fixed_mismatch=(q.A!=q.E[::-1] or q.B!=q.D[::-1] or q.M!=q.M[::-1])
        if not fixed_mismatch:
            if q.x!=q.y:g0=max(g0,1-sg)
            elif q.u!=q.v:h0=max(h0,1-sh)
            else:return None # permanently palindromic phase
        sg+=dg;sh+=dh
    return g0,h0


def selftest(n=12000):
    rng=Random(0x1962ABCD)
    test=0
    for t in range(n):
        b=(2,3,4,8,10,11,17,26,32)[t%9]
        p=rand_phase(rng,b)
        O,R,_=image_blocks(b,p)
        moves=[]
        for _ in range(rng.randrange(0,12)):
            i=rng.randrange(4);side=rng.choice(('L','R'))
            z=rng.randint(-3,3)
            move=Move(i,side,z)
            tentative=apply_moves(O,R,moves+[move])
            if tentative is not None:moves.append(move)
        result=apply_moves(O,R,moves)
        assert result is not None
        newblocks,off,(ng,nh)=result
        for g,h in ((ng,nh),(ng+1,nh+7),(ng+11,nh+2)):
            raw=weave(O,R,(0,0,0,0),g,h)
            transformed=weave(newblocks,R,off,g,h)
            assert raw==transformed,(b,p,moves,g,h)
        test+=1
    print('signed_rewrite_word_equalities',test*3,'PASS',test,'random traces')
    # A concrete nondegenerate decimal 2-band step with delta_g=delta_h=+1.
    p=Phase((9,),(0,9,7),(7,0,2,7,2),(2,7,9),(0,),5,4,2,7)
    q=Phase((1,),(0,6),(9,7,4,8),(0,6),(9,),0,9,9,0)
    moves=(Move(0,'L',1),Move(1,'L',1),Move(2,'L',1),Move(3,'L',1))
    assert signed_edge(10,p,q,moves)==(1,1,0,0)
    for g,h in ((0,0),(1,2),(10,3),(100,110)):
        w=word(p,g,h)
        assert val(10,word(q,g+1,h+1))==val(10,w)+val(10,w[::-1])
    print('base10_two_band_nontrivial_step_delta_1_1 PASS')
    # A nontrivial, positive-gain four-phase known-base control in base two.
    p0=Phase((1,0),(1,1),(1,1,0,1),(0,0),(0,0),1,0,1,0)
    p1=Phase((1,1),(0,0),(1,0,0,0),(1,1),(0,1),0,1,0,1)
    p2=Phase((1,0),(1,1),(1,0,1),(0,0),(0,0),1,0,1,0)
    p3=Phase((1,1),(0,0),(0,1,0),(1,1),(0,1),0,1,0,1)
    moves01=()
    moves12=(Move(0,'L',1),Move(0,'R',-1),Move(1,'L',1),Move(2,'L',1))
    moves23=()
    moves30=(Move(0,'L',1),Move(0,'R',-1),Move(1,'L',1),Move(1,'R',-1))
    ps=(p0,p1,p2,p3); ms=(moves01,moves12,moves23,moves30)
    assert [signed_edge(2,ps[j],ps[(j+1)%4],ms[j])[:2] for j in range(4)] == [(0,0),(0,1),(0,0),(0,0)]
    seed=signed_cycleOK(2,ps,ms)
    assert seed is not None
    g,h=(max(seed[0],2),max(seed[1],2))
    x=val(2,word(ps[0],g,h))
    for j in range(1000):
        p=ps[j%4]
        assert x==val(2,word(p,g,h)),(j,g,h)
        w=word(p,g,h)
        assert w!=w[::-1]
        independent_rev=int(bin(x)[2:][::-1],2)
        assert independent_rev==val(2,w[::-1])
        x+=independent_rev
        if j%4==1:h+=1
    print('base2_signed_cycle_4_phases_positive_inner_gain_1 seed',seed,'1000_steps_integer_replay_PASS')
    print('NO_DECIMAL_LYCHREL_CERTIFICATE_CLAIMED')

if __name__=='__main__':selftest()
