// W10: ordinary base-10 digit-list reverse-and-add with an independently
// evaluated central period-4 pair-word condition. No template drives the orbit.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
static uint64_t fnv(const vector<uint8_t> &d){
  uint64_t h=14695981039346656037ull;
  for(uint8_t x:d){h^=x;h*=1099511628211ull;}
  return h;
}
int main(int argc,char **argv){
  if(argc!=4){cerr<<"usage: period4_replay BLOCKS STEPS GUARD\n";return 2;}
  int q=atoi(argv[1]), T=atoi(argv[2]), guard=atoi(argv[3]);
  if(q<1||T<0||guard<0)return 2;
  vector<uint8_t> d;d.reserve(4*q+T+2);
  for(int i=0;i<q;i++){d.push_back(6);d.push_back(4);d.push_back(3);d.push_back(5);}
  int gam=0, first_zero=-1, neutral=0, clock_errors=0, matches=0;
  cout<<"step\tlength\tlength_increases\tinterior_digit_mismatches\tinterior_pair_mismatches\tcentral_word_lsd\tfnv64_lsd\n";
  for(int t=0;t<=T;t++){
    int n=(int)d.size();int a=t+guard, b=n-a-4;
    if(b<a){cerr<<"ERROR: core exhausted at step "<<t<<"\n";return 3;}
    int digit_errors=0,pair_errors=0;
    for(int i=a;i<=b;i++){
      digit_errors+=(d[i]!=d[i+4]);
      if(i+4<n/2)pair_errors+=(d[i]+d[n-1-i]!=d[i+4]+d[n-5-i]);
    }
    if(digit_errors||pair_errors){cerr<<"ERROR period/pair failure at "<<t<<"\n";return 4;}
    bool palindrome=true;
    for(int i=0;i<n/2;i++)if(d[i]!=d[n-1-i]){palindrome=false;break;}
    if(palindrome){cerr<<"ERROR actual palindrome at "<<t<<"\n";return 5;}
    uint8_t row[4];int m=(n/2)/4*4;
    for(int j=0;j<4;j++)row[j]=d[m+j];
    string middle;
    for(int j=0;j<4;j++)middle+=char('0'+row[3-j]);
    if(middle=="0000"&&first_zero<0)first_zero=t;
    if(t%1000==0||t==T)
      cout<<t<<'\t'<<n<<'\t'<<gam<<'\t'<<digit_errors<<'\t'<<pair_errors<<'\t'<<middle<<'\t'
          <<hex<<setw(16)<<setfill('0')<<fnv(d)<<dec<<setfill(' ')<<'\n';
    if(t==T)break;
    int next[4]={},num=0;
    for(int c0=0;c0<=1;c0++){
      int carry=c0,x[4];
      for(int j=0;j<4;j++){
        int s=row[j]+row[(n-1-j)%4]+carry;
        x[j]=s%10;carry=s/10;
      }
      if(carry==c0){num++;for(int j=0;j<4;j++)next[j]=x[j];}
    }
    if(num==2)neutral++;
    vector<uint8_t> e(n);int carry=0;
    for(int i=0;i<n;i++){
      int s=d[i]+d[n-1-i]+carry;
      e[i]=s%10;carry=s/10;
    }
    if(carry)e.push_back(carry);
    gam+=carry;
    if(num==1){
      int mid2=((int)e.size()/2)/4*4;
      for(int j=0;j<4;j++)if(e[mid2+j]!=next[j])clock_errors++;
      matches++;
    }
    d.swap(e);
  }
  cerr<<"PASS block=5346 q="<<q<<" steps="<<T<<" gamma="<<gam
      <<" first_zero_bulk="<<first_zero<<" unique_bulk_checks="<<matches
      <<" clock_cell_errors="<<clock_errors<<" neutral_bulk_steps="<<neutral<<"\n";
  if(clock_errors)return 6;
}
