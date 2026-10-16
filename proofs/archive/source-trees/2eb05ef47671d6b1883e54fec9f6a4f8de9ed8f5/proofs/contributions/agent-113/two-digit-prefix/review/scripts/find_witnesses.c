/* Independent re-derivation of sharpness witnesses: for each prefix ab with
   bound h, find the smallest R >= 1 whose FIRST palindrome T^t(R) (t >= 0)
   occurs at t = h and begins with ab.  Also the smallest R (intermediate
   palindromes allowed) with T^h(R) a palindrome beginning with ab. */
#include <stdio.h>
#include <stdint.h>
static uint64_t rev(uint64_t n){uint64_t r=0;while(n){r=r*10+n%10;n/=10;}return r;}
static int top2(uint64_t n){while(n>=100)n/=10;return (int)n;}
int main(void){
  int ab[13]={10,20,32,40,41,60,64,65,76,80,81,82,83};
  int bd[13]={1,2,2,3,3,3,3,6,3,4,4,4,4};
  uint64_t firstR[13]={0}, anyR[13]={0}; int left=26;
  for(uint64_t R=1; R<200000000ULL && left>0; R++){
    uint64_t x=R; int firstFound=0;
    for(int t=0;t<=6;t++){
      int ispal = (rev(x)==x);
      if(ispal && x>=10){
        int p=top2(x);
        for(int j=0;j<13;j++) if(ab[j]==p && bd[j]==t){
          if(!anyR[j]){anyR[j]=R;left--;}
          if(!firstFound && !firstR[j]){firstR[j]=R;left--;}
        }
      }
      if(ispal) firstFound=1;
      x=x+rev(x);
    }
  }
  for(int j=0;j<13;j++){
    uint64_t x=firstR[j]; printf("%d h=%d minFirstPalR=%llu path:",ab[j],bd[j],(unsigned long long)x);
    for(int t=0;t<=bd[j];t++){printf(" %llu",(unsigned long long)x);x=x+rev(x);}
    printf("   minAnyR=%llu\n",(unsigned long long)anyR[j]);
  }
  return 0;
}
