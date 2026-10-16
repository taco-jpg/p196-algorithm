// Exact finite discovery of repeated run skeletons. No all-time claim.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
using Run=pair<int,int>;
using Word=vector<Run>;
void append(Word &w,int x,int n) {
  if(n<=0)return;
  if(!w.empty()&&w.back().first==x)w.back().second+=n;
  else w.emplace_back(x,n);
}
Word canonical(const Word&w){Word z;for(auto[x,n]:w)append(z,x,n);return z;}
Word rev(const Word&w){return Word(w.rbegin(),w.rend());}
pair<Word,bool> step(const Word&q) {
  Word d; int c=0;
  for(auto[x,n]:q){int v=x+c;append(d,v%10,1);c=v/10;append(d,(x+c)%10,n-1);}
  if(c)append(d,1,1);
  if(d==rev(d))return {Word(),true};
  Word r=rev(d),out;int i=0,j=0,ni=d[0].second,nj=r[0].second;
  while(i<int(d.size())) {
    int n=min(ni,nj);append(out,d[i].first+r[j].first,n);
    ni-=n;nj-=n;
    if(!ni&&++i<int(d.size()))ni=d[i].second;
    if(!nj&&++j<int(r.size()))nj=r[j].second;
  }
  return {out,false};
}
string key(const Word&q){string s;for(auto[x,n]:q)s.push_back(char(x));return s;}
vector<int> lens(const Word&q){vector<int>v;for(auto[x,n]:q)v.push_back(n);return v;}
vector<int> diff(const vector<int>&a,const vector<int>&b){vector<int>v;for(int i=0;i<int(a.size());i++)v.push_back(a[i]-b[i]);return v;}
void dump(ostream&f,const Word&q){f<<'[';bool first=true;for(auto[x,n]:q){if(!first)f<<',';first=false;f<<'['<<x<<','<<n<<']';}f<<']';}
struct Seen{int t;vector<int>n;int prevperiod=-1;vector<int>delta;};
int main(int argc,char**argv){
  int M=argc>1?stoi(argv[1]):256,H=argc>2?stoi(argv[2]):160,mode=argc>3?stoi(argv[3]):0;
  string path=argc>4?argv[4]:"rle_phase_search.jsonl";
  ofstream f(path);long long seeds=0,steps=0,pals=0,repeats=0,three=0;
  auto start=chrono::steady_clock::now();
  for(int a=1;a<=18;a++)for(int b=0;b<=18;b++)for(int x=0;x<=18;x++)
  for(int z=0;z<=(mode?18:0);z++){
    Word half={{a,1}};if(mode)half.emplace_back(z,1);half.emplace_back(x,M);half.emplace_back(b,1);
    Word q=half;Word rr=rev(half);q.insert(q.end(),rr.begin(),rr.end());q=canonical(q);Word initial=q;
    ++seeds;unordered_map<string,Seen> seen;
    for(int t=0;t<=H;t++){
      auto k=key(q);auto n=lens(q);auto it=seen.find(k);
      if(it!=seen.end()){
        auto &old=it->second;int p=t-old.t;auto delta=diff(n,old.n);++repeats;
        bool valid=false,positive=false,negative=false;
        for(int d:delta){positive|=d>0;negative|=d<0;}
        valid=(p==old.prevperiod&&delta==old.delta);
        {
          if(valid)++three;f<<"{\"seed\":["<<a<<','<<b<<','<<x<<','<<z<<"],\"M\":"<<M<<",\"period\":"<<p<<",\"times\":["<<old.t<<','<<t<<"],\"three_matches\":"<<(valid?"true":"false")<<",\"mixed_drift\":"<<(positive&&negative?"true":"false")<<",\"delta\":[";
          for(int i=0;i<int(delta.size());i++){if(i)f<<',';f<<delta[i];}
          f<<"],\"initial\":";dump(f,initial);f<<",\"last\":";dump(f,q);f<<"}\n";
          if(valid)break;
        }
        old={t,n,p,delta};
      }else seen.emplace(k,Seen{t,n});
      if(t==H)break;
      auto[out,pal]=step(q);++steps;if(pal){++pals;break;}q=out;
    }
  }
  double sec=chrono::duration<double>(chrono::steady_clock::now()-start).count();
  cout<<"{\"status\":\"bounded RLE discovery only\",\"M\":"<<M<<",\"horizon\":"<<H<<",\"mode\":"<<mode<<",\"seeds\":"<<seeds<<",\"steps\":"<<steps<<",\"palindrome_outputs\":"<<pals<<",\"skeleton_repeats\":"<<repeats<<",\"three_phase_matches\":"<<three<<",\"seconds\":"<<sec<<"}\n";
  return 0;
}
