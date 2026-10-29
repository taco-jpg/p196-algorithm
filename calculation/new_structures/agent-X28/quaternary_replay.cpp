// agent-X28: independent decimal digit-array/GMP arithmetic of scaled base-4 W_r.
// g++ -std=c++17 -O3 quaternary_replay.cpp -lgmpxx -lgmp -o quaternary_replay
// ./quaternary_replay 12062 20000
#include <gmpxx.h>
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
uint64_t fnv(const string &s){uint64_t h=14695981039346656037ull;for(unsigned char c:s){h^=c;h*=1099511628211ull;}return h;}
string canon(const vector<unsigned char>&d){string s;s.reserve(d.size());for(auto x:d)s.push_back(char('0'+x));reverse(s.begin(),s.end());return s;}
vector<unsigned char> step(const vector<unsigned char>&d){int c=0;vector<unsigned char> o;o.reserve(d.size()+1);for(size_t i=0;i<d.size();++i){int z=int(d[i])+int(d[d.size()-1-i])+c;o.push_back(z%10);c=z/10;}if(c)o.push_back(c);return o;}
pair<size_t,int> max_run(const vector<unsigned char>& d, int value){size_t run=0,best=0;int blocks=0;for(size_t i=0;i<d.size();++i){int z=d[i]+d[d.size()-1-i]; if(z==value){++run;}else{if(run>best){best=run;blocks=1;}else if(run==best && run){blocks++;}run=0;}}if(run>best){best=run;blocks=1;}else if(run==best&&run)blocks++;return {best,blocks};}
int main(int argc,char**argv){int r=argc>1?atoi(argv[1]):12062,T=argc>2?atoi(argv[2]):20000;assert(r>=30);vector<unsigned char>d;
 for(int i=0;i<r;i++)d.push_back(0); d.push_back(9);d.push_back(6);for(int i=0;i<r;i++)d.push_back(9);d.push_back(0);d.push_back(3);
 string s=canon(d);mpz_class n(s,10),rv;int zeroRunMin=INT32_MAX,nineRunMin=INT32_MAX;int zeroFail=-1,nineFail=-1;
 for(int t=0;t<=T;t++){
   s=canon(d);string big=n.get_str(10);if(big!=s){cerr<<"DISAGREEMENT t="<<t<<"\n";return 2;}
   if(d==vector<unsigned char>(d.rbegin(),d.rend())){cerr<<"PALINDROME t="<<t<<"\n";return 3;}
   auto [z,nzb]=max_run(d,t<18?9:0);
   if(t<18){nineRunMin=min(nineRunMin,(int)z);if(nzb<2&&nineFail<0)nineFail=t;}else{zeroRunMin=min(zeroRunMin,(int)z);if(nzb<2&&zeroFail<0)zeroFail=t;}
   if(t==0||t==1||t==17||t==18||t==19||t==20||t==21||t==100||t==1000||t==5000||t==10000||t==15000||t==20000||t==T){cout<<"CHECK t="<<t<<" length="<<d.size()<<" pair_run_value="<<(t<18?9:0)<<" longest="<<z<<" max_run_blocks="<<nzb<<" fnv64="<<hex<<fnv(s)<<dec<<"\n";}
   if(t==T)break;
   string rev=big;reverse(rev.begin(),rev.end());rv=mpz_class(rev,10);n+=rv;d=step(d);
 }
 cout<<"SUCCESS r="<<r<<" T="<<T<<" nine_min="<<nineRunMin<<" zero_min="<<zeroRunMin<<" nine_blocks_failure="<<nineFail<<" zero_blocks_failure="<<zeroFail<<" final_len="<<d.size()<<" final_fnv64="<<hex<<fnv(canon(d))<<dec<<"\n";
 if(nineFail>=0||zeroFail>=0)return 4;
 return 0;
}
