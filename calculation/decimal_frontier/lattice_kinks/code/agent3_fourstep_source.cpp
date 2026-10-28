// Exact four-step midpoint-source cancellation and finite sharpness control.
// PAPER PROOF: reports/Agent3FourStepSource.md. No decimal certificate.
// Build: c++ -O3 -std=c++17 agent3_fourstep_source.cpp -o /tmp/agent3_fourstep
// Run: /tmp/agent3_fourstep ../data/lat2.txt /tmp/agent3_fourstep_state
#include <bits/stdc++.h>
using namespace std;
using ll=long long;
static int mod99(ll x){x%=99;return x<0?int(x+99):int(x);}
static int weight(int i){return i&1?10:1;} // 10^i mod 99
struct Lat{
 int p,nb,m,b;vector<int> g;vector<vector<int>> W,cup,B;
 explicit Lat(const string&path){
  ifstream f(path);if(!(f>>p>>nb>>m>>b))throw runtime_error("missing lattice data");
  if(p!=8||nb!=11||m!=48||b!=10)throw runtime_error("unexpected lattice header");
  g.resize(p);for(int &x:g)f>>x;
  W.assign(p,vector<int>(m));cup.assign(p,vector<int>(m));B.assign(p,vector<int>(nb));
  for(auto &v:W)for(int &x:v)f>>x;
  for(auto &v:cup)for(int &x:v)f>>x;
  for(auto &v:B)for(int &x:v)f>>x;
  if(!f)throw runtime_error("incomplete lattice data");
 }
 int cell(int t,int i)const{return i<nb?B[t%p][i]:W[t%p][(i-nb)%m];}
};
static void enumerate(const Lat&lat,int o,const string&stateDir){
 const int w=5,n=400+o,h=(n+1)/2;
 vector<int> low(h);for(int i=0;i<h;i++)low[i]=lat.cell(0,i);
 ll total=1;for(int i=0;i<w;i++)total*=((i==w-1&&(n&1))?10:19);
 ll start=0;bitset<99> seen;
 string ck=stateDir.empty()?"":stateDir+"/o"+to_string(o)+"_w5.state";
 if(!ck.empty()){
  ifstream in(ck);string bits;ll pos;
  if(in>>pos>>bits&&bits.size()==99&&pos>=0&&pos<=total){
   start=pos;for(int i=0;i<99;i++)seen[i]=bits[i]=='1';
  }
 }
 auto checkpoint=[&](ll pos){
  if(ck.empty())return;
  ofstream out(ck+".tmp");out<<pos<<" ";
  for(int i=0;i<99;i++)out<<(seen[i]?'1':'0');out<<"\n";
  out.close();if(rename((ck+".tmp").c_str(),ck.c_str()))throw runtime_error("checkpoint rename");
 };
 vector<int>P,O,C,P2;P.reserve(n+5);O.reserve(n+5);C.reserve(n+5);P2.reserve(n+5);
 for(ll index=start;index<total;index++){
  ll x=index;
  for(int i=0;i<w;i++){
   int dom=(i==w-1&&(n&1))?10:19;
   int v=int(x%dom);x/=dom;
   low[h-w+i]=(i==w-1&&(n&1))?2*v:v;
  }
  P.assign(low.begin(),low.end());
  for(int i=h-1-(n&1);i>=0;i--)P.push_back(low[i]);
  if((int)P.size()!=n)throw runtime_error("bad reflection");
  int Z[4];
  for(int t=0;t<4;t++){
   int len=(int)P.size(),hh=(len+1)/2,R=hh-1;
   C.clear();C.push_back(0);O.clear();
   for(int v:P){int s=v+C.back();O.push_back(s%10);C.push_back(s/10);}
   int g=C.back();if(g!=lat.g[t])throw runtime_error("overflow control failed");
   if(g)O.push_back(1);
   int q=weight(R);
   if(!(len&1)&&!g)Z[t]=mod99(-9LL*q*C[hh]);
   else if((len&1)&&!g)Z[t]=mod99(1LL*q*(C[R]-10*C[hh]));
   else if(!(len&1)&&g)Z[t]=mod99(10LL*q*O[hh]);
   else Z[t]=mod99(1LL*q*(-10*P[R]-9*C[hh]));
   P2.resize(O.size());for(size_t i=0;i<O.size();i++)P2[i]=O[i]+O[O.size()-1-i];
   P.swap(P2);
  }
  int source=mod99(22LL*(2*Z[0]+Z[1])+2*Z[2]+Z[3]);
  if(!(o&1)&&source%9)throw runtime_error("even-start mod-9 theorem contradicted");
  seen[source]=1;
  if((index+1)%100000==0)checkpoint(index+1);
 }
 checkpoint(total);
 if(!(o&1)){
  if(seen.count()!=11)throw runtime_error("even-start sharpness failed");
  for(int i=0;i<99;i++)if(seen[i]!=(i%9==0))throw runtime_error("wrong even-start residues");
 }else if(seen.count()!=90)throw runtime_error("odd-start control failed");
 cout<<"PASS o="<<o<<" w=5 assignments="<<total<<" four-step sources="<<seen.count()<<"\n";
}
int main(int argc,char**argv){
 if(argc<2||argc>3){cerr<<"usage: agent3_fourstep lat2.txt [checkpoint_dir]\n";return 2;}
 try{
  Lat lat(argv[1]);string dir=argc==3?argv[2]:"";
  if(!dir.empty())filesystem::create_directories(dir);
  for(int o=0;o<4;o++)enumerate(lat,o,dir);
  cout<<"ALL CHECKS PASSED: physical 4-step source control (no centre return claimed)\n";
 }catch(const exception&e){cerr<<"FAIL "<<e.what()<<"\n";return 1;}
}
