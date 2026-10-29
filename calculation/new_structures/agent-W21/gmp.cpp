// Independent GNU GMP integer replay. No pairword normalization or template updates.
// g++ -O3 -std=c++17 gmp.cpp -lgmpxx -lgmp -o /tmp/w21_gmp
#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using V=vector<int>;
static const V B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const V W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
static const V Q={17,10,13,11,18,15,1,2,10,4,1,8,17,4,10,2,15,16,8,0,5,4,14,9,8,0,3,11,18,1,0,9,0,17,9,8,5,1,3,1};
uint64_t fnv(const string& bigend){uint64_t h=14695981039346656037ULL;for(auto it=bigend.rbegin();it!=bigend.rend();it++){h^=(uint64_t)(unsigned char)*it;h*=1099511628211ULL;}return h;}
int main(int argc,char**argv){int copies=argc>1?atoi(argv[1]):225,steps=argc>2?atoi(argv[2]):20000;
 V half=B;for(int k=0;k<copies;k++)half.insert(half.end(),W.begin(),W.end());half.insert(half.end(),Q.begin(),Q.end());
 string s;for(int x:half)s.push_back(char('0'+(x-x/2)));
 for(auto it=half.rbegin();it!=half.rend();it++)s.push_back(char('0'+*it/2));
 mpz_class n(s,10);
 int palindrome_count=0;for(int t=0;t<=steps;t++){
  string a=n.get_str(), rev=a;reverse(rev.begin(),rev.end());if(a==rev)palindrome_count++;
  if(t==0||t==1000||t==5000||t==10000||t==20000||t==steps){cout<<"t="<<t<<" digits="<<a.size()<<" pal="<<(a==rev)<<" fnv64="<<hex<<fnv(a)<<dec<<"\n";}
  if(t<steps)n+=mpz_class(rev,10);
 }
 cout<<"palindrome_states="<<palindrome_count<<"\n";return palindrome_count?2:0;
}
