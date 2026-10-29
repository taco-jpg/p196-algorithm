// X07 one 20,001-step witness from the exponential mirror-gauge family.
// Independent GMP whole-integer engine + grade-school decimal digit engine +
// separate low-first scalar quotient engine at EVERY step.
// Requires: c++ -O3 -std=c++17 gmp_replay.cpp -lgmpxx -lgmp -o gmp_replay
#include <gmpxx.h>
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using V=vector<int>;
V toDigits(const string& s){V v;for(auto i=s.rbegin();i!=s.rend();i++)v.push_back(*i-'0');return v;}
string fromDigits(const V&v){string s;for(auto i=v.rbegin();i!=v.rend();i++)s+=char(*i+'0');return s;}
V school(const V&v){int c=0,n=v.size();V a;a.reserve(n+1);for(int i=0;i<n;i++){int z=v[i]+v[n-1-i]+c;a.push_back(z%10);c=z/10;}if(c)a.push_back(c);return a;}
V scalar(const V&q){int m=q.size(),b=0,c=1;V a(m),out;for(int i=0;i<m;i++){int z=-q[i]-b;if(z<0){z+=10;b=1;}else b=0;a[i]=z;}assert(b==1);for(int i=0;i<m;i++){int z=q[i]+a[m-1-i]+c;out.push_back(z%10);c=z/10;}if(c)out.push_back(c);return out;}
int main(int argc,char**argv){int h=argc>1?atoi(argv[1]):8278,T=argc>2?atoi(argv[2]):20001;const int m=10;const string A="6444444446"; // palindromic, 44 mod 9 = 8
  mpz_class pow10;mpz_ui_pow_ui(pow10.get_mpz_t(),10,h);mpz_class M=pow10-1;
  mpz_class q0("3555555554");assert(q0==mpz_class("10000000000")-mpz_class(A));
  mpz_class N=M*q0;V d=toDigits(N.get_str());V q=toDigits(q0.get_str());
  uint64_t hash=14695981039346656037ULL;
  for(int t=0;t<=T;t++){
    string s=N.get_str();if(s!=fromDigits(d)){cerr<<"ENGINE DISAGREEMENT "<<t<<"\n";return 3;}
    string r=s;reverse(r.begin(),r.end());if(s==r){cerr<<"PALINDROME "<<t<<"\n";return 4;}
    // Check whole integer against the *independent* quotient state.
    if(N!=M*mpz_class(fromDigits(q),10)){cerr<<"QUOTIENT DISAGREEMENT "<<t<<"\n";return 5;}
    if((int)q.size()>h){cerr<<"PROTECTED GUARD FAILED "<<t<<"\n";return 6;}
    for(int z:{(int)(s.size()%256),(int)(q.size()%256),t%256}){hash ^= z;hash*=1099511628211ULL;}
    if(t==T)break;
    V next=school(d);N+=mpz_class(r,10);d.swap(next);q=scalar(q);
    if(t==0||t==9999||t==T-1)cerr<<"checkpoint t="<<t+1<<" whole_digits="<<d.size()<<" quotient_digits="<<q.size()<<"\n";
  }
  cout<<"PASS A="<<A<<" h="<<h<<" steps="<<T<<" seed_digits="<<h+m<<" final_digits="<<d.size()<<" final_quotient_digits="<<q.size()<<" FNV64="<<hex<<hash<<dec<<"\n";
}
