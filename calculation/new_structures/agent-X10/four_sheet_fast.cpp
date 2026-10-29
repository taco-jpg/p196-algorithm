// Four-sheet two-parameter decimal carry engine. Independent implementation from four_sheet.py.
// g++ -std=c++17 -O3 four_sheet_fast.cpp -o four_sheet_fast
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
#include <string>
using namespace std;
struct Packet {int start=0;vector<unsigned char> d; bool empty() const{return d.empty();} int end() const{return start+(int)d.size()-1;} int length() const{return (int)d.size();} };
using S=array<Packet,4>;
Packet newpacket(const Packet&a,const Packet&b,int top) {
  if(a.empty()&&b.empty())return {};
  int l=INT32_MAX, h=INT32_MIN;
  if(!a.empty()){l=min(l,a.start);h=max(h,a.end());}
  if(!b.empty()){l=min(l,top-b.end());h=max(h,top-b.start);}
  vector<int> raw(h-l+2,0);
  if(!a.empty())for(int i=0;i<a.length();++i)raw[a.start+i-l]+=a.d[i];
  if(!b.empty())for(int i=0;i<b.length();++i)raw[top-(b.start+i)-l]+=b.d[i];
  int cy=0;vector<unsigned char> d(raw.size());
  for(size_t i=0;i<raw.size();++i){int w=raw[i]+cy;d[i]=w%10;cy=w/10;}
  if(cy){d.push_back(cy);}
  while(!d.empty()&&!d.back())d.pop_back();
  int z=0;while(z<(int)d.size()&&!d[z])++z;
  if(z==(int)d.size())return {};
  if(z) {d.erase(d.begin(),d.begin()+z);l+=z;}
  return Packet{l,move(d)};
}
S evolve(const S&x){
  if(x[3].empty())abort();
  int top=x[3].end();S y;
  for(int i=0;i<4;++i)y[i]=newpacket(x[i],x[3-i],top);
  return y;
}
int ceil_div(int a,int b){if(a<=0)return 0;return(a+b-1)/b;}
int needed_G(const S&x){
  int G=1;
  for(int i=0;i<4;i++)if(!x[i].empty()){
    if(i==0){if(x[i].start<0)abort();}
    else {int coef=(i==1)?1:(i==2)?3:4;G=max(G,ceil_div(-x[i].start,coef));}
  }
  for(int i=0;i<3;i++)if(!x[i].empty()&&!x[i+1].empty()){
    int den=(i==1)?2:1;
    G=max(G,ceil_div(x[i].end()-x[i+1].start+1,den));
  }
  return G;
}
bool palindrome(const S&x){
  if(x[3].empty())abort();
  int top=x[3].end();
  for(int i=0;i<4;i++){
    const auto&a=x[i];const auto&b=x[3-i];
    for(int j=0;j<a.length();++j){int pos=top-(a.start+j);int z=pos-b.start;
      if(a.d[j] && (z<0||z>=b.length()||b.d[z]!=a.d[j]))return false;
    }
  }
  return true;
}
uint64_t hash_packets(const S&x){uint64_t h=1469598103934665603ULL;for(int i=0;i<4;++i){
  h^=(uint64_t)(unsigned)(x[i].start);h*=1099511628211ULL;
  for(auto d:x[i].d){h^=d;h*=1099511628211ULL;}
}return h;}
int main(int argc,char**argv){
  int T=argc>1?atoi(argv[1]):20000;
  S x;
  x[0]={0,{5,7}};x[1]={0,{7,3}};x[2]={};x[3]={0,{8,8}};
  int G=0,pal=0;int firstbad=-1;
  cout<<"t,G,support,packet0,packet1,packet2,packet3,top_shift,pal,fnv64\n";
  for(int t=0;t<=T;t++){
     G=max(G,needed_G(x));
     int z=0;for(auto &p:x)z+=p.length();
     bool isp=palindrome(x);pal+=isp;
     if(isp&&firstbad==-1)firstbad=t;
     if(t<=3 || t==20||t==44||t==88||t==128||t==264||t==352||t==512||t==1000||t==2000||t==5000||t==10000||t==T){
       cout<<t<<","<<G<<","<<z;
       for(auto&p:x)cout<<","<<p.length();
       cout<<","<<x[3].end()<<","<<isp<<","<<hash_packets(x)<<"\n";
     }
     if(t<T)x=evolve(x);
  }
  cerr<<"RESULT steps="<<T<<" bound="<<G<<" pal_count="<<pal<<" first_pal="<<firstbad<<"\n";
  return 0;
}
