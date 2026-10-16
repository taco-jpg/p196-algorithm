from exist_tile_horn import *
import hashlib
start=time.monotonic();s,xs,meta=build();data=json.load(open('exist_tile_lazy_results.json'));cores=data['cores']
for core in cores:s.add(z3.Or([z3.Not(xs[k]) for k in core]))
s.set(timeout=45000);print('built',len(cores),flush=True);r=s.check();out=dict(meta,seed=None,status=str(r),seconds=time.monotonic()-start,learnt_cores=len(cores),decimal_existence_proved=False)
if r==z3.sat:
    out['tiles']=[i for i in range(NW) if z3.is_true(s.model().eval(xs[i],model_completion=True))];out['independent_check']=path_and_check(out['tiles']);out['decimal_existence_proved']=all(out['independent_check'].get(k,False) for k in ('nonempty','safe','closed'))
if r==z3.unknown:out['reason']=s.reason_unknown()
print(json.dumps(out,indent=2),flush=True);json.dump(out,open('exist_tile_hybrid_results.json','w'),indent=2)
