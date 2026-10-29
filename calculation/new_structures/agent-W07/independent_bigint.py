#!/usr/bin/env python3
"""Independent ordinary Python-bigint reversal, plus 20k FINAL-target inverse."""
import sys
sys.set_int_max_str_digits(0)
from reverse_fibre import inverse_pairword, fibre_count
B=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W=[17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]
def seed(q,toggle):
    p=B+W*q;lo=[];hi=[]
    for i,c in enumerate(p):
        x=min(c,9)
        if toggle and i>=len(B) and c==1:x=0
        lo.append(x);hi.append(c-x)
    return int(''.join(map(str,hi))+''.join(map(str,lo[::-1])))
def main():
    q=300;a=seed(q,False);b=seed(q,True)
    assert a!=b
    def r(x):return x+int(str(x)[::-1])
    target=r(a)
    assert target==r(b)
    p=inverse_pairword(str(target),len(str(a)))
    expected=B+W*q
    assert p==expected+expected[::-1]
    assert fibre_count(p)>2**600
    for t in range(401):
        s=str(a)
        assert s!=s[::-1],('palindrome',t)
        a=r(a)
    if len(sys.argv)>1:
        with open(sys.argv[1]) as f:
            final=f.readline().strip()
            expected_hash=int(f.readline())
            previous_len=int(f.readline())
        previous=inverse_pairword(final,previous_len)
        assert previous is not None
        h=1469598103934665603
        for x in previous:
            h=((h^(x+1))*1099511628211)&((1<<64)-1)
        assert h==expected_hash
        print('W07_BACKWARD_FROM_STEP_20000_PASS target_len',
              len(final),'decoded_predecessor_len',len(previous))
    print('W07_BIGINT_400_PASS q=300 length',
          len(str(a)),'inverse pairword length',len(p))
if __name__=='__main__':main()
