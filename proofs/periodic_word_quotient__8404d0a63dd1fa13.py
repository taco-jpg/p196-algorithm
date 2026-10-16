"""Actual finite symmetric words with a variable repeated four-symbol block.

State (B,H,w) means B w^k H reverse(w)^k reverse(B), k>=3. Whole-word
normalization computes every carry, including the clock. Guard periods and
the idempotent period carry map give an exact all-k transition. Finite
controls check the implementation; METHOD_AND_PROOF gives the identity.
"""
from pathlib import Path
from collections import Counter
import gzip,hashlib,json

ROOT=Path(__file__).parent
CONTROLS=(3,4,7,31)
CAPS=dict(graph_states=50000,path_steps=128,total_interface_width=512)


def full(s,k):
    b,h,w=s
    return b+w*k+h+w[::-1]*k+b[::-1]


def image(q):
    carry=0;digits=[]
    for x in q:
        carry,digit=divmod(x+carry,10);digits.append(digit)
    if carry:digits.append(carry)
    return tuple(a+b for a,b in zip(digits,digits[::-1])),carry


def valid(s):
    b,h,w=s
    return (len(w)==4 and all(0<=q<=18 for q in b+h+w)
            and h==h[::-1] and (len(h)%2==0 or h[len(h)//2]%2==0)
            and (b[0]>0 if b else w[0]>0))


def safe(s):
    b,h,w=s;alphabet=set(b+h+w);outside=b[0] if b else w[0]
    return not (max(alphabet)<=9 or (outside==11 and alphabet<={0,11}))


def transition(s):
    assert valid(s) and safe(s)
    b,h,w=s;out,gamma=image(full(s,3));nb=len(b)+4;nh=len(h)+8+gamma
    rb=out[:nb];rw=out[nb:nb+4];rh=out[nb+4:nb+4+nh]
    assert out==full((rb,rh,rw),1)
    for k in CONTROLS:
        outk,gammak=image(full(s,k))
        assert gammak==gamma and outk==full((rb,rh,rw),k-2)
    u=v=0
    while len(rb)>=4 and rb[-4:]==rw:rb=rb[:-4];u+=1
    while len(rh)>=8 and rh[:4]==rw and rh[-4:]==rw[::-1]:rh=rh[4:-4];v+=1
    target=(rb,rh,rw);delta=u+v-2
    assert valid(target)
    for k in CONTROLS:
        assert image(full(s,k))[0]==full(target,k+delta)
    assert 2*len(rb)+len(rh)+8*delta==2*len(b)+len(h)+gamma
    return dict(kind='edge' if safe(target) else 'unsafe_target',target=target,
                clock=gamma,exponent_delta=delta,absorbed_outer_periods=u,absorbed_center_pairs=v)


def main():
    phase=(0,9,18,9)
    initials=[((17,),h,phase) for h in [()]+[(c,) for c in range(0,19,2)]]
    graph={};paths=[];cycles=[]
    for initial in initials:
        state=initial;seen={};path=[];running=minimum=0
        while True:
            if state in seen:
                loop=path[seen[state]:];gain=sum(graph[s]['exponent_delta'] for s in loop)
                overflows=sum(graph[s]['clock'] for s in loop)
                assert 8*gain==overflows
                cycles.append(dict(initial=initial,loop=loop,exponent_gain=gain,overflows=overflows));status='CYCLE';break
            if len(path)>=CAPS['path_steps'] or len(state[0])+len(state[1])>CAPS['total_interface_width']:
                status='UNKNOWN_INTERFACE_OR_PATH_CAP';break
            if not safe(state):status='unsafe_initial';break
            if state not in graph:
                if len(graph)>=CAPS['graph_states']:status='UNKNOWN_GRAPH_CAP';break
                graph[state]=transition(state)
            seen[state]=len(path);path.append(state);r=graph[state]
            running+=r['exponent_delta'];minimum=min(minimum,running)
            if r['kind']!='edge':status=r['kind'];state=r['target'];break
            state=r['target']
        paths.append(dict(initial=initial,status=status,states=path,final_state=state,
                          exponent_floor_for_recorded_path=3-minimum))
    payload=json.dumps(dict(initials=initials,graph=[dict(state=s,**r) for s,r in sorted(graph.items())],paths=paths,cycles=cycles),
                       separators=(',',':'),sort_keys=True).encode()
    (ROOT/'periodic_word_quotient_controls.json.gz').write_bytes(gzip.compress(payload,mtime=0))
    out=dict(initial_outer=[17],initial_bulk=phase,initial_centers='empty or one even coefficient0..18',
             initial_states=len(initials),graph_states=len(graph),transition_counts=dict(Counter(r['kind'] for r in graph.values())),
             path_status_counts=dict(Counter(p['status'] for p in paths)),cycles=cycles,caps=CAPS,
             maximum_path_steps=max(len(p['states']) for p in paths),
             maximum_exponent_floor=max(p['exponent_floor_for_recorded_path'] for p in paths),
             largest_interfaces=[max(len(s[j]) for s in graph) for j in (0,1)],
             payload_sha256=hashlib.sha256(payload).hexdigest(),
             scope='Actual whole-word symbolic quotient; incomplete interface paths remain UNKNOWN',
             infinite_existence_proved=False)
    (ROOT/'periodic_word_quotient_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
