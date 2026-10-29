// Strict intermediate W9 matching is diagnostic ONLY; not endpoint-pruning.
#define main ac23_scan_main
#include "scan.cpp"
#undef main
int main(int argc,char**argv){
 try{
  int urank=0, phase=2, centre=2; uint64_t count=2476099,start=0;
  if(argc>1)urank=stoi(argv[1]);
  if(argc>2)count=stoull(argv[2]);
  vector<vector<int>> bs,ws;vector<int>gs;
  read_lat(argc>3?argv[3]:"calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt",bs,ws,gs);
  auto u=make_us()[urank];
  uint64_t hit[121]={},alltime[121]={},overflowmatch[121]={};
  for(uint64_t code=start;code<start+count;code+=64){
   vector<B>p=make(bs[phase],ws[phase],u,14,100,centre,code),digits,nxt;
   uint64_t valid=min<uint64_t>(64,start+count-code),mask=valid==64?~V(0):((V(1)<<valid)-1);
   V clock=mask, strict=mask;
   hit[0]+=__builtin_popcountll(mask);alltime[0]+=__builtin_popcountll(mask);overflowmatch[0]+=__builtin_popcountll(mask);
   for(int t=0;t<120;t++){
    int gam=gs[(phase+t)%12];
    V c=step(p,digits,nxt,gam);
    clock &= gam?c:~c;
    int root=(phase+t+1)%12;
    V ok=clock;
    for(int i=0;i<160;i++)ok &= eq(p[i],i<34?bs[root][i]:ws[root][(i-34)%9]);
    hit[t+1]+=__builtin_popcountll(ok);
    strict &=ok;
    alltime[t+1]+=__builtin_popcountll(strict);
    overflowmatch[t+1]+=__builtin_popcountll(clock);
   }
  }
  cout<<"phase="<<phase<<" U="<<u[0]<<","<<u[1]<<","<<u[2]<<" J_count="<<count<<" C=[4,4]\n";
  cout<<"step,clock_valid,stepwise_W9_exact,strict_all_steps_W9_exact\n";
  for(int t=0;t<=120;t++)cout<<t<<","<<overflowmatch[t]<<","<<hit[t]<<","<<alltime[t]<<"\n";
 }catch(exception&e){cerr<<e.what()<<"\n";return 2;}
}
