"""Exact arbitrary-block seam law: deterministic complete controls.

The all-input proof is SEAM_RESPONSE.md. No recurrence search is performed.
Every finite control input and its response data is retained in a compressed
canonical JSON stream; bounded checks are not an all-time claim.
"""
from __future__ import annotations
import gzip,hashlib,itertools,json,random,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'main_existence_attempt/correlation_pass/constructive'))
from seam_overlap import canonical,literal_step,realize


def normal(word,carry=0):
 digits=[];outgoing=[]
 for x in word:
  x+=carry;digits.append(x%10);carry=x//10;outgoing.append(carry)
 return tuple(digits),carry,tuple(outgoing)

def integer_digits(word,width):
 value=sum(x*10**i for i,x in enumerate(word))
 digits=tuple(map(int,str(value)[::-1]))
 assert len(digits)<=width
 return digits+(0,)*(width-len(digits))

def pair(d):return tuple(x+y for x,y in zip(d,d[::-1]))

def plus_shifted(target,word,shift):
 for i,x in enumerate(word):target[shift+i]+=x

def run9(w):
 return next((i for i,x in enumerate(w) if x!=9),len(w))

def check(words,label):
 assert words and all(w and all(0<=x<=18 for x in w) for w in words)
 length=sum(map(len,words));whole=tuple(itertools.chain.from_iterable(words))
 E=[0]*(length+1);K=[0]*length;isolated_carries=[0]*length
 carry=0;start=0;records=[]
 for word in words:
  d,h,c0=normal(word);dc,hc,cc=normal(word,carry)
  ell=run9(word);all9=int(ell==len(word))
  assert hc==h+all9*carry and h*all9==0
  assert tuple(a-b for a,b in zip(cc,c0))==tuple(carry*int(i<ell) for i in range(len(word)))
  plus_shifted(E,d+(h,),start)
  plus_shifted(K,(carry,)*ell,start)
  plus_shifted(isolated_carries,c0,start)
  records.append({'start':start,'incoming':carry,'isolated_final':h,'run9':ell,'all9':all9})
  carry=hc;start+=len(word)
 gamma=carry;width=length+gamma
 if not gamma:assert E.pop()==0
 actual_d,actual_h,actual_c=normal(whole)
 assert actual_h==gamma
 assert tuple(a-b for a,b in zip(actual_c,isolated_carries))==tuple(K)
 correction=[0]*(length+1)
 for i,k in enumerate(K):correction[i]-=10*k;correction[i+1]+=k
 if not gamma:assert correction.pop()==0
 predicted=tuple(e+h for e,h in zip(E,correction))
 actual=integer_digits(whole,width)
 assert predicted==actual==actual_d+((1,) if gamma else ())
 actual_pair=pair(actual);R=pair(E);pair_correction=pair(correction)
 assert actual_pair==tuple(x+y for x,y in zip(R,pair_correction))
 independent_mass=sum(sum(pair(normal(w)[0]+((1,) if normal(w)[1] else ()))) for w in words)
 assert sum(actual_pair)==independent_mass-18*sum(K)
 assert (actual_pair==R)==(not any(K))
 if tuple(E)==tuple(E[::-1]) and any(K):assert actual!=actual[::-1]
 is_canonical=canonical(whole)
 if is_canonical:assert literal_step(whole)==actual_pair
 if words==words[::-1] and all(w==w[::-1] for w in words):
  # Check common-clock reflection placement, including local exponent -1.
  local_sum={};start=0
  for word in words:
   d,h,_=normal(word);ew=d+((1,) if h else ())
   for i,x in enumerate(ew):
    local_sum[start+i]=local_sum.get(start+i,0)+x
    pos=start+len(word)+gamma-1-i
    local_sum[pos]=local_sum.get(pos,0)+x
   start+=len(word)
  assert all(v==0 for p,v in local_sum.items() if not 0<=p<width)
  assert tuple(local_sum.get(i,0) for i in range(width))==R
 return {'label':label,'words':words,'blocks':records,'gamma':gamma,
         'carry_mask':K,'actual_digits':actual,'mass_loss':18*sum(K),
         'canonical_whole':is_canonical,'raw_symmetric':E==E[::-1]}


def canonical_random(rng):
 if rng.randrange(4)==0:return (9,)*(2*rng.randrange(1,7))
 length=rng.randrange(1,13)
 if length==1:return (2*rng.randrange(1,10),)
 left=[rng.randrange(19) for _ in range(length//2)];left[0]=rng.randrange(1,19)
 center=[2*rng.randrange(10)] if length%2 else []
 return tuple(left+center+left[::-1])


def main():
 records=[]
 atoms=[(2*p,) for p in range(1,10)]+[(p,p) for p in range(1,19)]
 for b in atoms:
  for h in atoms:records.append(check([b,h,b],'exhaustive_three_block'))
 rng=random.Random(19691014)
 for _ in range(1000):
  words=[]
  for _ in range(rng.randrange(1,8)):
   n=rng.randrange(1,13)
   words.append((9,)*n if rng.randrange(4)==0 else tuple(rng.randrange(19) for _ in range(n)))
  records.append(check(words,'arbitrary_list'))
 for _ in range(1000):
  left=[canonical_random(rng) for _ in range(rng.randrange(1,5))]
  center=[canonical_random(rng)] if rng.randrange(2) else []
  records.append(check(left+center+left[::-1],'symmetric_list'))
 for ell in (1,2,5,32,127):
  words=[(11,11),(9,)*(2*ell),(9,)*(2*ell),(2,2),(9,)*(2*ell),(9,)*(2*ell),(11,11)]
  records.append(check(words,'all9_chain'))
 examples=[check([(9,9),(18,),(9,9)],'outer_all9_terminal_change'),
           check([(10,10),(2,),(10,10)],'mixed_clock_alignment'),
           check([(2,2),(18,),(2,2)],'interior_left_extension')]
 records+=examples
 encoded=json.dumps(records,sort_keys=True,separators=(',',':')).encode()
 archive=HERE/'seam_response_cases.json.gz';archive.write_bytes(gzip.compress(encoded,mtime=0))
 assert gzip.decompress(archive.read_bytes())==encoded
 classes={kind:sum(r['label']==kind for r in records) for kind in sorted({r['label'] for r in records})}
 result={'status':'all exact seam-law controls PASS; no recurrence search or all-time claim',
         'seed':19691014,'total_cases':len(records),'classes':classes,
         'canonical_ordinary_integer_controls':sum(r['canonical_whole'] for r in records),
         'nonzero_correction_cases':sum(any(r['carry_mask']) for r in records),
         'raw_symmetric_nonzero_correction_cases':sum(r['raw_symmetric'] and any(r['carry_mask']) for r in records),
         'full_record_archive':archive.name,'full_record_bytes':len(encoded),
         'compressed_bytes':archive.stat().st_size,'full_record_sha256':hashlib.sha256(encoded).hexdigest(),
         'examples':examples}
 (HERE/'seam_response.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))

if __name__=='__main__':main()
