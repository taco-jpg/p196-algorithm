// N27: emergent antiphase guard of a mobile saturated centre.
#define main n27_original_replay_main
#include "replay.cpp"
#undef main
static int centre18(const V&C){
 int n=(int)C.size(),l=(n-1)/2,r=n/2;
 if(C[l]!=18||C[r]!=18)return 0;
 while(l>0&&C[l-1]==18)--l;
 while(r+1<n&&C[r+1]==18)++r;
 return r-l+1;
}
int main(int argc,char**argv){
 int m=argc>1?atoi(argv[1]):3000,limit=argc>2?atoi(argv[2]):7254;
 S s{{12,9},{6},12000,0,0,0,0,0};
 s.C.insert(s.C.end(),m,9);s.C.push_back(6);
 V d=seed_from_pairs(build(s.B,s.C,s.g));
 int histogram[2][2]={{0,0},{0,0}},count=0,totalGamma=0;
 for(int t=0;t<limit;t++){
  require(!palindrome(d),"palindrome",t);
  require(pairword(d)==build(s.B,s.C,s.g),"full pairword mismatch",t);
  int q=centre18(s.C),c=-1,gam=-1;
  if(t>=1&&q>=3){
   V a,dc,dr;
   int e1=norm(s.B,0,a);
   int len=(int)(s.C.size()-q)/2;
   require(len>=0&&2*len+q==(int)s.C.size(),"centre not symmetric",t);
   V L(s.C.begin(),s.C.begin()+len);
   c=norm(L,e1,dc);
   int e2=norm(s.C,e1,dc);
   V B_rev(s.B.rbegin(),s.B.rend());
   gam=norm(B_rev,e2,dr);
  }
  V nxt=integer_step(d);
  int ordinaryGamma=(int)nxt.size()-(int)d.size();
  require(template_step(s),"carry-flip failed",t);
  require(ordinaryGamma==s.gam,"overflow differs from ordinary digits",t);
  if(t>=1&&q>=3){
   int q2=centre18(s.C);
   int predicted=q-gam-2*(1-gam)*(1-c);
   require(q2==predicted,"front transfer equation failed",t);
   require(c+gam==1,"antiphase carry guard failed",t);
   histogram[c][gam]++;count++;
  }
  totalGamma+=ordinaryGamma;
  d.swap(nxt);
 }
 printf("ANTIPHASE m=%d checked=%d c0g0=%d c0g1=%d c1g0=%d c1g1=%d overflow=%d q=%d gap=%d\n",
 m,count,histogram[0][0],histogram[0][1],histogram[1][0],histogram[1][1],
 totalGamma,centre18(s.C),s.g);
 return 0;
}
