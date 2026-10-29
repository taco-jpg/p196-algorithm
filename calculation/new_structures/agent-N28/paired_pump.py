#!/usr/bin/env python3
"""N28 paired-insertion carry-loop contracts, base 10. No infinite certificate claimed."""
import argparse, json, sys
sys.set_int_max_str_digits(0)
BANDS = ((2,), (6, 12), (18,))
LEFT = (18, 7, 18, 12)

def norm(p):
    d, carries, c = [], [0], 0
    for x in p:
        v=x+c; d.append(v%10); c=v//10; carries.append(c)
    if c: d.append(c)
    return d,carries

def pairs(d):return [d[i]+d[-1-i] for i in range(len(d))]
def insert(p,i,w):return p[:i]+list(w)+p[i:]

def family(k):
    half=list(LEFT); starts=[]
    for w, count in zip(BANDS,k):
        starts.append(len(half));half+=list(w)*count
    return half+[8]+half[::-1], starts

def digits(n): return [int(c) for c in str(n)[::-1]]
def seed(p):
    n=len(p);d=[0]*n
    assert n%2==1 and p[n//2]%2==0
    for i in range(n//2):
        z=p[i]; d[i]=z//2;d[-i-1]=z-z//2
    d[n//2]=p[n//2]//2
    assert d[-1] and pairs(d)==p
    return int(''.join(str(c) for c in d[::-1]))

def emit(w,c):
    out=[]
    for x in w:
        q=x+c;out.append(q%10);c=q//10
    return out,c

def step_contract(p,slots,words):
    D,carries=norm(p);gamma=len(D)-len(p)
    assert p==p[::-1]
    out=pairs(D);new=[]
    for j,(i,w) in enumerate(zip(slots,words)):
        m=len(w);h=len(D)-i;r=len(p)-i
        if not (i+m<=len(p)//2 and h+m<=len(p) and h>=len(p)//2):
            return None,f'CUT_OOB:j{j}'
        lo=p[i:i+m];hi=p[h:h+m];mir=p[r:r+m]
        if lo!=w or mir!=w[::-1]:return None,f'PERIOD_BREAK:j{j}'
        ld,c1=emit(lo,carries[i]);hd,c2=emit(hi,carries[h])
        if c1!=carries[i] or c2!=carries[h]:return None,f'CARRY_LOOP_FAIL:j{j}'
        plus=insert(insert(p,r,mir),i,w)
        if plus!=insert(insert(p,h,hi),i,lo):return None,f'GAMMA_SHIFT_INCOMPATIBLE:j{j}'
        Dplus,_=norm(plus)
        if Dplus!=insert(insert(D,h,hd),i,ld):return None,f'DIGIT_PUMP_FAIL:j{j}'
        v=[ld[x]+hd[-1-x] for x in range(m)]
        if pairs(Dplus)!=insert(insert(out,len(out)-i,v[::-1]),i,v):
            return None,f'PAIR_PUMP_FAIL:j{j}'
        new.append(v)
    anchor=next((i for i in range(min(slots)) if D[i]!=D[-1-i]),None)
    if anchor is None:return None,'NO_FIXED_NONPAL_WITNESS'
    return (out,new,gamma,anchor),'OK'

def expand(p,slots,words,delta):
    q=p[:]
    for i,w,n in reversed(list(zip(slots,words,delta))):
        q=insert(insert(q,len(q)-i,w[::-1]*n),i,w*n)
    return q

def init(k):
    p,starts=family((k,k,k))
    slots=[s+(k//2)*len(w) for s,w in zip(starts,BANDS)]
    return p,slots,[list(w) for w in BANDS]

def survey(k,limit):
    p,slots,words=init(k);trace=[]
    for t in range(limit):
        result,why=step_contract(p,slots,words)
        if result is None:return {'k':k,'edges':t,'failure':why,'trace':trace}
        q,words,g,anchor=result
        if t in (0,20,100,200,400,800,limit-1):
            trace.append({'t':t,'n':len(p),'gamma':g,'bands':words,'anchor':anchor})
        p=q
    return {'k':k,'edges':limit,'failure':'LIMIT','trace':trace}

def replay(k,steps):
    p,slots,words=init(k)
    changes=[(0,0,0),(1,0,0),(0,2,5),(7,11,13),(101,23,59)]
    vals=[seed(family(tuple(k+x for x in delta))[0]) for delta in changes]
    count=0;record=[]
    for t in range(steps+1):
        for i,(value,delta) in enumerate(zip(vals,changes)):
            d=digits(value)
            assert d!=d[::-1],('palindrome',t,i)
            assert pairs(d)==expand(p,slots,words,delta),('independent mismatch',t,i)
            count+=1
        if t==steps:break
        result,why=step_contract(p,slots,words)
        assert result is not None,(t,why)
        p,words,g,anchor=result
        vals=[v+int(str(v)[::-1]) for v in vals]
        if t in (0,20,100,200,steps-1):record.append((t,g,anchor))
    return {'steps':steps,'independent_bigint_pairword_checks':count,'k_min':k,'delta_vectors':changes,'final_pairword_length':len(p),'anchors':record}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--mode',choices=('replay','survey','seed'),default='replay')
    ap.add_argument('--k',type=int,default=240)
    ap.add_argument('--steps',type=int,default=232)
    a=ap.parse_args()
    if a.mode=='seed':
        print(seed(family((a.k,)*3)[0]));return
    if a.mode=='survey':print(json.dumps(survey(a.k,a.steps),indent=2));return
    print(json.dumps(replay(a.k,a.steps),indent=2))
if __name__=='__main__':main()
