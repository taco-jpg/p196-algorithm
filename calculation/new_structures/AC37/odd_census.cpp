// AC37: exact decimal reverse-and-add endpoint-only census; no strict W9 filter.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <vector>
using V=std::vector<uint8_t>;
static const std::array<int,34> B4={10,4,7,5,13,6,11,1,9,16,16,18,10,9,4,8,1,7,0,2,15,15,9,7,7,10,17,14,18,8,6,6,18,4};
static const std::array<int,9> W4={8,1,15,4,0,5,5,18,4};
struct Outcome {bool ret;int first;int gamma;int n;bool clock;};
V coefficients(const std::array<uint8_t,6>& J,const std::array<uint8_t,3>& U,const V& C,int q,int k){
 V h;h.reserve(34+9*q+6+3*k);
 for(int x:B4)h.push_back(x);
 for(int t=0;t<q;t++)for(int x:W4)h.push_back(x);
 for(int x:J)h.push_back(x);
 for(int t=0;t<k;t++)for(int x:U)h.push_back(x);
 V p=h;p.insert(p.end(),C.begin(),C.end());p.insert(p.end(),h.rbegin(),h.rend());return p;
}
V realize(const V& p){
 V d(p.size());int n=(int)p.size();
 for(int i=0;i<n/2;i++){
  d[i]=(p[i]>9)?p[i]-9:0;d[n-1-i]=(p[i]>9)?9:p[i];
 }
 if(n%2){if(p[n/2]%2)std::abort();d[n/2]=p[n/2]/2;}
 if(d.back()==0)std::abort();return d;
}
Outcome replay(const std::array<uint8_t,6>& J,const std::array<uint8_t,3>& U,const V& C,int q,int k){
 V p=coefficients(J,U,C,q,k),d=realize(p);
 int n=(int)d.size(),gamma=0;bool clock=true;
 d.resize(n+122);V buf(d.size());
 for(int t=0;t<120;t++){
  int carry=0;
  for(int i=0;i<n;i++){int s=d[i]+d[n-1-i]+carry;buf[i]=s%10;carry=s/10;}
  gamma+=carry;clock=clock&&(carry==(t%4==0));
  if(carry)buf[n++]=1;
  d.swap(buf);
 }
 V target=coefficients(J,U,C,q,k+5);
 int first=0,lim=(int)std::min((size_t)n,target.size());
 while(first<lim && d[first]+d[n-1-first]==target[first])first++;
 bool ok=(first==lim && n==(int)target.size());
 return {ok,ok?-1:first,gamma,n,clock};
}
int main(int argc,char**argv){
 if(argc!=3){std::cerr<<"usage: ac37_odd j0 j1 (both in [0,18])\n";return 2;}
 int j0=std::atoi(argv[1]),j1=std::atoi(argv[2]);
 if(j0<0||j0>=19||j1<0||j1>=19)return 3;
 const std::array<uint8_t,3> u0={9,0,18},u28={18,0,9};
 long long enumerated=0,eligible=0,checks=0,returns=0,clock_failures=0;
 std::map<int,long long> hist;
 for(int j2=0;j2<19;j2++)for(int j3=0;j3<19;j3++)
 for(int j4=0;j4<19;j4++)for(int j5=0;j5<19;j5++){
  std::array<uint8_t,6> J={(uint8_t)j0,(uint8_t)j1,(uint8_t)j2,(uint8_t)j3,(uint8_t)j4,(uint8_t)j5};
  enumerated++;
  int A=j0-j1+j2-j3+j4-j5;
  if((A%11+11)%11!=5)continue;  // only necessary for UNIFORM ODD-centre recurrence
  eligible++;
  for(auto U:{u0,u28}){
   auto r=replay(J,U,V{4,14,4},14,100);
   checks++;if(r.ret){
    returns++;std::cout<<"RETURN J=";
    for(int x:J)std::cout<<x<<",";
    std::cout<<" U=";for(int x:U)std::cout<<x<<",";
    std::cout<<"\n";
   }
   if(!r.clock||r.gamma!=30)clock_failures++;
   hist[r.first]++;
  }
 }
 std::cout<<"RESULT j0="<<j0<<" j1="<<j1<<" enumerated="<<enumerated
          <<" eligible="<<eligible<<" checked="<<checks
          <<" returns="<<returns<<" invalid_clock="<<clock_failures<<"\n";
 for(auto [i,c]:hist)std::cout<<"MISMATCH "<<i<<" "<<c<<"\n";
 return 0;
}
