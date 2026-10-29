// Independent GNU GMP integer checker. No call to W01's digit-array step.
#include <gmpxx.h>
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
#include <deque>
using namespace std;
static const int ROOT[39]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const int BULK[20]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
string seed(int h,int flags){string s(2*h,'0');for(int j=0;j<h;j++){
 int q=j<39?ROOT[j]:BULK[(j-39)%20];
 if((flags&1)&&j>=6000&&j<6050)q=(7*j+11)%19;
 if((flags&2)&&j>=8000&&j<8050)q=(3*j+7)%19;
 int a=min(q,9),b=q-a;s[2*h-1-j]=char('0'+a);s[j]=char('0'+b);}
 return s;}
int coef(const string&s,int j){return s[j]-'0'+s[s.size()-1-j]-'0';}
uint64_t hashstr(const string&s){uint64_t h=1469598103934665603ULL;for(unsigned char a:s){h^=a;h*=1099511628211ULL;}return h;}
struct R{int front;array<int,61> q,low,high;};
R residual(const array<string,4>&s){int n=s[0].size()/2,front=-1;
 auto get=[&](int k,int j,int side){return s[k][side?j:s[k].size()-1-j]-'0';};
 auto delta=[&](int j,int side){return get(3,j,side)-get(2,j,side)-get(1,j,side)+get(0,j,side);};
 for(int j=0;j<n;j++)if(delta(j,0)+delta(j,1)){front=j;break;}
 R r{};r.front=front;
 if(front>=0)for(int k=0;k<61;k++){int j=front-20+k;if(j<0||j>=n){cerr<<"OUT_OF_RANGE";exit(2);}r.low[k]=delta(j,0);r.high[k]=delta(j,1);r.q[k]=r.low[k]+r.high[k];}
 return r;
}
int main(int argc,char**argv){int T=argc>1?atoi(argv[1]):6000;int shift=argc>2?atoi(argv[2]):20;array<mpz_class,4> n;for(int k=0;k<4;k++)n[k]=mpz_class(seed(12000,k),10);
 deque<R> prev;int first=-1,last_failure=-1,check_count=0;
 for(int t=0;t<=T;t++){
  array<string,4>s;for(int k=0;k<4;k++)s[k]=n[k].get_str(10);
  R r=residual(s);if(r.front>=0&&first<0)first=t;
  if(t>=2242){const R &o=prev[prev.size()-88];bool front=r.front==o.front-shift;bool ok=front&&r.q==o.q&&r.low==o.low&&r.high==o.high;
   if(!ok)last_failure=t;if(t>=2836){if(!ok){cerr<<"BAD_GMP_RESIDUAL t="<<t<<" first="<<r.front<<" old="<<o.front<<"\n";return 2;}check_count++;}
  }
  prev.push_back(r);if(prev.size()>89)prev.pop_front();
  if(t<T)for(int k=0;k<4;k++){string rev=s[k];reverse(rev.begin(),rev.end());n[k]+=mpz_class(rev,10);}
 }
 if(first!=2154||last_failure!=2835){cerr<<"BAD_ONSET first="<<first<<" last_failure="<<last_failure<<"\n";return 3;}
 cout<<"W01_SCATTER_GMP_PASS first="<<first<<" last_failure="<<last_failure<<" stable_windows="<<check_count<<"\n";
}
