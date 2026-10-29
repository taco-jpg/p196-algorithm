// Independent little-endian digit-list reverse-and-add, no pairword code.
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
int main(int argc,char**argv){
  if(argc<3){std::cerr<<"usage: replay_int SEED_FILE STEPS\n";return 2;}
  std::ifstream file(argv[1]);std::string seed;file>>seed;
  if(seed.empty() || seed[0]=='0'){std::cerr<<"bad seed\n";return 2;}
  std::vector<unsigned char> a;
  for(auto it=seed.rbegin();it!=seed.rend();++it){if(*it<'0'||*it>'9')return 2;a.push_back(*it-'0');}
  const int steps=std::stoi(argv[2]);
  uint64_t checks=0,overflows=0;
  for(int t=1;t<=steps;++t){
    const size_t n=a.size();std::vector<unsigned char>b;b.reserve(n+1);int carry=0;
    for(size_t i=0;i<n;++i){int s=a[i]+a[n-1-i]+carry;b.push_back(s%10);carry=s/10;}
    if(carry){b.push_back(carry);++overflows;}
    bool pal=true;for(size_t i=0;i<b.size()/2;++i){if(b[i]!=b[b.size()-1-i]){pal=false;break;}}
    if(pal){std::cout<<"PAL_AT_STEP "<<t<<"\n";return 1;}
    a.swap(b);++checks;
    if(t==1 || t==232 || t==1000 || t==10000 || t==steps){
      uint64_t hash=14695981039346656037ULL;
      for(unsigned char d:a){hash^=d;hash*=1099511628211ULL;}
      std::cout<<"step="<<t<<" digits="<<a.size()<<" fnv64="<<hash<<"\n";
    }
  }
  std::cout<<"NO_PALINDROME_OBSERVED steps="<<checks<<" growth="<<overflows<<"\n";
}
