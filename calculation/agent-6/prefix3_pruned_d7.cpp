// Agent 6, T1: sound necessary product graph for decimal A120 cycles.
// Full center C (length <= D), padded first R coefficients of exterior B.
// Compile: c++ -O3 -std=c++17 -o a6 prefix3_center.cpp
// Run: ./a6 3 7   (D<=7,R<=3, first peel the center graph)
#include <algorithm>
#include <unordered_map>
#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <vector>
using namespace std;
using U=uint32_t;using Wide=uint64_t;
struct Center{int n,e;array<int,8>a;};
struct Arc{U to;int g;};
int R,D;
vector<Center> centers;
vector<vector<Arc>> ce,pe;
U pow19[5],off[9];
U center_key(int n,const array<int,8>&a){U v=off[n],p=1;for(int i=0;i<(n+1)/2;i++){v+=a[i]*p;p*=19;}return v;}
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
   const auto&c=centers[i];array<int,8>d{};int carry=c.e;
   for(int j=0;j<c.n;j++){int q=c.a[j]+carry;d[j]=q%10;carry=q/10;}
   for(int g=0;g<2;g++){
     const int L=c.n+g;array<int,8>raw{};
     if(!g)for(int j=0;j<L;j++)raw[j]=d[j]+d[L-1-j];
     else{int y=9*c.e;raw[0]=raw[L-1]=d[0]+y;
       for(int j=1;j<L-1;j++)raw[j]=d[j]+d[c.n-j];}
     for(int v=0;2*v<L;v++){
       int n=L-2*v;
       if(n<=D){array<int,8>a{};for(int k=0;k<n;k++)a[k]=raw[v+k];
         U to=index[center_key(n,a)];if(to!=numeric_limits<U>::max())ce[i].push_back({to,g});}
       if(L-2*v<2||raw[v]!=9||raw[L-v-1]!=9)break;
     }
   }
 }
}
void prune_center(){
    // A product cycle projects to a center-only cycle; peeling the latter
    // cannot delete any center visited by a product cycle.
    const U old=centers.size();vector<U>indeg(old),q;q.reserve(old);
    for(const auto& row:ce)for(const auto& a:row)indeg[a.to]++;
    for(U i=0;i<old;i++)if(indeg[i]==0)q.push_back(i);
    for(size_t i=0;i<q.size();i++)for(const auto& a:ce[q[i]])
        if(--indeg[a.to]==0)q.push_back(a.to);
    const U DEAD=UINT32_MAX;vector<U>rel(old,DEAD);U count=0;
    for(U i=0;i<old;i++)if(indeg[i])rel[i]=count++;
    vector<Center> compact(count);vector<vector<Arc>> c2(count);
    for(U i=0;i<old;i++)if(rel[i]!=DEAD){
        U k=rel[i];compact[k]=centers[i];
        for(const auto& a:ce[i])if(rel[a.to]!=DEAD)c2[k].push_back({rel[a.to],a.g});
    }
    centers.swap(compact);ce.swap(c2);
    cerr<<"center_prune original="<<old<<" removed="<<q.size()
        <<" survivor="<<centers.size()<<"\n";
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
 if(argc!=3)throw runtime_error("usage: a6 <prefix=1..3> <center=1..7>");
 R=stoi(argv[1]);D=stoi(argv[2]);if(R<1||R>3||D<1||D>7)throw runtime_error("unsupported bound");
 make_center();prune_center();make_prefix();
 Wide n=Wide(centers.size())*pe.size();
 if(n>100000000ULL)throw runtime_error("UNDECIDED: state budget");
 vector<U>deg(n),q;q.reserve(n);Wide arcs=0;
 for(U s=0;s<n;s++)successors(s,[&](U t){++deg[t];++arcs;});
 for(U s=0;s<n;s++)if(deg[s]==0)q.push_back(s);
 for(size_t k=0;k<q.size();k++)successors(q[k],[&](U t){if(--deg[t]==0)q.push_back(t);});
 cout<<"R="<<R<<" D="<<D<<" P="<<pe.size()<<" C="<<centers.size()
     <<" states="<<n<<" edges="<<arcs<<" removed="<<q.size()
     <<" residual="<<n-q.size()<<" status="<<(n==q.size()?"ACYCLIC":"CYCLIC_CORE")<<'\n';
 if(q.size()<n){
   const U nc=centers.size(),np=pe.size();
   vector<array<vector<U>,2>> pin(np),cin(nc);
   for(U p=0;p<np;p++)for(const auto&a:pe[p])pin[a.to][a.g].push_back(p);
   for(U c=0;c<nc;c++)for(const auto&a:ce[c])cin[a.to][a.g].push_back(c);
   U state=0;while(state<n && deg[state]==0)state++;
   unordered_map<U,size_t> seen;vector<U> backward;
   while(!seen.count(state)){
     seen[state]=backward.size();backward.push_back(state);
     U p=state/nc,c=state%nc;bool found=false;
     for(int g=0;g<2&&!found;g++)for(U pp:pin[p][g]){
       for(U cc:cin[c][g]){
         U prev=pp*nc+cc;
         if(deg[prev]){state=prev;found=true;break;}
       }
       if(found)break;
     }
     if(!found)throw runtime_error("Kahn residual lacks predecessor");
   }
   size_t start=seen[state];
   vector<U>cyc(backward.begin()+start,backward.end());
   reverse(cyc.begin(),cyc.end());
   int gs=0,vs=0,maxC=0;string gw,ew;
   for(size_t i=0;i<cyc.size();i++){
     U x=cyc[i],y=cyc[(i+1)%cyc.size()];U p=x/nc,c=x%nc,p2=y/nc,c2=y%nc;
     int g=-1;
     for(const auto&px:pe[p])if(px.to==p2){
       for(const auto&cx:ce[c])if(cx.to==c2&&cx.g==px.g){g=px.g;break;}
       if(g!=-1)break;
     }
     if(g<0)throw runtime_error("cycle witness edge replay failed");
     int v=(centers[c].n+g-centers[c2].n)/2;
     if(v<0||centers[c].n+g-centers[c2].n!=2*v)throw runtime_error("bad center trim");
     gs+=g;vs+=v;maxC=max(maxC,centers[c].n);gw+=char('0'+g);ew+=char('0'+centers[c].e);
   }
   cout<<"PROJECTED_ONLY_WITNESS period="<<cyc.size()<<" sumG="<<gs
       <<" sumV="<<vs<<" maxC="<<maxC<<" g="<<gw<<" e="<<ew<<"\n";
   for(size_t i=0;i<cyc.size()&&i<100;i++){
     U x=cyc[i],p=x/nc,c=x%nc;const auto&v=centers[c];
     U j=p;int aa=j%18+1;j/=18;
     cout<<"t="<<i<<" Bprefix=["<<aa;
     for(int k=1;k<R;k++){cout<<","<<j%19;j/=19;}
     cout<<"] C=[";
     for(int k=0;k<v.n;k++)cout<<(k?",":"")<<v.a[k];
     cout<<"] e="<<v.e<<"\n";
   }
 }
 return 0;
 }catch(const bad_alloc&){cerr<<"UNDECIDED: allocation\n";return 3;}
 catch(const exception&e){cerr<<e.what()<<'\n';return 2;}
}
