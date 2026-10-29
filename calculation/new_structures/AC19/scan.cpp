// AC19: exact centre-independent endpoint W9 census for rooted decimal phase 10.
// Reproduce: c++ -O3 -std=c++17 scan.cpp -o scan; ./scan 4115400 0 1
// The first L pair coefficients are known at both ends of any palindromic
// pairword. The carry entering the unknown high suffix is 0 or 1.
// The first coefficient != 9 when scanning that suffix from its inner edge
// merges those two carries. Retain only output pair coefficients independent
// of both possibilities. No strict-per-phase W9 constraint is imposed.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <iostream>
using namespace std;
static const int B[34]={2,11,1,1,11,17,14,3,9,3,0,0,12,13,16,4,9,6,6,4,6,4,8,14,12,16,12,8,17,5,6,5,9,16};
static const int W[9]={0,9,11,1,10,8,5,9,16};
static constexpr int CUT=160, MAX=512;
struct R {int mismatch,known,overflows;};
static R cone(const int *J,int nj,const int *U,int collar=44){
 unsigned char p[MAX],next[MAX],lo[MAX],hi[MAX];
 int n=0;
 for(int x:B)p[n++]=x;
 for(int j=0;j<14;j++)for(int x:W)p[n++]=x;
 for(int j=0;j<nj;j++)p[n++]=J[j];
 for(int j=0;j<collar;j++)for(int i=0;i<3;i++)p[n++]=U[i];
 assert(n<MAX);
 int overflows=0;
 for(int t=0;t<120;t++){
  int c=0;
  for(int i=0;i<n;i++){int z=p[i]+c;lo[i]=z%10;c=z/10;}
  c=0;int reset=-1;
  for(int j=0;j<n;j++){
   int x=p[n-1-j],z=x+c;hi[j]=z%10;c=z/10;
   if(reset<0 && x!=9)reset=j;
  }
  if(reset<0)return {-2,n,overflows};
  int gamma=c;
  overflows+=gamma;
  // Coefficient at index i uses upper digit j=n-1-i+gamma,
  // except i=0,gamma=1 which uses the new top overflow digit.
  int keep=n-reset-1+gamma;
  if(keep<=0)return {-3,n,overflows};
  for(int i=0;i<keep;i++){
   int h=(gamma && i==0)?gamma:hi[n-1-i+gamma];
   next[i]=lo[i]+h;
  }
  memcpy(p,next,keep);n=keep;
 }
 if(n<CUT)return {-1,n,overflows};
 for(int i=0;i<CUT;i++){
  int expected=(i<34)?B[i]:W[(i-34)%9];
  if(p[i]!=expected)return {i,n,overflows};
 }
 return {CUT,n,overflows};
}
int main(int argc,char **argv){
 uint64_t limit=(argc>1)?strtoull(argv[1],nullptr,10):4115400;
 uint64_t skip=(argc>2)?strtoull(argv[2],nullptr,10):0;
 bool verbose=(argc>3)?atoi(argv[3])!=0:false;
 int U[30][3],num=0;
 for(int a=0;a<=18;a+=2){int v[3]={9,a,18-a};
  for(int rot=0;rot<3;rot++){
   for(int i=0;i<3;i++)U[num][i]=v[(rot+i)%3];
   ++num;
  }
 }
 assert(num==30);
 uint64_t hist[161]={0},tested=0,preserved=0,unknown=0,wrongclock=0,fallback=0;
 int minL=MAX,maxL=0;
 for(int u=0;u<30;u++)for(int nj=3;nj<=4;nj++){
  uint32_t combos=(nj==3)?6859:130321;
  for(uint32_t code=0;code<combos;code++){
   uint64_t id=uint64_t(u)*137180+(nj==4?6859:0)+code;
   if(id<skip)continue;
   if(tested>=limit)goto done;
   int J[4]={0};uint32_t v=code;
   for(int i=0;i<nj;i++){J[i]=v%19;v/=19;}
   R r=cone(J,nj,U[u],44);
   if(r.mismatch<0){++fallback;r=cone(J,nj,U[u],100);}
   if(r.mismatch<0)++unknown;
   else if(r.mismatch==CUT)++preserved;
   else hist[r.mismatch]++;
   if(r.overflows!=30)++wrongclock;
   minL=min(minL,r.known);maxL=max(maxL,r.known);
   ++tested;
  }
 }
done:
 uint64_t sum=0;
 for(int i=0;i<161;i++)sum+=hist[i];
 cout<<"phase=10 J=3,4 U=all30 q=14 k>=100 C=all_palindromic"
     <<" tested="<<tested<<" total=4115400 endpoint_W9_preserved="<<preserved
     <<" undecided="<<unknown<<" overflow_bad="<<wrongclock
     <<" fallback_to_k100="<<fallback<<" cone_L_min="<<minL
     <<" cone_L_max="<<maxL<<" mismatches="<<sum<<"\n";
 if(verbose)for(int i=0;i<161;i++)if(hist[i])cout<<"hist["<<i<<"]="<<hist[i]<<"\n";
 return (unknown||wrongclock)?1:0;
}
