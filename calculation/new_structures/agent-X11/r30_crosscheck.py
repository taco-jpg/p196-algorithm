#!/usr/bin/env python3
"""Cross-check all scaled-width controls against the repository's R30 verifier."""
import json, pathlib, subprocess, tempfile
from independent_replay import all_cases
ROOT=pathlib.Path(__file__).resolve().parents[3]
R30=ROOT/'calculation/new_structures/R30/verify.cpp'
LATTICE=ROOT/'calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt'
def main():
    assert R30.is_file() and LATTICE.is_file(),(R30,LATTICE)
    results=list(all_cases())
    with tempfile.TemporaryDirectory(prefix='x11-r30-') as td:
        exe=pathlib.Path(td)/'r30_verify'
        subprocess.run(['g++','-O3','-std=c++17',str(R30),'-o',str(exe)],check=True)
        for x in results:
            C=','.join(['0']*x['centre_length']);J=','.join(map(str,x['J']))
            raw=subprocess.check_output([str(exe),str(LATTICE),str(x['q']),str(x['k']),J,'9,10,8',C,'120'],text=True)
            got=json.loads(raw)
            assert got['return'] is False,(x,got)
            assert got['first_mismatch']==x['first_mismatch'],(x,got)
            assert got['gamma']==x['gamma'],(x,got)
            assert got['sum_gamma']==x['sum_gamma']==30,(x,got)
            assert got['palindrome_at']==-1,(x,got)
            assert got['digits']==x['final_digits'],(x,got)
    print(json.dumps({'status':'R30_CROSSCHECK_PASS','cases':len(results),
      'widths':[[20,80],[40,160],[80,320],[160,640]],'junctions':4,'centre_lengths':[14,16,18,20,22,24],
      'engines':['repository R30 digit-vector verifier','Python bigint n+reverse','fresh-buffer decimal digit vector','folded pairword recurrence'],
      'exact_agreement':['return false','first mismatch index','all 120 overflow bits','overflow sum 30','nonpalindrome guard','final digit count']},separators=(',',':')))
if __name__=='__main__':main()