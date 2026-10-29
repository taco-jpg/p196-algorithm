// Independent ordinary decimal digit-list replay. Deliberately does not import Python transducer.
#include <cstdio>
#include <vector>
#include <cstdint>
#include <cstdlib>
#include <algorithm>
using namespace std;
int main(int argc,char**argv){
 int steps=argc>1?atoi(argv[1]):20000;
 vector<unsigned char> v={6,9,1};
 uint64_t allodd=0, firstNoOdd=UINT64_MAX, minOdd=UINT64_MAX, maxOdd=0, minLen=UINT64_MAX,maxLen=0;
 for(int t=0;t<=steps;t++){
   bool ispal=true;size_t odd=0,m=v.size()/2;
   for(size_t i=0;i<m;i++){
      unsigned x=v[i]+v[v.size()-1-i];
      odd+=(x&1);
      if(v[i]!=v[v.size()-1-i])ispal=false;
   }
   if(ispal){printf("PALINDROME t=%d length=%zu\n",t,v.size());return 1;}
   if(!odd && firstNoOdd==UINT64_MAX)firstNoOdd=t;
   if(odd) allodd++;
   minOdd=min(minOdd,(uint64_t)odd);maxOdd=max(maxOdd,(uint64_t)odd);
   minLen=min(minLen,(uint64_t)v.size());maxLen=max(maxLen,(uint64_t)v.size());
   if(t==steps)break;
   unsigned carry=0;size_t n=v.size();
   vector<unsigned char> old=v;
   for(size_t i=0;i<n;i++){
      unsigned x=old[i]+old[n-1-i]+carry;
      v[i]=x%10;carry=x/10;
   }
   if(carry)v.push_back((unsigned char)carry);
 }
 printf("COMPUTED: seed=196 steps=%d all %d+1 states nonpal, odd-witness-states=%llu, first-no-odd=%lld, length=%zu, minOdd=%llu maxOdd=%llu, minlen=%llu maxlen=%llu\n",steps,steps,(unsigned long long)allodd,(long long)(firstNoOdd==UINT64_MAX?-1:firstNoOdd),v.size(),(unsigned long long)minOdd,(unsigned long long)maxOdd,(unsigned long long)minLen,(unsigned long long)maxLen);
 return 0;
}
