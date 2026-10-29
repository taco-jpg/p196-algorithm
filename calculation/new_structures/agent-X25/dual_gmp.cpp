// X25: independent GMP n+reverse(n) checks complete pairwords and both moving fronts.
#define main x25_collision_unused_main
#include "collision.cpp"
#undef main
#include <gmpxx.h>
mpz_class realize(const Word& p){int n=p.size();string d(n,'0');for(int i=0;i<n/2;i++){int z=p[i],hi=i?max(0,z-9):max(1,z-9);d[i]=char('0'+z-hi);d[n-1-i]=char('0'+hi);}if(n%2){if(p[n/2]%2)abort();d[n/2]=char('0'+p[n/2]/2);}reverse(d.begin(),d.end());return mpz_class(d,10);}
Word from_big(const mpz_class& n){string s=n.get_str();Word out(s.size());for(int i=0;i<(int)s.size();i++)out[i]=(s[i]-'0')+(s[s.size()-1-i]-'0');return out;}
bool pal(const mpz_class& n){string s=n.get_str();return equal(s.begin(),s.begin()+s.size()/2,s.rbegin());}
void revadd(mpz_class &n){string s=n.get_str();reverse(s.begin(),s.end());n+=mpz_class(s,10);}
struct R{int al,ar,dl,dr;string alw,arw,dlw,drw;};
string win(const Word& p,int edge,int lo,int hi){string s;for(int d=lo;d<=hi;d++)s.push_back(char(p[edge+d]));return s;}
int main(int argc,char**argv){
 int q=argc>1?atoi(argv[1]):140,x=argc>2?atoi(argv[2]):960,H=argc>3?atoi(argv[3]):1792;
 Word bg=seed(q),a=patch(bg,x,A),d=patch(bg,x,D);
 mpz_class n0=realize(bg),n1=realize(a),n2=realize(d);vector<R> rows;
 for(int t=0;t<=H;t++){
  if(from_big(n0)!=bg||from_big(n1)!=a||from_big(n2)!=d){cerr<<"BIGINT FULL WORD mismatch t="<<t<<"\n";return 2;}
  if(pal(n0)||pal(n1)||pal(n2)){cerr<<"PALINDROME t="<<t<<"\n";return 2;}
  if((int)bg.size()!=2*(39+20*q)+7+(t+1)/2){cerr<<"length t="<<t<<"\n";return 2;}
  int al=bg.size(),ar=-1,dl=bg.size(),dr=-1;
  for(int j=0;j<(int)bg.size()/2;j++){if(a[j]!=bg[j])al=min(al,j),ar=max(ar,j);if(d[j]!=bg[j])dl=min(dl,j),dr=max(dr,j);}
  if(al<80||dl<80||ar+80>=bg.size()/2||dr+80>=bg.size()/2)abort();
  rows.push_back({al,ar,dl,dr,win(a,al,-80,20),win(a,ar,-20,80),win(d,dl,-80,20),win(d,dr,-20,80)});
  if(t<H){int g=step(bg),ga=step(a),gd=step(d);if(g!=ga||g!=gd||g!=(t%2==0))abort();revadd(n0);revadd(n1);revadd(n2);}
 }
 auto verify=[&](string species,int delay,int drift,int expected_last){
  int good=0,lastbad=-1;
  for(int t=0;t+delay<=H;t++){
   auto &u=rows[t],&v=rows[t+delay];
   bool ok=species=="AR"?(v.ar-u.ar==drift&&u.arw==v.arw):
           species=="DR"?(v.dr-u.dr==drift&&u.drw==v.drw):
           species=="AL"?(v.al-u.al==drift&&u.alw==v.alw):
                         (v.dl-u.dl==drift&&u.dlw==v.dlw);
   if(ok)good++;else lastbad=t;
  }
  cout<<species<<" shift_time="<<delay<<" shift_space="<<drift<<" good="<<good<<" lastbad="<<lastbad<<" stable_from="<<lastbad+1<<"\n";
  if(expected_last>=0&&lastbad!=expected_last)abort();
 };
 if(q==140&&x==960&&H==1792){
  verify("AL",88,-20,396);verify("DL",88,-20,241);
  verify("AR",792,540,421);verify("DR",792,540,493);
 }else{verify("AL",88,-20,-1);verify("DL",88,-20,-1);verify("AR",792,540,-1);verify("DR",792,540,-1);}
 cout<<"GMP_ALL_PAIRWORDS_PASS seeds=3 states="<<H+1<<" palindrome_hits=0\n";
}
