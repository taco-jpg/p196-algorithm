// Exhaustive rooted phase-zero p12/m9 J5 endpoint screen for U ranks 7 and 19.
// Exact pair-coefficient semantics; no J pruning or strict-W9 prefilter.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;
using V=vector<uint8_t>;
static const V B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static const V W={5,18,4,8,1,15,4,0,5};
static const V U7={6,9,12};
static const V U19={9,16,2};
static void append(V&a,const V&b){a.insert(a.end(),b.begin(),b.end());}
static void repeat(V&a,const V&b,int n){for(int i=0;i<n;i++)append(a,b);}
static V rev(V a){reverse(a.begin(),a.end());return a;}
static V templ(const V&J,const V&U,int q=14,int k=100){
 V h=B;repeat(h,W,q);append(h,J);repeat(h,U,k);V p=h;append(p,V{0,0,0});append(p,rev(h));return p;
}
static inline bool step(V&p){
 const size_t n=p.size();V d;d.resize(n+1);uint8_t c=0;
 for(size_t i=0;i<n;i++){unsigned z=p[i]+c;d[i]=z%10;c=z/10;}
 size_t dn=n;if(c)d[dn++]=c;
 V out;out.resize(dn);for(size_t i=0;i<dn;i++)out[i]=d[i]+d[dn-1-i];
 p.swap(out);return c!=0;
}
static inline bool is_prefix(const V&p,const V&t){return p.size()>=t.size()&&equal(t.begin(),t.end(),p.begin());}
static V decode(uint32_t x){V j(5);for(int i=0;i<5;i++){j[i]=x%19;x/=19;}return j;}
int main(int argc,char**argv){
 uint64_t start=argc>1?stoull(argv[1]):0,count=argc>2?stoull(argv[2]):2476099,end=min<uint64_t>(2476099,start+count);
 int rank=argc>3?stoi(argv[3]):7;if(rank!=7&&rank!=19){cerr<<"U rank must be 7 or 19\n";return 2;}
 const V&U=rank==7?U7:U19;V target=B;repeat(target,W,14);
 uint64_t checked=0,clockok=0,prefix=0,returns=0;map<int,uint64_t>hist;auto t0=chrono::steady_clock::now();
 for(uint64_t idx=start;idx<end;idx++){
  V J=decode(idx),p=templ(J,U);bool clock=true;
  for(int t=0;t<120;t++){bool g=step(p);if(g!=(t%4==0))clock=false;}
  checked++;clockok+=clock;size_t m=0;while(m<target.size()&&m<p.size()&&target[m]==p[m])m++;
  if(m==target.size())prefix++;hist[(int)m-(int)target.size()]++;
  if(is_prefix(p,target)){V h=B;repeat(h,W,14);append(h,J);repeat(h,U,105);V want=h;append(want,V{0,0,0});append(want,rev(h));if(p==want)returns++;}
  if((idx-start+1)%10000==0){double sec=chrono::duration<double>(chrono::steady_clock::now()-t0).count();cerr<<"PROGRESS U="<<rank<<" checked="<<(idx-start+1)<<" sec="<<sec<<" rate="<<((idx-start+1)/sec)<<" prefix="<<prefix<<"\n";}
 }
 double sec=chrono::duration<double>(chrono::steady_clock::now()-t0).count();
 cout<<"RESULT U="<<rank<<" range="<<start<<":"<<end<<" checked="<<checked<<" clock="<<clockok<<" prefix_restored="<<prefix<<" full_return="<<returns<<" seconds="<<sec<<" rate="<<(checked/sec)<<"\n";
 for(auto[k,v]:hist)cout<<"mismatch_offset="<<k<<" count="<<v<<"\n";
 return checked==end-start&&clockok==checked&&prefix==0&&returns==0?0:3;
}
