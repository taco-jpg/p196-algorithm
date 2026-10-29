// Independent ordinary GMP reverse-and-add verification of all twisted-phase snapshots.
#define W16_NO_MAIN
#include "twisted_macro.cpp"
#include <gmpxx.h>
int main(){
 const int kw=440,kv=530;
 Word h=B;for(int i=0;i<kw;i++)h.insert(h.end(),W.begin(),W.end());h.push_back(9);for(int i=0;i<kv;i++)h.insert(h.end(),V.begin(),V.end());
 Word p=h;p.push_back(9);p.insert(p.end(),h.rbegin(),h.rend());Word seed=normalize(p).first;
 string ss;for(auto it=seed.rbegin();it!=seed.rend();++it)ss.push_back('0'+*it);
 mpz_class n(ss);
 const int expected_twisted[12]={627,1247,1919,2571,3195,3823,4455,5131,5751,6367,6977,7629};
 const int expected_naive[12]={50053,50281,47413,47677,47963,46189,48441,48705,48945,52139,52397,7629};
 for(int t=1;t<=3264;t++){
   string s=n.get_str(),r=s;reverse(r.begin(),r.end());mpz_class rev(r);n+=rev;
   if(t%272)continue;
   string a=n.get_str();Word d;for(auto it=a.rbegin();it!=a.rend();++it)d.push_back(*it-'0');
   Word pre;for(auto it=s.rbegin();it!=s.rend();++it)pre.push_back(*it-'0');
   if(pal(d)){cerr<<"PAL at "<<t<<"\n";return 4;}
   Word actual=pairs(pre);int macro=t/272;
   Word target=expand_target(kw,kv,macro,20*macro%48);
   Word naive=expand_target(kw,kv,macro,0);
   if(actual.size()!=target.size())return 5;
   int diff=0,raw=0;
   for(size_t j=0;j<actual.size();j++){diff+=actual[j]!=target[j];raw+=actual[j]!=naive[j];}
   if(diff!=expected_twisted[macro-1]||raw!=expected_naive[macro-1]){
      cerr<<"mismatch at "<<t<<" computed="<<diff<<","<<raw<<"\n";return 6;
   }
   cout<<"GMP PASS macro="<<macro<<" t="<<t<<" phase="<<(20*macro%48)<<" twisted_mismatches="<<diff<<" naive="<<raw<<"\n";
 }
}
