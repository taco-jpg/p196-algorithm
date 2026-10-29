#define main old_main
#include "skew_contract.cpp"
#undef main
int main(int argc,char**argv){
 int kw=440,kv=530,T=argc>1?atoi(argv[1]):272;
 Word half=B;for(int j=0;j<kw;j++)half.insert(half.end(),W.begin(),W.end());half.push_back(9);for(int j=0;j<kv;j++)half.insert(half.end(),V.begin(),V.end());Word p=half;p.push_back(9);p.insert(p.end(),half.rbegin(),half.rend());Word d=normalize(p).first;
 for(int t=0;t<T;t++){Word q=pairs(d);d=addreverse(d);p=q;}
 int a=1,b=1; int len_expected=2*(B.size()+20*(kw+a)+1+48*(kv+b))+1;
 if((int)p.size()!=len_expected){cout<<"cannot use plus1 plus1 at T="<<T<<" actual="<<p.size()<<" expected="<<len_expected<<"\n";return 0;}
 long long best=LLONG_MAX;int bestw=-1,bestv=-1,bestfirst=-1;
 for(int rW=0;rW<20;rW++)for(int rV=0;rV<48;rV++){
  Word h=B;
  for(int j=0;j<kw+a;j++)for(int u=0;u<20;u++)h.push_back(W[(u+rW)%20]);
  h.push_back(9);
  for(int j=0;j<kv+b;j++)for(int u=0;u<48;u++)h.push_back(V[(u+rV)%48]);
  Word target=h;target.push_back(9);target.insert(target.end(),h.rbegin(),h.rend());
  int mismatches=0,first=-1,pre=0,post=0;
  for(size_t i=0;i<p.size();i++)if(p[i]!=target[i]){mismatches++;if(first<0)first=i;}
  if(mismatches<best){best=mismatches;bestw=rW;bestv=rV;bestfirst=first;}
  if(rW==0 && (rV==0 || rV==20)){cout<<"rotation "<<rV<<" mismatch="<<mismatches<<" first="<<first<<"\n";}
 }
 cout<<"best mismatch="<<best<<" wrotation="<<bestw<<" vrotation="<<bestv<<" first="<<bestfirst<<" total="<<p.size()<<"\n";
}
