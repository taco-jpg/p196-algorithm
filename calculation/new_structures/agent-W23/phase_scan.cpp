// W23 phase-resolved two-cell erasers on the decimal p8/m48 bulk.
// g++ -O3 -std=c++17 phase_scan.cpp -o /tmp/w23_phase && /tmp/w23_phase
#include <vector>
#include <iostream>
#include <map>
#include <tuple>
#include <algorithm>
using namespace std;using V=vector<int>;
const V W={4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,13,9,7,3,13,10,4,13,5,1,9,4,11,6,16,3,7,7,12,4,2,13,2,15,10,10,9,3};
V step(const V&a,int g){int n=a.size(),lo=0,hi=0;V u(n),v(n),q(n);
 for(int i=0;i<n;i++){int s=a[i]+lo;u[i]=s%10;lo=s/10;}
 for(int i=n-1;i>=0;i--){int s=a[i]+hi;v[i]=s%10;hi=s/10;}
 for(int i=0;i<n;i++)q[i]=u[i]+v[i-g>=0?i-g:n-1];return q;}
int main(){
 const int n=960;V background(n);for(int i=0;i<n;i++)background[i]=W[i%48];
 const int expected[8][2]={{3,5},{0,0},{0,0},{4,2},{3,5},{0,0},{0,0},{4,2}};
 for(int phase=0;phase<8;phase++){
  const int horizon=10;vector<V> pure(horizon+1);pure[0]=background;
  for(int t=0;t<horizon;t++)pure[t+1]=step(pure[t],1-(phase+t)%2);
  map<int,int> erasures;vector<tuple<int,int,int,int,int,int>> samples;
  for(int pos=410;pos<458;pos++)for(int x=0;x<19;x++)for(int y=0;y<19;y++){
   if(x==background[pos]&&y==background[pos+1])continue;
   if((x-background[pos])%9==0&&(y-background[pos+1])%9==0)continue;
   V changed=background;changed[pos]=x;changed[pos+1]=y;
   for(int t=1;t<=horizon;t++){
    changed=step(changed,1-(phase+t-1)%2);
    if(changed==pure[t]){
     erasures[t]++;
     samples.push_back({t,pos%48,background[pos],background[pos+1],x,y});break;
    }
   }
  }
  int total=0;for(auto e:erasures)total+=e.second;
  cout<<"PHASE "<<phase<<" total="<<total;
  for(auto [t,num]:erasures)cout<<" t"<<t<<"="<<num;
  cout<<"\n";sort(samples.begin(),samples.end());
  for(auto [t,pos,a,b,x,y]:samples)
   cout<<"PATCH "<<phase<<" "<<t<<" "<<pos<<" "<<a<<","<<b<<" -> "<<x<<","<<y<<"\n";
  if(expected[phase][0]==0){if(total!=0)return 7;}
  else if(erasures[expected[phase][0]]!=expected[phase][1] ||total!=expected[phase][1])return 8;
  background=step(background,1-phase%2);
 }
 cout<<"PASS phase-labelled p8/m48 eraser alphabet of 14 non-gauge patches\n";
 return 0;
}