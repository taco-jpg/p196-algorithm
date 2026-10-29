// Deterministic xorshift32 source; 128 arbitrary 40-cell packet pairs, 600 steps.
// Each seed is formed afresh, with centre packet translated by 20 in its pumped mate.
#include <bits/stdc++.h>
using namespace std;using W=vector<uint8_t>;
int pre[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
int cyc[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
W seed(int h,vector<int> const&last){W z(2*h);for(int i=0;i<h;i++){int p=i<39?pre[i]:cyc[(i-39)%20];if(i>=h-int(last.size()))p=last[i-(h-last.size())];z[i]=max(0,p-9);z[2*h-1-i]=p-z[i];}return z;}
void step(W&z){W y(z.size()+1);int n=z.size(),c=0;for(int i=0;i<n;i++){int s=z[i]+z[n-1-i]+c;y[i]=s%10;c=s/10;}if(c)y[n]=c;else y.resize(n);z.swap(y);}
int main(){
 uint32_t rng=0x817aff23;auto next=[&](){rng^=rng<<13;rng^=rng>>17;rng^=rng<<5;return rng;};long long cells=0;
 for(int test=0;test<128;test++){
  vector<int>packet(40);for(int& p:packet)p=next()%19;
  W x=seed(500,packet),y=seed(520,packet);
  for(int t=0;t<=600;t++){
   int n=x.size();if(y.size()!=n+40)return 1;
   for(int i=0;i<n/2;i++){
    int a=x[i]+x[n-1-i],j=i<39?i:i+20,b=y[j]+y[y.size()-1-j];cells++;
    if(a!=b){cerr<<"discrepancy test="<<test<<" t="<<t<<" i="<<i<<"\n";return 1;}
   }
   if(t<600){step(x);step(y);}
  }
 }
 cout<<"PASS: 128 xorshift32 40-cell packets, 600 steps, checked_cells="<<cells<<" rng_end="<<rng<<"\n";
 return cells==44224000&&rng==2616790242?0:1;
}
