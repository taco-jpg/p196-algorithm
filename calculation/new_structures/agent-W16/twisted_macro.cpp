// W16 independent phase-twisted macro-comparison for two decimal lattice domains.
// g++ -O3 -std=c++17 twisted_macro.cpp -o twisted_macro && ./twisted_macro
#define main w16_previous_main
#include "skew_contract.cpp"
#undef main
static Word expand_target(int kw,int kv,int copies,int vphase){
 Word h=B;
 for(int k=0;k<kw+copies;k++)h.insert(h.end(),W.begin(),W.end());
 h.push_back(9);
 for(int k=0;k<kv+copies;k++)for(int j=0;j<48;j++)h.push_back(V[(j+vphase)%48]);
 Word out=h;out.push_back(9);out.insert(out.end(),h.rbegin(),h.rend());return out;
}

#ifndef W16_NO_MAIN
int main(){
 const int kw=440,kv=530;
 Word h=B;for(int j=0;j<kw;j++)h.insert(h.end(),W.begin(),W.end());h.push_back(9);for(int j=0;j<kv;j++)h.insert(h.end(),V.begin(),V.end());
 Word p=h;p.push_back(9);p.insert(p.end(),h.rbegin(),h.rend());
 Word d=normalize(p).first;
 for(int t=0;t<272*12;t++){
  Word q=pairs(d);d=addreverse(d);p.swap(q);
  if((t+1)%272)continue;
  int hstep=(t+1)/272,phase=(20*hstep)%48;
  auto target=expand_target(kw,kv,hstep,phase);
  auto unrot=expand_target(kw,kv,hstep,0);
  if(p.size()!=target.size()){cout<<"length mismatch t="<<t+1<<"\n";return 1;}
  int mism=0,first=-1,raw=0,between=0,nearW=0,nearV=0,centre=0;
  int vbase=B.size()+20*(kw+hstep)+1;
  int mid=(int)target.size()/2;
  vector<int> miss;
  for(int i=0;i<(int)p.size();i++){
   raw+=(p[i]!=unrot[i]);
   if(p[i]!=target[i]){mism++;miss.push_back(i);if(first==-1)first=i;
     if(i<mid){if(i<vbase)nearW++;else if(i<vbase+48*(kv+hstep))nearV++;else centre++;}
   }
  }
  int maxgap=0,nclusters=0,last=-10000;
  for(int x:miss){if(x-last>5)nclusters++;maxgap=max(maxgap,x-last);last=x;}
  cout<<"macro="<<hstep<<" t="<<t+1<<" vphase="<<phase<<" naive="<<raw
      <<" twisted="<<mism<<" first="<<first<<" left_W_region="<<nearW
      <<" left_V_region="<<nearV<<" left_centre="<<centre<<" clustersGap5="<<nclusters<<"\n";
 }
}

#endif
