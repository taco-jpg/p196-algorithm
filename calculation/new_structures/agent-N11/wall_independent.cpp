// Independent MSB-first string/int replay of N_L with moving zero walls.
#include <bits/stdc++.h>
using namespace std;
static string seed(int L){uint32_t x=196;int m=L+130;string hi,lo;hi.reserve(m);lo.reserve(m);for(int i=0;i<m;i++){int p;if(i==64||i==L+65)p=11;else if(i>=65&&i<65+L)p=9;else{x^=x<<13;x^=x>>17;x^=x<<5;p=x%19;}if(i==0)p=12;hi+=char('0'+min(9,p));lo+=char('0'+max(0,p-9));}return hi+string(lo.rbegin(),lo.rend());}
static string plusrev(const string &s){int n=s.size(),c=0;string out;out.reserve(n+1);for(int i=n-1;i>=0;i--){int v=s[i]+s[n-1-i]-2*'0'+c;out+=char('0'+v%10);c=v/10;}if(c)out+='1';reverse(out.begin(),out.end());return out;}
static uint64_t digest(const string&s){uint64_t h=1469598103934665603ull;for(auto it=s.rbegin();it!=s.rend();++it){h^=*it-'0';h*=1099511628211ull;}return h;}
int main(int argc,char**argv){int L=argc>1?atoi(argv[1]):45000,limit=argc>2?atoi(argv[2]):110000,period=argc>3?atoi(argv[3]):10000;string s=seed(L);int A=-1,B=-1;int counts[2][2][2]={};int prevGam=0;
for(int t=0;t<=limit;t++){
 if(equal(s.begin(),s.begin()+s.size()/2,s.rbegin())){cerr<<"PAL step="<<t<<"\n";return 3;}
 if(t>0){int n=s.size();auto P=[&](int i){return s[n-1-i]+s[i]-2*'0';};int probe=A<0?65+L/2:(A+B)/2;if(P(probe)!=0){int found=-1;for(int i=max(0,A-2);i<=min(n/2-1,B+2);i++)if(P(i)==0){found=i;break;}if(found<0){cout<<"INDEPENDENT WALL ENDED t="<<t<<" final_digits="<<n<<" hash="<<hex<<digest(s)<<dec<<"\n";break;}probe=found;}
 int a=probe,b=probe;while(a>0&&P(a-1)==0)a--;while(b+1<n/2&&P(b+1)==0)b++;
 if(A>=0){int da=a-A,db=B-b;if(da<0||da>1||db<0||db>1){cerr<<"unexpected wall jump t="<<t<<"\n";return 4;}counts[prevGam][da][db]++;}
 if(t%period==0||t==1)cout<<"INDEPENDENT t="<<t<<" len="<<n<<" left="<<a<<" right="<<b<<" width="<<b-a+1<<" hash="<<hex<<digest(s)<<dec<<"\n";
 A=a;B=b;
 }
 if(t==limit)break;
 string nxt=plusrev(s);prevGam=int(nxt.size()>s.size());s=move(nxt);
}
for(int g=0;g<2;g++)for(int da=0;da<2;da++)for(int db=0;db<2;db++)if(counts[g][da][db])cout<<"INDEPENDENT transition g="<<g<<" left+="<<da<<" right-="<<db<<" count="<<counts[g][da][db]<<"\n";
}
