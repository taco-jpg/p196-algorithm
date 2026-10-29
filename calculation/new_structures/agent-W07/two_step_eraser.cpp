// W07 exact two-step decimal pairword eraser, full ordinary-digit 20k replay.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;using V=vector<int>;
const V B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
const V W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
V pair_seed(int q,int centre){
 V h=B;for(int i=0;i<q;i++)h.insert(h.end(),W.begin(),W.end());
 V p=h;p.insert(p.end(),h.rbegin(),h.rend());
 int L=h.size();assert(p[L-1]==13&&p[L]==13);
 if(centre!=13){p[L-1]=centre;p[L]=centre;}
 return p;
}
V realize(const V&p,bool toggle=false){
 int n=p.size();V d(n);
 for(int i=0;i<n/2;i++){
  int low=min(9,p[i]),high=p[i]-low;
  if(toggle && i>=39 && p[i]==1){low=0;high=1;}
  d[i]=low;d[n-1-i]=high;
 }
 assert(d.back()!=0);return d;
}
V step(const V&d){
 int n=d.size(),c=0;V next;next.reserve(n+1);
 for(int i=0;i<n;i++){int s=d[i]+d[n-1-i]+c;next.push_back(s%10);c=s/10;}
 if(c)next.push_back(c);
 assert(next.back()!=0);return next;
}
V coeffs(const V&d){int n=d.size();V p(n);for(int i=0;i<n;i++)p[i]=d[i]+d[n-1-i];return p;}
bool ispal(const V&d){return equal(d.begin(),d.begin()+d.size()/2,d.rbegin());}
uint64_t fnv(const V&d){uint64_t h=1469598103934665603ULL;for(int x:d){h^=x+1;h*=1099511628211ULL;}return h;}
int main(){
 for(int q=0;q<=100;q++){
  V p=pair_seed(q,13),r=pair_seed(q,4);
  assert(p!=r);V a=realize(p),b=realize(r);
  assert(!ispal(a)&&!ispal(b));
  a=step(a);b=step(b);
  assert(a!=b && coeffs(a)==coeffs(b));
  assert(!ispal(a)&&!ispal(b));
  assert(step(a)==step(b));
  assert(step(a)!=step(step(realize(pair_seed(q,5)))));
 }
 const int q=300;
 V p=pair_seed(q,13),r=pair_seed(q,4);
 V a=realize(p),a2=realize(p,true),b=realize(r),b2=realize(r,true);
 assert(a!=a2 && b!=b2 && p!=r);
 assert(step(a)==step(a2));assert(step(b)==step(b2));
 assert(step(a)!=step(b));
 assert(coeffs(step(a))==coeffs(step(b)));
 assert(step(step(a))==step(step(b)));
 V cal=realize(pair_seed(500,13));array<V,8> caps,bulks;
 for(int t=0;t<8;t++){
  auto word=coeffs(cal);
  caps[t]=V(word.begin(),word.begin()+39);
  bulks[t]=V(word.begin()+39,word.begin()+59);cal=step(cal);
 }
 int minbands=1000000,overflows=0;
 for(int t=0;t<=20000;t++){
  V word=coeffs(b);
  if(ispal(b)){cerr<<"PAL t="<<t<<"\n";return 3;}
  if(!equal(caps[t%8].begin(),caps[t%8].end(),word.begin())){
   cerr<<"CAP t="<<t<<"\n";return 4;
  }
  int count=0;
  while(39+(count+1)*20<=(int)word.size() &&
    equal(bulks[t%8].begin(),bulks[t%8].end(),word.begin()+39+20*count))count++;
  minbands=min(minbands,count);
  if(count<72){cerr<<"BAND t="<<t<<" count="<<count<<"\n";return 5;}
  if(t==20000)break;
  int n=b.size();b=step(b);
  if((int)b.size()-n!=(t%2==0)){cerr<<"GAMMA t="<<t<<"\n";return 6;}
  overflows+=(int)b.size()-n;
  if(t==0)assert(b!=step(a));
  if(t==1)assert(b==step(step(a)));
 }
 cout<<"W07_TWO_STEP_ERASER_20000_PASS q=300 seeds=2^(601) merged_t2 minbands="
  <<minbands<<" overflows="<<overflows<<" finaldigits="<<b.size()
  <<" fnv64="<<fnv(b)<<"\n";
 assert(fnv(b)==10989435956851471335ULL);
}
