// Agent X24 exploratory delayed-merger scan. Non-exhaustive for sampled width 5.
// g++ -O3 -std=c++17 depth_sweep.cpp -o depth_sweep
// ./depth_sweep 4 2 30
// ./depth_sweep 5 2 80 200000
#include <bits/stdc++.h>
using namespace std;
string B,W;
string encode(initializer_list<int> d){string x;for(int a:d)x+=char(a);return x;}
string F(const string& p){
 int c=0,n=p.size();string d(n,'\0');
 for(int i=0;i<n;i++){int v=(unsigned char)p[i]+c;d[i]=char(v%10);c=v/10;}
 if(c)d+=char(c);
 string q(d.size(),'\0');
 for(int i=0;i<(int)d.size();i++)q[i]=char((unsigned char)d[i]+(unsigned char)d[d.size()-1-i]);
 return q;
}
uint64_t H(const string& s){uint64_t h=0xcbf29ce484222325ull;for(char c:s){h^=(unsigned char)c;h*=0x100000001b3ull;}return h;}
string ss(const string& s){string out;for(unsigned char c:s)out+=to_string((int)c)+",";return out;}
int main(int argc,char**argv){
 int h=argc>1?atoi(argv[1]):4,r=argc>2?atoi(argv[2]):2,cap=argc>3?atoi(argv[3]):50,subset=argc>4?atoi(argv[4]):0;
 B=encode({17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13});
 W=encode({17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13});
 string left=B;for(int i=0;i<r;i++)left+=W;
 auto outer=left;reverse(outer.begin(),outer.end());
 int TOTAL=1;for(int i=0;i<h;i++)TOTAL*=19;
 int N=subset?min(TOTAL,subset):TOTAL;
 cerr<<"halfwidth="<<h<<" r="<<r<<" n_candidates="<<N<<" maxdepth="<<cap<<"\n";
 vector<string>curr(N),prev(N),cores(N);
 for(int ix=0;ix<N;ix++){
  int x=(subset?((int)((104729LL*ix+1234567)%TOTAL)):ix);
  string c(h,'\0');for(int j=0;j<h;j++){c[j]=char(x%19);x/=19;}
  string rc=c;reverse(rc.begin(),rc.end());cores[ix]=c;
  curr[ix]=left+c+rc+outer;
 }
 for(int t=0;t<cap;t++){
  unordered_map<uint64_t,int> seen;seen.reserve(N*2);
  int firstA=-1,firstB=-1,distinct=0;
  for(int ix=0;ix<N;ix++){
   string out=F(curr[ix]);uint64_t key=H(out);
   auto j=seen.find(key);
   if(j!=seen.end()&&out==prev[j->second]&&curr[ix]!=curr[j->second]){
    if(firstA<0){firstA=j->second;firstB=ix;}
    distinct++;
   }
   if(j==seen.end())seen.emplace(key,ix);
   prev[ix].swap(out);
  }
  if(firstA>=0)cout<<"merger at numeric t="<<(t+2)<<" pairwords="
   <<ss(cores[firstA])<<" :: "<<ss(cores[firstB])<<" collision_pairs="<<distinct<<"\n"<<flush;
  prev.swap(curr);
  if(t%10==0)cerr<<"checked step "<<t<<"\n";
 }
}
