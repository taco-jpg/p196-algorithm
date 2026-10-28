// Exact base-parametric p=2, overflow 01, position-automaton census.
// Build: c++ -O3 -std=c++17 agent10_g01_even_fast.cpp -o g01_even_fast
// Run: ./g01_even_fast 2 10000 output.csv
// Resume: parse the final complete row and restart at next base.
#include <bits/stdc++.h>
using namespace std;
struct Stats {int states=0, acceptdepth=-1, accepts=0;};
static Stats solve(int b){
  vector<unsigned char> seen(16ull*b,0);
  vector<int> q; q.reserve(8*b);
  int root=(0*4+2)*b+1; seen[root]=1;q.push_back(root);
  int start=0, stop=1,depth=0, hits=0, minhit=-1;
  while(start<stop){
    int next=stop;
    for(int i=start;i<stop;i++){
      int t=q[i],Y=t%b, z=t/b,H=z%4,L=z/4;
      int l0=L&1,l1=(L>>1)&1,h0=H&1,h1=(H>>1)&1;
      int S=l0+l1;
      if(i!=0 && S!=1){cerr<<"invalid invariant b="<<b<<"\n";abort();}
      for(int c0=0;c0<2;c0++){
        // Closed two-time column plus the one-carry invariant L'0+L'1=1:
        //   x0 = b*(1+h0) - (S+c0+Y).
        int x0=b*(1+h0)-(S+c0+Y);
        if(x0<0 || x0>2*b-2 || (i==0&&x0==0))continue;
        if((x0+c0)/b != h0)continue;
        int x1=(x0+l0)%b+(x0+c0)%b;
        if(x1>2*b-2 || x0!=(x1+l1)%b+Y)continue;
        int L2=(x0+l0)/b+2*((x1+l1)/b);
        if(L2!=1&&L2!=2){cerr<<"invariant contradicted b="<<b<<"\n";abort();}
        for(int c1=0;c1<2;c1++){
          if((x1+c1)/b != h1)continue;
          int H2=c0+2*c1,Y2=(x1+c1)%b;
          int v=(L2*4+H2)*b+Y2;
          if(seen[v])continue;
          seen[v]=1;q.push_back(v);next++;
          if((((L2&1)+(H2&1))==1) &&
             (((L2>>1)&1)+((H2>>1)&1)==1) &&
             Y2==(b-1)*((L2>>1)&1)){
            if(minhit<0)minhit=depth+1;
            hits++;
          }
        }
      }
    }
    start=stop;stop=next;depth++;
  }
  return {int(q.size()),minhit,hits};
}
int main(int argc,char**argv){
 if(argc<4){cerr<<"usage: g01_even_fast START END OUTPUT_CSV\n";return 2;}
 int start=stoi(argv[1]),end=stoi(argv[2]);ofstream out(argv[3],ios::app);
 if(!out){cerr<<"unable to open output\n";return 2;}
 for(int b=start;b<=end;b++){
  Stats s=solve(b);
  out<<b<<","<<s.states<<","<<s.acceptdepth<<","<<s.accepts<<"\n";
  if(b%100==0){out.flush();cerr<<"completed b="<<b<<" states="<<s.states<<" accepted="<<s.accepts<<"\n";}
 }
}
