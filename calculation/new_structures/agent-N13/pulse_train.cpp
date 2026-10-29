#include <bits/stdc++.h>
using namespace std;using V=vector<uint8_t>;
static const int PATH[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const int CYC[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
V seed(int H,bool patch1,bool patch2){V a(2*H);for(int j=0;j<H;j++){
 int q=j<39?PATH[j]:CYC[(j-39)%20];
 if(patch1 && j>=1800 && j<1850)q=(7*j+11)%19;
 if(patch2 && j>=2600 && j<2650)q=(3*j+7)%19;
 a[j]=min(q,9);a[2*H-1-j]=q-a[j];
 }return a;}
V step(const V&a){V b(a.size()+1);int c=0;for(size_t i=0;i<a.size();i++){int q=a[i]+a[a.size()-1-i]+c;b[i]=q%10;c=q/10;}if(c)b[a.size()]=c;else b.pop_back();return b;}
struct D {int lo,hi,cnt;};
D compare(const V&a,const V&b){int lo=-1,hi=-1,cnt=0;for(size_t i=0;i<min(a.size(),b.size())/2;i++){
 int x=a[i]+a[a.size()-1-i],y=b[i]+b[b.size()-1-i];if(x!=y){if(lo<0)lo=i;hi=i;cnt++;}}return {lo,hi,cnt};}
int main(int argc,char**argv){int T=argc>1?atoi(argv[1]):4000;
 V a=seed(5200,false,false),b=seed(5200,true,false),c=seed(5200,false,true),d=seed(5200,true,true);
 int firstOverlap=-1, firstNonlinear=-1, firstUnexpected=-1;
 cout<<"time\tlo1\thi1\tlo2\thi2\toverlap\tnonlinear\tunexpected\tumin\tumax\talllen\n";
 for(int t=0;t<=T;t++){
  if(a.size()!=b.size()||a.size()!=c.size()||a.size()!=d.size()){cerr<<"LENGTH_MISMATCH t="<<t<<"\n";return 2;}
  auto x=compare(a,b),y=compare(a,c);int overlap=0,nonlinear=0,unexpected=0,umin=-1,umax=-1;size_t H=min({a.size(),b.size(),c.size(),d.size()})/2;
  for(size_t j=0;j<H;j++){
   int p=a[j]+a[a.size()-1-j],p1=b[j]+b[b.size()-1-j],p2=c[j]+c[c.size()-1-j],pb=d[j]+d[d.size()-1-j];
   bool q1=p1!=p,q2=p2!=p;
   if(q1&&q2)overlap++;
   else if(pb!=(q1?p1:q2?p2:p))nonlinear++;
   if(!q1 && !q2 && pb!=p){unexpected++; if(umin<0)umin=j;umax=j;}
  }
  if(firstOverlap<0 && overlap>0)firstOverlap=t;
  if(firstNonlinear<0 && nonlinear>0)firstNonlinear=t;
  if(firstUnexpected<0 && unexpected>0)firstUnexpected=t;
  cout<<t<<"\t"<<x.lo<<"\t"<<x.hi<<"\t"<<y.lo<<"\t"<<y.hi<<"\t"<<overlap<<"\t"<<nonlinear<<"\t"<<unexpected<<"\t"<<umin<<"\t"<<umax<<"\t"<<a.size()<<"\n";
  if(t<T){a=step(a);b=step(b);c=step(c);d=step(d);}
 }
 cerr<<"first_overlap="<<firstOverlap<<" first_nonlinear="<<firstNonlinear<<" first_unexpected="<<firstUnexpected<<"\n";
}
