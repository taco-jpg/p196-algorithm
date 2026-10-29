// AC04 overapproximation of ALL centre completions with fixed outside letters.
// Missing correlations can give false positives, never false exclusions.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using V=std::vector<uint32_t>;
static constexpr uint32_t ALL=(1u<<19)-1;
static constexpr uint32_t EVEN=0x15555;
static constexpr int U[3][3]={{9,6,12},{6,12,9},{12,9,6}};
static constexpr int B[34]={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static constexpr int W[9]={5,18,4,8,1,15,4,0,5};
static inline uint32_t sumSets(uint32_t a,uint32_t b){
 uint32_t out=0;
 while(a){const int x=__builtin_ctz(a);a&=a-1;uint32_t c=b;while(c){out|=1u<<(x+__builtin_ctz(c));c&=c-1;}}
 return out;
}
static inline void normalize(uint32_t coeff,uint32_t carry,uint32_t& d,uint32_t& c2){
 d=c2=0;
 while(coeff){int v=__builtin_ctz(coeff);coeff&=coeff-1;uint32_t cs=carry;
  while(cs){int z=__builtin_ctz(cs);cs&=cs-1;int s=v+z;d|=1u<<(s%10);c2|=1u<<(s/10);}
 }
}
static V initial(int ui,int l,int r,uint64_t prefix,int q,int k){
 std::vector<int> h;h.insert(h.end(),B,B+34);
 for(int i=0;i<q;i++)h.insert(h.end(),W,W+9);
 h.push_back(5);
 for(int i=0;i<k;i++)h.insert(h.end(),U[ui],U[ui]+3);
 int n=h.size(), length=2*n+l;V p(length);
 for(int i=0;i<n;i++)p[i]=p[length-1-i]=1u<<h[i];
 for(int i=0;i<l;i++)p[n+i]=(l%2&&i==l/2)?EVEN:ALL;
 for(int j=0;j<r;j++){
  int alpha=(l%2&&j==l/2)?10:19;
  int x=prefix%alpha;prefix/=alpha;
  if(alpha==10)x*=2;
  p[n+j]=p[n+l-1-j]=1u<<x;
 }
 return p;
}
static int abstractCheck(int ui,int l,int r,uint64_t pref,int q,int k,int& gammaGood){
 V p=initial(ui,l,r,pref,q,k),digs,tmp;
 const int cut=34+9*q+1+3*k+15;
 const int orig=p.size();
 int totalGamma=0;gammaGood=1;
 for(int t=0;t<120;t++){
  digs.resize(p.size());uint32_t c=1;
  for(size_t i=0;i<p.size();i++){
   uint32_t d,c2;normalize(p[i],c,d,c2);c=c2;digs[i]=d;
  }
  if(c!=1&&c!=2){gammaGood=0;return -2;}
  bool g=c==2;
  if(g!=(t%4==0))gammaGood=0;
  totalGamma+=g;
  if(g)digs.push_back(1u<<1);
  int m=digs.size();tmp.resize(m);
  for(int i=0;i<m;i++)tmp[i]=sumSets(digs[i],digs[m-1-i]);
  p.swap(tmp);
 }
 if(totalGamma!=30||int(p.size())!=orig+30){gammaGood=0;return -3;}
 for(int i=cut-150;i<cut+l+150;i++){
  if(i>=cut&&i<cut+l){
   int j=std::min(i-cut,cut+l-1-i);
   if(j>=r)continue;
   uint64_t x=pref;for(int a=0;a<j;a++)x/=((l%2&&a==l/2)?10:19);
   int v=x%((l%2&&j==l/2)?10:19);
   if(l%2&&j==l/2)v*=2;
   if((p[i]&(1u<<v))==0)return i-cut;
  }else{
   int uidx= i<cut ? ((i-(34+9*q+1))%3+3)%3
     : ((cut+l-1-i)%3+3)%3;
   int v=U[ui][uidx];
   if(!(p[i]&(1u<<v)))return i-cut;
  }
 }
 return 1000000;
}
static uint64_t count(int l,int r){uint64_t n=1;for(int i=0;i<r;i++)n*=((l%2&&i==l/2)?10:19);return n;}
int main(int argc,char**argv){
 if(argc<4){std::cerr<<"usage: abstract_pruner Uidx length fixedOuter [limit] [q] [k]\n";return 2;}
 int ui=atoi(argv[1]),l=atoi(argv[2]),r=atoi(argv[3]),q=argc>5?atoi(argv[5]):14,k=argc>6?atoi(argv[6]):100;
 uint64_t limit=argc>4?strtoull(argv[4],0,10):count(l,r);
 if(ui<0||ui>=3||l<1||l>30||r<0||r>(l+1)/2)return 2;
 limit=std::min(limit,count(l,r));uint64_t reject=0,uncertain=0,ambig=0;
 int minfail=999999,maxfail=-999999;
 auto start=std::chrono::steady_clock::now();
 for(uint64_t p=0;p<limit;p++){
  int gammaGood=0;int a=abstractCheck(ui,l,r,p,q,k,gammaGood);
  if(!gammaGood)ambig++;
  if(a==1000000)uncertain++;
  else if(a!=-2&&a!=-3){reject++;minfail=std::min(a,minfail);maxfail=std::max(a,maxfail);}
 }
 double secs=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
 std::cout<<"ABSTRACT U="<<ui<<" L="<<l<<" fixed="<<r<<" possible-prefixes="<<count(l,r)<<" tested="<<limit<<" reject="<<reject<<" unresolved="<<uncertain<<" gamma_ambiguous="<<ambig<<" firstfail="<<minfail<<":"<<maxfail<<" seconds="<<secs<<"\n";
}