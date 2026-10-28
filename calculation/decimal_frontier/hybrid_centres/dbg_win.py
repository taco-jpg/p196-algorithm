from ortools.sat.python import cp_model
from hsat import tuples
from runsat import stream
import hwin
b=10
cyc=stream('p11'); p=11
gam=[cyc[t][1] for t in range(p)]; e1=[cyc[t][2] for t in range(p)]
print('gam',gam,'e1',e1)
# replicate solve_window but extract solution
T=p; K=3; A=0; N=9
m = cp_model.CpModel(); TUP = tuples(b)
Q = [[m.NewIntVar(0, 2 * b - 2, f"Q{t}_{i}") for i in range(K)] for t in range(T + 1)]
D=[]; AA=[]
for t in range(T):
    a = [m.NewBoolVar(f"a{t}_{i}") for i in range(K + 1)]
    d = [m.NewBoolVar(f"d{t}_{i}") for i in range(K + 1)]
    da = [m.NewIntVar(0, b - 1, f"da{t}_{i}") for i in range(K)]
    dd = [m.NewIntVar(0, b - 1, f"dd{t}_{i}") for i in range(K)]
    m.Add(a[0] == e1[t]); m.Add(d[0] == 1 - e1[t])
    for i in range(K):
        m.AddAllowedAssignments([Q[t][i], a[i], da[i], a[i + 1]], TUP)
        m.AddAllowedAssignments([Q[t][i], d[i + 1], dd[i], d[i]], TUP)
    if gam[t] == 0:
        for i in range(K): m.Add(Q[t + 1][i] == da[i] + dd[i])
    else:
        wconst = N * e1[t]
        m.Add(Q[t + 1][0] == da[0] + wconst)
        for i in range(1, K): m.Add(Q[t + 1][i] == da[i] + dd[i - 1])
    D.append(d); AA.append(a)
for i in range(K): m.Add(Q[T][i] == Q[0][i])
sol = cp_model.CpSolver(); st = sol.Solve(m); print(sol.StatusName(st))
for i in range(K):
    print('cell',i,'v',[sol.Value(Q[t][i]) for t in range(T+1)])
    print('   A_i',[sol.Value(AA[t][i]) for t in range(T)],' Dout_i',[sol.Value(D[t][i]) for t in range(T)],' Din_i',[sol.Value(D[t][i+1]) for t in range(T)])
