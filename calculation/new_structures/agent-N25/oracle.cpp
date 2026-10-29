// agent-N25: independently computed base-1,000,000,000 multi-precision integer reverse-and-add.
// Avoids the direct kernel's per-digit decimal carry loop entirely.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
static constexpr uint64_t RADIX=1000000000ULL;
using Big=vector<uint32_t>; // least significant 9-digit limb first
static Big parse(const string &s){Big a;for(size_t e=s.size();e;){size_t b=e>9?e-9:0;a.push_back(stoul(s.substr(b,e-b)));e=b;}while(a.size()>1&&a.back()==0)a.pop_back();return a;}
static string format(const Big &a){string s=to_string(a.back());for(size_t i=a.size()-1;i;--i){auto x=to_string(a[i-1]);s.append(9-x.size(),'0');s+=x;}return s;}
static Big add(const Big &a,const Big &b){Big out;size_t n=max(a.size(),b.size());uint64_t c=0;for(size_t i=0;i<n;i++){uint64_t v=c+(i<a.size()?a[i]:0)+(i<b.size()?b[i]:0);out.push_back(uint32_t(v%RADIX));c=v/RADIX;}if(c)out.push_back(uint32_t(c));return out;}
static uint64_t fnv(const string&s){uint64_t h=14695981039346656037ULL;for(char c:s){h^=(unsigned char)c;h*=1099511628211ULL;}return h;}
static string makeSeed(size_t g){return string("1789")+string(g,'0')+"3141"+string(g,'0')+"5926"+string(g,'0')+"5358";}
static void verify(const string &s,size_t gap,size_t step,size_t overflows){
 if(s.size()!=16+3*gap+overflows)throw runtime_error("length mismatch");
 for(size_t i=0,j=s.size()-1;i<j;i++,j--)if(s[i]!=s[j])goto not_pal;
 throw runtime_error("palindrome step="+to_string(step));
 not_pal: ;
 size_t w=gap-2*step+overflows;size_t pos[3]={4,8+gap,12+2*gap};
 for(auto p:pos){size_t l=p+step,r=s.size()-p-step-w;
  if(l+w>s.size()||r+w>s.size())throw runtime_error("bad interval");
  for(size_t k=0;k<w;k++)if(s[l+k]!='0'||s[r+k]!='0')throw runtime_error("nonzero protected interior");
 }
}
int main(int argc,char**argv){if(argc!=5){cerr<<"usage: oracle STEPS GAP TRACE FINAL\n";return 2;}size_t T=stoull(argv[1]),gap=stoull(argv[2]);if(gap<=2*T)return 2;
 Big a=parse(makeSeed(gap));ofstream f(argv[3]);size_t ov=0,oldlen=16+3*gap;
 for(size_t t=0;t<=T;t++){
  auto s=format(a);if(s.size()!=oldlen)throw runtime_error("next wrong length");verify(s,gap,t,ov);
  f<<t<<'\t'<<s.size()<<'\t'<<ov<<'\t'<<hex<<fnv(s)<<dec<<'\t'<<s.substr(0,12)<<'\t'<<s.substr(s.size()-12)<<'\n';
  if(t==T){ofstream last(argv[4]);last<<s<<'\n';cout<<"ORACLE PASS steps="<<T<<" gap="<<gap<<" length="<<s.size()<<" overflows="<<ov<<" firewall_min="<<gap-2*T+ov<<" fnv="<<hex<<fnv(s)<<dec<<"\n";break;}
  reverse(s.begin(),s.end());Big reversed=parse(s);
  a=add(a,reversed);size_t newlen=format(a).size();ov+=(newlen>oldlen);oldlen=newlen;
 }
}
