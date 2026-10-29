// AC28: exact centre-independent prefix gate for phase-7 p12/m9, LSD-first.
// g++ -O3 -march=native -std=c++17 -fopenmp prefix_census.cpp -o prefix_census
#include <bits/stdc++.h>
#include <omp.h>
using namespace std;
using Byte=uint8_t;
const int B7[34]={5,2,7,12,0,3,14,15,5,9,0,9,3,4,18,11,9,15,9,10,14,10,5,12,0,17,9,16,1,14,1,14,4,17};
const int W7[9]={11,9,12,2,9,2,4,0,17};
struct A {
 vector<Byte> p,lo,hi0,hi1,out;
 int gamma=0;
 void init(const array<int,5>&J,const array<int,3>&U,int q=14,int k=50) {
  gamma=0;p.clear();p.reserve(1200);
  for(int z:B7)p.push_back(z);
  for(int c=0;c<q;++c)for(int z:W7)p.push_back(z);
  for(int z:J)p.push_back(z);
  for(int c=0;c<k;++c)for(int z:U)p.push_back(z);
  lo.resize(p.size());hi0.resize(p.size());hi1.resize(p.size());out.resize(p.size());
 }
 bool step(){
  const int n=p.size();int c=0;
  for(int i=0;i<n;i++){int s=p[i]+c;lo[i]=s%10;c=s/10;}
  int c0=0,c1=1;
  for(int i=n-1;i>=0;i--){
   int s0=p[i]+c0,s1=p[i]+c1;
   hi0[i]=s0%10;hi1[i]=s1%10;c0=s0/10;c1=s1/10;
  }
  if(c0!=c1)return false;
  gamma+=c0;
  int len=0;
  for(int j=0;j<n;j++){
   int h0=c0?(j==0?1:int(hi0[j-1])):int(hi0[j]);
   int h1=c0?(j==0?1:int(hi1[j-1])):int(hi1[j]);
   if(h0!=h1)break;
   out[len++]=lo[j]+h0;
  }
  p.assign(out.begin(),out.begin()+len);
  return len>0;
 }
 int mismatchW(){
  const int limit=34+9*14,n=p.size();
  for(int i=0;i<min(n,limit);i++){
   int want=i<34?B7[i]:W7[(i-34)%9];
   if(p[i]!=want)return i;
  }
  return n<limit?-4:-1;
 }
};
int main(int argc,char**argv){
 const int u=argc>1?atoi(argv[1]):0;
 const int nth=argc>2?atoi(argv[2]):4;
 const int start=argc>3?atoi(argv[3]):0;
 const int count=argc>4?atoi(argv[4]):2476099;
 const int total=19*19*19*19*19;
 if(start<0||count<1||nth<1||start+count>total||u<0||u>=30){
  cerr<<"bad bounds\n";return 2;
 }
 int v=u/3,r=u%3;array<int,3> U={9,2*v,18-2*v};
 rotate(U.begin(),U.begin()+r,U.end());
 vector<map<int,long long>> hists(nth);
 vector<long long> gamma(nth),uncertain(nth),shorts(nth);
 vector<vector<int>> possible(nth);
 double t0=omp_get_wtime();
 #pragma omp parallel num_threads(nth)
 {
  int tid=omp_get_thread_num(); A a;
  #pragma omp for schedule(dynamic,512)
  for(int code=start;code<start+count;code++){
   int x=code;array<int,5> J;
   for(auto&z:J){z=x%19;x/=19;}
   a.init(J,U);bool okay=true;
   for(int t=0;t<120;t++)if(!a.step()){okay=false;break;}
   int mm=okay?a.mismatchW():-5;
   ++hists[tid][mm];
   if(!okay)uncertain[tid]++;
   if(a.gamma!=30)gamma[tid]++;
   if((int)a.p.size()<160)shorts[tid]++;
   if(mm==-1&&possible[tid].size()<30)possible[tid].push_back(code);
  }
 }
 map<int,long long> hist;
 for(auto&h:hists)for(auto [idx,n]:h)hist[idx]+=n;
 cout<<"U="<<U[0]<<","<<U[1]<<","<<U[2]<<" Jcodes="<<start<<".."<<start+count-1
     <<" total="<<count<<" t="<<setprecision(4)<<omp_get_wtime()-t0<<" sec\n";
 cout<<"gammaWrong="<<accumulate(gamma.begin(),gamma.end(),0LL)
     <<" uncertain="<<accumulate(uncertain.begin(),uncertain.end(),0LL)
     <<" short="<<accumulate(shorts.begin(),shorts.end(),0LL)<<"\n";
 cout<<"hist:";for(auto [idx,n]:hist)cout<<" "<<idx<<":"<<n;cout<<"\n";
 cout<<"possible W recover:";for(auto&pr:possible)for(auto code:pr)cout<<" "<<code;
 cout<<"\n";
}