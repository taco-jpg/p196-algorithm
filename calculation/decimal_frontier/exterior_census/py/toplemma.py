import sys,re
sys.path.insert(0,'/home/claude/research/w5_exterior/py')
from verify_ext import run_bx, parse, Bstep
for b,g in [(10,'11100010000'),(10,'100010001000'),(11,'001'),(11,'001001'),(17,'100001'),(26,'01'),(20,'00010001'),(4,'100'),(8,'1000')]:
    out=run_bx(b,g,['-first']); res,wit=parse(out)
    if not wit: print(b,g,'no wit'); continue
    L=[len(B) for B in wit]; mx=max(L)
    ok=all(L[t]<mx for t in range(len(g)) if g[t]=='1')
    # also, which times have max length
    print(b,g,'lengths',L,'max',mx,' overflow times have length<max:',ok, ' max-length times g:',[g[t] for t in range(len(g)) if L[t]==mx])
