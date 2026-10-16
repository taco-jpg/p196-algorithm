from itertools import product
import json

def words(L):
 if L==1:
  for c in range(2,19,2):yield (c,)
  return
 for a in range(1,19):
  for tail in product(range(19),repeat=L//2-1):
   p=(a,)+tail
   for c in ([None]if L%2==0 else range(0,19,2)):
    yield p+(()if c is None else(c,))+p[::-1]
def val(q):return sum(a*10**i for i,a in enumerate(q))
def main():
 old={};data=[]
 for L in range(1,9):
  now={};fixed=0;cross=[]
  for q in words(L):
   n=val(q)
   if n in now:fixed+=1
   now[n]=q
   if n in old:cross.append((n,old[n],q))
  nonpal=[r for r in cross if str(r[0])!=str(r[0])[::-1]]
  rec={'length':L,'states':len(now),'fixed_width_collisions':fixed,'cross_width_collisions':len(cross),'nonpal_cross_count':len(nonpal),'nonpal_examples':nonpal[:10]}
  print(json.dumps(rec),flush=True);data.append(rec);old=now
 json.dump(data,open('persist_inverse_probe_results.json','w'),indent=2)
if __name__=='__main__':main()
