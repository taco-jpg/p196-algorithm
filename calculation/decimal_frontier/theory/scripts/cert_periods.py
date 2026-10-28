#!/usr/bin/env python3
"""Periods of the B- and C-sequences of all known certificates (mirror selftest certs + PR #356 base 20), streams E,G and lengths."""
import sys; sys.path.insert(0,'/home/claude/research/w2_theory')
import lib, mirror as m
certs=list(m._lean_certs())
certs.append((20,lib.parse_lean_certs('/home/claude/r/lean/P196/Agent116Base20Certificate/Certificate.lean')))
for b,es in certs:
    p=len(es); Bs=[tuple(e[0]) for e in es]; Cs=[tuple(e[1]) for e in es]
    G=''.join(str(m.gam(b,e[0],e[1])) for e in es); E=''.join(str(m.e1(b,e[0])) for e in es)
    per=lambda X:[d for d in range(1,p+1) if p%d==0 and all(X[i]==X[(i+d)%p] for i in range(p))][0]
    print(f"b={b:2d} p={p:2d} E={E} G={G} sumgam={G.count('1')} B-period={per(Bs)} C-period={per(Cs)} |B|={[len(x) for x in Bs]} |C|={[len(x) for x in Cs]}")
