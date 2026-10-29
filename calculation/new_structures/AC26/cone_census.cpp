// AC26: centre-independent, endpoint-only two-ended carry-cone census.
// Full U=(9,0,18) rotations: ./cone_census 0 2476099 0 3 35
// Follow up any unresolved code with: ./cone_census <code> 1 <u_index> 1 100
// Compile: c++ -std=c++17 -O3 -march=native -o cone_census cone_census.cpp
// No strict-per-phase W9 pruning, no finite-radius assumption.
#include <array>
#include <algorithm>
#include <iostream>
#include <map>
#include <cstdlib>
using A=std::array<int,512>;
const int B[]={1,5,11,12,9,10,8,3,11,6,14,16,10,0,14,12,9,8,7,2,8,12,5,17,14,8,9,13,14,17,14,12,15,13};
const int W[]={12,9,7,10,4,5,10,14,13};
struct State{A p{},next{},low{},high{};int len=0;};
void init(State &s,int code,const std::array<int,3>&u,int r=35){
 int at=0;
 for(int x:B)s.p[at++]=x;
 for(int q=0;q<14;q++)for(int x:W)s.p[at++]=x;
 for(int j=0;j<5;j++){s.p[at++]=code%19;code/=19;}
 for(int j=0;j<r;j++)for(int x:u)s.p[at++]=x;
 s.len=at;
}
// For coefficients <=18, incoming high carry is 0/1. The two carry
// trajectories coalesce at the first non-9 coefficient (from inner cut).
// Thus discard trailing-nine-run length+1 high digits, with overflow shift.
int step(State &s){
 int L=s.len,j=0;
 while(j<L && s.p[L-1-j]==9)j++;
 if(j==L)return -1; // overflow ambiguous, never claim exclusion
 int carry=0;
 for(int i=0;i<L;i++){int v=s.p[i]+carry;s.low[i]=v%10;carry=v/10;}
 carry=0;
 for(int i=L-1;i>=0;i--){int v=s.p[i]+carry;s.high[i]=v%10;carry=v/10;}
 int gamma=carry, cut=L-j-1+gamma;
 for(int i=0;i<cut;i++){
   int upper=(gamma?(i==0?1:s.high[i-1]):s.high[i]);
   s.next[i]=s.low[i]+upper;
 }
 s.len=cut;s.p.swap(s.next);
 return gamma;
}
int test(int code,std::array<int,3> u,int r=35){
 State s;init(s,code,u,r);
 for(int t=0;t<120;t++){
  int gamma=step(s);
  if(gamma<0 || gamma!=(t%4==3))return -2;
 }
 A wanted;int n=0;
 for(int x:B)wanted[n++]=x;
 for(int q=0;q<14;q++)for(int x:W)wanted[n++]=x;
 for(int i=0;i<5;i++){wanted[n++]=code%19;code/=19;}
 for(int i=0;i<r+5;i++)for(int x:u)wanted[n++]=x;
 for(int i=0;i<s.len;i++)if(s.p[i]!=wanted[i])return i;
 return -1; // undecided by the prefix, NOT a full return
}
int main(int argc,char**argv){
 int start=argc>1?std::atoi(argv[1]):0;
 int count=argc>2?std::atoi(argv[2]):100;
 int ustart=argc>3?std::atoi(argv[3]):0;
 int ucount=argc>4?std::atoi(argv[4]):30;
 int r=argc>5?std::atoi(argv[5]):35;
 if(start<0||count<=0||start+count>2476099||ustart<0||ustart+ucount>30||r<0||r>100)return 2;
 long long unresolved=0,ambiguous=0,total=0;std::map<int,long long>hist;
 for(int id=ustart;id<ustart+ucount;id++){
  int a=(id/3)*2,shift=id%3;
  std::array<int,3>base={9,a,18-a};
  std::array<int,3>u={base[shift],base[(shift+1)%3],base[(shift+2)%3]};
  for(int code=start;code<start+count;code++){
   int first=test(code,u,r);total++;
   if(first==-1){unresolved++;std::cout<<"UNRESOLVED uid="<<id<<" Jcode="<<code<<"\n";}
   else if(first==-2)ambiguous++;
   else hist[first]++;
  }
 }
 std::cout<<"tested="<<total<<" unresolved="<<unresolved<<" clock_ambiguous="<<ambiguous<<" hist=";
 for(auto [first,count]:hist)std::cout<<first<<":"<<count<<",";
 std::cout<<"\n";
}
