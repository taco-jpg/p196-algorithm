// Independent glide-first arithmetic verification of parity-flipping centre alignment.
// Compile: g++ -O2 -std=c++17 calculation/decimal_frontier/lattice_kinks/code/agent14_parity_flip_independent.cpp -o /tmp/p196_agent14_independent
// Run from repository root: /tmp/p196_agent14_independent
#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <numeric>
#include <regex>
#include <sstream>
#include <string>
#include <tuple>
#include <vector>
using namespace std;
struct E {string name;vector<int> g;vector<vector<int>> w;};
vector<vector<int>> bracket(const string&s) {
 vector<vector<int>> out;regex r("\\[([0-9,]+)\\]");
 auto first=sregex_iterator(s.begin(),s.end(),r);
 for(auto i=first;i!=sregex_iterator();++i){vector<int> v;string st=(*i)[1];stringstream q(st);string item;while(getline(q,item,','))v.push_back(stoi(item));out.push_back(v);}return out;
}
vector<E> load(){
 vector<E> res;string line;
 ifstream f("calculation/decimal_frontier/lattice_formats/p8_scc.txt");assert(f.good());
 for(int k=0;getline(f,line);){
  if(line.rfind("SCC p=",0)!=0)continue;
  auto a=line.find(" g="),b=line.find(" size="),c=line.find(" cyc=");
  int p=stoi(line.substr(6,a-6));string gtxt=line.substr(a+3,b-a-3);vector<int> g;
  for(char v:gtxt)g.push_back(v-'0');
  auto cols=bracket(line.substr(c+5));int m=cols.size();assert(p==(int)g.size()&&m>0);
  vector<vector<int>> w(p,vector<int>(m));
  for(int i=0;i<m;i++){assert((int)cols[i].size()==p);for(int t=0;t<p;t++)w[t][i]=cols[i][t];}
  res.push_back({"p8-rec"+to_string(k++),g,w});
 }
 assert(res.size()==3);
 ifstream s("calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt");assert(s.good());
 int p,nB,m,b;s>>p>>nB>>m>>b;assert(b==10);vector<int>g(p);
 for(int&t:g)s>>t;
 vector<vector<int>>w(p,vector<int>(m));for(auto&row:w)for(int&v:row)s>>v;
 res.push_back({"p12-m9",g,w});
 return res;
}
int main(){
 for(const E&e:load()){
  int p=e.g.size(),m=e.w[0].size(),S=accumulate(e.g.begin(),e.g.end(),0);
  int L=p*(2*m/gcd(2*m,S));
  vector<pair<int,int>> glides;
  for(int dt=0;dt<p;dt++)for(int dx=0;dx<m;dx++){
   bool ok=true;
   for(int t=0;t<p&&ok;t++)for(int j=0;j<m;j++)
    if(e.w[t][j]+e.w[(t+dt)%p][(j+dx)%m]!=18){ok=false;break;}
   if(ok)glides.emplace_back(dt,dx);
  }
  vector<tuple<int,int,int>> sol;
  for(int parity=0;parity<2;parity++)for(int d=1;d<=L;d++){
   bool all=true;
   for(int t=0;t<p;t++){
    int G=0;for(int k=0;k<d;k++)G+=e.g[(t+k)%p];
    int shift=(G+1-parity)/2;
    if(G%2==0 || find(glides.begin(),glides.end(),make_pair(d%p,shift%m))==glides.end()){
     all=false;break;
    }
   }
   if(all){int G=0;for(int k=0;k<d;k++)G+=e.g[k%p];sol.emplace_back(parity,d,((G+1-parity)/2)%m);}
  }
  cout<<e.name<<" L="<<L<<" glides=";
  for(auto [a,b]:glides)cout<<"("<<a<<","<<b<<")";
  cout<<" solutions=";for(auto [a,b,c]:sol)cout<<"("<<a<<","<<b<<","<<c<<")";cout<<"\n";
  if(e.name=="p8-rec0"||e.name=="p8-rec1"){
   assert((glides==vector<pair<int,int>>{{2,5},{6,15}}));
   assert((sol==vector<tuple<int,int,int>>{{0,18,5},{1,62,15}}));
  } else if(e.name=="p8-rec2"){
   assert((glides==vector<pair<int,int>>{{4,24}}));assert(sol.empty());
  }else{assert(glides.empty());assert(sol.empty());}
 }
 cout<<"INDEPENDENT GLIDE/PHASE CONTROLS PASSED\n";
}
