// AC20: exhaustive endpoint-only phase-11 W9 prefix necessary-condition census.
// All 120 decimal coefficient/carry steps are computed; no phasewise W9 pruning.
#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <mutex>
#include <string>
#include <thread>
#include <vector>
using namespace std;
using Word=vector<uint8_t>;
constexpr int B[34]={5,2,3,3,3,16,9,7,18,6,0,1,5,8,13,9,18,12,12,8,12,8,17,9,6,14,5,18,14,11,12,11,9,12};
constexpr int W[9]={2,9,2,4,0,17,11,9,12};
constexpr int Q=14,K=100,PREFIX=34+9*Q,MAXN=1100;
struct Counts {uint64_t tested=0,retain=0,wrong_clock=0,wrong_size=0;array<uint64_t,MAXN+1> mismatch{};vector<string> survivors;};
static Word uword(int index){int a=2*(index/3),rot=index%3;Word u={(uint8_t)9,(uint8_t)a,(uint8_t)(18-a)};rotate(u.begin(),u.begin()+rot,u.end());return u;}
static void construct(uint8_t*p,int&len,const uint8_t*j,int nj,const Word&u,const Word&c){
 int h=0;for(int x:B)p[h++]=(uint8_t)x;for(int r=0;r<Q;r++)for(int x:W)p[h++]=(uint8_t)x;
 for(int r=0;r<nj;r++)p[h++]=j[r];
 for(int r=0;r<K;r++)for(auto x:u)p[h++]=x;
 len=2*h+(int)c.size();for(int z=0;z<(int)c.size();z++)p[h+z]=c[z];
 for(int z=0;z<h;z++)p[h+c.size()+z]=p[h-1-z];
}
static int epoch(uint8_t*p,int&n,uint8_t*d,uint8_t*next){int count=0;
 for(int t=0;t<120;t++){
  int carry=0;for(int i=0;i<n;i++){int x=p[i]+carry;d[i]=(uint8_t)(x%10);carry=x/10;}
  if(carry){if(n+1>=MAXN)return -1;d[n++]=(uint8_t)carry;count++;}
  for(int i=0;i<(n+1)/2;i++){int z=d[i]+d[n-1-i];next[i]=(uint8_t)z;next[n-1-i]=(uint8_t)z;}
  uint8_t*tmp=p;p=next;next=tmp;
 }
 // Even 120 swaps: original buffer p is final.
 return count;
}
static void process(int rank,int ctype,int cap,Counts&ans){
 Word u=uword(rank),c=ctype?Word{4,4}:Word{4,14,4};
 alignas(64) uint8_t p[MAXN],nxt[MAXN],digits[MAXN];uint8_t j[4];
 for(int nj=3;nj<=4;nj++){
  int count=nj==3?6859:130321;if(cap>0)count=min(count,cap);
  for(int x=0;x<count;x++){
   int y=x;for(int z=0;z<nj;z++){j[z]=y%19;y/=19;}
   int n=0;construct(p,n,j,nj,u,c);int gam=epoch(p,n,digits,nxt);ans.tested++;
   if(gam!=30)ans.wrong_clock++;
   if(n!=2*(34+9*Q+nj+3*(K+5))+(int)c.size())ans.wrong_size++;
   int diff=0;while(diff<34&&p[diff]==B[diff])diff++;
   while(diff<PREFIX&&p[diff]==W[(diff-34)%9])diff++;
   if(diff==PREFIX){ans.retain++;if(ans.survivors.size()<20){string s="U="+to_string(rank)+" C="+to_string(ctype)+" J=";for(int z=0;z<nj;z++)s+=to_string(j[z])+",";ans.survivors.push_back(s);}}
   else ans.mismatch[diff]++;
  }
 }
}
int main(int argc,char**argv){
 int start=argc>1?atoi(argv[1]):0,stop=argc>2?atoi(argv[2]):30,nc=argc>3?atoi(argv[3]):2,nthread=argc>4?atoi(argv[4]):4,cap=argc>5?atoi(argv[5]):0;
 atomic<int> next(0);vector<pair<int,int>> jobs;for(int c=0;c<nc;c++)for(int u=start;u<stop;u++)jobs.emplace_back(u,c);
 vector<Counts> results(jobs.size());auto began=chrono::steady_clock::now();vector<thread> th;
 for(int tid=0;tid<nthread;tid++)th.emplace_back([&](){
  int i;while((i=next.fetch_add(1))<(int)jobs.size()){
   auto [rank,ctype]=jobs[i];process(rank,ctype,cap,results[i]);
   {static mutex mu;lock_guard<mutex> lock(mu);cerr<<"FINISHED rank="<<rank<<" parity="<<ctype<<" checked="<<results[i].tested<<" retain="<<results[i].retain<<" clock_error="<<results[i].wrong_clock<<" size_error="<<results[i].wrong_size<<"\n";}
  }
 });
 for(auto&t:th)t.join();Counts total;
 for(auto&r:results){total.tested+=r.tested;total.retain+=r.retain;total.wrong_clock+=r.wrong_clock;total.wrong_size+=r.wrong_size;for(int i=0;i<=MAXN;i++)total.mismatch[i]+=r.mismatch[i];total.survivors.insert(total.survivors.end(),r.survivors.begin(),r.survivors.end());}
 cout<<"SUMMARY start="<<start<<" stop="<<stop<<" centres="<<nc<<" total="<<total.tested<<" W9_retained="<<total.retain<<" clock_errors="<<total.wrong_clock<<" length_errors="<<total.wrong_size<<" elapsed_s="<<chrono::duration<double>(chrono::steady_clock::now()-began).count()<<"\n";
 cout<<"FIRST_MISMATCH";for(int i=0;i<=MAXN;i++)if(total.mismatch[i])cout<<" "<<i<<":"<<total.mismatch[i];cout<<"\n";for(auto&s:total.survivors)cout<<"SURVIVOR "<<s<<"\n";
}