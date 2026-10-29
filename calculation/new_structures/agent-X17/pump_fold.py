#!/usr/bin/env python3
"""Finite-horizon tests for a uniform eight-folded-pair pumping insertion."""
import sys,csv
sys.set_int_max_str_digits(0)
M='88283583'
def initial(n,m):
 s=''.join(M[min(i,n-1-i)%8] for i in range(n))
 p=int(s)
 for k in range(1,9):
  if m>>(k-1)&1:p+=10**(n//2-k)
 return p
def st(n):
 s=str(n);return n+int(s[::-1])
def fold(n):
 s=str(n); L=len(s)
 return list(zip(s[::-1][:L//2],s[:L//2])),(s[L//2] if L%2 else '')
def table(n,T,selected=None):
 masks=selected or range(256)
 a={m:initial(n,m) for m in masks}
 b={m:initial(n+16,m) for m in masks}
 rows=[]
 for t in range(T+1):
  bounds=[];arrays=[]; centres=[]
  for mask in masks:
   av,ac=fold(a[mask]);bv,bc=fold(b[mask]);
   if len(bv)!=len(av)+8 or ac!=bc:
    print('INCOMPATIBLE LENGTH/CENTRE',n,t,mask,len(av),len(bv),ac,bc);return rows
   L=len(av)
   l=next((i for i in range(L) if av[i]!=bv[i]),L)
   r=next((i for i in range(L) if av[L-1-i]!=bv[len(bv)-1-i]),L)
   bounds.append((L-r,l));arrays.append((av,bv))
  lo=max(z[0] for z in bounds);hi=min(z[1] for z in bounds)
  wins=[]
  for j in range(lo,hi+1):
   blocks={tuple(bv[j:j+8]) for av,bv in arrays}
   if len(blocks)==1:wins.append((j,''.join(''.join(x) for x in next(iter(blocks)))))
  if not wins:
   print('PUMP FAIL',n,t,'jrange',lo,hi,'states',len(arrays));return rows
  # select rightmost uniform j (closest to centre)
  j,block=wins[-1]
  rows.append((n,t,len(arrays[0][0]),lo,hi,j,block,len(wins)))
  if t<T:
   a={mask:st(v) for mask,v in a.items()};b={mask:st(v) for mask,v in b.items()}
 return rows
if __name__=='__main__':
 n=int(sys.argv[1]) if len(sys.argv)>1 else 1001;T=int(sys.argv[2]) if len(sys.argv)>2 else 113
 rows=table(n,T)
 print('rows',len(rows),'n',n,'last',rows[-1] if rows else None)
 if len(sys.argv)>3:
  with open(sys.argv[3],'w',newline='') as f:
   w=csv.writer(f);w.writerow(['n','t','halfwidth','valid_min','valid_max','chosen_j','insertion_folded_pairs','common_choices']);w.writerows(rows)
