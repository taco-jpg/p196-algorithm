// Exact 73-phase, two-counter insertion/carry-port certificate for a rooted base-10 rec2/W48+U3 wall repair.
// All independent exponent extensions follow from the two-ended carry pumping lemma (see report).
// Full symmetric pairword normalizer, with explicit forward/reverse carry ports.
#include <bits/stdc++.h>
using namespace std;using R=vector<int>;
vector<R> read(string p){ifstream f(p);string s;vector<R>out;while(getline(f,s)){istringstream ss(s);string x;R row;while(getline(ss,x,','))row.push_back(stoi(x));out.push_back(row);}return out;}
R U={10,4,10};
R make(const R&B,const R&W,int q,int k,int d){R h=B;for(int i=0;i<q;i++)h.insert(h.end(),W.begin(),W.end());h.push_back(3);h.push_back(4);for(int i=0;i<k;i++)h.insert(h.end(),U.begin(),U.end());h.push_back(10);h.push_back(4);int j=11+q*48;h[j+2]+=d;h[j+4]-=d;R p=h;for(int i=(int)h.size()-2;i>=0;i--)p.push_back(h[i]);return p;}
struct Norm{R dig,carry,pair;int overflow;};
Norm norm(const R&p){Norm o;int n=p.size();o.carry.assign(n+2,0);for(int j=0;j<n;j++){int z=p[j]+o.carry[j];o.dig.push_back(z%10);o.carry[j+1]=z/10;}o.overflow=o.carry[n];if(o.overflow)o.dig.push_back(o.overflow);int m=o.dig.size();o.pair.resize(m);for(int j=0;j<m;j++)o.pair[j]=o.dig[j]+o.dig[m-1-j];return o;}
struct Check {int errors=0;string message;};
Check insertion(const R&small,const R&big,int cut,int block,int time,const string&label){
 Check z;int n=small.size(),m=big.size(),h=(n+1)/2;
 auto bad=[&](string s){z.errors++;if(z.message.empty())z.message=label+" t="+to_string(time)+" "+s;};
 if(m!=n+2*block)return bad("length mismatch"),z;
 if(cut<block || cut+2*block>h)return bad("cut not in 3-block interior"),z;
 for(int j=0;j<cut;j++)if(small[j]!=big[j]){bad("pre-insertion pairword differs at "+to_string(j));break;}
 for(int j=cut;j<h;j++)if(small[j]!=big[j+block]){bad("post-insertion pairword differs at "+to_string(j));break;}
 for(int j=0;j<block;j++){
  if(big[cut+j]!=small[cut+j]){bad("inserted word != existing word at "+to_string(j));break;}
 }
 for(int j=0;j<block;j++)if(small[cut+j]!=small[cut-block+j] || small[cut+j]!=small[cut+block+j]){bad("neighbor period mismatch at "+to_string(j));break;}
 // actual finite arithmetic carries must be fixed points on both ends of inserted block
 auto a=norm(small),b=norm(big);
 int inLow=b.carry[cut],outLow=b.carry[cut+block];
 int inHigh=b.carry[m-cut-block],outHigh=b.carry[m-cut];
 if(inLow!=outLow || inHigh!=outHigh){bad("inserted low/high ports not stationary: low "+to_string(inLow)+"/"+to_string(outLow)+" high "+to_string(inHigh)+"/"+to_string(outHigh));}
 if(inLow!=a.carry[cut]||inHigh!=a.carry[n-cut])bad("small-vs-large inlet carry mismatch");
 if(a.overflow!=b.overflow)bad("overflow mismatch");
 return z;
}
int main(int argc,char**argv){if(argc!=6){cerr<<"usage: repair72_pump rows.csv B.csv q k d\n";return 2;}auto W=read(argv[1]),B=read(argv[2]);if(W.size()!=8||B.size()!=8)return 2;int q=atoi(argv[3]),k=atoi(argv[4]),d=atoi(argv[5]);if(q<5||k<34||(d!=-5&&d!=4))return 2;int wCut=11+48*2;int uCut=11+48*q+2+3*(k/2);R x=make(B[0],W[0],q,k,d),xw=make(B[0],W[0],q+1,k,d),xu=make(B[0],W[0],q,k+1,d),xwu=make(B[0],W[0],q+1,k+1,d);int checkW=0,checkU=0,checkWU=0,rootfail=0,gammafail=0,oddFail=0;vector<int> fronts;
 for(int t=0;t<=72;t++){
  auto w=insertion(x,xw,wCut,48,t,"W48"),u=insertion(x,xu,uCut,3,t,"U3");auto wu1=insertion(xw,xwu,uCut+48,3,t,"WU via U"),wu2=insertion(xu,xwu,wCut,48,t,"WU via W");if(wu1.errors||wu2.errors){checkWU++;if(checkWU<=3)cerr<<(wu1.errors?wu1.message:wu2.message)<<"\n";}if(w.errors){checkW++;if(checkW<=3)cerr<<w.message<<'\n';}if(u.errors){checkU++;if(checkU<=3)cerr<<u.message<<'\n';}
  bool oddWitness=false;for(int j=0;j<11;j++)if(x[j]&1)oddWitness=true;if(!oddWitness)oddFail++;for(int j=0;j<11;j++)if(x[j]!=B[t%8][j]&&rootfail==0){rootfail=t+1;cerr<<"root fail "<<t<<" j="<<j<<'\n';}
  if(t%8==0){int h=(x.size()+1)/2,j=11;while(j<h&&x[j]==W[t%8][(j-11)%48])j++;fronts.push_back(j-11-48*q);}
  if(t==72)break;
  auto y=norm(x),yw=norm(xw),yu=norm(xu),ywu=norm(xwu);
  if(y.overflow!=(t%2==0)||yw.overflow!=y.overflow||yu.overflow!=y.overflow||ywu.overflow!=y.overflow)gammafail++;
  x=move(y.pair);xw=move(yw.pair);xu=move(yu.pair);xwu=move(ywu.pair);
 }
 cout<<"q="<<q<<" k="<<k<<" d="<<d<<" WphaseErrors="<<checkW<<" UphaseErrors="<<checkU<<" CornerErrors="<<checkWU<<" oddFail="<<oddFail<<" rootFail="<<rootfail<<" gammaFail="<<gammafail<<" terminalFront="<<fronts.back()<<" fronts=";
 for(int v:fronts){cout<<v<<',';}cout<<'\n';
 return (checkW||checkU||checkWU||oddFail||rootfail||gammafail||fronts.back()!=0)?1:0;
}