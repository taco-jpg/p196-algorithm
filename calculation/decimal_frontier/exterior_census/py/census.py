#!/usr/bin/env python3
"""Persistent census driver.  DB = out/db_b{b}.jsonl, one JSON record per (b,g) (latest wins):
 {b,p,G,g,status,states,depth,secs,cap,sec,acc:[e..]}
 status in EXHAUSTED / ACCEPT / CAPPED_states / CAPPED_time.
usage: census.py b p [--cap N] [--sec S] [--gmin x --gmax y] [--limit SECONDS_TOTAL] [--retry]
 Runs bx on the words of lists/all_p{p}.txt (or lists/fc_b{b}_p{p}_G*.txt) that have no decisive record.
 Capped words are retried only if --cap is larger than the cap used before (or --retry)."""
import sys, os, json, subprocess, argparse, glob, re, time
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
ap=argparse.ArgumentParser(); ap.add_argument('b',type=int); ap.add_argument('p',type=int)
ap.add_argument('--cap',type=int,default=3000000); ap.add_argument('--sec',type=float,default=60)
ap.add_argument('--gmin',type=int,default=0); ap.add_argument('--gmax',type=int,default=999)
ap.add_argument('--limit',type=float,default=1e9); ap.add_argument('--retry',action='store_true')
ap.add_argument('--bx',default=os.path.join(ROOT,'bin','bx')); ap.add_argument('--order',default='G')
ap.add_argument('--db',default=None,help='override DB file (for sharded Studio runs)')
ap.add_argument('--shard',default=None,help='i/N: process only words with (index in todo) %% N == i')
ap.add_argument('--seed',default=None,help='read-only DB loaded first (decisive records there are skipped)')
ap.add_argument('--lists',default=None,help='override lists dir')
a=ap.parse_args()
dbf=a.db or os.path.join(ROOT,'out',f'db_b{a.b}.jsonl')
LISTS=a.lists or os.path.join(ROOT,'lists')
import tempfile
db={}
for _f in ([a.seed] if a.seed else [])+[dbf]:
  if os.path.exists(_f):
    _pat='"p": %d,'%a.p
    for l in open(_f):
        if _pat not in l: continue       # cheap skip of other p (DB files can be huge)
        try: r=json.loads(l)
        except: continue
        if r['p']!=a.p: continue
        o=db.get((r['p'],r['g']))
        if o and o['status'] in ('EXHAUSTED','ACCEPT'): continue
        db[(r['p'],r['g'])]=r
words=[]
for f in sorted(glob.glob(os.path.join(LISTS,f'fc_b{a.b}_p{a.p}_G*.txt'))):
    G=int(re.search(r'_G(\d+)\.txt',f)[1])
    if G<a.gmin or G>a.gmax: continue
    for l in open(f):
        w=l.strip()
        if w: words.append((G,w))
words.sort(key=lambda x:(x[0],x[1]))
todo=[]
for G,w in words:
    r=db.get((a.p,w))
    if r and r['status'] in ('EXHAUSTED','ACCEPT'): continue
    if r and not a.retry and r.get('cap',0)>=a.cap and r['status'].startswith('CAPPED_states'): continue
    if r and not a.retry and r['status']=='CAPPED_time' and r.get('sec',0)>=a.sec: continue
    todo.append((G,w))
if a.shard:
    si,sn=map(int,a.shard.split('/')); todo=[x for i,x in enumerate(todo) if i%sn==si]
print(f'p={a.p}: {len(words)} words, {len(todo)} to run'+(f' (shard {a.shard})' if a.shard else ''),flush=True)
T0=time.time(); n=0
# run in chunks so that --limit is honoured and results are saved incrementally
CH=max(1,min(50,int(150e6/a.cap)))   # smaller chunks for big caps so that a timeout loses little
fo=open(dbf,'a')
for i in range(0,len(todo),CH):
    if time.time()-T0>a.limit: print('time limit reached'); break
    chunk=todo[i:i+CH]
    tmp=os.path.join(tempfile.gettempdir(),f'cen_{a.b}_{a.p}_{os.getpid()}.txt'); open(tmp,'w').write('\n'.join(w for G,w in chunk)+'\n')
    r=subprocess.run([a.bx,str(a.b),'-f',tmp,'-cap',str(a.cap),'-sec',str(a.sec)],capture_output=True,text=True)
    for l in r.stdout.splitlines():
        m=re.match(r'RES b=(\d+) p=(\d+) G=(\d+) g=([01]+) (\S+) states=(\d+) depth=(\d+) secs=([\d.]+)',l)
        if not m: continue
        rec=dict(b=int(m[1]),p=int(m[2]),G=int(m[3]),g=m[4],status=m[5],states=int(m[6]),depth=int(m[7]),secs=float(m[8]),cap=a.cap,sec=a.sec,
                 acc=re.findall(r' e=([01]+)@',l))
        mm=re.search(r'wdone=(-?\d+) m=(\d+)',l)
        if mm: rec['wdone']=int(mm[1]); rec['m']=int(mm[2])
        fo.write(json.dumps(rec)+'\n'); fo.flush(); n+=1
        if rec['status']!='EXHAUSTED': print(l,flush=True)
print(f'ran {n} words in {time.time()-T0:.0f}s')
