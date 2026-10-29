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
int main(int argc,char**argv){assert(argc==2);int passes=1;ofstream fout(argv[1],ios::binary);assert(fout.good());build();Rank R;int P[N],a[N],d[N];int accepted=0;auto start=chrono::steady_clock::now();
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
