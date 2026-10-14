"""Symbolic arbitrary-width reachability for the exact exterior column graph.

The clauses describe all finite spatial paths, not a bounded prefix scan.
A solver answer alone is not a finite Lychrel proof: SAT needs an extracted
path and finite-family replay; UNSAT needs a separately checked invariant.
Requires z3-solver. No project-specific modules are imported.
"""
from pathlib import Path
import argparse,itertools,json,time,hashlib,subprocess,sys
import z3 as z

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]

def variables(tag,J):
    return [[z.Int(f'{tag}_{part}_{j}') for j in range(J)] for part in 'abcz']

def flat(state):return [x for row in state for x in row]

def bounds(state):
    return [test for row in state[:3] for v in row for test in (v>=0,v<=1)]+[
        test for v in state[3] for test in (v>=-1,v<=9)]

def transition(old,new):
    J=len(old[0]);Q=[z.Int(f'Q_{j}') for j in range(J)]
    R=[z.Int(f'R_{j}') for j in range(J)]
    E=[z.Int(f'E_{j}') for j in range(J)]
    clauses=bounds(old)+bounds(new)
    for j in range(J):
        a,b,c,w=[row[j] for row in old]
        na,nb,nc,nw=[row[j] for row in new]
        q,r,e=Q[j],R[j],E[j]
        clauses += [q>=0,q<=18,r>=0,r<=18,e>=0,e<=1,
                    q+a-10*na>=0,q+a-10*na<=9,
                    q+nc-10*c>=0,q+nc-10*c<=9,
                    r==2*q+a+nc-10*na-10*c,
                    r+b-10*nb>=0,r+b-10*nb<=9,
                    nw==r-10*e,w+e>=0,w+e<=9,
                    Q[(j+1)%J]==r+b-10*nb+w+e]
    return clauses,Q+R+E

def initial(J,outer=8):
    return ((0,)*J,(1,)*J,(int(outer==8),)*J,(outer-1,)*J)

