// Independent all-time-domain check for base-10 g=(11000)^k.
// Does not use 5-step transfer tables; explores the original p=5k
// recurrence at EVERY time and all coefficient seeds at spatial columns 1-3.
// Count time-closed 3-column histories, and flag deviations from the claimed
// forced temporal coefficient paths. No SAT, state caps, or heuristics.
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <vector>
#include <array>
using namespace std;

using U = uint64_t;
struct Runner {
 int k,p; vector<int> g,rootx,rooth,x2,h2;
 U nroot=0,nsecond=0,nthird=0;
 Runner(int k_):k(k_),p(5*k_),g(p),rootx(p),rooth(p),x2(p),h2(p){
  for(int t=0;t<p;t++)g[t]=(t%5<2);
 }
 U third_count(const vector<int>& L, const vector<int>& H, const vector<int>& Y) {
  U valid=0,invalid=0;
  const int expect[5]={15,10,4,8,17};
  // DP over current coefficient and whether any intermediate coefficient
  // differed from the claimed five-time-step pattern. Count all carries.
  for(int z=0;z<=18;z++){
    array<array<U,2>,19> cur{},nxt{};
    cur[z][0]=1;
    for(int t=0;t<p;t++){
      nxt={};
      for(int x=0;x<=18;x++)for(int bad=0;bad<=1;bad++){
        U qty=cur[x][bad];if(!qty)continue;
        for(int c=0;c<=1;c++){
          if((x+c)/10!=H[t])continue;
          int y=(x+L[t])%10 + (g[t] ? Y[t] : (x+c)%10);
          assert(y>=0&&y<=18);
          nxt[y][bad || x!=expect[t%5]] += qty;
        }
      }
      cur=nxt;
    }
    valid+=cur[z][0];invalid+=cur[z][1];
  }
  if(invalid){cerr<<"unexpected third coefficient path "<<invalid<<"\n";abort();}
  return valid;
 }
 void closed_second() {
  nsecond++;
  static const int expect[5]={13,3,4,8,16};
  for(int t=0;t<p;t++)if(x2[t]!=expect[t%5]){
    cerr<<"unexpected second coefficient at t="<<t<<"\n";abort();
  }
  vector<int> L(p),H(p),Y(p);
  for(int t=0;t<p;t++){
    L[t]=(x2[t]+rootx[t]/10)/10;
    H[t]=h2[t];
    if(g[t]) Y[t]=(x2[t]+h2[t])%10;
  }
  nthird+=third_count(L,H,Y);
 }
 void second_dfs(int t,int x,int z,const vector<int>& L,const vector<int>& H,const vector<int>& Y){
  if(t==p){if(x==z)closed_second();return;}
  for(int c=0;c<=1;c++){
    if((x+c)/10!=H[t])continue;
    x2[t]=x;h2[t]=c;
    int y=(x+L[t])%10+(g[t]?Y[t]:(x+c)%10);
    assert(y>=0&&y<=18);
    second_dfs(t+1,y,z,L,H,Y);
  }
 }
 void closed_root(){
  nroot++;
  static const int expect[5]={9,10,1,2,4};
  for(int t=0;t<p;t++)if(rootx[t]!=expect[t%5]){
    cerr<<"unexpected root coefficient at t="<<t<<"\n";abort();
  }
  vector<int> L(p),H(p),Y(p);
  for(int t=0;t<p;t++){
    L[t]=rootx[t]/10;
    H[t]=rooth[t];
    if(g[t]) Y[t]=(rootx[t]+rooth[t])%10;
  }
  for(int x0=0;x0<=18;x0++)second_dfs(0,x0,x0,L,H,Y);
 }
 void root_dfs(int t,int x,int z){
  if(t==p){if(x==z)closed_root();return;}
  for(int c=0;c<=1;c++){
    if((x+c)/10!=g[t])continue;
    rootx[t]=x;rooth[t]=c;
    // initial L=0, overflow Y=1; canonical x0 >=1
    int y=x%10+(g[t]?1:(x+c)%10);
    assert(y>=0&&y<=18);
    root_dfs(t+1,y,z);
  }
 }
 void run(){
  for(int x0=1;x0<=18;x0++)root_dfs(0,x0,x0);
  U want=1;for(int j=0;j<k;j++)want*=4;
  if(nroot!=(U(1)<<k)||nsecond!=want||nthird!=want){
    cerr<<"count mismatch k="<<k<<" root="<<nroot<<" second="<<nsecond
        <<" third="<<nthird<<" expected="<<want<<"\n";abort();
  }
  cout<<"k="<<k<<" p="<<p<<" root="<<nroot<<" second="<<nsecond
      <<" closed_three_column="<<nthird<<" PASS\n";
 }
};
int main(int argc,char**argv){
 int kmax=argc>1?atoi(argv[1]):8;
 if(kmax<1||kmax>10){cerr<<"kmax must be in [1,10]\n";return 2;}
 for(int k=1;k<=kmax;k++)Runner(k).run();
}
