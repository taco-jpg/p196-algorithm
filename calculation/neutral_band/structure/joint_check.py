import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import neutral_band_search as N
def joint(b,B,C,maxsteps=400):
    r=N.run(b,B,C,maxsteps=maxsteps,maxlen=2000)
    if r[0]=='cycle':
        es=r[1]; return ('cycle', len(es), N.cycleOK(b,es,es[0][0],es[0][1]), N.is_cert(b,es), sum(N.gam(b,e[0],e[1]) for e in es), sum(e[4]+e[5] for e in es), es)
    return r
if __name__=="__main__":
    # base 26: B from the automaton (Q), several C survivors
    Q=[24,28,19,36,30,15,19,12]
    for C in ([27,27],[29,6,29],[32,20,20,32],[25,27,27,25],[25,29,6,29,25]):
        r=joint(26,Q,C); print(26,C,r[:6] if r[0]=='cycle' else r)
