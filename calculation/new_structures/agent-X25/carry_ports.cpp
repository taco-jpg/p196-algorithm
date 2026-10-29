// Probe physical two-ended decimal carry-port recurrence on right-moving X25 fronts.
#define main x25_collision_unused_main
#include "collision.cpp"
#undef main
using Gates=array<int,4>;
struct Snap {int ar,dr;Gates ag,dg;};
int pin_run(const Word& p,int k){int n=0;for(int j=k-1;j>=0&&p[j]==9;j--)++n;return n;}
vector<int> carries(const Word& p){vector<int> c(p.size()+1);for(size_t i=0;i<p.size();i++)c[i+1]=(p[i]+c[i])/10;return c;}
Gates gate(const Word& p,const vector<int>& c,int r){int n=p.size(),lo=r-20,hi=r+80;if(lo<0||hi>=n/2)abort();return {c[lo],c[hi+1],c[n-1-hi],c[n-lo]};}
int main(int argc,char**argv){int q=argc>1?atoi(argv[1]):600,x=argc>2?atoi(argv[2]):2500,H=argc>3?atoi(argv[3]):5000;Word bg=seed(q),a=patch(bg,x,A),d=patch(bg,x,D);vector<Snap> rec;array<int,4> maxpinA={0,0,0,0},maxpinD={0,0,0,0};
for(int t=0;t<=H;t++){
 int ar=-1,dr=-1;for(int i=0;i<(int)bg.size()/2;i++){if(a[i]!=bg[i])ar=i;if(d[i]!=bg[i])dr=i;}
 rec.push_back({ar,dr,gate(a,carries(a),ar),gate(d,carries(d),dr)});
 if(t>=497&&t+792<=H){int n=bg.size();array<int,4> ai={ar-20,ar+81,n-1-(ar+80),n-(ar-20)},di={dr-20,dr+81,n-1-(dr+80),n-(dr-20)};for(int k=0;k<4;k++){maxpinA[k]=max(maxpinA[k],pin_run(a,ai[k]));maxpinD[k]=max(maxpinD[k],pin_run(d,di[k]));}}
 if(t<H){int g=step(bg),ga=step(a),gd=step(d);if(g!=ga||g!=gd)abort();}
}
for(const auto &[name,species]:vector<pair<string,int>>{{"A",0},{"D",1}}){
 int matches=0,lastbad=-1,badbits[4]={};int onlygates=0,matchposition=0;
 for(int t=0;t+792<=H;t++){
  auto &u=rec[t],&v=rec[t+792];Gates z=species?u.dg:u.ag,w=species?v.dg:v.ag;
  bool pm=(species?(v.dr-u.dr):(v.ar-u.ar))==540;
  bool gm=z==w;
  if(pm)matchposition++;if(gm)onlygates++;
  if(pm&&gm)matches++;else{lastbad=t;for(int k=0;k<4;k++)badbits[k]+=(z[k]!=w[k]);}
 }
 cout<<name<<" gates_and_front_792 matches="<<matches<<"/"<<H+1-792<<" position="<<matchposition<<" gate="<<onlygates<<" lastfail="<<lastbad<<" stable_from="<<lastbad+1<<" badbits=";
 for(int k:badbits)cout<<k<<",";cout<<"\n";
 for(int t:{0,1,2,422,493,500,1000,1300,2000})if(t+792<=H){Gates z=species?rec[t].dg:rec[t].ag;cout<<"sample "<<name<<" t="<<t<<" ports=";for(int k:z)cout<<k;cout<<" compare=";for(int k:(species?rec[t+792].dg:rec[t+792].ag))cout<<k;cout<<"\n";}
}
cout<<"pin_runs_stable A=";for(int v:maxpinA)cout<<v<<",";cout<<" D=";for(int v:maxpinD)cout<<v<<",";cout<<"\n";
}
