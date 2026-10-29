"""Two-ended sound 0/1-carry abstraction of symmetric decimal pairwords."""
B=[10,4,7,5,13,6,11,1,9,16,16,18,10,9,4,8,1,7,0,2,15,15,9,7,7,10,17,14,18,8,6,6,18,4]
W=[8,1,15,4,0,5,5,18,4]
def step_hypothesis(prefix,incoming_upper_carry):
    low=[];carry=0
    for x in prefix:
        z=x+carry;low.append(z%10);carry=z//10
    upper=[];carry=incoming_upper_carry
    for x in prefix[::-1]:
        z=x+carry;upper.append(z%10);carry=z//10
    gamma=carry
    upper=upper[::-1]
    if gamma:
        return tuple(low[i]+(1 if i==0 else upper[i-1]) for i in range(len(prefix))),gamma
    return tuple(low[i]+upper[i] for i in range(len(prefix))),gamma
def common_prefix(x,y):
    for i,(a,b) in enumerate(zip(x,y)):
        if a!=b:return i
    return min(len(x),len(y))
def certified_prefix(prefix,steps=120):
    prefix=tuple(prefix);ambiguous=0
    for _ in range(steps):
        a,ga=step_hypothesis(prefix,0)
        b,gb=step_hypothesis(prefix,1)
        ambiguous+=(ga!=gb)
        prefix=a[:common_prefix(a,b)]
        if not prefix:break
    return prefix,ambiguous
