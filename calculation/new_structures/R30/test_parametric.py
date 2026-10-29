#!/usr/bin/env python3
"""All 120 symbolic phases vs real integers; independent C++ cross-check."""
import argparse, json, subprocess
from parametric import CannotProve, actual, actual_pair, digits, realize, tpl, step, load_lattice

def expand(s,q,k):
    out=[]
    for r in s:
        n=r.n.val(q,k)
        assert n>=0
        out.extend(r.word*n)
    return out

def main():
    a=argparse.ArgumentParser()
    a.add_argument('--lattice',required=True)
    a.add_argument('--cpp',required=True)
    args=a.parse_args()
    B,W,gamma=load_lattice(args.lattice)
    seeds=[([5],[9,14,4],[10]),([6,4],[9,2,16],[12]),([1,8,2],[9,0,18],[4,8,4])]
    J,U,C=seeds[0];sy=tpl(B,W,J,U,C)
    trials=[(256,256),(257,263)]
    states=[realize(expand(sy,q,k)) for q,k in trials]
    for t in range(120):
        for (q,k),n in zip(trials,states):
            assert expand(sy,q,k)==actual_pair(n),(t,q,k)
        new,g=step(sy,256,256)
        nxt=[]
        for (q,k),n in zip(trials,states):
            d=digits(n);rv=0
            for x in d:rv=rv*10+x
            nn=n+rv
            assert len(digits(nn))-len(d)==g,(t,q,k)
            nxt.append(nn)
        sy,states=new,nxt
    print('SYMBOLIC_VS_PYTHON_120_PHASES_PASS')
    for index,(J,U,C) in enumerate(seeds):
        for q,k in [(20,20),(40,40),(80,80),(160,160)]:
            py=actual(B,W,J,U,C,q,k,120)
            cmd=[args.cpp,args.lattice,str(q),str(k),','.join(map(str,J)),
                 ','.join(map(str,U)),','.join(map(str,C)),'120']
            cpp=json.loads(subprocess.check_output(cmd,text=True))
            for field in ['return','gamma','sum_gamma','first_mismatch','digits','expected_digits']:
                assert py[field]==cpp[field],(index,q,k,field,py,cpp)
            print('PYTHON_CPP_120_PASS',index,q,k,flush=True)
    print('R30_INDEPENDENT_TESTS_PASS')

if __name__=='__main__':main()
