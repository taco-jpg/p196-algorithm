import sys, re, glob, os, math
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
import mkjobs as MK
ROOT=os.path.expanduser('~/p196_run/r13a')
status={}
for d in glob.glob(ROOT+'/logs/*'):
    if not os.path.isdir(d): continue
    for f in glob.glob(d+'/i*.log'):
        for line in open(f):
            if not line.startswith('BANDRESULT L '): continue
            m=re.match(r'BANDRESULT L b=(\d+) clock=(\d+) V=([\d,]+) T=(\d+) epochs=(\d+)(?: Tprime=\d+)? tau=(\d+) R=(\d+) .* : rots=(\S+) status=(\w+)',line)
            if not m: continue
            b,clk,V,T,M,tau,R,rots,st=m.groups()
            if clk=='1000' and int(M)==1 and R=='12' and tau=='0': status[V]=st
PY=sys.executable; SJ=ROOT+'/seamjob.py'
out=[]
E='5,18,4,8,1,15,4,0,5'
for B in MK.parse('1000',8):
    if B['T']>12 or status.get(B['V'])!='PASS': continue
    for mul in (2,3,4):
        out.append(f"{PY} {SJ} --clock 1000 --E {E} --ET 12 --V {B['V']} --VT {B['T']} --Trot {B['Trot']} --Lmax 6 --timeout 60 --budget 300 --Nmul {mul}")
open(sys.argv[1],'w').write('\n'.join(out)+'\n')
print(len(out),'jobs')
