// Exact five-cell physical carry covariance rank certificate. C++17, standard library only.
// Compile: c++ -O3 -std=c++17 primary.cpp -o /tmp/agent3_fivecell_primary
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
using namespace std;
using U=uint64_t;
struct State {int p,a,d;};
constexpr int M=48, MASKS=32768, LIMIT=56576, TARGET=4672;
static U random_state=0x6a09e667f3bcc909ULL;
U random64(){
 U z=(random_state+=0x9e3779b97f4a7c15ULL);
 z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;
 z=(z^(z>>27))*0x94d049bb133111ebULL;
 return z^(z>>31);
}
struct Rank {
 int n,sz,rank=0;
 vector<vector<U>> pivot;
 explicit Rank(int n):n(n),sz((n+63)/64),pivot(n){}
 bool add(vector<U> x){
  for(int k=n-1;k>=0;k--){
   if(!((x[k>>6]>>(k&63))&1))continue;
   if(pivot[k].empty()){pivot[k]=move(x);rank++;return true;}
   for(int j=0;j<sz;j++)x[j]^=pivot[k][j];
  }
  return false;
 }
};
vector<int> readints(const string &path){ifstream f(path);assert(f.good());vector<int> v;int x;while(f>>x)v.push_back(x);return v;}
int main(int argc,char**argv){
 string dir=argc>1?argv[1]:"calculation/decimal_frontier/lattice_kinks/agent3_fivecell_covariance";
 vector<State> states;
 for(int p=0;p<19;p++)for(int a=0;a<2;a++)for(int d=0;d<2;d++)states.push_back({p,a,d});
 auto index=[](int p,int a,int d){return (p*2+a)*2+d;};
 vector<vector<int>> adj(76);
 for(int i=0;i<76;i++){
  auto [p,a,d]=states[i];
  for(int q=0;q<19;q++)for(int D=0;D<2;D++){
   int A=(p+a)/10;
   if(d==(q+D)/10)adj[i].push_back(index(q,A,D));
  }
 }
 size_t physical_edges=0;for(const auto &x:adj)physical_edges+=x.size();assert(physical_edges==1444);
 array<int,5> path{};
 vector<uint8_t> allowed(MASKS);
 vector<int> source(MASKS,-1),target(MASKS,-1);
 size_t walks=0;
 auto fourbits=[&](int start){
  int x=0;for(int k=0;k<4;k++){
   auto s=states[path[start+k]];
   x|=(s.p&1)<<k; x|=s.a<<(4+k); x|=s.d<<(8+k);
  }return x;
 };
 auto visit=[&](){
  int id=0;for(int k=0;k<5;k++){
   auto s=states[path[k]];
   id|=(s.p&1)<<k;id|=s.a<<(5+k);id|=s.d<<(10+k);
  }
  int u=fourbits(0),v=fourbits(1);
  if(allowed[id])assert(source[id]==u&&target[id]==v);
  else{allowed[id]=1;source[id]=u;target[id]=v;}
  walks++;
 };
 for(int s=0;s<76;s++){
  path[0]=s;
  for(int t:adj[s]){path[1]=t;
   for(int u:adj[t]){path[2]=u;
    for(int v:adj[u]){path[3]=v;
     for(int w:adj[v]){path[4]=w;visit();}
    }
   }
  }
 }
 assert(walks==9904396);
 vector<int> dense(MASKS,-1);
 int n=0;for(int i=0;i<MASKS;i++)if(allowed[i])dense[i]=n++;
 assert(n==5984);
 vector<vector<int>> undirected(4096);
 vector<int> used(4096);
 int loops=0;
 for(int i=0;i<MASKS;i++)if(allowed[i]){
  int u=source[i],v=target[i];used[u]=used[v]=1;
  undirected[u].push_back(v);undirected[v].push_back(u);
  if(u==v)loops++;
 }
 int vertices=accumulate(used.begin(),used.end(),0),components=0;
 vector<int> seen(4096);
 for(int i=0;i<4096;i++)if(used[i]&&!seen[i]){
  components++;vector<int> stack{i};seen[i]=1;
  while(!stack.empty()){
   int j=stack.back();stack.pop_back();
   for(int k:undirected[j])if(!seen[k]){seen[k]=1;stack.push_back(k);}
  }
 }
 assert(vertices==1312&&components==1&&loops==6);
 assert(n-vertices+components-1==TARGET);
 Rank ranks[3]={Rank(n),Rank(n),Rank(n)};
 vector<int> a(M),d(M),P(M);
 auto carries=[&](const vector<int>&X){
  int seed=-1;
  for(int s=0;s<2;s++){
   int c=s;for(int x:X)c=(x+c)/10;
   if(c==s){seed=s;break;}
  }
  assert(seed>=0);
  int c=seed;
  for(int j=0;j<M;j++){a[j]=c;c=(X[j]+c)/10;}
  seed=-1;
  for(int s=0;s<2;s++){
   int cc=s;for(int j=M-1;j>=0;j--)cc=(X[j]+cc)/10;
   if(cc==s){seed=s;break;}
  }
  assert(seed>=0);
  c=seed;
  for(int j=M-1;j>=0;j--){d[j]=c;c=(X[j]+c)/10;}
 };
 auto histogram=[&](const vector<int>&X){
  carries(X);vector<U> row((n+63)/64);
  for(int j=0;j<M;j++){
   int id=0;
   for(int k=0;k<5;k++){
    int h=(j+k)%M;
    id|=(X[h]&1)<<k;id|=a[h]<<(5+k);id|=d[h]<<(10+k);
   }
   int pos=dense[id];assert(pos>=0);
   row[pos>>6]^=U(1)<<(pos&63);
  }
  return row;
 };
 auto step=[&](const vector<int>&X,int g){
  carries(X);vector<int> Y(M);
  for(int j=0;j<M;j++){
   if(!g)Y[j]=2*X[j]+a[j]+d[j]-10*(a[(j+1)%M]+d[(j+M-1)%M]);
   else Y[j]=X[j]+X[(j+M-1)%M]+a[j]+d[(j+M-1)%M]-10*(a[(j+1)%M]+d[(j+M-2)%M]);
   assert(Y[j]>=0&&Y[j]<=18);
  }
  return Y;
 };
 int hit[3]={};U fnv=14695981039346656037ULL;
 for(int i=1;i<=LIMIT;i++){
  for(int j=0;j<M;j++)P[j]=random64()%19;
  auto row=histogram(P);
  if(ranks[0].add(move(row))&&ranks[0].rank==TARGET&&!hit[0])hit[0]=i;
  for(int g=0;g<2;g++){
   auto Y=step(P,g);
   for(int x:Y){fnv^=U(x);fnv*=1099511628211ULL;}
   auto f=histogram(Y);
   if(ranks[1+g].add(move(f))&&ranks[1+g].rank==TARGET&&!hit[1+g])hit[1+g]=i;
  }
 }
 assert(hit[0]==32700&&hit[1]==8523&&hit[2]==56576);
 assert(ranks[0].rank==TARGET&&ranks[1].rank==TARGET&&ranks[2].rank==TARGET);
 auto W0=readints(dir+"/rec2_w0.txt");assert(W0.size()==M);
 vector<int> W=W0;
 for(int t=0;t<8;t++){
  assert(*min_element(W.begin(),W.end())>=0&&*max_element(W.begin(),W.end())<=18);
  W=step(W,1-t%2);
 }
 assert(W==W0);
 cout<<"PASS: 76 states, 1444 physical carry edges, 9904396 five-state walks\n";
 cout<<"PASS: 5984 allowed five-cell patterns, 1312 connected four-cell endpoints, 6 loops\n";
 cout<<"PASS: per-phase 32768-feature cyclic-zero dimension 28096; rank 4672\n";
 cout<<"PASS: 56576 deterministic physical 48-cycles; source/g0/g1 rank4672 first at "<<hit[0]<<"/"<<hit[1]<<"/"<<hit[2]<<"\n";
 cout<<"PASS: FNV64 output-word digest "<<hex<<fnv<<dec<<"\n";
 cout<<"PASS: rec2 eight-phase p8/m48 return\n";
 cout<<"PAPER PROOF: eight-phase covariance rank37376/262144, kernel224768; no phase-coupled five-cell universal invariant\n";
}
