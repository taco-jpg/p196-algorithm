#define main rle_search_main
#include "rle_phase_search.cpp"
#undef main
bool matchS(const Word&q,int &m,int &n){
  vector<int>digits={9,18,9,0,9,18,9,0,9,18,9};
  if(q.size()!=digits.size())return false;
  for(int i=0;i<int(q.size());i++)if(q[i].first!=digits[i])return false;
  for(int i:{0,2,4,6,8,10})if(q[i].second!=2)return false;
  if(q[1].second!=5||q[9].second!=5)return false;
  m=q[5].second;n=q[3].second;
  return m>=8&&n>=7;
}
bool matchR(const Word&q,int &m,int &n){
  vector<int>digits={18,0,1,9,17,18,17,9,1,0,18};
  if(q.size()!=digits.size())return false;
  for(int i=0;i<int(q.size());i++)if(q[i].first!=digits[i])return false;
  if(q[0].second!=14||q[10].second!=14||q[3].second!=7||q[7].second!=7)return false;
  for(int i:{2,4,6,8})if(q[i].second!=1)return false;
  m=q[5].second+7;n=q[1].second+6;
  return m>=8&&n>=7;
}
int main(int argc,char**argv){
  int Max=argc>1?stoi(argv[1]):64,factor=argc>2?stoi(argv[2]):16;
  string path=argc>3?argv[3]:"regeneration_returns.jsonl";
  ofstream f(path);long long seeds=0,steps=0,pals=0,returns=0,ternary=0;
  long long olddeath=0,recreated=0;int death_min=1000000,death_max=0;
  auto start=chrono::steady_clock::now();
  for(int M=8;M<=Max;M++)for(int N=7;N<=Max;N++){
    Word q={{18,14},{0,N-6},{1,1},{9,7},{17,1},{18,M-7},{17,1},{9,7},{1,1},{0,N-6},{18,14}};
    ++seeds;bool inherited=true,newcentral=false;int death=-1;
    for(int t=14;t<=factor*(M+N)+64;t++){
      auto[out,pal]=step(q);++steps;if(pal){++pals;f<<"{\"M\":"<<M<<",\"N\":"<<N<<",\"palindrome_at\":"<<t<<",\"inherited_death\":"<<death<<"}\n";break;}q=out;
      if(inherited&&q[q.size()/2].first!=18){inherited=false;death=t;++olddeath;death_min=min(death_min,t);death_max=max(death_max,t);}
      if(!inherited&&!newcentral&&q[q.size()/2].first==18){newcentral=true;++recreated;}
      int m,n;bool s=matchS(q,m,n),r=!s&&matchR(q,m,n);
      if(s||r){++returns;f<<"{\"M\":"<<M<<",\"N\":"<<N<<",\"time\":"<<t<<",\"phase\":\""<<(s?"S":"R")<<"\",\"next_M\":"<<m<<",\"next_N\":"<<n<<",\"inherited_death\":"<<death<<"}\n";}
      bool tri=!inherited&&q.size()>1;
      for(auto[x,n]:q)if(x!=0&&x!=9&&x!=18)tri=false;
      if(tri){++ternary;f<<"{\"M\":"<<M<<",\"N\":"<<N<<",\"time\":"<<t<<",\"event\":\"three-symbol state after inherited death\",\"q\":";dump(f,q);f<<"}\n";}
    }
  }
  double sec=chrono::duration<double>(chrono::steady_clock::now()-start).count();
  cout<<"{\"status\":\"bounded variable-time regeneration return search only\",\"M_range\":[8,"<<Max<<"],\"N_range\":[7,"<<Max<<"],\"initial_step\":13,\"last_step\":\""<<factor<<"(M+N)+64\",\"seeds\":"<<seeds<<",\"steps\":"<<steps<<",\"palindrome_outputs\":"<<pals<<",\"returns_to_S_or_R\":"<<returns<<",\"three_symbol_states_after_death\":"<<ternary<<",\"inherited_center_deaths\":"<<olddeath<<",\"inherited_death_range\":["<<death_min<<','<<death_max<<"],\"new_center_18_after_death\":"<<recreated<<",\"seconds\":"<<sec<<"}\n";
}
