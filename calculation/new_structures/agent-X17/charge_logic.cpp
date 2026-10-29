// Independent base-10 digit-column 8-bit centre perturbation truth-table verifier.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using D=vector<uint8_t>;
D initial(int n, int mask){string motif="88283583";D d(n);for(int i=0;i<n;i++)d[i]=motif[min(i,n-1-i)%8]-'0';for(int k=1;k<=8;k++)if(mask>>(k-1)&1){int i=n/2-k;if(d[i]==9)abort();d[i]++;}return d;}
D step(const D& a){int n=(int)a.size(),carry=0;D b(n);for(int i=0;i<n;i++){int q=int(a[i])+int(a[n-1-i])+carry;b[i]=q%10;carry=q/10;}if(carry)b.push_back(carry);return b;}
int carry_at(const D& a,int j){int n=a.size(),carry=0;for(int i=0;i<j;i++){int q=int(a[i])+int(a[n-1-i])+carry;carry=q/10;}return carry;}
int high(const D&a,const D&b){if(a.size()!=b.size())return -1;int n=a.size(),k=0;while(k<n && a[n-1-k]==b[n-1-k])k++;return k;}
int main(int argc,char**argv){if(argc!=3){cerr<<"usage: charge_logic N CSV_OUT\n";return 2;}int n=atoi(argv[1]);if(n<31 || !(n&1))return 2;D base=initial(n,0);for(int t=0;t<107;t++)base=step(base);int J=base.size()-61;int c0=carry_at(base,J);D baseline108=step(base);ofstream f(argv[2]);f<<"mask,bits,differential_carry,matched_high_t108\n";int nSafe=0, nShock=0,minSafe=n, maxShock=0;for(int mask=0;mask<256;mask++){D x=initial(n,mask);for(int t=0;t<107;t++)x=step(x);int delta=c0^carry_at(x,J);int m=high(baseline108,step(x));f<<mask<<",\"";for(int k=7;k>=0;k--)f<<((mask>>k)&1);f<<"\","<<delta<<","<<m<<"\n";if(delta){nShock++;maxShock=max(maxShock,m);}else{nSafe++;minSafe=min(minSafe,m);}}cerr<<"N="<<n<<" J="<<J<<" safe="<<nSafe<<" shock="<<nShock<<" minSafe="<<minSafe<<" maxShock="<<maxShock<<"\n";}
