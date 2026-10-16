#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;
struct State {uint32_t l,r,p; uint8_t tag; bool operator==(State const& o)const{return l==o.l&&r==o.r&&p==o.p&&tag==o.tag;}};
struct Hash {size_t operator()(State const&s)const {uint64_t x=s.l*0x9e3779b185ebca87ULL+s.r;x^=x>>29;x=x*0xc2b2ae3d27d4eb4fULL+s.p;return (x^(x>>31))+s.tag*0x85ebca6b;}};
struct Node {State s; uint32_t parent;uint16_t depth;uint8_t digit;};
vector<int> hs,ins,opos;
vector<Node> nodes;
unordered_map<State,uint32_t,Hash> seen;
uint64_t edges=0;uint32_t current;int initialDigit,firstFilter=-1,violate=0;
void visit(int t,int q,uint32_t nl,uint32_t nr,uint32_t np,int j){
 if(t==11&&nodes[current].s.tag<4){
  int stage=nodes[current].s.tag;
  if(stage<violate&&q!=9)return;
  if(stage==violate&&q==9)return;
 }
 if(t==(int)hs.size()){
  edges++;State s{nl,nr,np,uint8_t(min(4,int(nodes[current].s.tag)+1))};auto it=seen.find(s);
  if(it==seen.end()){uint32_t id=nodes.size();seen.emplace(s,id);nodes.push_back({s,current,uint16_t(nodes[current].depth+1),uint8_t(initialDigit)});}return;
 }
 State st=nodes[current].s;int l=(st.l>>t)&1,r=(st.r>>t)&1;
 int z=q+l,lo=z%10,lc=z/10;
 for(int b=0;b<=1;b++){
  z=q+b;if(z/10!=r)continue;int hi=z%10;
  int nq=hs[t]?lo+((st.p>>(4*j))&15):lo+hi;
  visit(t+1,nq,nl|(uint32_t(lc)<<t),nr|(uint32_t(b)<<t),hs[t]?np|(uint32_t(hi)<<(4*j)):np,j+hs[t]);
 }
}
int head(State st){
 for(int middle=-1;middle<=18;middle+=middle<0?1:2){
  vector<int> q;if(middle>=0)q.push_back(middle);int j=0;bool ok=true;
  for(int t=0;t<(int)hs.size();t++){
   int c=(st.l>>t)&1;vector<int>d;
   for(int x:q){int z=x+c;d.push_back(z%10);c=z/10;}
   if(c!=int((st.r>>t)&1)){ok=false;break;}
   vector<int> out;
   if(hs[t]){
    int prev=(st.p>>(4*j++))&15;
    if(d.empty())out.push_back(2*prev);
    else{int end=d[0]+prev;out.push_back(end);for(int i=1;i<(int)d.size();i++)out.push_back(d[i]+d[d.size()-i]);out.push_back(end);}
   }else{for(int i=0;i<(int)d.size();i++)out.push_back(d[i]+d[d.size()-1-i]);}
   q.swap(out);
  }
  if(ok)return middle;
 }return -2;
}
int main(int argc,char**argv){
 int periods=argc>1?atoi(argv[1]):2;firstFilter=argc>2?atoi(argv[2]):-1;
 size_t maxstates=argc>3?strtoull(argv[3],nullptr,10):1000000;double seconds=argc>4?atof(argv[4]):30;
 violate=argc>5?atoi(argv[5]):0;
 if(periods>2){cerr<<"Masks support at most two periods\n";return 1;}
 int h[11]={1,1,0,0,0,1,0,0,0,0,1},r[11]={0,1,0,0,1,1,0,0,1,1,1};State start{0,0,0,0};int j=0;
 for(int p=0;p<periods;p++)for(int i=0;i<11;i++){int t=hs.size();hs.push_back(h[i]);ins.push_back(r[i]);start.l|=uint32_t(r[i])<<t;start.r|=uint32_t(1-r[i])<<t;if(h[i])start.p|=uint32_t(9*r[i])<<(4*j++);}
 nodes.reserve(maxstates+10000);seen.reserve(maxstates+10000);nodes.push_back({start,UINT32_MAX,0,0});seen[start]=0;
 auto begin=chrono::steady_clock::now();bool found=false;size_t done=0;
 for(current=0;current<nodes.size();current++){
  double elapsed=chrono::duration<double>(chrono::steady_clock::now()-begin).count();if(nodes.size()>maxstates||elapsed>seconds)break;
  int m=head(nodes[current].s);
  if(m!=-2){
   vector<int> half;uint32_t v=current;while(nodes[v].parent!=UINT32_MAX){half.push_back(nodes[v].digit);v=nodes[v].parent;}
   cout<<"FOUND core ";for(auto it=half.rbegin();it!=half.rend();++it)cout<<*it<<',';if(m>=0)cout<<m<<',';for(int x:half)cout<<x<<',';cout<<"\n";found=true;break;
  }
  for(initialDigit=0;initialDigit<=18;initialDigit++){
   if(current==0&&(initialDigit==9||(firstFilter>=0&&initialDigit!=firstFilter)))continue;
   visit(0,initialDigit,0,0,0,0);
  }
  done=current+1;
  if(done%100000==0)cerr<<"processed "<<done<<" states "<<nodes.size()<<" depth "<<nodes[current].depth<<" seconds "<<elapsed<<"\n";
 }
 double elapsed=chrono::duration<double>(chrono::steady_clock::now()-begin).count();
 cout<<"states "<<nodes.size()<<" edges "<<edges<<" processed "<<done<<" complete "<<(done==nodes.size())<<" found "<<found<<" seconds "<<elapsed<<"\n";
}
