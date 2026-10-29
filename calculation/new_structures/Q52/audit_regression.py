#!/usr/bin/env python3
"""Q52 independent big-integer replay and one-digit carry-terminal oracle.

python3 calculation/new_structures/Q52/audit_regression.py
Does not import the N08 transducer or its C++ replay.
"""
import sys
sys.set_int_max_str_digits(0)

def check_one_digit():
    count=0
    for b in range(2,101):
        for d in range(1,b):
            p=2*d
            n=p
            digits=[]
            while n:
                n,r=divmod(n,b)
                digits.append(r)
            pair=[digits[i]+digits[-1-i] for i in range(len(digits))]
            actual=(tuple(pair[:len(pair)//2]),pair[len(pair)//2] if len(pair)%2 else None)
            expected=((p-b+1,),None) if p>=b else ((),2*p)
            assert actual==expected,(b,d,actual,expected)
            count+=1
    print('ONE_DIGIT_TERMINAL_PASS',count)

def check_decimal():
    n=196
    evenonly=[]
    overflows=0
    for step in range(20000):
        s=str(n)
        assert s!=s[::-1],('PALINDROME',step)
        if not any((int(a)+int(b))%2 for a,b in zip(s,s[::-1])):
            evenonly.append(step)
        nxt=n+int(s[::-1])
        overflows+=len(str(nxt))>len(s)
        n=nxt
    assert len(str(n))==8296
    assert overflows==8293
    assert evenonly==[8,13,19],evenonly
    print('N08_DECIMAL_ORACLE_PASS',{'steps':20000,'final_length':8296,'overflows':8293,'evenonly':evenonly})

if __name__=='__main__':
    check_one_digit()
    check_decimal()
