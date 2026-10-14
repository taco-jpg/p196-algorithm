"""Independent replay: no transducer, synthesis, or orbit-search imports."""
from pathlib import Path
import hashlib,json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
source=ROOT/'main_existence_attempt/return_pass/language/safe_image2_nfa.json'
proof_file=HERE/'terminal_acceptance_result.json'
a=json.loads(source.read_text())
data=json.loads(proof_file.read_text())
assert data['status']=='EMPTY_ACCEPTANCE_FAMILY'
assert hashlib.sha256(source.read_bytes()).hexdigest()==data['nfa_sha256']
allflags={(u,j) for u,m in enumerate(a['terminal_masks']) for j in range(11) if m>>j&1}
seen=set()
max_steps=0
max_digits=0
palindrome_max_digits=0
for row in data['proofs']:
    u,j=row['flag']
    assert (u,j) in allflags and (u,j) not in seen
    pairs,c,path=row['pairs'],row['center'],row['path']
    assert j==(0 if c is None else c//2+1)
    assert c is None or c in range(0,19,2)
    assert len(path)==len(pairs)+1 and path[0] in a['initial'] and path[-1]==u
    assert pairs and 1<=pairs[0]<=18 or not pairs and c is not None and c>0
    assert all(type(q) is int and 0<=q<=18 for q in pairs)
    for node,q,nxt in zip(path,pairs,path[1:]):
        assert any(label==q and nxt in targets for label,targets in a['transitions'][node])
    # Independent arithmetic construction via place-value sum from low end.
    digits=[max(0,q-9) for q in pairs]
    if c is not None:
        digits.append(c//2)
    digits.extend(min(q,9) for q in reversed(pairs))
    n=sum(d*10**i for i,d in enumerate(digits))
    assert n>0
    max_digits=max(max_digits,len(str(n)))
    hit=row['hit_steps']
    assert type(hit) is int and 1<=hit<=data['orbit_limit']
    for t in range(1,hit+1):
        z=n
        reverse=0
        while z:
            reverse=10*reverse+z%10
            z//=10
        n+=reverse
        ds=str(n)
        assert (ds==ds[::-1])==(t==hit)
    max_steps=max(max_steps,hit)
    palindrome_max_digits=max(palindrome_max_digits,len(str(n)))
    seen.add((u,j))
assert seen==allflags
result=dict(status='INDEPENDENT_ALL_FLAGS_EXCLUSION_VERIFIED',nfa_states=len(a['transitions']),
            flags=len(allflags),verified_paths=len(seen),largest_first_hit=max_steps,
            largest_input_digits=max_digits,largest_palindrome_digits=palindrome_max_digits,
            nfa_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            certificate_sha256=hashlib.sha256(proof_file.read_bytes()).hexdigest())
(HERE/'terminal_certificate_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
