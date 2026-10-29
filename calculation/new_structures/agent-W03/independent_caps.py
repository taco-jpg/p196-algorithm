#!/usr/bin/env python3
# Independent real Python integers, exhaustive insertion position comparison.
import csv,random,sys
sys.set_int_max_str_digits(0)
def groups(n):
 s=str(n);return [int(s[max(i-2,0):i]) for i in range(len(s),0,-2)]
def inserted(a,b):
 x=groups(a);y=groups(b)
 return any(y[:i]==x[:i] and y[i:i+1]==[99] and y[i+1:]==x[i:] for i in range(len(x)+1))
def replay(head,tail,q,first0,maxrun0,firstheal0):
 a=int(f'{head:02d}'+'99'*q+f'{tail:02d}')
 b=int(f'{head:02d}'+'99'*(q+1)+f'{tail:02d}')
 first=None;run=0;maxrun=0;firstheal=-1
 for t in range(first0+81):
  active=inserted(a,b)
  if first is None and not active:first=t
  if first is not None:
   if t>first and active:
    run+=1;maxrun=max(maxrun,run)
    if firstheal<0:firstheal=t
   else:run=0
  assert str(a)!=str(a)[::-1] and str(b)!=str(b)[::-1],(head,tail,q,t)
  a+=int(str(a)[::-1]);b+=int(str(b)[::-1])
 assert (first,maxrun,firstheal)==(first0,maxrun0,firstheal0),(head,tail,q,first,maxrun,firstheal)
def main(path):
 rows=list(csv.DictReader(open(path)))
 assert len(rows)==2701,len(rows)
 groups_by={mode:[x for x in rows if x['mode']==mode] for mode in ['suffix','prefix','focused']}
 assert [len(groups_by[m]) for m in ['suffix','prefix','focused']]==[2250,90,361]
 ranked={m:max(int(x['maxrun']) for x in xs) for m,xs in groups_by.items()}
 assert ranked=={'suffix':7,'prefix':10,'focused':10},ranked
 assert all(x['palfree']=='1' for x in rows if x['head']=='88' and x['tail']=='26' and x['Q']=='200')
 champs=[next(x for x in rows if x['mode']==m and x['head']==h and x['tail']==tail and x['Q']==q) for m,h,tail,q in [('suffix','12','26','200'),('prefix','88','26','200')]]
 rng=random.Random(62881)
 chosen=champs+rng.sample(groups_by['suffix'],6)+rng.sample(groups_by['prefix'],6)+rng.sample(groups_by['focused'],6)
 for x in chosen:replay(*map(int,[x['head'],x['tail'],x['Q'],x['first'],x['maxrun'],x['firstheal']]))
 try:replay(88,26,200,681,11,686)
 except AssertionError:pass
 else:raise AssertionError('mutation control failed')
 print('PASS',len(rows),'cap settings; 20 independent bigint paired-orbit controls; mutation rejected')
if __name__=='__main__':main(sys.argv[1])
