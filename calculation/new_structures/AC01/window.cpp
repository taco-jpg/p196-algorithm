// AC01 exact centre-window solver with induction-checked escape fallback.
// Outside coefficients and carry ports match reference at EVERY accepted step.
#define AC01_NO_MAIN
#include "census.cpp"
struct Window {
 static constexpr int R=80,G=6;
 int u,n,q,k;Runner full;
 vector<vector<uint8_t>> p,digit;vector<vector<uint8_t>> carry;
 vector<int> lo,hi,gamma;uint64_t all=0,hits=0,fb=0,hash=1469598103934665603ULL;
 Window(int uu,int nn,int qq=14,int kk=100):u(uu),n(nn),q(qq),k(kk),full(uu,nn,qq,kk){
    vector<int> C(n,0);vector<int> source(full.coeff.begin(),full.coeff.end());
    int centre=int(source.size())/2;for(int i=0;i<n;i++)source[centre-n/2+i]=C[i];
    vector<uint8_t> digits(source.size());
    for(int i=0;i<int(source.size())/2;i++){
      int x=source[i],hi=std::min(9,x);digits[i]=uint8_t(x-hi);digits[source.size()-1-i]=uint8_t(hi);
    }
    if(source.size()&1)digits[source.size()/2]=uint8_t(source[source.size()/2]/2);
    for(int t=0;t<=120;t++){
      int len=digits.size();
      vector<uint8_t> pair(len),cr(len+1,0);
      for(int i=0;i<len;i++){pair[i]=digits[i]+digits[len-1-i];int s=int(pair[i])+cr[i];cr[i+1]=uint8_t(s>=10);}
      p.push_back(std::move(pair));carry.push_back(std::move(cr));
      int win=2*R+(len&1),l=(len-win)/2;
      lo.push_back(l);hi.push_back(l+win);
      if(t==120)break;
      vector<uint8_t> next(len+1,0);int carryx=0;
      for(int i=0;i<len;i++){
        int s=int(digits[i])+int(digits[len-1-i])+carryx;
        next[i]=uint8_t(s%10);carryx=s/10;
      }
      next.resize(len+carryx);if(carryx)next[len]=1;
      gamma.push_back(carryx);digits.swap(next);
    }
 }
 bool check(const vector<int>& C){
   int centre=p[0].size()/2;
   vector<uint8_t> cur(p[0].begin()+lo[0],p[0].begin()+hi[0]);
   for(int i=0;i<n;i++)cur[centre-n/2+i-lo[0]]=uint8_t(C[i]);
   uint8_t dig[2*R+2*G+32];vector<uint8_t> nx;
   bool escape=false;
   for(int t=0;t<120;t++){
     int l=lo[t],h=hi[t],start=l-G-5,end=h+G+5;
     int c=carry[t][start];
     for(int j=start;j<end;j++){
        int x=(j>=l&&j<h)?cur[j-l]:p[t][j];
        int s=x+c;dig[j-start]=uint8_t(s%10);c=s/10;
     }
     if(c!=carry[t][end]){escape=true;break;}
     int nl=lo[t+1],nh=hi[t+1],nstart=nl-G,nend=nh+G;
     nx.assign(nh-nl,0);
     for(int j=nstart;j<nend;j++){
       int mirror=int(p[t].size())-1-j+gamma[t];
       if(j<start||j>=end||mirror<start||mirror>=end){escape=true;break;}
       int v=int(dig[j-start])+int(dig[mirror-start]);
       if(j<nl||j>=nh){if(v!=p[t+1][j]){escape=true;break;}}
       else nx[j-nl]=uint8_t(v);
     }
     if(escape)break;
     cur.swap(nx);
   }
   bool ok=false;
   if(escape){fb++;ok=full.check(C);}else{
      const int N=int(p[120].size()),mid=N/2,rad=122+n+30;
      const int outHalf=(N-n)/2;
      ok=true;
      for(int i=mid-rad;i<=mid+rad;i++){
        int v=(i>=lo[120]&&i<hi[120])?cur[i-lo[120]]:p[120][i];
        int x=std::min(i,N-1-i);
        int want;
        int cutoff=int(full.coeff.size()-n)/2;
        if(x<outHalf){if(x<cutoff)want=full.coeff[x];else want=U[u][(x-cutoff)%3];}
        else want=C[x-outHalf];
        if(v!=want){ok=false;break;}
      }
   }
   all++; if(ok){hits++;cerr<<"CENTRE RETURN U="<<u<<" C="<<n<<" :";for(int v:C)cerr<<v<<',';cerr<<'\n';}
   hash^= uint64_t(ok)+31ULL*uint64_t(escape);hash*=1099511628211ULL;
   return ok;
 }
};
int main(int argc,char**argv){
 if(argc<5){cerr<<"usage: window Uidx C_length offset limit [q k stride audit]\n";return 2;}
 int u=atoi(argv[1]),n=atoi(argv[2]);uint64_t off=stoull(argv[3]),limit=stoull(argv[4]);int q=argc>5?atoi(argv[5]):14,k=argc>6?atoi(argv[6]):100;
 if(u<0||u>2||n<1||n>24)throw runtime_error("bad U or C length");
 uint64_t total=ipow(19,n/2)*(n&1?10:1);if(off>total)throw runtime_error("bad offset");limit=min(limit,total-off);
 Window window(u,n,q,k);vector<int>C(n);
 for(uint64_t j=off;j<off+limit;j++){
  uint64_t x=(off+(j-off)*(argc>7?stoull(argv[7]):1ULL))%total;int h=n/2;if(n&1){C[h]=2*int(x%10);x/=10;}
  for(int i=0;i<h;i++){C[i]=C[n-1-i]=int(x%19);x/=19;}
  bool win=window.check(C);
  if(argc>8 && std::string(argv[8])=="audit") { bool direct=window.full.check(C); if(win!=direct){cerr<<"WINDOW/DIRECT DISAGREE id="<<j<<"\n";return 3;} }
 }
 cout<<"CELL U="<<u<<" C="<<n<<" offset="<<off<<" checked="<<window.all<<" total="<<total<<" matches="<<window.hits<<" full_fallback="<<window.fb<<" hash64="<<hex<<window.hash<<dec<<" q="<<q<<" k="<<k<<" stride="<<(argc>7?stoull(argv[7]):1ULL)<<'\n';
}
