// Independent GMP integer N + rev_10(N), reconstruct full pairword each step.
#include <gmpxx.h>
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <fstream>
using namespace std;
static const int X[6]={8,16,14,10,2,4};
static const int Y[6]={16,14,10,2,4,8};
uint64_t hash_pairword(const vector<int>&d){uint64_t h=14695981039346656037ULL;for(int x:d){h^=uint64_t(x);h*=1099511628211ULL;}return h;}
struct Band{int start=-1,len=-1;};
pair<Band,Band> bands(const vector<int>&p,int t){
 int half=(p.size()+1)/2;Band a,b;
 for(int i=0;i<half;){int j=i+1;while(j<half&&p[j]==p[i])++j;
  if(p[i]==X[t%6]&&j-i>a.len)a={i,j-i};
  if(p[i]==Y[t%6]&&j-i>b.len)b={i,j-i};
  i=j;
 }
 return {a,b};
}
int main(int argc,char**argv){
 int k=argc>1?atoi(argv[1]):15000,T=argc>2?atoi(argv[2]):20000,minrun=argc>3?atoi(argv[3]):100;
 string seed="9"+string(k,'8')+"59"+string(k,'9')+"80"+string(k,'7')+"20"+string(k,'0')+"1";
 int start=argc>4?atoi(argv[4]):0;
 string input_path=argc>5?argv[5]:"-", output_path=argc>6?argv[6]:"-";
 string initial=seed;
 if(start>0){ifstream input(input_path);if(!getline(input,initial))return 8;}
 mpz_class N(initial,10);
 int minA=1<<30,minB=1<<30,maxGap=0;
 cout<<"step,digits,pair_fnv64,left_start,left_count,right_start,right_count,junction\n";
 for(int t=start;t<=T;t++){
  string s=N.get_str(10);int n=s.size();
  if(equal(s.begin(),s.begin()+n/2,s.rbegin())){cerr<<"PAL at step "<<t<<"\n";return 2;}
  vector<int>pairs(n);for(int i=0;i<n;i++)pairs[i]=(s[i]-'0')+(s[n-1-i]-'0');
  auto [a,b]=bands(pairs,t);
  if(a.len<minrun||b.len<minrun||b.start<a.start+a.len){
   cerr<<"BLOCK_SHAPE_FAILURE t="<<t<<" left="<<a.len<<" right="<<b.len<<"\n";return 3;
  }
  minA=min(minA,a.len);minB=min(minB,b.len);maxGap=max(maxGap,b.start-a.start-a.len);
  cout<<t<<","<<n<<","<<hex<<setw(16)<<setfill('0')<<hash_pairword(pairs)<<dec<<","<<a.start<<","<<a.len<<","<<b.start<<","<<b.len<<","<<(b.start-a.start-a.len)<<"\n";
  if(t==T){
   if(output_path!="-"){ofstream out(output_path);out<<s<<"\n";}
   break;
  }
  reverse(s.begin(),s.end());N+=mpz_class(s,10);
 }
 cerr<<"GMP_PASS states="<<(T-start+1)<<" final_digits="<<N.get_str(10).size()<<" min_left="<<minA<<" min_right="<<minB<<" max_gap="<<maxGap<<"\n";
}