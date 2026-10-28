// E2 p16 g=(01)^8, exact 16-step row map on ALL base10 4-cell rows.
// Local full functional-graph enumeration, uses precise carry recurrence.
#include <array>
#include <vector>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
using namespace std;
static constexpr int B=10,M=4,P=16,SIZE=19*19*19*19;
using Row=array<unsigned char,M>;
static inline bool phi(const Row&v,int gam,Row&out){
 int i0=-1;for(int i=0;i<M;i++)if(v[i]!=9){i0=i;break;}
 if(i0<0)return false;
 int A[M]={},D[M]={},e[M],f[M];
 A[(i0+1)%M]=v[i0]>=B;
 for(int j=1;j<M;j++){int i=(i0+j)%M;A[(i+1)%M]=(v[i]+A[i])/B;}
 D[(i0+M-1)%M]=v[i0]>=B;
 for(int j=1;j<M;j++){int i=(i0+M-j)%M;D[(i+M-1)%M]=(v[i]+D[i])/B;}
 for(int i=0;i<M;i++){e[i]=(v[i]+A[i])%B;f[i]=(v[i]+D[i])%B;}
 for(int i=0;i<M;i++)out[i]=e[i]+(gam?f[(i+M-1)%M]:f[i]);
 return true;
}
static Row decode(int s){Row r{};for(int i=0;i<M;i++){r[i]=s%19;s/=19;}return r;}
static int encode(const Row&r){int s=0;for(int i=M-1;i>=0;i--)s=s*19+r[i];return s;}
static bool mirror(const Row&r){for(int al=0;al<M;al++){bool ok=true;for(int i=0;i<M;i++)if(r[i]!=r[(al+M-i)%M]){ok=false;break;}if(ok)return true;}return false;}
static bool primitive(const Row&r){for(int d: {1,2}){bool same=true;for(int i=0;i<M;i++)if(r[i]!=r[(i+d)%M]){same=false;break;}if(same)return false;}return true;}
int main(){
 vector<int> next(SIZE,-1);
 int good=0,dead=0;
 for(int v=0;v<SIZE;v++){
  Row cur=decode(v),nxt;bool ok=true;
  for(int t=0;t<P;t++){if(!phi(cur,t&1,nxt)){ok=false;break;}cur=nxt;}
  if(ok){next[v]=encode(cur);good++;}else dead++;
 }
 vector<unsigned char>status(SIZE,0);vector<int>pos(SIZE,-1),path;
 int ncycles=0, cycstates=0, selfmirCycles=0, primSelfmirCycles=0, longerCycles=0,maxlen=0;
 for(int s=0;s<SIZE;s++){
  if(status[s])continue;
  path.clear();int cur=s;
  while(cur>=0 && status[cur]==0){status[cur]=1;pos[cur]=path.size();path.push_back(cur);cur=next[cur];}
  if(cur>=0 && status[cur]==1 && pos[cur]>=0){
   int begin=pos[cur],len=path.size()-begin;
   ncycles++;cycstates+=len;if(len>maxlen)maxlen=len;
   bool anyMirror=false, anyPrimMirror=false, everyPrim=true, everyMirror=true;
   for(int i=begin;i<(int)path.size();i++){
    Row r=decode(path[i]);bool mi=mirror(r),pr=primitive(r);
    anyMirror|=mi;anyPrimMirror|=(mi&&pr);everyPrim&=pr;everyMirror&=mi;
   }
   if(anyMirror)selfmirCycles++;
   if(anyPrimMirror){primSelfmirCycles++;if(len>1)longerCycles++;}
   printf("CYCLE len=%d selfmirror=%d primitive_selfmirror=%d every_mirror=%d every_primitive=%d seed=%d\n",len,(int)anyMirror,(int)anyPrimMirror,(int)everyMirror,(int)everyPrim,path[begin]);
  }
  for(int v:path){status[v]=2;pos[v]=-1;}
 }
 printf("COMPLETE states=%d valid=%d dead=%d cycles=%d cyclic_states=%d max_cycle_blocks=%d mirrored_cycles=%d primitive_mirror_cycles=%d primitive_mirror_longer=%d\n",SIZE,good,dead,ncycles,cycstates,maxlen,selfmirCycles,primSelfmirCycles,longerCycles);
}
