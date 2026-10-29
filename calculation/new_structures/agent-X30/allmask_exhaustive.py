"""Exhaust all 2^(Q//2) bit masks for Q=2..26; decimal arithmetic only."""
def step(s):
    n=len(s);c=0;out=['0']*n
    for i in range(n-1,-1,-1):
        z=ord(s[i])+ord(s[n-1-i])-96+c
        out[i]=str(z%10);c=z//10
    return ('1' if c else '')+''.join(out)

def create(q,mask):
    blocks=['5346']*q
    for a in range(q//2):
        if mask>>a&1:
            blocks[a]='2497'
            blocks[q-1-a]='4739'
    return ''.join(blocks)

def main():
    total=0
    for q in range(2,27):
        x='5346'*q;x1=step(x);x2=step(x1)
        for mask in range(1<<(q//2)):
            y=create(q,mask)
            assert y[0]!=y[-1],(q,mask,'t0')
            y1=step(y)
            assert y1[1]!=y1[-2],(q,mask,'t1')
            assert (y1==x1)==(mask==0),(q,mask,'first')
            assert step(y1)==x2,(q,mask,'second')
            total+=1
    print('PASS all subsets Q=2..26:',total,'seeds; first two nonpal; exact second-step merger')
if __name__=='__main__':
    main()
