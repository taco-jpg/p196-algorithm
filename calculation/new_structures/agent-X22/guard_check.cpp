// Independent literal-digit decimal reverse-add; compares anchored physical bulk.
#include <string>
#include <iostream>
#include <fstream>
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
 ifstream f(argv[1]);string s;f>>s;reverse(s.begin(),s.end());
 int minprefix=INT_MAX;
 for(int t=0;t<=20000;t++){
  int n=s.size();
  if(equal(s.begin(),s.begin()+n/2,s.rbegin())){cerr<<"PAL "<<t<<"\n";return 4;}
  if(t>0){
   for(int i=0;i<39;i++){
    int p=s[i]-'0'+s[n-1-i]-'0';
    if(p!=B[t%8][i]){cerr<<"B FAIL "<<t<<" i="<<i<<"\n";return 5;}
   }
   int run=0;
   for(int i=39;i<n/2;i++){
    int p=s[i]-'0'+s[n-1-i]-'0';
    if(p!=W[t%8][(i-39)%20])break;
    run++;
   }
   if(run<20){cerr<<"PREFIX FAIL "<<t<<" "<<run<<"\n";return 6;}
   minprefix=min(minprefix,run);
   if(t%2000==0||t==20000)cout<<t<<" length="<<n<<" anchored="<<run<<"\n";
  }
  if(t==20000)break;
  string out;out.reserve(n+1);int carry=0;
  for(int i=0;i<n;i++){int z=s[i]-'0'+s[n-1-i]-'0'+carry;out.push_back(char('0'+z%10));carry=z/10;}
  if(carry)out.push_back(char('0'+carry));
  s.swap(out);
 }
 cout<<"PASS anchored min="<<minprefix<<"\n";
}
