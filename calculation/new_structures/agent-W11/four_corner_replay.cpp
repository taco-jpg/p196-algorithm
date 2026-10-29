// W11: exact four-corner multivariate polynomial reverse/add,
// N = p00*10^s00 + p01*10^(q2+s01)+p10*10^(q1+s10)+p11*10^(q1+q2+s11).
#include <gmpxx.h>
#include <algorithm>
#include <array>
#include <climits>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <tuple>
using namespace std;
using P=array<mpz_class,4>;using S=array<long long,4>;
string dec(const mpz_class &x){return x.get_str();}
long long nd(const mpz_class &x){return x==0?0:(long long)dec(x).size();}
mpz_class rev(const mpz_class &x){if(x==0)return 0;string s=dec(x);reverse(s.begin(),s.end());return mpz_class(s,10);}
mpz_class pow10(long long n){if(n<0||n>200000)throw runtime_error("power out of range");mpz_class z;mpz_ui_pow_ui(z.get_mpz_t(),10,n);return z;}
long long offs(int k,long long q2,long long delta){return k==0?0:k==1?q2:k==2?q2+delta:2*q2+delta;}
string word(const P&p,const S&s,long long q2,long long delta){
 string w="";long long last=-1;for(int k=3;k>=0;k--){if(p[k]==0)continue;long long e=offs(k,q2,delta)+s[k];
  if(last>=0){long long gap=last-e-nd(p[k]);if(gap<0)throw runtime_error("overlap");w+=string(gap,'0');}
  w+=dec(p[k]);last=e;}
 if(last<0)throw runtime_error("zero integer");if(last>0)w+=string(last,'0');return w;
}
pair<P,S> nextstep(const P&p,const S&s){
 P np;S ns;long long E=s[3]+nd(p[3]);
 for(int k=0;k<4;k++){
  int j=3-k;bool a=p[k]!=0,b=p[j]!=0;
  if(!a&&!b){np[k]=0;ns[k]=0;continue;}
  long long r=E-s[j]-nd(p[j]);long long m=a&&b?min(s[k],r):a?s[k]:r;
  np[k]=(a?p[k]*pow10(s[k]-m):mpz_class(0))+(b?rev(p[j])*pow10(r-m):mpz_class(0));ns[k]=m;
 }
 return {np,ns};
}
static pair<long long,long long> sep_bounds(const P&p,const S&s){
 if(p[1]==0||p[2]==0)return {0,0};
 return {max(s[0]+nd(p[0])-s[1],s[2]+nd(p[2])-s[3]),s[1]+nd(p[1])-s[2]};
}
static pair<long long,long long> pair_bounds(const P&p,const S&s){
 long long E=s[3]+nd(p[3]);S left,right;
 for(int k=0;k<4;k++){
  int j=3-k;long long r=E-s[j]-nd(p[j]);
  left[k]=LLONG_MAX;right[k]=LLONG_MIN;
  if(p[k]!=0){left[k]=min(left[k],s[k]);right[k]=max(right[k],s[k]+nd(p[k]));}
  if(p[j]!=0){left[k]=min(left[k],r);right[k]=max(right[k],r+nd(rev(p[j])));}
 }
 return {max(right[0]-left[1],right[2]-left[3]),right[1]-left[2]};
}
static long long nonpal_bound(const P&p,const S&s){
 long long E=s[3]+nd(p[3]),m=0;S r;P rp;
 for(int k=0;k<4;k++){
  int j=3-k;if(p[j]){r[k]=E-s[j]-nd(p[j]);rp[k]=rev(p[j]);m=min(m,r[k]);}else{r[k]=0;rp[k]=0;}
  if(p[k])m=min(m,s[k]);
 }
 int h=-1;
 for(int k=3;k>=0;k--){
  if(!p[k]&&!rp[k])continue;
  if(!p[k]||!rp[k]){h=k;break;}
  long long u=min(s[k],r[k]);
  if(dec(p[k])+string(s[k]-u,'0')!=dec(rp[k])+string(r[k]-u,'0')){h=k;break;}
 }
 if(h<0)throw runtime_error("polynomial identical palindrome");
 if(h==0)return 0;
 long long M=0;
 for(int k=0;k<h;k++){
  if(p[k])M=max(M,nd(p[k])+s[k]-m);
  if(rp[k])M=max(M,nd(rp[k])+r[k]-m);
 }
 return M+1; // at most 6 lower terms, 10^(M+1)>6*10^M
}
uint64_t fnv(const string&s){uint64_t h=14695981039346656037ULL;for(unsigned char c:s){h^=c;h*=1099511628211ULL;}return h;}
string pairs(const string &s){string p(s.size(),'A');for(size_t i=0;i<s.size();i++)p[i]='A'+s[i]+s[s.size()-1-i]-2*'0';return p;}
string fullstep(const string&s){string out(s.size(),'0');int c=0;for(size_t i=0;i<s.size();i++){int x=s[s.size()-1-i]+s[i]-2*'0'+c;out[s.size()-1-i]='0'+x%10;c=x/10;}if(c)out.insert(out.begin(),'1');return out;}
bool pal(const string&s){for(size_t i=0;i<s.size()/2;i++)if(s[i]!=s[s.size()-1-i])return false;return true;}
int main(int argc,char**argv){
 try{
  if(argc!=8&&argc!=9)throw runtime_error("usage: four_corner Q2 DELTA END OUT.tsv STATE A M [RESUME]");
  long long q2=stoll(argv[1]),delta=stoll(argv[2]);int end=stoi(argv[3]),start=0;
  P p={75,mpz_class(argv[7]),0,mpz_class(argv[6])};S s={0,2,0,3};
  string actual=word(p,s,q2,delta);
  if(argc==9){ifstream in(argv[8]);if(!in)throw runtime_error("missing resume");in>>start;for(int k=0;k<4;k++)in>>s[k];for(int k=0;k<4;k++){string v;in>>v;p[k]=mpz_class(v,10);}in>>actual;if(actual!=word(p,s,q2,delta))throw runtime_error("invalid resume");}
  ofstream out(argv[4]);out<<"t\tlen00\tlen01\tlen10\tlen11\ts00\ts01\ts10\ts11\tq2_sep\tdelta_sep\tq2_pair\tdelta_pair\tq_nonpal\tdigits\tnum_hash\tpair_hash\n";
  long long Bq=0,Bd=0,Pq=0,Pd=0,Nb=0;
  for(int t=start;t<=end;t++){
   auto [bq,bd]=sep_bounds(p,s);auto [pq,pd]=pair_bounds(p,s);long long np=nonpal_bound(p,s);
   Bq=max(Bq,bq);Bd=max(Bd,bd);Pq=max(Pq,pq);Pd=max(Pd,pd);Nb=max(Nb,np);
   string w=word(p,s,q2,delta);
   if(w!=actual)throw runtime_error("digit replay mismatch at step "+to_string(t));
   if(pal(actual))throw runtime_error("palindrome at step "+to_string(t));
   if(t%1000==0||t==end){out<<t;for(int k=0;k<4;k++)out<<'\t'<<nd(p[k]);for(int k=0;k<4;k++)out<<'\t'<<s[k];out<<'\t'<<bq<<'\t'<<bd<<'\t'<<pq<<'\t'<<pd<<'\t'<<np<<'\t'<<w.size()<<'\t'<<hex<<fnv(w)<<'\t'<<fnv(pairs(w))<<std::dec<<'\n';out.flush();
    mpz_class x(w,10);string r=w;reverse(r.begin(),r.end());mpz_class n=x+mpz_class(r,10);if(t<end&&dec(n)!=fullstep(w))throw runtime_error("GMP checkpoint mismatch");
    cerr<<"step="<<t<<" Q2="<<max(Bq,max(Pq,Nb))<<" Qdelta="<<max(Bd,max(Pd,Nb))<<" digits="<<w.size()<<'\n';}
   if(t==end)break;
   actual=fullstep(actual);tie(p,s)=nextstep(p,s);
  }
  ofstream state(argv[5]);state<<end<<'\n';for(int k=0;k<4;k++)state<<s[k]<<' ';state<<'\n';for(int k=0;k<4;k++)state<<dec(p[k])<<'\n';state<<actual<<'\n';
  cerr<<"PASS until "<<end<<" Q2="<<max(Bq,max(Pq,Nb))<<" Qdelta="<<max(Bd,max(Pd,Nb))<<" digits="<<actual.size()<<'\n';
 }catch(const exception&e){cerr<<"FAIL: "<<e.what()<<'\n';return 1;}
}
