"""Find and universally check a leading front into the uniform q=6 bulk."""
from itertools import product
from resume_defect_interface import strip_step
from family_search_bulk_periods import bulk_step
import json
A=(3,10,15,8)

def samples(rotation=0,steps=120,width=16):
    left=A[rotation:]+A[:rotation];right=(6,);L=400
    q=left*(L//4)+right*1000;origin=0;seen={};cycles=[]
    for t in range(steps+1):
        b=len(q)
        while b and q[b-1]==right[0]:b-=1
        assert b>=width and b<len(q)-20
        profile=q[b-width:b];key=(t%2,profile)
        if key in seen:
            tt,pos=seen[key];cycles.append({'time':t,'earlier':tt,'period':t-tt,'shift':origin+b-pos,'profile':profile,'uniform':right[0],'phase':t%2})
            if t-tt==6:return cycles[-1]
        seen[key]=(t,origin+b)
        q,left,right,origin=strip_step(q,left,right,origin,t%2)
    return cycles[-1] if cycles else None

def update_suffix(q,uniform,phase,incoming):
    # Known suffix q followed by an infinite uniform nonneutral tail.
    data=q+(uniform,)*3
    c=incoming;lo=[]
    for x in data:v=x+c;lo.append(v%10);c=v//10
    c=int(uniform>=10);hi=[]
    for x in data[::-1]:v=x+c;hi.append(v%10);c=v//10
    hi=hi[::-1]
    # Drop position zero, whose overflow predecessor can be outside the window.
    out=tuple(lo[i]+hi[i-phase]for i in range(phase,len(data)-1))
    newuniform=2*((uniform+int(uniform>=10))%10)
    b=len(out)
    while b and out[b-1]==newuniform:b-=1
    return out[:b],newuniform,b+phase-len(q)

def certify(profile,uniform,phase,period,shift):
    """Branch over every possible incoming carry at every step.

    Keep the full resulting known suffix rather than truncating each step.
    A terminal suffix equal to the original profile gives a renewable barrier;
    positions left of that suffix are irrelevant to the next macro-step.
    """
    states={(profile,uniform,0)}
    maxstates=1
    for t in range(period):
        nxt=set()
        for q,u,d in states:
            for incoming in [0,1]:
                out,nu,move=update_suffix(q,u,(phase+t)%2,incoming)
                nxt.add((out,nu,d+move))
        states=nxt;maxstates=max(maxstates,len(states))
    failures=[]
    for q,u,d in states:
        if u!=uniform or d!=shift or len(q)<len(profile) or q[-len(profile):]!=profile:
            failures.append((q,u,d))
    return {'passed':not failures,'terminal_states':len(states),'max_states':maxstates,'failures':failures[:3]}

def validate_suffix_step(samples=2000):
    import random
    rng=random.Random(8613)
    for _ in range(samples):
        h=rng.randrange(2);u=rng.choice([6,12]);w=rng.randrange(1,13)
        suffix=tuple(rng.randrange(19)for _ in range(w-1))+(rng.choice([a for a in range(19)if a!=u]),)
        prefix=(17 if h else 8,)+tuple(rng.randrange(19)for _ in range(5))
        half=prefix+suffix+(u,)*20
        full=half+half[::-1];digits=[0]*len(full)
        for i in range(len(full)//2):
            digits[i]=max(0,full[i]-9);digits[-1-i]=full[i]-digits[i]
        n=sum(d*10**i for i,d in enumerate(digits));m=n+int(str(n)[::-1])
        nd=tuple(map(int,str(m)[::-1]));actual=tuple(a+b for a,b in zip(nd,nd[::-1]))
        assert len(actual)-len(full)==h
        c=0
        for x in prefix:c=(x+c)//10
        out,nu,shift=update_suffix(suffix,u,h,c)
        start=len(prefix)+h
        assert actual[start:start+len(out)]==out
        assert actual[start+len(out):start+len(out)+2]==(nu,nu)
        assert shift==len(out)+h-len(suffix)
    return samples

if __name__=='__main__':
    certificate=certify((8,),6,0,6,4)
    assert certificate['passed']
    states={((8,),6,0)};trace=[]
    for t in range(7):
        trace.append({'step':t,'states':sorted(states)})
        nxt=set()
        for q,u,d in states:
            for c in [0,1]:
                oq,nu,move=update_suffix(q,u,t%2,c);nxt.add((oq,nu,d+move))
        states=nxt
    result={'status':'passed','initial_suffix':[8],'initial_uniform':6,'initial_phase':'N','period':6,'advance':4,'incoming_carry_histories':64,'certificate':certificate,'independent_integer_checks':validate_suffix_step(),'trace':trace,'finite_lychrel_witness':False}
    print(json.dumps(result,indent=2));open('resume_history_search_front_results.json','w').write(json.dumps(result,indent=2))
