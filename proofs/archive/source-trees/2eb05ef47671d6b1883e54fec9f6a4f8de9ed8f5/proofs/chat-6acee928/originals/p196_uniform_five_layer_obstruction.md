# P196 的继续推进：统一五层前驱障碍与锐利六步上界

本轮证明了一个不限制数位长度、不限制非零项数量的数位障碍。它把上一轮混合奇数数位定理中的“中央数位为 1 或 5”限制完全去掉。

本文的无界参数结论采用逐列进位方程证明；附录计算用于核验，不代替证明。完整 P196 猜想仍未证明，本文也不主张文献首创。

## 1. 本轮结果

令
\[
T(N)=N+\operatorname{rev}(N),\qquad N_t=T^t(196).
\]
反转忽略前导零。对 \(n\) 位正整数 \(X\)，从低位开始记数位 \(a_i\)，定义对称数位和
\[
q(X)_i=a_i+a_{n-1-i}.
\]

**统一五层障碍。**设 \(X\) 至少有五位，且
\[
q(X)_{2j+1}=0,\qquad
q(X)_{2j}\in\{0,10,12,14,16\}.
\tag{1}
\]
则不存在任何正整数 \(A\) 满足
\[
\boxed{T^5(A)=X.}
\tag{2}
\]
本定理不要求 \(11\mid A\)，不限制中间项是否为回文，也不限制非零对称和的数量。四层前驱确实可能存在，所以五层障碍不能直接改成四层。

用 \(D(V)\) 表示把 \(V\) 的每个数位重复两次，用 \(I(V)\) 表示在每两个相邻数位之间插入一个零。例如
\[
D(121)=112211,\quad I(121)=10201,
\quad D(V)=11I(V).
\]

**推广后的混合数字定理。**设 \(V\) 为正回文，其非零数位属于 \(\{1,3,5,7\}\)，非零数位个数为奇数 \(h\le21\)，数位和为 \(w\)，并满足
\[
w\equiv2h\pmod{11}.
\tag{3}
\]
中央数位可以是 1、3、5、7 中的任意一个。定义
\[
H_{11}(P)=\sup\{k\ge0:\ \exists A>0,\ 11\mid A,\ T^k(A)=P\}.
\]
则
\[
\boxed{H_{11}(D(V))\le6.}
\tag{4}
\]
六步是整个目标族的最佳统一上界，下面给出达到六步的实例。若 \(D(V)\) 是从一个非回文的 11 倍数起点出发遇到的第一个回文，则最晚在第二步出现；对每个符合条件的 \(V\)，都可以构造首次回文恰在第二步的起点。

**196 推论。**上述所有 \(V\)，允许任意对称配置、任意长度的零串，均满足
\[
\boxed{N_t\ne D(V)\quad(t\ge0).}
\tag{5}
\]
该结论控制任意出现时刻，而不只是首次出现。

## 2. 基础进位方程

令来源的原始对称和为 \(s_i\)。它是对称字，每项在 0 到 18 之间，首项正；奇数长度时中央项为偶数。这些条件也足以实现某个正整数来源。

令来源有 \(n\) 位，则
\[
c_0=0,\qquad
c_{i+1}=\lfloor(s_i+c_i)/10\rfloor,
\qquad b_i=s_i+c_i-10c_{i+1}.
\tag{6}
\]
若 \(c_n=1\)，添上最高位 \(b_n=1\)，称为增位。否则称不增位。

把原始和规范化为输出数位，再求输出的对称和，记为 \(F(s)\)。于是
\[
q(T(N))=F(q(N)).
\tag{7}
\]

对不增位的一步，从两端同时向中央推进。记
\[
x=c_i,\quad y=c_{n-i},\quad x'=c_{i+1},\quad y'=c_{n-1-i},
\]
当前来源和为 \(s\)，输出对称和为 \(p\)，则
\[
x'=\lfloor(s+x)/10\rfloor,\quad
 y=\lfloor(s+y')/10\rfloor,
\quad p=2s+x+y'-10(x'+y).
\tag{8}
\]

