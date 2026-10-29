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
constexpr int M=48, LIMIT=56576, TARGET=4672;
static U rng=0x6a09e667f3bcc909ULL;
U random64(){
 rng+=0x9e3779b97f4a7c15ULL;
 U z=rng;
 z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;
 z=(z^(z>>27))*0x94d049bb133111ebULL;
 return z^(z>>31);
}
struct Rank {
 int sz,rank=0,n;
 vector<vector<U>> piv;
 explicit Rank(int n):sz((n+63)/64),n(n),piv(n){}
 bool add(vector<U> row){
  while(true){
   int block=0;while(block<sz&&!row[block])block++;
   if(block==sz)return false;
   int bit=block*64+__builtin_ctzll(row[block]);
   assert(bit<n);
   if(piv[bit].empty()){piv[bit]=move(row);rank++;return true;}
   for(int k=block;k<sz;k++)row[k]^=piv[bit][k];
  }
 }
};
struct Normalized{vector<int> D,O,C;};
Normalized schoolbook(const vector<int>&P){
 int h=P.size(),n=2*h;
 Normalized x;x.D.resize(n);x.O.resize(n);x.C.reserve(n+1);x.C.push_back(0);
 for(int j=0;j<h;j++){
  int high=min(9,P[j]);x.D[j]=P[j]-high;x.D[n-1-j]=high;
 }
 for(int j=0;j<n;j++){
  int value=x.D[j]+x.D[n-1-j]+x.C.back();
  x.O[j]=value%10;x.C.push_back(value/10);
 }
 if(x.C.back())x.O.push_back(x.C.back());
 return x;
}
vector<int> readints(const string &p){ifstream f(p);assert(f.good());vector<int> v;int x;while(f>>x)v.push_back(x);return v;}
int main(int argc,char**argv){
 string dir=argc>1?argv[1]:"calculation/decimal_frontier/lattice_kinks/agent3_fivecell_covariance";
 vector<uint8_t> four(4096);
 for(int p=0;p<19;p++)for(int q=0;q<19;q++)for(int r=0;r<19;r++)for(int s=0;s<19;s++)for(int a=0;a<2;a++)for(int high=0;high<2;high++){
  int A=(p+a)/10,B=(q+A)/10,C=(r+B)/10;
  int E=(s+high)/10,D=(r+E)/10,d=(q+D)/10;
  int mask=(p&1)|((q&1)<<1)|((r&1)<<2)|((s&1)<<3)
   |(a<<4)|(A<<5)|(B<<6)|(C<<7)|(d<<8)|(D<<9)|(E<<10)|(high<<11);
  four[mask]=1;
 }
 assert(accumulate(four.begin(),four.end(),0)==1312);
 vector<int> dense(32768,-1);
 vector<vector<int>> adj(4096);
 int edges=0,loops=0;
 for(int x=0;x<32768;x++){
  int p=x&31,a=(x>>5)&31,d=(x>>10)&31;
  int u=(p&15)|((a&15)<<4)|((d&15)<<8);
  int v=((p>>1)&15)|(((a>>1)&15)<<4)|(((d>>1)&15)<<8);
  if(four[u]&&four[v]){
   dense[x]=edges++;adj[u].push_back(v);adj[v].push_back(u);loops+=(u==v);
  }
 }
 assert(edges==5984&&loops==6);
 vector<int> seen(4096);int components=0;
 for(int i=0;i<4096;i++)if(four[i]&&!seen[i]){
  components++;vector<int> stack{i};seen[i]=1;
  while(!stack.empty()){
   int u=stack.back();stack.pop_back();
   for(int v:adj[u])if(!seen[v]){seen[v]=1;stack.push_back(v);}
  }
 }
 assert(components==1&&edges-1312==TARGET);
 auto histogram=[&](const vector<int>&P){
  vector<int> R;R.reserve(4*M);
  for(int k=0;k<4;k++)R.insert(R.end(),P.begin(),P.end());
  auto z=schoolbook(R);
  vector<U> row((edges+63)/64);
  for(int j=48;j<96;j++){
   int mask=0;
   for(int k=0;k<5;k++){
    int h=j+k;
    mask|=(R[h]&1)<<k;
    mask|=z.C[h]<<(5+k);
    mask|=z.C[2*(int)R.size()-1-h]<<(10+k);
   }
   int id=dense[mask];assert(id>=0);
   row[id>>6]^=U(1)<<(id&63);
  }
  return row;
 };
 auto physical_step=[&](const vector<int>&P,int g){
  vector<int> R;R.reserve(1+4*M);R.push_back(g?18:1);
  for(int k=0;k<4;k++)R.insert(R.end(),P.begin(),P.end());
  auto z=schoolbook(R);int h=R.size();
  assert(z.D.back()>0&&(int)z.O.size()==2*h+g);
  vector<int> out(M);
  for(int j=49;j<97;j++){
   out[j-49]=z.O[j]+z.O[2*h-1-j+g];
   assert(out[j-49]>=0&&out[j-49]<=18);
  }
  return out;
 };
 Rank piv[3]={Rank(edges),Rank(edges),Rank(edges)};
 int hits[3]={};U fnv=14695981039346656037ULL;
 vector<int>P(M);
 for(int i=1;i<=LIMIT;i++){
  for(int j=0;j<M;j++)P[j]=random64()%19;
  if(piv[0].add(histogram(P))&&piv[0].rank==TARGET&&!hits[0])hits[0]=i;
  for(int g=0;g<2;g++){
   auto Y=physical_step(P,g);
   for(int x:Y){fnv^=U(x);fnv*=1099511628211ULL;}
   if(piv[g+1].add(histogram(Y))&&piv[g+1].rank==TARGET&&!hits[g+1])hits[g+1]=i;
  }
 }
 assert(hits[0]==32700&&hits[1]==8523&&hits[2]==56576);
 assert(piv[0].rank==TARGET&&piv[1].rank==TARGET&&piv[2].rank==TARGET);
 assert(fnv==0x567a7f76b4b8de3fULL);
 vector<int> W=readints(dir+"/rec2_w0.txt");assert(W.size()==48);
 vector<int> prefixes=readints(dir+"/rec2_prefix.txt");assert(prefixes.size()==88);
 for(int t=0;t<8;t++){
  int g=1-t%2;
  vector<int> R(prefixes.begin()+11*t,prefixes.begin()+11*(t+1));
  for(int k=0;k<4;k++)R.insert(R.end(),W.begin(),W.end());
  auto z=schoolbook(R);int h=R.size();
  assert(z.D.back()>0&&z.D.size()==406&&z.O.size()==406u+g);
  vector<int> right,wrong;
  for(int j=59;j<155;j++)right.push_back(z.O[j]+z.O[2*h-1-j+g]);
  for(int j=59;j<107;j++)wrong.push_back(z.O[j]+z.O[2*h-1-j+(1-g)]);
  assert(equal(right.begin(),right.begin()+48,right.begin()+48));
  assert(!equal(wrong.begin(),wrong.end(),right.begin()));
  W.assign(right.begin(),right.begin()+48);
 }
 assert(W==readints(dir+"/rec2_w0.txt"));
 cout<<"INDEPENDENT PASS: 1312 four-cell endpoints, 5984 five-cell patterns, connected graph and 6 loops\n";
 cout<<"INDEPENDENT PASS: 384-digit source and 386/387-digit normalized g0/g1 image ranks all 4672\n";
 cout<<"INDEPENDENT PASS: rank first-hit 32700/8523/56576; FNV64 "<<hex<<fnv<<dec<<"\n";
 cout<<"INDEPENDENT PASS: eight 406-digit rec2 phase controls and wrong-overflow negatives\n";
 cout<<"PAPER PROOF: five-cell 8-phase covariance rank37376/262144, kernel224768\n";
}
