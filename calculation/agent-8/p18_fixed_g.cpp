// Agent 8: independent compact exact fixed-g B-side column transfer, base 10.
// c++ -O3 -std=c++17 p18_fixed_g.cpp -o p18_fixed_g
// ./p18_fixed_g 000100011000100011 5000000
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <unordered_set>
#include <vector>
using namespace std;
using U=uint64_t;
int p,ng;vector<int> g,idx;size_t cap;
unordered_set<U> seen;
vector<U> frontier,nxt;
uint64_t arcs=0;

bool accept(U s){
  for(int t=0;t<p;t++){
    int L=(s>>t)&1,H=(s>>(p+t))&1;
    if(L+H!=1)return false;
    if(g[t]){
      int Y=(s>>(2*p+4*idx[t]))&15;
      if(Y!=9*L)return false;
    }
  }
  return true;
}

void transitions(U s,bool first){
  int L[32],H[32],Y[32];
  for(int t=0;t<p;t++){
    L[t]=(s>>t)&1; H[t]=(s>>(p+t))&1;
    Y[t]=g[t]?int((s>>(2*p+4*idx[t]))&15):0;
  }
  struct Rec{
    static void go(int t,int x,int x0,U accum,const int*L,const int*H,const int*Y){
      if(t==p){
        if(x==x0){
          arcs++;
          if(seen.insert(accum).second)nxt.push_back(accum);
        }
        return;
      }
      for(int h=0;h<2;h++){
        if((x+h)/10!=H[t])continue;
        int d=(x+L[t])%10;
        int r=(x+h)%10;
        int nx=d+(g[t]?Y[t]:r);
        U next=accum | (U((x+L[t])/10)<<t) | (U(h)<<(p+t));
        if(g[t])next|=U(r)<<(2*p+4*idx[t]);
        go(t+1,nx,x0,next,L,H,Y);
      }
    }
  };
  for(int x0=(first?1:0);x0<=18;x0++)Rec::go(0,x0,x0,0,L,H,Y);
}
int main(int argc,char**argv){
  if(argc<2){cerr<<"usage: p18_fixed_g BITSTRING [MAXSTATES]\n";return 2;}
  string gs=argv[1];p=int(gs.size());cap=argc>=3?strtoull(argv[2],nullptr,10):300000;
  if(p<1||p>20){cerr<<"p must be in 1..20\n";return 2;}
  for(char c:gs){if(c!='0'&&c!='1')return 2;g.push_back(c-'0');}
  idx.assign(p,-1);ng=0; U start=0;
  for(int t=0;t<p;t++)if(g[t]){idx[t]=ng;ng++;start|=U(1)<<(p+t);start|=U(1)<<(2*p+4*idx[t]);}
  if(2*p+4*ng>64){cerr<<"ENCODING TOO WIDE\n";return 2;}
  seen.reserve(min(cap+1, size_t(10000000)));seen.insert(start);frontier.push_back(start);
  int depth=0;
  while(!frontier.empty()){
    nxt.clear();
    for(U state:frontier){
      if(accept(state)){
        cout<<"ACCEPT g="<<gs<<" depth="<<depth<<" states="<<seen.size()<<" arcs="<<arcs<<" L=";
        for(int t=0;t<p;t++)cout<<((state>>t)&1);
        cout<<"\n";return 0;
      }
      transitions(state,depth==0);
      if(seen.size()>cap){cout<<"CAPPED g="<<gs<<" depth="<<depth<<" states="<<seen.size()<<" arcs="<<arcs<<"\n";return 3;}
    }
    frontier.swap(nxt);depth++;
    if(depth>450){cout<<"DEPTH_CAPPED g="<<gs<<" depth="<<depth<<" states="<<seen.size()<<" arcs="<<arcs<<"\n";return 3;}
  }
  cout<<"EXHAUSTED g="<<gs<<" depth="<<depth<<" states="<<seen.size()<<" arcs="<<arcs<<"\n";
}