// Completely separate GMP integer replay, not using the packet recurrence.
// Build: g++ -O2 -std=c++17 independent_gmp.cpp -lgmpxx -lgmp -o independent_gmp
#include <gmpxx.h>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <stdexcept>
#include <cstdint>
using namespace std;
static uint64_t hash64(const string&s){uint64_t h=14695981039346656037ULL;for(unsigned char c:s){h^=c;h*=1099511628211ULL;}return h;}
static string pword(const string&s){string p(s.size(),'A');for(size_t i=0;i<s.size();i++)p[i]='A'+(s[i]-'0')+(s[s.size()-i-1]-'0');return p;}
static bool ispal(const string&s){for(size_t i=0;i<s.size()/2;i++)if(s[i]!=s[s.size()-1-i])return false;return true;}
int main(int argc,char**argv){
 try{
   if(argc!=7&&argc!=8)throw runtime_error("usage: independent_gmp Q END_STEP OUTPUT.tsv END_STATE.txt TOP MIDDLE [START_STATE.txt]");
   long long q=stoll(argv[1]),end=stoll(argv[2]);
   if(q<3||end<0)throw runtime_error("bad q or end");
   string first=argv[5],middle=argv[6],last="75";
   string w=first+string(q-1,'0')+middle+string(q-2,'0')+last;
   long long begin=0;
   if(argc==8){ifstream in(argv[7]);if(!in)throw runtime_error("cannot read starting state");in>>begin>>w;}
   mpz_class n(w,10);ofstream out(argv[3]);
   out<<"t\tdigits\tword_fnv64\tpair_fnv64\n";
   for(long long t=begin;t<=end;t++){
      string s=n.get_str();
      if(ispal(s))throw runtime_error("found palindrome at step "+to_string(t));
      if(t%1000==0||t==end){out<<t<<'\t'<<s.size()<<'\t'<<hex<<hash64(s)<<'\t'<<hash64(pword(s))<<dec<<'\n';out.flush();}
      if(t==end)break;
      string r=s;reverse(r.begin(),r.end());n+=mpz_class(r,10);
   }
   ofstream state(argv[4]);state<<end<<'\n'<<n.get_str()<<'\n';
   cerr<<"INDEPENDENT-GMP PASS end="<<end<<" digits="<<n.get_str().size()<<"\n";
 }catch(const exception&e){cerr<<"FAIL: "<<e.what()<<'\n';return 1;}
}
