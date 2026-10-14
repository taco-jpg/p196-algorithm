#define main rle_search_main
#include "rle_phase_search.cpp"
#undef main
int main(int argc,char**argv){
  int Kmax=argc>1?stoi(argv[1]):128;
  int factor=argc>2?stoi(argv[2]):24;
  int M=argc>3?stoi(argv[3]):10000;
  string path=argc>4?argv[4]:"three_band_returns.jsonl";
  ofstream f(path);long long steps=0,pals=0,returns=0;
  auto start=chrono::steady_clock::now();
  for(int K=1;K<=Kmax;K++){
    Word q={{9,K},{18,M},{9,K}};
    for(int t=1;t<=factor*K+128;t++){
      auto[out,pal]=step(q);++steps;if(pal){++pals;f<<"{\"K\":"<<K<<",\"M\":"<<M<<",\"palindrome_at\":"<<t<<"}\n";break;}q=out;
      if(q.size()==3&&q[0].first==9&&q[1].first==18&&q[2].first==9){
        ++returns;f<<"{\"K\":"<<K<<",\"M\":"<<M<<",\"time\":"<<t<<",\"next_K\":"<<q[0].second<<",\"next_M\":"<<q[1].second<<"}\n";
      }
    }
  }
  double sec=chrono::duration<double>(chrono::steady_clock::now()-start).count();
  cout<<"{\"status\":\"bounded three-band discovery only\",\"K_max\":"<<Kmax<<",\"M\":"<<M<<",\"horizon_formula\":\""<<factor<<"K+128\",\"steps\":"<<steps<<",\"palindrome_outputs\":"<<pals<<",\"returns\":"<<returns<<",\"seconds\":"<<sec<<"}\n";
}
