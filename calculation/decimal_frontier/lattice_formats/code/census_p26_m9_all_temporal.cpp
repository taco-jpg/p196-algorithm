// Exact complete functional graph for the p26, S=9 reflective m9 bulk.
// Local experimental source; source checked into the repository only with a result.
#include <algorithm>
#include <array>
#include <cstdio>
#include <cstring>
#include <map>
#include <string>
#include <vector>
using namespace std;
static constexpr int B=10,M=9,P=26,TOP=19,N=2476099;
static constexpr char G[]="10010100010101001010001000";
static bool phi(const int*x,int gam,int*y){
 int z=-1;for(int i=0;i<M;i++)if(x[i]!=B-1){z=i;break;}if(z<0)return false;
 int A[M],D[M],e[M],f[M];A[(z+1)%M]=x[z]>=B;
 for(int j=1;j<M;j++){int i=(z+j)%M;A[(i+1)%M]=(x[i]+A[i])/B;}
 D[(z+M-1)%M]=x[z]>=B;
 for(int j=1;j<M;j++){int i=(z+M-j)%M;D[(i+M-1)%M]=(x[i]+D[i])/B;}
 for(int i=0;i<M;i++){e[i]=(x[i]+A[i])%B;f[i]=(x[i]+D[i])%B;}
 for(int i=0;i<M;i++)y[i]=e[i]+f[(i+M-gam)%M];return true;
}
static bool independent(const int*x,int gam,int*y){
 int A[M],D[M],nA=0,nD=0;
 for(int seed=0;seed<=1;seed++){int c=seed,q[M];
  for(int i=0;i<M;i++){q[i]=c;c=(x[i]+c)/B;}if(c==seed){nA++;memcpy(A,q,sizeof A);}
  c=seed;for(int j=0;j<M;j++){int i=(M-j)%M;q[i]=c;c=(x[i]+c)/B;}if(c==seed){nD++;memcpy(D,q,sizeof D);}
 }
 if(nA!=1||nD!=1)return false;
 for(int i=0;i<M;i++){int j=(i+M-gam)%M;y[i]=(x[i]+A[i])%B+(x[j]+D[j])%B;}return true;
}
static bool primitive(const int*x){for(int d:{1,3}){bool same=true;for(int i=0;i<M;i++)if(x[i]!=x[(i+d)%M]){same=false;break;}if(same)return false;}return true;}
static void decode(int axis,int id,int*x,const int*rep){for(int j=0;j<5;j++){int i=rep[j],k=(axis+M-i)%M;x[i]=x[k]=id%TOP;id/=TOP;}}
static int encode(const int*x,const int*rep){int n=0,p=1;for(int j=0;j<5;j++){n+=x[rep[j]]*p;p*=TOP;}return n;}
// The complete-graph pass compares both cyclic carry constructions on every
// one of its 9*19^5*26 elementary transitions, not only on representatives.
static bool block(int*x){int y[M],z[M];for(int t=0;t<P;t++){int g=G[t]-'0';if(!phi(x,g,y))return false;if(!independent(x,g,z)||memcmp(y,z,sizeof y)){fprintf(stderr,"CARRY MISMATCH t=%d\n",t);exit(30);}memcpy(x,y,sizeof y);}return true;}
static void checkpoint(const char*path,int a){string q=string(path)+".tmp";FILE*f=fopen(q.c_str(),"w");if(!f)exit(20);fprintf(f,"%d\n",a);fclose(f);rename(q.c_str(),path);}
int main(int argc,char**argv){
 if(argc==2&&string(argv[1])=="--selftest"){unsigned long long s=0x5a34d0e991abULL;for(int k=0;k<200000;k++){int x[M],a[M],b[M];for(int j=0;j<M;j++){s=s*6364136223846793005ULL+1442695040888963407ULL;x[j]=(s>>33)%TOP;}if(phi(x,k&1,a)!=independent(x,k&1,b)||memcmp(a,b,sizeof a)){fprintf(stderr,"DIFFERENTIAL FAILURE %d\n",k);return 10;}}puts("SELFTEST 200000 PASS");return 0;}
 if(argc!=4){fprintf(stderr,"usage: CHECKPOINT SUMMARY CYCLES\n");return 2;}int first=0;FILE*f=fopen(argv[1],"r");if(f){fscanf(f,"%d",&first);fclose(f);}if(first<0||first>9)return 3;
 vector<int> next(N),where(N),stack;vector<unsigned char> colour(N);
 for(int axis=first;axis<M;axis++){
  int rep[5],nr=0;for(int i=0;i<M;i++)if(i<=(axis+M-i)%M)rep[nr++]=i;if(nr!=5)return 4;
  long long dead=0;for(int id=0;id<N;id++){int x[M];decode(axis,id,x,rep);if(!block(x)){next[id]=-1;dead++;continue;}for(int j=0;j<M;j++)if(x[j]!=x[(axis+M-j)%M])return 5;next[id]=encode(x,rep);}
  fill(colour.begin(),colour.end(),0);fill(where.begin(),where.end(),-1);map<int,long long> all,prim,labels;
  for(int id=0;id<N;id++)if(!colour[id]){stack.clear();int v=id;while(v>=0&&!colour[v]){colour[v]=1;where[v]=stack.size();stack.push_back(v);v=next[v];}if(v>=0&&colour[v]==1){int k=int(stack.size())-where[v];all[k]++;int x[M];decode(axis,v,x,rep);if(primitive(x)){prim[k]++;labels[k]+=k;int orig[M];memcpy(orig,x,sizeof x);int a=axis;for(int t=0;t<k*P;t++){for(int j=0;j<M;j++)if(x[j]!=x[(a+M-j)%M])return 6;int y[M],z[M];int g=G[t%P]-'0';if(!phi(x,g,y)||!independent(x,g,z)||memcmp(y,z,sizeof y))return 7;memcpy(x,y,sizeof x);a=(a+g)%M;}if(memcmp(x,orig,sizeof x)||a!=axis)return 8;f=fopen(argv[3],"a");if(!f)return 9;fprintf(f,"AXIS=%d K=%d ROW=",axis,k);for(int j=0;j<M;j++)fprintf(f,"%d%s",orig[j],j+1<M?",":"\n");fclose(f);}}for(int q:stack){colour[q]=2;where[q]=-1;}}
  const map<int,long long> expectedAll={{1,6},{2,4},{3,4},{4,2},{5,2},{6,1},{19,2},{24,2},{57,2}};
  const map<int,long long> expectedPrimitive={{1,2},{2,4},{4,2},{5,2},{6,1},{19,2},{24,2},{57,2}};
  if(dead!=1||all!=expectedAll||prim!=expectedPrimitive)return 12;
  f=fopen(argv[2],"a");if(!f)return 11;long long nc=0,np=0;for(auto q:all)nc+=q.second;for(auto q:prim)np+=q.second;fprintf(f,"AXIS=%d N=%d DEAD=%lld ALL_CYCLES=%lld PRIM_CYCLES=%lld\n",axis,N,dead,nc,np);for(auto q:all)fprintf(f,"CYCLE_LENGTH axis=%d k=%d count=%lld primitive_cycles=%lld primitive_labelled_starts=%lld\n",axis,q.first,q.second,prim[q.first],labels[q.first]);fclose(f);checkpoint(argv[1],axis+1);fprintf(stderr,"AXIS DONE %d primitive=%lld\n",axis,np);
 }
 puts("ALL AXES COMPLETE");return 0;
}
