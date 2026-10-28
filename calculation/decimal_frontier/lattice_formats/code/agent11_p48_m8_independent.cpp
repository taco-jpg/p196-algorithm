// Independent exact base-10 p=48 spatial-m8 mirrored-row census.
// Dual cyclic carry fixed-point solver, different from pivot-reset recurrence.
#include <array>
#include <cstdio>
#include <cstdint>
#include <cstdlib>
using namespace std;
#ifndef LAT_M
#define LAT_M 8
#endif
static constexpr int M=LAT_M,P=48,B=10;
using Row=array<unsigned char,M>;

static bool phi(const Row&r,int gam,Row&out){
 bool isneutral=true;for(int i=0;i<M;i++)if(r[i]!=9){isneutral=false;break;}
 if(isneutral)return false;
 int A[M],D[M],an=0,dn=0;
 for(int seed=0;seed<=1;seed++){
  int a[M];a[0]=seed;int carry=seed;
  for(int i=0;i<M;i++){carry=(r[i]+carry)/B;if(i+1<M)a[i+1]=carry;}
  if(carry==seed){an++;for(int i=0;i<M;i++)A[i]=a[i];}
 }
 for(int seed=0;seed<=1;seed++){
  int d[M];d[0]=seed;int carry=seed;
  for(int j=0;j<M;j++){int i=(M-j)%M;carry=(r[i]+carry)/B;d[(i+M-1)%M]=carry;}
  if(carry==seed){dn++;d[0]=seed;for(int i=0;i<M;i++)D[i]=d[i];}
 }
 if(an!=1||dn!=1){fprintf(stderr,"bad carries %d %d\n",an,dn);exit(4);}
 int e[M],f[M];
 for(int i=0;i<M;i++){e[i]=(r[i]+A[i])%B;f[i]=(r[i]+D[i])%B;}
 for(int i=0;i<M;i++)out[i]=e[i]+(gam?f[(i+M-1)%M]:f[i]);
 return true;
}
static uint64_t ipow(int n){uint64_t v=1;while(n--)v*=19;return v;}
int main(){uint64_t checked=0,hit=0;
 for(int axis=0;axis<M;axis++){
  int reps[M],nr=0,partner[M];for(int i=0;i<M;i++)partner[i]=(axis+M-i)%M;
  for(int i=0;i<M;i++)if(i<=partner[i])reps[nr++]=i;
  uint64_t n=ipow(nr);
  for(uint64_t idx=0;idx<n;idx++){
   Row orig{};uint64_t v=idx;for(int j=0;j<nr;j++){int z=v%19;v/=19;orig[reps[j]]=orig[partner[reps[j]]]=z;}
   Row cur=orig,nxt;bool valid=true;
   for(int t=0;t<P;t++){if(!phi(cur,t&1,nxt)){valid=false;break;}cur=nxt;}
   if(valid&&cur==orig){
    bool primitive=true;
    for(int d=1;d<M;d++){if(M%d)continue;bool same=true;for(int i=0;i<M;i++)if(orig[i]!=orig[(i+d)%M]){same=false;break;}if(same){primitive=false;break;}}
    if(primitive){hit++;printf("HIT axis=%d idx=%llu\n",axis,(unsigned long long)idx);}
   }
   checked++;
  }
 }
 printf("INDEPENDENT m=%d p=48 seeds=%llu primitive_returns=%llu\n",M,(unsigned long long)checked,(unsigned long long)hit);
}
