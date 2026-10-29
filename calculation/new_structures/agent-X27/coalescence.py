#!/usr/bin/env python3
"""Exact integer control: seven seeds with pairword (7,18^6,7) coalesce."""
def raa(n):
    return n+int(str(n)[::-1])

def main():
    target=None
    seeds=[]
    for a in range(1,8):
        b=7-a
        seed=int(str(a)+'9'*6+str(b))
        assert len(str(seed))==8
        s=str(seed)
        assert s!=s[::-1]
        assert [int(s[i])+int(s[7-i]) for i in range(8)]==[7]+[18]*6+[7]
        next_value=raa(seed)
        assert target is None or next_value==target
        target=next_value
        seeds.append(seed)
    assert target==89999987
    print('coalescent_seeds',seeds,'common_N1',target)
    # The two other Q<3 members of the b=10 and a+b=7 subfamily
    # cannot satisfy F32 through 20000 (but this makes no broader no-go claim).
    for Q in (0,1,2):
        n=int('1'+'9'*(2*Q)+'6')
        failure=None
        for t in range(32):
            s=str(n)
            if all((int(s[i])+int(s[-1-i]))%2==0 for i in range(len(s)//2)):
                failure=t;break
            n=raa(n)
        print('shorter_Q',Q,'first_parity_obstruction_loss',failure)
    print('COALESCENCE CHECK PASS')

if __name__=='__main__':main()
