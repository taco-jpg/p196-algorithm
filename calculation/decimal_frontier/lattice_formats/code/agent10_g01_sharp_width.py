#!/usr/bin/env python3
"""Symbolic four-state corridor and sharp earliest neutral B width for period-two g=01.

Usage:
 python3 agent10_g01_sharp_width.py --prove 256
 python3 agent10_g01_sharp_width.py --controls  # builds/runs existing bauto3 controls

Proof lives in reports/Agent10G01SharpWidth.md. The --prove option checks
exact integer carry equations for k=1..N; paper induction handles all k.
"""
import argparse, pathlib, subprocess, tempfile
F = (1, 0, 2, 1)
Q = (-2, -3, -1, -2)
ROOT = (0, 2, 1)

def successor(b, st, first=False):
    """Exact spatial cut transition, using proven one-carry invariant."""
    L,H,y=st; l0,l1=L&1,L>>1; h0,h1=H&1,H>>1
    s=l0+l1
    assert st == ROOT or s==1
    for c0 in (0,1):
        x0=b*(1+h0)-(s+c0+y)
        if not (int(first)<=x0<=2*b-2 and (x0+c0)//b==h0):continue
        x1=(x0+l0)%b+(x0+c0)%b
        if not (0<=x1<=2*b-2 and (x1+l1)%b+y==x0):continue
        a,e=(x0+l0)//b,(x1+l1)//b
        if a+e!=1:continue
        for c1 in (0,1):
            if (x1+c1)//b != h1:continue
            yield (a+2*e,c0+2*c1,(x1+c1)%b)

def accepting(b,st):
    L,H,y=st
    return L in (1,2) and (L&1)+(H&1)==1 and (L>>1)+(H>>1)==1 and y==(b-1)*(L>>1)

def layer_odd(b,A): return {(2,h,b-A+F[h]) for h in range(4)}
def layer_even(b,A):return {(1,h,A+Q[h]) for h in range(4)}

def next_layer(b,layer,first=False):
    return set(z for s in layer for z in successor(b,s,first=first))

def verify_parameter(m):
    """Exact formula checks for sharp base b_m = 3*2^(m-1)-4."""
    assert m>=2
    b=3*2**(m-1)-4
    states=next_layer(b,{ROOT},first=True)
    assert not any(accepting(b,s) for s in states)
    if m==2:
        assert next_layer(b,states)=={(2,1,1)}
        return b
    assert states==layer_odd(b,3)
    for t in range(1,m-1):
        A=3*2**(t-1)
        assert b>=4*A-4
        states=next_layer(b,states)
        expected=layer_even(b,2*A) if t%2 else layer_odd(b,2*A)
        assert states==expected,('corridor',m,t,states,expected)
        assert not any(accepting(b,s) for s in states)
    final=next_layer(b,states)
    target={(1,2,0)} if (m-1)%2==0 else {(2,1,b-1)}
    assert final==target,('terminal',m,final,target)
    return b

def verify_large_base_obstruction(m):
    """One base just above the sharp threshold checks terminal obstruction."""
    b=3*2**(m-1)-3
    states=next_layer(b,{ROOT},first=True)
    assert not any(accepting(b,s) for s in states)
    if m>=3:
        assert states==layer_odd(b,3)
        for t in range(1,m-1):
            states=next_layer(b,states)
            A=3*2**t
            assert states == (layer_odd(b,A) if (t+1)%2 else layer_even(b,A))
            assert not any(accepting(b,s) for s in states)
    final=next_layer(b,states)
    assert not any(accepting(b,s) for s in final),('violation',m)

def verify_generic_corridor():
    """Independent finite substitutions exercising both symbolic corridor cases."""
    for A in (3,6,12,24,48,96,192):
        for b in (4*A-4,4*A-3,4*A,6*A,10*A):
            assert next_layer(b,layer_odd(b,A))==layer_even(b,2*A),(A,b,'odd')
            assert next_layer(b,layer_even(b,A))==layer_odd(b,2*A),(A,b,'even')
    print('PASS generic O/E transition controls: A=3..192, b=4A-4,4A-3,4A,6A,10A')

def controls():
    repo=pathlib.Path(__file__).resolve().parents[4]
    bauto=repo/'calculation/decimal_frontier/lattice_formats/code/bauto3.cpp'
    if not bauto.exists():
        print('Repository controls require execution from full repository; no success is claimed.')
        raise SystemExit(2)
    with tempfile.TemporaryDirectory() as td:
        exe=pathlib.Path(td)/'bauto3'
        subprocess.run(['c++','-O3','-std=c++17',str(bauto),'-o',str(exe)],check=True)
        for b,g,need in [(9,'1100011000',('cyclen=4','depth=61')),
                          (13,'1010010000',('depth=55','depth=75'))]:
            out=subprocess.check_output([str(exe),str(b),'10','10','-g',g,'-cap','3000000','-maxscc','10'],text=True)
            for needle in need:
                assert needle in out,(b,needle,out[:1500])
            print('CONTROL PASS base',b,'g',g,', '.join(need))

def main():
    p=argparse.ArgumentParser();p.add_argument('--prove',type=int);p.add_argument('--controls',action='store_true');args=p.parse_args()
    if args.prove:
        verify_generic_corridor()
        for m in range(2,args.prove+1):
            verify_parameter(m)
            verify_large_base_obstruction(m)
        print(f'PASS sharp b_m and first-excluded b_m+1, m=2..{args.prove}; exact carry equations')
    if args.controls:controls()
    if not args.prove and not args.controls:p.print_help()
if __name__=='__main__':main()
