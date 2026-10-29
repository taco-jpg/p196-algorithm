// Agent X24: first exact merger at reverse-add step 22.
// Reuses GMP and positional-decimal engines from the earlier X24 result.
#define main packet_replay_previous_main
#include "packet_replay.cpp"
#undef main

string custom_seed(int r,vector<int> leftcentre){
 auto h=exterior_half(r);vector<int>p=h;
 p.insert(p.end(),leftcentre.begin(),leftcentre.end());
 p.insert(p.end(),leftcentre.rbegin(),leftcentre.rend());
 p.insert(p.end(),h.rbegin(),h.rend());
 string s(p.size(),'0');
 for(size_t i=0;i<p.size()/2;i++){
  int lo=p[i]/2,hi=p[i]-lo;
  if(lo<0||lo>9||hi<0||hi>9)exit(2);
  s[p.size()-1-i]=char('0'+lo);s[i]=char('0'+hi);
 }
 if(s[0]=='0')exit(2);
 return s;
}
int main(int argc,char**argv){
 int r=argc>1?atoi(argv[1]):234;
 int steps=argc>2?atoi(argv[2]):20000;
 build_phase();
 string init=custom_seed(r,{17,6,5,2,11});
 string other=custom_seed(r,{8,15,18,13,5});
 cout<<"initial_digits="<<init.size()<<" seed_A_hash="<<hex<<hash64(init)
   <<" seed_B_hash="<<hash64(other)<<dec<<"\n";
 mpz_t x,y;mpz_inits(x,y,NULL);string s=init,t=other,z;
 for(int i=0;i<=22;i++){
  if(i<22&&s==t){cerr<<"premature merge "<<i<<"\n";return 2;}
  if(i==22){if(s!=t){cerr<<"no step22 merge\n";return 3;}break;}
  if(equal(s.begin(),s.end(),s.rbegin())||equal(t.begin(),t.end(),t.rbegin())){cerr<<"early palindrome\n";return 4;}
  string as=add_reverse_string(s),bs=add_reverse_string(t);
  gmp_step(s,z,x,y);if(z!=as){cerr<<"bad GMP A\n";return 5;}s.swap(as);
  gmp_step(t,z,x,y);if(z!=bs){cerr<<"bad GMP B\n";return 6;}t.swap(bs);
 }
 cout<<"PASS first exact numerical merger at step22: hash="<<hex<<hash64(s)<<dec<<"\n";
 s=init;int pals=0,minbands=INT32_MAX;
 for(int i=0;i<=steps;i++){
  if(equal(s.begin(),s.end(),s.rbegin()))pals++;
  int bands=check_exterior(s,i%8,20);
  minbands=min(minbands,bands);
  if(i%1000==0||i==steps)cout<<"step="<<i<<" length="<<s.size()<<" bands="<<bands
    <<" pal_count="<<pals<<" hash64="<<hex<<hash64(s)<<dec<<"\n"<<flush;
  if(i==steps)break;
  auto bydigits=add_reverse_string(s);
  gmp_step(s,z,x,y);
  if(z!=bydigits){cerr<<"double-engine divergence at t="<<i<<"\n";return 7;}
  s.swap(bydigits);
 }
 mpz_clears(x,y,NULL);
 cout<<"RESULT steps="<<steps<<" first_merge=22 no_pal="<<(pals==0)
  <<" min_band_matches="<<minbands<<"\n";
 return pals==0&&minbands>=1?0:8;
}
