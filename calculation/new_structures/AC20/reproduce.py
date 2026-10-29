#!/usr/bin/env python3
"""Optional second implementation: run shared V16 carry-collar scanner, endpoint only.
From repository root: python3 calculation/new_structures/AC20/reproduce.py --full
"""
import argparse,concurrent.futures,pathlib,re,subprocess,tempfile
D=30*(19**3+19**4)
ENGINE='calculation/new_structures/V16/strict_w9_cell_local.cpp'
def main():
 p=argparse.ArgumentParser();p.add_argument('--full',action='store_true');p.add_argument('--sample',type=int,default=1000);a=p.parse_args()
 assert pathlib.Path(ENGINE).is_file()
 with tempfile.TemporaryDirectory() as tmp:
  exe=tmp+'/ac20'
  subprocess.run(['g++','-O3','-std=c++17',ENGINE,'-o',exe],check=True)
  ranges=[(i*823080,823080) for i in range(5)] if a.full else [(0,min(a.sample,D))]
  def one(item):
   st,n=item
   args=[exe,'--endpoint-only','--phase','11','--q','14','--k','100','--steps','120','--collar','170','--start',str(st),'--limit',str(n)]
   s=subprocess.run(args,check=True,capture_output=True,text=True).stdout
   m=re.search(r'range=\[(\d+),(\d+)\) tested=(\d+)',s)
   v=re.search(r'survivors=(\d+) clock_failures=(\d+)',s)
   assert m and v,(item,s[-1000:])
   lo,hi,seen=map(int,m.groups());surv,wrong=map(int,v.groups())
   assert lo==st and hi==st+n and seen==n
   return seen,surv,wrong
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:out=list(pool.map(one,ranges))
  seen=sum(x[0] for x in out);surv=sum(x[1] for x in out);wrong=sum(x[2] for x in out)
  assert seen==(D if a.full else min(D,a.sample))
  if a.full:assert surv==0 and wrong==0
  print('PHASE11_ENDPOINT_ONLY',seen,'of',D,'W9_restored',surv,'clock_errors',wrong)
if __name__=='__main__':main()
