#define main dual_replay_unused_main
#include "dual_replay.cpp"
#undef main
int main(){
 cout<<"Q,R,first_outer_digit,first_centre_digit,first_outer_pair,first_centre_pair\n";
 for(int q:{5,10,20,40,60,100})for(int r:{5,10,20,40,60,100}){
  Dig a[4]={seed(q,r),seed(q+1,r),seed(q,r+1),seed(q+1,r+1)};
  int fdq=-1,fdr=-1,fpq=-1,fpr=-1;
  for(int t=0;t<=550;t++){
   if(fdq<0&&(!insertion(a[0],a[1],2)||!insertion(a[2],a[3],2)))fdq=t;
   if(fdr<0&&(!insertion(a[0],a[2],1)||!insertion(a[1],a[3],1)))fdr=t;
   Dig pw[4]={pairword(a[0]),pairword(a[1]),pairword(a[2]),pairword(a[3])};
   if(fpq<0&&(!pair_insertion(pw[0],pw[1],4)||!pair_insertion(pw[2],pw[3],4)))fpq=t;
   if(fpr<0&&(!pair_insertion(pw[0],pw[2],2)||!pair_insertion(pw[1],pw[3],2)))fpr=t;
   if(fdq>=0&&fdr>=0&&fpq>=0&&fpr>=0)break;
   for(auto&x:a)step(x);
  }
  cout<<q<<","<<r<<","<<fdq<<","<<fdr<<","<<fpq<<","<<fpr<<"\n";
 }
}
