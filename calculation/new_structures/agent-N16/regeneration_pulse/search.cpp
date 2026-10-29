// Deterministic base-10 centre screen: 22-step outward pulse and 264-step retention.
#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>
using namespace std;
using V=vector<unsigned char>;
int cv(char c){return c<='9'?c-'0':c-'A'+10;}
V next_pair(const V&p){V d;d.reserve(p.size()+1);int c=0;for(int x:p){int z=x+c;d.push_back(z%10);c=z/10;}if(c)d.push_back(c);V ans(d.size());for(int i=0;i<(int)d.size();i++)ans[i]=d[i]+d[d.size()-1-i];return ans;}
int match(const V&p,const string&b,const string&w){int m=0;for(int i=0;i<(int)p.size()/2;i++){int x=i<39?cv(b[i]):cv(w[(i-39)%20]);if(p[i]!=x)break;++m;}return m;}
int main(int argc,char**argv){
 if(argc<2)return 2;int trials=argc>2?atoi(argv[2]):600000;
 ifstream f(argv[1]);string hdr;getline(f,hdr);vector<string>B(8),W(8);for(auto&x:B)getline(f,x);for(auto&x:W)getline(f,x);
 mt19937_64 rng(20261028);int q=5,h=39+20*q;V bulk;for(char c:B[0])bulk.push_back(cv(c));for(int j=0;j<q;j++)for(char c:W[0])bulk.push_back(cv(c));
 int best22=-999,best264=-999,screened=0,besttrial=-1;string bestcore;
 for(int trial=0;trial<trials;trial++){
  int width=1+(rng()%30);V low=bulk;string core;
  for(int i=0;i<width;i++){int v=rng()%19;low.push_back(v);core.push_back("0123456789ABCDEFGHI"[v]);}
  V p=low;for(auto j=low.rbegin();j!=low.rend();j++)p.push_back(*j);
  int initial=match(p,B[0],W[0]);
  for(int t=0;t<22;t++)p=next_pair(p);
  int gain=match(p,B[22%8],W[22%8])-initial;
  best22=max(best22,gain);
  if(gain>=0){++screened;for(int t=22;t<264;t++)p=next_pair(p);
   int final=match(p,B[264%8],W[264%8])-h;
   if(final>best264){best264=final;besttrial=trial;bestcore=core;}
  }
 }
 cout<<"SCREEN trials="<<trials<<" screened="<<screened<<" max22="<<best22<<" max264="<<best264<<" first264trial="<<besttrial<<" best264core="<<bestcore<<"\n";
}
