// W18 independent 100,000-step base-10 full-width digit oracle.
// Unlike wall.cpp, holds every decimal digit and adds N+reverse(N) directly.
// c++ -O3 -std=c++17 full_digits.cpp -o /tmp/w18-full && /tmp/w18-full 20702 100000
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
static uint64_t hashFull(const vector<uint8_t>&digits){
 uint64_t h=0;for(auto p=digits.rbegin();p!=digits.rend();++p)h=(h*131+*p+'0')%1000000007ULL;return h;
}
int main(int argc,char**argv){
 int Q=argc>1?atoi(argv[1]):20702,T=argc>2?atoi(argv[2]):100000;
 if(Q<1 || T<0)return 2;
 vector<uint8_t> n; n.reserve(120000);n.push_back(4);
 n.insert(n.end(),2*Q,9);n.push_back(5);
 int minBand=1<<30,minT=-1;
 for(int t=0;t<=T;t++){
  size_t m=n.size(),half=m/2;
  bool pal=true;for(size_t i=0;i<half;i++)if(n[i]!=n[m-1-i]){pal=false;break;}
  if(pal){cerr<<"PAL at t="<<t<<"\n";return 3;}
  int band=0;
  size_t i=(m-1)/2,j=m/2;
  while(j<m && n[i]==9 && n[j]==9){band+=(i==j?1:2);if(i==0)break;--i;++j;}
  if(band<minBand){minBand=band;minT=t;}
  if(band<2){cerr<<"BAND LOST at t="<<t<<"\n";return 4;}
  if(t==1||t==100||t==1000||t==5000||t==10000||t==20000||t==50000||t==T){
    cout<<"checkpoint t="<<t<<" digits="<<n.size()<<" band="<<band<<" hash="<<hashFull(n)<<"\n";
  }
  if(t==T)break;
  vector<uint8_t> y;y.reserve(m+1);int c=0;
  for(size_t z=0;z<m;z++){
   int s=(int)n[z]+(int)n[m-1-z]+c;y.push_back((uint8_t)(s%10));c=s/10;
  }
  if(c)y.push_back((uint8_t)c);
  n.swap(y);
 }
 cout<<"PASS Q="<<Q<<" T="<<T<<" min_band="<<minBand<<" min_t="<<minT
   <<" final_digits="<<n.size()<<" final_hash="<<hashFull(n)<<"\n";
}
