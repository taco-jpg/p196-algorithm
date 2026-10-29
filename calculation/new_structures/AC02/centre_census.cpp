// AC02: exact differential decimal reverse-and-add centre-window necessary-condition census.
// All state differences are propagated with decimal carries until rejoining the baseline carry.
// Non-rejoined exceptional paths are passed to the independent full-width engine, NEVER pruned.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
static bool AUDIT=false;static bool GATE=false;
using V=vector<uint8_t>;
const V B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
const V W={5,18,4,8,1,15,4,0,5};
const vector<V> us={{9,2,16},{2,16,9},{16,9,2}};
void append(V&v,const V&b,int reps=1){for(int r=0;r<reps;r++)v.insert(v.end(),b.begin(),b.end());}
V templ(const V&u,const V&c,int q=14,int k=100){V h=B;append(h,W,q);h.push_back(5);append(h,u,k);V p=h;append(p,c);p.insert(p.end(),h.rbegin(),h.rend());return p;}
struct Step {V digit,carry,next;int gamma;};
Step compute(const V&p){Step s;size_t n=p.size();s.digit.reserve(n+1);s.carry.reserve(n+1);s.carry.push_back(0);for(int i=0;i<(int)n;i++){int x=p[i]+s.carry.back();s.digit.push_back(x%10);s.carry.push_back(x/10);}s.gamma=s.carry.back();if(s.gamma)s.digit.push_back(s.gamma);int m=s.digit.size();s.next.resize(m);for(int i=0;i<m;i++)s.next[i]=s.digit[i]+s.digit[m-1-i];return s;}
V full(const V&u,const V&c,int *gamma=nullptr){V p=templ(u,c);int z=0;for(int t=0;t<120;t++){auto s=compute(p);z+=s.gamma;p.swap(s.next);}if(gamma)*gamma=z;return p;}
struct Base {vector<V> p,d,carry;vector<int> gamma;};
Base make_base(const V&u,int clen){Base b;b.p.push_back(templ(u,V(clen,0)));for(int t=0;t<120;t++){Step s=compute(b.p.back());b.d.push_back(move(s.digit));b.carry.push_back(move(s.carry));b.gamma.push_back(s.gamma);b.p.push_back(move(s.next));}return b;}
struct Search {Base base;V u;int clen;uint64_t cnt=0,gate_skipped=0,fail=0,exceptional=0,alive=0,max_width=0,full_verified=0;V witness;
 explicit Search(const V&u,int c):base(make_base(u,c)),u(u),clen(c){}
 // Physical exact full-decimal fallback for when a variable carry fails to rejoin.
 bool fallback(const V&c){exceptional++;int gs=0;V z=full(u,c,&gs);V target=templ(u,c,14,105);if(z.size()!=target.size()||gs!=30)return false;int mid=z.size()/2,span=122+clen+30;for(int i=max(0,mid-span);i<=min((int)z.size()-1,mid+span);i++)if(z[i]!=target[i])return false;return true;}
 bool test(const V&c){cnt++;auto& p0=base.p[0];int n=p0.size();int lo=n/2-clen/2,hi=lo+clen-1;uint8_t v0[4096],v1[4096],digits[4096];uint8_t *cur=v0,*nxt=v1;int width=clen;
 for(int i=0;i<clen;i++)cur[i]=c[i];
 V truth;if(AUDIT)truth=templ(u,c);
 for(int t=0;t<120;t++){
  const V&pb=base.p[t];const V&db=base.d[t];const V&cb=base.carry[t];const V&nb=base.p[t+1];
  int m=db.size(),carry=cb[lo],stop=-1;
  for(int i=lo;i<n;i++){
    int x=(i<=hi?cur[i-lo]:pb[i])+carry;int d=x%10;carry=x/10;
    digits[i-lo]=d;
    if(i>=hi&&carry==cb[i+1]){stop=i;break;}
  }
  if(stop<0){return fallback(c);}
  int lo2=min(lo,m-1-stop),hi2=m-1-lo2;
  max_width=max(max_width,(uint64_t)(hi2-lo2+1));
  for(int i=lo2;i<=hi2;i++){
   int a=(i>=lo&&i<=stop)?digits[i-lo]:db[i];
   int j=m-1-i;
   int b=(j>=lo&&j<=stop)?digits[j-lo]:db[j];
   nxt[i-lo2]=uint8_t(a+b);
  }
  lo=lo2;hi=hi2;swap(cur,nxt);width=hi-lo+1;n=nb.size();
  if(AUDIT){Step ss=compute(truth);truth.swap(ss.next);if(truth.size()!=nb.size())abort();for(int j=0;j<n;j++){int x=(j>=lo&&j<=hi)?cur[j-lo]:nb[j];if(x!=truth[j]){cerr<<"DIFFERENTIAL FAILURE t="<<t<<" j="<<j<<"\n";abort();}}}

 }
 int center=n/2,span=122+clen+30;
 const V& bb=base.p[120];V target=templ(u,c,14,105);
 if((int)target.size()!=n) return false;
 for(int i=max(0,center-span);i<=min(n-1,center+span);i++){
  int x=i>=lo&&i<=hi?cur[i-lo]:bb[i];
  if(x!=target[i])return false;
 }
 return true;
 }
 void enumerate(int level,int maxlevel,V&c,uint64_t cap){
   if(cap&&cnt>=cap)return;
   int h=clen/2;
   if(level==h){
     if(clen%2){for(int d=0;d<=18;d+=2){c[h]=d;
       if(GATE){int au=int(u[0])-int(u[1])+int(u[2]),ac=0;for(int j=0;j<clen;j++)ac+=(j%2?-1:1)*int(c[j]);if((au-ac)%11){gate_skipped++;continue;}}
       if(test(c)){alive++;witness=c;}}}
     else {if(test(c)){alive++;witness=c;}}
     return;
   }
   for(int d=0;d<=18;d++){
    c[level]=c[clen-1-level]=d;
    enumerate(level+1,maxlevel,c,cap);
    if(cap&&cnt>=cap)break;
   }
 }
 void run(uint64_t cap){V c(clen,0);enumerate(0,clen/2,c,cap);cout<<"U="<<int(u[0])<<","<<int(u[1])<<","<<int(u[2])<<" C="<<clen<<" checked="<<cnt<<" gate_excluded="<<gate_skipped<<" exceptional="<<exceptional<<" survivor="<<alive<<" max_diff_width="<<max_width; if(alive){cout<<" witness=";for(auto x:witness)cout<<int(x)<<",";}cout<<"\n"<<flush;}
};
int main(int argc,char**argv){int umin=argc>1?atoi(argv[1]):0,umax=argc>2?atoi(argv[2]):2,cmin=argc>3?atoi(argv[3]):7,cmax=argc>4?atoi(argv[4]):14;uint64_t cap=argc>5?strtoull(argv[5],nullptr,10):0;AUDIT=argc>6 && std::string(argv[6])=="audit";GATE=argc>6 && std::string(argv[6])=="oddallwidth";for(int ui=umin;ui<=umax;ui++)for(int c=cmin;c<=cmax;c++){Search x(us.at(ui),c);x.run(cap);}}