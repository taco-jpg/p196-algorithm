#include <bits/stdc++.h>
using namespace std; using V=vector<uint8_t>;
static const int PATH[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const int CYC[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
V init(int half,int start,int width){V a(2*half);for(int j=0;j<half;j++) {int q=j<39?PATH[j]:CYC[(j-39)%20];if(width && j>=start && j<start+width) q=(7*j+11)%19;a[j]=min(q,9);a[2*half-1-j]=q-a[j];}return a;}
V step(const V&a){V b(a.size()+1);int c=0;for(size_t i=0;i<a.size();i++){int q=a[i]+a[a.size()-1-i]+c;b[i]=q%10;c=q/10;}if(c)b[a.size()]=c;else b.pop_back();return b;}
struct Stat{int min,max,count,nA,nB;};
Stat stat(const V &a,const V &b){int lo=INT_MAX,hi=-1,num=0;
 for(int j=0;j<int(min(a.size(),b.size())/2);j++){
  if(a[j]+a[a.size()-1-j]!=b[j]+b[b.size()-1-j]){lo=min(lo,j);hi=max(hi,j);num++;}}
 return {lo==INT_MAX?-1:lo,hi,num,int(a.size()),int(b.size())};}
int front(const V &a,const V &b){int j=0;for(;j<int(min(a.size(),b.size())/2);j++){if(a[j]+a[a.size()-1-j]!=b[j]+b[b.size()-1-j])return j;}return -1;}
int main(int argc,char **argv){int H=argc>1?atoi(argv[1]):5200,sta=argc>2?atoi(argv[2]):2000,w=argc>3?atoi(argv[3]):100,T=argc>4?atoi(argv[4]):6000;
 V a=init(H,0,0),b=init(H,sta,w),reference=init(H+6800,0,0);int collision=-1;
 cout<<"time\tmin\tmax\tcount\tcenter_front\tlength\n";
 for(int t=0;t<=T;t++){
  auto s=stat(a,b);int c=front(a,reference);if(s.nA!=s.nB){cerr<<"LENGTH_MISMATCH t="<<t<<"\n";return 3;}
  cout<<t<<"\t"<<s.min<<"\t"<<s.max<<"\t"<<s.count<<"\t"<<c<<"\t"<<s.nA<<"\n";
  if(t>=1 && collision<0 && c>=0 && s.max>=c){collision=t;cerr<<"FIRST_COLLISION t="<<t<<" pulse_inner="<<s.max<<" center_outer="<<c<<"\n";}
  if(t<T){a=step(a);b=step(b);reference=step(reference);}
 }
 cerr<<"COLLISION="<<collision<<"\n";
}
