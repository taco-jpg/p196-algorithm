// W09 exact decimal digit-array replay; compile with c++ -std=c++17 -O3.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;
using D=vector<uint8_t>;
static const int L[]={7,12,16,10,7,4,12,8,15,13,17,1,17,18,16,3,5,0,2,12,18,10,1};
static const int PH[]={8,16,14,10,2,4};
D seed(int k){
 D a;for(int x:L)a.push_back(x/2);
 for(int i=0;i<2*k;i++)a.push_back(4);
 for(int i=22;i>=0;i--)a.push_back(L[i]-L[i]/2);
 return a;
}
D step(const D &a){
 int n=a.size(),carry=0;D z;z.reserve(n+1);
 for(int i=0;i<n;i++){int v=a[i]+a[n-1-i]+carry;z.push_back(v%10);carry=v/10;}
 if(carry)z.push_back(carry);
 return z;
}
int width(const D &a,int x){
 int l=(int(a.size())-1)/2,r=a.size()/2;
 while(l>=0&&r<(int)a.size()&&a[l]+a[r]==x){--l;++r;}
 return r-l-1;
}
uint64_t hash_lsd(const D &a){
 uint64_t h=14695981039346656037ULL;
 for(int x:a){h^=x;h*=1099511628211ULL;}
 return h;
}
int main(int argc,char**argv){
 int k=argc>1?atoi(argv[1]):22000,T=argc>2?atoi(argv[2]):20000;
 D a=seed(k);int pal=0,bad=-1,minW=100000,maxGain=-100000;long long gam=0;
 for(int t=0;t<=T;t++){
  int w=width(a,PH[t%6]);minW=min(minW,w);maxGain=max(maxGain,w-2*k);
  if(w<1 && bad<0)bad=t;
  bool ispal=true,odd=false;
  for(int i=0,n=a.size();i<n/2;i++){
   if(a[i]!=a[n-1-i])ispal=false;
   if((a[i]+a[n-1-i])%2)odd=true;
  }
  pal+=ispal;
  if(t==0||t<=12||t==18||t==24||t==30||t==36||
     t==100||t==1000||t==5000||t==10000||t==15000||t==20000)
    cout<<"t="<<t<<" digits="<<a.size()<<" width="<<w<<" gain="<<w-2*k
        <<" odd="<<odd<<" pal="<<ispal<<" overflow="<<gam
        <<" fnv="<<hex<<hash_lsd(a)<<dec<<"\n";
  if(t<T){D z=step(a);gam+=z.size()-a.size();a.swap(z);}
 }
 cout<<"TOTAL "<<T<<" pal="<<pal<<" firstShapeFailure="<<bad
     <<" minCentral="<<minW<<" maxGain="<<maxGain<<" gammas="<<gam<<"\n";
 return (pal||bad>=0)?1:0;
}
