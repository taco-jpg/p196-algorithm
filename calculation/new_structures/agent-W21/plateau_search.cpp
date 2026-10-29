// W21 seeded plateau search for terminal carry patch.
// c++ -O3 -std=c++17 plateau_search.cpp -o /tmp/w21_search; /tmp/w21_search 350000
#include <bits/stdc++.h>
using namespace std;
using V=vector<int>;
static const V B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const V W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
static const V R={17,3,1,13,17,11,14,3,18,1,2,0,13,3,0,16,6,9,6,1};
V step(const V& p){V d;d.reserve(p.size()+1);int c=0;for(int v:p){int x=v+c;d.push_back(x%10);c=x/10;}if(c)d.push_back(c);V r(d.size());for(int i=0,n=d.size();i<n;i++)r[i]=d[i]+d[n-1-i];return r;}
V seed(const V& half){V p=half;for(int i=(int)half.size()-1;i>=0;i--)p.push_back(half[i]);return p;}
V reference(){V a=B;for(int j=0;j<80;j++)a.insert(a.end(),W.begin(),W.end());V p=seed(a),e;for(int t=0;t<8;t++){e.insert(e.end(),p.begin(),p.begin()+39);p=step(p);}return e;}
int fitness(const V& core,const V& e,int cap=600){V a=B;a.insert(a.end(),core.begin(),core.end());V p=seed(a);for(int t=0;t<=cap;t++){for(int i=0;i<39;i++)if(p[i]!=e[39*(t%8)+i])return t;p=step(p);}return cap+1;}
int main(int argc,char**argv){int iters=argc>1?atoi(argv[1]):350000;V e=reference();mt19937 rng(991122+40*23);V best=W;best.insert(best.end(),R.begin(),R.end());V cur=best;int bests=fitness(best,e),sc=bests;cerr<<"initial="<<bests<<"\n";
 for(int k=1;k<=iters;k++){
  V trial=cur;int mutations=(rng()%10==0)?2:1;
  for(int j=0;j<mutations;j++){int pos=rng()%40;trial[pos]=(trial[pos]+1+rng()%18)%19;}
  int f=fitness(trial,e);
  if(f>bests){bests=f;best=trial;cout<<"BEST iteration="<<k<<" first_mismatch="<<f<<" patch=";for(int x:best)cout<<x<<",";cout<<"\n";}
  if(f>=sc){cur.swap(trial);sc=f;}else if((rng()%2000)==0){cur.swap(trial);sc=f;}
  if(k%50000==0){cur=best;sc=bests;}
 }
 cout<<"final_best="<<bests<<"\n";
}
