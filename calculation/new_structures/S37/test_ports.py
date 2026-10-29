"""Independent randomized oracle for the two-cut single-step insertion lemma."""
import random
from pump_window import norm,one_cut,normfrom,folded
R=random.Random(111)

def ins(p,a,w,r):
 n=len(p)
 return p[:a]+w*r+p[a:n-a]+w[::-1]*r+p[n-a:]

def run():
 valid=0;both=0;tries=40000
 for _ in range(tries):
  n=R.randrange(14,50);h=[R.randrange(19) for _ in range(n//2)]
  p=h+h[::-1] if n%2==0 else h+[2*R.randrange(10)]+h[::-1]
  a=R.randrange(1,n//2-3);b=R.randrange(a+1,n//2)
  v=[R.randrange(19) for _ in range(R.randrange(1,4))]
  w=[R.randrange(19) for _ in range(R.randrange(1,4))]
  f,_,_,_=folded(p)
  x=one_cut([(p,*folded(p)[1:])],a,v)
  y=one_cut([(p,*folded(p)[1:])],b,w)
  if x['ok']:
   valid+=1
   vp=x['terminal_word']
   for r in (1,2,3):
    got=folded(ins(p,a,v,r))[0]
    predicted=ins(f,a,vp,r)
    assert got==predicted,('one-cut',n,a,r,p,v)
  if x['ok'] and y['ok']:
   both+=1
   for r,s in ((1,1),(3,2),(2,4)):
    pp=ins(ins(p,b,w,s),a,v,r)
    got=folded(pp)[0]
    pred=ins(ins(f,b,y['terminal_word'],s),a,x['terminal_word'],r)
    assert got==pred,('two-cut',n,a,b,r,s,p,v,w)
 print('RANDOM TESTS',tries,'valid single cuts',valid,'valid two cuts',both)

if __name__=='__main__':run()
