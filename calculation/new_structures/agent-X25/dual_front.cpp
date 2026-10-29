// X25: 88/792-step dual-front 101-coefficient moving windows.
// Reuses only the exact pairword seed and recurrence from collision.cpp.
#define main x25_collision_unused_main
#include "collision.cpp"
#undef main
struct Snap {int al, ar, dl, dr; string aleft, aright, dleft, dright;};
string window(const Word& p,int edge,int lo,int hi){
 string s;for(int j=lo;j<=hi;j++){if(edge+j<0||edge+j>=(int)p.size())abort();s.push_back(char(p[edge+j]));}
 return s;
}
int main(int argc,char **argv){
 int q=argc>1?atoi(argv[1]):600, x=argc>2?atoi(argv[2]):2500, H=argc>3?atoi(argv[3]):5000;
 Word bg=seed(q),a=patch(bg,x,A),d=patch(bg,x,D);vector<Snap> all;all.reserve(H+1);
 for(int t=0;t<=H;t++){
  int n=bg.size(),al=n,ar=-1,dl=n,dr=-1;
  if(a.size()!=bg.size()||d.size()!=bg.size())abort();
  bool odd=false;for(int j=0;j<39;j++){
    if(bg[j]!=a[j]||bg[j]!=d[j])abort();
    if(bg[j]&1)odd=true;
  }
  if(!odd){cerr<<"nonpalindrome witness missing t="<<t<<"\n";return 2;}
  for(int j=0;j<n/2;j++){
   if(a[j]!=bg[j])al=min(al,j),ar=max(ar,j);
   if(d[j]!=bg[j])dl=min(dl,j),dr=max(dr,j);
  }
  if(al==n||dl==n||ar+80>=n/2||dr+80>=n/2||al<80||dl<80){cerr<<"edge violation t="<<t<<"\n";return 2;}
  all.push_back({al,ar,dl,dr,window(a,al,-80,20),window(a,ar,-20,80),window(d,dl,-80,20),window(d,dr,-20,80)});
  if(t<H){int g=step(bg),ga=step(a),gd=step(d);
    if(g!=ga||g!=gd||g!=(t%2==0)){cerr<<"clock t="<<t<<"\n";return 2;}}
 }
 auto test=[&](const string& name,int delay,int drift,int expectedlast){
  int total=0,good=0,lastfail=-1;
  for(int t=0;t+delay<=H;t++){
   auto &u=all[t],&v=all[t+delay];bool ok=false;
   if(name=="AR")ok=(v.ar-u.ar==drift&&u.aright==v.aright);
   if(name=="DR")ok=(v.dr-u.dr==drift&&u.dright==v.dright);
   if(name=="AL")ok=(v.al-u.al==drift&&u.aleft==v.aleft);
   if(name=="DL")ok=(v.dl-u.dl==drift&&u.dleft==v.dleft);
   total++;if(ok)good++;else lastfail=t;
  }
  cout<<name<<" delay="<<delay<<" drift="<<drift<<" total="<<total<<" matches="<<good<<" lastfailure="<<lastfail<<" stable_from="<<lastfail+1<<"\n";
  if(expectedlast>=0&&lastfail!=expectedlast)abort();
 };
 if(q==600&&x==2500&&H==5000){
   test("AL",88,-20,396);test("DL",88,-20,241);
   test("AR",792,540,421);test("DR",792,540,493);
 }else{test("AL",88,-20,-1);test("DL",88,-20,-1);test("AR",792,540,-1);test("DR",792,540,-1);}
 for(int delay=88;delay<792;delay+=88){test("AR",delay,60*(delay/88),-1);test("DR",delay,60*(delay/88),-1);}
}
