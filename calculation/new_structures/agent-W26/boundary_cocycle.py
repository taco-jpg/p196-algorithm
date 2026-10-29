#!/usr/bin/env python3
"""Exact two-scalar 8-step renormalization of W26 five-term decimal orbit family.
Run after run_fast.py (the orbit_110/111/112.bin streams are local scratch files).
"""
import struct, json
from pathlib import Path
from affine_core import derive_template, symbolic_from_template, poly_word_ls
DIR = Path(__file__).resolve().parent
P = 1000000007
E = (0,20,68,116,136)

def readword(f):
    b=f.read(4)
    assert b
    n=struct.unpack('<I',b)[0]
    data=f.read(n)
    assert len(data)==n
    return tuple(data)

def mod_fraction(f):
    return (f.numerator % P)*pow(f.denominator % P,-1,P)%P

def inverse_mod(M):
    n=len(M)
    A=[[(x % P) for x in row]+[int(i==j) for j in range(n)] for i,row in enumerate(M)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if A[i][j]),None)
        assert pivot is not None,('rank deficit',j)
        A[j],A[pivot]=A[pivot],A[j]
        inv=pow(A[j][j],-1,P)
        A[j]=[(v*inv)%P for v in A[j]]
        for i in range(n):
            if i!=j and A[i][j]:
                a=A[i][j]
                A[i]=[(x-a*y)%P for x,y in zip(A[i],A[j])]
    return [row[n:] for row in A]

def multiply(A,B):
    return [[sum(x*y for x,y in zip(row,col))%P for col in zip(*B)] for row in A]

def matvec(A,v):
    return [sum(x*y for x,y in zip(row,v))%P for row in A]

def check():
    streams=[open(DIR/f'orbit_{k}.bin','rb') for k in (110,111,112)]
    rows=[]
    try:
        for t in range(1025):
            tpl=derive_template(*(readword(f) for f in streams),110,1300,1016)
            assert tpl is not None,t
            p=poly_word_ls(symbolic_from_template(tpl))
            assert list(sorted(p))==list(E)
            rows.append(tuple(p[e] for e in E))
    finally:
        for f in streams:f.close()
    for t in range(1017):
        assert rows[t+8][0]==rows[t][0],('constant coefficient',t)
        assert rows[t+8][4]==10000*rows[t][4],('top coefficient',t)
    # Five samples determine a unique matrix modulo P; the sixth rejects it.
    vectors=[[mod_fraction(v) for v in rows[8*j]] for j in range(7)]
    A=[[vectors[j][i] for j in range(5)] for i in range(5)]
    B=[[vectors[j+1][i] for j in range(5)] for i in range(5)]
    M=multiply(B,inverse_mod(A))
    assert all(matvec(M,vectors[j])==vectors[j+1] for j in range(5))
    assert matvec(M,vectors[5])!=vectors[6]
    result={'status':'COMPUTED','t8_pairs_exact':1017,'a0_t_plus_8_equals_a0_t':True,
            'a136_t_plus_8_equals_10000_times_a136_t':True,
            'first_fitted_five_by_five_matrix_failure_macro_index':5,
            'modulus':P,'initial_five_vectors_full_rank_mod_prime':True,
            'not_claimed':'No infinite orbit; no closure for the three middle coefficients'}
    (DIR/'boundary_cocycle_expected.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':check()
