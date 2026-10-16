"""Independent exact support of canonical decimal palindromes modulo M.

The computation enumerates residues, not integers. Each transition chooses
an actual mirrored digit pair (or the single middle digit), so the output
is the exact set at a given length. Finite results do not prove stabilization.
"""
import argparse
import json
import math
from pathlib import Path


def rotate(bits, shift, modulus):
    shift %= modulus
    mask = (1 << modulus) - 1
    return ((bits << shift) | (bits >> (modulus-shift))) & mask


def palindrome_support(modulus, length):
    powers = [pow(10,i,modulus) for i in range(length)]
    if length == 1:
        return sum(1 << r for r in {d % modulus for d in range(1,10)})
    leading_weight = (powers[0]+powers[-1]) % modulus
    bits = 0
    for d in range(1,10): bits |= 1 << (d*leading_weight % modulus)
    for i in range(1,(length+1)//2):
        j=length-1-i
        weight = powers[i] if i==j else (powers[i]+powers[j]) % modulus
        new = 0
        for d in range(10): new |= rotate(bits,d*weight,modulus)
        bits = new
    return bits


def predicted_support(modulus, length):
    # A residue class contains a positive number with nonzero final digit
    # unless 10|M and the residue itself ends in0. Even-length palindromes
    # impose the additional necessary divisibility by gcd(M,11).
    return sum(1 << r for r in range(modulus)
               if not (modulus % 10 == 0 and r % 10 == 0)
               and (length % 2 or r % math.gcd(modulus,11) == 0))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--max-modulus',type=int,default=300)
    ap.add_argument('--max-length',type=int,default=80);args=ap.parse_args()
    result=[]
    for modulus in range(1,args.max_modulus+1):
        misses=[]
        for length in range(1,args.max_length+1):
            got=palindrome_support(modulus,length)
            allowed=predicted_support(modulus,length)
            assert got & ~allowed == 0,(modulus,length)
            if got!=allowed:misses.append(length)
        result.append({'modulus':modulus,
                       'last_unsaturated_tested_length':max(misses,default=0),
                       'tested_through_length':args.max_length})
    out={'scope':'Exact finite supports only; no extrapolation past tested lengths.',
         'moduli':args.max_modulus,'lengths_per_modulus':args.max_length,
         'records':result}
    Path('astra_root_palindrome_dp_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'moduli':args.max_modulus,'lengths_per_modulus':args.max_length,
                      'largest_last_missing_length':max(r['last_unsaturated_tested_length'] for r in result),
                      'unsaturated_at_final_length':[r['modulus'] for r in result if r['last_unsaturated_tested_length']==args.max_length]}))


if __name__=='__main__':main()
