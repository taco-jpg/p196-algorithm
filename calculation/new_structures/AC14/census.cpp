// AC14 phase-5 exact endpoint-only carry-prefix census.
// PAPER lemma: an unknown incoming suffix carry (0/1) is absorbed by
// the first coefficient != 9 in the high suffix. Drop undecidable outputs.
// This is NOT strict-W9 pruning: damage at intermediate steps is allowed.
#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
using namespace std;
static constexpr int B[34]={1,5,11,12,9,10,8,3,11,6,14,16,10,0,14,12,9,8,7,2,8,12,5,17,14,8,9,13,14,17,14,12,15,13};
static constexpr int W[9]={12,9,7,10,4,5,10,14,13};
static constexpr int G[12]={1,0,0,0,1,0,0,0,1,0,0,0};
static constexpr int K=48,Q=14,T=120,MAX=1024;
static int U[30][3];
struct Result{int mismatch,actual,wanted,known,totalNineDrops;};
void init(){
 int id=0;
 for(int a=0;a<=18;a+=2){
  int v[3]={9,a,18-a};
  for(int rot=0;rot<3;rot++){
   for(int j=0;j<3;j++)U[id][j]=v[(j+rot)%3];
   ++id;
  }
 }
 assert(id==30);
}
Result check(int len,int index,int rank){
 unsigned char p[MAX],n[MAX],low[MAX],high[MAX];
 const int L0=34+9*Q+len+3*K;
 int L=L0,s=0,digit[6]={},z=index;
 for(int i=0;i<34;i++)p[s++]=B[i];
 for(int q=0;q<Q;q++)for(int i=0;i<9;i++)p[s++]=W[i];
 for(int j=len-1;j>=0;j--){digit[j]=z%19;z/=19;}
 for(int j=0;j<len;j++)p[s++]=digit[j];
 for(int k=0;k<K;k++)for(int j=0;j<3;j++)p[s++]=U[rank][j];
 assert(s==L);
 int nineDrops=0;
 for(int t=0;t<T;t++){
  int r=0;
  while(r<L && p[L-1-r]==9)++r;
  if(r==L)return {-2,-1,-1,L,nineDrops};
  nineDrops+=r;
  int gamma=G[(t+5)%12];
  // For p[0]!=9, the highest carry is independent of the unknown
  // suffix inlet; the actual gamma must equal [p[0]>=10].
  if(p[0]==9 || (p[0]>=10)!=gamma)return {-3,-1,-1,L,nineDrops};
  int nextL=L-1-r+gamma;
  if(nextL<0)return {-4,-1,-1,L,nineDrops};
  int c=0;
  for(int i=0;i<L;i++){
   int v=p[i]+c;low[i]=v%10;c=v/10;
  }
  c=0;
  for(int j=0;j<L;j++){
   int v=p[L-1-j]+c;high[j]=v%10;c=v/10;
  }
  for(int i=0;i<nextL;i++){
   int hi=(gamma && i==0)?1:high[L-1-i+gamma];
   n[i]=low[i]+hi;
  }
  memcpy(p,n,nextL);L=nextL;
 }
 int first=-1,actual=-1,wanted=-1;
 for(int i=0;i<L;i++){
  int expect;
  if(i<34)expect=B[i];
  else if(i<34+9*Q)expect=W[(i-34)%9];
  else if(i<34+9*Q+len)expect=digit[i-(34+9*Q)];
  else expect=U[rank][(i-(34+9*Q+len))%3];
  if((int)p[i]!=expect){
   first=i;actual=p[i];wanted=expect;break;
  }
 }
 return {first,actual,wanted,L,nineDrops};
}
int main(int argc,char**argv){
 init();
 int r0=0,r1=30,l0=3,l1=4,limit=0,skip=0;
 if(argc>1)r0=atoi(argv[1]);
 if(argc>2)r1=atoi(argv[2]);
 if(argc>3)l0=atoi(argv[3]);
 if(argc>4)l1=atoi(argv[4]);
 if(argc>5)limit=atoi(argv[5]);
 if(argc>6)skip=atoi(argv[6]);
 if(r0<0||r1>30||r0>=r1||l0<0||l1>6||l0>l1)return 3;
 auto start=chrono::steady_clock::now();
 long long total=0,miss=0,unresolved=0;
 int minmis=1000000,maxmis=-1,minknown=1000000,maxDrops=0;
 for(int rank=r0;rank<r1;rank++)for(int len=l0;len<=l1;len++){
  int count=1;for(int j=0;j<len;j++)count*=19;
  if(limit && count>limit)count=limit;
  long long groupMiss=0,groupUnresolved=0;
  int groupMin=1000000,groupMax=-1;
  for(int i=skip;i<count;i++){
   Result x=check(len,i,rank);++total;
   if(x.mismatch>=0){
    ++miss;++groupMiss;
    minmis=min(minmis,x.mismatch);maxmis=max(maxmis,x.mismatch);
    groupMin=min(groupMin,x.mismatch);groupMax=max(groupMax,x.mismatch);
   }else if(x.mismatch==-1){++unresolved;++groupUnresolved;}
   else {fprintf(stderr,"ERROR rank=%d len=%d j=%d state=%d\n",rank,len,i,x.mismatch);return 2;}
   minknown=min(minknown,x.known);maxDrops=max(maxDrops,x.totalNineDrops);
  }
  fprintf(stderr,"GROUP rank=%d U=[%d,%d,%d] len=%d tested=%d mismatch=%lld unresolved=%lld first=[%d,%d]\n",
   rank,U[rank][0],U[rank][1],U[rank][2],len,count-skip,groupMiss,groupUnresolved,groupMin,groupMax);
 }
 double elapsed=chrono::duration<double>(chrono::steady_clock::now()-start).count();
 printf("TOTAL ranks=[%d,%d) len=[%d,%d] tested=%lld mismatch=%lld unresolved=%lld first=[%d,%d] minKnown=%d maxNineDrops=%d sec=%.2f\n",
   r0,r1,l0,l1,total,miss,unresolved,minmis,maxmis,minknown,maxDrops,elapsed);
 return 0;
}