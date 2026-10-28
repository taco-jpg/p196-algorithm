import re,sys
def parse_bw(line):
    m=re.search(r"ACCEPT b=(\d+) p=(\d+) g=(\d+) e=(\d+)",line)
    b,p,g,e=int(m[1]),int(m[2]),m[3],m[4]
    Bs=[[int(x) for x in s.split(',')] if s else [] for s in re.findall(r"\[([^\]]*)\]",line[line.index('B_t='):])]
    return b,p,g,e,Bs
if __name__=="__main__":
    sys.path.insert(0,'..')
    import lib
    for line in open(sys.argv[1]):
        if 'ACCEPT' not in line: continue
        b,p,g,e,Bs=parse_bw(line)
        print(b,p,g,e,[len(x) for x in Bs])
        for t in range(p):
            nb,e1,gm,u=lib.Bstep(b,Bs[t])
            ok = nb==Bs[(t+1)%p]
            print(t,"e1",e1,"gam",gm,"u",u,"next matches:",ok, "len",len(Bs[t]))
