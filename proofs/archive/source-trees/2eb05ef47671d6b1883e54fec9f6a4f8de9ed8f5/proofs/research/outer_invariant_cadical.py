"""Exact bit-vector bit-blasting with retained Z3 model conversion."""
import inspect,json,re,subprocess,sys,time,os
from pathlib import Path
import z3 as z
import outer_invariant_brown72 as brown

CADICAL=os.environ.get('CADICAL','cadical')

def run_solver(solver, outputs, stem, seconds):
    goal=z.Goal();goal.add(*solver.assertions())
    t0=time.monotonic()
    pipeline=z.Then('simplify','propagate-values','solve-eqs','elim-uncnstr','reduce-bv-size','bit-blast','tseitin-cnf')
    reduced=pipeline(goal)
    assert len(reduced)==1
    g=reduced[0];dimacs=g.dimacs()
    Path(stem+'.cnf').write_text(dimacs)
    names={int(m.group(1)):m.group(2)for m in re.finditer(r'^c (\d+) (.+)$',dimacs,re.M)}
    header=next(a for a in dimacs.splitlines()if a.startswith('p '))
    print(json.dumps({'stage':'encoded','header':header,'seconds':round(time.monotonic()-t0,3)}),flush=True)
    t0=time.monotonic()
    with open(stem+'.solver.log','w')as log:
        proc=subprocess.run([CADICAL,'-q','-t',str(seconds),stem+'.cnf'],stdout=log,stderr=subprocess.STDOUT,timeout=seconds+10)
    txt=Path(stem+'.solver.log').read_text()
    out={'stage':'solved','exit_code':proc.returncode,'seconds':round(time.monotonic()-t0,3)}
    if 's SATISFIABLE' in txt:
        lits=[]
        for line in txt.splitlines():
            if line.startswith('v '):lits.extend(map(int,line[2:].split()))
        assignment={abs(a):a>0 for a in lits if a}
        atoms={};seen=set();stack=list(g)
        while stack:
            a=stack.pop()
            if a.get_id() in seen:continue
            seen.add(a.get_id())
            if z.is_const(a) and z.is_bool(a):atoms[str(a.decl().name())]=a
            else:stack.extend(a.children())
        model=z.Model()
        for i,name in names.items():model.update_value(atoms[name],z.BoolVal(assignment.get(i,False)))
        original=g.convert_model(model)
        vals=[original.eval(a,model_completion=True).as_long()for a in outputs]
        checker=z.Solver();checker.add(*solver.assertions());checker.add(*[a==n for a,n in zip(outputs,vals)])
        check=checker.check();assert check==z.sat,('recovered_model_failed',check,vals)
        out.update(result='sat',values=vals,model_rechecked=True)
    elif 's UNSATISFIABLE' in txt:out['result']='unsat'
    else:out['result']='unknown'
    Path(stem+'.result.json').write_text(json.dumps(out,indent=2));print(json.dumps(out),flush=True)
    return out

if __name__=='__main__':
    if '--toy' in sys.argv:
        x=z.BitVec('toy_x',5);y=z.BitVec('toy_y',5);s=z.Solver();s.add(x+y==15,z.UGE(x,7),z.UGE(y,6),z.ULE(x,10),z.ULE(y,10))
        result=run_solver(s,[x,y],'outer_invariant_cadical_toy',5)
        assert result['result']=='sat' and sum(result['values'])==15
    else:
        K=int(sys.argv[1])if len(sys.argv)>1 else 24
        source=inspect.getsource(brown.search).replace('def search(','def build(',1).replace('t0=time.monotonic();res=solver.check()','return solver,edge\n    t0=time.monotonic();res=solver.check()',1)
        env=dict(vars(brown));exec(source,env)
        solver,edge=env['build'](K)
        print(json.dumps({'stage':'built','k':K,'period':72,'clock':'Brown','growth':36}),flush=True)
        run_solver(solver,edge,f'outer_invariant_cadical_brown72_K{K}',120)
