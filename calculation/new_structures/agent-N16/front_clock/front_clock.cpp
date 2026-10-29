// Exact 22-step affine front law; independent GMP and schoolbook integer engines.
#include <gmp.h>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <cstring>
#include <string>
#include <vector>
using namespace std;
static int cv(char c){return c<='9'?c-'0':c-'A'+10;}
static string number(const vector<unsigned char>&a){string s;for(auto it=a.rbegin();it!=a.rend();it++)s.push_back(char('0'+*it));return s;}
int main(int argc,char**argv){
 if(argc<2)return 1;
 int q=argc>2?stoi(argv[2]):300,H=argc>3?stoi(argv[3]):20000;
 if(q<1||H<44)return 2;
 ifstream f(argv[1]);string header;getline(f,header);
 vector<string>B(8),W(8);for(auto&x:B)getline(f,x);for(auto&x:W)getline(f,x);
 for(int t=0;t<8;t++)if(B[t].size()!=39||W[t].size()!=20)return 3;
 vector<int> p;for(char c:B[0])p.push_back(cv(c));
 for(int i=0;i<q;i++)for(char c:W[0])p.push_back(cv(c));
 vector<unsigned char>d;for(int v:p)d.push_back(max(0,v-9));
 for(auto it=p.rbegin();it!=p.rend();it++)d.push_back(min(9,*it));
 mpz_t n,r,z;mpz_inits(n,r,z,nullptr);string init=number(d);if(mpz_set_str(n,init.c_str(),10)!=0)return 4;
 const int F[22]={0,0,0,0,1,1,1,1,1,1,2,2,2,2,3,3,3,3,5,5,5,5};
 int minpre=1000000,checked=0;
 for(int t=0;t<=H;t++){
  string s(mpz_sizeinbase(n,10)+3,'\0');mpz_get_str(s.data(),10,n);s.resize(strlen(s.c_str()));
  if(s!=number(d)){cerr<<"integer divergence "<<t<<"\n";return 5;}
  int L=d.size(),m=0;for(int i=0;i<L/2;i++){
   int expected=i<39?cv(B[t%8][i]):cv(W[t%8][(i-39)%20]);
   if(d[i]+d[L-1-i]!=expected)break;
   ++m;
  }
  minpre=min(minpre,m);if(m<39){cerr<<"exterior loss "<<t<<"\n";return 6;}
  int D=39+20*q-m;
  if(t>=22){int expected=5*(t/22)+F[t%22];if(D!=expected){cerr<<"front law fail "<<t<<" "<<D<<" "<<expected<<"\n";return 7;}++checked;}
  if(t==H)break;
  vector<unsigned char>next;next.reserve(L+1);int carry=0;
  for(int i=0;i<L;i++){int v=d[i]+d[L-1-i]+carry;next.push_back(v%10);carry=v/10;}
  if(carry)next.push_back(carry);
  string rev=s;reverse(rev.begin(),rev.end());if(mpz_set_str(r,rev.c_str(),10)!=0)return 8;
  mpz_add(z,n,r);mpz_swap(n,z);
  if((int)next.size()-L!=(t%2==0))return 9;
  d.swap(next);
 }
 cout<<"FRONT_22_PASS q="<<q<<" H="<<H<<" phase_checks="<<checked<<" min_prefix="<<minpre<<" final_digits="<<d.size()<<" velocity=5/22\n";
 mpz_clears(n,r,z,nullptr);
}
