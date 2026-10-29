// X05 independent-counter exact affine-RLE reverse-add, optional GMP oracle.
// No approximate signs; if an ordering is not uniform on A>=a0,B>=b0, fail closed.
#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <stdexcept>
#include <string>
#include <vector>
#include <gmpxx.h>
using namespace std;
struct Len {long long c,a,b;};
Len add(Len x,Len y){return {x.c+y.c,x.a+y.a,x.b+y.b};}
Len sub(Len x,Len y){return {x.c-y.c,x.a-y.a,x.b-y.b};}
bool zero(Len x){return x.c==0&&x.a==0&&x.b==0;}
bool unit(Len x){return x.c==1&&x.a==0&&x.b==0;}
long long value(Len x,long long A,long long B){return x.c+x.a*A+x.b*B;}
struct Run{int v;Len n;};
using Word=vector<Run>;
struct Engine {
 long long mina,minb;
 explicit Engine(long long a,long long b):mina(a),minb(b){}
 bool pos(Len x) const {return x.a>=0&&x.b>=0&&value(x,mina,minb)>0;}
 void append(Word &w,int v,Len n) const {
   if(zero(n))return;
   if(!pos(n))throw runtime_error("nonpositive or variable-sign length");
   if(!w.empty() && w.back().v==v)w.back().n=add(w.back().n,n);
   else w.push_back({v,n});
 }
 // Sign -1/0/1 of difference on the whole infinite parameter orthant.
 int sign(Len x) const {
  if(zero(x))return 0;
  if(x.a>=0&&x.b>=0&&value(x,mina,minb)>=0)return 1;
  if(x.a<=0&&x.b<=0&&value(x,mina,minb)<=0)return -1;
  throw runtime_error("ambiguous interval order across independent parameters");
 }
 Word initial()const{
  Word w;
  append(w,9,{1,1,0});append(w,18,{2,0,0});append(w,9,{0,0,1});
  append(w,0,{2,0,0});append(w,9,{0,0,1});append(w,18,{2,0,0});append(w,9,{1,1,0});
  return w;
 }
 Word norm(const Word& w,int base=10)const{
   Word d;int carry=0;
   for(const auto &r:w){
     if(unit(r.n)){
       int s=r.v+carry;append(d,s%base,{1,0,0});carry=s/base;
     } else if(r.v==base-1){
       append(d,(r.v+carry)%base,r.n);
     } else {
       int s=r.v+carry;int cc=s/base;
       append(d,s%base,{1,0,0});
       append(d,(r.v+cc)%base,sub(r.n,{1,0,0}));
       carry=cc;
     }
   }
   if(carry)append(d,carry,{1,0,0});
   while(!d.empty()&&d.back().v==0)d.pop_back();
   if(d.empty())throw runtime_error("zero source value");
   return d;
 }
 pair<Word,bool> pairword(const Word& d)const{
   Word out;bool palindrome=true;
   size_t i=0;long long j=(long long)d.size()-1;
   Len lo=d[i].n,hi=d[j].n;
   while(i<d.size()&&j>=0){
     int cmp=sign(sub(lo,hi));
     Len use=cmp<=0?lo:hi;
     if(!pos(use))throw runtime_error("nonpositive zipper interval");
     if(d[i].v!=d[j].v)palindrome=false;
     append(out,d[i].v+d[j].v,use);
     lo=sub(lo,use);hi=sub(hi,use);
     if(zero(lo)){++i;if(i<d.size())lo=d[i].n;}
     if(zero(hi)){--j;if(j>=0)hi=d[j].n;}
   }
   if(!(i==d.size()&&j==-1))throw runtime_error("zip mismatch");
   return {move(out),palindrome};
 }
 long long length(const Word&w)const{long long s=0;for(auto &r:w)s+=value(r.n,mina,minb);return s;}
};

// Oracle 1: normalize expanded coefficient word, completely independent of
// affine zipper. No symbolic run skipping for the arithmetic comparison.
string expanded_normal(const Word& w,long long A,long long B){
 string digits;digits.reserve(2*(A+B)+40000);int carry=0;
 for(auto &r:w){
  long long n=value(r.n,A,B);
  if(n<0||n>2000000)throw runtime_error("bad concrete length");
  for(long long k=0;k<n;k++){
   int x=r.v+carry;digits.push_back(char('0'+x%10));carry=x/10;
  }
 }
 if(carry)digits.push_back(char('0'+carry));
 while(digits.size()>1&&digits.back()=='0')digits.pop_back();
 reverse(digits.begin(),digits.end());
 return digits;
}

