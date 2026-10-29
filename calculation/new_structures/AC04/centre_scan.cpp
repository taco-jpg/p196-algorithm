// AC04 exact endpoint-only centre census (LSD-first coefficient words).
// g++ -std=c++17 -O3 -o centre_scan centre_scan.cpp
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <vector>
using V=std::vector<uint8_t>;
const V B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
const V W={5,18,4,8,1,15,4,0,5};
const int UU[3][3]={{9,6,12},{6,12,9},{12,9,6}};
static V make(int q,int k,int ui,const V& C){
 V h;h.reserve(34+9*q+1+3*k);h.insert(h.end(),B.begin(),B.end());
 for(int i=0;i<q;i++)h.insert(h.end(),W.begin(),W.end());
 h.push_back(5);
 for(int i=0;i<k;i++)for(int v:UU[ui])h.push_back(v);
 V out=h;out.insert(out.end(),C.begin(),C.end());
 out.insert(out.end(),h.rbegin(),h.rend());return out;
}
static int next(V& p,V& tmp,V& digits){
 const int n=p.size();int carry=0;digits.resize(n+1);
 for(int i=0;i<n;i++){int s=int(p[i])+carry;digits[i]=s%10;carry=s/10;}
 int m=n+!!carry;if(carry)digits[n]=carry;
 tmp.resize(m);for(int i=0;i<m;i++)tmp[i]=digits[i]+digits[m-1-i];
 p.swap(tmp);return !!carry;
}
static int test(const V& C,int ui,int q,int k,V& p,V& tmp,V& dig,bool centralOnly,bool& clockOK){
 p=make(q,k,ui,C);const int original=p.size();
 int gamma=0;clockOK=true;
 for(int t=0;t<120;t++){
  int g=next(p,tmp,dig);gamma+=g;
  if(g!=(t%4==0))clockOK=false;
 }
 if(gamma!=30)return -3;
 if(p.size()!=size_t(original+30))return -4;
 int h=34+9*q+1+3*k;int centre0=h+15;
 if(centralOnly){
  int len=std::min(150,centre0);int lo=centre0-len;
  for(int i=lo;i<centre0+int(C.size())+len;i++){
   int expected=(i>=centre0&&i<centre0+int(C.size()))?C[i-centre0]
    :(i<centre0?UU[ui][((i-(h-3*k))%3+3)%3]:UU[ui][((centre0+int(C.size())-1-i)%3+3)%3]);
   if(p[i]!=expected)return i-centre0;
  }
  return 1000000;
 }
 V target=make(q,k+5,ui,C);
 for(size_t i=0;i<p.size();i++)if(p[i]!=target[i])return int(i);
 return 1000000;
}
static V unrank(uint64_t rank,int length){
 V C(length);int half=(length+1)/2;
 for(int i=0;i<half;i++){
  int base=(length%2&&i==half-1)?10:19;
  int z=rank%base;rank/=base;
  C[i]=C[length-1-i]=uint8_t((length%2&&i==half-1)?2*z:z);
 }
 return C;
}
static uint64_t total(int length){uint64_t n=1;for(int i=0;i<length/2;i++)n*=19;if(length%2)n*=10;return n;}
int main(int argc,char**argv){
 if(argc<4){std::cerr<<"usage: centre_scan Uidx length limit [offset] [q] [k] [mode=central|full]\n";return 2;}
 int ui=atoi(argv[1]),length=atoi(argv[2]);uint64_t limit=strtoull(argv[3],0,10),off=argc>4?strtoull(argv[4],0,10):0;
 int q=argc>5?atoi(argv[5]):14,k=argc>6?atoi(argv[6]):100;
 bool central=(argc>7 && !strcmp(argv[7],"central"));
 if(ui<0||ui>=3||length<1||length>16||off>=total(length)){std::cerr<<"bad range\n";return 2;}
 limit=std::min(limit,total(length)-off);V p,tmp,dig;
 uint64_t ok=0,wrongclock=0;int minMismatch=999999,maxMismatch=-999999;std::array<uint64_t,9> buckets{};
 auto start=std::chrono::steady_clock::now();
 for(uint64_t a=off;a<off+limit;a++){
  V C=unrank(a,length);bool clockOK;
  int answer=test(C,ui,q,k,p,tmp,dig,central,clockOK);
  if(!clockOK)wrongclock++;
  if(answer==1000000){ok++;if(ok<=10){std::cout<<"FOUND rank="<<a<<" C=";for(int z:C)std::cout<<z<<",";std::cout<<"\n";}}
  else {minMismatch=std::min(minMismatch,answer);maxMismatch=std::max(maxMismatch,answer);
    if(answer<0)buckets[0]++;
    else if(central)buckets[std::min(8,1+std::abs(answer)/20)]++;
    else buckets[std::min(8,1+answer/150)]++;
  }
 }
 auto end=std::chrono::steady_clock::now();double s=std::chrono::duration<double>(end-start).count();
 std::cout<<"RESULT U="<<ui<<" L="<<length<<" total="<<total(length)<<" offset="<<off<<" tested="<<limit<<" mode="<<(central?"central":"full")<<" successes="<<ok<<" wrongclock="<<wrongclock<<" min_mismatch="<<minMismatch<<" max_mismatch="<<maxMismatch<<" seconds="<<s<<" buckets=";
 for(auto z:buckets)std::cout<<z<<",";
 std::cout<<"\n";
}