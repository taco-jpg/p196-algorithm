// Independent decimal integer arithmetic and bounded-carry local checks (no Python).
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>
using V=std::vector<unsigned char>;
static V morph(int h){V w{14};for(int j=0;j<h;++j){V z;z.reserve(w.size()*2);for(auto x:w){z.push_back(x);z.push_back(30-x);}w.swap(z);}return w;}
static V seed(int h){auto w=morph(h);int n=2*(int(w.size())+1);V d(n,0);d[0]=0;d[n-1]=4;for(int i=1;i<n/2;++i){d[i]=w[i-1]-9;d[n-1-i]=9;}return d;}
static V addrev(const V&d){V q;q.reserve(d.size()+1);int c=0,n=d.size();for(int i=0;i<n;++i){int v=d[i]+d[n-1-i]+c;q.push_back(v%10);c=v/10;}if(c)q.push_back(c);while(q.size()>1&&q.back()==0)q.pop_back();return q;}
static V pair(const V&d){V p(d.size());for(int i=0;i<int(d.size());++i)p[i]=d[i]+d[d.size()-1-i];return p;}
static int carry(const V&p,int i,int dir){for(int j=0;j<2;++j,i+=dir){if(i<0||i>=int(p.size()))throw std::runtime_error("bad-boundary");if(p[i]!=9)return p[i]>=10;}throw std::runtime_error("two-neutral-run");}
static int max9(const V&p){int k=0,m=0;for(auto x:p){k=x==9?k+1:0;m=std::max(m,k);}return m;}
static bool pal(const V&d){return std::equal(d.begin(),d.end(),d.rbegin());}
static std::array<int,3> witness(const V&d){for(int i=0;i<int(d.size())/2;++i){if(d[i]!=d[d.size()-1-i])return {i,d[i],d[d.size()-1-i]};}return {-1,0,0};}
int main(){const char*schedule="011000010101001";int bulk=0,mutants=0;for(int h=2;h<=18;++h){V d=seed(h);assert(!pal(d));for(int t=0;t<15;++t){V p=pair(d);V e=addrev(d);V q=pair(e);int gamma=int(e.size())-int(d.size());if(gamma!=schedule[t]-'0'){std::cerr<<"gamma mismatch h="<<h<<" t="<<t<<"\n";return 1;}if(pal(e)){std::cerr<<"PALINDROME at h="<<h<<" t="<<t+1<<"\n";return 1;}
if(t>=3){if(max9(p)>1){std::cerr<<"neutral run h="<<h<<" t="<<t<<"\n";return 1;}
int half=int(p.size())/2;for(int i=3;i<half-3;++i){int low=(p[i]+carry(p,i-1,-1))%10;int high=(gamma==0? p[i]+carry(p,i+1,+1) : p[i-1]+carry(p,i,+1))%10;int v=low+high;if(q[i]!=v){std::cerr<<"predicted discrepancy h="<<h<<" t="<<t<<" i="<<i<<"\n";return 1;}++bulk;}
if(half>8){int i=half/2;int lower=carry(p,i-1,-1);int upper=gamma==0?carry(p,i+1,+1):carry(p,i,+1);int v=(p[i]+lower)%10+((gamma==0?p[i]:p[i-1])+upper)%10;assert(v==q[i]);assert(((v+1)%19)!=q[i]);++mutants;}}
d.swap(e);
}}
std::cout<<"INDEPENDENT_DECIMAL_BOUND_RUN_PASS levels=2..18 steps=15 bulk_cell_checks="<<bulk<<" mutation_rejections="<<mutants<<"\n";
}
