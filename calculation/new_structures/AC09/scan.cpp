// AC09: exact full-decimal folded pairword; NO intermediate strict-W9 pruning.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
static constexpr int B[]={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static constexpr int W[]={5,18,4,8,1,15,4,0,5};
static constexpr int U[3][3]={{9,16,2},{16,2,9},{2,9,16}};
struct Engine {
 std::array<uint8_t,10000> a{},b{},d{};
 uint8_t *p=a.data(),*next=b.data();
 int n=0;bool clock=true;
 void init(int uid,int clen,const int*half,int q,int k) {
  n=0;p=a.data();next=b.data();
  for(int x:B)p[n++]=x;
  for(int i=0;i<q;i++)for(int x:W)p[n++]=x;
  p[n++]=5;
  for(int i=0;i<k;i++)for(int x:U[uid])p[n++]=x;
  for(int i=0;i<clen;i++)p[n++]=half[i<clen/2?i:clen-1-i];
  int h=34+9*q+1+3*k;
  for(int i=h-1;i>=0;i--)p[n++]=p[i];
  clock=true;
 }
 void run(){
  for(int t=0;t<120;t++){
   int carry=0;
   for(int i=0;i<n;i++){int z=p[i]+carry;d[i]=z%10;carry=z/10;}
   int z=n+carry;
   if(carry)d[n]=carry;
   if(carry!=(t%4==0))clock=false;
   for(int i=0;i<z;i++)next[i]=d[i]+d[z-1-i];
   std::swap(p,next);n=z;
  }
 }
 bool centre_matches(int uid,int clen,const int*half,int collar=10)const{
  int mid=n/2;
  if(n%2!=clen%2)return false;
  for(int i=0;i<2*collar+clen;i++){
   int at=mid+i-(collar+clen/2),want;
   if(i<collar)want=U[uid][((i-collar)%3+3)%3];
   else if(i>=collar+clen)want=U[uid][2-(i-collar-clen)%3];
   else {int j=i-collar;want=half[j<clen/2?j:clen-1-j];}
   if(at<0||at>=n||p[at]!=want)return false;
  }
  return true;
 }
};
static uint64_t p19(int n){uint64_t v=1;while(n--)v*=19;return v;}
int main(int argc,char**argv){
 if(argc<4){std::cerr<<"usage: scan LENGTH UID LIMIT [Q] [K]; limit=0 for full\n";return 2;}
 int len=std::atoi(argv[1]),uid=std::atoi(argv[2]),q=argc>4?std::atoi(argv[4]):14,k=argc>5?std::atoi(argv[5]):100;
 uint64_t limit=std::strtoull(argv[3],nullptr,10),total=p19(len/2)*(len%2?10:1);
 if(len<1||len>20||uid<0||uid>2||q<0||k<0||2*(34+9*q+1+3*k+len)+120>10000)return 2;
 if(!limit||limit>total)limit=total;
 int v[10]={};Engine e;uint64_t hits=0,clock_bad=0;
 for(uint64_t j=0;j<limit;j++){
  uint64_t r=j;for(int t=0;t<(len+1)/2;t++){
   if(len%2&&t==len/2){v[t]=2*(r%10);r/=10;}
   else {v[t]=r%19;r/=19;}
  }
  e.init(uid,len,v,q,k);e.run();
  if(!e.clock)clock_bad++;
  if(e.centre_matches(uid,len,v)){
   hits++;
   if(hits<=8)std::cout<<"HIT uid="<<uid<<" len="<<len<<" index="<<j<<"\n";
  }
 }
 std::cout<<"CELL len="<<len<<" uid="<<uid<<" tested="<<limit<<" total="<<total<<" hits="<<hits<<" clock_fail="<<clock_bad<<"\n";
 return 0;
}
