// Independent GMP big-integer control: no digit-array arithmetic in transition.
// Input m,n,steps,min-run. Uses mpz_class to compute N + rev10(N).
#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
static string seed(int m,int n){
 vector<int> h{10};h.insert(h.end(),m,8);h.push_back(5);h.push_back(11);h.insert(h.end(),n,16);h.push_back(8);
 string high,low;for(int x:h){int v=min(9,x);high.push_back(char('0'+v));low.push_back(char('0'+x-v));}
 reverse(low.begin(),low.end());return high+low;
}
static bool bands(const string&s,int a,int b,int threshold,int&outA,int&outB){
 int half=(s.size()+1)/2;vector<int>B(half+1),suffix(half+1);outA=outB=0;
 auto p=[&](int i){return (s[i]-'0')+(s[s.size()-1-i]-'0');};
 for(int i=half-1;i>=0;i--){B[i]=p(i)==b?B[i+1]+1:0;suffix[i]=max(suffix[i+1],B[i]);}
 int run=0;
 for(int i=0;i<half;i++){
   run=p(i)==a?run+1:0;
   if(run>=threshold&&suffix[i+1]>=threshold){outA=max(outA,run);outB=max(outB,suffix[i+1]);}
 }
 return outA>=threshold && outB>=threshold;
}
static uint64_t wordfnv(const string&s){uint64_t h=1469598103934665603ull;for(char x:s){h^=uint8_t(x);h*=1099511628211ull;}return h;}
int main(int argc,char**argv){
 if(argc!=5)return 1;
 int m=stoi(argv[1]),n=stoi(argv[2]),steps=stoi(argv[3]),threshold=stoi(argv[4]);
 mpz_class N(seed(m,n),10);const int X[6]={8,16,14,10,2,4},Y[6]={16,14,10,2,4,8};
 uint64_t trace=1469598103934665603ULL;int minA=INT32_MAX,minB=INT32_MAX;
 for(int t=0;t<=steps;t++){
  string s=N.get_str(10);if(s.front()=='0')return 7;
  if(equal(s.begin(),s.begin()+s.size()/2,s.rbegin())){cerr<<"PAL "<<t<<"\n";return 2;}
  int a=0,b=0;
  if(!bands(s,X[t%6],Y[t%6],threshold,a,b)){cerr<<"BAND FAIL "<<t<<" "<<a<<" "<<b<<"\n";return 3;}
  minA=min(minA,a);minB=min(minB,b);
  for(uint64_t v:{uint64_t(t),uint64_t(s.size()),uint64_t(a),uint64_t(b)}){trace^=v;trace*=1099511628211ULL;}
  if(t%5000==0||t==steps)cout<<"CHECKPOINT "<<t<<" digits="<<s.size()<<" A="<<a<<" B="<<b<<" digest="<<hex<<trace<<" numeric_fnv="<<wordfnv(s)<<dec<<"\n"<<flush;
  if(t==steps)break;
  string rev(s.rbegin(),s.rend());N+=mpz_class(rev,10);
 }
 cout<<"GMP_20000_PASS states="<<steps+1<<" m="<<m<<" n="<<n<<" minA="<<minA<<" minB="<<minB<<" digest="<<hex<<trace<<dec<<"\n";
}