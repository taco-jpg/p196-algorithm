"""Literal integer and direct-NFA controls; no subset construction."""
from pathlib import Path
import hashlib,json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
source=ROOT/'main_existence_attempt/return_pass/language/safe_image2_nfa.json'
a=json.loads(source.read_text())


def fold(n):
    ds=[int(x) for x in str(n)]
    k=len(ds)//2
    return [ds[i]+ds[-1-i] for i in range(k)],2*ds[k] if len(ds)%2 else None


def accepting_flags(w):
    p,c=w
    states=set(a['initial'])
    for q in p:
        states={v for u in states for label,targets in a['transitions'][u] if label==q for v in targets}
    j=0 if c is None else c//2+1
    return [[u,j] for u in sorted(states) if a['terminal_masks'][u]>>j&1]


orbit=[89]
for _ in range(24):
    n=orbit[-1]
    orbit.append(n+int(str(n)[::-1]))
assert all(str(n)!=str(n)[::-1] for n in orbit[1:24])
assert str(orbit[24])==str(orbit[24])[::-1]
w=fold(orbit[22])
v=fold(orbit[23])
assert w==([17,9,10,11,9,9],None)
assert v==([8,8,1,3,2,0],0)
assert accepting_flags(w) and accepting_flags(v)
assert accepting_flags(([6,13],None))==[[6679,0]]
result=dict(status='PASS',first_palindrome_time_89=24,source_integer=orbit[22],
            target_integer=orbit[23],palindrome_integer=orbit[24],source_pair_word=w,
            target_pair_word=v,source_accepting_flags=accepting_flags(w),
            target_accepting_flags=accepting_flags(v),pair_word_1675_accepting_flags=[[6679,0]],
            nfa_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
(HERE/'ancestry_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
