// Base-10 p16 g=(01)^8, exact spatial period m=8, one-lap self-mirror row census.
// This is only a local resumable intermediate census; never publish partial rows.
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <algorithm>
using namespace std;
#ifndef LATTICE_M
#define LATTICE_M 8
#endif
static constexpr int M=LATTICE_M,B=10,P=16;
using Row=array<unsigned char,M>;
static bool phi(const Row&v,int gam,Row&out){
 int i0=-1;for(int i=0;i<M;i++)if(v[i]!=9){i0=i;break;}
 if(i0<0)return false;
 int A[M]={},D[M]={},e[M],f[M];
 A[(i0+1)%M]=v[i0]>=B;
 for(int s=1;s<M;s++){int i=(i0+s)%M;A[(i+1)%M]=(v[i]+A[i])/B;}
 D[(i0+M-1)%M]=v[i0]>=B;
 for(int s=1;s<M;s++){int i=(i0+M-s)%M;D[(i+M-1)%M]=(v[i]+D[i])/B;}
 for(int i=0;i<M;i++){e[i]=(v[i]+A[i])%B;f[i]=(v[i]+D[i])%B;}
 for(int i=0;i<M;i++)out[i]=e[i]+(gam?f[(i+M-1)%M]:f[i]);
 return true;
}
static uint64_t p19(int n){uint64_t z=1;while(n--)z*=19;return z;}
static void save(const string&s,int alpha,uint64_t index,uint64_t hits,uint64_t runs){
 string tmp=s+".tmp";FILE*f=fopen(tmp.c_str(),"w");if(!f)return;
 fprintf(f,"%d %llu %llu %llu\n",alpha,(unsigned long long)index,(unsigned long long)hits,(unsigned long long)runs);
 fclose(f);rename(tmp.c_str(),s.c_str());
}
int main(int argc,char**argv){
 if(argc!=3){fprintf(stderr,"usage: m8_rows STATE_PATH ROWS_PATH\n");return 2;}
 string state=argv[1],rows=argv[2];int alpha0=0;uint64_t index0=0,hits=0,runs=0;
 if(FILE*f=fopen(state.c_str(),"r")){unsigned long long a,b,c;int t;if(fscanf(f,"%d %llu %llu %llu",&t,&a,&b,&c)==4){alpha0=t;index0=a;hits=b;runs=c;}fclose(f);}
 FILE*out=fopen(rows.c_str(),"a");if(!out){perror("output");return 3;}
 for(int alpha=alpha0;alpha<M;alpha++){
  int reps[M],nr=0,partners[M];
  for(int i=0;i<M;i++)partners[i]=(alpha+M-i)%M;
  for(int i=0;i<M;i++)if(i<=partners[i])reps[nr++]=i;
  uint64_t total=p19(nr),initial=(alpha==alpha0?index0:0);
  fprintf(stderr,"AXIS alpha=%d reps=%d total=%llu start=%llu\n",alpha,nr,(unsigned long long)total,(unsigned long long)initial);
  for(uint64_t idx=initial;idx<total;idx++){
   Row r{};uint64_t z=idx;
   for(int q=0;q<nr;q++){int value=z%19;z/=19;r[reps[q]]=r[partners[reps[q]]]=value;}
   Row cur=r,nxt;bool ok=true;Row period[P];
   for(int t=0;t<P;t++){period[t]=cur;if(!phi(cur,t&1,nxt)){ok=false;break;}cur=nxt;}
   if(ok&&cur==r){
    int mp=M;for(int d: {1,2,4}){if(d>=M)continue;bool good=true;for(int t=0;t<P&&good;t++)for(int k=0;k<M;k++)if(period[t][k]!=period[t][(k+d)%M]){good=false;break;}if(good){mp=d;break;}}
    if(mp==M){hits++;fprintf(out,"%d %llu",alpha,(unsigned long long)idx);for(auto x:r)fprintf(out," %d",int(x));fprintf(out,"\n");}
   }
   runs++;
   if((idx+1)%50000==0){fflush(out);save(state,alpha,idx+1,hits,runs);fprintf(stderr,"PROGRESS axis=%d index=%llu hits=%llu scanned=%llu\n",alpha,(unsigned long long)(idx+1),(unsigned long long)hits,(unsigned long long)runs);}
  }
  fflush(out);save(state,alpha+1,0,hits,runs);
 }
 fclose(out);
 printf("COMPLETED m=%d p=16 selfmirror fixed rows=%llu enumerated=%llu\n",M,(unsigned long long)hits,(unsigned long long)runs);
 return 0;
}
