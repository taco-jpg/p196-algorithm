// W01: independent digit-vector construction of a base-10 two-pulse interaction
// starting from N13's rooted period-8 / period-20 lattice, extended across 20k steps.
#include <bits/stdc++.h>
using namespace std; using V=vector<uint8_t>;
static const int ROOT[39]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const int BULK[20]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
V seed(int h,int flags,int x=6000,int y=8000){V a(2*h);for(int j=0;j<h;j++){
 int q=j<39?ROOT[j]:BULK[(j-39)%20];
 if((flags&1) && j>=x && j<x+50)q=(7*j+11)%19;
 if((flags&2) && j>=y && j<y+50)q=(3*(j-y)+10)%19;
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
int main(int argc,char**argv){int y=argc>1?atoi(argv[1]):8000,T=argc>2?atoi(argv[2]):4800;
 array<V,4>v;for(int k=0;k<4;k++)v[k]=seed(12000,k,6000,y);const string alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
 cout<<"t,front,low,high\n";for(int t=0;t<=T;t++){
 int n=v[0].size()/2,lo=-1;
 // Palindromicity witness and synchronized output lengths for every true integer.
 for(int k=0;k<4;k++){
   if(v[k].size()!=v[0].size()){cerr<<"LENGTH_MISMATCH t="<<t;return 3;}
   bool odd=false;for(int j=0;j<39;j++)if(pairval(v[k],j)%2){odd=true;break;}
   if(!odd){cerr<<"MISSING_ODD_WITNESS t="<<t<<" seed="<<k;return 4;}
 }
 for(int j=0;j<n;j++){
  int z=pairval(v[3],j)-pairval(v[2],j)-pairval(v[1],j)+pairval(v[0],j);
  if(z){lo=j;break;}
 }
 if(t>=1750&&t<=T){string low,high;for(int r=-20;r<=40;r++){
   int j=lo+r;if(j<0||lo<0||j>=n){low+='?';high+='?';continue;}
   int a=(int)v[3][j]-(int)v[2][j]-(int)v[1][j]+(int)v[0][j];
   int b=(int)v[3][v[3].size()-1-j]-(int)v[2][v[2].size()-1-j]-(int)v[1][v[1].size()-1-j]+(int)v[0][v[0].size()-1-j];
   if(a+18<0||a+18>36||b+18<0||b+18>36){cerr<<"RANGE_ERROR";return 2;}
   low+=alphabet[a+18];high+=alphabet[b+18];
 }
 cout<<t<<","<<lo<<","<<low<<","<<high<<"\n";
 }
 if(t<T)for(auto &z:v)step(z);
 }
}