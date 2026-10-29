#define main four_sheet_original_main
#include "four_sheet_fast.cpp"
#undef main
struct Two{Packet lo,hi;};
Two next2(const Two&x){int h=x.hi.end();return {newpacket(x.lo,x.hi,h),newpacket(x.hi,x.lo,h)};}

#ifndef COMPLEMENT_FRONT_LIBRARY
int main(int argc,char**argv){
 int T=argc>1?atoi(argv[1]):20000;Two x={{0,{3,6}},{0,{6,4,1}}};
 int m_req=1,palcount=0,palfirst=-1;
 cout<<"t,M_required,lowlen,highlen,highstart,highend,pal,hash\n";
 for(int t=0;t<=T;t++){
  if(x.lo.start<0)throw runtime_error("negative low");
  m_req=max(m_req,1+x.lo.end()-x.hi.start);
  m_req=max(m_req,-x.hi.start);
  int h=x.hi.end();bool pal=true;
  for(int j=0;j<x.lo.length();j++){
   int k=h-(x.lo.start+j)-x.hi.start;
   int d=k>=0&&k<x.hi.length()?x.hi.d[k]:0;
   if(x.lo.d[j]!=d){pal=false;break;}
  }
  if(pal){for(int j=0;j<x.hi.length();j++){
   int k=h-(x.hi.start+j)-x.lo.start;
   int d=k>=0&&k<x.lo.length()?x.lo.d[k]:0;
   if(x.hi.d[j]!=d){pal=false;break;}
  }}
  if(pal){palcount++;if(palfirst<0)palfirst=t;}
  if(t<=20||t==44||t==88||t==264||t==1000||t==5000||t==10000||t==20000||t==T)
   cout<<t<<","<<m_req<<","<<x.lo.length()<<","<<x.hi.length()<<","<<x.hi.start<<","<<x.hi.end()<<","<<pal<<","<<hash_packets(S{x.lo,{}, {},x.hi})<<"\n";
  if(t<T)x=next2(x);
 }
 cerr<<"SUMMARY T="<<T<<" bound="<<m_req<<" palcount="<<palcount<<" first="<<palfirst<<"\n";
}

#endif // COMPLEMENT_FRONT_LIBRARY
