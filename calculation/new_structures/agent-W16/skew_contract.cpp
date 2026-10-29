// W16: two independently sized, phase-locked bulk domains, decimal reverse-add.
// Build: g++ -O3 -std=c++17 skew_contract.cpp -o skew_contract
// Run: ./skew_contract 440 530 20000
#include <bits/stdc++.h>
using namespace std;
using D=uint8_t; using Word=vector<D>;
static const Word B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const Word W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
static const Word V={4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,13,9,7,3,13,10,4,13,5,1,9,4,11,6,16,3,7,7,12,4,2,13,2,15,10,10,9,3};
static pair<Word,int> normalize(const Word& p){
 Word d;d.reserve(p.size()+1);int c=0;
 for(D x:p){int z=x+c;d.push_back(z%10);c=z/10;}
 if(c)d.push_back(c);return {move(d),c};
}
static Word addreverse(const Word& d){
 Word a; a.reserve(d.size()+1);int c=0;size_t n=d.size();
 for(size_t i=0;i<n;i++){int z=d[i]+d[n-1-i]+c;a.push_back(z%10);c=z/10;}
 if(c)a.push_back(c);return a;
}
static Word pairs(const Word& d){Word p(d.size());for(size_t i=0;i<d.size();i++)p[i]=d[i]+d[d.size()-1-i];return p;}
static Word bulk(const Word& w,int gamma){
 int c=0;Word low(w.size());
 // For any non-neutral W, carry after each block converges to a fixed point.
 auto fixed=[&](const Word& z){for(int a=0;a<=1;a++){int cc=a;Word out;for(D v:z){int x=v+cc;out.push_back(x%10);cc=x/10;}if(cc==a)return out;}throw runtime_error("no fixed carry");};
 low=fixed(w);Word rev=w;reverse(rev.begin(),rev.end());Word high=fixed(rev);reverse(high.begin(),high.end());
 Word next(w.size());int m=(int)w.size();for(int j=0;j<m;j++)next[j]=low[j]+high[(j-gamma+m)%m];return next;
}
static bool pal(const Word& d){for(size_t i=0,n=d.size();i<n/2;i++)if(d[i]!=d[n-1-i])return false;return true;}
static uint64_t hashdigits(const Word& d){uint64_t h=1469598103934665603ULL;for(D x:d){h^=x;h*=1099511628211ULL;}return h;}

