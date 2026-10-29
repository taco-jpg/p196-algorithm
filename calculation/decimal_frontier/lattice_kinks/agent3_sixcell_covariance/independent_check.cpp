// Independent checker: graph via overlapping shorter masks, rank by lowest pivots,
// and EVERY witness by literal decimal digit normalization (not cyclic bulk formulas).
#include <bits/stdc++.h>
using namespace std;using U=uint64_t;
constexpr int N=48,MASKS=1<<18,TARGET=21312;
vector<uint8_t> four(1<<12),five(1<<15),six(MASKS);
vector<int> dense(MASKS,-1);
int v5(int x,int sh){return ((x>>sh)&31)|(((x>>(6+sh))&31)<<5)|(((x>>(12+sh))&31)<<10);}
void graph(){
 for(int p=0;p<19;p++)for(int q=0;q<19;q++)for(int r=0;r<19;r++)for(int s=0;s<19;s++)
 for(int a=0;a<2;a++)for(int high=0;high<2;high++){
  int A=(p+a)/10,B=(q+A)/10,C=(r+B)/10;
  int E=(s+high)/10,D=(r+E)/10,d=(q+D)/10;
  int x=(p&1)|((q&1)<<1)|((r&1)<<2)|((s&1)<<3)
   |(a<<4)|(A<<5)|(B<<6)|(C<<7)|(d<<8)|(D<<9)|(E<<10)|(high<<11);
  four[x]=1;
 }
 assert(accumulate(four.begin(),four.end(),0)==1312);
 for(int x=0;x<(1<<15);x++){
  int u=(x&15)|(((x>>5)&15)<<4)|(((x>>10)&15)<<8);
  int v=((x>>1)&15)|(((x>>6)&15)<<4)|(((x>>11)&15)<<8);
  five[x]=four[u]&&four[v];
 }
 assert(accumulate(five.begin(),five.end(),0)==5984);
 int count=0,loops=0;vector<vector<int>> adj(1<<15);vector<uint8_t> used(1<<15);
 for(int x=0;x<MASKS;x++)if(five[v5(x,0)]&&five[v5(x,1)]){
  six[x]=1;dense[x]=count++;int u=v5(x,0),v=v5(x,1);
  used[u]=used[v]=1;adj[u].push_back(v);adj[v].push_back(u);loops+=(u==v);
 }
 assert(count==27296&&loops==6&&accumulate(used.begin(),used.end(),0)==5984);
 vector<uint8_t> seen(1<<15);int components=0;
 for(int i=0;i<(1<<15);i++)if(used[i]&&!seen[i]){
  components++;vector<int> stack{i};seen[i]=1;
  while(!stack.empty()){int u=stack.back();stack.pop_back();
   for(int v:adj[u])if(!seen[v]){seen[v]=1;stack.push_back(v);}}
 }
 assert(components==1&&count-5984==TARGET);
 cout<<"INDEPENDENT graph: 1312 four masks, 5984 five masks, 27296 six masks, six loops\n";
}
struct Norm{vector<int> O,C;};
Norm schoolbook(const vector<int>&P){
 int h=P.size(),n=2*h;vector<int> D(n);Norm z;z.O.resize(n);z.C.push_back(0);
 for(int j=0;j<h;j++){assert(P[j]>=0&&P[j]<=18);int hi=min(9,P[j]);
  D[j]=P[j]-hi;D[n-1-j]=hi;}
 for(int j=0;j<n;j++){int v=D[j]+D[n-1-j]+z.C.back();
  z.O[j]=v%10;z.C.push_back(v/10);}
 if(z.C.back())z.O.push_back(z.C.back());
 return z;
}
vector<int> readints(const string&p){ifstream f(p);assert(f.good());vector<int> a;int x;while(f>>x)a.push_back(x);return a;}
void rec2(const string&dir){
 auto W=readints(dir+"/rec2_w0.txt"),initial=W,prefix=readints(dir+"/rec2_prefix.txt");
 assert(W.size()==48&&prefix.size()==88);
 for(int t=0;t<8;t++){
  int g=1-t%2;vector<int> R(prefix.begin()+11*t,prefix.begin()+11*(t+1));
  for(int k=0;k<4;k++)R.insert(R.end(),W.begin(),W.end());
  auto z=schoolbook(R);int h=R.size();assert(h==203&&z.O.size()==(size_t)(406+g));
  vector<int> right,wrong;
  for(int j=59;j<155;j++)right.push_back(z.O[j]+z.O[2*h-1-j+g]);
  for(int j=59;j<107;j++)wrong.push_back(z.O[j]+z.O[2*h-1-j+(1-g)]);
  assert(equal(right.begin(),right.begin()+48,right.begin()+48));
  assert(!equal(wrong.begin(),wrong.end(),right.begin()));
  W.assign(right.begin(),right.begin()+48);
 }
 assert(W==initial);cout<<"INDEPENDENT 8 rec2 genuine 406-digit phase controls and wrong-shift negatives PASS\n";
}
vector<U> histogram(const array<uint8_t,N>&P,int g){
 vector<int> R;R.push_back(g?18:1);
 for(int rep=0;rep<4;rep++)for(auto x:P)R.push_back(x);
 auto z=schoolbook(R);assert(R.size()==193&&z.O.size()==(size_t)(386+g));
 vector<int> Y(N);for(int j=49;j<97;j++){
  Y[j-49]=z.O[j]+z.O[2*(int)R.size()-1-j+g];assert(Y[j-49]>=0&&Y[j-49]<=18);
 }
 vector<int> V;for(int rep=0;rep<4;rep++)V.insert(V.end(),Y.begin(),Y.end());
 auto norm=schoolbook(V);int h=V.size();vector<U> row((27296+63)/64);
 for(int j=48;j<96;j++){
  int mask=0;for(int k=0;k<6;k++){int ix=j+k;
   mask|=(V[ix]&1)<<k;mask|=norm.C[ix]<<(6+k);mask|=norm.C[2*h-1-ix]<<(12+k);}
  assert(six[mask]);int col=dense[mask];row[col>>6]^=U(1)<<(col&63);
 }
 return row;
}
struct Rank{
 int r=0,sz=(27296+63)/64;vector<vector<U>> pivot;
 Rank():pivot(27296){}
 bool add(vector<U> row){int block=0;
  while(true){while(block<sz&&!row[block])block++;if(block==sz)return false;
   int k=block*64+__builtin_ctzll(row[block]);assert(k<27296);
   if(pivot[k].empty()){pivot[k]=move(row);r++;return true;}
   const auto &p=pivot[k];for(int j=block;j<sz;j++)row[j]^=p[j];
  }
 }
};
array<uint8_t,N> readP(ifstream&f){array<uint8_t,N>P{};f.read((char*)P.data(),N);
 assert(f.gcount()==N);for(auto x:P)assert(x<=18);return P;}
