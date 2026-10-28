// Agent-8: exact m=9 reflective lattice Phi_g^(21*k), 1<=k<=8.
// Resumable enumeration of nine axes * 19^5 seed rows; no reachability claim.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <algorithm>
#include <string>
using namespace std;
static const int B=10, M=9, P=21, TOP=19;
static const char* G="001001010101001010101";
static const long long PERAXIS=2476099LL;
struct State {int axis=0;long long idx=0,tested=0,closed=0,primitive=0;long long periods[9]={};};

static bool phi(const int* x,int gam,int* y){
 int z=-1;
 for(int i=0;i<M;i++)if(x[i]!=B-1){z=i;break;}
 if(z<0)return false;
 int A[M],D[M],e[M],f[M];
 A[(z+1)%M]=int(x[z]>=B);
 for(int j=1;j<M;j++){int i=(z+j)%M;A[(i+1)%M]=(x[i]+A[i])/B;}
 D[(z+M-1)%M]=int(x[z]>=B);
 for(int j=1;j<M;j++){int i=(z+M-j)%M;D[(i+M-1)%M]=(x[i]+D[i])/B;}
 for(int i=0;i<M;i++){e[i]=(x[i]+A[i])%B;f[i]=(x[i]+D[i])%B;}
 for(int i=0;i<M;i++)y[i]=e[i]+f[(i+M-gam)%M];
 return true;
}
static bool phi_independent(const int*x,int gam,int*y){
 int A[M],D[M],nA=0,nD=0;
 for(int seed=0;seed<=1;seed++){
  int c=seed,q[M];
  for(int i=0;i<M;i++){q[i]=c;c=(x[i]+c)/B;}
  if(c==seed){nA++;memcpy(A,q,sizeof A);}
  c=seed;
  for(int j=0;j<M;j++){int i=(M-j)%M;q[i]=c;c=(x[i]+c)/B;}
  if(c==seed){nD++;memcpy(D,q,sizeof D);}
 }
 if(nA!=1||nD!=1)return false;
 for(int i=0;i<M;i++){
  int jm=(i+M-gam)%M;
  y[i]=(x[i]+A[i])%B+(x[jm]+D[jm])%B;
 }
 return true;
}
static bool spatial9(const int* x){
 for(int d: {1,3}){
  bool same=true;
  for(int i=0;i<M;i++)if(x[i]!=x[(i+d)%M]){same=false;break;}
  if(same)return false;
 }
 return true;
}
static void save(const State&s,const char*path){
 string tmp=string(path)+".tmp";
 FILE*f=fopen(tmp.c_str(),"w");if(!f){perror("checkpoint");exit(2);}
 fprintf(f,"%d %lld %lld %lld %lld",s.axis,s.idx,s.tested,s.closed,s.primitive);
 for(int j=1;j<=8;j++)fprintf(f," %lld",s.periods[j]);fprintf(f,"\n");
 fflush(f);fclose(f);if(rename(tmp.c_str(),path)){perror("rename");exit(3);}
}
static bool load(State &s,const char*path){
 FILE*f=fopen(path,"r");if(!f)return false;
 int n=fscanf(f,"%d %lld %lld %lld %lld",&s.axis,&s.idx,&s.tested,&s.closed,&s.primitive);
 for(int j=1;j<=8&&n==5;j++)if(fscanf(f,"%lld",&s.periods[j])!=1)n=0;
 fclose(f);return n==5;
}
int main(int argc,char**argv){
 if(argc==2 && string(argv[1])=="--selftest"){
  unsigned long long seed=0x5a34d0e991abULL;
  for(int k=0;k<200000;k++){
   int row[M],a[M],d[M];
   for(int j=0;j<M;j++){seed=seed*6364136223846793005ULL+1442695040888963407ULL;row[j]=(seed>>33)%TOP;}
   int g=k&1;
   bool aa=phi(row,g,a),bb=phi_independent(row,g,d);
   if(aa!=bb||(aa&&memcmp(a,d,sizeof a))){fprintf(stderr,"DIFFERENTIAL FAILURE k=%d\n",k);return 10;}
  }
  printf("SELFTEST 200000 independent cyclic-carry differential cases PASS\n");return 0;
 }
 if(argc<3){fprintf(stderr,"usage: m9_scan STATE_FILE CANDIDATE_FILE [MAX_SEEDS_PER_RUN]\n");return 2;}
 State s;load(s,argv[1]);const char* candidates=argv[2];
 long long budget=(argc>=4)?atoll(argv[3]):0;
 int refl[M],reps[M],nr=0;
 for(;s.axis<M;s.axis++){
  nr=0;for(int i=0;i<M;i++){refl[i]=(s.axis-i+M)%M;if(i<=refl[i])reps[nr++]=i;}
  if(nr!=5){fprintf(stderr,"bad axis %d %d\n",s.axis,nr);return 3;}
  for(;s.idx<PERAXIS;s.idx++){
   int ds[5],x[M]={0},y[M];long long zz=s.idx;
   for(int i=0;i<5;i++){ds[i]=zz%TOP;zz/=TOP;}
   for(int i=0;i<5;i++)x[reps[i]]=x[refl[reps[i]]]=ds[i];
   int original[M];memcpy(original,x,sizeof x);
   bool valid=true;int blockReturn=0;
   for(int block=1;block<=8 && valid && !blockReturn;block++){
    for(int t=0;t<P;t++){
     if(!phi(x,G[t]-'0',y)){valid=false;break;}
     memcpy(x,y,sizeof x);
    }
    if(valid && memcmp(x,original,sizeof x)==0)blockReturn=block;
   }
   s.tested++;
   if(blockReturn>0){
    s.closed++;
    if(spatial9(original)){
     s.primitive++;s.periods[blockReturn]++;
     memcpy(x,original,sizeof x);
     int axis=s.axis;
     for(int t=0;t<blockReturn*P;t++){
      for(int j=0;j<M;j++)if(x[j]!=x[(axis+M-j)%M]){fprintf(stderr,"mirror mismatch\n");return 5;}
      int check[M],calc[M];int gam=G[t%P]-'0';
      if(!phi_independent(x,gam,check)||!phi(x,gam,calc)||memcmp(check,calc,sizeof calc)){fprintf(stderr,"independent mismatch\n");return 6;}
      memcpy(x,check,sizeof x);axis=(axis+gam)%M;
     }
     if(memcmp(x,original,sizeof x)){fprintf(stderr,"return mismatch\n");return 7;}
     if(s.primitive<=1000){
      FILE*f=fopen(candidates,"a");if(!f)return 8;
      fprintf(f,"k=%d axis=%d index=%lld row=",blockReturn,s.axis,s.idx);
      for(int i=0;i<M;i++)fprintf(f,"%d%s",original[i],i+1<M?",":"\n");
      fclose(f);
     }
    }
   }
   if(s.tested%100000==0){State next=s;next.idx++;save(next,argv[1]);fprintf(stderr,"CHECKPOINT axis=%d idx=%lld tested=%lld closed=%lld primitive=%lld\n",s.axis,s.idx,s.tested,s.closed,s.primitive);fflush(stderr);}
   if(budget>0&&s.tested>=budget){s.idx++;save(s,argv[1]);fprintf(stderr,"PAUSED at %lld\n",s.tested);return 4;}
  }
  s.idx=0;State next=s;next.axis++;save(next,argv[1]);
  fprintf(stderr,"AXIS COMPLETE %d tested=%lld closed=%lld primitive=%lld\n",s.axis,s.tested,s.closed,s.primitive);
 }
 save(s,argv[1]);printf("COMPLETE tested=%lld expected=%lld closed=%lld primitive=%lld\n",s.tested,9*PERAXIS,s.closed,s.primitive);
 for(int i=1;i<=8;i++)printf("TEMPORAL_BLOCKS k=%d primitive=%lld\n",i,s.periods[i]);
 return s.tested==9*PERAXIS?0:9;
}
