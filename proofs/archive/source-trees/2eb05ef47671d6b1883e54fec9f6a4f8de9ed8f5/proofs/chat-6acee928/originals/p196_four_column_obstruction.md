# P196：33 首部的精确五层定理与 360 类三位首部排除证书

日期：2026-10-14。本文给出局部排除结果，**不构成完整的十进制 196 猜想证明**。这里的“本轮所得”不表示已完成文献查新，也不主张学术首创。

设

\[
T(n)=n+\operatorname{rev}(n),\qquad
H(P)=\max\{k\ge0:\exists A\in\mathbb Z_{>0},\ T^k(A)=P\}.
\]

反转时舍去新产生的前导零。因为 \(T(n)>n\)，固定正整数 \(P\) 的 \(H(P)\) 总是有限的。本文研究的是对无穷多个不同 \(P\) 同时有效、与位数无关的上界。中间出现回文并不停止迭代，也不会被删除。

本文的两个结论是：

1. 每个以 **33** 开头的十进制回文 \(P\) 都满足 \(H(P)\le5\)。这个类别的上界恰为 5，且可以在第 5 步首次出现回文。
2. 文末表中列出的 **360 种三位首部**，分别具有不超过 14 的统一祖先深度上界。由于 196 的第 0 至 14 项均非回文，196 的整条轨道都不可能出现这些首部的回文。

第一项下面给出可逐列手工检查的证明；第二项使用明确的有限进位图和完整验证程序。360 是被排除的首部类别数，不能解释成“完整猜想已证明了多少比例”。第二项表中的上界一般不声称最优。

## 1. 对称数位和与进位

将 \(X\) 的数位从低到高记为 \(a_0,\ldots,a_{n-1}\)，定义

\[
q(X)_i=a_i+a_{n-1-i}=s_i.
\]

字 \(s\) 对称，每项属于 \(\{0,\ldots,18\}\)，首项正；奇数长度的中央项为偶数。这样的字也总可以由某个正整数实现。

反转相加的逐列公式为

\[
c_0=0,\quad c_{i+1}=\left\lfloor\frac{s_i+c_i}{10}\right\rfloor,
\quad b_i=s_i+c_i-10c_{i+1}.
\tag{1}
\]

所有进位均为 0 或 1。若 \(c_n=1\)，添最高位 1，称为增位，记 G；否则记 N。不增位不等于内部没有进位。

将 \(s\) 按式 (1) 规范化，再取输出数字的对称数位和，所得映射记为 \(F\)。于是

\[
q(T(X))=F(q(X)).
\tag{2}
\]

**一步回文判据。** \(T(X)\) 是回文，当且仅当满足以下一项：

- 全部 \(s_i\le9\)，此时一步完全无进位；
- 全部 \(s_i\in\{0,11\}\)，此时增位。

证明不增位的必要性：回文对称性给出

\[
c_i-c_{n-1-i}=10(c_{i+1}-c_{n-i}).
\]

左侧只能为 \(-1,0,1\)，所以两侧均为零。从 \(c_0=c_n=0\) 开始，向内归纳得到所有进位为零。

增位时首尾输出都为 1，所以 \(s_0=11,c_1=1\)。若已知 \(s_{i-1}=11c_i\) 及 \(c_i=c_{n-i+1}\)，比较相应输出得到

\[
s_i=10c_{i+1}+c_{n-i}.
\]

右边的两个进位必须相等：若为 1、0，则同一个原始和 10 在另一端不进位，矛盾；若为 0、1，则原始和 1 在另一端进位，也矛盾。因此 \(s_i=11c_{i+1}\)，归纳完成。充分性直接代入式 (1)。

进一步写 \(s_i=11e_i\)，\(e_i\in\{0,1\}\)，增位回文的输出数位是 \(e_i+e_{i-1}\)，边界外的 \(e\) 为零。故长度至少 3 的增位回文，其前三位只能为

\[
110,\quad111,\quad121,\quad122.
\tag{3}
\]

## 2. 两端逐列逆推公式

在不增位步骤中，读入某一对原始和 \(s\)，保存低端输入进位 \(x\) 与高端输出进位 \(y\)。向内的新进位记为 \(x',y'\)。若输出对称和为 \(p\)，则恰需