// Oracle 2: actual arbitrary-precision integer reverse-add with GMP. This
// computes reverse(N) from a fresh decimal conversion, not from pairwords.
mpz_class reverse_decimal_number(const string& msd){
 string r(msd.rbegin(),msd.rend());
 mpz_class v; if(mpz_set_str(v.get_mpz_t(),r.c_str(),10)!=0)throw runtime_error("GMP parse");
 return v;
}
int main(int argc,char**argv){
  int steps=argc>1?atoi(argv[1]):2000;
  int a0=argc>2?atoi(argv[2]):10000;
  int b0=argc>3?atoi(argv[3]):10000;
  bool oracle=argc>4?atoi(argv[4])!=0:false;
  int A=argc>5?atoi(argv[5]):a0;
  int B=argc>6?atoi(argv[6]):b0+17;
  Engine engine(a0,b0);Word w=engine.initial();
  mpz_class n;
  if(oracle){string s=expanded_normal(w,A,B);if(mpz_set_str(n.get_mpz_t(),s.c_str(),10)!=0)throw runtime_error("initial GMP parse");}
  long long global_start=0;
  string input=argc>7?argv[7]:"-";
  string output=argc>8?argv[8]:"-";
  if(input!="-"){
    ifstream f(input); if(!f)throw runtime_error("checkpoint input missing");
    int sa,sb,sA,sB;size_t nr;string num;
    f>>global_start>>sa>>sb>>sA>>sB>>num>>nr;
    if(!f||sa!=a0||sb!=b0||sA!=A||sB!=B)throw runtime_error("checkpoint parameters mismatch");
    if(oracle && mpz_set_str(n.get_mpz_t(),num.c_str(),10)!=0)throw runtime_error("checkpoint GMP parse");
    w.clear();w.reserve(nr);
    for(size_t k=0;k<nr;k++){Run x;f>>x.v>>x.n.c>>x.n.a>>x.n.b;w.push_back(x);}
    if(!f)throw runtime_error("checkpoint input truncated");
  }
  auto start=chrono::steady_clock::now();
  for(int t=0;t<steps;t++){
     if(oracle){
        string expected=expanded_normal(w,A,B);
        string got=n.get_str();
        if(expected!=got)throw runtime_error("INDEPENDENT BIGINT PAIRWORD MISMATCH AT t="+to_string(global_start+t));
        string backwards(got.rbegin(),got.rend());
        if(backwards==got)throw runtime_error("INDEPENDENT PALINDROME t="+to_string(global_start+t));
        n+=reverse_decimal_number(got);
     }
     Word d=engine.norm(w);
     auto nxt=engine.pairword(d);
     if(nxt.second)throw runtime_error("SYMBOLIC PALINDROME t="+to_string(global_start+t));
     w=move(nxt.first);
     if(t<3 || (t+1)%250==0){
       auto dur=chrono::duration_cast<chrono::milliseconds>(chrono::steady_clock::now()-start).count();
       cout<<"step="<<(global_start+t+1)<<" runs="<<w.size()<<" min_len="<<engine.length(w)<<" secs="<<(dur/1000.0)<<"\n"<<flush;
     }
  }
  if(oracle){
    string got=n.get_str(),expected=expanded_normal(w,A,B);
    if(got!=expected)throw runtime_error("INDEPENDENT BIGINT FINAL MISMATCH");
    cout<<"INDEPENDENT_GMP_REPLAY_OK "<<steps<<" decimal digits="<<got.size()<<"\n";
  }
  if(output!="-"){
     ofstream f(output);if(!f)throw runtime_error("checkpoint output open");
     f<<(global_start+steps)<<" "<<a0<<" "<<b0<<" "<<A<<" "<<B<<" "<<(oracle?n.get_str():"0")<<" "<<w.size()<<"\n";
     for(auto &r:w)f<<r.v<<" "<<r.n.c<<" "<<r.n.a<<" "<<r.n.b<<"\n";
     if(!f)throw runtime_error("checkpoint output failed");
  }
  cout<<"SYMBOLIC_ALL_PARAMETER_STEPS_OK "<<(global_start+steps)<<"\n";
}
