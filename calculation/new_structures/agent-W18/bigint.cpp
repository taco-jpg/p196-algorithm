// W18 independent ordinary-integer oracle: base-1e9 limbs, decimal parsing
// and string reversal. Does not use or import wall.cpp. C++17.
// c++ -O3 -std=c++17 bigint.cpp -o /tmp/w18-big && /tmp/w18-big 4138 20000
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using Big=vector<uint32_t>;
constexpr uint64_t B=1000000000ULL;
static Big parse(const string &s){
 Big a;
 for(int end=(int)s.size();end>0;end-=9){int st=max(0,end-9);a.push_back((uint32_t)stoul(s.substr(st,end-st)));}
 while(a.size()>1 && a.back()==0)a.pop_back();return a;
}
static string render(const Big &a){
 string s=to_string(a.back());for(size_t i=a.size()-1;i>0;i--){string p=to_string(a[i-1]);s+=string(9-p.size(),'0')+p;}return s;
}
static Big add(const Big &a,const Big &b){
 Big c;size_t m=max(a.size(),b.size());c.reserve(m+1);uint64_t carry=0;
 for(size_t i=0;i<m;i++){
  uint64_t s=carry+(i<a.size()?a[i]:0)+(i<b.size()?b[i]:0);
  c.push_back((uint32_t)(s%B));carry=s/B;
 }
 if(carry)c.push_back((uint32_t)carry);
 return c;
}
static uint64_t hashString(const string &s){uint64_t h=0;for(char c:s)h=(131*h+int(c))%1000000007ULL;return h;}
int main(int argc,char**argv){
 int Q=argc>1?atoi(argv[1]):4138,T=argc>2?atoi(argv[2]):20000;
 if(Q<1||T<0){cerr<<"bad input\n";return 2;}
 Big n=parse("5"+string(2*Q,'9')+"4");int minBand=INT32_MAX,minAt=-1;
 for(int t=0;t<=T;t++){
  string s=render(n);
  if(equal(s.begin(),s.begin()+s.size()/2,s.rbegin())){cerr<<"palindrome at "<<t<<"\n";return 3;}
  // Central mirrored all-nine interval measured independently from full digits.
  size_t left=(s.size()-1)/2,right=s.size()/2;
  int band=0;
  while(left<s.size() && right<s.size() && s[left]=='9' && s[right]=='9'){
   band+= (left==right?1:2);if(!left)break;--left;++right;
  }
  if(band<minBand){minBand=band;minAt=t;}
  if(band<2){cerr<<"central nine band lost at "<<t<<"\n";return 4;}
  if(t==1||t==100||t==1000||t==5000||t==10000||t==T)
   cout<<"checkpoint t="<<t<<" digits="<<s.size()<<" band="<<band<<" hash="<<hashString(s)<<"\n";
  if(t==T){cout<<"PASS Q="<<Q<<" T="<<T<<" min_band="<<minBand<<" min_t="<<minAt
               <<" final_digits="<<s.size()<<" final_band="<<band<<" final_hash="<<hashString(s)<<"\n";break;}
  string r(s.rbegin(),s.rend());n=add(n,parse(r));
 }
}
