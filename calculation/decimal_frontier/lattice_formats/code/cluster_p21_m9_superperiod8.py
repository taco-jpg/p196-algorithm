#!/usr/bin/env python3
"""Canonicalize local p21/m9 bulk rows under spatial rotation and 21-step time shifts."""
from collections import Counter, defaultdict
from pathlib import Path
import argparse, re
B=10;M=9;G='001001010101001010101'

def phi(row,g):
 try:z=next(i for i,x in enumerate(row) if x!=B-1)
 except StopIteration:return None
 a=[0]*M;d=[0]*M
 a[(z+1)%M]=d[(z-1)%M]=int(row[z]>=B)
 for j in range(1,M):
  i=(z+j)%M;a[(i+1)%M]=(row[i]+a[i])//B
  i=(z-j)%M;d[(i-1)%M]=(row[i]+d[i])//B
 e=[(row[i]+a[i])%B for i in range(M)]
 f=[(row[i]+d[i])%B for i in range(M)]
 return tuple(e[i]+f[(i-g)%M] for i in range(M))

def period_block(row):
 for bit in G:row=phi(row,int(bit))
 return row

def canonical(row,k):
 rows=[]
 for _ in range(k):rows.append(row);row=period_block(row)
 assert row==rows[0]
 return min(tuple(tuple(rows[(t+phase)%k][(i+rot)%M] for i in range(M))
                  for t in range(k)) for phase in range(k) for rot in range(M))

def run(path):
 rows=[];classes=defaultdict(list)
 for s in Path(path).read_text().splitlines():
  m=re.fullmatch(r'k=(\d+) axis=(\d+) index=(\d+) row=([0-9,]+)',s)
  assert m,s
  k,a,idx=map(int,m.groups()[:3]);row=tuple(map(int,m.group(4).split(',')))
  rows.append((k,a,idx,row));classes[(k,canonical(row,k))].append((a,idx,row))
 hist=dict(sorted(Counter(k for k,_,_,_ in rows).items()))
 chist=dict(sorted(Counter(k for k,_ in classes).items()))
 print('labelled primitive m=9 rows:',len(rows),'period_histogram:',hist)
 print('families modulo spatial/time shifts:',len(classes),'period_histogram:',chist)
 for (k,rep),values in sorted(classes.items(),key=lambda q:(q[0][0],q[0][1])):
  print('family blocks=',k,'members=',len(values),'representative=',rep[0])
 assert len(rows)==378 and hist=={2:90,4:216,8:72}
 assert len(classes)==12 and chist=={2:5,4:6,8:1}
 return rows,classes

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('candidate_rows_file');args=a.parse_args();run(args.candidate_rows_file)