当 \(p\ne9\) 时，必有
\[
x'=y,\qquad y'=x\mathbin{\oplus}(p\bmod2),
\quad s=10y+\frac{p-x-y'}2.
\tag{9}
\]
证明：若 \(x'\ne y\)，同一原始和在两侧的进位判定不同，迫使 \(s=9\)；代入式 (8) 得 \(p=9\)，与假定矛盾。其他等式直接由式 (8) 得到。

由此有三项后果：

1. 不增位输出的最外对称和至少为 2。因为不增位迫使最外原始和 \(s_0\le9\)，且 \(s_0>0\)，输出首尾和为 \(2s_0+c_{n-1}\ge2\)。
2. 若不增位输出的对称和全部为偶数，从外状态 \((0,0)\) 出发，式 (9) 强制所有状态仍为 \((0,0)\)，来源和逐项为 \(p/2\)。所有进位为零，输出是回文。
3. 偶数长度的不增位输出，若其对称和不含 9，则前半部的奇数项数量必须是偶数。因为状态异或每次改变 \(p\bmod2\)，而外边界与中央边界的状态异或都为零。

一步回文判据也会使用：
\[
T(N)\text{ 为回文}
\iff
(\forall i,\ s_i\le9)
\quad\text{或}\quad
(\forall i,\ s_i\in\{0,11\}).
\tag{10}
\]
前一情形不增位且完全无进位；后一情形增位，输出为 \(11U\)，其中 \(U\) 为只含 0、1 的回文。

不增位部分的证明来自输出两侧相等：进位之差的绝对值至多 1，却必须等于另一个进位之差的 10 倍，故两者均为零，从边界向内得到全部进位为零。

增位部分：首尾输出为 1，先得到 \(s_0=11\)。向内归纳得到
\(s_i=10c_{i+1}+c_{n-i}\)。这两个进位必须相等，否则分别产生“和为 10 却无进位”或“和为 1 却有进位”的矛盾。因此所有 \(s_i\) 均为 0 或 11。反向直接代入式 (6) 即可验证。

## 3. 增位输出的短前缀限制

若输出增位，最外对称和为 \(j\le9\)，则来源最外原始和为
\[
s_0=j+9.
\]
输出次高位为 \(j-1+c_{n-1}\)，所以
\[
j-1\le q(T(N))_1\le j+9.
\tag{11}
\]

以下表格只列出实际数位存在时的必要条件。来源的第二原始和记为 \(s_1\)。使用式 (6)，再检查高端进位确实可以产生，得到：

| 输出前两项 \((j,p_1)\) | 可能的来源前两项 \((s_0,s_1)\) | 输出第三项 \(p_2\) 的下界 |
|---|---|---:|
| \((1,0)\) | \((10,9)\) | 9 |
| \((1,5)\) | \((10,4)\)、\((10,13)\) | 3 |
| \((1,10)\) | \((10,18)\) | 8 |
| \((2,10)\) | \((11,8)\)、\((11,17)\) | 7 |
| \((3,10)\) | \((12,7)\)、\((12,16)\) | 6 |

例如 \(j=1,p_1=10\) 时，次高输出数位只能为 1，次低输出数位只能为 9，因此 \(s_1=18\)；与它相对应的下一高端数位至少为 8，得到第三项至少为 8。其他各行同样逐列计算。

还有一个特殊的首项 10 障碍。若增位输出的对称和满足
\[
p_0=10,\qquad p_1=p_3=0,
\]
则
\[
p_2\in\{1,2\}.
\tag{12}
\]
证明：首项给出 \(s_0=9,c_1=0,c_n=1\)。\(p_1=0\) 给出
\(c_{n-1}=1,s_1=10,c_2=1\)。令 \(z=c_{n-2}\)，由 \(p_3=0\) 得
\(s_2+c_{n-3}=10z\)，所以 \((z,s_2)\) 仅可能为 \((0,0),(1,9),(1,10)\)。因此
\[
p_2=(s_2+1)\bmod10+z\in\{1,2\}.
\]
五位输出发生中央重合时，这些等式仍然成立。

## 4. 统一五层障碍的完整手算证明

设 \(Q_0=q(X)\) 满足式 (1)。由于 \(Q_0\) 对称、最外项正、所有奇数位置为零，它的长度必为奇数。

假设存在逐层前驱，记其原始对称和为
\[
F(Q_1)=Q_0,\quad F(Q_2)=Q_1,\quad\ldots.
\]
如果某层不存在前驱，证明已经结束。以下只列出前驱存在时的必要条件。

**第一层。**来源不可能增位：输出最外对称和大于 10 时立即不可能；等于 10 时，式 (12) 与 \(Q_{0,2}\in\{0,10,12,14,16\}\) 矛盾。因此第一层不增位。\(Q_0\) 全为偶数，由式 (9)，
\[
Q_1=Q_0/2.
\]
令其最外项为 \(A\)，下一偶数位置为 \(B\)，则
\[
Q_1=(A,0,B,0,\ldots),
\quad A\in\{5,6,7,8\},
\quad B\in\{0,5,6,7,8\}.
\]

**第二层。**由式 (11)，最外项至少为 5、第二项为零的 \(Q_1\) 不能由增位产生。所以第二层也不增位。应用式 (9) 得到下表。

**第三层。**第二层表中的前缀也排除了增位：前两项为 \((3,0)\)、\((4,0)\) 时违反式 (11)；前缀为 \((2,10,2/3)\)、\((3,10,2/3)\) 时违反上一节表格中第三项的下界。故第三层仍不增位，再应用式 (9)。

| \(A\) | \(Q_2\) 的必要前三项 | \(Q_3\) 的必要前三项 |
|---:|---|---|
| 5 | \((2,10,2/3)\) | \((1,5,1)\) |
| 6 | \((3,0,0/2/3/4)\) | \((1,10,0/1)\) |
| 7 | \((3,10,2/3)\) | \((1,15,0/1)\) |
| 8 | \((4,0,0/2/3/4)\) | \((2,0,0/1/2)\) |

斜线表示允许值集合，而非除法。无法满足中央条件或遇到不允许的零时，分支提前结束；这只会减少可能性。

**第四层。**前三行的首项为 1，因此不可能有不增位前驱。它们也不可能有增位前驱：

- \((1,5,1)\) 的第三项小于 3；
- \((1,10,0/1)\) 的第三项小于 8；
- \((1,15,\ldots)\) 的第二项大于式 (11) 允许的 10。

因此，第四层只可能来自最后一行。其 \(Q_3\) 前两项为 \((2,0)\)，式 (11) 排除增位，式 (9) 又强制
\[
\boxed{Q_4\text{ 的前三项为 }(1,0,0)\text{ 或 }(1,0,1).}
\tag{13}
\]

**第五层。**式 (13) 的首项为 1，排除不增位前驱；其第二项为零，而第三项小于 9，排除增位前驱。因此第五层为空。

这就证明 \(X\notin T^5(\mathbb Z_{>0})\)。整个证明只使用前缀和合法进位方程，没有限制后续数位的长度、非零项数量或中央取值。∎

## 5. 与最后两步进位段数的联系

为使推论可独立复核，这里重述所需的进位结构，并给出证明要点。

如果 \(X\to M\) 增位，而 \(M\to P\) 无进位，则第一步进位满足
\[
e_i=c_{i+1}=c_{n-i},\qquad u_i=s_i-9e_i,
\tag{14}
\]
其中 \(u\) 为合法回文数位字，且 \(P=11U\)。

证明进位对称性：第二步无进位给出 \(b_i+b_{n-i}\le9\)。最外侧先得 \(c_1=c_n=1\)。令缺陷 \(\delta_i=c_{i+1}-c_{n-i}\)，首尾为零。第一个负缺陷迫使 \(s_i=9,c_i=0\)，于是 \(b_i=9\)，其对应数位至少为 1，矛盾。正缺陷则迫使 \(s_i=9,c_i=1,c_{n-i-1}=0\)，对应高端数位为 9；无进位要求下一低端输出为零，继续迫使下一缺陷为正。正缺陷传播到零边界也矛盾。因此全部缺陷为零。随后直接代入式 (6)，得到输出对称和 \(u_i+u_{i-1}\)，即 \(P=11U\)。

现在令 \(P=D(V)=11I(V)\)。唯一除法强制 \(U=I(V)\)，其非零位置全为偶数位置。进位 1 段只能在 \(u_i>0\) 的位置启动；由对称性，每段终点也在这样的偶数位置。每段对交错和的贡献恰为 1。

若共有 \(k\) 段，\(V\) 非零数位个数为 \(h\)、数位和为 \(w\)，则
\[
1\le k\le h,\qquad
\sum_i(-1)^ie_i=k,
\quad \sum_i(-1)^iu_i=w.
\tag{15}
\]
当中央数位为奇数时，来源中央原始和必须为偶数，强制中央进位为 1，所以 \(k\) 为奇数。

来源 \(X\) 的长度为奇数，因此若 \(11\mid X\)，
\[
0\equiv2X\equiv\sum_i(-1)^is_i
=w+9k\equiv w-2k\pmod{11}.
\tag{16}
\]

如果 \(k=h\)，每一进位段必须是一个孤立单点，且恰好占据一个非零位置。于是
\[
\boxed{q(X)_i=u_i+9\mathbf1_{u_i>0}.}
\tag{17}
\]

## 6. 推广后的六步定理及首次回文两步定理

设 \(V\) 满足式 (3) 的条件，\(P=D(V)\)。非零数位个数为奇数，故 \(V\) 为奇数长度，中央数位为 1、3、5、7 之一。

考察从任意 11 的倍数出发、在第 \(t\ge2\) 步到达 \(P\) 的路径。11 的整除性在反转相加中保持。

最后一步不能增位：根据式 (10)，增位回文的商 \(P/11\) 必须为二进制数位回文。但唯一的商为 \(I(V)\)。若 \(V\) 含 3、5、7，则商不是二进制数位字；若其全部非零数位都是 1，则商的中央项为 1，要求来源中央原始和为 11，不合法。

最后两步也不能都不增位：最后无进位要求中间项的对称和等于 \(P\) 的数位字。它不含 9，前半部恰有奇数个奇数项 \(h\)，违反第 2 节的奇偶性质。

因此最后两步只能是“增位、无进位”。由式 (16)、中央进位的奇偶性，
\[
k\equiv h\pmod{11},\qquad k\equiv h\pmod2,
\quad1\le k\le h\le21.
\]
也即 \(k\equiv h\pmod{22}\)，唯一可能是 \(k=h\)。由式 (17)，最后两步之前的数 \(X\) 的对称和恰满足式 (1)：其非零项为 \(v_j+9\in\{10,12,14,16\}\)，所有奇数位置为零。

统一五层障碍说明 \(X\) 最多有四层前驱。因此
\[
t-2\le4,\qquad t\le6.
\]
这证明式 (4)，并且覆盖所有中间回文情况。∎

如果 \(P\) 是该路径中的第一个回文，\(t\ge3\) 时 \(X\) 有前驱。第 4 节第一层证明说明该前驱不增位，而 \(q(X)\) 全为偶数，所以 \(X\) 已经是回文，与首次性矛盾。因此首次到达这个目标族的回文只能在前两步。

这个两步上界对每一个符合条件的 \(V\) 都可以达到：取式 (17) 的可实现原始和字 \(s\)，在最外数位对上选择高位为 \(v_0\)、低位为 9，其余数位对合法分配，中央数位为 \((v_{\rm mid}+9)/2\)。得到非回文起点 \(A\)，且
\[
2A\equiv w+9h\equiv0\pmod{11}.
\]
第一步增位，最高位为 1、最低位为 \(v_0-1\in\{0,2,4,6\}\)，所以中间项非回文；第二步恰为 \(D(V)\)。∎

“首次回文最多两步”只适用于本文明确规定的目标族；这里没有给所有可能回文的首次到达时间一个统一上界。

## 7. 六步上界可以达到

取
\[
A=1003100101010909090299000,
\qquad 11\mid A.
\]
直接计算得：

| 步数 | 轨道项 | 是否回文 |
|---:|---|---|
| 0 | 1003100101010909090299000 | 否 |
| 1 | 1013021010101010100312001 | 否 |
| 2 | 2015151020202020201515102 | 是 |
| 3 | 4030302040404040403030204 | 否 |
| 4 | 8050605080808080805060508 | 是 |
| 5 | 16101210161616161610121016 | 否 |
| 6 | 77113311777777777711331177 | 是 |

最后一项为
\[
D(7131777771317).
\]
其 \(h=13,w=59\)，满足 \(59\equiv26\pmod{11}\)。因此
\[
\boxed{H_{11}(D(7131777771317))=6.}
\]
第 4 步的数满足式 (1)，并具有四层前驱，所以统一五层障碍也是锐利的。

这条路径在第 2 步已经出现另一个回文，故六步例子与首次回文两步定理没有冲突。例子还显示，回文之后的下一项可以再次成为非回文，不能假设回文性在迭代中保持。

## 8. 对 196 的全时刻排除

\(N_3=7436\) 是 11 的倍数，且 \(11\mid N_t\) 对 \(t\ge3\) 保持。若上述目标在 \(t\ge3\) 时出现，式 (4) 强制
\[
t\le3+6=9.
\]
前十项为
\[
196,887,1675,7436,13783,52514,94039,
187088,1067869,10755470.
\]
最大仅有八位。

若 \(h\ge5\)，目标至少有十位，全部排除。\(h=1\) 无法满足式 (3)。\(h=3\) 时，写三个非零数位为 \(a,c,a\)，检查
\[
2a+c\equiv6\pmod{11},\qquad a,c\in\{1,3,5,7\},
\]
只有两种：\((a,c)=(5,7)\)、\((7,3)\)。因此目标分别是
\[
55\,0^{2r}77\,0^{2r}55,
\qquad
77\,0^{2r}33\,0^{2r}77,
\quad r\ge0.
\]
\(r\ge1\) 时至少有十位；\(r=0\) 的 \(557755,773377\) 均不在前十项中。由此证明式 (5)。∎

## 9. 核验与剩余缺口

本轮自包含程序运行通过：

- 75,447 个可实现原始和字，检查真实加法中的短前缀进位限制；
- 七项前缀覆盖的五层反推计数为 \(500,100,56,17,2,0\)；
- 3,748 个完整的高对称和字，检查五层前驱为空，以及第四层必须具有式 (13) 前缀；
- 4,098 个混合数位目标，检查全部最后两步分支、五层障碍及首次回文恰在两步的构造；
- 六步锐性路径与 196 的前十项。

中央数位限制已经去掉，但 \(h\le21\) 与 \(w\equiv2h\pmod{11}\) 仍然需要。当 \(h\ge23\) 时，\(k=h-22\) 也可能符合段数条件，不能继续强迫所有进位孤立。

此前的五对 7 剩余分支是“锚点为 16，其余位置为 9”的原始和语言，不满足本轮要求的奇数位置为零；本轮没有排除它。\(55\,0^{2r}\,55\) 也仍在未解决范围。

本文所得是一个统一的数位前驱障碍及扩大的无限回文排除族，没有证明 196 永远不出现任何回文。

## 附录：自包含核验代码

只使用 Python 标准库。代码不读取其他证明文件，不调用网络。

```python
from itertools import product
from collections import Counter
from functools import lru_cache

def T(n): return n+int(str(n)[::-1])
def D(v): return int(''.join(x*2 for x in str(v)))
def I(v): return int('0'.join(str(v)))
def ds(n): return tuple(map(int,str(n)[::-1]))
def q(n):
 a=ds(n);return tuple(x+y for x,y in zip(a,a[::-1]))
def normalize(s):
 a=[];carry=0
 for x in s:
  carry,x=divmod(x+carry,10);a.append(x)
 if carry:a.append(carry)
 return tuple(a)
def F(s):
 a=normalize(s);return tuple(x+y for x,y in zip(a,a[::-1]))
def feasible(s):
 return bool(s) and s[0]>0 and s==s[::-1] and all(0<=x<=18 for x in s) and (len(s)%2==0 or s[len(s)//2]%2==0)
def representative(s):
 a=[0]*len(s)
 for i in range(len(s)//2):
  a[-1-i]=max(1 if i==0 else 0,s[i]-9);a[i]=s[i]-a[-1-i]
 if len(s)%2:a[len(s)//2]=s[len(s)//2]//2
 return sum(d*10**i for i,d in enumerate(a))

@lru_cache(maxsize=10000)
def inverse(qt):
 # Exact inverse of F on feasible symmetric digit-sum words.
 L=len(qt);ans=set()
 for grow in (0,1):
  n=L-grow
  if n<1:continue
  half=(n+1)//2
  if not grow:
   states=[((),0,0)]
   for p in qt[:half]:
    nxt=[]
    for word,x,y in states:
     for u in range(1 if not word else 0,19):
      xx=(u+x)//10
      for yy in (0,1):
       if (u+yy)//10==y and 2*u+x+yy-10*(xx+y)==p:
        nxt.append((word+(u,),xx,yy))
    states=nxt
   words=[word for word,_,_ in states]
  else:
   if qt[0]>10:continue
   u=qt[0]+9 if qt[0]<=9 else 9
   states=[((u,),u//10,1)]
   for p in qt[1:half]:
    nxt=[]
    for word,x,y in states:
     for yy in (0,1):
      if (word[-1]+yy)//10!=y:continue
      b=p-word[-1]-yy+10*y
      if 0<=b<=9:
       for xx in (0,1):
        u=b+10*xx-x
        if 0<=u<=18:nxt.append((word+(u,),xx,yy))
    states=nxt
   words=[word for word,_,_ in states]
  for word in words:
   s=word+word[:n//2][::-1]
   if feasible(s) and F(s)==qt:ans.add(s)
 return tuple(sorted(ans))

def v2(n):
 k=0
 while n%2==0:k+=1;n//=2
 return k

def with_gaps(values,gaps):
 # Palindromic nonzero skeleton and its symmetric zero gaps.
 a=len(gaps);allgaps=tuple(gaps)+tuple(gaps)[::-1]
 assert len(values)==2*a+1
 return int(''.join(str(x)+('0'*allgaps[i] if i<len(allgaps) else '') for i,x in enumerate(values)))


@lru_cache(None)
def inverse_prefix(q):
 K=len(q);ans=set()
 # Keep K-1 outer layers; the omitted layer certifies the boundary carry.
 states={((),0,0)}
 for i,p in enumerate(q):
  nxt=set()
  for word,x,y in states:
   for u in range(1 if i==0 else 0,19):
    xx=(u+x)//10
    for yy in (0,1):
     if (u+yy)//10==y and 2*u+x+yy-10*(xx+y)==p:
      nxt.add((word+(u,),xx,yy))
  states=nxt
 for word,x,y in states:ans.add(word[:-1])
 if q[0]<=10:
  u=q[0]+9 if q[0]<=9 else 9
  states={((u,),u//10,1)}
  for p in q[1:]:
   nxt=set()
   for word,x,y in states:
    for yy in (0,1):
     if (word[-1]+yy)//10!=y:continue
     digit=p-word[-1]-yy+10*y
     if not 0<=digit<=9:continue
     for xx in (0,1):
      u=digit+10*xx-x
      if 0<=u<=18:nxt.add((word+(u,),xx,yy))
   states=nxt
  for word,x,y in states:
   if any((word[-1]+z)//10==y for z in (0,1)):ans.add(word[:-1])
 return tuple(sorted(ans))


def high_words(max_length):
 C=(10,12,14,16)
 for n in range(1,max_length+1,2):
  if n==1:
   for c in C:yield (c,)
   continue
  h=n//2;places=list(range(0,h,2))
  for vals in product(C,range(1)): # outer entry is nonzero
   first=vals[0]
   for tail in product((0,)+C,repeat=len(places)-1):
    left=[0]*h
    for i,c in zip(places,(first,)+tail):left[i]=c
    centers=((0,)+C) if h%2==0 else (0,)
    for c in centers:yield tuple(left)+(c,)+tuple(left[::-1])

def check_prefix_certificate():
 C=(10,12,14,16)
 states={(c,0,a,0,b,0,d) for c in C for a,b,d in product((0,)+C,repeat=3)}
 counts=[len(states)]
 for _ in range(5):
  states={p for q in states for p in inverse_prefix(q)};counts.append(len(states))
 assert counts==[500,100,56,17,2,0],counts
 print('prefix certificate:',counts,flush=True)

def check_full_high_words():
 count=0;maximum=0
 for q0 in high_words(17):
  states={q0};height=-1
  while states:
   height+=1
   assert height<=4,(q0,states)
   if len(q0)>=5 and height==4:
    assert all(s[:3] in ((1,0,0),(1,0,1)) for s in states)
   states={p for q in states for p in inverse(q)}
  count+=1;maximum=max(maximum,height)
 assert count==3748,(count,maximum)
 print('full high-word cases:',count,'maximum depth:',maximum,flush=True)

def all_raw_words(max_length):
 for n in range(1,max_length+1):
  if n==1:
   for c in range(2,19,2):yield (c,)
   continue
  for first in range(1,19):
   for tail in product(range(19),repeat=n//2-1):
    left=(first,)+tail
    centers=range(0,19,2) if n%2 else (None,)
    for c in centers:yield left+(c,)+left[::-1] if c is not None else left+left[::-1]

def check_growth_rules():
 count=0
 for s in all_raw_words(7):
  a=normalize(s);p=F(s);growth=len(a)>len(s)
  if not growth:assert p[0]>=2
  elif p[0]<=9 and len(p)>=3:
   j=p[0];assert j-1<=p[1]<=j+9
   if j==1 and p[1]==0:assert p[2]>=9
   if j==1 and p[1]==5:assert p[2]>=3
   if j==1 and p[1]==10:assert p[2]>=8
   if j in (2,3) and p[1]==10:assert p[2]>=6
  count+=1
 assert count==75447
 print('actual integer carry-rule checks:',count,flush=True)

def check_generalized_targets():
 count=0;by_h=[]
 for h in (3,5,7,9,11,13):
  skeletons=0;a=(h-1)//2
  for left in product((1,3,5,7),repeat=a):
   for center in (1,3,5,7):
    values=left+(center,)+left[::-1]
    if (sum(values)-2*h)%11:continue
    skeletons+=1
    for gaps in ((0,)*a,tuple(i%2 for i in range(a))):
     v=with_gaps(values,gaps);target=D(v);raw=ds(target)
     parents=inverse(raw)
     assert not any(len(s)==len(raw) for s in parents)
     gn={s for s in parents if len(s)==len(raw)-1 and representative(s)%11==0}
     expected=tuple(x+9 if x else 0 for x in ds(I(v)))
     assert gn=={expected},(v,gn)
     roots={expected}
     for _ in range(5):roots={p for q in roots for p in inverse(q)}
     assert not roots,v
     # Every target has a first-hit two-step source divisible by 11.
     root=representative(expected)
     assert root%11==0 and str(root)!=str(root)[::-1]
     middle=T(root)
     assert str(middle)!=str(middle)[::-1] and T(middle)==target
     count+=1
  by_h.append((h,skeletons))
 print('generalized target cases:',count,'skeleton counts:',by_h,flush=True)

def check_sharpness_and_196():
 root=1003100101010909090299000;n=root;path=[]
 for k in range(7):path.append(n);assert n%11==0;n=T(n)
 assert path==[1003100101010909090299000,1013021010101010100312001,2015151020202020201515102,4030302040404040403030204,8050605080808080805060508,16101210161616161610121016,77113311777777777711331177]
 V=7131777771317
 assert len(str(V))==13 and sum(map(int,str(V)))==59 and D(V)==path[-1]
 q0=q(path[4]);assert all(x==0 if i%2 else x in (0,10,12,14,16) for i,x in enumerate(q0))
 states={q0}
 for _ in range(4):states={p for z in states for p in inverse(z)}
 assert q(root) in states
 states={p for z in states for p in inverse(z)};assert not states
 n=196;early=[]
 for _ in range(10):early.append(n);n=T(n)
 assert early[-1]==10755470 and all(n not in (557755,773377) for n in early)
 print('sharp six-step 11-multiple source:',root,flush=True)
 print('196 initial segment:',early,flush=True)

if __name__=='__main__':
 check_growth_rules();check_prefix_certificate();check_full_high_words();check_generalized_targets();check_sharpness_and_196()
```
