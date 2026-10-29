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
int main(int argc,char**argv){int T=argc>1?atoi(argv[1]):20000;int H=argc>2?atoi(argv[2]):12000;
 array<V,4> v;for(int k=0;k<4;k++)v[k]=seed(H,k);
 deque<Snap> queue;int firstoverlap=-1,firstnonlinear=-1,firstunexpected=-1,frontbad=-1,windowbad=-1,odd_fail=-1;
 long long checks=0,twowindow=0,shape_checks=0;array<array<int,59>,8> tile{};int shape_fail=-1,min_untouched=INT_MAX;uint64_t checksum=1469598103934665603ULL;
 cout<<"t,front_B,front_D,front_C,right_B,right_C,overlap,nonlinear,unexpected,odd_witness,decimal_length\n";
 for(int t=0;t<=T;t++){
  int n=v[0].size();for(int k=1;k<4;k++)if((int)v[k].size()!=n){cerr<<"FAIL lengths t="<<t<<"\n";return 2;}
  int fb=first(v[0],v[1]),fc=first(v[0],v[2]),fd=first(v[0],v[3]);int rb=-1,rc=-1,ov=0,non=0,un=0,odd=-1;
  for(int j=0;j<n/2;j++){
   int a=pairval(v[0],j),b=pairval(v[1],j),c=pairval(v[2],j),d=pairval(v[3],j);
   bool x=b!=a,y=c!=a;if(x)rb=j;if(y)rc=j;
   if(x&&y)ov++;else if(d!=(x?b:y?c:a))non++;
   if(!x&&!y&&d!=a)un++;
  }
  if(t<8)for(int j=0;j<59;j++)tile[t][j]=pairval(v[0],j);
  int intact=min(fb,fc);min_untouched=min(intact,min_untouched);
  for(int j=0;j<intact;j++){int e=j<39?tile[t%8][j]:tile[t%8][39+(j-39)%20];for(int k=0;k<4;k++){shape_checks++;if(pairval(v[k],j)!=e && shape_fail<0)shape_fail=t;}}
  for(int j=0;j<39;j++)if(pairval(v[0],j)&1){odd=j;break;}
  if(odd<0 || pairval(v[1],odd)!=pairval(v[0],odd) || pairval(v[2],odd)!=pairval(v[0],odd)||pairval(v[3],odd)!=pairval(v[0],odd)){
   if(odd_fail<0)odd_fail=t;
  }
  if(t>=1000){const Snap& old=queue[queue.size()-88];
    if(fb!=old.fb-20 || fd!=old.fd-20 || n!=(int)old.v[0].size()+44){if(frontbad<0)frontbad=t;}
    if(t>=1000){bool good=matchwin(v,old,fb,old.fb);if(!good&&windowbad<0)windowbad=t;checks+=3*2*81;twowindow++;}
  }
  if(firstoverlap<0&&ov)firstoverlap=t;
  if(firstnonlinear<0&&non)firstnonlinear=t;
  if(firstunexpected<0&&un)firstunexpected=t;
  if(t%100==0 || (t>=firstoverlap&&t<firstoverlap+30))cout<<t<<","<<fb<<","<<fd<<","<<fc<<","<<rb<<","<<rc<<","<<ov<<","<<non<<","<<un<<","<<odd<<","<<n<<"\n";
  if(t==0||t==1000||t==2154||t==2161||t==8000||t==20000){uint64_t h=1469598103934665603ULL;for(int k=n-1;k>=0;k--){h^=(unsigned)(v[3][k]+'0');h*=1099511628211ULL;}cerr<<"W01_D_CHECKPOINT t="<<t<<" len="<<n<<" fnv64="<<h<<"\n";}
  checksum^=(uint64_t)fb;checksum*=1099511628211ULL;checksum^=(uint64_t)(fd+31*non+131*un);checksum*=1099511628211ULL;
  queue.push_back({v,fb,fd});if(queue.size()>89)queue.pop_front();
  if(t<T)for(auto &a:v)step(a);
 }
 cerr<<"W01_EVENTS overlap="<<firstoverlap<<" nonlinear="<<firstnonlinear<<" unexpected="<<firstunexpected<<" odd_failure="<<odd_fail<<" front_88_failure="<<frontbad<<" digit_window_88_failure="<<windowbad<<" digit_equalities="<<checks<<" window_times="<<twowindow<<" checksum="<<checksum<<" shape_fail="<<shape_fail<<" shape_checks="<<shape_checks<<" minimum_intact="<<min_untouched<<"\n";
 return odd_fail>=0 || frontbad>=0 || windowbad>=0 || shape_fail>=0;
}
