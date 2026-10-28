// count counter-realizable cyclic gam words (necklaces) per length p, base b.  DFS with prefix sharing.
#include <bits/stdc++.h>
using namespace std;
int b,n; unsigned long long T[2][70]; // T[s][x] = mask of successors (x in 1..2b-2 -> bit x)
int emit=0; int P; unsigned long long cntWords, cntNeck; map<int,long long> byG;
bool isNecklaceMin(unsigned long long w,int p){ // w bit t = symbol at time t ; check minimal rotation
  unsigned long long full=(p==64)?~0ULL:((1ULL<<p)-1);
  for(int r=1;r<p;r++){ unsigned long long rot=((w>>r)|(w<<(p-r)))&full; if(rot<w) return false; } return true; }
void dfs(int t,unsigned long long w,vector<unsigned long long>&cur){
  if(t==P){
    bool ok=false; for(int x=1;x<=n;x++) if(cur[x]&(1ULL<<x)) {ok=true;break;}
    if(!ok) return;
    cntWords++;
    if(isNecklaceMin(w,P)){ cntNeck++; byG[__builtin_popcountll(w)]++; if(emit){ printf("%d %d ",P,__builtin_popcountll(w)); for(int t=0;t<P;t++) putchar('0'+((w>>t)&1)); putchar('\n'); } }
    return; }
  for(int s=0;s<2;s++){
    vector<unsigned long long> nx(n+1,0); bool any=false;
    for(int x0=1;x0<=n;x0++){ unsigned long long m=cur[x0],r=0; while(m){int x=__builtin_ctzll(m); m&=m-1; r|=T[s][x];} nx[x0]=r; if(r) any=true; }
    if(any) dfs(t+1,w|((unsigned long long)s<<t),nx);
  }
}
int main(int argc,char**argv){
  b=atoi(argv[1]); int pmin=atoi(argv[2]),pmax=atoi(argv[3]); n=2*b-2; if(argc>4) emit=1;
  for(int x=1;x<=n;x++){ T[0][x]=T[1][x]=0;
    for(int k=0;k<2;k++){ if(x+k<=b-1){ int nx=2*x+k; if(nx<=n) T[0][x]|=1ULL<<nx; } else if(x+k>=b){ T[1][x]|=1ULL<<((x%b)+1); } } }
  for(P=pmin;P<=pmax;P++){
    cntWords=cntNeck=0; byG.clear();
    vector<unsigned long long> cur(n+1,0); for(int x=1;x<=n;x++) cur[x]=1ULL<<x;
    dfs(0,0,cur);
    if(!emit) printf("p=%d realizable words %llu necklaces %llu  byG:",P,cntWords,cntNeck); for(auto&kv:byG) printf(" %d:%lld",kv.first,kv.second); printf("\n"); fflush(stdout);
  }
}
