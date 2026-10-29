// AC10: exact sparse-difference simulation for the 120-step center-sector endpoint.
// Pair coefficients LSD first; no strict-phase W9 filtering.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
#include <array>
#include <string>
#include <chrono>
using V=std::vector<int>;
static const V B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static const V W={5,18,4,8,1,15,4,0,5};
static const std::array<std::array<int,3>,3> US={{{9,18,0},{18,0,9},{0,9,18}}};
static V tpl(int u,const V&C,int q=14,int k=100){
 V h=B;for(int i=0;i<q;i++)h.insert(h.end(),W.begin(),W.end());
 h.push_back(5);for(int i=0;i<k;i++)for(int v:US[u])h.push_back(v);
 V p=h;p.insert(p.end(),C.begin(),C.end());p.insert(p.end(),h.rbegin(),h.rend());return p;
}
struct Layer{V p,carry,digit;int gamma;};
static Layer transition(const V&p){
 int n=p.size(),c=0;V a(n),carry(n+1),next(n);carry[0]=0;
 for(int i=0;i<n;i++){int s=p[i]+c;a[i]=s%10;c=s/10;carry[i+1]=c;}
 int gamma=c!=0;if(gamma)a.push_back(c);
 int nn=a.size();next.resize(nn);
 for(int i=0;i<nn;i++)next[i]=a[i]+a[nn-1-i];
 return {std::move(next),std::move(carry),std::move(a),gamma};
}
static std::vector<Layer> refs(int u,int size){
 V zero(size);auto p=tpl(u,zero);std::vector<Layer> base;base.reserve(121);
 for(int t=0;t<120;t++){
  auto x=transition(p);Layer r;r.p=std::move(p);
  r.carry=std::move(x.carry);r.digit=std::move(x.digit);r.gamma=x.gamma;
  p=std::move(x.p);base.push_back(std::move(r));
 }
 Layer finish;finish.p=std::move(p);base.push_back(std::move(finish));return base;
}
struct Tester{
 int u,size,n0,centre0;std::vector<Layer> base;V da,db;
 uint64_t tested=0,pass=0,overflowChanges=0,scalar_ops=0;
 explicit Tester(int ui,int sz):u(ui),size(sz),base(refs(ui,sz)){
  n0=tpl(ui,V(sz)).size();centre0=n0/2;
  da.resize(n0+40);db.resize(n0+40);
 }
 bool test(const V&C,bool audit=false){
  std::fill(da.begin()+centre0-size/2,da.begin()+centre0-size/2+size,0);
  int lo=centre0-size/2,hi=lo-1;
  for(int j=0;j<size;j++)if(C[j]!=0){da[lo+j]=C[j];hi=lo+j;}
  int lastHi=hi;if(hi<lo)lo=n0;
  V denseAudit;if(audit)denseAudit=tpl(u,C);
  for(int t=0;t<120;t++){
   const auto &r=base[t],&rnext=base[t+1];int n=r.carry.size()-1;
   if(lo>=n)break;
   int c=r.carry[lo],nl=(int)db.size(),nh=-1;bool reset=false;
   for(int i=lo;i<n;i++){
    int pi=(i<=lastHi?da[i]:0);
    int original=r.digit[i]+10*r.carry[i+1]-r.carry[i];
    int s=original+pi+c,d=s%10,co=s/10;
    int diff=d-r.digit[i];
    if(diff){
     db[i]+=diff;int mir=(int)rnext.p.size()-1-i;
     db[mir]+=diff;nl=std::min(nl,std::min(i,mir));nh=std::max(nh,std::max(i,mir));
    }
    scalar_ops++;c=co;
    if(i>=lastHi&&c==r.carry[i+1]){reset=true;break;}
   }
   if(!reset&&c!=r.carry[n]){overflowChanges++;return false;}
   if(lastHi>=lo)std::fill(da.begin()+lo,da.begin()+lastHi+1,0);
   da.swap(db);lo=nl;lastHi=nh;
   if(audit){
    denseAudit=transition(denseAudit).p;
    if(denseAudit.size()!=rnext.p.size())std::abort();
    for(int j=0;j<(int)rnext.p.size();j++){
     int got=rnext.p[j]+(j>=lo&&j<=lastHi?da[j]:0);
     if(denseAudit[j]!=got){std::cerr<<"SPARSE/DENSE mismatch phase="<<t+1<<" index="<<j<<"\n";std::abort();}
    }
   }
  }
  int n=base[120].p.size();if(lo>n)lo=n;
  const V &baseFinal=base[120].p;
  V wanted=tpl(u,C,14,105);
  if(wanted.size()!=baseFinal.size())return false;
  int radius=122+size+30,mid=(int)wanted.size()/2;
  bool success=true;
  for(int i=mid-radius;i<=mid+radius;i++){
   if(i<0||i>=n)continue;
   int actual=baseFinal[i]+(i>=lo&&i<=lastHi?da[i]:0);
   if(actual!=wanted[i]){success=false;break;}
  }
  if(audit){
   V p=tpl(u,C);for(int j=0;j<120;j++)p=transition(p).p;
   if(p.size()!=baseFinal.size())std::abort();
   for(int j=0;j<n;j++)
    if(p[j]!=baseFinal[j]+(j>=lo&&j<=lastHi?da[j]:0))std::abort();
  }
  if(lastHi>=lo)std::fill(da.begin()+lo,da.begin()+lastHi+1,0);
  tested++;pass+=success;return success;
 }
};
static V centre_from_index(int sz,uint64_t index){
 int h=sz/2;V C(sz);for(int i=0;i<h;i++){
  int v=index%19;index/=19;C[i]=C[sz-1-i]=v;
 }
 if(sz%2)C[h]=2*(index%10);return C;
}
static uint64_t pow19(int x){uint64_t p=1;for(int i=0;i<x;i++)p*=19;return p;}
int main(int argc,char **argv){
 if(argc<5){std::cerr<<"usage: centre_sparse U(0-2) C_length count offset [print_matches] [audit]\n";return 2;}
 int u=std::stoi(argv[1]),sz=std::stoi(argv[2]);
 uint64_t count=std::stoull(argv[3]),offset=std::stoull(argv[4]);
 if(u<0||u>2||sz<1||sz>24)return 2;
 Tester test(u,sz);uint64_t total=pow19(sz/2)*(sz%2?10:1);
 if(offset>total)return 2;if(count==0||count>total-offset)count=total-offset;
 auto t0=std::chrono::steady_clock::now();
 for(uint64_t i=offset;i<offset+count;i++){
  auto C=centre_from_index(sz,i);
  if(test.test(C,argc>6)&&argc>5){
   std::cout<<"FOUND u="<<u<<" size="<<sz<<" index="<<i<<" C=";
   for(int v:C)std::cout<<v<<",";std::cout<<"\n";
  }
 }
 double secs=std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count();
 std::cout<<"CELL u="<<u<<" length="<<sz<<" offset="<<offset
          <<" processed="<<count<<" total="<<total<<" center_pass="<<test.pass
          <<" gamma_diff="<<test.overflowChanges<<" scalar_ops="<<test.scalar_ops
          <<" seconds="<<secs<<"\n";
}