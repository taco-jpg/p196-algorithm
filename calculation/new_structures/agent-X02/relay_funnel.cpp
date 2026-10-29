// X02: independent decimal DIGIT arithmetic, exact two-step fibre and finite central carry-erasure relay.
#include <bits/stdc++.h>
using namespace std;
using D=vector<unsigned char>;
static D step(const D& d){
  const size_t n=d.size();D y;y.reserve(n+1);int c=0;
  for(size_t i=0;i<n;i++){
    int z=(int)d[i]+d[n-1-i]+c;
    y.push_back((unsigned char)(z%10));c=z/10;
  }
  if(c)y.push_back((unsigned char)c);
  if(y.back()==0)throw runtime_error("leading zero");
  return y;
}
static D seed(int h,int a,unsigned long long key){
  D d(2*h);uint64_t s=key;
  for(int j=0;j<h;j++){
    s^=s<<13;s^=s>>7;s^=s<<17;
    int p=(j==0||((s>>43)&1))?a+9:a;
    int high=min(p,9);int low=p-high;
    d[j]=low;d[2*h-1-j]=high;
  }
  return d;
}
int main(int argc,char**argv){
  int h= argc>1?atoi(argv[1]):20200, H=argc>2?atoi(argv[2]):20000;
  if(h<=H+30){cerr<<"h must exceed H + 30\n";return 2;}
  D a=seed(h,8,123456),b=seed(h,8,999777);
  if(a==b)throw runtime_error("seeds equal");
  D a1=step(a),b1=step(b),a2=step(a1),b2=step(b1);
  if(a1==b1||a2!=b2)throw runtime_error("two-step funnel failure");
  cout<<"FUNNEL_PASS h="<<h<<" length_N0="<<a.size()<<" length_N1="<<a1.size()<<" length_N2="<<a2.size()<<"\n";
  D formula(2*h+1,7); formula[0]=8;formula[1]=6;formula.back()=9;
  if(formula!=a2)throw runtime_error("closed form failed");
  cout<<"CLOSED_FORM_PASS N2=9 7^("<<2*h-2<<") 68\n";
  D d=std::move(a2);int uniform[6]={14,10,2,4,8,16};
  int64_t nchecked=0;int mincentral=INT_MAX;
  for(int t=0;t<=H;t++){
    const int n=(int)d.size();const int margin=t+20;
    int left=margin,right=n-margin-1;
    if(left>=right)throw runtime_error("insufficient corridor");
    mincentral=min(mincentral,right-left+1);
    int q=uniform[t%6];
    for(int j=left;j<=right;j++){
      if((int)d[j]+d[n-j-1]!=q){
        cerr<<"BAND_FAILURE t="<<t<<" index="<<j<<" q="<<(int)d[j]+d[n-j-1]<<" expected="<<q<<"\n";
        return 3;
      }
      nchecked++;
    }
    bool pal=true;
    for(int j=0;j<n/2;j++)if(d[j]!=d[n-j-1]){pal=false;break;}
    if(pal){cerr<<"PALINDROME t="<<t<<"\n";return 4;}
    if(t!=H)d=step(d);
  }
  uint64_t sig=1469598103934665603ULL;
  for(auto digit:d){sig^=(uint64_t)digit+1;sig*=1099511628211ULL;}
  cout<<"DIGIT_FNV64="<<hex<<sig<<dec<<"\n";
  cout<<"REPLAY_PASS H="<<H<<" checked_central_paircells="<<nchecked<<" min_corridor="<<mincentral<<" final_digits="<<d.size()<<"\n";
  return 0;
}
