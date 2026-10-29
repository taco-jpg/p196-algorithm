// Independent GMP whole-integer reverse-add and phase-specific physical bulk.
#include <gmpxx.h>
#include <string>
#include <fstream>
#include <iostream>
#include <algorithm>
#include <climits>
using namespace std;
static const int W[8][20]={
{17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13},
{12,11,4,5,12,10,7,8,12,10,3,2,7,10,8,8,9,5,17,11},
{6,3,9,11,5,1,15,17,5,1,7,4,15,0,17,16,18,11,15,4},
{10,9,13,1,7,6,7,14,13,6,8,11,10,6,8,15,16,11,8,10},
{2,0,7,3,14,12,15,9,7,13,17,3,1,13,17,11,14,3,18,1},
{3,2,7,10,8,8,9,5,17,11,12,11,4,5,12,10,7,8,12,10},
{7,4,15,0,17,16,18,11,15,4,6,3,9,11,5,1,15,17,5,1},
{8,11,10,6,8,15,16,11,8,10,10,9,13,1,7,6,7,14,13,6}};
int main(int argc,char**argv){
 if(argc<3)return 2;
 int B[8][39];ifstream b(argv[2]);for(int t=0;t<8;t++)for(int i=0;i<39;i++)b>>B[t][i];
 ifstream f(argv[1]);string seed;f>>seed;mpz_class N(seed,10);
 int minrun=INT_MAX;
 for(int t=0;t<=20000;t++){
  string s=N.get_str(),rev=s;reverse(rev.begin(),rev.end());
  int n=s.size();
  if(s==rev){cerr<<"PAL "<<t<<"\n";return 3;}
  if(t>0){
   for(int i=0;i<39;i++){
    int p=(s[n-1-i]-'0')+(s[i]-'0');
    if(p!=B[t%8][i]){cerr<<"BFAIL "<<t<<" "<<i<<"\n";return 4;}
   }
   int r=0;
   for(int i=39;i<n/2;i++){
    int p=(s[n-1-i]-'0')+(s[i]-'0');
    if(p!=W[t%8][(i-39)%20])break;
    r++;
   }
   if(r<20){cerr<<"SHORT "<<t<<" "<<r<<"\n";return 5;}
   minrun=min(minrun,r);
   if(t%2000==0||t==20000)cout<<t<<" length="<<n<<" anchored="<<r<<"\n";
  }
  if(t!=20000)N+=mpz_class(rev,10);
 }
 cout<<"PASS anchored min="<<minrun<<"\n";
}
