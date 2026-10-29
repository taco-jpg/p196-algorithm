// Deterministic local mutation refinement of the 264-step constructive pulse.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>
using namespace std;using V=vector<unsigned char>;
int cv(char c){return c<='9'?c-'0':c-'A'+10;}
static vector<string>B(8),W(8);static V bulk;static const int h=139;
V step(const V&p){V d;d.reserve(p.size()+1);int c=0;for(int x:p){int s=x+c;d.push_back(s%10);c=s/10;}if(c)d.push_back(c);V out(d.size());for(int i=0;i<(int)d.size();i++)out[i]=d[i]+d[d.size()-1-i];return out;}
int match(const V&p,int t){int k=0;for(int i=0;i<(int)p.size()/2;i++){int expected=i<39?cv(B[t%8][i]):cv(W[t%8][(i-39)%20]);if(p[i]!=expected)break;k++;}return k;}
int score(const string&core,int H=264){V low=bulk;for(char c:core)low.push_back(cv(c));V p=low;for(auto j=low.rbegin();j!=low.rend();j++)p.push_back(*j);for(int t=0;t<H;t++){if(match(p,t)<39)return -999;int size=p.size();p=step(p);if(int(p.size())-size!=(t%2==0))return -999;}return match(p,H)-h;}
int main(int argc,char**argv){
 if(argc<2)return 2;ifstream f(argv[1]);string line;getline(f,line);for(auto&x:B)getline(f,x);for(auto&x:W)getline(f,x);for(char c:B[0])bulk.push_back(cv(c));for(int j=0;j<5;j++)for(char c:W[0])bulk.push_back(cv(c));
 string root=argc>3?argv[3]:"HEBBBCI8D2645G2HFAHE3CG5IG8F2",best=root;int bs=score(best);
 mt19937_64 rng(20261028);int iters=argc>2?atoi(argv[2]):30000;string alphabet="0123456789ABCDEFGHI";
 for(int trial=0;trial<iters;trial++){
  string candidate=best;
  int edits=1+(rng()%10==0?1:0);
  for(int e=0;e<edits;e++){
   int choice=rng()%12;
   if(choice==0&&candidate.size()>1)candidate.erase(candidate.begin()+rng()%candidate.size());
   else if(choice==1&&candidate.size()<50)candidate.insert(candidate.begin()+rng()%(candidate.size()+1),alphabet[rng()%19]);
   else candidate[rng()%candidate.size()]=alphabet[rng()%19];
  }
  int sc=score(candidate);
  if(sc>bs){best=candidate;bs=sc;cout<<"BETTER trial="<<trial<<" score="<<bs<<" core="<<best<<"\n";}
 }
 cout<<"RESULT best="<<bs<<" length="<<best.size()<<" core="<<best<<"\n";
}
