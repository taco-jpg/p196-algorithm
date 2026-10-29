// A single genuine phase-2 trajectory showing temporary W9 damage can heal.
#define main ac23_scan_main
#include "scan.cpp"
#undef main
int main(int argc,char**argv){
 vector<vector<int>>b,w;vector<int>g;
 read_lat(argc>1?argv[1]:"calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt",b,w,g);
 auto u=make_us()[0];bool found15=false,found85=false;
 for(uint64_t code=0;code<2476099;code+=64){
  vector<B>p=make(b[2],w[2],u,14,100,2,code),d,nxt;
  V valid=code+64<=2476099?~V(0):((V(1)<<(2476099-code))-1);
  V strict=valid,clock=valid;
  for(int t=1;t<=85;t++){
   int gm=g[(2+t-1)%12];V c=step(p,d,nxt,gm);
   clock&=gm?c:~c;
   V instant=clock;
   for(int i=0;i<160;i++)instant&=eq(p[i],i<34?b[(2+t)%12][i]:w[(2+t)%12][(i-34)%9]);
   if((t==15&&!found15)||(t==85&&!found85)){
    V healing=instant&~strict&valid;
    if(healing){int lane=__builtin_ctzll(healing);auto j=decode(code+lane);
      cout<<"HEAL t="<<t<<" index="<<(code+lane)<<" J="<<j[0]<<','<<j[1]<<','<<j[2]<<','<<j[3]<<','<<j[4]<<"\n";
      if(t==15)found15=true;else found85=true;
    }
   }
   strict&=instant;
  }
  if(found15&&found85)break;
 }
 if(!found15||!found85){cerr<<"missing witness t15="<<found15<<" t85="<<found85<<"\n";return 2;}
}
