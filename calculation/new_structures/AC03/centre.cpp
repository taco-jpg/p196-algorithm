// AC03: exact phase-0 rooted decimal centre-window census (LSD-first pair coefficients).
// The incoming cut carries are certified separately by abstract.py.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
using V=std::vector<uint8_t>;
const V B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
const V W={5,18,4,8,1,15,4,0,5};
const std::array<V,3> Us={V{9,4,14},V{4,14,9},V{14,9,4}};
const V J={5};
const int Q=14,K=100,steps=120;
void append(V&a,const V&b){a.insert(a.end(),b.begin(),b.end());}
V templ(const V&C,int u,int k=K){V h=B;for(int i=0;i<Q;i++)append(h,W);append(h,J);for(int i=0;i<k;i++)append(h,Us[u]);V p=h;append(p,C);for(auto it=h.rbegin();it!=h.rend();++it)p.push_back(*it);return p;}
V centre(uint64_t id,int len){V c(len);for(int i=0;i<len/2;i++){c[i]=c[len-1-i]=id%19;id/=19;}if(len&1){c[len/2]=2*(id%10);id/=10;}if(id)throw std::runtime_error("centre out of range");return c;}
uint64_t count(int len){uint64_t v=1;for(int i=0;i<len/2;i++)v*=19;if(len&1)v*=10;return v;}
V next(const V&p,int&overflow){V d(p.size());int c=0;for(size_t i=0;i<p.size();i++){int z=p[i]+c;d[i]=z%10;c=z/10;}overflow=c;if(c)d.push_back(c);V z(d.size());for(size_t i=0;i<d.size();i++)z[i]=d[i]+d[d.size()-1-i];return z;}
int port(const V&p,size_t start){int c=0;for(size_t i=0;i<start;i++)c=(p[i]+c)/10;return c;}
struct Baseline{std::array<int,steps> gam{},port{};int source_n=0,s0=280;};
Baseline baseline(int u,int l){V C(l,0),p=templ(C,u);Baseline b;b.source_n=p.size();for(int t=0;t<steps;t++){b.port[t]=port(p,b.s0+t);p=next(p,b.gam[t]);}return b;}
V localnext(const V&p,int incoming,int gamma){const int n=p.size();if(n<=4)throw std::runtime_error("local window exhausted");V d(n);int c=incoming;for(int i=0;i<n;i++){int z=p[i]+c;d[i]=z%10;c=z/10;}V z(n+gamma-2);for(int a=0;a<(int)z.size();a++){int j=a+1,rev=n+gamma-1-j;z[a]=d[j]+d[rev];}return z;}
struct Result{bool match;int first,err,actual,expected;};
Result check(const V&C,int u,const Baseline&b,bool full=false){V p=templ(C,u),want=templ(C,u,K+5);if((int)p.size()!=b.source_n)throw std::runtime_error("source length");V a(p.begin()+b.s0,p.end()-b.s0);int sum=0;
for(int t=0;t<steps;t++){if(full){if(a!=V(p.begin()+b.s0+t,p.end()-b.s0-t))return {false,t,1,0,0};if(port(p,b.s0+t)!=b.port[t])return {false,t,2,port(p,b.s0+t),b.port[t]};}
a=localnext(a,b.port[t],b.gam[t]);sum+=b.gam[t];if(full){int g=0;p=next(p,g);if(g!=b.gam[t])return {false,t,3,g,b.gam[t]};}}
if(sum!=30)throw std::runtime_error("bad overflow clock");int sf=b.s0+steps;V tar(want.begin()+sf,want.end()-sf);if(a.size()!=tar.size())return {false,-1,4,(int)a.size(),(int)tar.size()};for(int i=0;i<(int)a.size();i++)if(a[i]!=tar[i])return {false,i,0,a[i],tar[i]};return {true,-1,0,0,0};}
int main(int argc,char**argv){if(argc<2){std::cerr<<"usage: centre [scan|validate|inspect] [len] [U:0/1/2] [start] [end]\n";return 2;}
std::string cmd=argv[1];int len=argc>2?atoi(argv[2]):7,u=argc>3?atoi(argv[3]):0;if(len<1||len>24||u<0||u>2)throw std::runtime_error("bad args");auto b=baseline(u,len);
if(cmd=="inspect"){std::cout<<"n="<<b.source_n<<" cut="<<b.s0<<" gam=";for(auto z:b.gam)std::cout<<z;std::cout<<" ports=";for(auto z:b.port)std::cout<<z;std::cout<<"\n";return 0;}
uint64_t n=count(len),lo=argc>4?strtoull(argv[4],nullptr,10):0,hi=argc>5?strtoull(argv[5],nullptr,10):n;hi=std::min(hi,n);if(lo>hi)throw std::runtime_error("range");
uint64_t hits=0,portbad=0;std::map<int,uint64_t> mis;auto t0=std::chrono::steady_clock::now();
for(uint64_t id=lo;id<hi;id++){V c=centre(id,len);Result r=check(c,u,b,cmd=="validate");
if(r.err){if(portbad<5)std::cerr<<"PORT-ERROR len="<<len<<" u="<<u<<" id="<<id<<" t="<<r.first<<" code="<<r.err<<" actual="<<r.actual<<" exp="<<r.expected<<"\n";portbad++;}
if(r.match){hits++;if(hits<10){std::cout<<"HIT len="<<len<<" u="<<u<<" id="<<id<<" C=";for(int x:c)std::cout<<x<<",";std::cout<<"\n";}}else mis[r.first]++;}
double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count();
std::cout<<"CELL len="<<len<<" U="<<u<<" cases="<<hi-lo<<" total="<<n<<" hits="<<hits<<" port_errors="<<portbad<<" seconds="<<sec<<" first_mismatches=";for(auto [k,v]:mis)std::cout<<k<<":"<<v<<",";std::cout<<"\n";
}
