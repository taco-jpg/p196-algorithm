// Independent 20,000-step base-1286 ordinary digit-list reverse-and-add replay.
// No generator, solver, Python, or external JSON dependency.
// Build: c++ -std=c++17 -O3 calculation/neutral_band/agent10_base1286/replay.cpp -o /tmp/replay1286
// Run:   /tmp/replay1286 calculation/neutral_band/agent10_base1286/cert_b1286.json 20000
#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <regex>
#include <string>
#include <vector>
using namespace std;
static constexpr int BASE=1286;
vector<vector<int>> arrays(const string&s,const string&name){
  vector<vector<int>> ans; regex pattern("\\\""+name+"\\\"[[:space:]]*:[[:space:]]*\\[([^\\]]*)\\]");
  for(sregex_iterator it(s.begin(),s.end(),pattern),end;it!=end;++it){
    string body=(*it)[1];regex numbers("-?[0-9]+");vector<int> v;
    for(sregex_iterator jt(body.begin(),body.end(),numbers);jt!=end;++jt)v.push_back(stoi((*jt).str()));
    ans.push_back(move(v));
  }
  return ans;
}
vector<int> fields(const string&s,const string&name){
  vector<int> ans;regex pattern("\\\""+name+"\\\"[[:space:]]*:[[:space:]]*([0-9]+)");
  for(sregex_iterator it(s.begin(),s.end(),pattern),end;it!=end;++it)ans.push_back(stoi((*it)[1]));
  return ans;
}
vector<int> tmpl(const vector<int>&B,const vector<int>&C,int gap){
  vector<int> out;out.reserve(2*(B.size()+gap)+C.size());
  out.insert(out.end(),B.begin(),B.end());
  out.insert(out.end(),gap,BASE-1);out.insert(out.end(),C.begin(),C.end());
  out.insert(out.end(),gap,BASE-1);
  out.insert(out.end(),B.rbegin(),B.rend());
  return out;
}
vector<int> number_from_pairs(const vector<int>&P){
  int n=P.size();assert(n>0);vector<int>d(n,0);
  for(int i=0;i<n/2;i++){
    int sum=P[i];assert(P[n-i-1]==sum && sum>=0 && sum<=2*BASE-2);
    int hi=min(sum,BASE-1);int lo=sum-hi;
    d[i]=lo;d[n-i-1]=hi;
  }
  if(n&1){assert(P[n/2]%2==0);d[n/2]=P[n/2]/2;}
  assert(d.back()>0);
  return d;
}
int main(int argc,char**argv){
  if(argc<2){cerr<<"usage: replay1286 DATA [STEPS]\n";return 2;}
  ifstream in(argv[1]);if(!in){cerr<<"missing input\n";return 2;}
  string src((istreambuf_iterator<char>(in)),istreambuf_iterator<char>());
  auto B=arrays(src,"B"),C=arrays(src,"C"); auto gain=fields(src,"cycle_band_gain");
  auto U=fields(src,"u"),V=fields(src,"v"),G=fields(src,"gamma"),initial=fields(src,"initial_band");
  assert(B.size()==4 && C.size()==4 && U.size()==4 && V.size()==4 && G.size()==4);
  assert(initial.size()==1 && gain.size()==1 && gain[0]==1);
  int steps=argc>2?stoi(argv[2]):20000;
  int gap=initial[0];vector<int> d=number_from_pairs(tmpl(B[0],C[0],gap));
  for(int t=0;t<steps;t++){
    int phase=t%4;
    vector<int> expected=tmpl(B[phase],C[phase],gap);
    if(d.size()!=expected.size()){cerr<<"LENGTH FAIL at step "<<t<<"\n";return 3;}
    bool is_pal=true;
    for(size_t i=0;i<d.size();i++){
      if(d[i]+d[d.size()-1-i]!=expected[i]){cerr<<"PAIR FAIL step="<<t<<" index="<<i<<"\n";return 4;}
      if(d[i]!=d[d.size()-1-i])is_pal=false;
    }
    if(is_pal){cerr<<"PALINDROME at step "<<t<<"\n";return 5;}
    vector<int> next;next.reserve(d.size()+1);int carry=0;
    for(size_t i=0;i<d.size();i++){
      int s=d[i]+d[d.size()-1-i]+carry;
      next.push_back(s%BASE);carry=s/BASE;
    }
    if(carry)next.push_back(carry);
    while(next.size()>1 && next.back()==0)next.pop_back();
    d.swap(next);
    gap+=U[phase]+V[phase]-G[phase];
    if(gap<initial[0]-1){cerr<<"BAND UNDERFLOW\n";return 6;}
  }
  cout<<"PASS: "<<steps<<" independent ordinary digit-list base1286 reverse-add steps; "
      <<"all full pair words match cycle and none is palindromic; final digits="<<d.size()<<" gap="<<gap<<"\n";
}
