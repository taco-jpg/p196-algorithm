import sys
sys.argv=['x','11','100','10','10']
exec(open('ext_sat.py').read().split("s=cp_model.CpSolver()")[0])
sol=[[13,16,19,15],[3,9,15,14,4],[6,19,9,7]]
for t in range(p):
    row=sol[t]+[b-1]*(K-len(sol[t]))
    for k in range(K): m.Add(B[t][k]==row[k])
s=cp_model.CpSolver(); s.parameters.num_workers=1; s.parameters.max_time_in_seconds=10
st=s.Solve(m); print(s.StatusName(st))
