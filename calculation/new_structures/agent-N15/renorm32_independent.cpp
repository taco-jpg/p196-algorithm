// Independent ordinary decimal N+reverse N validates time-15 32-state spatial grammar.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
using Bytes=std::vector<uint8_t>;
struct State {std::string factor;int out,left,right,cls;};
static std::string morph(std::string w,int h){for(int j=0;j<h;++j){std::string z;z.reserve(w.size()*2);for(auto x:w){z.push_back(x);z.push_back(x=='0'?'1':'0');}w.swap(z);}return w;}
static Bytes seed(const std::string&w){int n=2*(int(w.size())+1);Bytes d(n,0);d[0]=0;d[n-1]=4;for(int i=1;i<n/2;++i){d[i]=w[i-1]=='0'?5:7;d[n-1-i]=9;}return d;}
static Bytes addrev(const Bytes&d){Bytes out;out.reserve(d.size()+1);int c=0,n=d.size();for(int i=0;i<n;++i){int z=d[i]+d[n-1-i]+c;out.push_back(z%10);c=z/10;}if(c)out.push_back(c);return out;}
static Bytes pair(const Bytes&d){Bytes p(d.size());for(int i=0;i<int(d.size());++i)p[i]=d[i]+d[d.size()-1-i];return p;}
int main(int argc,char**argv){if(argc!=2){std::cerr<<"need renorm32_states.tsv path\n";return 2;}std::ifstream file(argv[1]);assert(file);std::string line;std::vector<State> states;std::unordered_map<std::string,int> lookup;
while(std::getline(file,line)){if(line.empty()||line[0]=='#')continue;std::istringstream s(line);int id;State z;s>>id>>z.factor>>z.out>>z.left>>z.right>>z.cls;assert(id==int(states.size()));assert(z.factor.size()==77);lookup[z.factor]=id;states.push_back(z);}assert(states.size()==240);assert(lookup.size()==240);
int checked_edges=0;std::vector<int> outputs(32,-1),offspring0(32,-1),offspring1(32,-1);for(int i=0;i<240;i++){auto s=states[i];auto c=s.cls;assert(c>=0&&c<32);if(outputs[c]<0){outputs[c]=s.out;offspring0[c]=states[s.left].cls;offspring1[c]=states[s.right].cls;}else{assert(outputs[c]==s.out);assert(offspring0[c]==states[s.left].cls);assert(offspring1[c]==states[s.right].cls);}auto x=morph(s.factor,1);assert(lookup.at(x.substr(38,77))==s.left);assert(lookup.at(x.substr(39,77))==s.right);++checked_edges;}assert(std::count_if(outputs.begin(),outputs.end(),[](int x){return x>=0;})==32);
std::vector<Bytes> P(15);int bulk=0,child=0;std::vector<int> stateSeen(240,0),observedVal(240,-1);
for(int h=7;h<=14;++h){std::string w=morph("0",h);auto d=seed(w);for(int t=0;t<15;t++)d=addrev(d);auto p=pair(d);if(h<=13)P[h-7]=p;for(int c=38;c<int(w.size())-38;c++){auto it=lookup.find(w.substr(c-38,77));if(it==lookup.end()){std::cerr<<"Unknown actual factor h="<<h<<"\n";return 1;}int id=it->second;stateSeen[id]++;int got=p[c+2];if(observedVal[id]<0)observedVal[id]=got;else assert(observedVal[id]==got);if(got!=states[id].out){std::cerr<<"Independent integer disagrees at h="<<h<<", c="<<c<<"\n";return 1;}++bulk;}
if(h>=9){std::cout<<"INTEGER_REALIZATION h="<<h<<" pairdigits="<<p.size()<<" interior_cells="<<w.size()-76<<"\n";}}
// Every 77-factor occurs at h9, hence each single-state label mutation is detected.
for(auto count:stateSeen)assert(count>0);int mutant=0;for(int i=0;i<240;i++){int changed=(states[i].out+1)%19;assert(observedVal[i]==states[i].out);assert(changed!=observedVal[i]);++mutant;}
// Cross-height identities are tested on the same authentic integer orbits,
// not just on combinatorially substituted words.
for(int h=7;h<=12;++h){auto w=morph("0",h);auto &next=P[h+1-7];for(int c=38;c<int(w.size())-38;++c){int id=lookup.at(w.substr(c-38,77));auto &s=states[id];if(next[2*c+2]!=states[s.left].out||next[2*c+3]!=states[s.right].out){std::cerr<<"Cross-scale fails h="<<h<<" c="<<c<<"\n";return 1;}child+=2;}}
std::cout<<"RENORM_ORDINARY_DECIMAL_PASS alphabet=240 quotient=32 full_integer_bulk="<<bulk<<" cross_scale_children="<<child<<" encoded_edges="<<checked_edges<<" mutation_rejections="<<mutant<<"\n";}
