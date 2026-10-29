// Independent digit-array reverse-and-add, full palindrome and bulk checks.
#include <string>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <climits>
#include <cstdint>
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
int maxmatch(const string &v,int t){
 int n=v.size(),best=0,run=0;
 for(int i=39;i<n/2;i++){
  int p=(v[i]-'0')+(v[n-1-i]-'0');
  if(p==W[t%8][(i-39)%20]){run++;best=max(best,run);}else run=0;
 }
 return best;
}
int main(int argc,char**argv){
 if(argc<3){cerr<<"usage: replay_digits seedfile steps\n";return 2;}
 ifstream fin(argv[1]);string s;fin>>s;
 if(s.empty()){cerr<<"empty seed\n";return 2;}
 reverse(s.begin(),s.end());
 int steps=stoi(argv[2]),minimal=INT_MAX;
 uint64_t digest=1469598103934665603ULL;
 for(int t=0;t<=steps;t++){
  int n=s.size(),matched=t?maxmatch(s,t):-1;
  for(int i=n-1;i>=0;i--)digest=(digest^(uint64_t)(unsigned char)s[i])*1099511628211ULL;
  digest=(digest^255ULL)*1099511628211ULL;
  if(t && matched<40){cerr<<"band fail "<<t<<" "<<matched<<"\n";return 3;}
  if(t)minimal=min(minimal,matched);
  if(equal(s.begin(),s.begin()+n/2,s.rbegin())){cerr<<"palindrome "<<t<<"\n";return 4;}
  if(t%2000==0||t==steps)cout<<"CHECK "<<t<<" digits="<<n<<" longest_bulk="<<matched<<"\n";
  if(t==steps)break;
  string out;out.reserve(n+1);int carry=0;
  for(int i=0;i<n;i++){
   int sum=(s[i]-'0')+(s[n-1-i]-'0')+carry;
   out.push_back(char('0'+sum%10));carry=sum/10;
  }
  if(carry)out.push_back(char('0'+carry));
  s.swap(out);
 }
 cout<<"PASSED digits "<<steps<<" min_longest_bulk="<<minimal<<" digest="<<hex<<digest<<dec<<"\n";
}
