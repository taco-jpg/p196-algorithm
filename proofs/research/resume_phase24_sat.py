"""Width-16 period-24 search with exact temporal phase reduction.

The 30 eligible bulks split into ten orbits under eight-step evolution.
A boundary solution for any orbit member shifts by eight steps to a solution
for every other member, with the same maximum boundary width. Therefore one
UNSAT representative per orbit excludes all thirty width-16 instances.
This does not exclude larger widths, other families, or Lychrel numbers.
"""
import argparse,inspect,json,re
from pathlib import Path
import outer_invariant_cadical as engine
from novel_encoding_phase24_boundary import build
from family_search_bulk_periods import bulk_step

def correct_header(dimacs):
    lines=dimacs.splitlines()
    maximum=max(abs(int(v)) for line in lines if line and line[0] not in 'cp' for v in line.split())
    count=sum(bool(line and line[0] not in 'cp') for line in lines)
    lines=[f'p cnf {maximum} {count}' if line.startswith('p ') else line for line in lines]
    return '\n'.join(lines)+'\n'

def phase_orbits():
    src=json.loads(Path('carry_invariant_research_centers_results.json').read_text())
    remaining={tuple(r['block']) for r in src if r['schedule'][0]==1 and sum(r['block'])%9==0}
    rows=[]
    while remaining:
        b=min(remaining);orbit=[]
        while b not in orbit:
            orbit.append(b)
            for t in range(8):b=next(iter(bulk_step(b,1-t%2)))
        assert b==orbit[0] and set(orbit)<=remaining
        rows.append(orbit);remaining-=set(orbit)
    assert len(rows)==10 and sum(map(len,rows))==30
    return rows

def runner():
    source=inspect.getsource(engine.run_solver).replace("'solve-eqs',",'').replace("'elim-uncnstr',",'')
    source=source.replace('dimacs=g.dimacs()','dimacs=correct_header(g.dimacs())')
    env=dict(vars(engine));env['correct_header']=correct_header;exec(source,env)
    return env['run_solver']

def collect():
    rows=[]
    for orbit in phase_orbits():
        B=orbit[0];stem='resume_phase24_'+''.join(f'{x:02}'for x in B)+'_K16'
        result=json.loads(Path(stem+'.result.json').read_text())
        lines=Path(stem+'.cnf').read_text().splitlines();header=next(x for x in lines if x.startswith('p ')).split()
        maximum=max(abs(int(v)) for line in lines if line and line[0]not in'cp'for v in line.split())
        clauses=sum(bool(line and line[0]not in'cp')for line in lines)
        valid=int(header[2])>=maximum and int(header[3])==clauses
        assert valid and result['result']=='unsat' and result['exit_code']==20
        rows.append({'representative':B,'covered_blocks':orbit,'maximum_boundary_width':16,'result':'unsat','seconds':result['seconds'],'dimacs_header_valid':valid,'clauses':clauses,'max_literal':maximum,'stem':stem})
    output={'period':24,'covered_blocks':30,'representatives':10,'method':'CaDiCaL plus exact eight-step temporal phase symmetry','proof_certificate_checked':False,'rows':rows,'unbounded_width_status':'unknown'}
    Path('resume_phase24_complete_width16.json').write_text(json.dumps(output,indent=2))
    print(json.dumps(output,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--collect',action='store_true');p.add_argument('--seconds',type=int,default=30);args=p.parse_args()
    if args.collect:collect()
    else:
        solve=runner()
        for orbit in phase_orbits():
            B=orbit[0];s,e=build(B,16);stem='resume_phase24_'+''.join(f'{x:02}'for x in B)+'_K16'
            print(json.dumps({'representative':B,'covered_blocks':orbit,'max_boundary_width':16}),flush=True)
            solve(s,e,stem,args.seconds)
