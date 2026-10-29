// W28: modulo-200 centre-programmed non-gauge three-step particle erasure.
// g++ -O3 -std=c++17 modular_eraser.cpp -lgmpxx -lgmp -o /tmp/w28 && /tmp/w28 260 20000
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
#include <gmpxx.h>
using namespace std;
using Word=vector<uint8_t>;
static constexpr int Bv[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static constexpr int Wv[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
static constexpr int MOD=200;
static constexpr int active[]={0,1,3,7,21,34,55,89,144,199};
Word template_word(int K, int program){
  Word h;for(int x:Bv)h.push_back(x);
  for(int j=0;j<K;j++)for(int x:Wv)h.push_back(x);
  h.push_back(8);
  if(program){
    for(int j=3;j+4<=K;j++){
      bool yes=false;
      for(int x:active)if(j%MOD==x)yes=true;
      if(program==2)yes=(j%7==0 || j%7==3);
      if(!yes)continue;
      int s=39+20*j+5;
      assert(h[s]==11&&h[s+1]==14&&h[s+2]==3);
      h[s]=6;h[s+1]=6;h[s+2]=7;
    }
  }
  Word p=h;
  for(int i=int(h.size())-2;i>=0;i--)p.push_back(h[i]);
  assert(p.size()==2*(39+20*K)+1);
  return p;
}
Word coeff_step(const Word& p){Word ds;ds.reserve(p.size()+1);int carry=0;for(int x:p){int v=x+carry;ds.push_back(v%10);carry=v/10;}if(carry)ds.push_back(carry);Word q(ds.size());for(size_t i=0;i<ds.size();i++)q[i]=ds[i]+ds[ds.size()-1-i];return q;}
string decimal_seed(const Word& p){assert(p.size()%2==1);int n=p.size();string s(n,'0');for(int i=0;i<n/2;i++){int x=p[i],lo=max(0,x-9);s[n-1-i]=char('0'+lo);s[i]=char('0'+x-lo);}s[n/2]=char('0'+p[n/2]/2);assert(s[0]!='0');return s;}
uint64_t hashstr(const string& s){uint64_t h=14695981039346656037ULL;for(char c:s){h^=static_cast<unsigned char>(c);h*=1099511628211ULL;}return h;}
string add_reverse(const string& s){string d;d.reserve(s.size()+1);int carry=0;for(int i=int(s.size())-1;i>=0;i--){int v=(s[i]-'0')+(s[s.size()-1-i]-'0')+carry;d.push_back(char('0'+v%10));carry=v/10;}if(carry)d.push_back(char('0'+carry));reverse(d.begin(),d.end());return d;}
Word digits_pairword(const string& s){Word p(s.size());for(size_t i=0;i<s.size();i++)p[i]=(s[i]-'0')+(s[s.size()-1-i]-'0');return p;}
int main(int argc,char**argv){int K=argc>1?atoi(argv[1]):260,steps=argc>2?atoi(argv[2]):20000;
 if(K<8||steps<0)return 2;
 Word base=template_word(K,0),masked=template_word(K,1),another=template_word(K,2);
 string a=decimal_seed(base),b=decimal_seed(masked),c=decimal_seed(another);
 for(int t=0;t<=4;t++){
  if(digits_pairword(a)!=base||digits_pairword(b)!=masked||digits_pairword(c)!=another){cerr<<"early pairword error "<<t<<"\n";return 3;}
  if(a==string(a.rbegin(),a.rend())||b==string(b.rbegin(),b.rend())||c==string(c.rbegin(),c.rend())){cerr<<"early palindrome "<<t<<"\n";return 9;}
  if(t==3 && !(base==masked && base==another)){cerr<<"packet erasure failure\n";return 4;}
  if(t==4 && !(a==b&&a==c)){cerr<<"physical merge failure\n";return 5;}
  if(t<4){base=coeff_step(base);masked=coeff_step(masked);another=coeff_step(another);a=add_reverse(a);b=add_reverse(b);c=add_reverse(c);}
 }
 cout<<"EARLY three programs: entire pairwords coalesce t=3, physical integers t=4, length="<<a.size()<<"\n";
 string d=decimal_seed(template_word(K,1));mpz_class g(d,10);
 Word p=template_word(K,1);
 Word ref=template_word(50,0);vector<Word> phases(8),bands(8);
 for(int t=0;t<8;t++){phases[t]=Word(ref.begin(),ref.begin()+39);bands[t]=Word(ref.begin()+39,ref.begin()+59);ref=coeff_step(ref);}
 assert(phases[0][0]==17 && phases[1][0]==8 && phases[2][0]==17);
 const int checks[]={0,1,2,3,4,8,88,1000,5000,10000,15000,20000};
 int overflow=0,min_repeats=1000000;
 for(int t=0;t<=steps;t++){
   if(p.size()<39||!equal(phases[t%8].begin(),phases[t%8].end(),p.begin())){cerr<<"root prefix broke at "<<t<<"\n";return 10;}
   int repeats=0;
   while(39+20*(repeats+1)<=int(p.size())/2 &&
     equal(bands[t%8].begin(),bands[t%8].end(),p.begin()+39+20*repeats))repeats++;
   min_repeats=min(min_repeats,repeats);
   if(repeats<1){cerr<<"last full lattice band lost at "<<t<<"\n";return 11;}
   if(d.size()!=p.size()||digits_pairword(d)!=p){cerr<<"coeff mismatch at "<<t<<"\n";return 6;}
   if(d==string(d.rbegin(),d.rend())){cerr<<"PAL at t="<<t<<"\n";return 7;}
   string gs=g.get_str();if(gs!=d){cerr<<"GMP mismatch at "<<t<<"\n";return 8;}
   bool print=false;for(int x:checks)if(x==t)print=true;
   if(print)cout<<"CHECK step="<<t<<" digits="<<d.size()<<" hash="<<hashstr(d)<<" bands="<<repeats<<" first39=";
   if(print){for(int j=0;j<39;j++)cout<<int(p[j])<<",";cout<<"\n";}
   if(t==steps)break;
   string before=d;
   d=add_reverse(before);
   if(d.size()>before.size())overflow++;
   string gr=gs;reverse(gr.begin(),gr.end());mpz_class rev(gr,10);g+=rev;
   p=coeff_step(p);
 }
 cout<<"PASS k="<<K<<" steps="<<steps<<" no_pal="<<steps+1<<" overflow="<<overflow<<" min_bands="<<min_repeats<<" end_digits="<<d.size()<<" end_hash="<<hashstr(d)<<"\n";
}
