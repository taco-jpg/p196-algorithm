// W38 exact finite representative screen for the rooted p12/m9 phase-0 U=(9,16,2), odd-C cell.
// The accompanying CELL_REPORT.md proves why the 120-step W9-cut window is width/centre independent.
#include <algorithm>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using V = vector<int>;
static const V B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static const V W={5,18,4,8,1,15,4,0,5};
static const V U={9,16,2};
static const V C={0,16,0}; // legal representative; its coefficients do not affect the protected W9-cut cone.
static void append(V& a,const V& b){a.insert(a.end(),b.begin(),b.end());}
static V power(const V& w,int n){V x;x.reserve(w.size()*n);for(int i=0;i<n;i++)append(x,w);return x;}
static V templ(const V& J,int q,int k){V h=B;append(h,power(W,q));append(h,J);append(h,power(U,k));V p=h;append(p,C);V r=h;reverse(r.begin(),r.end());append(p,r);return p;}
static V realize(const V& p){V d(p.size());for(size_t i=0;i<p.size()/2;i++){int hi=min(9,p[i]);d[i]=p[i]-hi;d[p.size()-1-i]=hi;}if(p.size()%2){if(p[p.size()/2]%2)throw runtime_error("odd centre coefficient");d[p.size()/2]=p[p.size()/2]/2;}if(d.empty()||d.back()==0)throw runtime_error("noncanonical source");return d;}
static V step(const V& d,int& gamma){V o;o.reserve(d.size()+1);int c=0;for(size_t i=0;i<d.size();i++){int z=d[i]+d[d.size()-1-i]+c;o.push_back(z%10);c=z/10;}gamma=c;if(c)o.push_back(c);return o;}
static V pairword(const V& d){V p(d.size());for(size_t i=0;i<d.size();i++)p[i]=d[i]+d[d.size()-1-i];return p;}
static int alt(const V& J){int a=0;for(size_t i=0;i<J.size();i++)a+=(i%2?-1:1)*J[i];return a;}
struct Stats{long long tested=0,w9=0,clock=0,returns=0,before_cut=0;map<int,long long> hist;};
int main(){
 const vector<pair<int,int>> widths={{20,20},{40,40},{80,80},{160,160}};vector<Stats> stats(widths.size());long long j3=0,j4=0;
 for(int L=3;L<=4;L++){
  const int residue=(L==3?3:8);long long lim=1;for(int i=0;i<L;i++)lim*=19;
  for(long long code=0;code<lim;code++){
   long long z=code;V J(L);for(int i=0;i<L;i++){J[i]=z%19;z/=19;}
   if((alt(J)%11+11)%11!=residue)continue;
   if(L==3)j3++;else j4++;
   for(size_t wi=0;wi<widths.size();wi++){
    const int q=widths[wi].first,k=widths[wi].second;Stats& s=stats[wi];s.tested++;
    V p=templ(J,q,k),d=realize(p);string gam;int sum_gamma=0;
    for(int t=0;t<120;t++){int g=0;V nd=step(d,g);gam+=char('0'+g);sum_gamma+=g;d.swap(nd);}
    string expected_gamma;for(int t=0;t<30;t++)expected_gamma+="1000";
    if(gam==expected_gamma&&sum_gamma==30)s.clock++;
    V got=pairword(d),wp=B;append(wp,power(W,q));
    const bool w9=got.size()>=wp.size()&&equal(wp.begin(),wp.end(),got.begin());if(w9)s.w9++;
    V h=B;append(h,power(W,q));append(h,J);append(h,power(U,k+5));V target=h;append(target,C);V rh=h;reverse(rh.begin(),rh.end());append(target,rh);
    size_t fm=0;while(fm<got.size()&&fm<target.size()&&got[fm]==target[fm])fm++;
    const bool equal_all=(got==target);if(equal_all)s.returns++;
    if(fm<wp.size()){s.before_cut++;s.hist[(int)fm-(int)wp.size()]++;}
   }
  }
 }
 const map<int,long long> expected_hist={{-25,123},{-24,283},{-23,5909},{-22,4921},{-21,570},{-20,557},{-19,53},{-18,44},{-16,5},{-15,5}};
 if(j3!=626||j4!=11844)throw runtime_error("mod-11 J gate count regression");
 const long long jraw=19LL*19*19+19LL*19*19*19;
 long long csum=0,cp=19;for(int r=1;r<=6;r++){csum+=cp;cp*=19;}
 const long long craw=10*csum;
 const long long cgated=csum;
 if(jraw!=137180||craw!=496595400||cgated!=49659540||cgated*(j3+j4)!=619254463800LL)throw runtime_error("search-space arithmetic regression");
 cout<<"SPACE raw_J="<<jraw<<" raw_C="<<craw<<" raw_pairs="<<jraw*craw<<" gated_C="<<cgated<<" gated_pairs="<<cgated*(j3+j4)<<"\n";
 cout<<"GATE_COUNTS J3="<<j3<<" J4="<<j4<<" total="<<(j3+j4)<<"\n";
 for(size_t i=0;i<widths.size();i++){
  const Stats&s=stats[i];cout<<"WIDTH q="<<widths[i].first<<" k="<<widths[i].second<<" tested="<<s.tested<<" clock="<<s.clock<<" W9_exact="<<s.w9<<" full_return="<<s.returns<<" first_mismatch_before_cut="<<s.before_cut<<"\n";
  for(auto [off,n]:s.hist)cout<<"  offset="<<off<<" count="<<n<<"\n";
  if(s.tested!=12470||s.clock!=12470||s.w9!=0||s.returns!=0||s.before_cut!=12470||s.hist!=expected_hist)throw runtime_error("screen regression at q="+to_string(widths[i].first)+" k="+to_string(widths[i].second));
  if(i&&s.hist!=stats[0].hist)throw runtime_error("width-dependent boundary histogram");
 }
 cout<<"W38_SCREEN_PASS: all 12,470 odd-centre-mod11-admissible J words fail W9 preservation at every tested width; exact local-window histogram is width-invariant.\n";
}
