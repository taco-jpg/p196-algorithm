// Independent arithmetic engines: decimal vectors and GMP mpz_class.
// Compile: g++ -O3 -std=c++17 replay.cpp -lgmpxx -lgmp -o replay
#include <gmpxx.h>
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;
static bool pal(const vector<uint8_t>&d) {
  for(size_t i=0,j=d.size()-1;i<j;i++,j--) if(d[i]!=d[j]) return false;
  return true;
}
static vector<uint8_t> raa(const vector<uint8_t>&d) {
  vector<uint8_t> o; o.reserve(d.size()+1);
  unsigned carry=0;
  for(size_t i=0,n=d.size();i<n;i++){
    unsigned v=unsigned(d[i])+d[n-1-i]+carry;
    o.push_back(v%10); carry=v/10;
  }
  if(carry) o.push_back(carry);
  return o;
}
static vector<uint8_t> digitsof(const mpz_class& z) {
  string s=z.get_str(10); vector<uint8_t> d;
  d.reserve(s.size()); for(auto it=s.rbegin();it!=s.rend();++it)d.push_back(*it-'0');
  return d;
}
static mpz_class raa_gmp(const mpz_class& z) {
  string s=z.get_str(10); reverse(s.begin(),s.end());
  // mpz_set_str rejects leading zeros in decimal? Accepts ordinary base10.
  mpz_class r(s,10); return z+r;
}
static vector<uint8_t> pairword(const vector<uint8_t>& d) {
  vector<uint8_t> p; p.reserve(d.size());
  for(size_t i=0,n=d.size();i<n;i++)p.push_back(d[i]+d[n-1-i]);
  return p;
}
static vector<uint8_t> frompair(const vector<uint8_t>& p) {
  vector<uint8_t> out; out.reserve(p.size()+1);
  unsigned c=0;
  for(uint8_t x:p) {unsigned q=unsigned(x)+c;out.push_back(q%10); c=q/10;}
  if(c)out.push_back(c);
  return out;
}
static uint64_t fnv(uint64_t h,unsigned x){return (h^x)*1099511628211ULL;}
int main(int argc,char**argv){
  if(argc<3){cerr<<"usage: ./replay SEED STEPS [stride]"<<endl;return 2;}
  string seed=argv[1]; int steps=atoi(argv[2]),stride=argc>3?atoi(argv[3]):1000;
  mpz_class z(seed,10); auto d=digitsof(z);
  uint64_t digest=1469598103934665603ULL;
  long long overflows=0; int minodd=1000000000,minfirstodd=1000000000,maxfirstodd=-1;
  long long palcount=0,evenodd=0; vector<int> alleven_steps;array<long long,21> firstoddhist{};
  array<long long,21> min_oddprefix{};map<string,long long> prefix4;
  for(int t=0;t<=steps;t++){
    if(d!=digitsof(z)){cerr<<"GMP mismatch at t="<<t<<"\n";return 3;}
    auto p=pairword(d);
    int oddcount=0, firstodd=-1;
    for(size_t i=0;i<(p.size()+1)/2;i++)if(p[i]&1){oddcount++;if(firstodd<0)firstodd=(int)i;}
    minodd=min(minodd,oddcount); if(firstodd>=0){minfirstodd=min(minfirstodd,firstodd);maxfirstodd=max(maxfirstodd,firstodd);firstoddhist[min(20,firstodd)]++;}
    if(firstodd<0){evenodd++;alleven_steps.push_back(t);}
    if(pal(d))palcount++;
    for(int lim=1;lim<=20;lim++)if(firstodd>=0&&firstodd<lim)min_oddprefix[lim]++;
    string key; for(int i=0;i<4 && i<(int)p.size();i++){if(i)key+=',';key+=to_string(p[i]);} prefix4[key]++;
    for(unsigned q: {unsigned(d.size()),unsigned(p[0]),unsigned(oddcount),unsigned(firstodd+1)})digest=fnv(digest,q);
    if(t%stride==0 || t==steps){
      cout<<"SAMPLE t="<<t<<" digits="<<d.size()<<" odd_half="<<oddcount<<" first_odd="<<firstodd<<" pair_prefix=";
      for(int i=0;i<min(12,(int)p.size());i++){if(i)cout<<",";cout<<unsigned(p[i]);}
      cout<<"\n";
    }
    if(t==steps)break;
    auto v=raa(d); auto k=frompair(p);
    if(v!=k){cerr<<"Pair normalization mismatch t="<<t<<"\n";return 4;}
    z=raa_gmp(z);
    if(v!=digitsof(z)){cerr<<"Independent GMP mismatch at t="<<t<<"\n";return 5;}
    if(v.size()>d.size())overflows++;
    d=move(v);
  }
  cout<<"RESULT seed="<<seed<<" steps="<<steps<<" final_digits="<<d.size()<<" overflows="<<overflows<<" pal_states="<<palcount<<" all_even_half_states="<<evenodd<<" min_odd_half="<<minodd<<" first_odd_min="<<minfirstodd<<" first_odd_max="<<maxfirstodd<<" digest="<<hex<<digest<<dec<<"\n";
  cout<<"FIRST_ODD_HIST ";for(int i=0;i<=20;i++)if(firstoddhist[i])cout<<i<<":"<<firstoddhist[i]<<" ";cout<<"\n";
  cout<<"PREFIX_COVER ";for(int i=1;i<=20;i++)cout<<i<<":"<<min_oddprefix[i]<<" ";cout<<"\n";
  cout<<"PREFIX4_DISTINCT="<<prefix4.size()<<"\n";
  cout<<"ALL_EVEN_STEPS=";for(int t:alleven_steps)cout<<t<<",";cout<<"\n";
}
