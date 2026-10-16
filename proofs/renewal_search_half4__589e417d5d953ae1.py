"""Exhaustive safe-renewal search at wall widths eight and nine."""
from renewal_search_scan import *
import time

def run():
    started=time.monotonic();counts=Counter();events=[];hist=Counter();chains=[]
    terminal=Counter();maximum_exit_step=0
    for W in m.wall_words(4):
        if len(W)<8:continue
        for C in range(1,len(W)+1):
            q=m.difference_word(W,C)
            if not m.word_valid(q):continue
            counts['valid']+=1
            if m.digit_monotone(m.wall_step(W)[2],C):continue
            counts['failure']+=1
            Q,d=qstep(q);z=balance(Q)
            if d==d[::-1]:counts['pal']+=1;continue
            if not z:continue
            counts['safe_rebalance']+=1
            ev=dict(W=W,C=C,newW=z[0],newC=z[1]);events.append(ev)
            oldC=C;chain=[]
            for t in range(120):
                Q,d=qstep(q);z=balance(Q)
                if d==d[::-1]:stop='pal';break
                if z is None:stop='unbalanced';break
                if z[1]>oldC:chain.append((t+1,oldC,z[1],z[0]))
                oldC=z[1];q=Q
            else:stop='capped'
            terminal[stop]+=1;hist[len(chain)]+=1
            maximum_exit_step=max(maximum_exit_step,t+1)
            if len(chain)>2:chains.append(dict(seed=ev,chain=chain,steps=t,stop=stop))
    out=dict(counts=counts,events=events,chain_histogram=hist,chains=chains,
             terminal=terminal,maximum_exit_step=maximum_exit_step,
             seconds=time.monotonic()-started)
    Path(__file__).with_name('renewal_search_half4_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='events'},indent=2))
if __name__=='__main__':run()
