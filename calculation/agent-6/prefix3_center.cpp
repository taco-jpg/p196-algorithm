// Agent 6, T1: sound necessary product graph for decimal A120 cycles.
// Full center C (length <= D), padded first R coefficients of exterior B.
// Compile: c++ -O3 -std=c++17 -o a6 prefix3_center.cpp
// Run: ./a6 3 6   (D<=6,R<=3, resource guard <100M graph vertices)
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <vector>
using namespace std;
using U=uint32_t;using Wide=uint64_t;
struct Center{int n,e;array<int,7>a;};
struct Arc{U to;int g;};
int R,D;
vector<Center> centers;
vector<vector<Arc>> ce,pe;
U pow19[5],off[8];
U center_key(int n,const array<int,7>&a){U v=off[n],p=1;for(int i=0;i<(n+1)/2;i++){v+=a[i]*p;p*=19;}return v;}
void make_center(){
 pow19[0]=1;for(int i=1;i<5;i++)pow19[i]=pow19[i-1]*19;
 off[1]=0;for(int n=1;n<=D;n++)off[n+1]=off[n]+pow19[(n+1)/2];
 for(int n=1;n<=D;n++)for(U h=0;h<pow19[(n+1)/2];h++){
  Center c{};c.n=n;U z=h;
  for(int i=0;i<(n+1)/2;i++){c.a[i]=z%19;z/=19;}
  for(int i=0;i<n/2;i++)c.a[n-1-i]=c.a[i];
  int choice=-1;
  for(int e=0;e<2;e++){int carry=e;for(int i=0;i<n;i++)carry=(c.a[i]+carry)/10;
    if(carry==1-e){if(choice!=-1)throw runtime_error("two center inputs");choice=e;}}
  if(choice!=-1){c.e=choice;centers.push_back(c);}
 }
 vector<U> index(off[D+1],numeric_limits<U>::max());
 for(U i=0;i<centers.size();i++)index[center_key(centers[i].n,centers[i].a)]=i;
 ce.resize(centers.size());
 for(U i=0;i<centers.size();i++){
   const auto&c=centers[i];array<int,7>d{};int carry=c.e;
   for(int j=0;j<c.n;j++){int q=c.a[j]+carry;d[j]=q%10;carry=q/10;}
   for(int g=0;g<2;g++){
     const int L=c.n+g;array<int,7>raw{};
     if(!g)for(int j=0;j<L;j++)raw[j]=d[j]+d[L-1-j];
     else{int y=9*c.e;raw[0]=raw[L-1]=d[0]+y;
       for(int j=1;j<L-1;j++)raw[j]=d[j]+d[c.n-j];}
     for(int v=0;2*v<L;v++){
       int n=L-2*v;
       if(n<=D){array<int,7>a{};for(int k=0;k<n;k++)a[k]=raw[v+k];
         U to=index[center_key(n,a)];if(to!=numeric_limits<U>::max())ce[i].push_back({to,g});}
       if(L-2*v<2||raw[v]!=9||raw[L-v-1]!=9)break;
     }
   }
 }
}
void make_prefix(){
 U count=18;for(int k=1;k<R;k++)count*=19;
 pe.resize(count);
 for(U id=0;id<count;id++){
   int a[3]={9,9,9};a[0]=id%18+1;U z=id/18;
   for(int i=1;i<R;i++){a[i]=z%19;z/=19;}
   for(int carryTop=0;carryTop<2;carryTop++){
     int h[4]{};h[R]=carryTop;
     for(int i=R-1;i>=0;i--)h[i]=(a[i]+h[i+1])/10;
     int g=h[0],lo=0,nxt[3]{};
     for(int i=0;i<R;i++){
       int digit=(a[i]+lo)%10;lo=(a[i]+lo)/10;
       int rev=(g?(i==0?1:(a[i-1]+h[i])%10):(a[i]+h[i+1])%10);
       nxt[i]=digit+rev;
     }
     if(nxt[0]<1||nxt[0]>18)throw runtime_error("bad exterior head");
     U to=nxt[0]-1,mult=18;
     for(int i=1;i<R;i++){if(nxt[i]<0||nxt[i]>18)throw runtime_error("bad projected digit");
       to+=nxt[i]*mult;mult*=19;}
     bool seen=false;for(auto&edge:pe[id])if(edge.to==to&&edge.g==g)seen=true;
     if(!seen)pe[id].push_back({to,g});
   }
 }
}
template<class F>inline void successors(U s,const F&f){
 U n=centers.size(),p=s/n,c=s%n;
 for(const auto&ex:pe[p])for(const auto&mid:ce[c])if(ex.g==mid.g)f(ex.to*n+mid.to);
}
int main(int argc,char**argv){
 try{
 if(argc!=3)throw runtime_error("usage: a6 <prefix=1..3> <center=1..6>");
 R=stoi(argv[1]);D=stoi(argv[2]);if(R<1||R>3||D<1||D>6)throw runtime_error("unsupported bound");
 make_center();make_prefix();
 Wide n=Wide(centers.size())*pe.size();
 if(n>100000000ULL)throw runtime_error("UNDECIDED: state budget");
 vector<U>deg(n),q;q.reserve(n);vector<U>longest(n,0);Wide arcs=0;
 for(U s=0;s<n;s++)successors(s,[&](U t){++deg[t];++arcs;});
 for(U s=0;s<n;s++)if(deg[s]==0)q.push_back(s);
 for(size_t k=0;k<q.size();k++){U s=q[k];successors(s,[&](U t){if(longest[t]<longest[s]+1)longest[t]=longest[s]+1; if(--deg[t]==0)q.push_back(t);});}
 cout<<"R="<<R<<" D="<<D<<" P="<<pe.size()<<" C="<<centers.size()
     <<" states="<<n<<" edges="<<arcs<<" removed="<<q.size()
     <<" residual="<<n-q.size()<<" max_path_edges="<<*max_element(longest.begin(),longest.end())<<" status="<<(n==q.size()?"ACYCLIC":"CYCLIC_CORE")<<'\n';
 return 0;
 }catch(const bad_alloc&){cerr<<"UNDECIDED: allocation\n";return 3;}
 catch(const exception&e){cerr<<e.what()<<'\n';return 2;}
}
