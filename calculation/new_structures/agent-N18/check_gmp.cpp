// Agent N18: independent ordinary-GMP-integer reverse/add and actual decimal-digit pairing.
// Compile with -lgmpxx -lgmp. Reads lattice.txt; does not use the pair-word normalizer.
#include <gmpxx.h>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
int main(int argc,char**argv){
 int q=argc>1?atoi(argv[1]):256,steps=argc>2?atoi(argv[2]):20000;
 int col[39][8],row[8][20];ifstream f("lattice.txt");
 if(!f){cerr<<"lattice.txt missing\n";return 5;}
 for(auto &a:col)for(int &v:a)f>>v;
 for(auto &a:row)for(int &v:a)f>>v;
 vector<int> a;
 for(auto &c:col)a.push_back(c[0]);
 for(int j=0;j<20*q;j++)a.push_back(row[0][j%20]);
 vector<int> d;
 for(int x:a)d.push_back(min(9,x));
 d.push_back(0);
 for(int j=(int)a.size()-1;j>=0;j--)d.push_back(a[j]-min(9,a[j]));
 string s;for(int j=(int)d.size()-1;j>=0;j--)s.push_back(char('0'+d[j]));
 if(s[0]=='0'){cerr<<"noncanonical seed\n";return 3;}
 mpz_class z(s,10);int minBand=1000000,overflows=0;
 for(int t=0;t<=steps;t++){
  s=z.get_str(10);int phase=t%8;
  if(equal(s.begin(),s.end(),s.rbegin())){cerr<<"palindrome t="<<t<<"\n";return 2;}
  int n=s.size();
  for(int j=0;j<39;j++)
   if((s[n-1-j]-'0')+(s[j]-'0')!=col[j][phase]){
    cerr<<"exterior mismatch t="<<t<<" j="<<j<<"\n";return 1;
   }
  int matched=0,cap=n/2-39;
  while(matched<cap&&(s[n-1-(39+matched)]-'0')+(s[39+matched]-'0')==row[phase][matched%20])matched++;
  minBand=min(minBand,matched/20);
  if(t==0||t==1||t==8||t==100||t==1000||t==10000||t==steps)
   cout<<"checkpoint "<<t<<" digits="<<n<<" bands="<<matched/20<<" no-pal=yes exterior=ok\n"<<flush;
  if(t==steps)break;
  reverse(s.begin(),s.end());
  int oldN=n;
  z+=mpz_class(s,10);
  overflows+=(z.get_str(10).size()>size_t(oldN));
 }
 cout<<"PASS GMP q="<<q<<" steps="<<steps<<" min_complete_bands="<<minBand<<" overflows="<<overflows<<"\n";
}
