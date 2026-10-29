// Independent real decimal digit-list RAA; check moving pairword frontier.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
#include "phase.h"
using namespace std;
vector<unsigned char> seed(int k,int core){
 vector<int> p(B0.begin(),B0.end());
 for(int i=0;i<k;i++)p.insert(p.end(),W0.begin(),W0.end());
 if(core==1){p.push_back(0);p.push_back(18);}
 if(core==2){p.push_back(2);p.push_back(4);}
 if(core==3){p.push_back(9);p.push_back(6);}
 vector<unsigned char>d(p.size()*2);
 for(size_t i=0;i<p.size();i++){d[i]=p[i]/2;d[d.size()-1-i]=p[i]-d[i];}
 return d;
}
void step(vector<unsigned char>&d){
 vector<unsigned char>out(d.size()+1);int c=0;
 for(size_t i=0,j=d.size()-1;i<d.size();i++,j--){int v=d[i]+d[j]+c;out[i]=v%10;c=v/10;}
 if(c)out[d.size()]=c;else out.pop_back();d.swap(out);
}
string window(const vector<unsigned char>&d,int h){
 string s;s.reserve(120);int n=(int)d.size();
 for(int j=-40;j<80;j++){int ix=h+j;
   if(ix<0||ix>=n/2){s+='!';continue;}
   s+="0123456789ABCDEFGHI"[d[ix]+d[n-1-ix]];
 }
 return s;
}
int first_bad(const vector<unsigned char>&d,int t){
 int half=(int)d.size()/2;
 for(int i=0;i<half;i++){
  int w=i<39?PHASE_B[t%8][i]:PHASE_W[t%8][(i-39)%20];
  if(d[i]+d[d.size()-1-i]!=w)return i;
 }
 return half;
}
uint64_t fnv(const string&s){
 uint64_t h=1469598103934665603ull;
 for(auto x:s){h^=(unsigned char)x;h*=1099511628211ull;}
 return h;
}
int main(int argc,char**argv){
 const int k=argc>1?atoi(argv[1]):300,T=argc>2?atoi(argv[2]):20000,
 core=argc>3?atoi(argv[3]):0,start=argc>4?atoi(argv[4]):1082;
 if(k<1||T<start+88||core<0||core>3)return 2;
 vector<unsigned char>d=seed(k,core);
 array<string,89>contexts;array<int,89>hs{};array<int,22>prior_loss{};
 int checks=0,losschecks=0,prev_h=-1;
 for(int t=0;t<=T;t++){
  int h=first_bad(d,t);
  if(h<59){cerr<<"exterior loss t="<<t<<"\n";return 3;}
  if(prev_h>=0){
      int delta=prev_h-h,i=t-1;
      if(i>=62 && delta!=prior_loss[(i-22)%22]){
          cerr<<"loss 22-cycle mismatch t="<<t<<" delta="<<delta<<"\n";return 6;
      }
      if(i>=62)losschecks++;
      prior_loss[i%22]=delta;
  }
  prev_h=h;
  string s=window(d,h);
  if(s.find('!')!=string::npos&&t>=start){
    cerr<<"window out of bounds "<<t<<"\n";return 4;
  }
  if(t>=start+88){
    int j=(t-88)%89;
    if(hs[j]-h!=20||contexts[j]!=s){
      cerr<<"glider mismatch t="<<t<<" previous="<<t-88
          <<" old_h="<<hs[j]<<" h="<<h<<"\n";return 5;
    }
    checks++;
  }
  contexts[t%89]=s;hs[t%89]=h;
  if(t==1100||t==1188||t==T)
    cout<<"t="<<t<<" h="<<h<<" window_fnv64="<<hex<<fnv(s)<<dec<<"\n";
  if(t<T)step(d);
 }
 cout<<"PASS k="<<k<<" core="<<core<<" steps="<<T
     <<" glider_pairs="<<checks<<" window=120 temporal_period=88 spatial_shift=-20"
     <<" first_valid_previous_t="<<start<<" loss22_checks="<<losschecks<<"\n";
 return 0;
}
