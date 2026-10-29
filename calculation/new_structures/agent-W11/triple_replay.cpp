// W11: three independently moving decimal packets and a second, full-digit RAA path.
// Build: g++ -O2 -std=c++17 triple_replay.cpp -lgmpxx -lgmp -o triple_replay
#include <gmpxx.h>
#include <array>
#include <algorithm>
#include <fstream>
#include <climits>
#include <cstdint>
#include <iomanip>
#include <tuple>
#include <iostream>
#include <stdexcept>
#include <string>
using namespace std;
using P=array<mpz_class,3>;
using S=array<long long,3>;
static string dec(const mpz_class&a){return a.get_str();}
static mpz_class rev(const mpz_class&a){string z=dec(a);reverse(z.begin(),z.end());return mpz_class(z,10);}
static long long digits(const mpz_class&a){return (long long)dec(a).size();}
static mpz_class ten(long long e){if(e<0||e>1000000)throw runtime_error("power limit");mpz_class z;mpz_ui_pow_ui(z.get_mpz_t(),10,(unsigned long)e);return z;}
static long long sep(const P&p,const S&s){return max(s[0]+digits(p[0])-s[1],s[1]+digits(p[1])-s[2]);}
static string word(const P&p,const S&s,long long q){
  long long g0=q+s[1]-s[0]-digits(p[0]),g1=q+s[2]-s[1]-digits(p[1]);
  if(s[0]<0||g0<0||g1<0)throw runtime_error("packet overlap");
  return dec(p[2])+string(g1,'0')+dec(p[1])+string(g0,'0')+dec(p[0])+string(s[0],'0');
}
static pair<P,S> step(const P&p,const S&s){
  long long e=s[2]+digits(p[2]);P a;S t;
  for(int k=0;k<3;k++){int j=2-k;long long r=e-s[j]-digits(p[j]),m=min(r,s[k]);t[k]=m;a[k]=p[k]*ten(s[k]-m)+rev(p[j])*ten(r-m);}
  return {a,t};
}
// The pairword has three disjoint finite zones if q>=pairsep.
// The zones are coefficientwise sums, with NO carry, of each packet
// and the opposite packet reflected about the entire integer's midpoint.
static long long pairsep(const P&p,const S&s){
  long long e=s[2]+digits(p[2]);S a,b;
  for(int k=0;k<3;k++){
    int j=2-k;long long r=e-s[j]-digits(p[j]);
    string z=dec(p[j]);long long n=z.size();
    while(n>1&&z[n-1]=='0')n--;
    a[k]=min(s[k],r);b[k]=max(s[k]+digits(p[k]),r+n);
  }
  return max(b[0]-a[1],b[1]-a[2]);
}
// D(X) = N(X)-reverse(N(X)) = 10^m sum d_k X^k, X=10^q.
// If degree h is nonzero, the <=4 lower packet terms are each
// smaller than 10^M. The integer-root bound q>=M+1 proves D(10^q)!=0.
static long long nonpalbound(const P&p,const S&s){
  long long e=s[2]+digits(p[2]),m=0;S r;P rp;
  for(int k=0;k<3;k++){int j=2-k;r[k]=e-s[j]-digits(p[j]);rp[k]=rev(p[j]);m=min(m,min(s[k],r[k]));}
  int h=-1;
  for(int k=2;k>=0;k--){
    long long x=min(s[k],r[k]);
    if(dec(p[k])+string(s[k]-x,'0') != dec(rp[k])+string(r[k]-x,'0')){h=k;break;}
  }
  if(h<0)throw runtime_error("palindromic polynomial");
  if(h==0)return 0;
  long long M=0;
  for(int k=0;k<h;k++){M=max(M,digits(p[k])+s[k]-m);M=max(M,digits(rp[k])+r[k]-m);}
  return M+1;
}
static uint64_t fnv(const string&s){uint64_t h=14695981039346656037ULL;for(unsigned char c:s){h^=c;h*=1099511628211ULL;}return h;}
static string pairs(const string&w){
  string p(w.size(),'A');
  for(size_t i=0;i<w.size();i++)p[i]='A'+(w[i]-'0')+(w[w.size()-1-i]-'0');
  return p;
}
// Independently add the entire integer to its reversal in ordinary decimal digits.
static string addfull(const string&w){
  string z(w.size(),'0');int carry=0;
  for(size_t i=0;i<w.size();i++){
    int x=(w[w.size()-1-i]-'0')+(w[i]-'0')+carry;
    z[w.size()-1-i]=char('0'+x%10);carry=x/10;
  }
  if(carry)z.insert(z.begin(),'1');
  while(z.size()>1&&z[0]=='0')z.erase(z.begin());
  return z;
}
static bool pal(const string&w){for(size_t i=0;i<w.size()/2;i++)if(w[i]!=w[w.size()-1-i])return false;return true;}
int main(int argc,char**argv){
 try{
  if(argc!=8&&argc!=9)throw runtime_error("usage: triple_replay TOP MID BOTTOM Q END_STEP OUT.tsv STATE [RESUME]");
  P p={mpz_class(argv[3]),mpz_class(argv[2]),mpz_class(argv[1])};S s={0,0,0};
  long long q=stoll(argv[4]);int end=stoi(argv[5]),start=0;
  if(q<1||end<0||p[0]<=0||p[1]<=0||p[2]<=0)throw runtime_error("invalid arguments");
  string actual=word(p,s,q);
  if(argc==9){
    ifstream in(argv[8]);if(!in)throw runtime_error("missing resume state");
    in>>start>>s[0]>>s[1]>>s[2];
    for(int k=0;k<3;k++){string z;in>>z;p[k]=mpz_class(z,10);}
    in>>actual;
    if(actual!=word(p,s,q))throw runtime_error("bad resume state");
  }
  ofstream out(argv[6]);
  out<<"t\tlenA\tlenM\tlenC\ts2\ts1\ts0\tgap1\tgap0\tqsep\tqpair\tqnonpal\tfull_digits\tfull_fnv64\tpair_fnv64\n";
  long long maxsep=0,maxpair=0,maxnp=0,mingap=LLONG_MAX;
  for(int t=start;t<=end;t++){
    long long a=sep(p,s),b=pairsep(p,s),c=nonpalbound(p,s);
    maxsep=max(maxsep,a);maxpair=max(maxpair,b);maxnp=max(maxnp,c);
    string w=word(p,s,q);
    if(w!=actual)throw runtime_error("full digit replay mismatch at "+to_string(t));
    if(pal(actual))throw runtime_error("palindrome at "+to_string(t));
    long long g1=q+s[2]-s[1]-digits(p[1]),g0=q+s[1]-s[0]-digits(p[0]);
    mingap=min(mingap,min(g0,g1));
    if(t%1000==0||t==end){
      out<<t<<'\t'<<digits(p[2])<<'\t'<<digits(p[1])<<'\t'<<digits(p[0])<<'\t'<<s[2]<<'\t'<<s[1]<<'\t'<<s[0]<<'\t'<<g1<<'\t'<<g0<<'\t'<<a<<'\t'<<b<<'\t'<<c<<'\t'<<w.size()<<'\t'<<hex<<fnv(w)<<'\t'<<fnv(pairs(w))<<std::dec<<'\n';
      mpz_class n(w,10);string rw=w;reverse(rw.begin(),rw.end());
      if(t<end&&dec(n+mpz_class(rw,10))!=addfull(w))throw runtime_error("GMP control mismatch");
    }
    if(t==end)break;
    actual=addfull(actual);
    tie(p,s)=step(p,s);
  }
  ofstream state(argv[7]);state<<end<<' '<<s[0]<<' '<<s[1]<<' '<<s[2]<<'\n';
  for(int k=0;k<3;k++)state<<dec(p[k])<<'\n';
  state<<actual<<'\n';
  cerr<<"PASS steps="<<end<<" q="<<q<<" max_sep="<<maxsep<<" max_pair="<<maxpair<<" max_nonpal="<<maxnp<<" min_gap="<<mingap<<" digits="<<actual.size()<<"\n";
  return 0;
 }catch(const exception&e){cerr<<"FAIL: "<<e.what()<<"\n";return 1;}
}
