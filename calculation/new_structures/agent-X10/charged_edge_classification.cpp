#define COMPLEMENT_FRONT_LIBRARY
#include "complement_front_probe.cpp"
#include <tuple>
#include <sstream>
struct Entry{int s,t,Q,firstpal,L,H,lowfinal,highfinal,highstart;};
int main(int argc,char**argv){
 int T=argc>1?atoi(argv[1]):1000;
 vector<Entry> arr;
 for(int s=10;s<=18;s++)for(int t=10;t<=19;t++){
  int L=10*(t-10)+(s-10),H=100+10*(s-9)+(t-10);
  Packet lo,hi;
  if(L){lo.start=0;lo.d.push_back(L%10);if(L>=10)lo.d.push_back(L/10);}
  int h=H;while(h){hi.d.push_back(h%10);h/=10;}
  Two x={lo,hi};int Q=1,firstpal=-1;
  for(int k=0;k<=T;k++){
   if(x.lo.start<0)throw runtime_error("negative low packet");
   if(!x.lo.empty())Q=max(Q,1+x.lo.end()-x.hi.start);
   Q=max(Q,-x.hi.start);
   bool pal=true;int top=x.hi.end();
   for(int j=0;j<x.lo.length();j++){
    int z=top-x.lo.start-j-x.hi.start;
    int rhs=(z>=0&&z<x.hi.length())?x.hi.d[z]:0;
    if(x.lo.d[j]!=rhs){pal=false;break;}
   }
   if(pal)for(int j=0;j<x.hi.length();j++){
    int z=top-x.hi.start-j-x.lo.start;
    int lhs=(z>=0&&z<x.lo.length())?x.lo.d[z]:0;
    if(x.hi.d[j]!=lhs){pal=false;break;}
   }
   if(pal&&firstpal==-1){firstpal=k;break;}
   if(k<T)x=next2(x);
  }
  arr.push_back({s,t,Q,firstpal,L,H,x.lo.length(),x.hi.length(),x.hi.start});
 }
 sort(arr.begin(),arr.end(),[](auto&a,auto&b){
  if((a.firstpal==-1)!=(b.firstpal==-1))return a.firstpal==-1;
  if(a.Q!=b.Q)return a.Q<b.Q;
  return a.s<b.s||(a.s==b.s&&a.t<b.t);
 });
 cout<<"s,t,H,L,M_required,first_pal,lo_len,hi_len,hi_start\n";
 for(const auto &x:arr)cout<<x.s<<","<<x.t<<","<<x.H<<","<<x.L<<","<<x.Q<<","<<x.firstpal<<","<<x.lowfinal<<","<<x.highfinal<<","<<x.highstart<<"\n";
}
