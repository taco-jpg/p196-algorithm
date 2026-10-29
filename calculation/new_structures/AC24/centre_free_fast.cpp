#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <algorithm>
#include <array>
#include <chrono>
using namespace std;
static constexpr int B3[34]={5,2,3,12,16,2,15,10,9,7,18,8,15,9,1,14,0,3,10,0,17,17,9,3,3,15,8,7,9,4,3,3,9,2};
static constexpr int W3[9]={4,0,17,11,9,12,2,9,2};
static constexpr int K=40, Q=14, MAXN=1000;
static uint8_t P[MAXN],N[MAXN],lo[MAXN],hi0[MAXN],hi1[MAXN];
static int init(const array<int,5>&J,const array<int,3>&U){
 int n=0;for(int x:B3)P[n++]=x;
 for(int j=0;j<Q;j++)for(int x:W3)P[n++]=x;
 for(int x:J)P[n++]=x;
 for(int j=0;j<K;j++)for(int x:U)P[n++]=x;
 return n;
}
// Invariant: P[0..n) is forced by the physical pairword's low prefix,
// for EVERY palindromic completion. Its reversed copy is the high suffix.
// Carry entering that high suffix may be either 0 or 1; both normalize
// identically after the last non-nine coefficient is crossed from the top.
// Hence indices strictly below `last` have forced upper normalized digits.
static int propagate(int n,int& gammaBad){
 for(int t=0;t<120;t++){
  int last=n-1;
  while(last>=0 && P[last]==9)last--;
  if(last<0){gammaBad++;return 0;}
  int carry=0;
  for(int i=n-1;i>=0;i--){
   int x=P[i]+carry;
   hi0[i]=(x>=10)?(x-10):x;
   carry=(x>=10);
  }
  int gamma=carry;
  // A high-side final carry of 1 introduces a new most-significant digit.
  // The next symmetric pairword is aligned with the high digits at index
  // i-1 (not i). Thus the forced next prefix length is last+gamma.
  int nn=last+gamma;
  carry=0;
  for(int i=0;i<nn;i++){
   int x=P[i]+carry, low=x>=10?x-10:x;
   carry=x>=10;
   N[i]=low+(gamma?(i?hi0[i-1]:1):hi0[i]);
  }
  n=nn;
  for(int i=0;i<n;i++)P[i]=N[i];
 }
 return n;
}
int main(int argc,char**argv){
 uint64_t begin=argc>1?strtoull(argv[1],0,10):0;
 uint64_t count=argc>2?strtoull(argv[2],0,10):10000;
 int a=argc>3?atoi(argv[3]):0, r=argc>4?atoi(argv[4]):0;
 array<int,3> U={9,a,18-a};rotate(U.begin(),U.begin()+r,U.end());
 uint64_t mismatch[162]={}, unknown=0, clockBad=0, longest=0;
 int minLen=1000,maxLen=0;uint64_t bestJ=0;
 auto t0=chrono::steady_clock::now();
 for(uint64_t z=begin;z<begin+count;z++){
  auto x=z;array<int,5>J{};for(int i=0;i<5;i++){J[i]=x%19;x/=19;}
  int n=init(J,U), err=0; n=propagate(n,err);
  minLen=min(minLen,n);maxLen=max(maxLen,n);clockBad+=err;
  // Endpoint-only necessary condition. Never reject intermediate W9 damage:
  // it may heal. Reject only inside a prefix proved forced after all 120 steps.
  int pos=0;while(pos<n&&pos<160&&P[pos]==(pos<34?B3[pos]:W3[(pos-34)%9]))pos++;
  if(pos<160&&pos<n){mismatch[pos]++;}else{unknown++;if(pos>longest){longest=pos;bestJ=z;}}
 }
 double time=chrono::duration<double>(chrono::steady_clock::now()-t0).count();
 printf("a=%d r=%d U=%d,%d,%d [%llu,%llu) secs=%.2f rate=%.1fJ/s minLen=%d maxLen=%d clockBad=%llu provedMismatch=%llu UNKNOWN=%llu longest=%llu bestJ=%llu\n",a,r,U[0],U[1],U[2],(unsigned long long)begin,(unsigned long long)(begin+count),time,count/time,minLen,maxLen,(unsigned long long)clockBad,(unsigned long long)(count-unknown),(unsigned long long)unknown,(unsigned long long)longest,(unsigned long long)bestJ);
 for(int i=0;i<162;i++)if(mismatch[i])printf("%d:%llu ",i,(unsigned long long)mismatch[i]);puts("");
}
