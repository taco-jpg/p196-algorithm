// W24: moving-cut full-pairword pump in the complementary p8/m20 family.
// Build: g++ -O3 -std=c++17 sliding_pump_gmp.cpp -lgmpxx -lgmp -o /tmp/w24pump
// Run: /tmp/w24pump 900 20000
#define main w24_dual_front_standalone_main
#include "dual_front.cpp"
#undef main
#include <map>

static std::string necklace20(const std::vector<unsigned char> &d, int i){
  std::string s;
  int n=d.size();
  for(int j=0;j<20;j++)s.push_back(char('A'+d[i+j]+d[n-1-i-j]));
  std::string best=s;
  for(int j=1;j<20;j++)best=std::min(best,s.substr(j)+s.substr(0,j));
  return best;
}
int main(int argc,char**argv){
 try{
  int q=argc>1?atoi(argv[1]):900,steps=argc>2?atoi(argv[2]):20000;
  auto a=initial(q),b=initial(q+1);
  mpz_class na(str(a),10),nb(str(b),10);
  std::map<std::string,int> seen;
  int minrun=1000000000,minmargin=1000000000,nonpal=0,agreement=0;
  std::cout<<"{\"q\":"<<q<<",\"steps\":"<<steps<<",\"checkpoints\":[";
  bool first=true;
  for(int t=0;t<=steps;t++){
   int sa=a.size(),sb=b.size();
   Run r=longest_period20(a);
   int cut=(r.start+r.stop)/2;
   int mismatch=-1;
   if(sb!=sa+40)mismatch=-2;
   else for(int i=0;i<sa/2;i++){
      int s=a[i]+a[sa-1-i];
      int j=i<cut?i:i+20;
      int l=b[j]+b[sb-1-j];
      if(s!=l){mismatch=i;break;}
   }
   // The inserted 20 sites must be the actual current spatial-period word,
   // not merely an arbitrary unmatched block in the longer orbit.
   if(mismatch==-1){
     for(int j=0;j<20;j++){
       int i=cut+j;
       int ps=a[i]+a[sa-1-i];
       int pb=b[i]+b[sb-1-i];
       if(ps!=pb){mismatch=i;break;}
     }
   }
   if(mismatch!=-1)throw std::runtime_error(
      "moving pump mismatch at step "+std::to_string(t)+" index "+std::to_string(mismatch));
   minrun=std::min(minrun,r.length);
   minmargin=std::min(minmargin,std::min(cut-r.start,r.stop-cut));
   seen.emplace(necklace20(a,r.start+30),t);
   bool palA=true,palB=true;
   for(int i=0;i<sa/2;i++)if(a[i]!=a[sa-1-i]){palA=false;break;}
   for(int i=0;i<sb/2;i++)if(b[i]!=b[sb-1-i]){palB=false;break;}
   if(palA||palB)throw std::runtime_error("palindrome at step "+std::to_string(t));
   nonpal++;
   if(t==0||t==8||t==88||t==500||t==1000||t==2000||
      t==5000||t==10000||t==15000||t==steps){
      if(!first)std::cout<<",";
      first=false;
      std::cout<<"{\"t\":"<<t<<",\"digits_short\":"<<sa
               <<",\"digits_long\":"<<sb<<",\"cut\":"<<cut
               <<",\"left\":"<<r.start<<",\"right\":"<<r.stop
               <<",\"run20\":"<<r.length<<",\"fnv_short\":"<<fnv_hash(a)
               <<",\"fnv_long\":"<<fnv_hash(b)<<"}";
   }
   if(t<steps){
     step_vector(a);step_vector(b);step_gmp(na);step_gmp(nb);
     if(str(a)!=na.get_str(10)||str(b)!=nb.get_str(10))
       throw std::runtime_error("GMP disagreement at "+std::to_string(t+1));
     agreement++;
   }
  }
  std::cout<<"],\"unique_period20_necklaces\":"<<seen.size()
           <<",\"min_run20\":"<<minrun<<",\"min_cut_margin\":"<<minmargin
           <<",\"nonpal_state_pairs\":"<<nonpal
           <<",\"gmp_checks_per_track\":"<<agreement<<"}"<<std::endl;
 }catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<"\n";return 1;}
}
