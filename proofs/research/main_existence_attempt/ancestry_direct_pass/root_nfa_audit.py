"""Replay component exclusions without importing the discovery program."""
import hashlib,json
from pathlib import Path
here=Path(__file__).resolve().parent
nfap=here.parent/'return_pass/language/safe_image2_nfa.json'
cp=here/'language/terminal_acceptance_result.json'
n=json.loads(nfap.read_text());c=json.loads(cp.read_text())
assert hashlib.sha256(nfap.read_bytes()).hexdigest()==c['nfa_sha256']
expected={(i,j) for i,mask in enumerate(n['terminal_masks']) for j in range(11) if mask>>j&1}
edges=[dict(row) for row in n['transitions']]
seen=set();max_steps=0;max_digits=0
for item in c['proofs']:
    flag=tuple(item['flag']);assert flag in expected and flag not in seen
    pairs,center,path=item['pairs'],item['center'],item['path']
    assert len(path)==len(pairs)+1 and path[0] in n['initial'] and path[-1]==flag[0]
    assert flag[1]==(0 if center is None else center//2+1)
    assert center is None or (0<=center<=18 and center%2==0)
    assert all(0<=q<=18 for q in pairs)
    assert (pairs and pairs[0]>0) or (not pairs and center is not None and center>0)
    for u,q,v in zip(path,pairs,path[1:]):assert v in edges[u].get(q,[])
    high=[min(q,9) for q in pairs]
    low=[max(q-9,0) for q in pairs][::-1]
    text=''.join(map(str,high+([] if center is None else [center//2])+low))
    x=int(text);max_digits=max(max_digits,len(text))
    for t in range(1,item['hit_steps']+1):
        x+=int(str(x)[::-1])
        pal=str(x)==str(x)[::-1]
        assert pal==(t==item['hit_steps'])
    seen.add(flag);max_steps=max(max_steps,item['hit_steps'])
assert seen==expected and len(seen)==8396
r={'status':'PASS','terminal_flags_checked':len(seen),'max_first_hit':max_steps,
   'max_input_digits':max_digits,'nfa_sha256':c['nfa_sha256'],
   'certificate_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
   'scope':'No nonempty choice of the original NFA terminal flags yields a safe forward-closed language. This does not exclude refined configuration languages or prove Lychrel existence.'}
(here/'root_nfa_audit.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r))
