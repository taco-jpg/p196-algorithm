// Exact independent decimal-frontier time-column DFS.
// Classifies the explicit depth-four state family, not all reachable states.
// Compile: c++ -O3 -std=c++17 agent16_interior_exact.cpp -o /tmp/a16_interior
// Run: /tmp/a16_interior 4 12
#include <bits/stdc++.h>
using namespace std;

int count_paths(int r,int s,int j,int u,int v){
  if(r<4||r>24||j<0||j>=r||s<0||s>1||u<0||u>1||v<0||v>1)abort();
  const int b=1<<(r+1),p=2*r+4;
  vector<int>g(p),L(p),H(p),Y(p);
  g[0]=g[r+1]=g[r+2]=1;
  string l=string(r+2,'1')+"0"+string(j+1,'1')+string(r-j,'0');
  string h=(s?string(j+1,'1'):"0"+string(j,'1'))+string(r-j,'0');
  h+=char('0'+u);h+=char('0'+v);h+=string(r,'1');h+='0';
  if((int)l.size()!=p||(int)h.size()!=p)abort();
  for(int t=0;t<p;t++){L[t]=l[t]-'0';H[t]=h[t]-'0';}
  Y[0]=b-2+s;Y[r+1]=b-(1<<(r-j))-1+u;Y[r+2]=b-(1<<(r-j))-1+v;
  int paths=0;
  for(int x0=0;x0<=2*b-2;x0++){
    auto rec=[&](auto&&self,int t,int x)->void{
      if(t==p){if(x==x0)paths++;return;}
      if(x<0||x>2*b-2)return;
      for(int c=0;c<=1;c++){
        if((x+c)/b!=H[t])continue;
        int next=(x+L[t])%b+(g[t]?Y[t]:(x+c)%b);
        self(self,t+1,next);
      }
    };rec(rec,0,x0);
  }
  return paths;
}

int main(int argc,char**argv){
  if(argc!=3){cerr<<"usage: a16_interior MIN_R MAX_R\n";return 2;}
  int low=atoi(argv[1]),high=atoi(argv[2]);
  if(low<4||high>18||low>high)return 2;
  const set<tuple<int,int,int,int>> expected={
    // encoded (s, j-(r-2),u,v)
    {0,0,0,1},{0,0,1,1},{0,1,1,0},{0,1,1,1},{1,1,0,0},{1,1,1,0}
  };
  for(int r=low;r<=high;r++){
    long interior=0;map<tuple<int,int,int,int>,int> live;
    for(int s=0;s<=1;s++)for(int j=0;j<r;j++)for(int u=0;u<=1;u++)for(int v=0;v<=1;v++){
      int n=count_paths(r,s,j,u,v);
      if(j<=r-3){
        if(n!=0){cerr<<"COUNTEREXAMPLE r="<<r<<" s="<<s<<" j="<<j<<" u="<<u<<" v="<<v<<" paths="<<n<<"\n";return 1;}
        interior++;
      }else if(n){live[{s,j-(r-2),u,v}]=n;}
    }
    if(interior!=8*(r-2))return 1;
    if(live.size()!=expected.size())return 1;
    for(auto const& t:expected){
      auto it=live.find(t);if(it==live.end())return 1;
      int exp=(get<1>(t)==0?4:(get<0>(t)==0?8:4));
      if(it->second!=exp){cerr<<"wrong boundary count "<<it->second<<" expected "<<exp<<"\n";return 1;}
    }
    cout<<"PASS r="<<r<<" b="<<(1<<(r+1))<<" no-edge interior="<<interior
        <<" boundary-active="<<live.size()<<" boundary-paths=32\n"<<flush;
  }
  cout<<"PASS exact state-family time-closure controls\n";
}