\[
x'=\left\lfloor\frac{s+x}{10}\right\rfloor,\qquad
y=\left\lfloor\frac{s+y'}{10}\right\rfloor,\qquad
p=2s+x+y'-10(x'+y).
\tag{4}
\]

初态为 \((x,y)=(0,0)\)。如果 \(p\ne9\)，可简化为

\[
x'=y,\quad y'=x\mathbin{\mathrm{xor}}(p\bmod2),\quad
s=10y+\frac{p-x-y'}2,
\tag{5}
\]

并检查 \(0\le s\le18\)，首项还须正。若 \(p=9\)，直接使用式 (4)，不能强行用式 (5)。

增位时，若输出对称和首项 \(j\le9\)，则来源首项为 \(j+9\)。输出第二项 \(b\) 满足

\[
j-1\le b\le j+9.
\tag{6}
\]

若 \(b=j-1\)，来源第二项必为 9，两端对应进位分别为 1 与 0；输出第三项因而至少为 9。若第三项也为 9，这个进位状态继续传播，输出第四项仍至少为 9。在本文使用的可行长度下，特别有

\[
F(s)=(3,2,9,d,\ldots)\text{ 且增位}
\quad\Longrightarrow\quad d\ge9.
\tag{7}
\]

这里的传播可直接检查：低端 \(9+1\) 输出 0、继续进位；高端输出进位为 0 的原始和 9，只能输入进位 0，输出 9。二者的输出对称和是 9；要继续维持这一值，下一低端输出又必须为零。

另有两个会用到的立即排除条件：没有一次反转相加的输出，其 \(q\) 首部为

\[
(1,b,\ldots),\ b>10;
\qquad (1,10,z,\ldots),\ z<8.
\tag{8}
\]

因为不增位输出的首对称和至少为 2，只需检查增位。此时来源首项为 10，输出第二项至多为 10；若恰为 10，来源第二项被迫为 18，输出第三项至少为 8。两位来源增到三位时，输出 \(q\) 为 \((j,2j,j)\)，不产生上述例外；一位来源也不会产生例外。

## 3. 33 首部定理：五层上界的手工证明

**定理。** 每个以 33 开头的回文 \(P\) 都满足 \(H(P)\le5\)。

先处理短目标：\(H(33)=3\)，由 \(3\to6\to12\to33\) 实现；其直接前驱只有 12、21、30，后两者无前驱，所以没有更深来源。\(333\) 的中央位为奇数，无法由无进位步骤产生；首位为 3，又不能由增位回文步骤产生，故 \(H(333)=0\)。

以下设 \(P\) 至少四位。反设存在六步链

\[
A_0\to A_1\to A_2\to A_3\to A_4\to A_5\to P.
\tag{9}
\]

最后一步必定不增位且没有内部进位，因此 \(q(A_5)\) 就是 \(P\) 的数位字，首部为 \((3,3,c,\ldots)\)，所有项均不超过 9。

用式 (4) 及增位公式逐层逆推。表中 \((a,b;S)\) 表示前两项为 \(a,b\)，第三项属于 \(S\)；只列必要条件，允许过度包含。

| 层 | 尚可能的前三项 |
|---|---|
| \(q(A_5)\) | \((3,3;\{0,\ldots,9\})\) |
| \(q(A_4)\) | \((1,11;\{9,\ldots,14\})\)，或 \((12,0;\{0,\ldots,18\})\)，或 \((12,9;\{9,\ldots,18\})\) |
| \(q(A_3)\) | \((6,0;\{0,\ldots,9\})\)，或 \((6,4;\{9,14,15,16,17,18\})\) |
| \(q(A_2)\) | \((3,0;\{0,\ldots,4\})\)，或 \((3,2;\{4,7,8,9\})\) |

第二行的 \((1,11,\ldots)\) 分支由式 (8) 排除。首项 12 的状态只能有不增位前驱；首部 \((6,0)\)、\((6,4)\) 的增位前驱被式 (6) 排除。因此表中后两次逆推均为 N。

如果 \(A_1\to A_2\) 不增位，式 (4) 给出

\[
q(A_1)=(1,10,z,\ldots),\ z\in\{0,1\},
\quad\text{或}\quad q(A_1)=(1,11,z,\ldots).
\]

两者都不可能有前驱 \(A_0\)，由式 (8) 矛盾。

所以 \(A_1\to A_2\) 必须增位。式 (6) 排除首部 \((3,0)\)，并在 \((3,2)\) 分支迫使第三项至少为 9。因此只剩

\[
q(A_2)=(3,2,9,d,\ldots),\qquad d\ge9.
\tag{10}
\]

下面证明剩余三步到 \(A_5\) 实际迫使 \(d\le7\)。这正是三位置逆推遗漏的约束。

假设 \(d\ge8\)。沿着表中已确定的 N、N、G 三步，用式 (1) 或 (4) 逐列计算，有

| 步骤 | 必然的前四项 |
|---|---|
| \(q(A_2)\) | \((3,2,9,d)\)，\(d\ge8\) |
| \(q(A_3)\) | \((6,4,18,w)\)，\(w\ge16\) |
| \(q(A_4)\) | \((12,9,17,v)\)，\(v\ge13\) |
| \(q(A_5)\) | \((3,3,8,e)\)，\(e\ge11\) |

核算如下。第一步前三对的相关进位均为零，相应高端输出进位为零还迫使 \(d\le9\)，故 \(w=2d+\alpha\ge16\)，\(\alpha\in\{0,1\}\)。第二步中，输出第二项为 9，强制相应高端进位为 1；由于 \(w\ge16\)，再向内的高端输出进位也为 1，因而第三项恰为 17，第四项

\[
v=2w+1+\gamma-20\ge13,\qquad \gamma\in\{0,1\}.
\]

第三步增位，来源首部为 \((12,9,17,v)\)。低端第四个输出数字为 \(v-9\ge4\)，与之配对的高端输出数字至少为 7，所以 \(e\ge11\)。这与 \(q(A_5)\) 全部为十进制数字、因而均不超过 9 矛盾。

故 \(d\le7\)，与式 (10) 的 \(d\ge9\) 冲突，六步链不可能存在。

长度边界没有被略去：表中首部为 \((12,0)\)、\((12,9)\) 的对称字至少三项，随后的 N 步保持长度；唯一需要第四项的分支 \((3,2,9,\ldots)\)，不可能长 3 或 4，长 5 又会有奇数中央项 9，所以至少长 6。上述四位置运算始终合法。定理得证。

**上界最优。** 直接相加得到

\[
1109090\to2018101\to3036203\to6062506
\to12115112\to33266233.
\]

最后一项是回文，之前所有项都不是回文。所以该类别的统一深度上界及首次命中上界都恰为 5。不是说每个 33 类目标的深度都等于 5。

结合上一轮十三类定理，已有完整两位首部排除类变为

\[
10,20,32,\mathbf{33},40,41,60,64,65,76,80,81,82,83.
\]

## 4. 四位置有限图：从单个定理推广到 360 类

为了避免把大量分支写成未经检查的手算表，现定义一个完整的有限上近似图。

顶点是全部四元组

\[
\mathcal V=\{1,\ldots,18\}\times\{0,\ldots,18\}^3,
\qquad |\mathcal V|=123462.
\]

若式 (4) 允许来源首部 \(s\) 产生目标首部 \(p\)，加入 N 边 \(p\to s\)。所有未知内部进位都枚举 0、1。

G 边的精确外侧递推为：若 \(p_0\le9\)，来源首项 \(s_0=p_0+9\)；若 \(p_0=10\)，来源首项 \(s_0=9\)；若 \(p_0>10\)，无 G 边。初态

\[
x=\lfloor s_0/10\rfloor,\qquad y=1.
\]

保存前一个原始和 \(v\)，对下一输出对称和 \(p_i\)，枚举 \(y'\in\{0,1\}\) 满足

\[
\lfloor(v+y')/10\rfloor=y.
\]

低端输出数字必须等于

\[
d=p_i-v-y'+10y\in\{0,\ldots,9\}.
\]

再枚举 \(x'\in\{0,1\}\)，取

\[
s_i=d+10x'-x\in\{0,\ldots,18\},
\]

更新 \((x,y)\gets(x',y')\)。第四项之后还检查最后一个已知高端列至少存在一个合法输入进位。程序完整保留全部分支。

这个图可能包含无法向中央延拓的路径；但每个真实、来源至少四位的反转相加步骤一定给出图中的一条边。因此，**图中没有长路径就足以排除真实长祖先链**。不需要声称每条图路径都能实现。

对无出边顶点赋秩 0；如果某顶点的所有出邻点已有有限秩，赋予

\[
r(p)=1+\max_{p\to s}r(s).
\tag{11}
\]

迭代直到不再赋值。赋了秩的顶点不可能有长度超过其秩的逆向路径。未赋秩的顶点不作排除结论。

完整计算有 185193 条不同的边，75482 个顶点取得有限秩，最大秩为 20。这里的“最大秩 20”是图的统计量，不是所有回文或所有整数的等待上界。

对回文首部 \(abc\)，从十个顶点 \((a,b,c,d)\)、\(0\le d\le9\) 出发。先排除式 (3) 的四种首部，因为它们可能由最后一步增位产生；其余首部的最后一步必定无进位。

若 \(b<a\)，第一条逆向图边还可限定为 N。理由是：若 \(X\to M\) 增位且 \(M\to P\) 无进位，式 (6) 的 \(b<a\) 只能取 \(b=a-1\)；随后式 (7) 的 9 与进位状态不断传播。由于全部目标对称和不超过 9，低端始终被迫延续进位 1，高端始终被迫为 0，最终同一中央进位被要求同时为 0、1，矛盾。这也包含短长度边界；两位来源增至三位的对称和为 \((j,2j,j)\)，不会下降。

记第一步所有允许出邻点的并集为 \(S_{abc}\)。若该集合为空，取 \(B(abc)=1\)；若非空且每个点都取得有限秩，取

\[
B(abc)=2+\max_{s\in S_{abc}}r(s).
\tag{12}
\]

于是所有由至少四位来源开始的链都满足 \(H(P)\le B(abc)\)。程序共得到 360 个 \(abc\)，最大 \(B\) 为 14。

**完整的短位数边界。** 若存在长 \(B+1\) 的反例链，并且其中某项少于四位，因为 \(T(n)>n\)，其初始数一定小于 1000。因此只须对全部 \(1\le A<1000\) 计算相应的 \(B+1\) 次迭代。程序检查全部这些情况，没有例外。这是一项有限边界证明，并非用有限数值试验替代无限长度论证。

上界的分布如下：

| 上界 B | 首部类别数 |
|---|---:|
| 1 | 55 |
| 2 | 53 |
| 3 | 110 |
| 4 | 69 |
| 5 | 15 |
| 6 | 17 |
| 7 | 7 |
| 8 | 13 |
| 9 | 5 |
| 10 | 4 |
| 11 | 2 |
| 12 | 7 |
| 13 | 1 |
| 14 | 2 |

特别地，\(B(120)=7\)、\(B(310)=13\)、\(B(561)=B(620)=14\)，而 \(B(680)=2\)。这些例子中的上界不声称最优。33 类四位置逆推的集合大小依次为

\[
100,346,171,107,62,0,
\]

与第 3 节的手工五层证明一致。

## 5. 对 196 轨道的全时排除与仍然缺少的论证

直接计算 \(N_0=196,N_{t+1}=T(N_t)\)，第 0 至 14 项为

\[
\begin{aligned}
&196,887,1675,7436,13783,52514,94039,187088,\\
&1067869,10755470,18211171,35322452,60744805,\\
&111589511,227574622.
\end{aligned}
\]

它们均非回文。如果以后某时刻 \(t>14\) 到达表中的回文 \(P\)，原轨道就给出 \(H(P)\ge t>14\ge B(abc)\)，矛盾。因此排除的是这 360 类目标的**全部未来时刻**。

但表外还有许多首部没有被排除。这里没有证明 196 只会到达表内首部，更没有证明其全部潜在回文都属于已排除的其他无限族。要完成原猜想，仍需覆盖剩余目标，或建立一条对 196 整条轨道保持、且与一切回文不相容的性质。

作为缺口的具体提醒，\(89\) 的轨道第 24 步首次达到 \(8813200023188\)；其首部 881 不在本表。这个事实只表明本表不是全部回文的统一等待定理，不说明 196 会到达该数。该轨道也可直接用同一个整数递推独立检查。

本文没有 Lean 形式化证明。第二项属于附带完整源码的有限状态计算证明；附带的 198702 个可行原始和字的逐列覆盖检查是额外交叉核验，不承担无限长度推理。公开的背景与轨道定义可参见 [OEIS A006960](https://oeis.org/A006960)；这里不将背景资料当作本文新推导的证明。

## 6. 全部 360 类首部与可重现程序

下表第一列是前两位，第二列的 `c:B` 表示第三位为 c 时，统一上界为 B；未列出的 c 不作结论。

| 前两位 | 第三位 : 上界 |
|---|---|
| 10 | 0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:1, 8:1, 9:1 |
| 12 | 0:7 |
| 13 | 0:1 |
| 14 | 0:1, 1:1 |
| 15 | 0:1, 1:1, 2:1 |
| 16 | 0:1, 1:1, 2:1, 3:1 |
| 17 | 0:1, 1:1, 2:1, 3:1, 4:1 |
| 18 | 0:1, 1:1, 2:1, 3:1, 4:1, 5:1 |
| 19 | 0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:7 |
| 20 | 0:2, 1:2, 2:2, 3:2, 4:2, 5:2, 6:2, 7:2, 8:2, 9:2 |
| 21 | 4:8, 5:8 |
| 24 | 0:2, 1:8 |
| 25 | 0:9, 6:7 |
| 26 | 0:2, 1:2, 2:2 |
| 27 | 2:6, 3:7 |
| 28 | 0:2, 1:2, 2:2, 3:2, 4:2 |
| 30 | 0:1, 1:2, 2:2, 3:2, 4:2, 5:2, 6:2, 7:2, 8:2 |
| 31 | 0:13 |
| 32 | 0:1, 1:2, 2:2, 3:2, 4:2, 5:2, 6:2, 7:2, 8:2, 9:2 |
| 33 | 0:5, 1:5, 2:5, 3:5, 4:5, 5:5, 6:5, 7:5, 8:5, 9:5 |
| 34 | 0:8, 1:8, 2:8, 3:8, 4:8, 5:8, 6:8, 7:8 |
| 35 | 0:2 |
| 36 | 0:1, 1:2 |
| 37 | 0:2, 1:2, 2:2, 6:8 |
| 38 | 0:1, 1:2, 2:2, 3:2 |
| 40 | 0:3, 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3, 9:3 |
| 41 | 0:3, 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3, 9:3 |
| 42 | 3:3, 4:9, 7:3, 8:3 |
| 47 | 8:7 |
| 48 | 0:3, 1:3, 2:9 |
| 50 | 0:1, 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3 |
| 52 | 0:1, 1:3, 5:3 |
| 53 | 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3, 9:3 |
| 54 | 0:1, 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3 |
| 56 | 0:5, 1:14 |
| 58 | 0:1, 1:3, 2:5, 9:5 |
| 59 | 1:11, 2:10 |
| 60 | 0:2, 1:2, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3, 9:3 |
| 61 | 0:3, 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3 |
| 62 | 0:14, 1:3, 5:3, 9:3 |
| 64 | 0:2, 1:2, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3, 9:3 |
| 65 | 0:6, 1:6, 2:6, 3:6, 4:6, 5:6, 6:6, 7:6, 8:6, 9:6 |
| 67 | 6:5 |
| 68 | 0:2 |
| 69 | 0:9, 1:9, 8:5 |
| 70 | 0:1, 1:2, 2:2, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3 |
| 72 | 0:1, 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3 |
| 73 | 1:12 |
| 74 | 0:1, 1:2, 2:2, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3 |
| 75 | 0:12, 4:12 |
| 76 | 0:1, 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3, 9:3 |
| 77 | 1:6, 2:6, 3:6, 4:6, 5:12, 6:12, 9:6 |
| 78 | 0:6, 1:12, 2:12 |
| 80 | 0:4, 1:4, 2:4, 3:4, 4:4, 5:4, 6:4, 7:4, 8:4, 9:4 |
| 81 | 0:4, 1:4, 2:4, 3:4, 4:4, 5:4, 6:4, 7:4, 8:4, 9:4 |
| 82 | 0:4, 1:4, 2:4, 3:4, 4:4, 5:4, 6:4, 7:4, 8:4, 9:4 |
| 83 | 0:4, 1:4, 2:4, 3:4, 4:4, 5:4, 6:4, 7:4, 8:4, 9:4 |
| 84 | 5:4, 6:4, 7:4, 8:4 |
| 85 | 0:10, 1:10, 2:4, 3:4, 4:4, 5:10 |
| 86 | 7:4, 8:4 |
| 90 | 0:1, 1:4, 2:4, 3:4, 4:11 |
| 92 | 0:1, 1:4, 2:7, 5:4 |
| 93 | 9:8 |
| 94 | 0:1, 1:4, 2:4, 3:4, 4:4, 5:4, 6:4, 7:4, 8:4 |
| 96 | 0:1, 1:4, 8:7 |
| 97 | 4:4, 5:4, 6:4 |
| 98 | 0:1, 1:4, 2:4, 3:4 |

将下列代码保存为 `four_column_obstruction.py`，用 Python 3 运行。仅依赖标准库，默认会重建整个有限图、验证秩、检查全部短位数边界，并输出完整首部表。

```python
"""Finite carry certificates; Python standard library only.

This is not a proof of the full 196 conjecture. The accompanying report
proves why these finite prefix certificates apply to unbounded lengths.
"""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product


def T(n):
    return n + int(str(n)[::-1])


def pal(n):
    a = str(n)
    return a == a[::-1]


def normalize(s):
    digits, carry = [], 0
    for u in s:
        carry, d = divmod(u + carry, 10)
        digits.append(d)
    if carry:
        digits.append(carry)
    return tuple(digits)


def forward(s):
    d = normalize(s)
    return tuple(a + b for a, b in zip(d, d[::-1]))


@lru_cache(None)
def inv_nongrowth(p):
    states = {((), 0, 0)}
    for i, v in enumerate(p):
        nxt = set()
        for word, x, y in states:
            for s in range(1 if i == 0 else 0, 19):
                xx = (s + x) // 10
                for yy in (0, 1):
                    if ((s + yy) // 10 == y
                            and 2*s + x + yy - 10*(xx + y) == v):
                        nxt.add((word + (s,), xx, yy))
        states = nxt
    return frozenset(word for word, _, _ in states)


@lru_cache(None)
def inv_growth(p):
    if p[0] > 10:
        return frozenset()
    first = p[0] + 9 if p[0] <= 9 else 9
    states = {((first,), first // 10, 1)}
    for v in p[1:]:
        nxt = set()
        for word, x, y in states:
            for yy in (0, 1):
                if (word[-1] + yy) // 10 != y:
                    continue
                digit = v - word[-1] - yy + 10*y
                if not 0 <= digit <= 9:
                    continue
                for xx in (0, 1):
                    s = digit + 10*xx - x
                    if 0 <= s <= 18:
                        nxt.add((word + (s,), xx, yy))
        states = nxt
    return frozenset(word for word, _, y in states
                     if any((word[-1] + z) // 10 == y for z in (0, 1)))


@lru_cache(None)
def inv_prefix(p):
    return inv_nongrowth(p) | inv_growth(p)


def graph_certificate():
    nodes = list(product(range(1, 19), range(19), range(19), range(19)))
    edges = {p: inv_prefix(p) for p in nodes}
    back = defaultdict(list)
    remaining = {p: len(vs) for p, vs in edges.items()}
    for p, vs in edges.items():
        for u in vs:
            back[u].append(p)
    queue = [p for p, n in remaining.items() if n == 0]
    rank = {p: 0 for p in queue}
    for u in queue:
        for p in back[u]:
            remaining[p] -= 1
            if remaining[p] == 0:
                rank[p] = 1 + max(rank[v] for v in edges[p])
                queue.append(p)
    # Check every assigned rank against every edge; no path is discarded.
    for p, h in rank.items():
        assert all(v in rank for v in edges[p])
        assert h == (1 + max(rank[v] for v in edges[p]) if edges[p] else 0)
    bounds = {}
    growth_pal_prefixes = {(1, 1, 0), (1, 1, 1), (1, 2, 1), (1, 2, 2)}
    for a, b, c in product(range(1, 10), range(10), range(10)):
        if (a, b, c) in growth_pal_prefixes:
            continue
        roots = {(a, b, c, d) for d in range(10)}
        inverse = inv_nongrowth if b < a else inv_prefix
        vs = {s for p in roots for s in inverse(p)}
        if not vs:
            bounds[100*a + 10*b + c] = 1
        elif all(s in rank for s in vs):
            bounds[100*a + 10*b + c] = 2 + max(rank[s] for s in vs)
    assert len(nodes) == 123462
    assert sum(map(len, edges.values())) == 185193
    assert len(rank) == 75482 and max(rank.values()) == 20
    assert len(bounds) == 360 and max(bounds.values()) == 14
    assert dict(sorted(Counter(bounds.values()).items())) == {
        1: 55, 2: 53, 3: 110, 4: 69, 5: 15, 6: 17, 7: 7,
        8: 13, 9: 5, 10: 4, 11: 2, 12: 7, 13: 1, 14: 2}
    return bounds


def raw_words(n):
    half = n // 2
    for first in range(1, 19):
        for tail in product(range(19), repeat=half-1):
            left = (first,) + tail
            if n % 2:
                for center in range(0, 19, 2):
                    yield left + (center,) + left[::-1]
            else:
                yield left + left[::-1]


def carry_coverage_check():
    count = 0
    for n in range(4, 9):
        for s in raw_words(n):
            d = normalize(s)
            p = forward(s)
            inverse = inv_growth if len(d) > n else inv_nongrowth
            assert s[:4] in inverse(p[:4]), (s, p)
            if len(d) > n and max(p) <= 9:
                assert p[1] >= p[0]
            count += 1
    assert count == 198702
    return count


def short_boundary_check(bounds):
    # If a (B+1)-step counterexample has any <4-digit entry, its initial
    # number is <1000, because T(n)>n. This is the entire small boundary.
    for root in range(1, 1000):
        n = root
        for k in range(1, max(bounds.values())+2):
            n = T(n)
            ds = str(n)
            if len(ds) >= 3 and ds == ds[::-1]:
                h = bounds.get(int(ds[:3]))
                assert h is None or k != h+1, (root, k, n, h)
        n = root
        for _ in range(6):
            n = T(n)
        assert not (pal(n) and str(n).startswith('33')), (root, n)


def prefix_33_check():
    layer = {(3, 3, c, d) for c, d in product(range(10), repeat=2)}
    counts = [len(layer)]
    for _ in range(5):
        layer = {s for p in layer for s in inv_prefix(p)}
        counts.append(len(layer))
    assert counts == [100, 346, 171, 107, 62, 0]
    path = [1109090]
    for _ in range(5):
        path.append(T(path[-1]))
    assert path == [1109090, 2018101, 3036203, 6062506, 12115112, 33266233]
    assert all(not pal(n) for n in path[:-1]) and pal(path[-1])
    return counts, path


def verify():
    bounds = graph_certificate()
    coverage = carry_coverage_check()
    short_boundary_check(bounds)
    counts, sharp_path = prefix_33_check()
    orbit = [196]
    for _ in range(14):
        orbit.append(T(orbit[-1]))
    assert not any(map(pal, orbit))
    delayed = [89]
    for _ in range(24):
        delayed.append(T(delayed[-1]))
    assert delayed[-1] == 8813200023188 and pal(delayed[-1])
    assert all(not pal(n) for n in delayed[:-1]) and 881 not in bounds
    return {'bounds': bounds, 'coverage': coverage, 'prefix_33_counts': counts,
            'sharp_path': sharp_path, 'orbit_through_14': orbit}


if __name__ == '__main__':
    result = verify()
    for k, v in result.items():
        print(k, v)
    print('All certificates passed. The full 196 conjecture remains unproved here.')
```

