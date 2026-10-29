// Base-10 synchronized two-band 480-edge matrix-pumping certificate.
// g++ -O3 -std=c++17 chain480.cpp -o chain480 && ./chain480
// Reuses only the explicit seed arrays and independent integer-digit engine.
#define main n01_unused_big_replay_main
#include "replay20k.cpp"
#undef main
using U=uint64_t;
struct Bits{U lo=0,hi=0;void add(int j){if(j<64)lo|=(1ULL<<j);else hi|=(1ULL<<(j-64));}bool has(int j)const{return j<64?(lo>>j)&1:(hi>>(j-64))&1;}void absorb(Bits b){lo|=b.lo;hi|=b.hi;}bool operator==(const Bits&b)const{return lo==b.lo&&hi==b.hi;}};
struct Matrix{array<Bits,80> row;bool operator==(const Matrix&b)const{return row==b.row;}};
static Matrix identity(){Matrix m;for(int i=0;i<80;i++)m.row[i].add(i);return m;}
static Matrix mul(const Matrix&A,const Matrix&B){
 Matrix M;
 for(int i=0;i<80;i++){
  U l=A.row[i].lo,h=A.row[i].hi;
  while(l){int j=__builtin_ctzll(l);M.row[i].absorb(B.row[j]);l&=l-1;}
  while(h){int j=64+__builtin_ctzll(h);M.row[i].absorb(B.row[j]);h&=h-1;}
 }
 return M;
}
static int state_id(int a,int h,int z,int e){return ((a*2+h)*10+z)*2+e;}
static const array<array<array<Matrix,19>,19>,2>&symbols(){
 static array<array<array<Matrix,19>,19>,2> cache=[](){
  array<array<array<Matrix,19>,19>,2> r{};
  for(int g=0;g<2;g++)for(int x=0;x<19;x++)for(int y=0;y<19;y++){
   Matrix&M=r[g][x][y];
   for(int a=0;a<2;a++)for(int h=0;h<2;h++)for(int z=0;z<10;z++)for(int e=0;e<2;e++)for(int inward=0;inward<2;inward++){
    int dl=(x+a)%10,dh=(x+inward)%10,u=(g?z:dh);
    if((x+inward)/10!=h || y!=dl+u)continue;
    M.row[state_id(a,h,z,e)].add(state_id((x+a)/10,inward,dh,e||(dl!=u)));
   }
  }return r;
 }();return cache;
}
static Matrix word(const vector<Digit>&from,const vector<Digit>&to,int g){
 if(from.size()!=to.size())throw runtime_error("word length mismatch");
 Matrix M=identity();auto& cache=symbols();
 for(size_t i=0;i<from.size();i++){
  if(from[i]>18||to[i]>18)throw runtime_error("symbol out of range");
  M=mul(M,cache[g][from[i]][to[i]]);
 }
 return M;
}
static bool accepts(const Matrix&M,int g,int center,int outcenter){
 const Bits b=M.row[state_id(0,g,g,0)];
 for(int i=0;i<80;i++)if(b.has(i)){
  int a=i/40,h=(i/20)%2,prev=(i/2)%10,e=i%2;
  if(center<0){
   if(a!=h)continue;
   if(g==0){if(outcenter!=-1)continue;} else if(outcenter!=2*prev)continue;
  }else{
   int d=(center+a)%10;
   if((center+a)/10!=h)continue;
   if(outcenter!=(g?d+prev:2*d))continue;
   if(g && d!=prev)e=1;
  }
  if(e)return true;
 }
 return false;
}
static constexpr int K=40,STEPS=480;
struct State{vector<Digit> B,W,J,V,C;int center=-1;
 bool operator==(const State&b)const{return B==b.B&&W==b.W&&J==b.J&&V==b.V&&C==b.C&&center==b.center;}
};
static vector<Digit> seed(int k){
 vector<Digit> h=B;
 for(int j=0;j<k;j++)h.insert(h.end(),W.begin(),W.end());
 h.push_back(9);
 for(int j=0;j<k;j++)h.insert(h.end(),V.begin(),V.end());
 vector<Digit>P=h;P.push_back(9);P.insert(P.end(),h.rbegin(),h.rend());return P;
}
static State extract(const vector<Digit>&P,int k,const vector<Digit>&w,const vector<Digit>&v){
 const int a=199,b=20*k-601,c=20*k+616,d=68*k-1304;
 const int n=P.size()/2;
 if(k<K||d>n || b<a || c<b || d<c)throw runtime_error("cut ordering");
 for(int j=a;j<b;j++)if(P[j]!=w[(j-a)%20])throw runtime_error("W lost");
 for(int j=c;j<d;j++)if(P[j]!=v[(j-c)%48])throw runtime_error("V lost");
 auto take=[&](int l,int r){return vector<Digit>(P.begin()+l,P.begin()+r);};
 return {take(0,a),w,take(b,c),v,take(d,n),P.size()%2?int(P[n]):-1};
}
static bool edge(const State&s,const State&u,int gamma){
 if(s.B.size()!=u.B.size() || s.J.size()!=u.J.size())throw runtime_error("literals changed size");
 Matrix M0=word(s.B,u.B,gamma),MW=word(s.W,u.W,gamma),MJ=word(s.J,u.J,gamma),MV=word(s.V,u.V,gamma);
 vector<Digit> to;
 int last=-1;
 if(s.C.size()==u.C.size()) {to=u.C;last=u.center;}
 else if(s.C.size()+1==u.C.size() && s.center>=0 && u.center<0){to=u.C;last=to.back();to.pop_back();}
 else throw runtime_error("center parity geometry failed");
 Matrix MC=word(s.C,to,gamma);
 // Every band-copy count r=k-K >= 0 is covered by idempotence plus r=0,1.
 if(!(mul(MW,MW)==MW) || !(mul(MV,MV)==MV))throw runtime_error("band-matrix not idempotent");
 Matrix a=mul(mul(M0,MJ),MC);
 Matrix b=mul(mul(mul(mul(M0,MW),MJ),MV),MC);
 return accepts(a,gamma,s.center,last) && accepts(b,gamma,s.center,last);
}
int main(){
 vector<Digit>P[3],D[3];for(int i=0;i<3;i++){P[i]=seed(K+i);D[i]=normalize_coeff(P[i]).first;}
 vector<Digit>w=W,v=V;State old{};
 for(int t=0;t<=STEPS;t++){
  State s=extract(P[0],K,w,v);
  for(int i=1;i<3;i++)if(!(extract(P[i],K+i,w,v)==s))throw runtime_error("three-seed factorization mismatch at t="+to_string(t));
  if(t>0 && !edge(old,s,(t-1)%2==0))throw runtime_error("matrix edge failed t="+to_string(t-1));
  if(t==STEPS){
   for(int i=0;i<3;i++)if(palindrome(D[i]) || normalize_coeff(P[i]).first!=D[i] || normalize_coeff(P[i]).second!=(t%2==0))throw runtime_error("final state control failed");
   cout<<"PASS: EXACT 480 successive decimal edges for ALL k>=40; both two-band matrices idempotent, independent digit replay k=40,41,42 at all 481 states; center suffix="<<s.C.size()<<"; no infinite orbit certificate\n";return 0;}
  old=move(s);
  for(int i=0;i<3;i++){
   if(palindrome(D[i]))throw runtime_error("palindrome t="+to_string(t));
   if(normalize_coeff(P[i]).first!=D[i])throw runtime_error("integer/pairword mismatch");
   if(normalize_coeff(P[i]).second!=(t%2==0))throw runtime_error("overflow mismatch");
   auto nextP=pair_word(D[i]);auto nextD=ordinary_add_reverse(D[i]);P[i].swap(nextP);D[i].swap(nextD);
  }
  w=bulk(w,t%2==0);v=bulk(v,t%2==0);
  if((t+1)%80==0)cerr<<"certified "<<(t+1)<<" edges\n";
 }
}
