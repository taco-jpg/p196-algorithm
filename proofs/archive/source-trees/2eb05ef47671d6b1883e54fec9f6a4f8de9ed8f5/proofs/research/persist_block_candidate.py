"""Independent ordinary-integer tests of the newly found exterior connector.
No finite test in this file is a proof of an infinite family.
"""
import json
from pathlib import Path

PERIODS = [1,1,4,5]
SCHEDULE = [1,1,0,0,0,1,0,0,0,0,1]
records = json.loads(Path('persist_block_neutral_timechange_results.json').read_text())
record = next(row for row in records if row['periods'] == PERIODS)
PATH = record['accepted'][0]['path']
LEFT = ''.join(str(a) for a,b in PATH)
RIGHT = ''.join(str(b) for a,b in reversed(PATH))

def numeral(center, gap):
    return LEFT + '9'*gap + center + '0'*gap + RIGHT

def trace(center, gap):
    s = numeral(center,gap)
    history, growths = [s], []
    for _ in SCHEDULE:
        t = str(int(s)+int(s[::-1]))
        growths.append(len(t)-len(s))
        history.append(t)
        s = t
    expected = numeral(center,gap+2)
    prefix, suffix = LEFT+'9'*(gap+2), '0'*(gap+2)+RIGHT
    return dict(center=center,gap=gap,clock=growths,exact_clock=growths==SCHEDULE,
        return_identity=s==expected,exterior_match=s.startswith(prefix) and s.endswith(suffix),
        final=s,expected=expected,history=history)

if __name__ == '__main__':
    from itertools import product
    records=[]
    counts={'tested':0,'clock':0,'exterior':0,'return':0}
    for length in range(5):
        for digits in product('0123456789',repeat=length):
            center=''.join(digits)
            row=trace(center,8)
            counts['tested']+=1
            counts['clock']+=row['exact_clock']
            counts['exterior']+=row['exterior_match']
            counts['return']+=row['return_identity']
            if row['exterior_match'] or row['return_identity']:
                records.append(row)
    out=dict(left=LEFT,right=RIGHT,path=PATH,counts=counts,records=records)
    Path('persist_block_candidate_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({'left':LEFT,'right':RIGHT,'counts':counts,
        'examples':[{k:v for k,v in r.items() if k!='history'}for r in records[:3]]}),flush=True)