def direct_successors(state):
    """Integer carry enumeration independently using div/mod operations."""
    J=len(state[0]);out=set()
    def walk(j,Q,Q0,rows):
        if j==J:
            if Q==Q0:out.add(tuple(tuple(row) for row in rows))
            return
        a,b,c,w=(row[j] for row in state)
        for nc in (0,1):
            if (Q+nc)//10!=c:continue
            R=(Q+a)%10+(Q+nc)%10
            for e in (0,1):
                if R<9 and e!=0 or R>9 and e!=1:continue
                if not 0<=w+e<=9:continue
                Qn=(R+b)%10+w+e
                if not 0<=Qn<=18:continue
                vals=((Q+a)//10,(R+b)//10,nc,R-10*e)
                walk(j+1,Qn,Q0,[row+[v] for row,v in zip(rows,vals)])
    for q in range(19):walk(0,q,q,[[],[],[],[]])
    return out

def encoding_checks():
    records=[]
    states=[((a,),(b,),(c,),(w,)) for a,b,c in itertools.product(range(2),repeat=3)
            for w in range(-1,10)]
    states += [initial(12),initial(12,9)]
    for state in states:
        J=len(state[0]);old=variables('old',J);new=variables('new',J)
        constraints,_=transition(old,new);solver=z.Solver();solver.add(*constraints)
        solver.add(*[v==n for v,n in zip(flat(old),flat(state))])
        found=set()
        while solver.check()==z.sat:
            model=solver.model();successor=tuple(tuple(model.eval(v).as_long() for v in row) for row in new)
            found.add(successor)
            solver.add(z.Or(*[v!=n for v,n in zip(flat(new),flat(successor))]))
        expected=direct_successors(state)
        assert found==expected,(state,len(found),len(expected))
        records.append(dict(phase_pairs=J,state=state,successors=len(found)))
    result=dict(status='exact_transition_controls_passed',controls=len(records),
                all_88_single_phase_states=True,period24_roots_checked=True,
                records=records,z3_version=z.get_version_string())
    (HERE/'spacer_encoding_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)

def targets():
    # Existing target metadata includes exact one-column suffixes. The
    # direct bulk states are identified by the empty suffix convention.
    path=PROJECT/'main_existence_attempt/morphic_return/exterior_all_chiralities_target_metadata.json'
    data=json.loads(path.read_text())
    return data

def run(seconds=90):
    started=time.monotonic();J=12;old=variables('old',J);new=variables('new',J)
    clauses,aux=transition(old,new)
    reach=z.Function('Reach',*([z.IntSort()]*(4*J)),z.BoolSort())
    goal=z.Function('BoundaryReached',z.BoolSort())
    fp=z.Fixedpoint();fp.set(engine='spacer',timeout=int(seconds*1000))
    fp.register_relation(reach,goal);fp.declare_var(*(flat(old)+flat(new)+aux))
    fp.rule(reach(*flat(initial(J))))
    fp.rule(reach(*flat(new)),[reach(*flat(old)),*clauses])
    # The empty column suffix denotes a direct bulk cut state.
    data=targets();items=data['metadata'] if isinstance(data,dict) and 'metadata' in data else data
    direct=set()
    for item in items:
        if item['columns']==[]:
            state=tuple(tuple(row) for row in item['state'])
            # Metadata deduplicates coincident target/suffix states. The
            # root is fixed under every temporal rotation, so include the
            # full rotation-invariant direct target set explicitly.
            for shift in range(J):
                direct.add(tuple(row[shift:]+row[:shift] for row in state))
    assert len(direct)==12,len(direct)
    for target in sorted(direct):
        assert len(target)==4 and all(len(row)==J for row in target)
        fp.rule(goal(),reach(*flat(target)))
    problem=fp.sexpr()+'\n(query BoundaryReached)\n'
    (HERE/'spacer_boundary.smt2').write_text(problem)
    answer=None
    try:
        result=str(fp.query(goal()))
        if result=='unknown':
            reason=fp.reason_unknown()
        else:
            reason=None
            answer=str(fp.get_answer())
    except z.Z3Exception as exc:
        result='unknown';reason=str(exc)
    if answer is not None:
        (HERE/'spacer_answer.txt').write_text(answer+'\n')
    record=dict(status=result,reason=reason,elapsed_seconds=time.monotonic()-started,
                timeout_seconds=seconds,direct_targets=len(direct),z3_version=z.get_version_string(),
                problem_sha256=hashlib.sha256(problem.encode()).hexdigest(),
                scope='24-phase 8/17 exterior column graph; not full decimal existence',
                independently_checked_answer=False)
    (HERE/'spacer_result.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record),flush=True)

def supervised_run(seconds):
    """Enforce a process deadline even if the solver timeout is unresponsive."""
    started=time.monotonic()
    try:
        child=subprocess.run([sys.executable,str(Path(__file__).resolve()),
                              '--worker','--seconds',str(seconds)],
                             capture_output=True,text=True,timeout=seconds+5)
        print(child.stdout,end='',flush=True)
        if child.stderr:print(child.stderr,end='',file=sys.stderr,flush=True)
        if child.returncode:raise SystemExit(child.returncode)
    except subprocess.TimeoutExpired:
        problem=(HERE/'spacer_boundary.smt2').read_bytes()
        record=dict(status='unknown',reason='external process deadline',
                    elapsed_seconds=time.monotonic()-started,
                    requested_solver_timeout_seconds=seconds,
                    external_timeout_seconds=seconds+5,
                    problem_sha256=hashlib.sha256(problem).hexdigest(),
                    independently_checked_answer=False,
                    scope='24-phase 8/17 exterior column graph; not full decimal existence')
        (HERE/'spacer_result.json').write_text(json.dumps(record,indent=2)+'\n')
        print(json.dumps(record),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--checks',action='store_true');p.add_argument('--seconds',type=float,default=90)
    p.add_argument('--worker',action='store_true',help=argparse.SUPPRESS)
    args=p.parse_args()
    if args.checks:encoding_checks()
    elif args.worker:run(args.seconds)
    else:supervised_run(args.seconds)
