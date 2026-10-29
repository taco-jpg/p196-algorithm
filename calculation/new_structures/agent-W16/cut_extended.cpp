// W16: two independently pumped periodic bands with a deeper, phase-respecting cut.
// Reproduce: g++ -std=c++17 -O3 cut_extended.cpp -o /tmp/w16_cut
//            /tmp/w16_cut 440 530 33456 40 427
#define main w16_original_main
#include "skew_contract.cpp"
#undef main
int main(int argc,char**argv){
 const int kw=argc>1?stoi(argv[1]):440,kv=argc>2?stoi(argv[2]):530;
 const int T=argc>3?stoi(argv[3]):33456;
 const int jW=argc>4?stoi(argv[4]):40,jV=argc>5?stoi(argv[5]):427;
 if(kw<440||kv<530||jW<0||jV<0||jW>=kw||jV>=kv||T<0){
  cerr<<"require kw>=440 kv>=530 0<=jW<kw 0<=jV<kv T>=0\n";return 2;
 }
 Word half=B;
 for(int k=0;k<kw;k++)half.insert(half.end(),W.begin(),W.end());
 half.push_back(9);
 for(int k=0;k<kv;k++)half.insert(half.end(),V.begin(),V.end());
 Word p=half;p.push_back(9);p.insert(p.end(),half.rbegin(),half.rend());
 Word d=normalize(p).first,a=W,b=V;
 const size_t vbase=B.size()+20*(size_t)kw+1;
 const size_t cutW=B.size()+20*(size_t)jW,cutV=vbase+48*(size_t)jV;
 if(cutW+20>=half.size()||cutV+48>=half.size())return 2;
 for(int t=0;t<=T;t++){
  if(pal(d)){cerr<<"palindrome t="<<t<<"\n";return 3;}
  if(p.size()/2<=cutV+48){cerr<<"V cut past centre t="<<t<<"\n";return 4;}
  auto norm=normalize(p);int gamma=norm.second;
  if(norm.first!=d){cerr<<"normalization mismatch t="<<t<<"\n";return 7;}
  if(gamma!=((t&1)==0)){cerr<<"overflow clock mismatch t="<<t<<" gamma="<<gamma<<"\n";return 8;}
  size_t anchor=0;
  while(anchor<cutW && d[anchor]==d[d.size()-1-anchor])anchor++;
  must(anchor<cutW,"no external nonpalindrome witness",t);
  if(t==T)break;  // The final state needs no further parametric edge.
  must(equal(a.begin(),a.end(),p.begin()+cutW),"W cut consumed",t);
  must(equal(b.begin(),b.end(),p.begin()+cutV),"V cut consumed",t);
  Word vW=contract_step(p,d,cutW,20,t);
  Word vV=contract_step(p,d,cutV,48,t);
  must(vW==bulk(a,gamma)&&vV==bulk(b,gamma),"bulk transducer mismatch",t);
  if(t==0||t==1||t==8||t==88||t==1000||t==10000||t==T-1){
    vector<size_t> cuts={cutW,cutV};
    vector<Word> ws={Word(p.begin()+cutW,p.begin()+cutW+20),Word(p.begin()+cutV,p.begin()+cutV+48)};
    Word pp=pump(p,cuts,ws,{2,1});Word dd=normalize(pp).first;
    Word expected=pump(pairs(d),cuts,{vW,vV},{2,1});
    must(pairs(dd)==expected,"two-counter pumping oracle",t);
    must(!pal(dd),"pumped palindrome",t);
  }
  Word nextD=addreverse(d),nextP=pairs(d);
  d.swap(nextD);p.swap(nextP);a=bulk(a,gamma);b=bulk(b,gamma);
 }
 cout<<"PASS W16 deeper-cut kw="<<kw<<" kv="<<kv<<" steps="<<T
     <<" cutW="<<cutW<<" cutV="<<cutV
     <<" seed_digits="<<2*half.size()+2<<" final_digits="<<d.size()
     <<" nonpal_states="<<T+1<<" fnv64="<<hex<<hashdigits(d)<<dec<<"\n";
 return 0;
}