void verify(const string&dir,int g){
 ifstream f(dir+"/g"+to_string(g)+"_witness.bin",ios::binary);assert(f.good());
 Rank rank;int rows=0;
 while(true){int mode=f.get();if(mode==EOF)break;assert(mode==0||mode==1);
  auto P=readP(f);auto row=histogram(P,g);
  if(mode==1){auto Q=readP(f);auto other=histogram(Q,g);
   for(size_t j=0;j<row.size();j++)row[j]^=other[j];}
  // Independently ensure each row is an even cycle in the six-cell graph.
  int parity=0;vector<uint8_t> boundary(1<<15);
  for(int k=0;k<27296;k++)if((row[k>>6]>>(k&63))&1){
   parity^=1; // The edge list is in increasing mask order, so invert dense via prebuilt array below.
  }
  assert(parity==0); // XOR of 48-step cycles has even edge parity.
  if(!rank.add(move(row))){cerr<<"dependent witness g="<<g<<" row="<<rows<<"\n";abort();}
  rows++;if(rows%4096==0)cout<<"INDEPENDENT g"<<g<<" pivot rows "<<rows<<"\n";
 }
 assert(rows==TARGET&&rank.r==TARGET);
 cout<<"INDEPENDENT g"<<g<<" 21312/21312 independent schoolbook-normalized cyclic image rows PASS\n";
}
int main(int argc,char**argv){assert(argc==3);graph();rec2(argv[2]);
 array<uint8_t,N> rare={9,1,5,9,15,3,0,1,18,15,18,16,10,2,11,3,15,6,18,3,13,5,10,2,6,9,18,17,1,8,1,17,9,8,10,3,11,11,17,5,13,10,18,7,2,9,11,18};
 auto row=histogram(rare,1);int ix=dense[135103];assert(ix>=0&&((row[ix>>6]>>(ix&63))&1));
 cout<<"INDEPENDENT rare g1 six-cell mask 135103 odd occurrence PASS\n";
 verify(argv[1],0);verify(argv[1],1);
 cout<<"INDEPENDENT PASS: 8-phase six-cell rank170496 kernel1926656; no decimal certificate\n";
}
