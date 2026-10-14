"""Exact periodic-bulk analysis for the eleven-step neutral-interface clock.

These are bi-infinite periodic bulk transitions, not finite-integer orbit
tests. A candidate bulk still requires both finite exterior and center glue.
"""
from itertools import product
from pathlib import Path
import json,time
from family_search_bulk_periods import bulk_step

SCHEDULE=(1,1,0,0,0,1,0,0,0,0,1)

def evolution(word):
    states={tuple(word)};history=[sorted(states)]
    for overflow in SCHEDULE:
        states={out for source in states for out in bulk_step(source,overflow)}
        history.append(sorted(states))
    return states,history

def rotations(word):
    return {word[j:]+word[:j]for j in range(len(word))}

def search(period):
    candidates=[];tested=0
    for word in product(range(19),repeat=period):
        if len(set(word))==1 or word!=min(rotations(word)):continue
        tested+=1
        outputs,_=evolution(word)
        matches=outputs & rotations(word)
        if matches:candidates.append({'word':word,'outputs':sorted(matches)})
    return {'period':period,'nonconstant_rotation_classes':tested,'candidates':candidates}

if __name__=='__main__':
    started=time.monotonic()
    outputs,history=evolution((13,14))
    row={'input':[13,14],'schedule':SCHEDULE,'history':history,'outputs':sorted(outputs)}
    print(json.dumps(row),flush=True)
    period_results=[]
    for period in (2,3):
        result=search(period);period_results.append(result)
        print(json.dumps(result),flush=True)
    doc={'alternating_13_14':row,'periodic_bulk_search':period_results,'seconds':time.monotonic()-started}
    Path('persist_block_nested_bulk_results.json').write_text(json.dumps(doc,indent=2))
