// Independent finite anchor: two decimal seed lengths, exact digit RAA,
// all-centre-zero check and four-zero insertion comparison at EVERY state.
#include <bits/stdc++.h>
using namespace std;
struct Orbit {
 vector<uint8_t>d;
 Orbit(int q){d.reserve(4*q+20005);for(int i=0;i<q;i++){d.push_back(6);d.push_back(4);d.push_back(3);d.push_back(5);}}
 bool palindrome()const{for(size_t i=0,j=d.size()-1;i<j;i++,j--)if(d[i]!=d[j])return false;return true;}
 void step(){int n=d.size(),c=0;vector<uint8_t>z(n);for(int i=0;i<n;i++){int t=d[i]+d[n-1-i]+c;z[i]=t%10;c=t/10;}if(c)z.push_back(c);d.swap(z);}
};
int main(int argc,char**argv){int T=argc>1?atoi(argv[1]):20000;if(T<33||T>30000)return 2;
 Orbit a(8000),b(8001);int minzeros=INT_MAX,atmin=-1;cout<<"step\tlength_q8000\tlength_q8001\tcentral_zeros_q8000\tboundaries_equal\n";
 for(int t=0;t<=T;t++){
  int n=a.d.size(),n2=b.d.size();if(a.palindrome()||b.palindrome()){cerr<<"PAL "<<t<<"\n";return 3;}
  if(n2!=n+4){cerr<<"length mismatch at "<<t<<"\n";return 4;}
  if(t>=33){int cut=t+64,interior=n-2*cut;if(interior<5)return 5;
   if(interior<minzeros){minzeros=interior;atmin=t;}
   for(int j=0;j<cut;j++)if(a.d[j]!=b.d[j]||a.d[n-1-j]!=b.d[n2-1-j]){cerr<<"outside mismatch "<<t<<","<<j<<"\n";return 6;}
   for(int j=cut;j<n-cut;j++)if(a.d[j]){cerr<<"anchor core not zero "<<t<<","<<j<<"\n";return 7;}
   for(int j=cut;j<n2-cut;j++)if(b.d[j]){cerr<<"comparison core not zero "<<t<<","<<j<<"\n";return 8;}
   if(t==33||t%1000==0||t==T)cout<<t<<'\t'<<n<<'\t'<<n2<<'\t'<<interior<<"\tYES\n";
  }
  if(t<T){a.step();b.step();}
 }
 cerr<<"PASS both exact integer orbits; universal-zero anchor comparisons "<<T-32<<"; min zeros "<<minzeros<<" at t="<<atmin<<"\n";
}