static void must(bool ok, const string& why, int t){
 if(!ok){cerr<<"contract failure t="<<t<<" reason="<<why<<"\n";exit(20);}
}
static Word ins(const Word& p,size_t i,const Word& w){Word x=p;x.insert(x.begin()+i,w.begin(),w.end());return x;}
static Word pump(const Word& p,const vector<size_t>& cuts,const vector<Word>& w,const vector<int>& delta){
 Word x=p;
 for(int j=(int)cuts.size()-1;j>=0;--j){
   for(int z=0;z<delta[j];z++){
     Word rev=w[j];reverse(rev.begin(),rev.end());
     x=ins(x,x.size()-cuts[j],rev);x=ins(x,cuts[j],w[j]);
   }
 }
 return x;
}
static Word contract_step(const Word& p, const Word& d, size_t i, int m, int t){
 const size_t n=p.size(),nd=d.size(),r=n-i,h=nd-i;
 must(i+m<=n/2 && h+m<=n,"cuts OOB",t);
 int carry=0;Word C(n+1);C[0]=0;
 for(size_t x=0;x<n;x++){carry=(p[x]+carry)/10;C[x+1]=carry;}
 Word low(p.begin()+i,p.begin()+i+m);
 Word high(p.begin()+h,p.begin()+h+m);
 Word reversed=low;reverse(reversed.begin(),reversed.end());
 must(equal(reversed.begin(),reversed.end(),p.begin()+r),"mirror band",t);
 if(nd!=n){ // gamma=1, high cut shifts by one, insert commutes with periodic region.
   must(r+m<n,"right overrun",t);
   must(p[r]==p[r+m],"gamma cut phase slip",t);
 }
 auto emit=[&](const Word& w,int c){Word o;for(D a:w){int z=a+c;o.push_back(z%10);c=z/10;}return pair<Word,int>(o,c);};
 auto [dl,cl]=emit(low,C[i]);auto [dh,ch]=emit(high,C[h]);
 must(cl==C[i] && ch==C[h],"carry loop",t);
 Word v(m);for(int x=0;x<m;x++)v[x]=dl[x]+dh[m-x-1];
 return v;
}
int main(int argc,char**argv){
 int kw=argc>1?stoi(argv[1]):440,kv=argc>2?stoi(argv[2]):530,T=argc>3?stoi(argv[3]):20000;
 if(kw<400||kv<400){cerr<<"kw and kv >=400\n";return 2;}
 Word half=B;
 for(int k=0;k<kw;k++)half.insert(half.end(),W.begin(),W.end());
 half.push_back(9);
 for(int k=0;k<kv;k++)half.insert(half.end(),V.begin(),V.end());
 Word p=half;p.push_back(9);p.insert(p.end(),half.rbegin(),half.rend());
 Word d=normalize(p).first,a=W,b=V;
 size_t w0=B.size()+400,w1=B.size()+1400;
 size_t vbase=B.size()+20*(size_t)kw+1,v0=vbase+15000,v1=vbase+15960;
 if(v1>=half.size())throw runtime_error("bad V window");
 unsigned long long total_checks=0;
 for(int t=0;t<=T;t++){
  if(pal(d)){cerr<<"pal t="<<t<<"\n";return 3;}
  if(p.size()/2<=v1){cerr<<"V window lost t="<<t<<"\n";return 4;}
  for(size_t j=w0;j<w1;j++)if(p[j]!=a[(j-B.size())%a.size()]){cerr<<"W mismatch t="<<t<<" j="<<j<<"\n";return 5;}
  for(size_t j=v0;j<v1;j++)if(p[j]!=b[(j-vbase)%b.size()]){cerr<<"V mismatch t="<<t<<" j="<<j<<"\n";return 6;}
  auto norm=normalize(p);int gamma=norm.second;
  if(norm.first!=d){cerr<<"norm mismatch t="<<t<<"\n";return 7;}
  if(gamma!=((t&1)==0)){cerr<<"clock mismatch t="<<t<<" gamma="<<gamma<<"\n";return 8;}
  size_t cut1=B.size()+800,cut2=vbase+15360;
  size_t anchor=0;while(anchor<cut1 && d[anchor]==d[d.size()-1-anchor])anchor++;
  must(anchor<cut1,"no external nonpalindrome witness",t);
  if(t==T)break;
  Word vW=contract_step(p,d,cut1,20,t);
  Word vV=contract_step(p,d,cut2,48,t);
  must(vW==bulk(a,gamma) && vV==bulk(b,gamma),"bulk transducer disagree",t);
  if(t==0 || t==1 || t==8 || t==88 || t==1000 || t==10000 || t==T-1){
      vector<size_t> cuts={cut1,cut2};vector<Word> ws={Word(p.begin()+cut1,p.begin()+cut1+20),Word(p.begin()+cut2,p.begin()+cut2+48)};
      Word pp=pump(p,cuts,ws,{2,1}); Word dd=normalize(pp).first;
      Word qq=pairs(d);Word expected=pump(qq,cuts,{vW,vV},{2,1});
      must(pairs(dd)==expected,"full two-counter pumping oracle",t);
      must(!pal(dd),"pumped palindrome",t);
  }
  Word d1=addreverse(d),p1=pairs(d);
  d.swap(d1);p.swap(p1);a=bulk(a,gamma);b=bulk(b,gamma);total_checks++;
 }
 cout<<"PASS kw="<<kw<<" kv="<<kv<<" steps="<<T<<" seed_digits="<<2*half.size()+2
     <<" final_digits="<<d.size()<<" asymmetry_cells="<<20*kw-48*kv
     <<" window20="<<w1-w0<<" window48="<<v1-v0
     <<" nonpal_states="<<T+1<<" digit_steps="<<total_checks<<" fnv64="<<hex<<hashdigits(d)<<dec<<"\n";
 return 0;
}
