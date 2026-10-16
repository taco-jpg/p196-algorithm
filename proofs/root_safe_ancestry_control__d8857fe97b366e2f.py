"""Ordinary arithmetic control; no carry-transducer implementation imports."""
import json
from pathlib import Path
n=89
orbit=[n]
while True:
    n+=int(str(n)[::-1])
    orbit.append(n)
    if str(n)==str(n)[::-1]:
        break
assert len(orbit)-1==24
def folded(n):
    s=str(n)
    return [[int(s[i])+int(s[-1-i]) for i in range(len(s)//2)],
            2*int(s[len(s)//2]) if len(s)%2 else None]
result={'seed':89,'first_palindrome_time':24,'orbit':orbit,
        'q_safe_nonclosed_source':folded(orbit[22]),
        'q_bad_target':folded(orbit[23]),'palindrome_output':orbit[24],
        'scope':'For each r<=22, q(T^22(89)) belongs to S_r minus B but its image belongs to B. S_r minus B alone is not forward invariant at those depths.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='orbit'}))
