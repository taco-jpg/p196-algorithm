// Independent arbitrary-precision GMP integer reverse-and-add validation.
// g++ -O3 -std=c++17 replay_gmp20k.cpp -lgmpxx -lgmp -o replay_gmp20k
// ./replay_gmp20k 500 20000
#define main n01_reference_main_not_called
#include "replay20k.cpp"
#undef main
#include <gmpxx.h>
int main(int argc, char**argv){
 int k=argc>1?stoi(argv[1]):500,steps=argc>2?stoi(argv[2]):20000;
 vector<Digit> h=B;
 for(int i=0;i<k;i++)h.insert(h.end(),W.begin(),W.end());
 h.push_back(9);
 for(int i=0;i<k;i++)h.insert(h.end(),V.begin(),V.end());
 vector<Digit> p=h;p.push_back(9);p.insert(p.end(),h.rbegin(),h.rend());
 mpz_class n=0;
 for(auto it=p.rbegin();it!=p.rend();++it){n*=10;n+=mpz_class(static_cast<unsigned int>(*it));}
 for(int t=0;t<=steps;t++){
   string s=n.get_str(10);
   if(equal(s.begin(),s.begin()+s.size()/2,s.rbegin())){cerr<<"PAL at "<<t<<"\n";return 2;}
   if(t==steps){
     uint64_t hash=1469598103934665603ULL;
     for(auto it=s.rbegin();it!=s.rend();++it){hash^=uint64_t(*it-'0');hash*=1099511628211ULL;}
     cout<<"GMP PASS k="<<k<<" steps="<<steps<<" digits="<<s.size()<<" FNV64="<<hex<<hash<<dec<<"\n";
     break;
   }
   reverse(s.begin(),s.end());
   mpz_class r(s,10);n+=r;
   if((t+1)%2000==0)cerr<<"GMP verified "<<t+1<<" steps\n";
 }
 return 0;
}
