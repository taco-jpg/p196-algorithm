#!/usr/bin/env python3
"""Strict rerun of the COMPLETE 17-stream agent-15 follow-up, not census slices."""
import csv,sys,subprocess,re,tempfile,pathlib
root=pathlib.Path(__file__).resolve().parent
compact=root/'agent15_compact'
mirror=root/'agent15_mirror'
ind=root/'agent15_independent_mirror'

def output(b,g,cap):
    with tempfile.NamedTemporaryFile('w',delete=False) as f:
        f.write(g+'\n');fn=f.name
    try:
        p=subprocess.run([str(compact),str(b),str(cap),fn],check=True,capture_output=True,text=True)
        line=next(line for line in p.stdout.splitlines() if line.startswith(('CAPPED ','DECIDED_ACYCLIC ','EXHAUSTED_REPEAT ')))
        return line
    finally:pathlib.Path(fn).unlink()

def main():
    # Mandatory controls: exact state count, edge count, and known repeated-edge SCC structure.
    for b,w,n,e,rep in [(9,'1100011000',956310,1005301,48992),
                         (13,'1010010000',250302,254201,3900),
                         (7,'10'*12,32771,40962,8192)]:
        s=output(b,w,3000000)
        assert 'EXHAUSTED_REPEAT' in s and f'states={n} ' in s and f'edges={e} ' in s and f'repeated={rep} ' in s,s
        print('PASS CONTROL',b,w,flush=True)
    rows=list(csv.DictReader((root/'agent15_f2_17.tsv').open(),delimiter='\t'))
    assert len(rows)==17 and len(set((r['base'],r['overflow']) for r in rows))==17
    assert sum(r['status']=='CAPPED' for r in rows)==8
    for index,r in enumerate(rows,1):
        b=int(r['base']);w=r['overflow'];cap=int(r['state_cap'])
        assert len(w)==int(r['period'])
        text=output(b,w,cap)
        for q in (r['status'],f"states={r['states']} ",f"edges={r['edges']} ",f"repeated={r['repeated_edges']} "):
            assert q in text,(index,r,q,text)
        print('PASS',index,'of',len(rows),r['base'],w,r['status'],flush=True)
    # Mirror-row control and independent second implementation of cyclic carries.
    subprocess.run([str(ind)],check=True)
    subprocess.run([sys.executable,str(root/'agent15_independent_predecessor.py')],check=True)
    b7='101001010110001011000'
    for m,tested,hits,genuine in [(1,13,2,2),(3,169,2,0),(9,371293,2,0)]:
        s=subprocess.run([str(mirror), '7', b7,str(m),'1000000'],capture_output=True,text=True,check=True).stdout
        assert f'EXHAUSTED b=7 p=21 m={m} tested={tested} return_rows={hits} genuine_rows={genuine}' in s,s
    print('ALL CHECKS PASSED: all 17 follow-up streams and exact b7 p21 mirror no-go')
if __name__=='__main__':main()
