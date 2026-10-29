// Exact digit-array reverse-add oracle, independent of the rational-polynomial checker.
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <cstdint>
#include <stdexcept>
using namespace std;
using Word=vector<uint8_t>;
Word normalize(const Word &p){
  Word d;d.reserve(p.size()+1);int c=0;
  for(auto x:p){int v=x+c;if(v>19)throw runtime_error("coefficient out of range");d.push_back(v%10);c=v/10;}
  if(c)d.push_back(c);
  if(d.back()==0)throw runtime_error("noncanonical");
  return d;
}
Word pairword(const Word &d){
  Word q(d.size());
  for(size_t i=0;i<d.size();i++)q[i]=d[i]+d[d.size()-1-i];
  return q;
}
void writeword(FILE*f,const Word&p){
  uint32_t n=(uint32_t)p.size();fwrite(&n,4,1,f);fwrite(p.data(),1,p.size(),f);
}
int main(int argc,char**argv){
  if(argc!=4)return 2;
  int steps=atoi(argv[3]);
  FILE*in=fopen(argv[1],"rb");FILE*out=fopen(argv[2],"wb");
  if(!in||!out)return 3;
  fseek(in,0,SEEK_END);long n=ftell(in);rewind(in);
  Word p(n);
  if(fread(p.data(),1,n,in)!=(size_t)n)return 4;
  fclose(in);
  for(int t=0;t<=steps;t++){
    writeword(out,p);
    if(t==steps)break;
    Word d=normalize(p);p=pairword(d);
  }
  fclose(out);return 0;
}
