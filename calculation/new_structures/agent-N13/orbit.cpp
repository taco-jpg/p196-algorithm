#include <bits/stdc++.h>
using namespace std;
// First spatial component of exact rec0 p8 SCC from repository p8_scc.txt.
static const vector<int> path={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const vector<int> cyc={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
static const int expected[8][8]={
 {17,8,17,8,17,8,17,8},
 {5,13,6,14,8,16,13,12},
 {0,5,11,8,17,16,14,9},
 {1,1,2,4,8,16,14,10},
 {13,5,10,3,6,14,10,6},
 {4,8,16,8,17,14,10,2},
 {14,9,18,16,13,12,6,7},
 {12,8,16,16,14,9,0,6}
};
int main(int argc,char**argv){
  int half= argc>1 ? stoi(argv[1]):1000;
  int steps=argc>2 ? stoi(argv[2]):1000;
  int reserve=argc>3 ? stoi(argv[3]):0; // central one-sided replacement radius
  int method=argc>4 ? stoi(argv[4]):0; // 0 and 1 are distinct digit lifts
  vector<uint8_t> p(2*half);
  for(int j=0;j<half;j++){
    int q = j<(int)path.size()? path[j] : cyc[(j-(int)path.size())%cyc.size()];
    if(reserve && j>=half-reserve) q=(j*7+11)%19;
    p[j]=p[2*half-1-j]=q;
  }
  vector<uint8_t> a(2*half);
  for(int j=0;j<half;j++){
    int q=p[j]; int lo;
    if(method==0) lo=min(9,q);
    else lo=max(0,q-9);
    a[j]=lo; a[a.size()-1-j]=q-lo;
  }
  // Save exact decimal seed for independent whole-bigint replay.
  {ofstream seed("seed.txt");for(int j=int(a.size())-1;j>=0;j--)seed<<int(a[j]);seed<<"\n";}
  // last digit must be nonzero: initial pair coefficient p[0]=17 so both constructions satisfy.
  int firstError=-1, firstEven=-1, firstPalindrome=-1, firstGamma=-1;
  int checked=0, parityFailures=0; int maxdigits=a.size();
  int minprefix=INT_MAX; int minTime=0; int longest=0;
  vector<pair<int,int>> sample;
  for(int t=0;t<=steps;t++){
    int n=a.size();maxdigits=max(maxdigits,n);
    bool pal=true; int prefix=0;
    for(int j=0;j<n/2;j++){
      int q=a[j]+a[n-1-j];
      if(a[j]!=a[n-1-j])pal=false;
      int ex= (j<8) ? expected[j][t%8] : -1;
      if(j<8 && ex==q && prefix==j) prefix++;
    }
    // Mark whether any of the first 8 coefficient pairs is odd: permanent nonpalindrome witness.
    bool odd=false;
    for(int j=0;j<min(8,n/2);j++)odd|=((a[j]+a[n-1-j])&1);
    if(!odd)parityFailures++;
    if(pal && firstPalindrome<0)firstPalindrome=t;
    if(prefix<8 && firstError<0)firstError=t;
    if(prefix<minprefix){minprefix=prefix;minTime=t;}
    if(t==0 || t==steps || t%1000==0) sample.push_back({t,n});
    if(t==steps)break;
    vector<uint8_t> b(n+1); int carry=0;
    for(int j=0;j<n;j++){
      int sum=a[j]+a[n-1-j]+carry;
      b[j]=sum%10;carry=sum/10;
    }
    if(carry != (t%2==0) && firstGamma<0)firstGamma=t;
    if(carry){b[n]=carry;} else b.pop_back();
    a.swap(b);
  }
  cout<<"half="<<half<<" steps="<<steps<<" reserve="<<reserve<<" method="<<method
      <<" first_gamma_error="<<firstGamma<<" first_prefix8_error="<<firstError<<" first_palindrome="<<firstPalindrome
      <<" first_odd_pair_loss="<<(parityFailures?"YES":"NO")<<" final_digits="<<a.size()<<"\n";
  for(auto [t,n]:sample)cout<<" t="<<t<<" n="<<n;cout<<"\n";
  // digest of last decimal integer (last 24 decimal digits, first 24 digits)
  cout<<"low24=";for(int j=0;j<min(24,(int)a.size());j++)cout<<int(a[j]);
  cout<<" high24=";for(int j=(int)a.size()-1;j>=max(0,(int)a.size()-24);j--)cout<<int(a[j]);cout<<"\n";
}
