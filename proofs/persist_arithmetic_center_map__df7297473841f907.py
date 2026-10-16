import json,time,sys
from pathlib import Path
pairs=next(x for x in json.load(open('persist_block_neutral_timechange_results.json')) if x['periods']==[1,1,4,5])['accepted'][0]['path']
A=''.join(str(a) for a,b in pairs);B=''.join(str(b) for a,b in pairs)[::-1]
def center_map(c,m=20):
 left=A+'9'*m;right='0'*m+B
 outleft=A+'9'*(m+2);outright='0'*(m+2)+B
 lo,ro=int(left)*10**(c+len(right)),int(right)
 scale=10**len(right)
 head,tail=int(outleft),int(outright);tailmod=10**len(outright)
 blockmod=10**c
 rows=[];sgn={-1:0,0:0,1:0};sameclock=0
 expected=[1,1,0,0,0,1,0,0,0,0,1]
 for C in range(blockmod):
  n=lo+C*scale+ro
  clock=[]
  for _ in range(11):
   old=n;n+=int(str(n)[::-1]);clock.append(int(len(str(n))>len(str(old))))
  if clock==expected:sameclock+=1
  if n%tailmod!=tail:continue
  v=n//tailmod
  if v//blockmod!=head:continue
  Cp=v%blockmod
  rows.append((C,Cp));sgn[(Cp>C)-(Cp<C)]+=1
 return dict(c=c,m=m,valid=len(rows),sameclock=sameclock,sign=sgn,rows=rows)
if __name__=='__main__':
 cs=list(map(int,sys.argv[1:])) or [0,1,2,3,4]
 result=[]
 for c in cs:
  t=time.time();r=center_map(c);r['seconds']=time.time()-t;result.append(r)
  print(json.dumps({k:v for k,v in r.items() if k!='rows'}),flush=True)
 Path('persist_arithmetic_center_map_results.json').write_text(json.dumps(result,indent=2))
