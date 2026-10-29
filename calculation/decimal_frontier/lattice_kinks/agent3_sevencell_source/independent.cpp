// Independent seven-cell physical parity/carry rank checker.
// Uses forward-state-set DP (not overlap gluing), a different spanning tree and
// opposite GF(2) pivot order, and genuine 386-/406-digit schoolbook normalization.
#include <bits/stdc++.h>
using namespace std;using U=uint64_t;
constexpr int K=7,N=48,SPACE=1<<21,TARGET=97216,COL=97217,WORDS=(COL+63)/64;
struct State{int p,a,d;};State st[76];vector<int> adj[76];
struct Bits{U lo=0,hi=0;void add(int i){if(i<64)lo|=U(1)<<i;else hi|=U(1)<<(i-64);}bool any()const{return lo||hi;}};
vector<uint8_t> allowed(SPACE),tree(SPACE);vector<int> chord(SPACE,-1);
int sh(int x,int k,int shift){int m=(1<<(k-1))-1;return ((x>>shift)&m)|(((x>>(k+shift))&m)<<(k-1))|(((x>>(2*k+shift))&m)<<(2*(k-1)));}
int extend(int x,int k,State s){int m=(1<<k)-1;int p=x&m,a=(x>>k)&m,d=(x>>(2*k))&m;return (p|((s.p&1)<<k))|((a|(s.a<<k))<<(k+1))|((d|(s.d<<k))<<(2*k+2));}
void build(){for(int p=0;p<19;p++)for(int a=0;a<2;a++)for(int d=0;d<2;d++){int i=(p*2+a)*2+d;st[i]={p,a,d};for(int q=0;q<19;q++)for(int D=0;D<2;D++)if(d==(q+D)/10)adj[i].push_back((q*2+(p+a)/10)*2+D);}
 vector<Bits> dp(8);for(int i=0;i<76;i++)dp[(st[i].p&1)|(st[i].a<<1)|(st[i].d<<2)].add(i);
 for(int k=1;k<7;k++){vector<Bits> nxt(1<<(3*(k+1)));for(int x=0;x<(int)dp.size();x++)if(dp[x].any()){
  auto extendstates=[&](U bits,int off){while(bits){int id=off+__builtin_ctzll(bits);bits&=bits-1;for(int v:adj[id])nxt[extend(x,k,st[v])].add(v);}};
  extendstates(dp[x].lo,0);extendstates(dp[x].hi,64);
 }
 dp.swap(nxt);int cnt=0;for(auto &v:dp)cnt+=v.any();int expected[]={0,8,64,288,1312,5984,27296,124512};assert(cnt==expected[k+1]);cerr<<"INDEPENDENT DP length "<<k+1<<" masks "<<cnt<<"\n";
 }
 int edges=0;vector<vector<pair<int,int>>> graph(1<<18);vector<uint8_t> used(1<<18);
 for(int x=0;x<SPACE;x++)if(dp[x].any()){allowed[x]=1;edges++;int u=sh(x,7,0),v=sh(x,7,1);graph[u].push_back({v,x});graph[v].push_back({u,x});used[u]=used[v]=1;}
 assert(edges==124512);assert(accumulate(used.begin(),used.end(),0)==27296);
 vector<uint8_t> seen(1<<18);queue<int> Q;int first=find(used.begin(),used.end(),1)-used.begin();Q.push(first);seen[first]=1;int vertices=0;
 while(!Q.empty()){int u=Q.front();Q.pop();vertices++;for(auto [v,e]:graph[u])if(!seen[v]){seen[v]=1;tree[e]=1;Q.push(v);}}
 assert(vertices==27296);int nc=0,loops=0;for(int x=0;x<SPACE;x++)if(allowed[x]){if(!tree[x])chord[x]=nc++;loops+=(sh(x,7,0)==sh(x,7,1));}
 assert(nc==COL&&loops==6);cerr<<"INDEPENDENT graph: 124512 seven-masks, 27296 connected endpoints, 97217 chords, 6 loops\n";
}
struct Norm{vector<int> O,C;};
Norm schoolbook(const vector<int>&P){int h=P.size(),n=2*h;vector<int>D(n);Norm z;z.O.resize(n);z.C.push_back(0);
 for(int j=0;j<h;j++){assert(P[j]>=0&&P[j]<=18);int hi=min(9,P[j]);D[j]=P[j]-hi;D[n-1-j]=hi;assert(D[j]<=9&&D[n-1-j]<=9);}
 for(int j=0;j<n;j++){int v=D[j]+D[n-1-j]+z.C.back();z.O[j]=v%10;z.C.push_back(v/10);}if(z.C.back())z.O.push_back(z.C.back());return z;}
