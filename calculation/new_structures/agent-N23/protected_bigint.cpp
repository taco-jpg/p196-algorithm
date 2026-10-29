// Independent arbitrary-precision integers in base 1,000,000,000; reversal as ordinary decimal string.
#include <cstdint>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <string>
#include <iostream>
using namespace std;
static constexpr uint64_t B=1000000000ULL;
using Big=vector<uint32_t>;
static Big parse(const string&s){
 Big a;for(int end=(int)s.size();end>0;end-=9){int i=max(0,end-9);a.push_back((uint32_t)stoul(s.substr(i,end-i)));}
 while(a.size()>1&&a.back()==0)a.pop_back();return a;
}
static string render(const Big&a){
 string s=to_string(a.back());
 for(int i=(int)a.size()-2;i>=0;i--){string u=to_string(a[i]);s+=string(9-u.size(),'0')+u;}
 return s;
}
static Big add(const Big&a,const Big&b){
 Big c;int n=max(a.size(),b.size());c.reserve(n+1);uint64_t carry=0;
 for(int i=0;i<n;i++){uint64_t w=carry+(i<(int)a.size()?a[i]:0)+(i<(int)b.size()?b[i]:0);
 c.push_back((uint32_t)(w%B));carry=w/B;}
 if(carry)c.push_back((uint32_t)carry);return c;
}
int main(int argc,char**argv){
 int Q=(argc>1)?atoi(argv[1]):7000,steps=(argc>2)?atoi(argv[2]):20000;
 string seed="12"+string(2*Q,'9')+"34";Big N=parse(seed);
 int mincore=1<<30,first=0,last=0;uint64_t modhash=0;
 for(int t=0;t<=steps;t++){
  string s=render(N),r=s;reverse(r.begin(),r.end());
  if(s==r){cerr<<"PALINDROME at "<<t<<"\n";return 1;}
  int n=(int)s.size(),a=(n-1)/2,b=n/2,core=0;if(n%2){a=n/2;b=a;}
  while(a>=0&&b<n&&s[a]=='9'&&s[b]=='9'){core+=(a==b?1:2);a--;b++;}
  if(core<1000){cerr<<"band exhaust at t="<<t<<" core="<<core<<"\n";return 2;}
  if(t==0)first=core;if(t==steps)last=core;mincore=min(mincore,core);
  if(t==steps){
   for(char ch:s)modhash=(modhash*131+ch)%1000000007ULL;
   cout<<"PASS BIGINT limbs base=1e9 steps="<<steps<<" Q="<<Q<<" final_len="<<s.size()<<" core_first="<<first<<" core_final="<<last<<" mincore="<<mincore<<" checksum_mod1000000007="<<modhash<<"\n";break;
  }
  size_t i=r.find_first_not_of('0');if(i==string::npos)r="0";else r.erase(0,i);
  N=add(N,parse(r));
 }
}
