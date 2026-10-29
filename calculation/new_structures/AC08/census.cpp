// AC08: exact physical base-ten centre-window endpoint census.
// Compile: g++ -O3 -std=c++17 census.cpp -o census
// Run: ./census <U-index 0..2> <C-length> <count; 0=all> [offset] [progress-every]
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>
using V=std::vector<uint8_t>;
static constexpr int B[34]={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static constexpr int W[9]={5,18,4,8,1,15,4,0,5};
static constexpr int U[3][3]={{9,14,4},{14,4,9},{4,9,14}};
static constexpr int Q=14,K=100,STEPS=120;
V halfword(int u,int k=K){
 V h;h.reserve(34+Q*9+1+3*k);
 for(int x:B)h.push_back(x);
 for(int j=0;j<Q;j++)for(int x:W)h.push_back(x);
 h.push_back(5);
 for(int j=0;j<k;j++)for(int x:U[u])h.push_back(x);
 return h;
}
struct Result {int first=-1,over=0,clockwrong=0;bool matches=false;};
Result run(const V& h,const V& want,const V& C,V& a,V& b){
 size_t half=h.size(),cn=C.size(),n=2*half+cn;
 a.resize(n+150);b.resize(n+150);
 for(size_t i=0;i<half;i++){
  int v=h[i];a[i]=std::max(0,v-9);a[n-1-i]=std::min(9,v);
 }
 for(size_t i=0;i<cn/2;i++){
  int v=C[i];a[half+i]=std::max(0,v-9);
  a[half+cn-1-i]=std::min(9,v);
 }
 if(cn%2)a[half+cn/2]=C[cn/2]/2;
 Result r;
 for(int t=0;t<STEPS;t++){
  int carry=0;
  for(size_t i=0;i<n;i++){
   int s=(int)a[i]+a[n-1-i]+carry;
   b[i]=s%10;carry=s/10;
  }
  if(carry)b[n++]=carry;
  r.over+=(carry!=0);
  if(carry!=(t%4==0))r.clockwrong++;
  a.swap(b);
 }
 if(n!=2*half+cn+30){r.first=-999;r.matches=false;return r;}
 size_t mid=n/2,radius=122+cn+30;
 size_t low=mid>radius?mid-radius:0;
 size_t high=std::min(n,mid+radius+1);
 r.matches=true;
 for(size_t i=low;i<high;i++){
  int got=(int)a[i]+a[n-1-i];
  if(got!=want[i]){r.matches=false;r.first=(int)i-(int)mid;break;}
 }
 return r;
}
uint64_t pow19(int k){uint64_t x=1;while(k--)x*=19;return x;}
V decode(uint64_t n,int len){
 V c(len);for(int i=0;i<len/2;i++){
  int v=n%19;n/=19;c[i]=v;c[len-1-i]=v;
 }
 if(len%2)c[len/2]=2*(n%10);
 return c;
}
int main(int argc,char**argv){
 if(argc<4){std::cerr<<"usage: census Uid length count [offset] [progress_every]\n";return 2;}
 int u=std::stoi(argv[1]),len=std::stoi(argv[2]);
 uint64_t cap=std::stoull(argv[3]),offset=argc>4?std::stoull(argv[4]):0;
 uint64_t progress=argc>5?std::stoull(argv[5]):100000;
 if(u<0||u>2||len<1||len>20)return 2;
 uint64_t total=pow19(len/2)*(len%2?10:1);
 if(offset>total)return 2;
 if(!cap||cap>total-offset)cap=total-offset;
 V h=halfword(u),outH=halfword(u,K+5),C=decode(offset,len);
 V target=outH;target.insert(target.end(),C.begin(),C.end());
 target.insert(target.end(),outH.rbegin(),outH.rend());
 V a,b;uint64_t matches=0,pruned11=0,simulated=0,wrongclock=0,wronggrowth=0;
 int minimum=9999,maximum=-9999;
 const int au[3]={-1,19,9};
 auto start=std::chrono::steady_clock::now();
 for(uint64_t idx=offset;idx<offset+cap;idx++){
  C=decode(idx,len);
  // Sound one-epoch endpoint exclusion: every N_120 is 0 mod 11.
  // For odd C, A(Ptarget)=10-2*A(U)+A(C) mod 11.
  if(len%2){
   int ac=0;
   for(int i=0;i<len;i++)ac+=(i%2?-int(C[i]):int(C[i]));
   if(((10-2*au[u]+ac)%11+11)%11!=0){pruned11++;continue;}
  }
  simulated++;
  for(int i=0;i<len;i++)target[h.size()+15+i]=C[i];
  Result r=run(h,target,C,a,b);
  if(r.matches){matches++;if(matches<=5)std::cout<<"FOUND code="<<idx<<"\n";}
  if(r.clockwrong)wrongclock++;
  if(r.over!=30)wronggrowth++;
  minimum=std::min(minimum,r.first);maximum=std::max(maximum,r.first);
  if(progress&&(idx-offset+1)%progress==0)
   std::cerr<<"PROGRESS "<<(idx-offset+1)<<"/"<<cap<<" matches="<<matches<<"\n";
 }
 double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
 std::cout<<"RESULT u="<<u<<" L="<<len<<" offset="<<offset<<" count="<<cap
 <<" total="<<total<<" matches="<<matches<<" mod11_pruned="<<pruned11
 <<" evaluated="<<simulated<<" clockwrong="<<wrongclock
 <<" growthwrong="<<wronggrowth<<" first=["<<minimum<<","<<maximum
 <<"] secs="<<seconds<<"\n";
}