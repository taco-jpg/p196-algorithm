#include <bits/stdc++.h>
#include <gmpxx.h>
using namespace std;
// Independent GMP big-integer accumulator plus separately coded schoolbook digit stream.
// At EVERY step update GMP by the reversed decimal integer; compare full values every 100.
string seed(int A,int L,int C){vector<int> p;p.insert(p.end(),A,8);p.insert(p.end(),L,9);p.insert(p.end(),C,10);p.insert(p.end(),L,9);p.insert(p.end(),A,8);int n=p.size();string s(n,'0');for(int i=0;i<n/2;i++){int lo=min(p[i],9),hi=p[i]-lo;if(i==0){hi=8;lo=0;}s[i]='0'+hi;s[n-1-i]='0'+lo;}return s;}
string digitstep(const string&s){int n=s.size(),carry=0;string out(n,'0');for(int i=n-1;i>=0;i--){int y=(s[i]-'0')+(s[n-i-1]-'0')+carry;out[i]='0'+y%10;carry=y/10;}if(carry)out.insert(out.begin(),'1');return out;}
int main(int argc,char**argv){int A=argc>1?atoi(argv[1]):14000,L=argc>2?atoi(argv[2]):8000,C=argc>3?atoi(argv[3]):16000,H=argc>4?atoi(argv[4]):20000;string s=seed(A,L,C);mpz_class n(s,10);
 for(int t=0;t<H;t++){
  string r(s.rbegin(),s.rend());n+=mpz_class(r,10);
  s=digitstep(s);
  if(t<4||(t+1)%100==0||(t+1)==H){if(n.get_str()!=s){cerr<<"MISMATCH GMP t="<<t+1<<"\n";return 2;}if((t+1)%2000==0)cerr<<"GMP checked t="<<t+1<<" digits="<<s.size()<<"\n";}
 }
 ofstream("w22_gmp_final_digits.txt")<<s;
 cout<<"GMP_PASS steps="<<H<<" digits="<<s.size()<<" final_prefix="<<s.substr(0,80)<<" final_suffix="<<s.substr(s.size()-80)<<"\n";
}
