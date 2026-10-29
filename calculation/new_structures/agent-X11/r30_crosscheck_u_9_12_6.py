#!/usr/bin/env python3
"""Cross-check scaled-width U=(9,12,6) controls against repository R30."""
import json,pathlib,subprocess,tempfile
from independent_replay_u_9_12_6 import run
ROOT=pathlib.Path(__file__).resolve().parents[3]
R30=ROOT/'calculation/new_structures/R30/verify.cpp'
LATTICE=ROOT/'calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt'
def main():
    assert R30.is_file() and LATTICE.is_file(),(R30,LATTICE)
    widths=[(20,80),(40,160),(80,320),(160,640)]
    junctions=[[0,0,0],[18,18,18],[0,0,0,0],[18,18,18,18]]
    centres=[14,24]
    with tempfile.TemporaryDirectory(prefix='x11-r30-u126-') as td:
        exe=pathlib.Path(td)/'r30_verify'
        subprocess.run(['g++','-O3','-std=c++17',str(R30),'-o',str(exe)],check=True);count=0
        for q,k in widths:
            for J in junctions:
                for clen in centres:
                    x=run(q,k,J,clen);C=','.join(['0']*clen);Jcsv=','.join(map(str,J))
                    raw=subprocess.check_output([str(exe),str(LATTICE),str(q),str(k),Jcsv,'9,12,6',C,'120'],text=True);got=json.loads(raw)
                    assert got['return'] is False and got['first_mismatch']==x['first_mismatch'],(x,got)
                    assert got['gamma']==x['gamma'] and got['sum_gamma']==x['sum_gamma']==30,(x,got)
                    assert got['palindrome_at']==-1 and got['digits']==x['final_digits'],(x,got)
                    count+=1
    print(json.dumps({'status':'R30_CROSSCHECK_PASS','cases':count,'widths':widths,'junctions':len(junctions),'centre_lengths':centres,'engines':['repository R30 digit-vector verifier','Python bigint n+reverse','fresh-buffer decimal digit vector','folded pairword recurrence'],'agreement':['first mismatch','all overflow bits','overflow sum','palindrome guard','final digit count']},separators=(',',':')))
if __name__=='__main__':main()