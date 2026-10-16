#define main rle_search_main
#include "rle_phase_search.cpp"
#undef main
#include <functional>
int main(int argc,char**argv){
  int M=argc>1?stoi(argv[1]):256,H=argc>2?stoi(argv[2]):400;
  string path=argc>3?argv[3]:"multiband_candidates.jsonl";
  ofstream f(path);long long seeds=0,steps=0,pals=0,repeats=0,three=0;
  auto start=chrono::steady_clock::now();
  vector<int> widths={1,2,3,4,5,6,7,8,9,10,12,14,18,24,32,M};
  vector<int> small={2,5,7,M};
  sort(widths.begin(),widths.end());widths.erase(unique(widths.begin(),widths.end()),widths.end());
  sort(small.begin(),small.end());small.erase(unique(small.begin(),small.end()),small.end());
  for(int R=1;R<=5;R++){
    auto &choices=R<=3?widths:small;
    vector<int>w(R);
    function<void(int)> recur=[&](int level){
      if(level<R){for(int n:choices){w[level]=n;recur(level+1);}return;}
      if(find(w.begin(),w.end(),M)==w.end())return;
      Word half={{9,2}};
      for(int i=0;i<R-1;i++){half.emplace_back(i%2?0:18,w[i]);half.emplace_back(9,2);}
      Word q=half;q.emplace_back((R-1)%2?0:18,w.back());auto rr=rev(half);q.insert(q.end(),rr.begin(),rr.end());q=canonical(q);Word initial=q;
      ++seeds;unordered_map<string,Seen>seen;
      for(int t=0;t<=H;t++){
        auto k=key(q);auto n=lens(q);auto it=seen.find(k);
        if(it!=seen.end()){
          auto &old=it->second;int p=t-old.t;auto delta=diff(n,old.n);++repeats;
          bool valid=p==old.prevperiod&&delta==old.delta;
          if(valid)++three;
          f<<"{\"widths\":[";for(int i=0;i<R;i++){if(i)f<<',';f<<w[i];}
          f<<"],\"M\":"<<M<<",\"period\":"<<p<<",\"times\":["<<old.t<<','<<t<<"],\"three_matches\":"<<(valid?"true":"false")<<",\"delta\":[";
          for(int i=0;i<int(delta.size());i++){if(i)f<<',';f<<delta[i];}
          f<<"],\"initial\":";dump(f,initial);f<<",\"last\":";dump(f,q);f<<"}\n";
          if(valid)break;
          old={t,n,p,delta};
        }else seen.emplace(k,Seen{t,n});
        if(t==H)break;
        auto[out,pal]=step(q);++steps;if(pal){++pals;break;}q=out;
      }
    };
    recur(0);
  }
  double sec=chrono::duration<double>(chrono::steady_clock::now()-start).count();
  cout<<"{\"status\":\"bounded multiple reservoir discovery only\",\"M\":"<<M<<",\"horizon\":"<<H<<",\"width_alphabet\":[";
  for(int i=0;i<int(widths.size());i++){if(i)cout<<',';cout<<widths[i];}
  cout<<"],\"half_domain_counts\":[1,2,3,4,5],\"last_two_count_alphabet\":[";
  for(int i=0;i<int(small.size());i++){if(i)cout<<',';cout<<small[i];}
  cout<<"],\"seeds\":"<<seeds<<",\"steps\":"<<steps<<",\"palindrome_outputs\":"<<pals<<",\"skeleton_repeats\":"<<repeats<<",\"three_phase_matches\":"<<three<<",\"seconds\":"<<sec<<"}\n";
}
