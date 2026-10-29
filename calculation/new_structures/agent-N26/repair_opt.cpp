// Deterministic stochastic synthesis of a finite-life repaired centre (not SAT proof).
// g++ -std=c++17 -O3 repair_opt.cpp -o repair_opt
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>
using namespace std;
using R=array<int,8>;
vector<R> parse(const string&s){vector<R>v;size_t p=0;while((p=s.find('[',p))!=string::npos){auto q=s.find(']',p);R row{};string x=s.substr(p+1,q-p-1);size_t z=0;for(int i=0;i<8;i++){size_t k=x.find(',',z);row[i]=stoi(x.substr(z,k-z));z=k+1;}v.push_back(row);p=q+1;}return v;}
vector<R>path,cyc;
vector<int> prefix(int copies){vector<int>a;for(auto r:path)a.push_back(r[0]);for(int j=0;j<copies;j++)for(auto r:cyc)a.push_back(r[0]);return a;}
vector<int> mk(const vector<int>&A,const vector<int>&core){vector<int>P=A;P.insert(P.end(),core.begin(),core.end());P.insert(P.end(),core.rbegin(),core.rend());P.insert(P.end(),A.rbegin(),A.rend());return P;}
int fitness(const vector<int>& A,const vector<int>&core,int Tmax){auto P=mk(A,core);for(int t=0;t<=Tmax;t++){
  if(P.size()<78)return t;
  for(int j=0;j<39;j++)if(P[j]!=path[j][t%8])return t;
  int carry=0;vector<int>D;D.reserve(P.size()+1);
  for(int p:P){int q=p+carry;D.push_back(q%10);carry=q/10;}
  if(carry)D.push_back(carry);
  if(carry!=(t%2==0?1:0))return t;
  vector<int>newP;newP.reserve(D.size());
  for(size_t j=0;j<D.size();j++)newP.push_back(D[j]+D[D.size()-1-j]);
  P=move(newP);
 }return Tmax+1;}
int main(int argc,char**argv){
 if(argc!=5){cerr<<"usage repair_opt p8_rec0_rows.txt copies core_halfwidth iterations\n";return 1;}
 ifstream in(argv[1]);string a,b;getline(in,a);getline(in,b);path=parse(a);cyc=parse(b);
 int copies=stoi(argv[2]),width=stoi(argv[3]),iter=stoi(argv[4]);auto A=prefix(copies);
 vector<int>base;for(int j=0;j<width;j++)base.push_back(cyc[j%20][0]);
 mt19937_64 rng(0x620A26);uniform_int_distribution<int> digit(0,18), idx(0,width-1);
 int f0=fitness(A,base,400),best=f0;auto bestCore=base;
 cout<<"baseline="<<f0<<" copies="<<copies<<" halfwidth="<<width<<"\n";
 int improved=0;
 for(int i=0;i<iter;i++){
   vector<int>trial;
   if(i%100==0)trial=base;
   else if(i%7==0)trial=bestCore;
   else trial=(rng()%2?base:bestCore);
   int k=1+(rng()%((i%10==0)?min(8,width):min(3,width)));
   while(k--){int j=idx(rng);trial[j]=digit(rng);}
   int score=fitness(A,trial,400);
   if(score>best){best=score;bestCore=trial;improved++;cout<<"IMPROVE iter="<<i<<" first_mismatch="<<score<<" center=";for(int x:trial)cout<<x<<",";cout<<"\n"<<flush;}
 }
 cout<<"FINAL baseline="<<f0<<" best="<<best<<" improved="<<improved<<"\n";
}
