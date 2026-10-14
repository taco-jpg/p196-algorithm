#include <array>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <fstream>
#include <iostream>
#include <chrono>
#include <cstdint>
#include <algorithm>
using namespace std;
struct State {uint64_t f,z; bool operator==(const State&o)const{return f==o.f&&z==o.z;}};
struct Hash {size_t operator()(const State&s)const{uint64_t x=s.z^(s.f*0x9e3779b97f4a7c15ULL);x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;return x^(x>>31);}};
State canonical(State s){
 State best=s;constexpr uint64_t low11=2047ULL|(2047ULL<<12)|(2047ULL<<24),first=1ULL|(1ULL<<12)|(1ULL<<24);
 for(int k=1;k<12;k++){s.f=((s.f>>1)&low11)|((s.f&first)<<11);s.z=(s.z>>4)|((s.z&15)<<44);if(s.f<best.f||(s.f==best.f&&s.z<best.z))best=s;}return best;
}
struct Opt{int Q,a,b,c,e,R;};
vector<Opt> opts[88];
int code(int a,int b,int c,int z){return ((a*2+b)*2+c)*11+z+1;}
void initialize(){for(int a=0;a<2;a++)for(int b=0;b<2;b++)for(int c=0;c<2;c++)for(int z=-1;z<=9;z++){
 auto &v=opts[code(a,b,c,z)];
 for(int e=0;e<2;e++){int R=z+10*e;if(R<0||R>18||(R<9&&e)||(R>9&&!e))continue;
 for(int Q=0;Q<=18;Q++)for(int A=0;A<2;A++)for(int B=0;B<2;B++)if((Q+A)/10==a&&(Q+A)%10+(Q+c)%10==R&&(R+B)/10==b)v.push_back({Q,A,B,(Q+c)/10,e,R});}
}}
int compat(const Opt &x,const Opt &y){int z=y.Q-(x.R+x.b)%10-x.e;if(z< -1||z>9||(z==-1&&!x.e)||(z==9&&x.e))return -100;return z;}
array<int,12> decode(State s){array<int,12> r;for(int j=0;j<12;j++)r[j]=code((s.f>>j)&1,(s.f>>(12+j))&1,(s.f>>(24+j))&1,int((s.z>>(4*j))&15)-1);return r;}
bool viable(State s){auto a=decode(s);for(auto x:a)if(opts[x].empty())return false;
 for(int first=0;first<int(opts[a[0]].size());first++){int mask=1<<first;
 for(int j=0;j<11&&mask;j++){int nm=0;for(int x=0;x<int(opts[a[j]].size());x++)if(mask&(1<<x))for(int y=0;y<int(opts[a[j+1]].size());y++)if(compat(opts[a[j]][x],opts[a[j+1]][y])!=-100)nm|=1<<y;mask=nm;}
 for(int last=0;last<int(opts[a[11]].size());last++)if((mask&(1<<last))&&compat(opts[a[11]][last],opts[a[0]][first])!=-100)return true;
 }return false;
}
template<class F>void predecessors(State s,F emit){auto a=decode(s);for(auto x:a)if(opts[x].empty())return;array<Opt,12> path;
 auto walk=[&](auto&&self,int j,uint64_t f,uint64_t z)->void{
  if(j==12){int zz=compat(path[11],path[0]);if(zz!=-100)emit(State{f,z|(uint64_t(zz+1)<<44)},path);return;}
  for(auto op:opts[a[j]]){int zz=j?compat(path[j-1],op):0;if(j&&zz==-100)continue;path[j]=op;
   self(self,j+1,f|(uint64_t(op.a)<<j)|(uint64_t(op.b)<<(12+j))|(uint64_t(op.c)<<(24+j)),j?z|(uint64_t(zz+1)<<(4*(j-1))):z);
  }
 };walk(walk,0,0,0);
}
int main(int argc,char**argv){initialize();string dir=argc>1?argv[1]:".";size_t cap=argc>2?stoull(argv[2]):2000000;int layers=argc>3?stoi(argv[3]):15;bool prune=argc>4?stoi(argv[4]):true;
 ifstream in(dir+"/targets.txt");int nt;in>>nt;unordered_set<State,Hash> seen;vector<State> cur;for(int i=0;i<nt;i++){State s;in>>s.f>>s.z;s=canonical(s);if(seen.insert(s).second)cur.push_back(s);}
 State root{uint64_t(4095)<<12|uint64_t(4095)<<24,0};for(int j=0;j<12;j++)root.z|=8ULL<<(4*j);
 auto begin=chrono::steady_clock::now();bool hit=false,cut=false;size_t expanded=0;
 cout<<"{\"kind\":\"initial\",\"orbits\":"<<cur.size()<<",\"root_viable\":"<<viable(root)<<",\"prune\":"<<prune<<"}"<<endl;
 for(int dep=1;dep<=layers&&!cur.empty();dep++){
  vector<State> next;size_t edges=0,live=0,root_hits=0;unordered_map<size_t,size_t> histogram;
  for(auto s:cur){size_t degree=0;predecessors(s,[&](State old,const array<Opt,12>&path){edges++;degree++;if(old==root){hit=true;root_hits++;cout<<"{\"kind\":\"ROOT_HIT\",\"reverse_depth\":"<<dep<<"}"<<endl;}if(prune&&!viable(old)&&!(old==root))return;live++;old=canonical(old);if(seen.insert(old).second)next.push_back(old);});histogram[degree]++;expanded++;if(seen.size()>=cap){cut=true;break;}}
  cout<<"{\"kind\":\"layer\",\"depth\":"<<dep<<",\"parents\":"<<cur.size()<<",\"edges\":"<<edges<<",\"viable_edges\":"<<live<<",\"new_orbits\":"<<next.size()<<",\"seen\":"<<seen.size()<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-begin).count()<<",\"complete\":"<<(!cut)<<",\"root_hits\":"<<root_hits<<"}"<<endl;
  if(cut)break;cur=move(next);
 }
 if(!cut&&cur.empty()&&!hit){
  vector<State> certificate(seen.begin(),seen.end());sort(certificate.begin(),certificate.end(),[](State a,State b){return a.f<b.f||(a.f==b.f&&a.z<b.z);});
  ofstream out(dir+"/viable_closed_states.txt");out<<certificate.size()<<'\n';for(auto s:certificate)out<<s.f<<' '<<s.z<<'\n';
 }
 cout<<"{\"kind\":\"summary\",\"hit\":"<<hit<<",\"cut\":"<<cut<<",\"seen\":"<<seen.size()<<",\"expanded\":"<<expanded<<",\"status\":\""<<(hit?"root intersection requires path replay":cut?"UNKNOWN state cap":cur.empty()?"reverse closure excludes root":"UNKNOWN depth cap")<<"\"}"<<endl;
}
