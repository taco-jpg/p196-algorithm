#include <bits/stdc++.h>
#include <gmpxx.h>
using namespace std;
using Word=vector<uint8_t>;
const array<int,34> B={2,11,1,6,8,1,7,15,9,3,9,4,7,9,10,16,9,11,4,10,8,8,9,11,11,7,4,3,9,12,1,1,9,11};
const array<int,9> W={1,10,8,5,9,16,0,9,11};
const array<int,11> K={6,1,0,1,11,14,10,6,11,16,1};
Word reference(int n){assert(n%2==0);Word p(n);for(int i=0;i<n/2;i++){int x=i<34?B[i]:W[(i-34)%9];p[i]=p[n-1-i]=x;}return p;}
Word injected(const Word &r,initializer_list<int> xs){auto q=r;int n=r.size();for(int x:xs)for(int j=0;j<11;j++)q[x+j]=q[n-1-x-j]=K[j];return q;}
Word step(const Word &a){int n=a.size(), c=0;Word d(n+1),o;for(int i=0;i<n;i++){int z=a[i]+c;d[i]=z%10;c=z/10;}if(c)d[n]=c;else d.pop_back();int nn=d.size();o.resize(nn);for(int i=0;i<nn;i++)o[i]=d[i]+d[nn-1-i];return o;}
// Exact independent GMP arithmetic, not derived from the pairword-normalization engine.
mpz_class realize(const Word &q){int n=q.size();string s(n,'0');for(int i=0;i<n/2;i++){int x=q[i],lo=(i==0?max(1,x-9):min(9,x)),hi=x-lo;if(i==0 && hi==0){lo--;hi++;}if(i!=0){lo=min(9,x);hi=x-lo;}if(lo<0||lo>9||hi<0||hi>9)throw runtime_error("invalid digit split");s[n-1-i]='0'+lo;s[i]='0'+hi;}if(s[0]=='0')throw runtime_error("leading zero");mpz_class v;int rc=mpz_set_str(v.get_mpz_t(),s.c_str(),10);assert(rc==0);return v;}
string canonical(mpz_class const &n){size_t d=mpz_sizeinbase(n.get_mpz_t(),10)+3;string s(d,'\0');mpz_get_str(s.data(),10,n.get_mpz_t());s.resize(strlen(s.c_str()));return s;}
Word pairword(const string &s){int n=s.size();Word w(n);for(int i=0;i<n;i++)w[i]=(s[n-1-i]-'0')+(s[i]-'0');return w;}
void bigint_step(mpz_class &n){string s=canonical(n),r=s;reverse(r.begin(),r.end());mpz_class other;int rc=mpz_set_str(other.get_mpz_t(),r.c_str(),10);assert(rc==0);n+=other;}
int main(int argc,char **argv){int N=argc>1?atoi(argv[1]):90000,H=argc>2?atoi(argv[2]):20000,A=argc>3?atoi(argv[3]):12000,C=argc>4?atoi(argv[4]):32000;bool gmp=argc>5?atoi(argv[5]):true;
 assert(A>34&&C>A+11&&C+11<N/2);
 auto p=reference(N);array<Word,4> words={p,injected(p,{A}),injected(p,{C}),injected(p,{A,C})};
 array<mpz_class,4> nums; if(gmp)for(int j=0;j<4;j++)nums[j]=realize(words[j]);
 if(gmp && argc>6 && atoi(argv[6])!=0)nums[3]+=1; // negative control: arithmetic checker must reject corrupted seed
 for(int t=0;t<=H;t++){
   int len=words[0].size();
   const array<int,12> prefix={0,0,0,1,1,1,1,2,2,2,2,3};
   if(len!=N+3*(t/12)+prefix[t%12]){cerr<<"OVERFLOW_SCHEDULE_FAIL "<<t<<"\n";return 7;}
   for(int j=1;j<4;j++)if(words[j].size()!=size_t(len)) {cerr<<"GAMMA_FAIL "<<t<<"\n";return 2;}
   int nbad=0,minbad=-1,minstart[2]={INT_MAX,INT_MAX},maxstart[2]={-1,-1},cnt[2]={0,0};
   for(int i=0;i<len/2;i++){
      if(int(words[1][i])+int(words[2][i])!=int(words[0][i])+int(words[3][i])){nbad++;if(minbad<0)minbad=i;}
      for(int j=0;j<2;j++)if(words[j+1][i]!=words[0][i]){cnt[j]++;minstart[j]=min(minstart[j],i);maxstart[j]=max(maxstart[j],i);}
   }
   if(minstart[0]<=34 || maxstart[1]>=len/2-34 || maxstart[0]>=minstart[1]){
      cerr<<"ISOLATION_FAIL step="<<t<<" left_gap="<<minstart[0]-34<<" inter_gap="<<minstart[1]-maxstart[0]-1<<" centre_gap="<<len/2-34-maxstart[1]<<"\n";
      return 8;
   }
   if(nbad){cout<<"COLLISION step="<<t<<" first="<<minbad<<" count="<<nbad<<"\n";return 3;}
   if(gmp){for(int j=0;j<4;j++){
      string s=canonical(nums[j]);if(s==string(s.rbegin(),s.rend())){cerr<<"PAL step="<<t<<" seed="<<j<<"\n";return 4;}
      if(pairword(s)!=words[j]){cerr<<"PAIR_MISMATCH step="<<t<<" seed="<<j<<"\n";return 5;}
   }}
   if(t%1000==0||t==H){cout<<"PASS step="<<t<<" digits="<<len<<" supports="<<minstart[0]<<","<<maxstart[0]<<","<<cnt[0]<<";"<<minstart[1]<<","<<maxstart[1]<<","<<cnt[1]<<"\n"<<flush;}
   if(t==H)break;
   for(auto &w:words)w=step(w);
   if(gmp)for(auto &x:nums)bigint_step(x);
 }
 if(gmp)cout<<"LONG_TRAIN_PASS "<<H<<" steps, four independent GMP decimal big integers, full pairword/ non-pal / additive train each step\n";
 else cout<<"COEFFICIENT_TRAIN_PASS "<<H<<" steps, support-isolation/overflow/full-pairword superposition at every step\n";
}
