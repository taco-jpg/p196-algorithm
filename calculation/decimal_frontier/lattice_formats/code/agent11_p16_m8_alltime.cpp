// Exact full all-temporal functional graph of base10 g=(01)^8 on reflection-symmetric rows.
// Axis-labelled states include duplicates, but transitions target the canonical lowest axis.
// A necessary closure check ensures every nonneutral image is also reflection-symmetric.
#include <array>
#include <vector>
#include <map>
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <algorithm>
using namespace std;
#ifndef LAT_M
#define LAT_M 8
#endif
static constexpr int M=LAT_M,B=10,PER=16;
using Row=array<unsigned char,M>;
struct Axis {int nr, reps[M], partner[M];uint64_t total,offset;};
Axis axes[M];
static uint64_t ipow(int x){uint64_t z=1;while(x--)z*=19;return z;}
static bool phi(const Row&v,int gam,Row&out){
 int i0=-1;for(int i=0;i<M;i++)if(v[i]!=9){i0=i;break;}
 if(i0<0)return false;
 int A[M]={},D[M]={},e[M],f[M];A[(i0+1)%M]=v[i0]>=B;
 for(int j=1;j<M;j++){int i=(i0+j)%M;A[(i+1)%M]=(v[i]+A[i])/B;}
 D[(i0+M-1)%M]=v[i0]>=B;
 for(int j=1;j<M;j++){int i=(i0+M-j)%M;D[(i+M-1)%M]=(v[i]+D[i])/B;}
 for(int i=0;i<M;i++){e[i]=(v[i]+A[i])%B;f[i]=(v[i]+D[i])%B;}
 for(int i=0;i<M;i++)out[i]=e[i]+(gam?f[(i+M-1)%M]:f[i]);
 return true;
}
static Row decode(int axis,uint64_t idx){Row r{};Axis&a=axes[axis];for(int j=0;j<a.nr;j++){int val=idx%19;idx/=19;r[a.reps[j]]=r[a.partner[a.reps[j]]]=val;}return r;}
static int64_t canonical(const Row&r){
 for(int a=0;a<M;a++){
  auto&ax=axes[a];bool sym=true;
  for(int j=0;j<M;j++)if(r[j]!=r[ax.partner[j]]){sym=false;break;}
  if(!sym)continue;
  uint64_t idx=0,pow=1;
  for(int j=0;j<ax.nr;j++){idx+=(uint64_t)r[ax.reps[j]]*pow;pow*=19;}
  return (int64_t)(ax.offset+idx);
 }
 return -1;
}
static bool primitive(const Row&r){for(int d=1;d<M;d++){if(M%d)continue;bool eq=true;for(int i=0;i<M;i++)if(r[i]!=r[(i+d)%M]){eq=false;break;}if(eq)return false;}return true;}
int main(int argc,char**argv){
 if(argc<2){fprintf(stderr,"usage: symgraph OUTPUT_PREFIX\n");return 2;}
 uint64_t NN=0;
 for(int a=0;a<M;a++){Axis&ax=axes[a];ax.nr=0;ax.offset=NN;
  for(int i=0;i<M;i++)ax.partner[i]=(a+M-i)%M;
  for(int i=0;i<M;i++)if(i<=ax.partner[i])ax.reps[ax.nr++]=i;
  ax.total=ipow(ax.nr);NN+=ax.total;
 }
 fprintf(stderr,"DOMAIN M=%d nodes=%llu\n",M,(unsigned long long)NN);
 vector<int32_t>next(NN,-1);uint64_t good=0,dead=0,not_symmetric=0,dup=0;
 for(int a=0;a<M;a++){
  Axis&ax=axes[a];
  for(uint64_t idx=0;idx<ax.total;idx++){
   uint64_t id=ax.offset+idx;
   Row start=decode(a,idx),cur=start,nxt;bool valid=true;
   for(int t=0;t<PER;t++)if(!phi(cur,t&1,nxt)){valid=false;break;}else cur=nxt;
   if(!valid){dead++;continue;}
   int64_t target=canonical(cur);
   if(target<0){not_symmetric++;continue;}
   next[id]=(int32_t)target;good++;
   int64_t canstart=canonical(start);if(canstart!=(int64_t)id)dup++;
  }
  fprintf(stderr,"AXIS %d complete good=%llu dead=%llu not_symmetric=%llu\n",a,(unsigned long long)good,(unsigned long long)dead,(unsigned long long)not_symmetric);
 }
 if(not_symmetric){fprintf(stderr,"ERROR domain not closed: %llu images leave symmetry\n",(unsigned long long)not_symmetric);return 5;}
 vector<unsigned char>visit(NN,0);vector<int32_t>pos(NN,-1),path;
 uint64_t cyc=0,primitiveCyc=0,cycStates=0,primitiveCycStates=0;
 map<int,uint64_t>lens,prLens;
 for(uint64_t id=0;id<NN;id++){
  if(visit[id])continue;
  path.clear();int32_t cur=(int32_t)id;
  while(cur>=0 && visit[cur]==0){visit[cur]=1;pos[cur]=path.size();path.push_back(cur);cur=next[cur];}
  if(cur>=0&&visit[cur]==1&&pos[cur]>=0){
   int sz=(int)path.size()-pos[cur];cyc++;cycStates+=sz;lens[sz]++;
   int s=path[pos[cur]],a=0;while(a<M&&s>=(int64_t)(axes[a].offset+axes[a].total))a++;
   Row r=decode(a,s-axes[a].offset);
   if(primitive(r)){primitiveCyc++;primitiveCycStates+=sz;prLens[sz]++;}
  }
  for(int k:path){visit[k]=2;pos[k]=-1;}
 }
 FILE*f=fopen(argv[1],"w");if(!f){perror("output");return 3;}
 fprintf(f,"GRAPH M=%d nodes=%llu live=%llu dead=%llu lost_symmetry=%llu duplicate_axes=%llu cycles=%llu cycle_members=%llu primitive_cycles=%llu primitive_cycle_members=%llu\n",M,(unsigned long long)NN,(unsigned long long)good,(unsigned long long)dead,(unsigned long long)not_symmetric,(unsigned long long)dup,(unsigned long long)cyc,(unsigned long long)cycStates,(unsigned long long)primitiveCyc,(unsigned long long)primitiveCycStates);
 for(auto [length,n]:lens)fprintf(f,"CYCLE_LEN %d count=%llu\n",length,(unsigned long long)n);
 for(auto [length,n]:prLens)fprintf(f,"PRIMITIVE_CYCLE_LEN %d count=%llu\n",length,(unsigned long long)n);
 fclose(f);
 printf("COMPLETED M=%d nodes=%llu cycles=%llu primitive=%llu\n",M,(unsigned long long)NN,(unsigned long long)cyc,(unsigned long long)primitiveCyc);
}
