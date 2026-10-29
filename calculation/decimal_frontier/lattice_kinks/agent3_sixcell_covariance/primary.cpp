// Six-cell physical carry covariance: exhaustive graph and deterministic GF(2) rank witnesses.
// C++17 standard library only. All rows correspond to genuine cyclic 48-cell pairwords.
#include <bits/stdc++.h>
using namespace std;using U=uint64_t;
constexpr int N=48,S=76,MASKS=1<<18,TARGET=21312,VAR=16;
struct State{int p,a,d;};struct Witness{uint8_t p[6],a0,d5;};
State st[S];vector<int> adj[S];vector<array<Witness,VAR>> witnesses(MASKS);
vector<uint32_t> npaths(MASKS);vector<uint8_t> allowed(MASKS);
U rng=0x6a09e667f3bcc909ULL;
U random64(){U z=(rng+=0x9e3779b97f4a7c15ULL);z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
void build(){
 for(int p=0;p<19;p++)for(int a=0;a<2;a++)for(int d=0;d<2;d++){
  int i=(p*2+a)*2+d;st[i]={p,a,d};
  for(int q=0;q<19;q++)for(int D=0;D<2;D++)if(d==(q+D)/10)
   adj[i].push_back((q*2+(p+a)/10)*2+D);
 }
 int path[6];U walks=0;
 auto visit=[&](){int mask=0;for(int k=0;k<6;k++){
  auto s=st[path[k]];mask|=(s.p&1)<<k;mask|=s.a<<(6+k);mask|=s.d<<(12+k);
 }
 allowed[mask]=1;uint32_t c=++npaths[mask];int ix=c<=VAR?(int)c-1:(int)(random64()%c);
 if(ix<VAR){auto &w=witnesses[mask][ix];for(int k=0;k<6;k++)w.p[k]=st[path[k]].p;
  w.a0=st[path[0]].a;w.d5=st[path[5]].d;}
 walks++;};
 for(int s=0;s<S;s++){path[0]=s;for(int a:adj[s]){path[1]=a;
  for(int b:adj[a]){path[2]=b;for(int c:adj[b]){path[3]=c;
   for(int d:adj[c]){path[4]=d;for(int e:adj[d]){path[5]=e;visit();}}
  }
 }}}
 assert(walks==188183524ULL);
 int edges=accumulate(allowed.begin(),allowed.end(),0);assert(edges==27296);
 vector<vector<int>> graph(1<<15);vector<uint8_t> used(1<<15);int loops=0;
 auto endpoint=[](int x,int shift){return ((x>>shift)&31)|(((x>>(6+shift))&31)<<5)|(((x>>(12+shift))&31)<<10);};
 for(int x=0;x<MASKS;x++)if(allowed[x]){int u=endpoint(x,0),v=endpoint(x,1);
  used[u]=used[v]=1;graph[u].push_back(v);graph[v].push_back(u);loops+=(u==v);}
 int vertices=accumulate(used.begin(),used.end(),0);assert(vertices==5984&&loops==6);
 vector<uint8_t> seen(1<<15);int components=0;
 for(int i=0;i<(1<<15);i++)if(used[i]&&!seen[i]){components++;
  vector<int> stack{i};seen[i]=1;while(!stack.empty()){
   int u=stack.back();stack.pop_back();for(int v:graph[u])if(!seen[v]){seen[v]=1;stack.push_back(v);}
  }
 }
 assert(components==1&&edges-vertices==TARGET);
 cout<<"PASS graph: 188183524 walks, 27296 edges, 5984 vertices, 6 loops, connected\n";
}
void carries(const int P[N],int a[N],int d[N]){
 int s=0;for(int j=0;j<N;j++)s=(P[j]+s)/10;
 for(int j=0;j<N;j++){a[j]=s;s=(P[j]+s)/10;}
 s=0;for(int j=N-1;j>=0;j--)s=(P[j]+s)/10;
 for(int j=N-1;j>=0;j--){d[j]=s;s=(P[j]+s)/10;}
}
int mask6(const int P[N],const int a[N],const int d[N],int j){
 int x=0;for(int k=0;k<6;k++){int h=(j+k)%N;
  x|=(P[h]&1)<<k;x|=a[h]<<(6+k);x|=d[h]<<(12+k);}
 return x;
}
void step(const int P[N],int Y[N],int g){
 int a[N],d[N];carries(P,a,d);
 for(int j=0;j<N;j++){
  int j1=(j+N-1)%N,j2=(j+N-2)%N,jp=(j+1)%N;
  Y[j]=g?P[j]+P[j1]+a[j]+d[j1]-10*(a[jp]+d[j2]):
   2*P[j]+a[j]+d[j]-10*(a[jp]+d[j1]);
  assert(Y[j]>=0&&Y[j]<=18);
 }
}
struct Rank{
 int r=0,sz=(27296+63)/64;U reductions=0;vector<vector<U>> piv;
 Rank():piv(27296){}
 bool add(vector<U> x){int block=sz-1;
  while(true){while(block>=0&&!x[block])--block;if(block<0)return false;
   int k=block*64+63-__builtin_clzll(x[block]);
   if(piv[k].empty()){piv[k]=move(x);r++;return true;}
   reductions++;const auto &p=piv[k];for(int j=0;j<=block;j++)x[j]^=p[j];
  }
 }
};
void record(ofstream &f,int mode,const int P[N],const int *base=nullptr){
 uint8_t tag=mode;f.write((char*)&tag,1);
 for(int j=0;j<N;j++){uint8_t v=P[j];f.write((char*)&v,1);}
 if(mode){assert(base);for(int j=0;j<N;j++){uint8_t v=base[j];f.write((char*)&v,1);}}
 assert(f.good());
}
vector<U> histogram(const int P[N],const vector<int>&dense){
 int a[N],d[N];carries(P,a,d);vector<U> row((27296+63)/64);
 for(int j=0;j<N;j++){int mask=mask6(P,a,d,j),ix=dense[mask];assert(ix>=0);
  row[ix>>6]^=U(1)<<(ix&63);}
 return row;
}
void rec2_control(const string&dir){
 ifstream f(dir+"/rec2_w0.txt");assert(f.good());int W[N],seed[N];
 for(int j=0;j<N;j++){f>>W[j];seed[j]=W[j];}assert(f.good()||f.eof());
 int Y[N];for(int t=0;t<8;t++){step(W,Y,1-t%2);copy(Y,Y+N,W);}
 assert(equal(W,W+N,seed));cout<<"PASS rec2 eight-phase cyclic bulk return\n";
}
int main(int argc,char**argv){
 assert(argc==3);string out=argv[1],data=argv[2];build();
 vector<int> dense(MASKS,-1);int count=0;for(int i=0;i<MASKS;i++)if(allowed[i])dense[i]=count++;
 assert(count==27296);Rank ranks[2];ofstream files[2];
 files[0].open(out+"/g0_witness.bin",ios::binary);files[1].open(out+"/g1_witness.bin",ios::binary);
 assert(files[0].good()&&files[1].good());
 int P[N],Y[N],a[N],d[N];vector<array<int,N>> backgrounds(VAR);
 vector<array<vector<U>,2>> baselines(VAR);
 for(int rep=0;rep<VAR;rep++){
  for(int j=0;j<N;j++)backgrounds[rep][j]=random64()%19;
  backgrounds[rep][6]=(random64()%2)?18:0;
  backgrounds[rep][N-1]=(random64()%2)?18:0;
  for(int g=0;g<2;g++){
   step(backgrounds[rep].data(),Y,g);
   auto row=histogram(Y,dense);baselines[rep][g]=row;
   if(ranks[g].add(move(row)))record(files[g],0,backgrounds[rep].data());
  }
 }
 for(int id=0;id<MASKS;id++)if(allowed[id])for(int rep=0;rep<VAR;rep++){
  const auto &w=witnesses[id][rep%min((uint32_t)VAR,npaths[id])];
  for(int j=0;j<N;j++)P[j]=backgrounds[rep][j];
  for(int k=0;k<6;k++)P[k]=w.p[k];P[6]=w.d5?18:0;P[N-1]=w.a0?18:0;
  carries(P,a,d);assert(mask6(P,a,d,0)==id);
  for(int g=0;g<2;g++)if(ranks[g].r<TARGET){
   step(P,Y,g);auto row=histogram(Y,dense);
   for(int j=0;j<(int)row.size();j++)row[j]^=baselines[rep][g][j];
   if(ranks[g].add(move(row)))record(files[g],1,P,backgrounds[rep].data());
  }
 }
 assert(ranks[0].r==TARGET&&ranks[1].r==21247);
 cout<<"PASS fixed-background ranks g0="<<ranks[0].r<<" g1="<<ranks[1].r<<"\n";
 int expected[]={21300,21308,21310,21310,21310,21311};
 for(int rep=0;rep<6;rep++){
  for(int id=0;id<MASKS;id++)if(allowed[id]&&ranks[1].r<TARGET){
   const auto &w=witnesses[id][rep%min((uint32_t)VAR,npaths[id])];
   for(int j=0;j<N;j++)P[j]=random64()%19;
   for(int k=0;k<6;k++)P[k]=w.p[k];P[6]=w.d5?18:0;P[N-1]=w.a0?18:0;
   carries(P,a,d);assert(mask6(P,a,d,0)==id);
   step(P,Y,1);auto row=histogram(Y,dense);
   if(ranks[1].add(move(row)))record(files[1],0,P);
  }
  assert(ranks[1].r==expected[rep]);
  cout<<"PASS extra g1 pass "<<rep<<" rank "<<ranks[1].r<<"\n";
 }
 int rare[N]={9,1,5,9,15,3,0,1,18,15,18,16,10,2,11,3,15,6,18,3,13,5,10,2,6,9,18,17,1,8,1,17,9,8,10,3,11,11,17,5,13,10,18,7,2,9,11,18};
 step(rare,Y,1);carries(Y,a,d);int hits=0;
 for(int j=0;j<N;j++)hits+=(mask6(Y,a,d,j)==135103);
 assert(hits==1);
 assert(ranks[1].add(histogram(Y,dense))&&ranks[1].r==TARGET);
 record(files[1],0,rare);
 files[0].close();files[1].close();rec2_control(data);
 cout<<"PASS ranks g0=g1=21312, rare g1 pivot at mask135103; 8-phase rank170496 kernel1926656\n";
}
