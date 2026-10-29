// W07: full pairword insertion identity for 20,000 ordinary decimal steps.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;using V=vector<int>;
static const V B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const V W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
V seed(int q){
 V h=B;for(int i=0;i<q;i++)h.insert(h.end(),W.begin(),W.end());
 V p=h;p.insert(p.end(),h.rbegin(),h.rend());
 V d(p.size());
 for(int i=0;i<(int)p.size()/2;i++){
  d[i]=min(p[i],9);d[(int)p.size()-1-i]=p[i]-d[i];
 }
 assert(d.back()>0);return d;
}
V step(const V&a){
 V out;out.reserve(a.size()+1);int c=0,n=a.size();
 for(int i=0;i<n;i++){int x=a[i]+a[n-1-i]+c;out.push_back(x%10);c=x/10;}
 if(c)out.push_back(c);return out;
}
V pairword(const V&d){
 int n=d.size();V p(n);
 for(int i=0;i<n;i++)p[i]=d[i]+d[n-1-i];
 return p;
}
V insert(const V&p,const V&w){
 assert(p.size()>=78);
 V z;z.reserve(p.size()+2*w.size());
 z.insert(z.end(),p.begin(),p.begin()+39);
 z.insert(z.end(),w.begin(),w.end());
 z.insert(z.end(),p.begin()+39,p.end()-39);
 z.insert(z.end(),w.rbegin(),w.rend());
 z.insert(z.end(),p.end()-39,p.end());
 return z;
}
int main(int argc,char**){
 V a=seed(300),b=seed(301),cal=seed(500);
 array<V,8> phases;
 for(int i=0;i<8;i++){
  auto p=pairword(cal);
  phases[i]=V(p.begin()+39,p.begin()+59);
  cal=step(cal);
 }
 assert(phases[0]==W);
 if(argc>1)phases[0][0]=(phases[0][0]+1)%19;
 for(int t=0;t<=20000;t++){
  auto p=pairword(a),r=pairword(b);
  auto expected=insert(p,phases[t%8]);
  if(r!=expected){cerr<<"INSERT FAIL t="<<t<<"\n";return 2;}
  if(a==V(a.rbegin(),a.rend()) || b==V(b.rbegin(),b.rend()))return 3;
  if(t<20000){a=step(a);b=step(b);}
 }
 cout<<"W07_UNIFORM_INSERTION_20000_PASS exact full pairword q300 vs q301 all 20001 slices; 20,000 literal digit steps per seed\n";
}
