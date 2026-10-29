// Phase-dependent independent band insertions on real decimal pairword orbits.
#define main X20_unused
#include "two_counter.cpp"
#undef main
static V pumped(const V&p,const V&w,const V&v,int m,int mode){int z=p.size()/2;V h(p.begin(),p.begin()+z);size_t wx=39+600, vx=39+20*m+1+15168;
 if((mode&2)&&vx>h.size())throw runtime_error("V cut past middle");
 if(mode&1){h.insert(h.begin()+wx,w.begin(),w.end());vx+=20;}
 if(mode&2)h.insert(h.begin()+vx,v.begin(),v.end());
 V o=h;if(p.size()%2)o.push_back(p[z]);o.insert(o.end(),h.rbegin(),h.rend());return o;}
static int carryAfter(const V&w,int c){for(int x:w)c=(x+c)/10;return c;}
static void guards(const V&p,const V&w,const V&v,int m){
 vector<int> carry(p.size()+1);for(size_t i=0;i<p.size();i++)carry[i+1]=(p[i]+carry[i])/10;
 for(auto [x,block]: vector<pair<int,V>>{{39+600,w},{39+20*m+1+15168,v}}){
  V back=block;reverse(back.begin(),back.end());
  if(carryAfter(block,carry[x])!=carry[x])throw runtime_error("low carry not saturated");
  int high=p.size()-x;
  if(carryAfter(back,carry[high])!=carry[high])throw runtime_error("high carry not saturated");
  for(int j=-2*(int)block.size();j<2*(int)block.size();j++){
   int at=x+j;
   // At each cut we are strictly inside a periodic run, not across its boundary.
   if(p[at]!=block[(j%(int)block.size()+(int)block.size())%block.size()])throw runtime_error("cut window is not periodic");
  }
 }
}
static int firstodd(const V&p,int cap){for(int j=0;j<cap;j++)if(p[j]%2)return j;return -1;}
int main(int argc,char**argv){int m=argc>1?stoi(argv[1]):427,n=argc>2?stoi(argv[2]):509,N=argc>3?stoi(argv[3]):20000,start=argc>4?stoi(argv[4]):0;V p=seed(m,n),d=norm(p).first,w=W,v=Q;int maxFirstOdd=-1;for(int t=0;t<N;t++){
 if(!equal(p.begin(),p.begin()+p.size()/2,p.rbegin()))throw runtime_error("not symmetric pairword");
 guards(p,w,v,m);int odd=firstodd(p,39);if(odd==-1){cerr<<"NO exterior odd at t="<<t<<"\n";return 9;}maxFirstOdd=max(maxFirstOdd,odd);
 int gam=norm(p).second;
 auto nextP=pairs(d),nextD=add(d),wn=bulk(w,gam),vn=bulk(v,gam);
 for(int mode=1;mode<=3;mode++){
  if(t<start)continue;
  V in=pumped(p,w,v,m,mode);
  auto normed=norm(in);if(normed.second!=gam){cerr<<"GAM shift mode="<<mode<<" t="<<t<<"\n";return 4;}
  auto observed=pairs(normed.first),target=pumped(nextP,wn,vn,m,mode);
  if(observed!=target){size_t j=0;while(j<min(observed.size(),target.size())&&observed[j]==target[j])j++;cerr<<"FAIL mode="<<mode<<" t="<<t<<" at j="<<j<<" obs="<<observed.size()<<" target="<<target.size()<<"\n";return 5;}
 }
 p.swap(nextP);d.swap(nextD);w.swap(wn);v.swap(vn);
 if((t+1)%2000==0)cerr<<"X20 pump commutation "<<t+1<<" / "<<N<<"; max first exterior odd index "<<maxFirstOdd<<"\n";
 }
 if(firstodd(p,39)==-1)throw runtime_error("terminal safety witness lost");
 cout<<"PASS "<<N<<" exact W/V/W+V pump identities for m="<<m<<" n="<<n<<" (all three pump identities for each t>=start), max first odd index="<<maxFirstOdd<<"\n";
}
