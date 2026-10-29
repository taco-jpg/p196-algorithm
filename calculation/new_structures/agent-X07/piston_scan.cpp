// X07: exhaustive four-digit negative-perturbation seed census for nine-piston.
// Reproduce: g++ -std=c++17 -O3 piston_scan.cpp -lgmpxx -lgmp -o piston_scan
//            ./piston_scan 20000
#define main repdigit_main_unused
#include "repdigit_front.cpp"
#undef main
#include <map>
int main(int argc,char**argv){
  const int H=argc>1?atoi(argv[1]):20000;
  std::map<int,std::vector<int>> winners;
  for(int k=-9999;k<=-1;k++){
    Front f=start(9,k);
    int m=f.left.size(),j=0;
    while(j<m && ((f.left[j]+f.right[m-1-j])%2==0))j++;
    if(j==m)continue;
    step(f);const int invariant=int(f.left.size())-f.over;
    bool survives=true;
    for(int t=1;t<=H;t++){
      const int w=f.left.size();int odd=0;
      while(odd<w && ((f.left[odd]+f.right[w-1-odd])%2==0))odd++;
      if(odd==w || w-f.over!=invariant){survives=false;break;}
      if(t!=H)step(f);
    }
    if(survives)winners[invariant].push_back(k);
  }
  int total=0;for(auto &r:winners)total+=r.second.size();
  cout<<"X07 PISTON SCAN k=-9999..-1 H="<<H<<" survivors="<<total<<"\n";
  for(auto &[offset, ks]:winners){
    cout<<"offset="<<offset<<" count="<<ks.size()<<" seeds=";
    for(int k:ks)cout<<k<<",";
    cout<<"\n";
  }
}
