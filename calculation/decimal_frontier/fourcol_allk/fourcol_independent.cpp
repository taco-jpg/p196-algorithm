// Whole-time independent four-column counting in the canonical bauto3 model.
// Unlike fourcol_block_graph.py this does NOT use five-step block matrices.
// Search root, second, and third spatial columns via direct full-time DFS,
// then count all closed fourth-column histories with per-time integer DP.
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <vector>
using namespace std;
using U=uint64_t;
struct Run{
 int k,p;vector<int> g,x0,h0,x1,h1,x2,h2;
 U n0=0,n1=0,n2=0,n3=0;
 Run(int k_):k(k_),p(5*k),g(p),x0(p),h0(p),x1(p),h1(p),x2(p),h2(p){for(int t=0;t<p;t++)g[t]=(t%5<2);}
 U fourth_count(const vector<int>&L,const vector<int>&H,const vector<int>&Y){
  U total=0;
  // Direct step-by-step time closure with arbitrary fourth coefficients 0..18.
  for(int initial=0;initial<=18;initial++){
   array<U,19>dp{},nx{};dp[initial]=1;
   for(int t=0;t<p;t++){
    nx={};
    for(int x=0;x<=18;x++)if(dp[x])for(int c=0;c<=1;c++){
      if((x+c)/10!=H[t])continue;
      int y=(x+L[t])%10+(g[t]?Y[t]:(x+c)%10);
      assert(0<=y&&y<=18);nx[y]+=dp[x];
    }
    dp=nx;
   }
   total+=dp[initial];
  }
  return total;
 }
 void finish_third(const vector<int>& L2){
  n2++;
  int expected[5]={15,10,4,8,17};
  for(int t=0;t<p;t++)if(x2[t]!=expected[t%5])abort();
  vector<int>L(p),H(p),Y(p);
  for(int t=0;t<p;t++){
   L[t]=(x2[t]+L2[t])/10;H[t]=h2[t];
   if(g[t])Y[t]=(x2[t]+h2[t])%10;
  }
  n3+=fourth_count(L,H,Y);
 }
 void third_dfs(int t,int x,int initial,const vector<int>&L,
                const vector<int>&H,const vector<int>&Y){
  if(t==p){if(x==initial)finish_third(L);return;}
  for(int c=0;c<=1;c++){
   if((x+c)/10!=H[t])continue;
   x2[t]=x;h2[t]=c;
   int next=(x+L[t])%10+(g[t]?Y[t]:(x+c)%10);
   assert(0<=next&&next<=18);
   third_dfs(t+1,next,initial,L,H,Y);
  }
 }
 void finish_second(const vector<int>& L1){
  n1++;
  int expected[5]={13,3,4,8,16};
  for(int t=0;t<p;t++)if(x1[t]!=expected[t%5])abort();
  vector<int>L(p),H(p),Y(p);
  for(int t=0;t<p;t++){
   L[t]=(x1[t]+L1[t])/10;H[t]=h1[t];
   if(g[t])Y[t]=(x1[t]+h1[t])%10;
  }
  for(int initial=0;initial<=18;initial++)third_dfs(0,initial,initial,L,H,Y);
 }
 void second_dfs(int t,int x,int initial,const vector<int>&L,
                  const vector<int>&H,const vector<int>&Y){
  if(t==p){if(x==initial)finish_second(L);return;}
  for(int c=0;c<=1;c++){
   if((x+c)/10!=H[t])continue;
   x1[t]=x;h1[t]=c;
   int next=(x+L[t])%10+(g[t]?Y[t]:(x+c)%10);
   assert(0<=next&&next<=18);
   second_dfs(t+1,next,initial,L,H,Y);
  }
 }
 void finish_root(){
  n0++;
  int expected[5]={9,10,1,2,4};
  for(int t=0;t<p;t++)if(x0[t]!=expected[t%5])abort();
  vector<int>L(p),H(p),Y(p);
  for(int t=0;t<p;t++){
   L[t]=x0[t]/10;H[t]=h0[t];
   if(g[t])Y[t]=(x0[t]+h0[t])%10;
  }
  for(int initial=0;initial<=18;initial++)second_dfs(0,initial,initial,L,H,Y);
 }
 void root_dfs(int t,int x,int initial){
  if(t==p){if(x==initial)finish_root();return;}
  for(int c=0;c<=1;c++){
   if((x+c)/10!=g[t])continue;
   x0[t]=x;h0[t]=c;
   int next=x%10+(g[t]?1:(x+c)%10);
   assert(0<=next&&next<=18);
   root_dfs(t+1,next,initial);
  }
 }
 void execute(){
  for(int initial=1;initial<=18;initial++)root_dfs(0,initial,initial);
  U expect0=U(1)<<k, expect1=U(1)<<(2*k);
  // F_k = 4^k + (4+2sqrt(10))^k + (4-2sqrt(10))^k,
  // where the algebraic sum satisfies Q_k=8*Q_(k-1)+24*Q_(k-2).
  U qa=2,qb=8;
  for(int i=2;i<=k;i++){U q=8*qb+24*qa;qa=qb;qb=q;}
  U expect3=expect1+(k==1?8:qb);
  if(n0!=expect0||n1!=expect1||n2!=expect1||n3!=expect3){
    cerr<<"FAIL k="<<k<<" got="<<n0<<","<<n1<<","<<n2<<","<<n3
        <<" expected="<<expect0<<","<<expect1<<","<<expect1<<","<<expect3<<"\n";abort();
  }
  cout<<"k="<<k<<" root="<<n0<<" second="<<n1<<" third="<<n2
      <<" fourth="<<n3<<" PASS\n";
 }
};
int main(int argc,char**argv){int top=argc>1?atoi(argv[1]):6;
 if(top<1||top>8){cerr<<"k must be <=8 for whole-trajectory enumeration\n";return 2;}
 for(int k=1;k<=top;k++)Run(k).execute();
}
