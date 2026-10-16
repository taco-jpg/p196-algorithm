"""Emit the explicit three-step affine inverse ladder (no search)."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
TAILS = HERE.parent/'tails'


def fixed(value, length=1):
    return [value, [0], length]


def variable(value, constant):
    return [value, [1], constant]


def mirror(prefix, center=None):
    return prefix + ([] if center is None else [fixed(center)]) + prefix[::-1]


prefixes = {
    'A': [fixed(2),fixed(12),fixed(4,2),variable(9,1),fixed(14),fixed(16,2),fixed(15)],
    'B': [fixed(5),fixed(4),variable(9,4),fixed(14,2),fixed(12)],
    'C': [fixed(10),variable(9,6),fixed(10),fixed(6)],
    'Q': [fixed(1,2),variable(0,5),fixed(1),fixed(7)],
}
certificate = dict(
    status='EXPLICIT_ALL_PARAMETER_INVERSE_LADDER',
    parameter='r = 6+k, every integer k>=0; r=5 checked separately',
    folded_formulas={
        'A':'(2,12,4,4,9^(r-5),14,16,16,15), no center',
        'B':'(5,4,9^(r-2),14,14,12), no center',
        'C':'(10,9^r,10,6), no center',
        'Q':'(1,1,0^(r-1),1,7), center 12'},
    full_pair_words={name:mirror(p,12 if name=='Q' else None) for name,p in prefixes.items()},
    transitions=[['A','B'],['B','C'],['C','Q']],
    safety_pairs={'A':16,'B':14,'C':10,'Q':12},
    first_positive_palindrome_times={'A':14,'B':13,'C':12,'Q':11},
    tail_certificate_path='../tails/symbolic_tail_certificates.json',
    tail_certificate_sha256=hashlib.sha256((TAILS/'symbolic_tail_certificates.json').read_bytes()).hexdigest(),
    finite_excision_target='F10 = S2 intersect first eleven outputs nonpalindromic',
    arbitrary_finite_symmetric_difference_remains_not_closed=True,
    positive_invariant_found=False)
(HERE/'inverse_ladder_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
print(json.dumps({k:v for k,v in certificate.items() if k!='full_pair_words'},indent=2))
