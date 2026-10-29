// W07: literal decimal-digit reverse-and-add with rooted pairword guard.
// No coefficient normalizer is used to advance the actual integer orbit.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;
using V=vector<int>;
static const V B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const V W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
V initial_pairword(int q){
 V h=B;for(int j=0;j<q;j++)h.insert(h.end(),W.begin(),W.end());
 V p=h;p.insert(p.end(),h.rbegin(),h.rend());return p;
}
V realize(int q,bool toggle){
 V p=initial_pairword(q);int n=p.size();V d(n);
 for(int i=0;i<n/2;i++){
  int x=p[i],low=min(x,9),high=x-low;
  if(toggle && i>=39 && i<39+20*q && x==1){low=0;high=1;}
  d[i]=low;d[n-1-i]=high;
 }
 assert(d.back()!=0);return d;
}
V step(const V&d){
 int n=d.size(),carry=0;V r;r.reserve(n+1);
 for(int i=0;i<n;i++){int t=d[i]+d[n-1-i]+carry;r.push_back(t%10);carry=t/10;}
 if(carry)r.push_back(carry);
 assert(r.back()!=0);return r;
}
V halfpair(const V&d){
 int n=d.size();V p;p.reserve((n+1)/2);
 for(int i=0;i<(n+1)/2;i++)p.push_back(d[i]+d[n-1-i]);
 return p;
}
bool ispal(const V&d){return equal(d.begin(),d.begin()+d.size()/2,d.rbegin());}
uint64_t hash_digits(const V&d){
 uint64_t h=1469598103934665603ULL;
 for(int x:d){h^=x+1;h*=1099511628211ULL;}
 return h;
}
int main(int argc,char**argv){
 int q=argc>1?atoi(argv[1]):300,steps=argc>2?atoi(argv[2]):20000;
 assert(q>=1 && steps>=1);
 V a=realize(q,false),b=realize(q,true);
 assert(a!=b && !ispal(a) && !ispal(b));
 assert(step(a)==step(b));
 int one_positions=0;for(int x:W)if(x==1)one_positions++;
 assert(one_positions==2);
 // Independent 500-copy calibration of all 8 cap and bulk phase words.
 int control_q=max(q+200,500);V c=realize(control_q,false);
 array<V,8> cap,bulk;
 for(int t=0;t<8;t++){
  auto p=halfpair(c);assert(p.size()>=39+100);
  cap[t]=V(p.begin(),p.begin()+39);
  bulk[t]=V(p.begin()+39,p.begin()+59);
  c=step(c);
 }
 assert(cap[0]==B && bulk[0]==W);
 int minbands=1000000000,overflows=0;V penultimate;
 for(int t=0;t<=steps;t++){
  auto p=halfpair(a);
  if(ispal(a)){cerr<<"PALINDROME at "<<t<<"\n";return 2;}
  if(!equal(cap[t%8].begin(),cap[t%8].end(),p.begin())){
   cerr<<"CAP BAD at "<<t<<"\n";return 3;
  }
  int bands=0;
  while(39+(bands+1)*20<=(int)p.size()){
   if(!equal(bulk[t%8].begin(),bulk[t%8].end(),
             p.begin()+39+bands*20))break;
   bands++;
  }
  minbands=min(minbands,bands);
  if(bands<1){cerr<<"BULK BAD at "<<t<<"\n";return 4;}
  if(t==steps)break;
  if(t==steps-1)penultimate=a;
  int before=a.size();a=step(a);int delta=(int)a.size()-before;
  if(delta!=(t%2==0)){cerr<<"GAMMA BAD at "<<t<<"\n";return 5;}
  overflows+=delta;
 }
 if(argc>3){
  ofstream out(argv[3]);assert(out);
  for(auto it=a.rbegin();it!=a.rend();++it)out<<*it;
  out<<"\n";
  int n=penultimate.size();V fullp;fullp.reserve(n);
  for(int i=0;i<n;i++)fullp.push_back(penultimate[i]+penultimate[n-1-i]);
  out<<hash_digits(fullp)<<"\n"<<n<<"\n";
 }
 cout<<"W07_DECIMAL_"<<steps<<"_PASS q="<<q
  <<" initial_digits="<<realize(q,false).size()
  <<" final_digits="<<a.size()<<" gamma1="<<overflows
  <<" min_complete_20_bands="<<minbands
  <<" one_step_coalescing_seed_count_at_least=2^("<<one_positions*q<<")"
  <<" final_fnv64="<<hash_digits(a)<<"\n";
}
