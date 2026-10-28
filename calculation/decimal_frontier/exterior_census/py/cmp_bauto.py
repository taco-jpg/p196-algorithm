import sys,subprocess,re,time
sys.path.insert(0,'/home/claude/research/w5_exterior/py')
from necklaces import necklaces
b=int(sys.argv[1]); p=int(sys.argv[2])
words=necklaces(p)
open('/tmp/claude-0/cmp_words_%d.txt'%p,'w').write('\n'.join(words)+'\n')
t=time.time()
r1=subprocess.run(['bin/bauto2_w1',str(b),str(p),str(p),'-cap','3000000'],capture_output=True,text=True,timeout=600)
t1=time.time()-t; t=time.time()
r2=subprocess.run(['bin/bx',str(b),'-f','/tmp/claude-0/cmp_words_%d.txt'%p,'-cap','3000000'],capture_output=True,text=True,timeout=600)
t2=time.time()-t
def canon(w): return min(w[i:]+w[:i] for i in range(len(w)))
def canonpair(g,e): return min((g[i:]+g[:i],e[i:]+e[:i]) for i in range(len(g)))
A={}
for l in r1.stdout.splitlines():
    m=re.match(r'WORD b=\d+ p=\d+ g=([01]+) states=(\d+)',l)
    if m: A.setdefault(canon(m[1]),{})['states']=int(m[2])
    m=re.match(r'ACCEPT b=\d+ p=\d+ g=([01]+) e=([01]+)',l)
    if m: A.setdefault(canon(m[1]),{}).setdefault('acc',set()).add(canonpair(m[1],m[2]))
    m=re.match(r'STATECAP b=\d+ p=\d+ g=([01]+) states=(\d+)',l)
    if m: A.setdefault(canon(m[1]),{})['cap']=True
Bd={}
for l in r2.stdout.splitlines():
    m=re.match(r'RES b=\d+ p=\d+ G=\d+ g=([01]+) (\S+) states=(\d+)',l)
    if m:
        d=Bd.setdefault(canon(m[1]),{}); d['states']=int(m[3]); d['status']=m[2]; d['m']=int(re.search(r' m=(\d+)',l)[1])
        d['acc']=set(canonpair(m[1],e) for e in re.findall(r' e=([01]+)@',l))
bad=0; nacc=0
for w in map(canon,words):
    a=A.get(w); bb=Bd.get(w)
    if a is None or bb is None: print('MISSING',w,a,bb); bad+=1; continue
    if a.get('cap') or bb['status'].startswith('CAPPED'): 
        print('cap',w,a,bb['status']); continue
    if (bb['m']==1 and a['states']!=bb['states']) or a.get('acc',set())!=bb['acc']:
        print('MISMATCH',w,a,bb); bad+=1
    nacc+=len(bb['acc'])
print(f'base {b} p={p}: {len(words)} words, mismatches {bad}, accepts compared {nacc}; time bauto2 {t1:.1f}s bx {t2:.1f}s')
