// W22: Exact antiphase neutral-9 pumping lemma, checked on every step of 20k trajectory.
// g++ -O3 -std=c++17 hinge_pump.cpp -o hinge_pump && ./hinge_pump
#include <bits/stdc++.h>
using namespace std; using V=vector<uint8_t>;
V base(int A=14000,int L=8000,int C=16000){V p;p.insert(p.end(),A,8);p.insert(p.end(),L,9);p.insert(p.end(),C,10);p.insert(p.end(),L,9);p.insert(p.end(),A,8);return p;}
V insert9(const V&p,int j,int k=1){int n=p.size();assert(n>2*j);V q;q.reserve(n+2*k);q.insert(q.end(),p.begin(),p.begin()+j);q.insert(q.end(),k,9);q.insert(q.end(),p.begin()+j,p.begin()+n-j);q.insert(q.end(),k,9);q.insert(q.end(),p.begin()+n-j,p.end());return q;}
V step(const V&p,int&gamma,int j=-1,int *cj=nullptr,int *cu=nullptr){int c=0;V d;d.reserve(p.size()+1);for(int i=0;i<(int)p.size();i++){if(j>=0&&i==j)*cj=c;if(j>=0&&i==int(p.size())-j)*cu=c;int z=int(p[i])+c;c=z/10;d.push_back(z%10);}gamma=c;if(c)d.push_back(c);int n=d.size();V q(n);for(int i=0;i<n;i++)q[i]=d[i]+d[n-i-1];return q;}
pair<int,int> first9(const V&p){int n=p.size()/2,best=0,st=0,s=0;for(int i=0;i<=n;i++){if(i<n&&p[i]==9)continue;if(i-s>best){best=i-s;st=s;}s=i+1;}return {st,best};}
int main(int argc,char**argv){const int H=argc>1?atoi(argv[1]):20000,j=21750;V p=base();int opp=0,comm=0,g1=0,minmargin=INT_MAX,maxstart=0,minend=INT_MAX;
 for(int t=0;t<H;t++){
  auto [start,len]=first9(p);int end=start+len;maxstart=max(maxstart,start);minend=min(minend,end);
  int margin=min(j-start,end-1-j);minmargin=min(minmargin,margin);
  if(margin<2){cerr<<"FAIL fixed-site margin at t="<<t<<" start="<<start<<" end="<<end<<"\n";return 2;}
  int g,cl=-1,cu=-1;V q=step(p,g,j,&cl,&cu);g1+=g;
  if(cl+cu!=1){cerr<<"FAIL charge at t="<<t<<" pair="<<cl<<","<<cu<<"\n";return 3;}
  opp++;
  V pi=insert9(p,j);int gi;V qi=step(pi,gi);V expect=insert9(q,j);
  if(g!=gi||qi!=expect){cerr<<"FAIL pump at t="<<t<<" g="<<g<<","<<gi<<"\n";return 4;}
  comm++;
  if(t==0||t==1||t==2||t==5000||t==10000||t==15000||t==19999){
   int g37;V q37=step(insert9(p,j,37),g37);
   if(g37!=g||q37!=insert9(q,j,37)){cerr<<"FAIL k37 t="<<t<<"\n";return 5;}
   cout<<"CHECK t="<<t<<" carry="<<cl<<","<<cu<<" margin="<<margin<<" gamma="<<g<<" k37=PASS\n";
  }
  p.swap(q);
 }
 auto [st,nine]=first9(p);maxstart=max(maxstart,st);minend=min(minend,st+nine);
 if(!(st+2<=j&&j+2<st+nine)){cerr<<"FAIL final margin\n";return 6;}
 if(H==20000 && (opp!=20000||comm!=20000||g1!=8296||maxstart!=21549||minend!=22000)){cerr<<"FAIL expected ledger\n";return 7;}
 V bad=base(60,80,120);fill(bad.begin()+60+80,bad.begin()+60+80+120,8);int gb;V qb=step(bad,gb);V bi=insert9(bad,100);int gi;V qi=step(bi,gi);V be=insert9(qb,100);
 if(qi==be){cerr<<"FAIL negative control\n";return 8;}
 cout<<"PUMP_PASS steps="<<H<<" opposed="<<opp<<" commute="<<comm<<" gamma="<<g1<<" max_start="<<maxstart<<" min_end="<<minend<<" invariant_fixed_j="<<j<<" min_margin="<<minmargin<<" negative=PASS\n";
}
