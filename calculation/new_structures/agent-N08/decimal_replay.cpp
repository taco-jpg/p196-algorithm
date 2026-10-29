// Independent ordinary decimal digit-list reverse-and-add replay.
// g++ -O3 -std=c++17 -Wall -Wextra decimal_replay.cpp -o decimal_replay
#include <iostream>
#include <vector>
#include <string>
#include <array>
using namespace std;
int main(int argc,char**argv) {
 string seed=argc>1?argv[1]:"196";
 int steps=argc>2?stoi(argv[2]):20000;
 vector<unsigned char>d;
 for(int i=(int)seed.size()-1;i>=0;--i)d.push_back(seed[i]-'0');
 long long odd_all=0,even_all=0,pal=0,inc=0,total_odd=0;
 array<long long,19> coeff{};
 int first_no_odd=-1;
 for(int t=0;t<steps;t++) {
   int n=(int)d.size();bool palindrome=true,odd=false;int count_odd=0;
   for(int i=0;i<n;i++) {
      int s=d[i]+d[n-1-i];coeff[s]++;
      if(s%2){odd=true;count_odd++;}
      if(d[i]!=d[n-1-i])palindrome=false;
   }
   if(palindrome){cout<<"PAL step="<<t<<" n="<<n<<"\n";pal++;break;}
   if(odd){odd_all++;total_odd+=count_odd;}
   else {even_all++;if(first_no_odd<0)first_no_odd=t;
         cout<<"EVENONLY step="<<t<<" len="<<n<<"\n";}
   int carry=0;
   for(int i=0;i<n;i++){
      int z=d[i]+d[n-1-i]+carry;
      d[i]=z%10;carry=z/10;
   }
   if(carry){d.push_back(carry);inc++;}
   if(t==0||t==1||t==2||t==10||t==100||t==999||t==steps-1)
      cout<<"STEP "<<t<<" len="<<n<<" next_len="<<d.size()
          <<" odd_pairs="<<count_odd<<" gamma="<<carry<<"\n";
 }
 cout<<"RESULT seed="<<seed<<" steps="<<steps<<" palindrome="<<pal
     <<" oddguard_pass="<<odd_all<<" evenonly="<<even_all
     <<" first_no_odd="<<first_no_odd<<" overflow="<<inc
     <<" final_length="<<d.size()
     <<" mean_oddpairs="<<(odd_all?double(total_odd)/odd_all:0)<<"\n";
 cout<<"COEFF";for(int x=0;x<19;x++)cout<<' '<<coeff[x];cout<<'\n';
}
