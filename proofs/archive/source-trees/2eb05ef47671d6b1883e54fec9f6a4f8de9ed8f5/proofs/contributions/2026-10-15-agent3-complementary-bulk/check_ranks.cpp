// Independent literal-integer checker for outer_scan.cpp rank certificates.
// It does NOT use the quotient normalization formulas or scanner transition.
// Source pair word: B c^2 (18-c)^4 c^2 reverse(B), A=C=empty, g=h=2.
// For L<=5 its width is <=18; value <=2*(10^18-1) fits uint64_t.
// Build: g++ -std=c++17 -O2 -Wall -Wextra -pedantic check_ranks.cpp -o check_ranks
// Run: ./check_ranks 5 ranks-L5.bin
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <iterator>
#include <stdexcept>
#include <string>
#include <vector>

int main(int argc, char** argv) { try {
  if(argc!=3) throw std::runtime_error("Usage: check_ranks L ranks.bin");
  int L=std::stoi(argv[1]);
  if(L<0 || L>5) throw std::runtime_error("Literal uint64 checker supports L=0..5");
  std::array<uint32_t,8> pow19{}, offset{}; pow19[0]=1;
  for(int n=1;n<=L+1;++n){pow19[n]=19*pow19[n-1];offset[n]=offset[n-1]+pow19[n-1];}
  uint32_t stride=offset[L+1], slots=8*stride;
  std::ifstream input(argv[2],std::ios::binary);
  if(!input) throw std::runtime_error("Cannot read rank file");
  std::vector<uint8_t> rank((std::istreambuf_iterator<char>(input)),{});
  if(rank.size()!=slots) throw std::runtime_error("Wrong byte count");
  std::array<uint64_t,254> hist{}; uint64_t checked=0, invalid=0; int maximum=0;
  for(uint32_t id=0;id<slots;++id){
    int c=2*(id/stride+1);uint32_t wordcode=id%stride;int n=0;
    while(n<L && wordcode>=offset[n+1])++n;
    wordcode-=offset[n];std::array<int,6>B{};
    for(int i=0;i<n;++i){B[i]=wordcode%19;wordcode/=19;}
    if(n>0 && (B[0]==0 || B[n-1]==c)){
      if(rank[id]!=255)throw std::runtime_error("Invalid code lacks 255 sentinel");
      ++invalid;continue;
    }
    if(rank[id]==0 || rank[id]>=254)throw std::runtime_error("Invalid rank for canonical state");
    std::array<int,20> q{}; int width=0;
    for(int i=0;i<n;++i)q[width++]=B[i];
    q[width++]=c;q[width++]=c;
    for(int i=0;i<4;++i)q[width++]=18-c;
    q[width++]=c;q[width++]=c;
    for(int i=n-1;i>=0;--i)q[width++]=B[i];
    uint64_t value=0;
    for(int i=width-1;i>=0;--i)value=10*value+static_cast<uint64_t>(q[i]);
    std::array<int,20> digits{};int digitslen=0;
    do{digits[digitslen++]=value%10;value/=10;}while(value);
    if(digitslen!=width && digitslen!=width+1)throw std::runtime_error("Unexpected canonical width");
    std::array<int,7> next{};int nextlen=n+1;
    for(int i=0;i<nextlen;++i)next[i]=digits[i]+digits[digitslen-1-i];
    int nextphase=(2*c)%18; // Different expression for F on the eight even phases.
    while(nextlen>0 && next[nextlen-1]==nextphase)--nextlen;
    unsigned targetrank=0;
    if(nextlen<=L){
      if(nextphase<2 || nextphase>16 || nextphase%2)throw std::runtime_error("Bad target phase");
      if(nextlen && (next[0]==0 || next[nextlen-1]==nextphase))throw std::runtime_error("Bad target interface");
      uint32_t target=(nextphase/2-1)*stride+offset[nextlen];
      for(int i=0;i<nextlen;++i){if(next[i]<0 || next[i]>18)throw std::runtime_error("Bad coefficient");target+=next[i]*pow19[i];}
      targetrank=rank.at(target);
      if(targetrank==0 || targetrank>=254)throw std::runtime_error("Target rank missing");
    }
    if(rank[id]!=targetrank+1)throw std::runtime_error("Literal-integer rank equation failed at code "+std::to_string(id));
    ++hist[rank[id]];++checked;if(rank[id]>maximum)maximum=rank[id];
  }
  std::cout<<"{\"bound\":"<<L<<",\"checked_states\":"<<checked<<",\"invalid_codes\":"<<invalid
           <<",\"max_exit_time\":"<<maximum<<",\"literal_integer_rank_check\":true,\"histogram\":{";
  for(int r=1;r<=maximum;++r){if(r>1)std::cout<<",";std::cout<<"\""<<r<<"\":"<<hist[r];}
  std::cout<<"}}\n";
} catch(const std::exception& e){std::cerr<<e.what()<<"\n";return 1;}}
