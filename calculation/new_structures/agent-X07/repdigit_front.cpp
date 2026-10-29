// X07: exact two-ended decimal frontier for repdigits plus a short perturbation.
// Compile: g++ -O3 -std=c++17 repdigit_front.cpp -lgmpxx -lgmp -o repdigit_front
// Run: ./repdigit_front 9 -1 13000 20000
// The symbolic half-line is independent of n; the GMP and schoolbook replays
// are independent entire-integer computations, checked at every iteration.
#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using Digits=vector<uint8_t>;
struct Front {Digits left,right; int bulk; int t=0; int over=0;};

Front start(int a,int k,int cap=6) {
  if(a<1||a>9||k < -9999||k>9999)throw runtime_error("parameter range");
  int64_t v=0;for(int i=0;i<cap;i++)v=10*v+a;
  v+=k;if(v<0||v>=1000000)throw runtime_error("cap outside six digits");
  Front f;f.bulk=a;
  for(int i=0;i<cap;i++){f.left.push_back(v%10);v/=10;f.right.push_back(a);}
  return f;
}

bool possible_palindrome(const Front&f) {
  int m=f.left.size();
  for(int i=0;i<m;i++)if(f.left[i]!=f.right[m-1-i])return false;
  return true;
}

// Sound for arbitrary central length L>=2, in least-significant-first digits.
// Returns the actual leading overflow gamma of N+rev(N) in {0,1}.
int step(Front&f) {
  const int m=f.left.size();
  Digits low, high;low.reserve(m+1);high.reserve(m+1);
  int carry=0;
  for(int i=0;i<m;i++){
    int z=f.left[i]+f.right[m-1-i]+carry;
    low.push_back(z%10);carry=z/10;
  }
  // The first bulk cell may see the boundary carry; all later cells
  // see fixed carry floor(2*u/10), since 2*u is never 9.
  const int first=(2*f.bulk+carry)%10;
  carry=(2*f.bulk+carry)/10;
  const int fixed=2*f.bulk/10;
  if(carry!=fixed)throw runtime_error("nonabsorbing bulk");
  const int next_bulk=(2*f.bulk+fixed)%10;
  for(int i=0;i<m;i++){
    int z=f.right[i]+f.left[m-1-i]+carry;
    high.push_back(z%10);carry=z/10;
  }
  const int gamma=carry;
  low.push_back(first);
  if(gamma)high.push_back(1);
  else high.insert(high.begin(),next_bulk);
  // Canonical reduction: remove matched bulk digits from both inner faces.
  int trim=0;
  while(trim<(int)low.size()&&low[low.size()-1-trim]==next_bulk&&high[trim]==next_bulk)trim++;
  if(trim){low.resize(low.size()-trim);high.erase(high.begin(),high.begin()+trim);}
  f.left.swap(low);f.right.swap(high);f.bulk=next_bulk;
  f.over+=gamma;f.t++;
  return gamma;
}

Digits make_digits(int a,int k,int n){
  Digits d(n,a);int64_t c=k;
  for(int i=0;c!=0;i++){
    if(i>=n)throw runtime_error("perturbation changed seed length");
    int64_t v=d[i]+c,r=(v%10+10)%10;c=(v-r)/10;d[i]=r;
  }
  if(d.back()==0)throw runtime_error("leading zero");return d;
}

Digits schoolbook(const Digits&d){
  Digits result;result.reserve(d.size()+1);int c=0,n=d.size();
  for(int i=0;i<n;i++){int z=d[i]+d[n-1-i]+c;result.push_back(z%10);c=z/10;}
  if(c)result.push_back(c);return result;
}
string decimal(const Digits&d){string out;out.reserve(d.size());for(auto i=d.rbegin();i!=d.rend();i++)out.push_back('0'+*i);return out;}
uint64_t fnv(uint64_t h,uint64_t v){for(int j=0;j<8;j++){h^=(v>>(8*j))&255;h*=1099511628211ULL;}return h;}

