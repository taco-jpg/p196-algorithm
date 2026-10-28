// Independent time-by-time coefficient DP for decimal overflow (11 0^r)^k.
// This C++ code does not construct block edges or import the Python proof.
#include <array>
#include <cassert>
#include <cstdlib>
#include <cstdint>
#include <iostream>
using namespace std;
using U=uint64_t;
U count_closed(int r,int k){
 U total=0;
 for(int start=1;start<=18;start++){
  array<U,19>cur{},next{};cur[start]=1;
  for(int t=0;t<(r+2)*k;t++){
   int g=(t%(r+2)<2);
   next={};
   for(int x=0;x<=18;x++)if(cur[x])for(int c=0;c<=1;c++){
    if((x+c)/10!=g)continue;
    int y=x%10+(g?1:(x+c)%10);
    assert(y>=0&&y<=18);
    next[y]+=cur[x];
   }
   cur=next;
  }
  total+=cur[start];
 }
 return total;
}
int main(int argc,char**argv){
 int rmax=argc>1?atoi(argv[1]):100,kmax=argc>2?atoi(argv[2]):12;
 if(rmax<5||rmax>500||kmax<1||kmax>20)return 2;
 for(int r=1;r<=rmax;r++)for(int k=1;k<=kmax;k++){
  U count=count_closed(r,k);
  U expected=(r==3)?(U(1)<<k):0;
  if(count!=expected){cerr<<"FAIL r="<<r<<" k="<<k<<" got="<<count<<" expected="<<expected<<"\n";abort();}
 }
 cout<<"PASS: independently checked all "<<rmax*kmax<<" base-10 rooted time-closure pairs (r,k)"<<"; only r=3 has 2^k paths\n";
}
