// agent-N30: centre-agnostic expanding-number, shrinking-certified-cone family.
// Build: c++ -O3 -std=c++17 cone_family.cpp -o cone_family
// Run:   ./cone_family 16000 20000 37 3
#include <iomanip>
#include <sstream>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

static uint64_t rng=UINT64_C(0x9a702f4ed37008c5);
uint64_t random_u64(){rng^=rng<<13;rng^=rng>>7;rng^=rng<<17;return rng;}

int main(int argc,char**argv){
  const int K=argc>1?atoi(argv[1]):24000;
  const int steps=argc>2?atoi(argv[2]):20000;
  const int m=argc>3?atoi(argv[3]):37;
  const char centre_digit=argc>4?argv[4][0]:'3';
  if(K<1||steps<1||m<1||centre_digit<'0'||centre_digit>'9') return 2;
  vector<unsigned char> low(K), high(K);
  for(int j=0;j<K;j++){
    uint64_t a=random_u64(),b=random_u64();
    low[j]=a%10; high[j]=b%10;
  }
  high[0]=1+(high[0]%9);
  // Actual integer seeded with arbitrary middle 3...3. The abstract proof
  // below does not read the middle and is valid for EVERY middle length >=1.
  string s;
  s.reserve(2*K+m);
  for(int j=0;j<K;j++)s.push_back('0'+high[j]);
  s.append(m,centre_digit);
  for(int j=K-1;j>=0;j--)s.push_back('0'+low[j]);
  // Independent arbitrary-precision oracle uses base-10^9 limbs, not digit carries.
  struct BigInt {
    static constexpr uint32_t base() { return 1000000000U; }
    vector<uint32_t> limbs;
    explicit BigInt(const string &s) {
      for(int end=(int)s.size();end>0;end-=9) {
        int beg=max(0,end-9);
        limbs.push_back((uint32_t)stoul(s.substr(beg,end-beg)));
      }
      while(limbs.size()>1 && limbs.back()==0)limbs.pop_back();
    }
    string str() const {
      string ans=to_string(limbs.back());
      for(int i=(int)limbs.size()-2;i>=0;i--) {
        string t=to_string(limbs[i]);ans+=string(9-t.size(),'0')+t;
      }
      return ans;
    }
    void add(const BigInt &r) {
      size_t n=max(limbs.size(),r.limbs.size());limbs.resize(n,0);
      uint64_t carry=0;
      for(size_t i=0;i<n;i++) {
        uint64_t a=limbs[i]+carry+(i<r.limbs.size()?r.limbs[i]:0);
        limbs[i]=a%base();carry=a/base();
      }
      if(carry)limbs.push_back((uint32_t)carry);
    }
  };
  BigInt N(s);
  vector<unsigned char> lnew,hnew,hi_digits,lo_digits;
  int k=K, min_k=K;
  long long discarded_reset9=0, overflow=0, palindrome=0;
  int max_reset9=0, min_witness=K, max_witness=0;
  cerr<<"Starting base-1e9 bigint + independently computed guaranteed exterior, seed digits="<<s.size()<<"\n";
  for(int t=0;t<=steps;t++){
    string exact=N.str();
    int n=exact.size();
    if(n<2*k+1){cerr<<"FAIL core length invariant at "<<t<<"\n";return 3;}
    if(equal(exact.begin(),exact.end(),exact.rbegin())){cerr<<"FAIL palindrome at "<<t<<"\n";return 4;}
    palindrome++;
    int witness=-1;
    for(int j=0;j<k;j++){
      if(exact[n-1-j]!='0'+low[j]||exact[j]!='0'+high[j]){
        cerr<<"FAIL cone mismatch at "<<t<<" position "<<j<<"\n";return 5;
      }
      if(witness<0 && low[j]!=high[j])witness=j;
    }
    if(witness<0){cerr<<"FAIL universal witness at "<<t<<"\n";return 6;}
    min_witness=min(min_witness,witness);
    max_witness=max(max_witness,witness);
    if(t==0||t==1||t==10||t==100||t==1000||t==5000||t==10000||t==15000||t==steps){
      cout<<"SAMPLE step="<<t<<" digits="<<n<<" guaranteed_pairs="<<k<<" first_witness="<<witness<<" total_discarded_9="<<discarded_reset9<<"\n";
    }
    if(t==steps)break;
    // Cone prediction uses only exterior low/high digits, no actual N or centre.
    int r=k;
    while(r>0 && int(low[r-1])+int(high[r-1])==9)r--;
    int skipped=k-r;
    discarded_reset9+=skipped;max_reset9=max(max_reset9,skipped);
    if(r<=0){cerr<<"FAIL cone exhausted at "<<t<<"\n";return 7;}
    lo_digits.assign(r,0);hi_digits.assign(r,0);
    int carry=0;
    for(int j=0;j<r;j++){
      int z=low[j]+high[j]+carry;
      lo_digits[j]=z%10;carry=z/10;
    }
    // From p[r-1]!=9 the carry leaving the rightmost inner marker is
    // independent of the unknown carry entering it (0 or 1).
    carry=(int(low[r-1])+int(high[r-1])>=10);
    for(int j=r-2;j>=0;j--){
      int z=low[j]+high[j]+carry;
      hi_digits[j]=z%10;carry=z/10;
    }
    int ov=carry;
    overflow+=ov;
    // Overflow adds a known leading digit, so the trusted width need NOT shrink.
    // Without overflow, the innermost high digit still depends on centre carry.
    int nk=ov?r:(r-1);
    if(nk==0){cerr<<"FAIL cone exhausted at "<<t<<"\n";return 7;}
    lnew.assign(nk,0);hnew.assign(nk,0);
    for(int j=0;j<nk;j++){
      lnew[j]=lo_digits[j];
      hnew[j]=ov?(j==0?1:hi_digits[j-1]):hi_digits[j];
    }
    low.swap(lnew);high.swap(hnew);k=nk;min_k=min(min_k,k);
    // Independent arithmetic oracle: decimal string reversal and GMP bigint.
    string sr=exact;
    reverse(sr.begin(),sr.end());
    BigInt R(sr);
    N.add(R);
  }
  cout<<"VERDICT PASS\n";
  cout<<"RESULT steps="<<steps<<" checked_integers="<<palindrome<<" k0="<<K
      <<" remaining_k="<<k<<" min_k="<<min_k<<" core_length="<<m<<" core_digit="<<centre_digit
      <<" overflow_count="<<overflow<<" 9_reset_discards="<<discarded_reset9
      <<" max_reset_run="<<max_reset9<<" max_first_witness="<<max_witness<<"\n";
}
