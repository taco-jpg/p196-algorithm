// W07: four independent two-step pairword gates per period-20 block.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <random>
#include <vector>
using namespace std;using V=vector<int>;
const V B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
const V W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
V seedpair(int q){V h=B;for(int i=0;i<q;i++)h.insert(h.end(),W.begin(),W.end());V p=h;p.insert(p.end(),h.rbegin(),h.rend());return p;}
V apply(V p,int q,const vector<char>&bits){int n=p.size();assert((int)bits.size()==4*q+1);int idx=0;
 for(int k=0;k<q;k++)for(int j:{0,4,8,12}){
  int i=39+20*k+j;if(bits[idx++]){int s=p[i];int z=s>=9?s-9:s+9;p[i]=p[n-1-i]=z;}
 }
 if(bits[idx])p[n/2-1]=p[n/2]=4;
 return p;
}
V realize(const V&p){int n=p.size();V d(n);for(int i=0;i<n/2;i++){int lo=min(p[i],9);d[i]=lo;d[n-1-i]=p[i]-lo;}assert(d.back()!=0);return d;}
V step(const V&d){int n=d.size(),c=0;V out;out.reserve(n+1);for(int i=0;i<n;i++){int x=d[i]+d[n-1-i]+c;out.push_back(x%10);c=x/10;}if(c)out.push_back(c);return out;}
V pairword(const V&d){int n=d.size();V p(n);for(int i=0;i<n;i++)p[i]=d[i]+d[n-1-i];return p;}
V normalize(const V&p){int c=0;V v;for(int x:p){int r=x+c;v.push_back(r%10);c=r/10;}if(c)v.push_back(c);return v;}
uint64_t fnv(const V&d){uint64_t h=1469598103934665603ULL;for(int x:d){h^=x+1;h*=1099511628211ULL;}return h;}
int main(){mt19937_64 gen(4102831);int cases=0;
 for(int q:{1,2,3,4,10,300}){
  V p=seedpair(q);auto goal=pairword(step(realize(p)));int nbits=4*q+1;
  unsigned long long total=nbits<=17?(1ULL<<nbits):1024;
  for(unsigned long long k=0;k<total;k++){
   vector<char> bits(nbits);for(int i=0;i<nbits;i++)bits[i]=nbits<=17?((k>>i)&1):(gen()&1);
   V altered=apply(p,q,bits);
   V digit=normalize(altered);assert(digit==step(realize(altered)));
   assert(pairword(digit)==goal);
   cases++;
  }
  cout<<"q="<<q<<" masks="<<total<<" independent pairword merger PASS\n";
 }
 const int q=300;V p=seedpair(q);vector<char> bits(1201,1);V a=step(realize(apply(p,q,bits)));
 V b=step(realize(p));assert(a!=b && pairword(a)==pairword(b));
 assert(step(a)==step(b));
 cout<<"W07_MULTI_GATES_PASS cases="<<cases<<" q300 firsts_differ=1 seconds_identical=1 first_FNV="<<fnv(a)<<"\n";
}
