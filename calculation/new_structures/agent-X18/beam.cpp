// X18: nonexhaustive C++ beam around a long, nonperiodic p8/m20 symmetric centre.
// Build: g++ -O3 -std=c++17 beam.cpp -o beam
// Reproduce: ./beam 60 128 12 777  (CHAMPION score 30370)
// Coefficient rows B and W are from ../agent-N18/lattice.txt, time phase zero.
#include <bits/stdc++.h>
using namespace std;
static const int B[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const int W[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
using Vec=vector<unsigned char>;
struct Eval{int pass=0, partial=0, similarity=0, unexpected=0, boundary=0;array<int,8> prefix{};};
static void run88(Vec& P,int& bad){
 Vec digits,next;
 for(int t=0;t<88;t++){
  int c=0;digits.resize(P.size());
  for(size_t i=0;i<P.size();i++){int v=P[i]+c;digits[i]=v%10;c=v/10;}
  if(c)digits.push_back(1);
  bad+=(c!=(t%2==0));
  next.resize(digits.size());
  for(size_t i=0,n=digits.size();i<n;i++)next[i]=digits[i]+digits[n-1-i];
  P.swap(next);
 }
}
static Vec seed(const Vec& U){
 Vec C={8,0,0};C.insert(C.end(),U.begin(),U.end());C.push_back(16);
 C.insert(C.end(),U.rbegin(),U.rend());C.insert(C.end(),{0,0,8});
 Vec L(B,B+39);L.insert(L.end(),W,W+20);
 Vec P=L;P.insert(P.end(),C.begin(),C.end());P.insert(P.end(),L.rbegin(),L.rend());return P;
}
static Eval eval(const Vec& U,int maxR=5){
 Eval e;Vec P=seed(U);Vec pad(B,B+39);
 for(int r=0;r<maxR;r++){
  run88(P,e.unexpected);
  int n=pad.size();
  if(P.size()<size_t(2*n+20) ||
     !equal(pad.begin(),pad.end(),P.begin()) ||
     !equal(pad.begin(),pad.end(),P.rbegin())){e.boundary=r+1;break;}
  int j=0;while(j<20 && P[n+j]==W[j])j++;
  e.prefix[r]=j;e.similarity=0;
  for(int v=0;v<20;v++)e.similarity+=(P[n+v]==W[v]);
  if(j<20){e.partial=j;break;}
  e.pass++;
  // Do NOT add fresh bands: P already represents the actual evolving pair word.
 }
 return e;
}
static uint64_t splitmix(uint64_t& x){
 x+=0x9e3779b97f4a7c15ULL;uint64_t z=x;
 z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;
 z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);
}
struct Item{Vec U;Eval e;uint64_t tie;};
static string key(const Vec& v){return string(v.begin(),v.end());}
static int objective(const Eval&e){return e.pass*10000+e.similarity*70+e.partial*10-e.unexpected*4-e.boundary*100;}
int main(int argc,char**argv){
 int n=argc>1?atoi(argv[1]):60,beam=argc>2?atoi(argv[2]):128,rounds=argc>3?atoi(argv[3]):12;
 uint64_t sd=argc>4?strtoull(argv[4],nullptr,10):777;
 if(n<40||n>120||beam<1||rounds<1)return 2;
 Vec base(n,1);base[13]=7;base[20]=7;base[30]=6;
 vector<Item>frontier{{base,eval(base),0}};
 int bestOne=-1;pair<int,int>at={-1,-1};
 for(int i=0;i<n;i++)for(int d=0;d<=18;d++){
  Vec U=base;U[i]=d;auto e=eval(U);int s=objective(e);
  if(s>bestOne){bestOne=s;at={i,d};}
 }
 cout<<"ONE_SITE n="<<n<<" base="<<objective(frontier[0].e)
     <<" best="<<bestOne<<" pos="<<at.first<<" digit="<<at.second<<"\n";
 unordered_set<string>visited;visited.insert(key(base));
 int global=objective(frontier[0].e);Item champion=frontier[0];
 for(int round=0;round<rounds;round++){
  vector<Item>candidates;candidates.reserve(size_t(beam)*100);
  for(auto&it:frontier){
   for(int k=0;k<min(n,18);k++){
    int pos=int(splitmix(sd)%n),digit=int(splitmix(sd)%19);
    Vec U=it.U;U[pos]=digit;
    if(k%3==1){int p2=int(splitmix(sd)%n);U[p2]=int(splitmix(sd)%19);}
    if(k%3==2){int p2=int(splitmix(sd)%n),p3=int(splitmix(sd)%n);
      U[p2]=int(splitmix(sd)%19);U[p3]=int(splitmix(sd)%19);}
    auto k0=key(U);if(!visited.insert(k0).second)continue;
    Eval e=eval(U);
    if(e.pass>=4){cout<<"FOUR_SUCCESS ";for(int x:U)cout<<x<<",";cout<<"\n";return 0;}
    candidates.push_back({move(U),e,splitmix(sd)});
   }
   int pos=(round+int(splitmix(sd)%n))%n;
   for(int d=0;d<=18;d++){
    Vec U=it.U;U[pos]=d;auto k0=key(U);
    if(!visited.insert(k0).second)continue;
    Eval e=eval(U);
    if(e.pass>=4){cout<<"FOUR_SUCCESS ";for(int x:U)cout<<x<<",";cout<<"\n";return 0;}
    candidates.push_back({move(U),e,splitmix(sd)});
   }
  }
  sort(candidates.begin(),candidates.end(),[](const Item&a,const Item&b){
   int x=objective(a.e),y=objective(b.e);return x!=y?x>y:a.tie<b.tie;
  });
  frontier.clear();
  for(auto&it:candidates){
   if(int(frontier.size())==beam)break;
   int score=objective(it.e);
   if(score>global){global=score;champion=it;}
   frontier.push_back(move(it));
  }
  if(frontier.empty())break;
  cout<<"ROUND "<<round<<" visited="<<visited.size()
      <<" best="<<objective(frontier[0].e)<<" pass="<<frontier[0].e.pass
      <<" partial="<<frontier[0].e.partial<<"\n";
 }
 cout<<"CHAMPION n="<<n<<" score="<<global<<" ";
 for(int x:champion.U)cout<<x<<",";
 cout<<"\n";
}
