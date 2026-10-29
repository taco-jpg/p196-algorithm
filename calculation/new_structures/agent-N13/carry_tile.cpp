#include <bits/stdc++.h>
using namespace std;
using V=vector<uint8_t>;
static const int PATH[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const int CYC[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
V init(int half,int replacement){V a(2*half);for(int j=0;j<half;j++){int q=j<39?PATH[j]:CYC[(j-39)%20];if(replacement && j>=half-replacement)q=(7*j+11)%19;a[j]=min(q,9);a[2*half-1-j]=q-a[j];}return a;}
V step(const V&a){V b(a.size()+1);int c=0;for(size_t i=0;i<a.size();i++){int q=a[i]+a[a.size()-1-i]+c;b[i]=q%10;c=q/10;}if(c)b[a.size()]=c;else b.pop_back();return b;}
V carry(const V&a){V c(a.size()+1);for(size_t i=0;i<a.size();i++){c[i+1]=(a[i]+a[a.size()-1-i]+c[i])>=10;}return c;}
int front(const V&a,const V&b){int j=0;for(;j<int(min(a.size(),b.size())/2);j++)if(a[j]+a[a.size()-1-j]!=b[j]+b[b.size()-1-j])break;return j;}
struct S {int f, len; uint8_t LA,LB,HA,HB, endLA,endLB,endHA,endHB;};
int main(int argc,char**argv){int T=argc>1?atoi(argv[1]):20000;
 V a=init(5200,0),b=init(5200,100);deque<S> q;int m[8]={0};int contrast=0;ofstream csv(argc>2?argv[2]:"carry88.csv");
 csv<<"phase,lowA,lowB,highA,highB,lowEndA,lowEndB,highEndA,highEndB\n";
 for(int t=0;t<=T;t++){
  int f=front(a,b),n=a.size();V ca=carry(a),cb=carry(b);int lo=f-100, hi=n-1-(f+74);int endlo=f+75, endhi=n-(f-100);
  S s{f,n,ca[lo],cb[lo],ca[hi],cb[hi],ca[endlo],cb[endlo],ca[endhi],cb[endhi]};
  if(t>=1000){auto p=q[q.size()-88];
    int vals[]={int(s.LA!=p.LA),int(s.LB!=p.LB),int(s.HA!=p.HA),int(s.HB!=p.HB),int(s.endLA!=p.endLA),int(s.endLB!=p.endLB),int(s.endHA!=p.endHA),int(s.endHB!=p.endHB)};
    for(int i=0;i<8;i++)m[i]+=vals[i];
    if(t<1088){csv<<(t-1000)<<","<<int(s.LA)<<","<<int(s.LB)<<","<<int(s.HA)<<","<<int(s.HB)<<","<<int(s.endLA)<<","<<int(s.endLB)<<","<<int(s.endHA)<<","<<int(s.endHB)<<"\n";if(s.HA!=s.HB)contrast++;}
  }
  q.push_back(s);if(q.size()>89)q.pop_front();
  if(t<T){a=step(a);b=step(b);}
 }
 cout<<"CARRY_EIGHT_GATES_88_PHASES high_A_B_differ_phases="<<contrast<<" comparisons="<<(T-999)<<" mismatch_counts=";for(int x:m)cout<<x<<",";cout<<"\n";
 if(T!=20000 || contrast<1)return 2;
 for(int x:m){if(x)return 1;}
 cout<<"SHEARED_88_CARRY_TILE_PASS\n";
}
