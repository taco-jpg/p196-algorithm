// B-system census: all cycles of the autonomous B-map (e2 forced = 1-e1) on coefficient lists of length 0..nmax.
// usage: bcensus b nmax [verbose]     memory ~ 4 bytes * sum_n (2b-1)^n + 1 byte per state
// B-map (exact mirror of nextB/trim with e2 := 1-e1):  see bsys.py
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <map>
#include <string>
#include <algorithm>
using namespace std;
typedef uint64_t u64; typedef uint32_t u32;
int b, nmax; u64 W; // W = 2b-1
vector<u64> off; // off[n] = start index of length n
static inline u64 encode(const int*B,int n){u64 x=0;for(int i=n-1;i>=0;i--)x=x*W+B[i];return off[n]+x;}
// returns successor index or UINT64_MAX (dead / out of window). also e1,gam,u
const u64 NONE=~0ULL;
u64 succ(const int*B,int n,int&e1,int&gam,int&u){
  int DB[64],DR[64],c=0;
  for(int i=0;i<n;i++){int v=B[i]+c;DB[i]=v%b;c=v/b;} e1=c;
  int e2=1-e1; c=e2;
  for(int i=0;i<n;i++){int v=B[n-1-i]+c;DR[i]=v%b;c=v/b;} gam=c;
  int nb[66];int m;
  if(gam==0){m=n;for(int k=0;k<n;k++)nb[k]=DB[k]+DR[n-1-k];}
  else{m=n+1;int xd=(b-1)*(1-e1);for(int k=0;k<=n;k++){int f=(k<n)?DB[k]:xd;int s=(k==0)?1:DR[n-k];nb[k]=f+s;}}
  u=0;while(m>0&&nb[m-1]==b-1){m--;u++;}
  if(m>0&&nb[0]==0)return NONE;
  if(m>nmax)return NONE;
  return encode(nb,m);
}
void decode(u64 idx,int*B,int&n){n=0;while(n+1<=nmax&&idx>=off[n+1])n++;u64 x=idx-off[n];for(int i=0;i<n;i++){B[i]=x%W;x/=W;}}
int main(int argc,char**argv){
  b=atoi(argv[1]);nmax=atoi(argv[2]);bool verbose=argc>3;W=2*b-1;
  off.assign(nmax+2,0);u64 p=1;for(int n=0;n<=nmax;n++){off[n]=(n?off[n-1]+p/ W:0);} // recompute properly below
  off[0]=0;u64 pw=1;for(int n=0;n<=nmax;n++){off[n+1]=off[n]+pw;pw*=W;}
  u64 S=off[nmax+1];
  fprintf(stderr,"states %llu\n",(unsigned long long)S);
  vector<u32> nx(S);
  for(int n=0;n<=nmax;n++){
    vector<int>B(n+1,0);
    u64 cnt=off[n+1]-off[n];
    for(u64 x=0;x<cnt;x++){
      u64 y=x;for(int i=0;i<n;i++){B[i]=y%W;y/=W;}
      u64 id=off[n]+x;
      if(n>0&&B[0]==0){nx[id]=UINT32_MAX;continue;}
      int e1,g,u;u64 s=succ(B.data(),n,e1,g,u);
      nx[id]=(s==NONE)?UINT32_MAX:(u32)s;
    }
  }
  vector<uint8_t> col(S,0);
  map<string,long> streams; long ncyc=0;
  for(u64 s0=0;s0<S;s0++){
    if(col[s0])continue;
    vector<u32> path;u64 cur=s0;
    while(cur!=UINT32_MAX&&col[cur]==0){col[cur]=1;path.push_back(cur);cur=nx[cur];}
    if(cur!=UINT32_MAX&&col[cur]==1){
      size_t i=find(path.begin(),path.end(),(u32)cur)-path.begin();
      // cycle path[i..]
      vector<u32> cyc(path.begin()+i,path.end());
      int B[64],n;string es,gs,us,ns;
      for(u32 st:cyc){decode(st,B,n);int e1,g,u;succ(B,n,e1,g,u);es+=char('0'+e1);gs+=char('0'+g);us+=char('0'+u);ns+=to_string(n)+",";}
      // canonical rotation (by joint string)
      string joint;size_t L=cyc.size();size_t best=0;string bj;
      for(size_t r=0;r<L;r++){string j;for(size_t k=0;k<L;k++){size_t q=(r+k)%L;j+=es[q];j+=gs[q];j+=us[q];}if(r==0||j<bj){bj=j;best=r;}}
      string e2s,g2s,u2s;for(size_t k=0;k<L;k++){size_t q=(best+k)%L;e2s+=es[q];g2s+=gs[q];u2s+=us[q];}
      bool minimal=true; // count cycle once: only when smallest state id is first element
      u32 mn=*min_element(cyc.begin(),cyc.end());
      ncyc++;
      string key="p"+to_string(L)+" e="+e2s+" g="+g2s+" u="+u2s;
      streams[key]++;
      if(verbose){decode(cyc[best],B,n);printf("CYCLE %s start n=%d B=[",key.c_str(),n);for(int i=0;i<n;i++)printf("%d%s",B[i],i+1<n?",":"");printf("] lens=%s\n",ns.c_str());}
    }
    for(u32 x:path)col[x]=2;
  }
  printf("base %d nmax %d: %ld cycles\n",b,nmax,ncyc);
  for(auto&kv:streams)printf("  %ld x %s\n",kv.second,kv.first.c_str());
}
