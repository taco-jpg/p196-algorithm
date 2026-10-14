"""Finite certificate for equality in the existing outer-digit growth bound."""
import json
from itertools import product

def potential(a):
 if a in (4,6,7,8,10,11,12,14):return 1
 if a in (9,13,15,16,17):return 2
 return 3 if a==18 else 0

def move(q,inside):
 c=0;lo=[]
 for a in q:lo.append((a+c)%10);c=(a+c)//10
 hi=[0]*3;c=inside
 for i in (2,1,0):hi[i]=(q[i]+c)%10;c=(q[i]+c)//10
 h=c
 out=(lo[0]+1,lo[1]+hi[0],lo[2]+hi[1]) if h else tuple(a+b for a,b in zip(lo,hi))
 return out,h

def main():
 states=[(a,b,c) for a in range(1,19) for b,c in product(range(19),repeat=2)]
 ids={q:i for i,q in enumerate(states)};zero=[];total=0
 for i,q in enumerate(states):
  for inside in (0,1):
   r,h=move(q,inside);j=ids[r];slack=1-2*h+potential(q[0])-potential(r[0]);total+=1
   assert slack>=0
   if slack==0:zero.append((i,j))
 live=set(range(len(states)));rounds=[]
 while True:
  outgoing={u for u,v in zero if u in live and v in live};incoming={v for u,v in zero if u in live and v in live}
  new=live&outgoing&incoming;rounds.append(len(new))
  if new==live:break
  live=new
 expected=[(8,16,16),(17,13,14),(8,12,9),(17,5,0),(8,13,5),(17,6,11),(8,14,8),(17,8,17)]
 assert {states[i] for i in live}==set(expected)
 edges={(states[u],states[v]) for u,v in zero if u in live and v in live}
 assert edges=={(expected[i],expected[(i+1)%8]) for i in range(8)}
 out={'states':len(states),'transition_inputs':total,'potential':'CarryHistory.outerPotential from the main Lean source','zero_slack_inputs':len(zero),'pruning_sizes':rounds,'unique_directed_cycle':expected,'conclusion':'A cyclic exterior attaining growth=period/2 has period divisible by 8.'}
 json.dump(out,open('exist_uniform_critical_results.json','w'),indent=2);print(json.dumps(out))
if __name__=='__main__':main()
