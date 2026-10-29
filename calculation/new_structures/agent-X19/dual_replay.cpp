// Agent X19: four-corner actual base-10 digit and independent decimal-string arithmetic.
// Compile: g++ -O3 -std=c++17 dual_replay.cpp -o dual_replay
// Usage: ./dual_replay <Q> <R> <steps>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using Dig=vector<uint8_t>;
string seed_text(int q,int r){return "12"+string(2*q,'9')+"34"+string(2*r,'9')+"56"+string(2*q,'9')+"78";}
Dig seed(int q,int r){string s=seed_text(q,r); Dig a; a.reserve(s.size());for(auto i=s.rbegin();i!=s.rend();++i)a.push_back(*i-'0');return a;}
void step(Dig& a){const int n=a.size();int c=0;Dig b;b.reserve(n+1);for(int i=0;i<n;i++){int v=a[i]+a[n-1-i]+c;b.push_back(v%10);c=v/10;}if(c)b.push_back(c);a.swap(b);}
// Independent implementation, MSB-first strings, not sharing normalization or carries with step().
void string_step(string &s){string reverse_s=s;reverse(reverse_s.begin(),reverse_s.end()); // rev(n), strip leading zeros
 size_t k=reverse_s.find_first_not_of('0');if(k==string::npos)reverse_s="0";else reverse_s.erase(0,k);
 int i=(int)s.size()-1,j=(int)reverse_s.size()-1,c=0;string out;out.reserve(max(i,j)+2);
 while(i>=0||j>=0||c){int u=c;if(i>=0)u+=s[i--]-'0';if(j>=0)u+=reverse_s[j--]-'0';out.push_back('0'+u%10);c=u/10;}reverse(out.begin(),out.end());s.swap(out);
}
bool eq(const Dig &a,const string &s){if(a.size()!=s.size())return false;for(size_t i=0;i<a.size();i++)if(a[i] !=s[s.size()-1-i]-'0')return false;return true;}
bool pal(const Dig&a){for(size_t i=0,j=a.size()-1;i<j;i++,j--)if(a[i]!=a[j])return false;return true;}
// Deleting exactly 'count' isolated base-100 99 blocks in B yields A, at any locations.
// State k means B has consumed k extra blocks; independent of arithmetic and seed construction.
bool insertion(const Dig&A,const Dig&B,int count){if(B.size()!=A.size()+size_t(2*count))return false;
 const int n=(A.size()+1)/2,m=n+count;uint8_t ok[3]={1,0,0};
 for(int i=0;i<m;i++){
   uint8_t next[3]={0,0,0};int bi=B[2*i]+(2*i+1<(int)B.size()?10*B[2*i+1]:0);
   for(int k=0;k<=count;k++)if(ok[k]){
     if(k<count&&bi==99)next[k+1]=1;
     int j=i-k;
     if(j<n){int ai=A[2*j]+(2*j+1<(int)A.size()?10*A[2*j+1]:0);if(ai==bi)next[k]=1;}
   }
   for(int k=0;k<=count;k++)ok[k]=next[k];
 }
 return ok[count];
}

Dig pairword(const Dig&a){Dig p(a.size());for(size_t i=0,n=a.size();i<n;i++)p[i]=a[i]+a[n-1-i];return p;}
// Exact block deletion on symmetric coefficient words (one cell = coefficient 0..18).
// Outer Q insertion must introduce four 18-cells; centre R insertion two 18-cells.
bool pair_insertion(const Dig&A,const Dig&B,int count){
 if(B.size()!=A.size()+size_t(count))return false;
 size_t j=0;int omitted=0;
 for(uint8_t v:B){
   if(j<A.size()&&v==A[j]){j++;continue;}
   if(v==18&&omitted<count){omitted++;continue;}
   return false;
 }
 return j==A.size()&&omitted==count;
}

uint64_t digest(uint64_t h,const Dig&a){for(uint8_t c:a){h^=c+1;h*=1099511628211ULL;}return h;}
int main(int argc,char**argv){if(argc!=4){cerr<<"usage Q R steps\n";return 2;}int q=atoi(argv[1]),r=atoi(argv[2]),tmax=atoi(argv[3]);if(q<1||r<1||tmax<1)return 2;
 Dig a[4]={seed(q,r),seed(q+1,r),seed(q,r+1),seed(q+1,r+1)};
 string independent=seed_text(q,r); uint64_t h=1469598103934665603ULL; int minOdd=1000000000;
 for(int t=0;t<=tmax;t++){
   if(!eq(a[0],independent)){cerr<<"INDEPENDENT_ARITHMETIC_MISMATCH t="<<t<<"\n";return 4;}
   for(int k=0;k<4;k++){
      if(pal(a[k])){cerr<<"PAL t="<<t<<" k="<<k<<"\n";return 5;}
      int odd=0;const auto &v=a[k];for(size_t i=0,n=v.size();i<n/2;i++)odd+=((v[i]+v[n-1-i])&1);
      minOdd=min(minOdd,odd);
    }
   // Two independent commuting 99-band increments, four edges of a parameter square.
   if(!insertion(a[0],a[1],2)||!insertion(a[2],a[3],2) || !insertion(a[0],a[2],1)||!insertion(a[1],a[3],1)){
     cerr<<"SQUARE_INSERTION_BREAK t="<<t<<" lens="<<a[0].size()<<","<<a[1].size()<<","<<a[2].size()<<","<<a[3].size()<<"\n";return 6;
   }
   Dig pw[4]={pairword(a[0]),pairword(a[1]),pairword(a[2]),pairword(a[3])};
   if(!pair_insertion(pw[0],pw[1],4)||!pair_insertion(pw[2],pw[3],4)||!pair_insertion(pw[0],pw[2],2)||!pair_insertion(pw[1],pw[3],2)){
       cerr<<"PAIRWORD_18_INSERTION_BREAK t="<<t<<"\n";return 7;
   }
   h=digest(h,a[0]); if(t%2000==0)cerr<<"CHECK t="<<t<<" len="<<a[0].size()<<" digest="<<hex<<h<<dec<<"\n";
   if(t<tmax){for(auto&x:a)step(x);string_step(independent);}
 }
 cout<<"PASS Q="<<q<<" R="<<r<<" steps="<<tmax<<" all_four_nonpalindromic=true all_four_digit_and_pairword_square_edges_exact=true independent_string_check_every_step=true digits_final="<<a[0].size()<<" fnv64="<<hex<<h<<dec<<" min_odd_pair_coefficients="<<minOdd<<"\n";return 0;
}
