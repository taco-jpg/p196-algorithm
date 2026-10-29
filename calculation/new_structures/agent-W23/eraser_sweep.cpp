// W23 p8/m48 (and m20 control): exact finite-window two-cell eraser census.
// g++ -O3 -std=c++17 eraser_sweep.cpp -o /tmp/w23_sweep && /tmp/w23_sweep
#include <vector>
#include <iostream>
#include <map>
using namespace std;
using V=vector<int>;
const V W20={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
const V W48={4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,13,9,7,3,13,10,4,13,5,1,9,4,11,6,16,3,7,7,12,4,2,13,2,15,10,10,9,3};
V step(const V&a,int g){int n=a.size(),lo=0,hi=0;V u(n),v(n),q(n);
 for(int i=0;i<n;i++){int s=a[i]+lo;u[i]=s%10;lo=s/10;}
 for(int i=n-1;i>=0;i--){int s=a[i]+hi;v[i]=s%10;hi=s/10;}
 for(int i=0;i<n;i++)q[i]=u[i]+v[i-g>=0?i-g:n-1];return q;}
int main(){
 for(const V&W:{W20,W48}){
  const int len=960,period=16;
  V initial(len);for(int i=0;i<len;i++)initial[i]=W[i%W.size()];
  vector<V> background(period+1);background[0]=initial;
  for(int t=0;t<period;t++)background[t+1]=step(background[t],1-t%2);
  int tested=0, nongauge=0;map<int,int> erased;
  for(int pos=410;pos<410+(int)W.size();pos++)
   for(int a=0;a<19;a++)for(int b=0;b<19;b++){
    if(a==initial[pos] && b==initial[pos+1])continue;
    tested++;bool gauge=(a-initial[pos])%9==0 && (b-initial[pos+1])%9==0;
    V x=initial;x[pos]=a;x[pos+1]=b;
    for(int t=1;t<=period;t++){
     x=step(x,1-(t-1)%2);
     if(x==background[t]){
      erased[t]++;if(!gauge){
       nongauge++;cout<<"ERASER m="<<W.size()<<" offset="<<pos%W.size()
        <<" "<<initial[pos]<<","<<initial[pos+1]<<" -> "<<a<<","<<b
        <<" at t="<<t<<"\n";
      }break;
     }
    }
   }
  cout<<"SUMMARY m="<<W.size()<<" tested="<<tested<<" nongauge="<<nongauge;
  for(auto e:erased)cout<<" erase_t"<<e.first<<"="<<e.second;cout<<"\n";
  if(W.size()==20 && !(tested==7200 && nongauge==0 && erased[1]==44))return 2;
  if(W.size()==48 && !(tested==17280 && nongauge==5 && erased[1]==101 && erased[3]==5))return 3;
 }
 return 0;
}