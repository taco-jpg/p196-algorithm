// Agent 4 T2: fixed-overflow full-width B position-automaton port.
// Independently scoped port of calculation/neutral_band/structure/bauto.cpp.
// Inputs: binary overflow stream; max seen states; optional max depth; optional -w.
// CAPPED and DEPTH-CAPPED are UNDECIDED, not negative results.
#include <bits/stdc++.h>
using namespace std;
using U=unsigned __int128;
struct KH {
  size_t operator()(U k) const {
    uint64_t a=(uint64_t)k,b=(uint64_t)(k>>64);
    return (size_t)((a*0x9E3779B97F4A7C15ULL)^(b*0xC2B2AE3D27D4EB4FULL)^(a>>29));
  }
};
int p,ng,g[32],yi[32],tidx[32];
U mask;
inline U pack(U L,U H,const int*Y) {
  U z=L|(H<<p);
  for(int i=0;i<ng;i++)z|=U(Y[i])<<(2*p+4*i);
  return z;
}
inline void unpack(U z,U&L,U&H,int*Y){
  L=z&mask;H=(z>>p)&mask;
  for(int i=0;i<ng;i++)Y[i]=(z>>(2*p+4*i))&15;
}
inline bool accepting(U L,U H,const int*Y){
  if((L^H)!=mask)return false;
  for(int i=0;i<ng;i++)if(Y[i]!=9*int((L>>tidx[i])&1))return false;
  return true;
}
int main(int argc,char**argv){
  if(argc<3){cerr<<"usage: fixed_g_B_probe gword maxStates [maxDepth] [-w]\n";return 2;}
  string str=argv[1];p=(int)str.size();
  if(p<1||p>24)return 2;
  U cap=strtoull(argv[2],nullptr,10);
  int maxdepth=argc>3?atoi(argv[3]):100;
  bool witness=argc>4 && string(argv[4])=="-w";
  mask=(U(1)<<p)-1;
  for(int t=0;t<p;t++){
    if(str[t]!='0'&&str[t]!='1')return 2;
    g[t]=str[t]-'0';yi[t]=g[t]?ng:-1;
    if(g[t])tidx[ng++]=t;
  }
  if(2*p+4*ng>127){cerr<<"128-bit packing insufficient\n";return 2;}
  int initY[32]{};
  for(int i=0;i<ng;i++)initY[i]=1;
  U H0=0;
  for(int t=0;t<p;t++)H0|=U(g[t])<<t;
  U start=pack(0,H0,initY);
  unordered_set<U,KH> seen;seen.insert(start);
  unordered_map<U,pair<U,vector<int>>,KH> parent;
  if(witness)parent[start]={0,{}};
  vector<U>frontier{start},next;
  for(int depth=0;depth<=maxdepth;depth++){
    next.clear();
    for(U z:frontier){
      U L,H;int Y[32];
      unpack(z,L,H,Y);
      if(accepting(L,H,Y)){
        string e;
        for(int t=0;t<p;t++)e+=char('0'+((L>>t)&1));
        cout<<"ACCEPT g="<<str<<" e="<<e<<" depth="<<depth<<" states="<<seen.size()<<"\n";
        if(witness){
          vector<vector<int>>cols;U cur=z;
          while(cur!=start){
            auto it=parent.find(cur);
            if(it==parent.end())break;
            cols.push_back(it->second.second);
            cur=it->second.first;
          }
          reverse(cols.begin(),cols.end());
          vector<int>B0;
          for(auto&col:cols)B0.push_back(col[0]);
          while(!B0.empty()&&B0.back()==9)B0.pop_back();
          cout<<"B0=[";
          for(size_t k=0;k<B0.size();k++)cout<<(k?",":"")<<B0[k];
          cout<<"]\n";
        }
        return 0;
      }
      for(int x0=depth==0?1:0;x0<=18;x0++){
        int xs[32]{},hn[32]{};
        function<void(int,int)> visit=[&](int t,int x){
          if(t==p){
            if(x!=x0)return;
            U L2=0,H2=0;int Y2[32]{};
            for(int k=0;k<p;k++){
              L2|=U((xs[k]+int((L>>k)&1))/10)<<k;
              H2|=U(hn[k])<<k;
            }
            for(int i=0;i<ng;i++){
              int tt=tidx[i];
              Y2[i]=(xs[tt]+hn[tt])%10;
            }
            U key=pack(L2,H2,Y2);
            if(seen.insert(key).second){
              next.push_back(key);
              if(witness)parent[key]={z,vector<int>(xs,xs+p)};
            }
            return;
          }
          for(int c=0;c<2;c++){
            if((x+c)/10!=int((H>>t)&1))continue;
            xs[t]=x;hn[t]=c;
            int y=(x+int((L>>t)&1))%10
              +(g[t]?Y[yi[t]]:(x+c)%10);
            visit(t+1,y);
          }
        };
        visit(0,x0);
      }
    }
    if(seen.size()>cap){
      cout<<"CAPPED g="<<str<<" depth="<<depth<<" states="<<seen.size()<<"\n";
      return 3;
    }
    if(next.empty()){
      cout<<"EXHAUSTED-NO-B-CYCLE g="<<str<<" depth="<<depth<<" states="<<seen.size()<<"\n";
      return 0;
    }
    frontier.swap(next);
  }
  cout<<"DEPTH-CAPPED-UNDECIDED g="<<str<<" states="<<seen.size()<<"\n";
  return 3;
}