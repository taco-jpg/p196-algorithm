// W11 standalone exact symbolic phase verifier. Only GMP is required.
// Build: g++ -O2 -std=c++17 phase_synchronizer.cpp -lgmpxx -lgmp -o phase_synchronizer
// Usage: ./phase_synchronizer [steps=20000] [--bad-guard]
#include <gmpxx.h>
#include <array>
#include <algorithm>
#include <map>
#include <tuple>
#include <iostream>
#include <string>
#include <stdexcept>
#include <climits>
using namespace std;
using P=array<mpz_class,4>;
using S=array<long long,4>;
static string str(const mpz_class&n){return n.get_str();}
static int len(const mpz_class&n){return n==0?0:(int)str(n).size();}
static mpz_class reversed(const mpz_class&n){
 if(n==0)return 0;
 string x=str(n);reverse(x.begin(),x.end());return mpz_class(x,10);
}
static mpz_class ten(long long k){
 if(k<0||k>1000000)throw runtime_error("invalid power of ten");
 mpz_class x;mpz_ui_pow_ui(x.get_mpz_t(),10,(unsigned long)k);return x;
}
static pair<P,S> packet_step(const P&p,const S&s){
 const long long E=s[3]+len(p[3]);
 P out;S sh;
 for(int k=0;k<4;k++){
   int j=3-k;
   bool a=p[k]!=0,b=p[j]!=0;
   if(!a&&!b){out[k]=0;sh[k]=0;continue;}
   long long r=E-s[j]-len(p[j]);
   long long h=a&&b?min(s[k],r):(a?s[k]:r);
   out[k]=(a?p[k]*ten(s[k]-h):mpz_class(0)) + (b?reversed(p[j])*ten(r-h):mpz_class(0));
   sh[k]=h;
 }
 return {out,sh};
}
int main(int argc,char**argv){
 try{
  int T=(argc>1?stoi(argv[1]):20000);
  bool bad=(argc>2&&string(argv[2])=="--bad-guard");
  if(T<1||T>100000)throw runtime_error("bad horizon");
  P p={75,3,0,88};S s={0,2,0,3};
  if(bad){p={163,10,10,145};s={0,2,2,4};}
  map<long long,long long> phase_count;
  map<tuple<int,int,int,int>,long long> table;
  long long middle_trailing=0,guard_hits=0,min_phase=LLONG_MAX,max_phase=LLONG_MIN,max_middle_digits=0;
  for(int t=(bad?1:0);t<=T;t++){
   if(t>0){
    if(p[1]!=p[2]||s[1]!=s[2]||p[1]<=0)throw runtime_error("middle packets not synchronized at "+to_string(t));
    long long E=s[3]+len(p[3]);
    long long th=E-2*s[1]-len(p[1]);
    if(th< -1||th>1)throw runtime_error("phase outside {-1,0,1} at "+to_string(t));
    if(th==1&&p[1]%10==0)throw runtime_error("phase-1 nonzero-units guard failed at "+to_string(t));
    min_phase=min(min_phase,th);max_phase=max(max_phase,th);
    phase_count[th]++;
    middle_trailing+=(p[1]%10==0);
    guard_hits+=(th==1);
    max_middle_digits=max(max_middle_digits,(long long)len(p[1]));
    if(t==T)break;
    P np;S ns;tie(np,ns)=packet_step(p,s);
    long long nextE=ns[3]+len(np[3]);
    long long gamma=nextE-E;
    if(gamma!=0&&gamma!=1)throw runtime_error("outer growth not in {0,1} at "+to_string(t));
    mpz_class proposed=0;
    if(th==-1){proposed=10*p[1]+reversed(p[1]);if(ns[1]!=s[1]-1)throw runtime_error("wrong -1 shift");}
    if(th==0){proposed=p[1]+reversed(p[1]);if(ns[1]!=s[1])throw runtime_error("wrong 0 shift");}
    if(th==1){proposed=p[1]+10*reversed(p[1]);if(ns[1]!=s[1])throw runtime_error("wrong +1 shift");}
    if(np[1]!=proposed)throw runtime_error("middle local rule mismatch at "+to_string(t));
    long long baseline=len(p[1])+(th==-1||th==1);
    long long carry=len(np[1])-baseline;
    if(carry!=0&&carry!=1)throw runtime_error("non-Boolean central length carry");
    long long nextPhase=nextE-2*ns[1]-len(np[1]);
    if(nextPhase!=gamma-carry)throw runtime_error("theta'=gamma-carry failed");
    table[{(int)th,(int)nextPhase,(int)gamma,(int)carry}]++;
    p=np;s=ns;
   }else tie(p,s)=packet_step(p,s);
  }
  cout<<"PASS steps="<<T<<" base=10 phases={-1:"<<phase_count[-1]<<",0:"<<phase_count[0]<<",1:"<<phase_count[1]<<"}"
      <<" middle-trailing="<<middle_trailing<<" positive-phase="<<guard_hits<<" max-middle-digits="<<max_middle_digits<<"\n";
  for(auto it:table){auto [a,b,g,c]=it.first;cout<<"EDGE "<<a<<" "<<b<<" "<<g<<" "<<c<<" "<<it.second<<"\n";}
  return 0;
 }catch(const exception&e){cerr<<"REJECT: "<<e.what()<<'\n';return 1;}
}
