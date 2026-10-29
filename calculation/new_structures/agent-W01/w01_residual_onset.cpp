// W01: independent digit-vector construction of a base-10 two-pulse interaction
// starting from N13's rooted period-8 / period-20 lattice, extended across 20k steps.
#include <bits/stdc++.h>
using namespace std; using V=vector<uint8_t>;
static const int ROOT[39]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const int BULK[20]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
V seed(int h,int flags,int x=6000,int y=8000){V a(2*h);for(int j=0;j<h;j++){
 int q=j<39?ROOT[j]:BULK[(j-39)%20];
 if((flags&1) && j>=x && j<x+50)q=(7*j+11)%19;
 if((flags&2) && j>=y && j<y+50)q=(3*j+7)%19;
 a[j]=min(q,9);a[2*h-j-1]=q-a[j];}return a;}
void step(V &a){int n=a.size(),carry=0;V b(n+1);for(int i=0;i<n;i++){
 int z=a[i]+a[n-1-i]+carry;b[i]=z%10;carry=z/10;}
 if(carry)b[n]=carry;else b.pop_back();a.swap(b);}
int pairval(const V&v,int j){return v[j]+v[v.size()-1-j];}
int first(const V&a,const V&b){int n=min(a.size(),b.size())/2;for(int j=0;j<n;j++)if(pairval(a,j)!=pairval(b,j))return j;return -1;}
struct Snap{array<V,4> v;int fb,fd;};
bool matchwin(const array<V,4> &curr,const Snap &old,int f,int oldf,int r0=-40,int r1=40){
 for(int k:{0,1,3})for(int r=r0;r<=r1;r++){
  const V&a=curr[k],&b=old.v[k];int j=f+r,p=oldf+r;
  if(j<0||p<0||j>=(int)a.size()/2||p>=(int)b.size()/2)return false;
  if(a[j]!=b[p]||a[a.size()-1-j]!=b[b.size()-1-p])return false;
 }
 return true;
}
int main(int argc,char**argv){int T=argc>1?atoi(argv[1]):20000;array<V,4> v;for(int k=0;k<4;k++)v[k]=seed(12000,k);int first=-1;struct Snap{int front;vector<int8_t> r,low,high;};deque<Snap> prior;int countRec=0,countFrontRec=0,countDigitRec=0,firstDigitBad=-1,lastDigitBad=-1,firstBad=-1,lastBad=-1,firstFrontBad=-1,lastFrontBad=-1,firstCheck=2242;
 cout<<"t,res_lo,res_hi,res_cnt,res_sum,res_l1,front88,reswin88\n";
 for(int t=0;t<=T;t++){
 int n=v[0].size()/2;vector<int8_t> r(n),low(n),high(n);int lo=-1,hi=-1,cnt=0,sum=0,l1=0;
 for(int j=0;j<n;j++){int z=pairval(v[3],j)-pairval(v[2],j)-pairval(v[1],j)+pairval(v[0],j);r[j]=z;
 low[j]=(int)v[3][j]-(int)v[2][j]-(int)v[1][j]+(int)v[0][j];
 high[j]=(int)v[3][v[3].size()-1-j]-(int)v[2][v[2].size()-1-j]-(int)v[1][v[1].size()-1-j]+(int)v[0][v[0].size()-1-j];
 if(z){if(lo<0)lo=j;hi=j;cnt++;sum+=z;l1+=abs(z);}}
 if(first<0&&cnt)first=t;
 int a=-1,b=-1;
 if(t>=88&&t>=firstCheck&&lo>=0){auto& old=prior[prior.size()-88];a=lo==old.front-20;countFrontRec+=a;
 b=a;bool physical=a;for(int off=-20;off<=40;off++)if(lo+off<0||old.front+off<0||lo+off>=n||old.front+off>=(int)old.r.size()||r[lo+off]!=old.r[old.front+off])b=0;
 for(int off=-20;off<=40;off++)if(lo+off<0||old.front+off<0||lo+off>=n||old.front+off>=(int)old.low.size()||low[lo+off]!=old.low[old.front+off]||high[lo+off]!=old.high[old.front+off])physical=false;
 countDigitRec+=physical;if(!physical){if(firstDigitBad<0)firstDigitBad=t;lastDigitBad=t;}
 countRec+=b;if(!a){if(firstFrontBad<0)firstFrontBad=t;lastFrontBad=t;}if(!b){if(firstBad<0)firstBad=t;lastBad=t;}}
 if(t%100==0||(t>=first&&t<first+30))cout<<t<<","<<lo<<","<<hi<<","<<cnt<<","<<sum<<","<<l1<<","<<a<<","<<b<<"\n";
 prior.push_back({lo,move(r),move(low),move(high)});if(prior.size()>89)prior.pop_front();
 if(t<T)for(auto &x:v)step(x);
 }
 cerr<<"W01_RESIDUAL first="<<first<<" stable_front_count="<<countFrontRec<<" stable_window_count="<<countRec<<" stable_physical_residual_count="<<countDigitRec<<" first_physical_failure="<<firstDigitBad<<" last_physical_failure="<<lastDigitBad<<" first_front_failure="<<firstFrontBad<<" last_front_failure="<<lastFrontBad<<" first_window_failure="<<firstBad<<" last_window_failure="<<lastBad<<" tested_time="<<firstCheck<<".."<<T<<"\n";
}