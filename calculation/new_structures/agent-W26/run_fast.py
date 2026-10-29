#!/usr/bin/env python3
"""COMPUTED: 1024 universal decimal reverse-add edges with five-term Q[X] identities."""
from affine_core import *
import struct, subprocess, json, hashlib
from pathlib import Path
DIR=Path(__file__).resolve().parent

def make_data(kmin,steps):
    exe=DIR/'orbit_coeff'
    subprocess.run(['g++','-O3','-std=c++17',str(DIR/'orbit_coeff.cpp'),'-o',str(exe)],check=True)
    paths=[]
    for k in range(kmin,kmin+3):
        i=DIR/f'input_{k}.dat'
        o=DIR/f'orbit_{k}.bin'
        i.write_bytes(bytes(source(k)))
        subprocess.run([str(exe),str(i),str(o),str(steps)],check=True)
        paths.append(o)
    return paths

def readone(f):
    raw=f.read(4)
    if not raw:return None
    n=struct.unpack('<I',raw)[0]
    x=f.read(n)
    assert len(x)==n
    return tuple(x)

def check(kmin=110,blen=1300,vshift=1016,steps=1024):
    paths=make_data(kmin,steps)
    files=[open(p,'rb') for p in paths]
    prev=None;counts={};nverified=0;checkpoints=[];hashx=hashlib.sha256()
    try:
        for t in range(steps+1):
            ps=[readone(f) for f in files]
            assert all(p is not None for p in ps)
            tpl=derive_template(*ps,kmin,blen,vshift)
            if tpl is None:
                raise AssertionError(('template mismatch',t))
            q=symbolic_from_template(tpl)
            poly=poly_word_ls(q)
            rev=poly_word_ls(reverse_segments(q))
            if prev is None:
                assert poly==original_source_poly(kmin),('incorrect source family',t)
            else:
                assert poly==prev,('nonclosing exact polynomial identity',t)
            assert sorted(poly)==[0,20,68,116,136]
            assert all(0<=z<=18 for block in tpl for z in block)
            low=q[0][0][0]
            high=q[-1][0][-1]
            assert high>0 and low!=high,('no uniform nonpalindrome witness',t)
            counts[str((low,high))]=counts.get(str((low,high)),0)+1
            prev=poly_add(poly,rev)
            nverified+=1
            hashx.update(str([str(poly[e]) for e in sorted(poly)]).encode())
            if t in (0,1,2,8,64,128,256,512,768,1024,2048):
                w=expand(q,2)
                assert eval_digit_word(w)==poly_value_at(poly,2)
                checkpoints.append({'t':t,'canonical_length':len(w),'low':low,'high':high,
                    'sha256_coeffs':hashlib.sha256(str(poly).encode()).hexdigest()})
    finally:
        for f in files:f.close()
    assert nverified==steps+1
    report={'status':'COMPUTED','base':10,'k_min':kmin+1,'universal_steps':steps,
        'all_q_exact_edges':steps,'polynomial_support':[0,20,68,116,136],
        'strict_outer_digit_witness_counts':counts,
        'source_coef_root':list(source(kmin+1)[:8]),
        'checkpoints':checkpoints,'all_symbolic_polynomial_coeffs_sha256':hashx.hexdigest(),
        'not_claimed':'No infinite certificate, no temporal return, no Lean compilation'}
    (DIR/'expected.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__':
    import sys
    kmin=int(sys.argv[1]) if len(sys.argv)>1 else 110
    steps=int(sys.argv[2]) if len(sys.argv)>2 else 1024
    blen=int(sys.argv[3]) if len(sys.argv)>3 else 1300
    vshift=int(sys.argv[4]) if len(sys.argv)>4 else 1016
    check(kmin,blen,vshift,steps)
