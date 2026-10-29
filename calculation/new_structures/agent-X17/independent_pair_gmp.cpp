// Independent GMP big-integer reverse-and-add oracle, compared byte-for-byte
// with a separately implemented base-10 digit-vector orbit at EVERY step.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include <gmpxx.h>
using namespace std;
using D=vector<unsigned char>;
// This oracle builds the seed in conventional most-significant-first order.
string initial(int n,const string &motif){
 string x(n,'0');
 for(int j=0;j<n;++j)x[j]=motif[min(j,n-j-1)%motif.size()];
 return x;
}
mpz_class decimal_step(const mpz_class& x){
 string s=x.get_str(10);reverse(s.begin(),s.end());
 mpz_class rev(s,10); return x+rev;
}
// Independent direct digit-list arithmetic, LSD-first.
D digit_step(const D &x){
 D y; y.reserve(x.size()+1); unsigned carry=0;size_t n=x.size();
 for(size_t k=0;k<n;k++){
   unsigned total=unsigned(x[k])+unsigned(x[n-1-k])+carry;
   y.push_back(static_cast<unsigned char>(total-10*(total>=10)));
   carry=unsigned(total>=10);
 }
 if(carry)y.push_back(1);
 return y;
}
string conventional(const D &x){string s; s.reserve(x.size());for(auto it=x.rbegin();it!=x.rend();++it)s.push_back(char('0'+*it));return s;}
D fromstr(const string &s){D d;d.reserve(s.size());for(auto it=s.rbegin();it!=s.rend();++it)d.push_back(static_cast<unsigned char>(*it-'0'));return d;}
uint64_t fnvhash(const D &x){uint64_t h=14695981039346656037ULL;for(auto z:x){h^=z;h*=1099511628211ULL;}return h;}
int main(int argc,char**argv){
 if(argc!=7){cerr<<"usage: independent_pair_gmp ODD_LENGTH STEPS MOTIF OFFSET1 OFFSET2 CHECKPOINTS.csv\n";return 2;}
 int n=atoi(argv[1]), steps=atoi(argv[2]), off=atoi(argv[4]),off2=atoi(argv[5]);string motif=argv[3];
 if(n<3||n%2!=1||off<1||off>n/2||off2<1||off2>n/2||off==off2)return 2;
 string p=initial(n,motif);string q=p;
 const int pos=n/2+off, pos2=n/2+off2; // 0-based most-significant index, "off" away from centre
 if(q[pos]=='9'||q[pos2]=='9')return 2;
 ++q[pos];++q[pos2];
 mpz_class a(p,10),b(q,10);
 D x=fromstr(p),y=fromstr(q);
 ofstream f(argv[6]);f<<"t,length,matched,min_witness,base_hash,pert_hash\n";
 int first_pal=-1,first_length_split=-1,minmatched=n;
 for(int t=0;t<=steps;t++){
   string as=a.get_str(10),bs=b.get_str(10);
   // Deterministic FULL decimal word comparison, not a hash comparison.
   if(as!=conventional(x)||bs!=conventional(y)){
      cerr<<"FAIL full decimal arithmetic equality at t="<<t<<"\n";return 1;
   }
   if(as.size()!=bs.size()) {first_length_split=t;break;}
   int l=0,r=0,nn=int(x.size());
   while(l<nn&&x[l]==y[l])++l;
   while(r<nn&&x[nn-1-r]==y[nn-1-r])++r;
   int m=min(l,r),w=-1;minmatched=min(minmatched,m);
   for(int k=0;k<m;k++)if(x[k]!=x[nn-1-k]){w=k;break;}
   if(t>0&&w<0){cerr<<"FAIL no external asymmetry witness t="<<t<<"\n";return 1;}
   if(bs==string(bs.rbegin(),bs.rend())){first_pal=t;break;}
   if(t<=10||t%100==0||t==steps){
      f<<t<<","<<nn<<","<<m<<","<<w<<","<<fnvhash(x)<<","<<fnvhash(y)<<"\n";
   }
   if(t<steps){a=decimal_step(a);b=decimal_step(b);x=digit_step(x);y=digit_step(y);}
 }
 cerr<<"gmp_digit_full_compare=PASS N="<<n<<" t=0.."<<steps<<" first_pal="<<first_pal
     <<" length_split="<<first_length_split<<" min_matched_ends="<<minmatched
     <<"\n";
 return first_pal>=0||first_length_split>=0?1:0;
}
