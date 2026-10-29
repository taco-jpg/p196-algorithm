// Independent GMP arbitrary-precision arithmetic, separate from digit-vector kernel.
// Reproduce baseline: ./gmp_check calculation/new_structures/agent-N16/rows.txt 300 14000 20000 --single
// Reproduce full quartet (short control): ./gmp_check calculation/new_structures/agent-N16/rows.txt 300 14000 2000
#include <gmp.h>
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
static vector<string>B(8),W(8);
static int cv(char c){return c<='9'?c-'0':c-'A'+10;}
static string seed(int q,int z){
 vector<int> p;for(char c:B[0])p.push_back(cv(c));
 for(int k=0;k<q;k++)for(char c:W[0])p.push_back(cv(c));
 p.insert(p.end(),z,0);int left=39+20*q;
 for(int j=left-1;j>=0;j--)p.push_back(p[j]);
 int n=p.size();string s(n,'0');for(int j=0;j<n/2;j++){s[n-1-j]=char('0'+max(0,p[j]-9));s[j]=char('0'+min(9,p[j]));}if(n&1)s[n/2]=char('0'+p[n/2]/2);return s;
}
static string textnum(const mpz_t x){string s(mpz_sizeinbase(x,10)+3,'\0');mpz_get_str(s.data(),10,x);s.resize(strlen(s.c_str()));return s;}
static void advance(mpz_t x){string s=textnum(x);reverse(s.begin(),s.end());mpz_t r;mpz_init(r);if(mpz_set_str(r,s.c_str(),10))abort();mpz_add(x,x,r);mpz_clear(r);}
static string pairs(const string&s){int n=s.size();string p(n,'0');for(int i=0;i<n;i++)p[i]=char('A'+s[i]-'0'+s[n-1-i]-'0');return p;}
static string wpump(const string&p,int t){string v=p.substr(0,39);for(char c:W[t%8])v+=char('A'+cv(c));v+=p.substr(39,p.size()-78);for(auto it=W[t%8].rbegin();it!=W[t%8].rend();it++)v+=char('A'+cv(*it));v+=p.substr(p.size()-39);return v;}
static string zpump(string p){p.insert(p.begin()+p.size()/2,'A');return p;}
static int zerorun(const string&p){int n=p.size(),i=n/2-1;if(n%2 && p[i+1]!='A')return 0;int cnt=0;while(i>=0&&p[i]=='A'){cnt++;i--;}return 2*cnt+(n%2);}
static uint64_t FNV=1469598103934665603ULL;
static void add(uint64_t x){FNV^=x;FNV*=1099511628211ULL;}
int main(int argc,char**argv){string rows=argc>1?argv[1]:"calculation/new_structures/agent-N16/rows.txt";int q=argc>2?atoi(argv[2]):300,z=argc>3?atoi(argv[3]):14000,T=argc>4?atoi(argv[4]):20000;bool single=argc>5&&string(argv[5])=="--single";ifstream f(rows);if(!f)return 2;string hdr;getline(f,hdr);for(int j=0;j<8;j++)getline(f,B[j]);for(int j=0;j<8;j++)getline(f,W[j]);if(B[0].size()!=39||W[0].size()!=20)return 3;
 mpz_t x[4];for(int i=0;i<(single?1:4);i++){mpz_init(x[i]);auto s=seed(q+(i&1),z+(i>=2));if(mpz_set_str(x[i],s.c_str(),10))return 4;}
 int minpre=1000000,minzero=1000000;for(int t=0;t<=T;t++){
   string s[4],p[4];for(int i=0;i<(single?1:4);i++){s[i]=textnum(x[i]);p[i]=pairs(s[i]);}
   if(!single&&(wpump(p[0],t)!=p[1]||zpump(p[0])!=p[2]||wpump(p[2],t)!=p[3]||zpump(p[1])!=p[3])){cerr<<"FAIL pump "<<t<<"\n";return 5;}
   int pr=0;while(pr<(int)p[0].size()/2){int exp=pr<39?cv(B[t%8][pr]):cv(W[t%8][(pr-39)%20]);if(p[0][pr]!=char('A'+exp))break;pr++;}
   int zero=zerorun(p[0]);minpre=min(minpre,pr);minzero=min(minzero,zero);
   for(int i=0;i<(single?1:4);i++)if(s[i]==string(s[i].rbegin(),s[i].rend())){cerr<<"PAL "<<t<<"\n";return 6;}
   add(t);add(s[0].size());add(pr);add(zero);for(int j=0;j<16;j++)add(p[0][j]-'A');
   if(t==T)break;for(int i=0;i<(single?1:4);i++)advance(x[i]);
 }
 cerr<<"GMP_PASS q="<<q<<" z="<<z<<" steps="<<T<<" min_prefix="<<minpre<<" min_zero="<<minzero<<" fnv="<<hex<<FNV<<dec<<"\n";
 for(int i=0;i<(single?1:4);i++)mpz_clear(x[i]);return 0;
}
