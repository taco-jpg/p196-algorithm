// AC41. Endpoint-only phase8 J6, J0=0, U=(9,0,18) full suffix census.
// Reproduce: g++ -O3 -std=c++17 census.cpp -o ac11 && ./ac11 0 137180
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
using namespace std;
static constexpr int B[34]={10,4,15,4,1,7,9,11,11,18,0,18,6,9,17,4,0,12,0,2,10,1,12,4,2,15,0,13,4,8,4,8,10,15};
static constexpr int W[9]={4,0,5,5,18,4,8,1,15};
static constexpr int MAXN=512, Q=14, UCOPIES=40, CUT=34+9*Q;
struct Result {int mismatch,known,gamma,problem_step;};

// Known LSD-first outer prefix p of a symmetric pairword, unknown interior.
// The carry entering the high (mirrored) prefix from the interior is either
// 0 or 1. At any p[r]!=9, both incoming carries yield identical outgoing
// carry, hence all high normalized digits j<r are determined. This gives
// EXACT next outer coefficients up to r+overflow, without constraining
// intermediate W9 preservation. There is no strict-phase pruning here.
static bool step(const uint8_t*p,int n,uint8_t*out,int&nn,int&gamma) {
  int r=n-1;
  while(r>=0 && p[r]==9)--r;
  if(r<0)return false;
  uint8_t low[MAXN],high[MAXN];
  int c=0;
  for(int j=0;j<n;j++){
    int z=p[j]+c;c=(z>=10);low[j]=uint8_t(z-10*c);
  }
  c=(p[r]>=10);
  for(int j=r-1;j>=0;j--){
    int z=p[j]+c;c=(z>=10);high[j]=uint8_t(z-10*c);
  }
  gamma=c;nn=r+gamma;
  if(nn<=0)return false;
  if(gamma)out[0]=uint8_t(low[0]+1);
  for(int j=gamma;j<nn;j++)out[j]=uint8_t(low[j]+high[j-gamma]);
  return true;
}
static Result test(int nj,const int*J,const int*U) {
  uint8_t aa[MAXN],bb[MAXN],*p=aa,*q=bb;int n=0;
  for(int v:B)p[n++]=uint8_t(v);
  for(int j=0;j<Q;j++)for(int v:W)p[n++]=uint8_t(v);
  for(int j=0;j<nj;j++)p[n++]=uint8_t(J[j]);
  for(int j=0;j<UCOPIES;j++)for(int h=0;h<3;h++)p[n++]=uint8_t(U[h]);
  assert(n<=MAXN);
  int sum=0;
  for(int t=0;t<120;t++){
    int nn=0,g=0;
    if(!step(p,n,q,nn,g))return {-2,n,sum,t};
    if(g!=int(t%4==0))return {-3,n,sum,t};
    sum+=g;n=nn;swap(p,q);
  }
  for(int j=0;j<min(n,CUT);j++){
    int expected=(j<34)?B[j]:W[(j-34)%9];
    if(p[j]!=expected)return {j,n,sum,-1};
  }
  return {-1,n,sum,-1};
}
int main(int argc,char**argv) {
  long long first=0,last=2476099;
  if(argc==3){first=atoll(argv[1]);last=atoll(argv[2]);}
  if(first<0||last>2476099||first>=last)return 2;
  long long total=0,unresolved=0,invalid=0;
  int minKnown=MAXN,minDiff=MAXN,maxDiff=-1;
  array<long long,190> hist{};
  int U[3]={9,0,18};
  for(long long code=first;code<last;code++){
    long long z=code;int J[6]={0,0,0,0,0,0};
    for(int j=1;j<6;j++){J[j]=int(z%19);z/=19;}
    Result r=test(6,J,U);total++;
    minKnown=min(minKnown,r.known);
    if(r.mismatch==-2||r.mismatch==-3||r.gamma!=30)invalid++;
    else if(r.mismatch<0)unresolved++;
    else {hist[r.mismatch]++;minDiff=min(minDiff,r.mismatch);maxDiff=max(maxDiff,r.mismatch);}
  }
  printf("PHASE=8 |J|=6 J0=0 U=(9,0,18) q=14 k>=40 C=ANY_REALIZABLE_PALINDROMIC\n");
  printf("RANGE=[%lld,%lld) TOTAL=%lld W9_FAIL=%lld UNRESOLVED=%lld INVALID=%lld MIN_KNOWN=%d DIFF_MIN=%d DIFF_MAX=%d\n",
    first,last,total,total-unresolved-invalid,unresolved,invalid,minKnown,minDiff,maxDiff);
  printf("HIST=");for(int j=0;j<int(hist.size());j++)if(hist[j])printf(" %d:%lld",j,hist[j]);puts("");
  return (unresolved||invalid)?1:0;
}
