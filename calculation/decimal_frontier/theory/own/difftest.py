import sys, random, subprocess
sys.path.insert(0,'/home/claude/research/w2_theory'); sys.path.insert(0,'/home/claude/research/w2_theory/scripts')
import lib, mirror as m
from parse_bw import parse_bw
line=[l for l in open('/home/claude/research/w2_theory/out2/bauto_p11_w.txt') if 'ACCEPT' in l][0]
b,p,g,e,Bs=parse_bw(line)
random.seed(1)
def randpal():
    L=random.randint(1,9); h=(L+1)//2
    half=[random.randint(0,2*b-2) for _ in range(h)]
    if L%2==1: half[-1]=random.randrange(0,2*b-1,2)
    if L>=2 and half[0]==b-1: half[0]=random.choice([x for x in range(2*b-1) if x!=b-1])
    return half+half[:L//2][::-1]
tot=0; surv=0; bad=0
for t in range(p):
    B=Bs[t]; et=m.e1(b,B); nb,e1,gm,u=lib.Bstep(b,B)
    Cs=[randpal() for _ in range(40000)]
    inp=''.join(f"{len(C)} "+' '.join(map(str,C))+"\n" for C in Cs)
    out=subprocess.run(['./cfg',str(b),str(et),str(gm),'9','img'],input=inp,capture_output=True,text=True).stdout.split('\n')
    for C,o in zip(Cs,out):
        r=m.step(b,B,C)   # canonical max trim from mirror; step returns None if hyp fails
        tot+=1
        if r is None or len(r[3])==0: exp='DEAD'
        else: exp=f"{len(r[3])} "+' '.join(map(str,r[3]))
        if exp!='DEAD': surv+=1
        if exp!=o.strip():
            bad+=1
            if bad<5: print("MISMATCH",t,C,exp,o)
print("tested",tot,"survived one step",surv,"mismatches",bad)
