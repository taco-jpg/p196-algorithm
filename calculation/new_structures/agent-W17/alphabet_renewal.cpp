// W17: exact phase-locked binary centre-alphabet experiment (not an infinite certificate).
// Compile: c++ -O3 -std=c++17 alphabet_renewal.cpp -lgmpxx -lgmp -o alphabet_renewal
// Run from this directory: ./alphabet_renewal lattice.txt 4096
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <gmpxx.h>
#include <numeric>
#include <string>
#include <vector>
using namespace std;
struct Lattice {
  int ext[39][8]{}; int lattice[8][20]{};
  vector<int> B, W;
  explicit Lattice(const string &path) {
    ifstream in(path); if (!in) { cerr<<"missing lattice data\n"; exit(2); }
    for (auto &row : ext) for (int &v : row) if (!(in>>v)) exit(3);
    for (auto &row : lattice) for (int &v : row) if (!(in>>v)) exit(4);
    for (const auto &row : ext) B.push_back(row[0]);
    for (int v:lattice[0]) W.push_back(v);
  }
};
static const vector<int> sites={0,2,4,6,8,10,12,14,16,18,22,26};
vector<int> centre(uint32_t mask, int special, int width=40) {
  vector<int> U(width,1); U[13]=special&1?16:7;
  U[20]=special&2?16:7; U[30]=special&4?15:6;
  for (int k=0;k<(int)sites.size();k++) if (mask&(1u<<k)) U[sites[k]]=10;
  vector<int> C={8,0,0}; C.insert(C.end(),U.begin(),U.end());
  C.push_back(16); C.insert(C.end(),U.rbegin(),U.rend());
  C.insert(C.end(),{0,0,8}); return C;
}
vector<int> makeP(const Lattice &z,const vector<int> &C,int q) {
  vector<int> a=z.B;
  for(int i=0;i<q;i++) a.insert(a.end(),z.W.begin(),z.W.end());
  vector<int> P=a; P.insert(P.end(),C.begin(),C.end());
  P.insert(P.end(),a.rbegin(),a.rend()); return P;
}
void check(bool b,const string &s){if(!b){cerr<<"FAIL: "<<s<<"\n";exit(5);}}
// Independent *pair-coefficient* propagation; normalized decimal addition.
int stepPair(vector<int> &P) {
  int carry=0; vector<int> digits;digits.reserve(P.size()+1);
  for(int x:P){int k=x+carry;digits.push_back(k%10);carry=k/10;}
  if(carry)digits.push_back(carry);
  vector<int> next(digits.size());
  for(size_t i=0;i<digits.size();i++)next[i]=digits[i]+digits[digits.size()-1-i];
  P.swap(next);return carry;
}
// Fully independent *ordinary decimal digits* carry/reverse/add.
vector<int> makeDigits(const vector<int> &P) {
  vector<int>d(P.size());int n=(int)P.size();
  check(P==vector<int>(P.rbegin(),P.rend()),"initial symmetry");
  for(int i=0;i<n/2;i++){d[i]=min(9,P[i]);d[n-1-i]=P[i]-d[i];}
  if(n%2){check(P[n/2]%2==0,"odd centre");d[n/2]=P[n/2]/2;}
  check(d.back()>0,"positive leading digit");return d;
}
int stepDigits(vector<int> &d) {
  int n=d.size(),carry=0;vector<int> nxt;nxt.reserve(n+1);
  for(int i=0;i<n;i++){int s=d[i]+d[n-1-i]+carry;nxt.push_back(s%10);carry=s/10;}
  if(carry)nxt.push_back(carry);
  d.swap(nxt);return carry;
}
vector<int> pairs(const vector<int>&d){int n=d.size();vector<int>p(n);for(int i=0;i<n;i++)p[i]=d[i]+d[n-1-i];return p;}
void run(const Lattice &z,uint32_t mask,int special,int q,bool fullIndependent){
  const auto C=centre(mask,special);vector<int>P=makeP(z,C,q);
  vector<int>d;if(fullIndependent)d=makeDigits(P);
  int initial=(int)P.size();
  for(int t=0;t<=352;t++) {
    check((int)P.size()>=78,"exterior vanished");
    for(int j=0;j<39;j++)check(P[j]==z.ext[j][t%8],"exterior phase t="+to_string(t));
    bool odd=false;for(int x:P)if(x%2){odd=true;break;}
    check(odd,"nonpalindromic pair witness t="+to_string(t));
    if(fullIndependent){
      check(P==pairs(d),"ordinary digits disagree at t="+to_string(t));
      check(d!=vector<int>(d.rbegin(),d.rend()),"ordinary digit palindrome");
    }
    if(t%88==0){
      check((int)P.size()==initial+44*(t/88),"incorrect macro length");
      int fixed=39+20*q;
      if(t<=264){
        vector<int>A=z.B;for(int j=0;j<q;j++)A.insert(A.end(),z.W.begin(),z.W.end());
        check(equal(A.begin(),A.end(),P.begin()) && equal(A.begin(),A.end(),P.rbegin()),"band renewal at "+to_string(t));
        check((int)P.size()-2*fixed==87+44*(t/88),"core length");
      } else {
        int start=39+20*(q-1),match=0;
        while(match<20&&P[start+match]==z.W[match])match++;
        check(match==2,"expected break on fourth attempt: "+to_string(match));
      }
    }
    if(t==352)break;
    int g=stepPair(P);
    check(g==((t%2)==0),"coefficient overflow t="+to_string(t));
    if(fullIndependent)check(stepDigits(d)==g,"digit engine overflow t="+to_string(t));
  }
}
void longReplay(const Lattice &z, uint32_t mask, int special, int q, int T) {
  vector<int>P=makeP(z,centre(mask,special),q);
  vector<int>d=makeDigits(P);
  string init;for(auto it=d.rbegin();it!=d.rend();++it)init.push_back(char('0'+*it));
  mpz_class N(init,10);
  uint64_t hash=14695981039346656037ULL;
  for(int t=0;t<=T;t++){
    string ss=N.get_str(10);
    check(ss.size()==d.size(),"GMP versus schoolbook length");
    for(size_t i=0;i<d.size();i++)check(d[i]==ss[ss.size()-1-i]-'0',"GMP versus schoolbook digit");
    check(P==pairs(d),"GMP versus coefficient pairword");
    check(ss!=string(ss.rbegin(),ss.rend()),"actual palindrome");
    for(int j=0;j<39;j++)check(P[j]==z.ext[j][t%8],"long exterior t="+to_string(t));
    if(t==88||t==176||t==264){vector<int>a=z.B;for(int j=0;j<q;j++)a.insert(a.end(),z.W.begin(),z.W.end());check(equal(a.begin(),a.end(),P.begin()) && equal(a.begin(),a.end(),P.rbegin()),"long renewal");}
    int bulkMatch=0;int half=P.size()/2;while(39+bulkMatch<half && P[39+bulkMatch]==z.lattice[t%8][bulkMatch%20])bulkMatch++;
    if(t==0||t==88||t==176||t==264||t==352||t==5000||t==10000||t==15000||t==T){
      hash=14695981039346656037ULL;for(char c:ss){hash ^= uint8_t(c);hash*=1099511628211ULL;}
      cout<<"checkpoint t="<<t<<" digits="<<ss.size()<<" fnv64="<<hash<<" lattice_match="<<bulkMatch<<" full_W="<<(bulkMatch/20)<<"\n";
    }
    if(t==T)break;
    string rev(ss.rbegin(),ss.rend());
    mpz_class R(rev,10);N+=R;
    int a=stepDigits(d),b=stepPair(P);
    check(a==b&&a==((t%2)==0),"GMP/decimal/pair carry mismatch");
  }
  cout<<"PASS long replay T="<<T<<" q="<<q<<" mask="<<mask<<" special="<<special<<" (GMP + digit-list + pairword)\n";
}
int main(int argc,char **argv){
  if(argc<3){cerr<<"usage: alphabet_renewal lattice.txt number_of_masks[1..4096]\n";return 2;}
  Lattice z(argv[1]);if(argc>3&&string(argv[3])=="--long"){longReplay(z,4095,7,225,20000);return 0;}int masks=atoi(argv[2]);check(masks>=1&&masks<=4096,"number_of_masks range");
  uint64_t count=0;for(int m=0;m<masks;m++)for(int s=0;s<8;s++){
    // All 8 specials and all 12 binary choices independently vary.
    bool independently=(m==0||m==1||m==42||m==4095) && (s==0||s==7);
    run(z,m,s,1,independently);
    if(independently){for(int q=2;q<=4;q++)run(z,m,s,q,true);}
    count++;
  }
  cout<<"PASS centres="<<count<<" each 352 steps q=1; triple renewal t=88,176,264; fourth W-prefix=2\n";
  cout<<"Independent ordinary-digit checks: 8 centre masks/specials x q=1..4 x 352 steps\n";
}
