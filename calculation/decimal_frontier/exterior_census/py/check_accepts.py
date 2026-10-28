#!/usr/bin/env python3
"""Classify every ACCEPT / accepted-e stream in one or more DB files.
usage: check_accepts.py DB.jsonl [DB2.jsonl ...]
A pair (g,e) is KNOWN if its cyclic primitive root equals (up to rotation) the p11 stream (g=00001110001,e=00111010011)
or the p12 stream (g=000100010001,e=101101010010).  Anything else is printed as NEW (-> verify_ext.py, then center search; STOP and report)."""
import sys,json
def root(g,e):
    p=len(g); pairs=[g[i]+e[i] for i in range(p)]
    for d in range(1,p+1):
        if p%d==0 and pairs[:d]*(p//d)==pairs: pairs=pairs[:d]; break
    d=len(pairs); return min(tuple(pairs[i:]+pairs[:i]) for i in range(d))
KNOWN={root('00001110001','00111010011'):'p11',root('000100010001','101101010010'):'p12'}
new=0; tot=0
for f in sys.argv[1:]:
    for l in open(f):
        try: r=json.loads(l)
        except: continue
        for e in r.get('acc',[]):
            tot+=1; k=root(r['g'],e)
            if k in KNOWN: print(f"{r['status']:9s} p={r['p']} g={r['g']} e={e}: repetition/rotation of {KNOWN[k]} (root length {len(k)})")
            else: new+=1; print(f"NEW !!!   p={r['p']} g={r['g']} e={e} status={r['status']} root_len={len(k)}")
print(f'{tot} accepted streams, {new} NEW')