vector<int> readints(const string&p){ifstream f(p);assert(f.good());vector<int> a;int x;while(f>>x)a.push_back(x);return a;}
void rec2(const string&dir){auto W=readints(dir+"/rec2_w0.txt"),initial=W,prefix=readints(dir+"/rec2_prefix.txt");assert(W.size()==48&&prefix.size()==88);
 for(int t=0;t<8;t++){int g=1-t%2;vector<int>R(prefix.begin()+11*t,prefix.begin()+11*(t+1));for(int k=0;k<4;k++)R.insert(R.end(),W.begin(),W.end());
  auto z=schoolbook(R);int h=R.size();assert(h==203&&z.O.size()==(size_t)(406+g));vector<int>Y(48),wrong(48);
  for(int j=59;j<107;j++){Y[j-59]=z.O[j]+z.O[2*h-1-j+g];wrong[j-59]=z.O[j]+z.O[2*h-1-j+(1-g)];}
  assert(Y!=wrong);W=Y;
 }assert(W==initial);cerr<<"INDEPENDENT 8 genuine 406-digit rec2 phase controls PASS\n";}
vector<U> histogram(const array<uint8_t,N>&P){vector<int>R;R.reserve(193);R.push_back(1);for(int t=0;t<4;t++)for(int j=0;j<N;j++)R.push_back(P[j]);
 auto z=schoolbook(R);assert(z.O.size()==386||z.O.size()==387);vector<U>row(WORDS);vector<uint8_t>boundary(1<<18);
 for(int j=49;j<97;j++){int x=0;for(int k=0;k<K;k++){int h=j+k;x|=(R[h]&1)<<k;x|=z.C[h]<<(K+k);x|=z.C[2*(int)R.size()-1-h]<<(2*K+k);}
  assert(allowed[x]);int c=chord[x];if(c>=0)row[c>>6]^=U(1)<<(c&63);int u=sh(x,7,0),v=sh(x,7,1);boundary[u]^=1;boundary[v]^=1;
 }assert(accumulate(boundary.begin(),boundary.end(),0)==0);return row;}
struct Rank{vector<vector<U>>piv;int r=0;uint64_t reductions=0;Rank():piv(COL){}
 bool add(vector<U> x){int block=WORDS-1;while(true){while(block>=0&&!x[block])block--;if(block<0)return false;int k=block*64+63-__builtin_clzll(x[block]);auto &p=piv[k];if(p.empty()){p.assign(x.begin(),x.begin()+block+1);r++;return true;}for(int j=0;j<=block;j++)x[j]^=p[j];reductions++;}}};
int main(int argc,char**argv){assert(argc==3);build();rec2(argv[2]);ifstream f(argv[1],ios::binary);assert(f.good());Rank rank;int count=0;
 while(true){array<uint8_t,N>P;f.read((char*)P.data(),N);auto got=f.gcount();if(got==0)break;assert(got==N);for(auto v:P)assert(v<=18);auto row=histogram(P);if(!rank.add(move(row))){cerr<<"Dependent row "<<count<<"\n";abort();}count++;
  if(count%8192==0)cerr<<"INDEPENDENT schoolbook pivot "<<count<<"\n";
 }assert(count==TARGET&&rank.r==TARGET);cerr<<"INDEPENDENT PASS 97216 independent physical 48-cycles, 386-digit normalization, 7-cell rank 97216\n";}
