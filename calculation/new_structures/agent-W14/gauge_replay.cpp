// W14 modular local gauge and ordinary-integer 20,000-step replay.
// g++ -O3 -std=c++17 gauge_replay.cpp -lgmp -o gauge_replay && ./gauge_replay rows.txt 300 20000
#include <gmp.h>
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
static int cv(char c){if(c>='0'&&c<='9')return c-'0';if(c>='A'&&c<='I')return c-'A'+10;throw runtime_error("bad base19");}
struct Rows {vector<vector<int>> B,W; Rows(string path){ifstream f(path);if(!f)throw runtime_error("no rows");string s;while(f>>s){if(s[0]=='#'){getline(f,s);continue;} vector<int>v;for(char c:s)v.push_back(cv(c));if(B.size()<8){if(v.size()!=39)throw runtime_error("B width");B.push_back(v);}else {if(v.size()!=20)throw runtime_error("W width");W.push_back(v);}}if(B.size()!=8||W.size()!=8)throw runtime_error("row count");}};
static vector<int> half(const Rows&r,int q){vector<int>a=r.B[0];for(int j=0;j<q;j++)a.insert(a.end(),r.W[0].begin(),r.W[0].end());return a;}
static vector<int> safe(const vector<int>&a){vector<int>s;for(int i=1;i+1<(int)a.size();i++)if(a[i]!=0&&a[i]!=9&&a[i]!=18&&a[i-1]!=9&&a[i+1]!=9)s.push_back(i);return s;}
static uint64_t mix(uint64_t z){z+=0x9e3779b97f4a7c15ull;z=(z^(z>>30))*0xbf58476d1ce4e5b9ull;z=(z^(z>>27))*0x94d049bb133111ebull;return z^(z>>31);}
static vector<int> gauge(const vector<int>&a, const vector<int>&s){auto m=a;for(int i:s)if(mix((uint64_t)i+714614ull)&1)m[i]+=(m[i]<9?9:-9);return m;}
static vector<int> seed_digits(const vector<int>&a){int h=a.size();vector<int>d(2*h);for(int i=0;i<h;i++){d[i]=max(0,a[i]-9);d[2*h-1-i]=min(9,a[i]);}if(d.back()==0)throw runtime_error("leading zero");return d;}
static string decimal(const vector<int>&d){string s;for(int i=int(d.size())-1;i>=0;i--)s.push_back(char('0'+d[i]));return s;}
static vector<int> school_step(const vector<int>&d){int n=d.size(),c=0;vector<int>v(n+1);for(int i=0;i<n;i++){int z=d[i]+d[n-1-i]+c;v[i]=z%10;c=z/10;}if(c)v[n]=c;else v.pop_back();return v;}
static void gmp_step(mpz_t n){char* raw=mpz_get_str(nullptr,10,n);string s(raw);void(*freefn)(void*,size_t);mp_get_memory_functions(nullptr,nullptr,&freefn);freefn(raw,s.size()+1);reverse(s.begin(),s.end()); // leading zeroes acceptable for parsed reverse
 mpz_t r;mpz_init(r);if(mpz_set_str(r,s.c_str(),10))throw runtime_error("parse reverse");mpz_add(n,n,r);mpz_clear(r);}
static int match_prefix(const vector<int>&d,const Rows&r,int t,int q){int n=d.size(),match=0;for(int i=0;i<(int)r.B[0].size()+20*q&&i<n/2;i++){int target=i<39?r.B[t%8][i]:r.W[t%8][(i-39)%20];if(d[i]+d[n-1-i]!=target)break;match++;}return match;}
static bool palindrome(const vector<int>&d){for(int i=0,j=int(d.size())-1;i<j;i++,j--)if(d[i]!=d[j])return false;return true;}
int main(int argc,char**argv){try{
 if(argc!=4){cerr<<"usage: ./gauge_replay rows.txt 300 20000\n";return 2;}Rows r(argv[1]);int q=stoi(argv[2]), H=stoi(argv[3]);if(q<1||H<2)return 2;
 auto base=half(r,q);auto S=safe(base);auto mutant=gauge(base,S);auto db=seed_digits(base),dm=seed_digits(mutant);int flips=0;for(int i:S)flips+=(base[i]!=mutant[i]);
 cout<<"q="<<q<<" coeff-half="<<base.size()<<" gauge_free="<<S.size()<<" deterministic_flips="<<flips<<" seed_digits="<<db.size()<<"\n";
 if(q==300&&S.size()!=4518)throw runtime_error("unexpected gauge freedom count");
 auto base1=school_step(db),mut1=school_step(dm),base2=school_step(base1),mut2=school_step(mut1);
 if(db==dm || base1==mut1 || base2!=mut2)throw runtime_error("gauge convergence failure");
 cout<<"two-step exact schoolbook convergence PASS; first-step difference="<<(base1!=mut1)<<"\n";
 string n0=decimal(dm);mpz_t n;mpz_init(n);if(mpz_set_str(n,n0.c_str(),10))throw runtime_error("bad seed");
 vector<int>d=dm;int minprefix=INT32_MAX;uint64_t hash=1469598103934665603ull;
 for(int t=0;t<=H;t++){
   if(d.back()==0||palindrome(d))throw runtime_error("palindrome or leading zero at "+to_string(t));
   int z=match_prefix(d,r,t,q);if(t>=1)minprefix=min(minprefix,z);
   if(t>=1&&z<39)throw runtime_error("rooted exterior lost at "+to_string(t));
   if(t>=1&&q==300&&H==20000 &&z<39+72*20)throw runtime_error("72 complete bands lost at "+to_string(t));
   auto s=decimal(d);
   char* raw=mpz_get_str(nullptr,10,n);string g(raw);void(*freefn)(void*,size_t);mp_get_memory_functions(nullptr,nullptr,&freefn);freefn(raw,g.size()+1);
   if(g!=s)throw runtime_error("GMP/schoolbook discrepancy at "+to_string(t));
   for(uint64_t x:{uint64_t(t),uint64_t(d.size()),uint64_t(z)}){hash^=x;hash*=1099511628211ull;}
   if(t==2 && d!=mut2)throw runtime_error("at t2 mismatch");
   if(t<H){int old=d.size();d=school_step(d);gmp_step(n);if(q==300&&H==20000 && (int)d.size()!=old+(t%2==0))throw runtime_error("overflow clock mismatch at "+to_string(t));}
 }
 mpz_clear(n);cout<<"PASS independent GMP and schoolbook digit-vector replay H="<<H<<" states="<<H+1<<" min_exact_lattice_prefix="<<minprefix<<" fnv64="<<hex<<hash<<dec<<" no palindromes\n";
 }catch(const exception&e){cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}
