// Independent exhaustive inverse-pair audit using literal decimal integers.
// Compile: g++ -O2 -std=c++17 root_inverse_audit.cpp -o /tmp/root_inverse_audit
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>
using U=std::uint64_t;
U reverse10(U n){U r=0;while(n){r=10*r+n%10;n/=10;}return r;}
U realize(const std::vector<int>& p,int center){
 U n=0;for(int x:p)n=10*n+std::min(x,9);
 if(center>=0)n=10*n+center;
 for(auto i=p.rbegin();i!=p.rend();++i)n=10*n+std::max(*i-9,0);
 return n;
}
int main(){
 std::array<std::array<int,5>,2> target={{{5,0,5,13,17},{2,10,2,6,18}}};
 std::array<unsigned,2> hits={0,0}; U checked=0;
 std::cout<<"{\"matches\":[";bool comma=false;
 for(int L:{9,10}){
  int m=L/2,limit=1;for(int i=0;i<m;++i)limit*=19;
  for(int z=0;z<limit;++z){
   int k=z;std::vector<int> p(m);for(int&i:p){i=k%19;k/=19;}if(!p[0])continue;
   for(int mid=0;mid<(L%2?10:1);++mid){
    U n=realize(p,L%2?mid:-1),out=n+reverse10(n);++checked;
    std::string s=std::to_string(out);if(s.size()!=10)continue;
    std::array<int,5> q;for(int i=0;i<5;++i)q[i]=s[i]+s[9-i]-2*'0';
    for(int t=0;t<2;++t)if(q==target[t]){
     ++hits[t];if(comma)std::cout<<",";comma=true;
     std::cout<<"{\"target\":"<<t<<",\"predecessor_representative\":"<<n<<",\"actual_image\":"<<out<<",\"input_pair_word\":[";
     for(int i=0;i<m;++i){if(i)std::cout<<",";std::cout<<p[i];}
     std::cout<<"],\"input_center\":"<<(L%2?2*mid:-1)<<",\"actual_image_is_palindrome\":"<<(out==reverse10(out)?"true":"false")<<"}";
    }
   }
  }
 }
 std::cout<<"],\"canonical_pair_words_checked\":"<<checked<<",\"predecessor_counts\":["<<hits[0]<<","<<hits[1]<<"],\"status\":\""<<(hits[0]==1&&hits[1]==1?"PASS":"FAIL")<<"\"}\n";
 return hits[0]==1&&hits[1]==1?0:1;
}
