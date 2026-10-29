// K1 rec2 seven-cell physical cyclic parity/carry source rank experiment.
// C++17; 48-cell exact physical words. Not a decimal Lychrel certificate.
#include <bits/stdc++.h>
using namespace std;
using U=uint64_t;
constexpr int N=48,K=7,SPACE=1<<21;
struct S {int p,a,d;};S states[76];vector<int> out[76];vector<int> match[8];
vector<uint8_t> allowed(SPACE);vector<int> dense(SPACE,-1),chord(SPACE,-1);vector<array<uint8_t,9>> witness(SPACE);
int parent[1<<18],dep[1<<18];
int findp(int a){while(parent[a]!=a){parent[a]=parent[parent[a]];a=parent[a];}return a;}
bool unite(int a,int b){a=findp(a);b=findp(b);if(a==b)return false;parent[b]=a;return true;}
int sh(int x,int k,int shift){int m=(1<<(k-1))-1;return ((x>>shift)&m)|(((x>>(k+shift))&m)<<(k-1))|(((x>>(2*k+shift))&m)<<(2*(k-1)));}
int getmask(const int p[],const int a[],const int d[],int j){int x=0;for(int k=0;k<K;k++){int h=(j+k)%N;x|=(p[h]&1)<<k;x|=a[h]<<(K+k);x|=d[h]<<(2*K+k);}return x;}
void carries(const int P[],int a[],int d[]){int s=0;for(int j=0;j<N;j++)s=(P[j]+s)/10;for(int j=0;j<N;j++){a[j]=s;s=(P[j]+s)/10;}s=0;for(int j=N-1;j>=0;j--)s=(P[j]+s)/10;for(int j=N-1;j>=0;j--){d[j]=s;s=(P[j]+s)/10;}}
void init(){for(int p=0;p<19;p++)for(int a=0;a<2;a++)for(int d=0;d<2;d++){int id=(p*2+a)*2+d;states[id]={p,a,d};match[(p&1)|(a<<1)|(d<<2)].push_back(id);for(int q=0;q<19;q++)for(int D=0;D<2;D++)if(d==(q+D)/10)out[id].push_back((q*2+(p+a)/10)*2+D);}}
int walk[7];bool findwalk(int mask,int k){if(k==7)return true;int sym=((mask>>k)&1)|(((mask>>(K+k))&1)<<1)|(((mask>>(2*K+k))&1)<<2);if(k==0){for(int id:match[sym]){walk[0]=id;if(findwalk(mask,1))return true;}}else{for(int id:out[walk[k-1]]){auto s=states[id];if(((s.p&1)|(s.a<<1)|(s.d<<2))==sym){walk[k]=id;if(findwalk(mask,k+1))return true;}}}return false;}
void build(){init();vector<uint8_t> four(1<<12);for(int p=0;p<19;p++)for(int q=0;q<19;q++)for(int r=0;r<19;r++)for(int z=0;z<19;z++)for(int a=0;a<2;a++)for(int h=0;h<2;h++){
 int A=(p+a)/10,B=(q+A)/10,C=(r+B)/10,E=(z+h)/10,D=(r+E)/10,d=(q+D)/10;
 int x=(p&1)|((q&1)<<1)|((r&1)<<2)|((z&1)<<3)|(a<<4)|(A<<5)|(B<<6)|(C<<7)|(d<<8)|(D<<9)|(E<<10)|(h<<11);four[x]=1;
 }assert(accumulate(four.begin(),four.end(),0)==1312);
 vector<uint8_t> five(1<<15),six(1<<18);
 for(int x=0;x<(1<<15);x++)five[x]=four[sh(x,5,0)]&&four[sh(x,5,1)];assert(accumulate(five.begin(),five.end(),0)==5984);
 for(int x=0;x<(1<<18);x++)six[x]=five[sh(x,6,0)]&&five[sh(x,6,1)];assert(accumulate(six.begin(),six.end(),0)==27296);
 int edges=0;for(int x=0;x<SPACE;x++)if(six[sh(x,7,0)]&&six[sh(x,7,1)]){allowed[x]=1;dense[x]=edges++;}
 assert(edges==124512);cerr<<"GRAPH seven edges "<<edges<<"\n";
 int cnt=0;for(int x=0;x<SPACE;x++)if(allowed[x]){if(!findwalk(x,0)){cerr<<"No physical path for "<<x<<"\n";abort();}auto &w=witness[x];for(int j=0;j<7;j++)w[j]=states[walk[j]].p;w[7]=states[walk[0]].a;w[8]=states[walk[6]].d;if(++cnt%25000==0)cerr<<"PATHS "<<cnt<<"\n";}
 for(int i=0;i<(1<<18);i++)parent[i]=i;
 int nchord=0,loops=0;for(int x=0;x<SPACE;x++)if(allowed[x]){int u=sh(x,7,0),v=sh(x,7,1);loops+=(u==v);if(!unite(u,v))chord[x]=nchord++;}
 assert(nchord==97217&&loops==6);cerr<<"GRAPH seven endpoints 27296, chords "<<nchord<<", loops "<<loops<<"\n";
}
U seed=0x6a09e667f3bcc909ULL;U random64(){U z=(seed+=0x9e3779b97f4a7c15ULL);z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
constexpr int COLS=97217,WORDS=(COLS+63)/64;
struct Rank{
 vector<vector<U>> piv;int rank=0;uint64_t reductions=0;
 Rank():piv(COLS){}
 bool add(vector<U>& row){int start=0;while(start<WORDS){while(start<WORDS&&!row[start])start++;if(start==WORDS)return false;int k=start*64+__builtin_ctzll(row[start]);auto &p=piv[k];if(p.empty()){p.assign(row.begin()+start,row.end());rank++;return true;}for(int j=start;j<WORDS;j++)row[j]^=p[j-start];reductions++;}return false;}
};
vector<U> histogram(const int P[],int *counts=nullptr){int a[N],d[N];carries(P,a,d);vector<U> row(WORDS);for(int j=0;j<N;j++){int mask=getmask(P,a,d,j);assert(allowed[mask]);int c=chord[mask];if(c>=0)row[c>>6]^=U(1)<<(c&63);if(counts)counts[j]=mask;}return row;}
void source_main(int argc,char**argv){assert(argc==2);int passes=1;ofstream fout(argv[1],ios::binary);assert(fout.good());build();Rank R;int P[N],a[N],d[N];int accepted=0;auto start=chrono::steady_clock::now();
 for(int rep=0;rep<passes&&R.rank<97216;rep++){
  for(int mask=0;mask<SPACE&&R.rank<97216;mask++)if(allowed[mask]){
   auto &w=witness[mask];for(int j=0;j<N;j++)P[j]=rep==0?0:int(random64()%19);
   for(int j=0;j<7;j++)P[j]=w[j];P[7]=w[8]?18:0;P[47]=w[7]?18:0;
   carries(P,a,d);if(getmask(P,a,d,0)!=mask){cerr<<"BAD PHYSICAL TARGET "<<mask<<"\n";abort();}
   auto row=histogram(P);if(R.add(row)){accepted++;for(int j=0;j<N;j++){uint8_t b=P[j];fout.write((char*)&b,1);}assert(fout.good());}
   if(accepted&&accepted%2048==0&&R.rank==accepted){auto sec=chrono::duration<double>(chrono::steady_clock::now()-start).count();cerr<<"RANK "<<R.rank<<" mask "<<mask<<" pass "<<rep<<" sec "<<sec<<" reductions "<<R.reductions<<"\n";}
  }
  cerr<<"PASS "<<rep<<" rank "<<R.rank<<" reductions "<<R.reductions<<"\n";
 }
 fout.close();assert(R.rank==97216);cerr<<"DONE rank "<<R.rank<<" target97216 witness bytes "<<int64_t(R.rank)*N<<"\n";
}


struct OutputEdge {int u,v,y;};
void output_step(const int P[N],int Y[N],int g){
 int a[N],d[N];carries(P,a,d);
 for(int j=0;j<N;j++){
  int jm=(j+N-1)%N,jmm=(j+N-2)%N,jp=(j+1)%N;
  Y[j]=g?P[j]+P[jm]+a[j]+d[jm]-10*(a[jp]+d[jmm]):
   2*P[j]+a[j]+d[j]-10*(a[jp]+d[jm]);
  assert(Y[j]>=0&&Y[j]<=18);
 }
}
int image_main(int argc,char**argv){
 assert(argc==4);int g=atoi(argv[1]),hub=atoi(argv[2]);assert(g==0||g==1);build();
 vector<OutputEdge> E;vector<vector<int>> from(76);
 for(int u=0;u<76;u++)for(int v:out[u]){
  auto x=states[u],z=states[v];
  int y=g?z.p+x.p+z.a+x.d-10*((z.p+z.a)/10+(x.p+x.d)/10):
   2*z.p+z.a+z.d-10*((z.p+z.a)/10+(z.p+z.d)/10);
  assert(y>=0&&y<=18);int id=E.size();E.push_back({u,v,y});from[u].push_back(id);
 }
 assert(E.size()==1444);int H=E.size()*4;
 vector<array<vector<int>,8>> bylabel(H);vector<vector<int>> forward(H),reverse(H),nodes(8);
 vector<int> label(H);
 for(int id=0;id<(int)E.size();id++)for(int a=0;a<2;a++)for(int d=0;d<2;d++){
  int u=id*4+a*2+d;label[u]=(E[id].y&1)|(a<<1)|(d<<2);nodes[label[u]].push_back(u);
 }
 for(int id=0;id<(int)E.size();id++)for(int a=0;a<2;a++)for(int d=0;d<2;d++){
  int u=id*4+a*2+d;
  for(int j:from[E[id].v])for(int D=0;D<2;D++)if(d==(E[j].y+D)/10){
   int A=(E[id].y+a)/10,v=j*4+A*2+D;
   forward[u].push_back(v);reverse[v].push_back(u);bylabel[u][label[v]].push_back(v);
  }
 }
 auto bfs=[&](const vector<vector<int>>&G){
  vector<int>dist(H,-1),parent(H,-1),q;dist[hub]=0;q.push_back(hub);
  for(int z=0;z<(int)q.size();z++)for(int v:G[q[z]])if(dist[v]<0){
   dist[v]=dist[q[z]]+1;parent[v]=q[z];q.push_back(v);
  }
  return make_pair(dist,parent);
 };
 auto [outdist,fromhub]=bfs(forward);auto [indist,tohub]=bfs(reverse);
 vector<uint8_t> good(H);int nGood=0;
 for(int u=0;u<H;u++)if(outdist[u]>=0&&indist[u]>=0){
  good[u]=1;nGood++;assert(outdist[u]+indist[u]<=41);
 }
 assert(nGood==(g?5626:3116));
 ofstream f(argv[3],ios::binary);assert(f.good());Rank R;
 vector<vector<int>>pred(K,vector<int>(H,-1)),seen(K,vector<int>(H));
 int stamp=0,found=0;
 for(int mask=0;mask<SPACE;mask++)if(allowed[mask]){
  ++stamp;int l[K];for(int i=0;i<K;i++)l[i]=((mask>>i)&1)|(((mask>>(K+i))&1)<<1)|(((mask>>(2*K+i))&1)<<2);
  vector<int>cur,nxt;for(int u:nodes[l[0]])if(good[u]){cur.push_back(u);seen[0][u]=stamp;}
  for(int i=1;i<K;i++){
   nxt.clear();for(int u:cur)for(int v:bylabel[u][l[i]])if(good[v]&&seen[i][v]!=stamp){
    seen[i][v]=stamp;pred[i][v]=u;nxt.push_back(v);
   }
   cur.swap(nxt);if(cur.empty())break;
  }
  assert(!cur.empty());array<int,K>seq;seq[K-1]=cur[0];
  for(int i=K-1;i>0;i--)seq[i-1]=pred[i][seq[i]];
  vector<int>ring(seq.begin(),seq.end());int u=seq[K-1];
  while(u!=hub){u=tohub[u];assert(u>=0);ring.push_back(u);}
  int pad=48-(int)ring.size()-max(0,outdist[seq[0]]-1);assert(pad>=0);
  for(int i=0;i<pad;i++)ring.push_back(hub);
  vector<int>suffix;u=seq[0];while(u!=hub){suffix.push_back(u);u=fromhub[u];assert(u>=0);}
  std::reverse(suffix.begin(),suffix.end());if(!suffix.empty())suffix.pop_back();
  ring.insert(ring.end(),suffix.begin(),suffix.end());assert(ring.size()==48);
  int P[N],Y[N],a[N],d[N];for(int i=0;i<N;i++)P[i]=states[E[ring[i]/4].v].p;
  output_step(P,Y,g);carries(Y,a,d);assert(getmask(Y,a,d,0)==mask);
  auto row=histogram(Y);if(R.add(row))for(int x:P){uint8_t b=x;f.write((char*)&b,1);}
  found++;
 }
 f.close();assert(found==124512&&R.rank==97216);
 cerr<<"DONE seven-cell g"<<g<<" output rank "<<R.rank<<" of 97216\n";
 return 0;
}
int main(int argc,char**argv){
 assert(argc==4);int g=atoi(argv[1]);
 if(g==2){char *args[2]={argv[0],argv[3]};source_main(2,args);return 0;}
 return image_main(argc,argv);
}