int main(int argc,char**argv)try{
  const int a=argc>1?atoi(argv[1]):9, k=argc>2?atoi(argv[2]):-1;
  const int n0=argc>3?atoi(argv[3]):13000, H=argc>4?atoi(argv[4]):20000;
  if(n0<0||H<0||(n0!=0&&n0<20))throw runtime_error("invalid n0/H");
  // n0=0 requests an exact symbolic run valid for every sufficiently long n.
  if(n0==0){
    Front g=start(a,k);int maxNeeded=0,maxM=0,maxOdd=-1,maxWitness=-1;
    for(int t=0;t<=H;t++){
      int m=g.left.size(),firstOdd=0,firstDiff=0;
      while(firstOdd<m && ((g.left[firstOdd]+g.right[m-1-firstOdd])%2==0))firstOdd++;
      while(firstDiff<m && g.left[firstDiff]==g.right[m-1-firstDiff])firstDiff++;
      if(firstDiff==m){cout<<"SYMBOLIC PALINDROME t="<<t<<"\n";return 3;}
      maxNeeded=max(maxNeeded,2*m-g.over);maxM=max(maxM,m);
      maxWitness=max(maxWitness,firstDiff);
      if(firstOdd==m){cout<<"SYMBOLIC NO-ODD-COEFFICIENT t="<<t<<"\n";return 4;}
      maxOdd=max(maxOdd,firstOdd);
      if(t!=H)step(g);
    }
    cout<<"X07 SYMBOLIC PASS a="<<a<<" k="<<k<<" horizon="<<H
        <<" min_n_for_L_ge_2="<<maxNeeded+2<<" max_front="<<maxM
        <<" max_odd_index="<<maxOdd<<" max_mismatch_index="<<maxWitness
        <<" overflow_total="<<g.over<<" final_bulk="<<g.bulk<<"\n";
    return 0;
  }
  Front f=start(a,k);Digits d=make_digits(a,k,n0);
  mpz_class big(decimal(d),10);
  int minGap=INT32_MAX,maxM=0,maxNeeded=0,firstPal=-1,maxWitness=0,atMaxWitness=0;
  int witnessHist[11]={};
  uint64_t hash=14695981039346656037ULL;
  for(int t=0;t<=H;t++){
    const int len=d.size(),m=f.left.size(),gap=len-2*m;
    if(gap<2)throw runtime_error("fronts collide at t="+to_string(t));
    minGap=min(minGap,gap);maxM=max(maxM,m);
    maxNeeded=max(maxNeeded,2*m-f.over);
    if(t!=f.t||len!=n0+f.over)throw runtime_error("length/overflow mismatch");
    if(big.get_str()!=decimal(d))throw runtime_error("GMP vs schoolbook mismatch at t="+to_string(t));
    for(int i=0;i<m;i++){
      if(d[i]!=f.left[i]||d[len-m+i]!=f.right[i])
        throw runtime_error("front mismatch at t="+to_string(t));
    }
    for(int i=m;i<len-m;i++)if(d[i]!=f.bulk)throw runtime_error("bulk mismatch at t="+to_string(t));
    bool p=true;for(int i=0;i<len/2;i++)if(d[i]!=d[len-1-i]){p=false;break;}
    if(p!=possible_palindrome(f))throw runtime_error("palindrome criterion mismatch");
    if(p){firstPal=t;break;}
    int witness=0;while(witness<m&&f.left[witness]==f.right[m-1-witness])witness++;
    if(witness>maxWitness){maxWitness=witness;atMaxWitness=t;}
    witnessHist[min(witness,10)]++;
    hash=fnv(fnv(fnv(fnv(hash,len),m),f.bulk),witness);
    if(t==H)break;
    string reverse=big.get_str();std::reverse(reverse.begin(),reverse.end());
    big+=mpz_class(reverse,10);
    d=schoolbook(d);
    step(f);
    if(t==0 || (t+1)%5000==0)
      cerr<<"checkpoint t="<<t+1<<" m="<<f.left.size()<<" bulk="<<f.bulk<<" gap="<<(int)d.size()-2*(int)f.left.size()<<" over="<<f.over<<"\n";
  }
  cout<<"X07 "<<(firstPal<0?"PASS":"PALINDROME")<<" a="<<a<<" k="<<k<<" n0="<<n0
      <<" horizon="<<H<<" first_pal="<<firstPal<<" min_gap="<<minGap<<" max_front="<<maxM
      <<" max_2m_minus_overflow="<<maxNeeded<<" final_digits="<<d.size()
      <<" overflow_total="<<f.over<<" max_witness="<<maxWitness<<" witness_at_t="<<atMaxWitness<<" FNV64="<<hex<<hash<<dec<<"\n";
  cout<<"WITNESS_HIST_0_TO_9_AND_GE10:";for(int v:witnessHist)cout<<" "<<v;cout<<"\n";
  return firstPal<0?0:3;
}catch(const exception&e){cerr<<"ERROR: "<<e.what()<<"\n";return 2;}
