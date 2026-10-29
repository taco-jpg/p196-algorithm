// S12: exact all-width mod-101 carry-source delta under U^k -> U^(k+5).
// Build from repository root: g++ -O3 -std=c++17 calculation/new_structures/S12/epoch_delta.cpp -o /tmp/s12_epoch_delta
#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <set>
#include <string>
#include <sstream>
#include <utility>
#include <vector>
using namespace std;
using Word = vector<int>; // coefficient or decimal digits, LSD first where applicable
constexpr int MOD = 101;
int md(long long x) { x %= MOD; if (x < 0) x += MOD; return int(x); }
int mul(int a, int b) { return a * b % MOD; }
int pow10m(int n) { int r = 1; for (int i = 0; i < n % 4; ++i) r = mul(r, 10); return r; }
int powxm(int n) { int r = 1; for (int i = 0; i < n % 4; ++i) r = mul(r, md(-10)); return r; }
int geom10(int k) { int r = 0; for (int i = 0; i < k; ++i) r = md(r + pow10m(i)); return r; }

struct Root { Word gamma; vector<Word> W; vector<Word> B; };
Root read_root(const string& path) {
  ifstream f(path); if (!f) throw runtime_error("cannot open lattice data: " + path);
  vector<Word> rows; string line;
  while (getline(f, line)) { if (line.empty()) continue; Word row; int x; istringstream iss(line); while (iss >> x) row.push_back(x); if (!row.empty()) rows.push_back(row); }
  if (rows.size() != 38 || rows[0] != Word({12,34,9,10})) throw runtime_error("unexpected p12/m9 lattice layout");
  Root r; r.gamma=rows[1]; r.W.assign(rows.begin()+2, rows.begin()+14); r.B.assign(rows.begin()+26, rows.begin()+38);
  for (auto& w:r.W) if(w.size()!=9) throw runtime_error("W row width != 9");
  for (auto& b:r.B) if(b.size()!=34) throw runtime_error("B row width != 34");
  return r;
}
Word repeat(const Word& a, int n) { Word z; z.reserve(a.size()*n); for(int i=0;i<n;++i) z.insert(z.end(),a.begin(),a.end()); return z; }
Word reverse_word(Word a) { reverse(a.begin(),a.end()); return a; }
Word pairword(const Root& root, int q, int k, const Word& J, const Word& U, const Word& C) {
  Word H=root.B[0], w=repeat(root.W[0],q), u=repeat(U,k);
  H.insert(H.end(),w.begin(),w.end()); H.insert(H.end(),J.begin(),J.end()); H.insert(H.end(),u.begin(),u.end());
  Word P=H; P.insert(P.end(),C.begin(),C.end()); Word rh=reverse_word(H); P.insert(P.end(),rh.begin(),rh.end()); return P;
}
struct Carries { int K; Word out; int gamma; };
Carries normalize(const Word& P) {
  int carry=0, K=0; Word cs; cs.reserve(P.size());
  for(size_t i=0;i<P.size();++i) { carry=(P[i]+carry)/10; cs.push_back(carry); K=md(K+mul(carry,powxm(int(i+1)))); }
  return {K,cs,carry};
}
pair<int,int> block(const Word& u, int c0) {
  int c=c0, A=0;
  for(size_t i=0;i<u.size();++i) { c=(u[i]+c)/10; A=md(A+mul(c,powxm(int(i+1)))); }
  return {c,A};
}
int segment_K(const Word& carries, int lo, int hi) {
  int r=0; for(int i=lo;i<hi;++i) r=md(r+mul(carries[i],powxm(i+1))); return r;
}
int predict_delta_K(const Root& root,int q,int k,const Word& J,const Word& U,const Word& C,const Carries& oldc) {
  Word V=reverse_word(U); const int a=int(root.B[0].size()+root.W[0].size()*q+J.size());
  const int c=int(C.size()), s=a+3*k, sc=s, t=sc+c, z=t+3*k;
  const int betaU=block(U,0).first, betaU1=block(U,1).first;
  const int betaV=block(V,0).first, betaV1=block(V,1).first;
  assert(betaU==betaU1 && betaV==betaV1); // each motif has a low (<9) and high (>9) reset
  const int AU=block(U,betaU).second;
  const int b=(t==0?0:oldc.out[t-1]);
  const int AV0=block(V,b).second, AVstar=block(V,betaV).second;
  assert(block(V,b).first==betaV && block(V,betaV).first==betaV);
  const int KC=segment_K(oldc.out,sc,sc+c), KZ=segment_K(oldc.out,z,int(oldc.out.size()));
  int pred=mul(powxm(s),AU);
  pred=md(pred+9LL*KC);
  const int right_local=md(9LL*AV0+mul(AVstar,md(1-2LL*geom10(k))));
  pred=md(pred+mul(powxm(t),right_local)-2LL*KZ);
  return pred;
}
Word source_digits(const Word& P) {
  if(P.size()%2 || !equal(P.begin(),P.end(),P.rbegin())) throw runtime_error("pairword must be symmetric and even-length");
  const int h=int(P.size()/2); Word lo,hi; lo.reserve(h);hi.reserve(h);
  for(int i=0;i<h;++i) { int l=max(P[i]-9,0); lo.push_back(l); hi.push_back(P[i]-l); }
  Word d=lo; for(auto it=hi.rbegin();it!=hi.rend();++it)d.push_back(*it);
  if(d.back()==0) throw runtime_error("invalid canonical source");
  for(size_t i=0;i<d.size();++i) if(d[i]+d[d.size()-1-i]!=P[i]) throw runtime_error("source pairword mismatch");
  return d;
}
vector<Word> motifs() {
  set<Word> out;
  for(int a=0;a<=18;a+=2) { Word u={9,a,18-a}; for(int r=0;r<3;++r) { Word v=u; rotate(v.begin(),v.begin()+r,v.end()); out.insert(v); } }
  return vector<Word>(out.begin(),out.end());
}
int main(int argc,char**argv) {
  try {
    const string path=argc>1?argv[1]:"calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt";
    Root root=read_root(path); auto Us=motifs(); if(Us.size()!=30) throw runtime_error("expected 30 distinct charge-zero U3 motifs");
    vector<pair<int,int>> widths; for(int q=20;q<24;++q)for(int k=40;k<44;++k)widths.push_back({q,k});
    for(int n:{20,40,80,160}) widths.push_back({n,n});
    vector<pair<Word,Word>> collars={
      {{5},{1,1}},
      {{4,12},{12,4,4,12}},
      {{18,6,10},{2,8,12,12,8,2}},
      {{14,18,1,15,4,16,12,10,4,6,3,9,13,10,1,9,7},{4,0,8,12,12,8,0,4}}
    };
    long long checked=0;
    for(const auto& U:Us) for(const auto& collar:collars) for(auto [q,k]:widths) {
      const Word& J=collar.first; const Word& C=collar.second;
      Word P=pairword(root,q,k,J,U,C), P5=pairword(root,q,k+5,J,U,C);
      Word d=source_digits(P), d5=source_digits(P5);
      Carries oldc=normalize(P), newc=normalize(P5);
      if(oldc.gamma!=1 || newc.gamma!=1) throw runtime_error("rooted phase-0 overflow must be 1");
      int predicted=predict_delta_K(root,q,k,J,U,C,oldc), actual=md(newc.K-oldc.K);
      if(predicted!=actual) { cerr<<"FAIL q="<<q<<" k="<<k<<" U="<<U[0]<<","<<U[1]<<","<<U[2]<<" predicted="<<predicted<<" actual="<<actual<<"\n"; return 1; }
      if(d.size()!=P.size() || d5.size()!=P5.size()) throw runtime_error("source length mismatch");
      checked++;
    }
    cout<<"PASS S12 exact carry-source delta: "<<checked<<" cases, 30 U motifs, 4 even-centre collars, 20 (q,k) pairs.\n";
    cout<<"Identity is all-width by the carry-reset proof and period-four weights; tests are independent finite controls only.\n";
  } catch(const exception& e) { cerr<<e.what()<<"\n"; return 2; }
}
