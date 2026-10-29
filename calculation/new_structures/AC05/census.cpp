#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <map>
#include <stdexcept>
#include <vector>
using namespace std;
using V=vector<uint8_t>;
static const V B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static const V W={5,18,4,8,1,15,4,0,5};
static const int UR[3][3]={{9,8,10},{8,10,9},{10,9,8}};
void app(V &v,const V &w){v.insert(v.end(),w.begin(),w.end());}
V templ(int u, const V &c,int q,int k){ V h=B;for(int i=0;i<q;i++)app(h,W);h.push_back(5);for(int i=0;i<k;i++)for(int j=0;j<3;j++)h.push_back(UR[u][j]);V p=h;app(p,c);reverse(h.begin(),h.end());app(p,h);return p;}
V realize(const V &p){int n=p.size();V d(n);for(int i=0;i<n/2;i++){int hi=min(9,int(p[i])),lo=int(p[i])-hi;assert(lo>=0&&lo<=9);d[i]=lo;d[n-i-1]=hi;}if(n&1){assert((p[n/2]&1)==0);d[n/2]=p[n/2]/2;}assert(d.back()!=0);return d;}
int run(int u,const V&c,int q,int k, int window, int *off=nullptr, int *clockok=nullptr){
 V p=templ(u,c,q,k),d=realize(p),nxt;int n=d.size(),total=0;bool clk=true;
 const int gam[12]={1,0,0,0,1,0,0,0,1,0,0,0};
 for(int t=0;t<120;t++){
  nxt.resize(n+1);int carry=0;
  for(int i=0;i<n;i++){int sum=int(d[i])+int(d[n-1-i])+carry; nxt[i]=sum%10;carry=sum/10;}
  nxt[n]=carry;int delta=(carry>0);total+=delta;
  if(delta!=gam[t%12])clk=false;
  nxt.resize(n+delta);d.swap(nxt);n+=delta;
 }
 if(clockok)*clockok=clk;
 V expected=templ(u,c,q,k+5);
 if(expected.size()!=d.size()){if(off)*off=-9999;return 0;}
 int N=d.size(),cen=N/2, first=0x7fffffff;
 for(int i=max(0,cen-window);i<min(N,cen+window);i++){
  uint8_t pair=d[i]+d[N-i-1];
  if(pair!=expected[i]){first=i-cen;break;}
 }
 if(off)*off=first;
 return first==0x7fffffff && clk;
}
struct PortModel {
 int u,L,q,k,R=64,window;V c0; bool clock_ok=true;
 vector<V> baseline; vector<int> il,ir,carry_in,carry_out;
 PortModel(int uu,int LL,int qq,int kk,int ww,int rr=64):u(uu),L(LL),q(qq),k(kk),R(rr),window(ww),c0(L,0){
  baseline.reserve(121);baseline.push_back(realize(templ(u,c0,q,k)));
  for(int t=0;t<120;t++){
   const V &d=baseline.back();int n=d.size();int l=(n-1)/2-R,r=n-1-l;
   il.push_back(l);ir.push_back(r);
   V nxt(n+1);int carry=0,cin=-1,cout=-1;
   for(int i=0;i<n;i++){
    if(i==l)cin=carry;
    int sum=int(d[i])+int(d[n-1-i])+carry;
    nxt[i]=sum%10;carry=sum/10;
    if(i==r)cout=carry;
   }
   carry_in.push_back(cin);carry_out.push_back(cout);
   if((carry>0)!=((t%4)==0))clock_ok=false;
   nxt[n]=carry;nxt.resize(n+(carry>0));baseline.push_back(move(nxt));
  }
  int n=baseline.back().size();il.push_back((n-1)/2-R);ir.push_back(n-1-il.back());
 }
 bool fast(int u,const V&c,int *ports_fail=nullptr){
  V p=templ(u,c,q,k),d=realize(p);
  int l=il[0],r=ir[0];V seg(d.begin()+l,d.begin()+r+1),nextseg,tmp;
  for(int t=0;t<120;t++){
   int n=baseline[t].size();int cl=il[t],cr=ir[t];
   int nl=il[t+1],nr=ir[t+1];int carry=carry_in[t];
   tmp.resize(seg.size());
   for(int j=0;j<int(seg.size());j++){
    int sum=int(seg[j])+int(seg[seg.size()-1-j])+carry;
    tmp[j]=sum%10;carry=sum/10;
   }
   if(carry!=carry_out[t]){if(ports_fail)(*ports_fail)++;return run(u,c,q,k,window);}
   const V &ref=baseline[t+1];nextseg.assign(ref.begin()+nl,ref.begin()+nr+1);
   for(int i=cl;i<=cr;i++){
    if(i<nl||i>nr){if(tmp[i-cl]!=ref[i]){if(ports_fail)(*ports_fail)++;return run(u,c,q,k,window);}}
    else nextseg[i-nl]=tmp[i-cl];
   }
   seg.swap(nextseg);
  }
  V expected=templ(u,c,q,k+5);int n=baseline.back().size();
  if(expected.size()!=n||!clock_ok)return false;
  int cen=n/2;
  for(int i=max(0,cen-window);i<min(n,cen+window);i++){
   int d1=(i>=il[120]&&i<=ir[120])?seg[i-il[120]]:baseline[120][i];
   int mi=n-1-i;
   int d2=(mi>=il[120]&&mi<=ir[120])?seg[mi-il[120]]:baseline[120][mi];
   if(d1+d2!=expected[i])return false;
  }
  return true;
 }
};
int main(int argc,char**argv){
 int u=argc>1?atoi(argv[1]):0,L=argc>2?atoi(argv[2]):7;
 uint64_t max=argc>3?strtoull(argv[3],0,10):0, start=argc>4?strtoull(argv[4],0,10):0;
 int q=argc>5?atoi(argv[5]):14,k=argc>6?atoi(argv[6]):100,window=argc>7?atoi(argv[7]):160;
 bool use_fast=argc>8?atoi(argv[8]):0; PortModel *port=use_fast?new PortModel(u,L,q,k,window):nullptr;int portbad=0;
 bool mod11_prune=argc>9?atoi(argv[9]):0;uint64_t eliminated=0;
 if(mod11_prune && window<152+L)throw runtime_error("mod-11 centre-window pruning requires window>=152+L under T12");
 int half=L/2;uint64_t count=1;for(int j=0;j<half;j++)count*=19; if(L&1)count*=10;
 if(!max||max>count-start)max=count-start;
 uint64_t found=0,clockbad=0;map<int,uint64_t> hist;auto then=chrono::steady_clock::now();
 for(uint64_t ii=start;ii<start+max;ii++){
  uint64_t x=ii;V c(L);
  if(L&1){c[half]=2*(x%10);x/=10;}
  for(int j=0;j<half;j++){c[j]=c[L-j-1]=x%19;x/=19;}
  if(mod11_prune && (L&1)){
   int alt=0;for(int j=0;j<L;j++)alt+=(j%2?-int(c[j]):int(c[j]));
   const int residues[3]={0,7,9};
   if((alt%11+11)%11!=residues[u]){eliminated++;continue;}
  }
  int off=0,clk=0;int ok=use_fast?port->fast(u,c,&portbad):run(u,c,q,k,window,&off,&clk);
  if(!use_fast&&!clk)clockbad++;
  if(ok){found++;if(found<=3){cout<<"FOUND u="<<u<<" L="<<L<<" id="<<ii<<" C=";for(auto c0:c)cout<<int(c0)<<",";cout<<"\n";}}
  if(!use_fast)hist[off]++;
 }
 double dt=chrono::duration<double>(chrono::steady_clock::now()-then).count();
 cout<<"RESULT u="<<u<<" L="<<L<<" start="<<start<<" tested="<<max<<" space="<<count<<" hits="<<found<<" clockbad="<<clockbad<<" seconds="<<dt<<" eliminated_by_mod11="<<eliminated<<" port_fallback="<<portbad<<" first_offset_hist=";if(use_fast)cout<<"UNREPORTED_FAST";else for(const auto&[pos,num]:hist)cout<<pos<<":"<<num<<",";cout<<"\n";
 return 0;
}
