// Independent direct decimal reverse-and-add and coefficient-word replay.
// g++ -O3 -std=c++17 replay20k.cpp -o replay20k && ./replay20k 500 20000
#include <bits/stdc++.h>
using namespace std;
using Digit=uint8_t;
static const vector<Digit> B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const vector<Digit> W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
static const vector<Digit> V={4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,13,9,7,3,13,10,4,13,5,1,9,4,11,6,16,3,7,7,12,4,2,13,2,15,10,10,9,3};

static pair<vector<Digit>,int> normalize_coeff(const vector<Digit>& P){
 vector<Digit> d;d.reserve(P.size()+1);int c=0;
 for(Digit x:P){int z=int(x)+c;d.push_back(z%10);c=z/10;}
 int gamma=c;if(c)d.push_back(c);
 return {move(d),gamma};
}
static vector<Digit> ordinary_add_reverse(const vector<Digit>& D){
 size_t n=D.size();vector<Digit> out(n);int c=0;
 for(size_t i=0;i<n;i++){int z=int(D[i])+int(D[n-1-i])+c;out[i]=z%10;c=z/10;}
 if(c)out.push_back(c);return out;
}
static vector<Digit> pair_word(const vector<Digit>& D){
 size_t n=D.size();vector<Digit> P(n);
 for(size_t i=0;i<n;i++)P[i]=D[i]+D[n-1-i];return P;
}
static vector<Digit> fixednorm(const vector<Digit>& w){
 for(int init=0;init<=1;init++){
  int c=init;vector<Digit> out;out.reserve(w.size());
  for(Digit x:w){int y=int(x)+c;out.push_back(y%10);c=y/10;}
  if(c==init)return out;
 }
 throw runtime_error("no cyclic fixed carry");
}
static vector<Digit> bulk(const vector<Digit>& w,int gamma){
 auto L=fixednorm(w),r=w;reverse(r.begin(),r.end());auto H=fixednorm(r);reverse(H.begin(),H.end());
 vector<Digit> z(w.size());int m=w.size();
 for(int i=0;i<m;i++)z[i]=L[i]+H[(i-gamma+m)%m];
 return z;
}
static bool palindrome(const vector<Digit>& D){
 for(size_t i=0,n=D.size();i<n/2;i++)if(D[i]!=D[n-1-i])return false;
 return true;
}
int main(int argc,char**argv){
 const int k=argc>1?stoi(argv[1]):500,steps=argc>2?stoi(argv[2]):20000;
 if(k<400){cerr<<"k>=400 required for fixed windows\n";return 2;}
 vector<Digit> half=B;
 for(int rep=0;rep<k;rep++)half.insert(half.end(),W.begin(),W.end());
 half.push_back(9);
 for(int rep=0;rep<k;rep++)half.insert(half.end(),V.begin(),V.end());
 vector<Digit>P=half;P.push_back(9);P.insert(P.end(),half.rbegin(),half.rend());
 auto norm0=normalize_coeff(P);vector<Digit>D=move(norm0.first);vector<Digit> Wa=W,Va=V;
 const size_t ws=39+400,we=39+1400,vs=39+20*k+1+15000,ve=39+20*k+1+15960;
 if(ve>=half.size())throw runtime_error("V-window not internal");
 auto clock=chrono::steady_clock::now();
 uint64_t mismatch=0;
 for(int t=0;t<=steps;t++){
  if(palindrome(D)){cerr<<"PAL at t="<<t<<"\n";return 3;}
  if(P.size()/2<ve){cerr<<"window past center at t="<<t<<"\n";return 4;}
  for(size_t j=ws;j<we;j++)if(P[j]!=Wa[(j-39)%Wa.size()]){cerr<<"W lost at t="<<t<<" j="<<j<<"\n";return 5;}
  size_t base=39+20*k+1;
  for(size_t j=vs;j<ve;j++)if(P[j]!=Va[(j-base)%Va.size()]){cerr<<"V lost at t="<<t<<" j="<<j<<"\n";return 6;}
  auto check=normalize_coeff(P);
  if(check.first!=D){cerr<<"independent number disagreement at t="<<t<<"\n";return 7;}
  int gamma=check.second;
  if(gamma!=(t%2==0)){cerr<<"clock lost t="<<t<<" gamma="<<gamma<<"\n";return 8;}
  if(t==steps)break;
  vector<Digit> nextD=ordinary_add_reverse(D);
  vector<Digit> nextP=pair_word(D);
  D.swap(nextD);P.swap(nextP);
  Wa=bulk(Wa,gamma);Va=bulk(Va,gamma);
  if((t+1)%2000==0){cerr<<"verified "<<(t+1)<<" steps; digits="<<D.size()<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-clock).count()<<"\n";}
 }
 if(palindrome(D)){cerr<<"PAL at final state\n";return 9;}
 uint64_t hash=1469598103934665603ULL;
 for(Digit x:D){hash^=x;hash*=1099511628211ULL;}
 cout<<"PASS k="<<k<<" steps="<<steps<<" digits="<<D.size()<<" gamma=10 alternating, nonpal at all 20001 states, 50xW/20xV full-period bands at all 20001 states, independent RAA equality every step, FNV64="<<hex<<hash<<dec<<"\n";
 return 0;
}
