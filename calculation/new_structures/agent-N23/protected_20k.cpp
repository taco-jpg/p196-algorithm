// Independent unrestricted-length base10 digit-vector replay, pairword centre checked EVERY step.
#include <cstdint>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;
int main(int argc,char**argv){
 int Q=(argc>1)?atoi(argv[1]):7000,steps=(argc>2)?atoi(argv[2]):20000;
 if(Q<1||steps<1)return 2;
 vector<uint8_t>d;d.reserve(2*Q+steps+10);
 d.push_back(4);d.push_back(3);
 for(int j=0;j<2*Q;j++)d.push_back(9);
 d.push_back(2);d.push_back(1);
 int min_center=1<<30,first_low=-1,last_low=-1;long long sumcenter=0;
 for(int t=0;t<=steps;t++){
  int n=(int)d.size();if(d.back()==0)return 3;
  bool pal=true;for(int i=0;i<n/2;i++)if(d[i]!=d[n-1-i]){pal=false;break;}
  if(pal){cerr<<"PALINDROME at t="<<t<<"\n";return 4;}
  int a=n/2-1,b=(n+1)/2;if(n%2){a=n/2;b=a;}
  int core=0;
  while(a>=0&&b<n&&d[a]+d[n-1-a]==18&&d[b]+d[n-1-b]==18){core+=(a==b?1:2);a--;b++;}
  if(core<1000){cerr<<"CENTRAL_BAND_EXHAUSTED t="<<t<<" core="<<core<<" len="<<n<<"\n";return 5;}
  min_center=min(min_center,core);sumcenter+=core;
  if(t==0)first_low=core;if(t==steps)last_low=core;
  if(t==steps)break;
  int carry=0;vector<uint8_t>out;out.reserve(n+1);
  for(int i=0;i<n;i++){int s=d[i]+d[n-i-1]+carry;out.push_back(s%10);carry=s/10;}
  if(carry)out.push_back(carry);d.swap(out);
 }
 cout<<"PASS base10 digitlist reverse-add steps="<<steps<<" Q="<<Q<<" final_len="<<d.size()<<" ";
 uint64_t hash=0;for(int i=(int)d.size()-1;i>=0;i--)hash=(hash*131+(uint64_t)(48+d[i]))%1000000007ULL;
 cout<<"center18_initial="<<first_low<<" center18_final="<<last_low<<" min_center18="<<min_center<<" sum_center="<<sumcenter<<" checksum_mod1000000007="<<hash<<"\n";
}
