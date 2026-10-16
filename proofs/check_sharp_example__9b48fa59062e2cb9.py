#!/usr/bin/env python3
"""Literal ordinary-integer replay of the externally supplied sharp example."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
PHASES = ((4,4,0),(8,8,0),(16,16,0),(7,14,7),(15,8,15),(6,14,14),(13,9,9))
middle = [1,1,14,16,14,1,1]
q0 = [4,4,0] + middle + [0,4,4]
d = [0] * len(q0)
for i in range(len(q0)//2):
    d[-1-i] = min(9,q0[i])
    d[i] = q0[i] - d[-1-i]
d[len(q0)//2] = q0[len(q0)//2]//2
seed = sum(a*10**i for i,a in enumerate(d))
states = []
n = seed
for t in range(29):
    ds = [int(a) for a in str(n)[::-1]]
    q = [a+b for a,b in zip(ds,reversed(ds))]
    if t == 0:
        assert q == q0
    states.append({"time":t, "integer":str(n), "pair_word":q,
                   "prefix":q[:3], "on_phase_clock":tuple(q[:3])==PHASES[t%7],
                   "is_palindrome":str(n)==str(n)[::-1]})
    n += int(str(n)[::-1])
assert all(s['on_phase_clock'] for s in states[:27])
assert not states[27]['on_phase_clock']
assert all(states[t]['prefix']==[4,4,0] for t in (0,7,14,21))
assert states[28]['prefix'] != [4,4,0]
assert not any(s['is_palindrome'] for s in states[1:])
result = {"status":"PASS", "external_example_commit":"6889b717599343b6773d376e728ca5b03cf68527",
          "seed":str(seed), "three_consecutive_safe_returns":[7,14,21],
          "initial_phase_clock_transitions":26,"first_phase_deviation_state":27,
          "safe_positive_steps_checked":28, "all_states":states,
          "later_behavior_claimed":False,"main_existence_proved":False}
(HERE/'sharp_example.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='all_states'},indent=2))
