// Decimal folded-pairword two-block transport. Ordinary digit-vector reverse/add.
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
using namespace std;
static const int X[6]={8,16,14,10,2,4};
static const int Y[6]={16,14,10,2,4,8};
uint64_t fnv_pair(const vector<unsigned char>&d){
 uint64_t h=14695981039346656037ULL;int n=d.size();
 for(int i=0;i<n;i++){h^=uint64_t(d[i]+d[n-1-i]);h*=1099511628211ULL;}return h;
}
struct Band{int start=-1,len=-1;};
static pair<Band,Band> bands(const vector<unsigned char>&d,int t){
 int n=d.size(),h=(n+1)/2;Band a,b;
 for(int i=0;i<h;){int p=d[i]+d[n-1-i], j=i+1;
   while(j<h && d[j]+d[n-1-j]==p)++j;
   if(p==X[t%6]&&j-i>a.len)a={i,j-i};
   if(p==Y[t%6]&&j-i>b.len)b={i,j-i};
   i=j;
 }
 return {a,b};
}
int main(int argc,char**argv){
 int k=argc>1?atoi(argv[1]):15000,T=argc>2?atoi(argv[2]):20000,minrun=argc>3?atoi(argv[3]):100;
 string s="9"+string(k,'8')+"59"+string(k,'9')+"80"+string(k,'7')+"20"+string(k,'0')+"1";
 vector<unsigned char>d;for(auto it=s.rbegin();it!=s.rend();++it)d.push_back(*it-'0');
 int first_pal=-1,minA=1<<30,minB=1<<30,maxGap=0;
 cout<<"step,digits,pair_fnv64,left_start,left_count,right_start,right_count,junction\n";
 for(int t=0;t<=T;t++){
  int n=d.size();
  bool pal=true;for(int i=0;i<n/2;i++)if(d[i]!=d[n-1-i]){pal=false;break;}
  if(pal){cerr<<"PAL at step "<<t<<"\n";return 2;}
  auto [a,b]=bands(d,t);
  if(a.len<minrun||b.len<minrun||b.start<a.start+a.len){
    cerr<<"BLOCK_SHAPE_FAILURE t="<<t<<" left="<<a.len<<" right="<<b.len<<" astart="<<a.start<<" bstart="<<b.start<<"\n";return 3;
  }
  minA=min(minA,a.len);minB=min(minB,b.len);maxGap=max(maxGap,b.start-a.start-a.len);
  cout<<t<<","<<n<<","<<hex<<setw(16)<<setfill('0')<<fnv_pair(d)<<dec<<","<<a.start<<","<<a.len<<","<<b.start<<","<<b.len<<","<<(b.start-a.start-a.len)<<"\n";
  if(t==T)break;
  vector<unsigned char>next(n+1);int carry=0;
  for(int i=0;i<n;i++){int x=d[i]+d[n-1-i]+carry;next[i]=x%10;carry=x/10;}
  if(carry)next[n]=carry;else next.pop_back();d.swap(next);
 }
 cerr<<"DIGITS_PASS states="<<(T+1)<<" final_digits="<<d.size()<<" min_left="<<minA<<" min_right="<<minB<<" max_gap="<<maxGap<<"\n";
}