// agent-N25: independent ordinary decimal digit-list reverse-and-add.
// Reproduce: g++ -std=c++17 -O3 direct.cpp -o direct; ./direct 20000 40001 trace.tsv final.txt
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
static const string PACKETS[4]={"1789","3141","5926","5358"};
static string seed(size_t gap){return PACKETS[0]+string(gap,'0')+PACKETS[1]+string(gap,'0')+PACKETS[2]+string(gap,'0')+PACKETS[3];}
static uint64_t fnv(const string &s){uint64_t h=14695981039346656037ULL;for(unsigned char c:s){h^=c;h*=1099511628211ULL;}return h;}
static string step(const string &s){size_t n=s.size();string out(n,'0');int carry=0;for(size_t i=0;i<n;i++){int v=(s[n-1-i]-'0')+(s[i]-'0')+carry;out[n-1-i]=char('0'+v%10);carry=v/10;}if(carry)out.insert(out.begin(),'1');return out;}
static void verify(const string &s,size_t g,size_t t,size_t overflow){
 size_t N=s.size();size_t n0=16+3*g;
 if(N!=n0+overflow)throw runtime_error("length conservation");
 if(s==string(s.rbegin(),s.rend()))throw runtime_error("PALINDROME step="+to_string(t));
 // Three zero bands in MSB orientation, I0_i reflected in the same digit string.
 size_t start[3]={4,8+g,12+2*g};
 for(size_t k=0;k<3;k++){
  size_t a=start[k]+t, width=g-2*t+overflow;
  if(width==0 || a+width>N)throw runtime_error("protected sector exhausted");
  if(s.compare(a,width,string(width,'0'))!=0)throw runtime_error("carry-free firewall violation sector="+to_string(k)+" step="+to_string(t));
  // The mirror interval must also be zero.
  size_t mir=N-a-width;
  if(s.compare(mir,width,string(width,'0'))!=0)throw runtime_error("reflection violation");
 }
}
int main(int argc,char **argv){if(argc!=5){cerr<<"usage: direct STEPS GAP TRACE FINAL\n";return 2;}size_t T=stoull(argv[1]),g=stoull(argv[2]);if(g<=2*T){cerr<<"need GAP>2*STEPS\n";return 2;}
 string s=seed(g);ofstream f(argv[3]);if(!f)throw runtime_error("trace open");size_t ov=0;
 for(size_t t=0;t<=T;t++){
  verify(s,g,t,ov);
  f<<t<<'\t'<<s.size()<<'\t'<<ov<<'\t'<<hex<<fnv(s)<<dec<<'\t'<<s.substr(0,12)<<'\t'<<s.substr(s.size()-12)<<'\n';
  if(t==T)break;
  auto next=step(s);ov+=(next.size()>s.size());s=std::move(next);
 }
 ofstream last(argv[4]);last<<s<<'\n';
 cout<<"DIRECT PASS steps="<<T<<" gap="<<g<<" length="<<s.size()<<" overflows="<<ov<<" firewall_min="<<g-2*T+ov<<" fnv="<<hex<<fnv(s)<<dec<<"\n";
}
