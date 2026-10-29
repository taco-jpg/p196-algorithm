// W06 independent canonical decimal GMP check, no digit-array step or phase synthesis.
#include <gmpxx.h>
#include <vector>
#include <string>
#include <algorithm>
#include <iostream>
#include <cstdlib>
#include <cstdint>
using namespace std;
const vector<int> B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
const vector<int> W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
const int WP[8][20]={
{17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13},
{12,11,4,5,12,10,7,8,12,10,3,2,7,10,8,8,9,5,17,11},
{6,3,9,11,5,1,15,17,5,1,7,4,15,0,17,16,18,11,15,4},
{10,9,13,1,7,6,7,14,13,6,8,11,10,6,8,15,16,11,8,10},
{2,0,7,3,14,12,15,9,7,13,17,3,1,13,17,11,14,3,18,1},
{3,2,7,10,8,8,9,5,17,11,12,11,4,5,12,10,7,8,12,10},
{7,4,15,0,17,16,18,11,15,4,6,3,9,11,5,1,15,17,5,1},
{8,11,10,6,8,15,16,11,8,10,10,9,13,1,7,6,7,14,13,6}};
const int BP[8][39]={
{17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13},
{8,13,5,1,5,8,9,8,2,18,14,13,15,12,12,7,11,5,8,6,10,15,7,10,4,7,2,2,8,10,13,8,14,11,15,14,5,17,11},
{17,6,11,2,10,16,18,16,5,17,10,8,12,6,5,16,2,11,16,13,1,11,16,0,9,14,4,4,17,1,7,18,9,4,12,9,12,15,4},
{8,14,8,4,3,8,16,16,12,13,9,9,11,9,11,12,9,4,9,11,5,3,9,7,10,4,9,8,12,9,8,16,8,14,7,3,3,9,10},
{17,8,17,8,6,17,13,14,6,8,0,0,4,0,4,5,9,10,9,2,11,6,18,15,0,9,18,17,4,9,18,12,18,8,15,6,7,9,1},
{8,16,16,16,14,14,12,9,11,14,8,0,4,4,4,9,15,0,0,12,4,8,15,15,6,10,8,17,12,14,8,12,12,17,14,12,13,16,10},
{17,13,14,14,10,10,6,0,4,9,17,0,8,8,9,9,10,1,1,4,9,17,11,11,14,0,18,15,6,9,18,5,6,16,10,6,8,14,1},
{8,12,9,10,6,2,7,6,4,14,7,8,8,16,18,9,0,2,2,5,14,7,10,4,7,5,9,15,12,16,8,14,11,13,8,7,14,13,6}};
int main(int argc,char**argv){
 int K=argc>1?atoi(argv[1]):320,T=argc>2?atoi(argv[2]):20000,L=argc>3?atoi(argv[3]):180,typ=argc>4?atoi(argv[4]):9;
 vector<int> h=B;for(int j=0;j<K;j++)h.insert(h.end(),W.begin(),W.end());h.insert(h.end(),L,typ);
 vector<int> p=h;p.push_back(18);p.insert(p.end(),h.rbegin(),h.rend());
 string s(p.size(),'0');
 for(int i=0;i<(int)h.size();i++){s[i]='0'+min(9,p[i]);s[s.size()-i-1]='0'+p[i]-min(9,p[i]);}
 s[h.size()]='9';reverse(s.begin(),s.end());mpz_class n(s,10);
 vector<string>windows(T+1);vector<int>front(T+1);
 int pals=0,badclock=0;uint64_t hash=1469598103934665603ull;
 for(int t=0;t<=T;t++){
  string dec=n.get_str(10),rev=dec;reverse(rev.begin(),rev.end());
  pals+=(dec==rev);int N=dec.size();
  int f=0;
  for(;f<N/2;f++){
   int v=dec[N-1-f]-'0'+dec[f]-'0';
   int e=f<39?BP[t%8][f]:WP[t%8][(f-39)%20];
   if(v!=e)break;
  }
  if(f<80){cerr<<"root exhausted at "<<t<<"\n";return 2;}
  front[t]=f;
  for(int i=f-40;i<f+80;i++)
   windows[t]+="0123456789ABCDEFGHI"[dec[N-1-i]-'0'+dec[i]-'0'];
  if(t==T){
   for(unsigned char c:dec){hash^=c;hash*=1099511628211ull;}
   cout<<"GMP final_digits="<<N<<" h="<<f<<" pal="<<pals
       <<" clockbad="<<badclock<<" full_MSD_FNV64="<<hex<<hash<<std::dec<<"\n";
   break;
  }
  mpz_class next=n+mpz_class(rev,10);
  badclock+=(int(next.get_str(10).size())-N !=(t%2==0?1:0));n=next;
 }
 int bad=0;
 for(int t=898;t+44<=T;t++)bad+=(front[t+44]!=front[t]-10||windows[t+44]!=windows[t]);
 cout<<"GMP 44-return checks="<<T-898-44+1<<" mismatches="<<bad
     <<" h0="<<front[0]<<" h898="<<front[898]<<" hT="<<front[T]<<"\n";
 if(T==20000&&K==320&&L==180&&typ==9)
  if(front[0]!=6439||front[898]!=6234||front[T]!=1894||
     hash!=0xa2032887cdcb0524ull||pals||badclock||bad)return 1;
 return (pals||badclock||bad)?1:0;
}