// Independent direct decimal digit-vector reverse-and-add; no template code.
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <string>
using namespace std;
int main(int argc,char**argv){
 string seed=argc>1?argv[1]:"110102959969697";
 int steps=argc>2?atoi(argv[2]):20000;
 vector<int> d;for(int i=(int)seed.size()-1;i>=0;i--)d.push_back(seed[i]-'0');
 int firstPal=-1,nonpal=0;
 for(int t=0;t<=steps;t++){
  bool pal=true;
  for(size_t i=0;i<d.size()/2;i++)if(d[i]!=d[d.size()-1-i]){pal=false;break;}
  if(pal){firstPal=t;break;}
  nonpal++;
  if(t==steps)break;
  vector<int> e;e.reserve(d.size()+1);int carry=0;
  for(size_t i=0;i<d.size();i++){
   int s=d[i]+d[d.size()-1-i]+carry;
   e.push_back(s%10);carry=s/10;
  }
  if(carry)e.push_back(carry);
  d.swap(e);
 }
 printf("seed=%s first_pal=%d nonpal_checked=%d last_digits=%zu\n",
        seed.c_str(),firstPal,nonpal,d.size());
 return firstPal<0?0:1;
}
