# P196 的继续推进：进位段计数定理与七对同数字的无限排除族

本轮得到一项更广的轨道排除结论。记 \(0^j\) 为连续 \(j\) 个零，下面的表达式均表示十进制数位串的连接。对任意 \(a,b,c\ge0\) 和 \(d\in\{1,\ldots,9\}\)，196 的反转相加轨道在任何时刻都不出现

\[
dd\,0^{2a}\,dd\,0^{2b}\,dd\,0^{2c}\,dd\,
0^{2c}\,dd\,0^{2b}\,dd\,0^{2a}\,dd.
\tag{A}
\]

零串允许为空，所以结论也包括十四个相同数字组成的回文。这里的三个零串参数没有上界。

此外，对五对同数字的族

\[
dd\,0^{2a}\,dd\,0^{2b}\,dd\,0^{2b}\,dd\,0^{2a}\,dd
\tag{B}
\]

排除了 \(d\in\{1,2,3,4,5,6,8,9\}\)，\(d=7\) 尚未排除。

支撑这些结论的是一个纯数位的充要条件，以及一个可复核的七层前驱障碍。后者有一部分采用有限的精确数位枚举：通过前缀覆盖证明把任意长度归约到固定的 32 个前缀，以及 32 个短字。它不是检查某个很大的迭代次数后猜测结论。本文明确保留这一计算机辅助证明的性质，不把它说成已经完成了全部手算化或形式化验证。

完整的 196 猜想仍未在本轮得到证明。上一轮剩余的 \(55\,0^{2r}\,55\) 也仍未排除。本文不主张文献首创。

## 1. 定义和进位工具

令

\[
T(N)=N+\operatorname{rev}(N),\qquad N_t=T^t(196).
\]

反转忽略前导零。对 \(n\) 位正整数 \(N\)，从低位开始记其数位为 \(a_i\)，并记

\[
q(N)_i=a_i+a_{n-1-i}=s_i.
\]

可实现的对称和字恰好满足

\[
s_i=s_{n-1-i},\quad 0\le s_i\le18,\quad s_0>0,
\]

并且奇数长度的中央项为偶数。计算 \(T(N)\) 的规则是

\[
c_0=0,\qquad
c_{i+1}=\lfloor(s_i+c_i)/10\rfloor,\qquad
b_i=s_i+c_i-10c_{i+1}.
\tag{1}
\]

若 \(c_n=1\)，再添最高位 1，称这一步增位。所有进位均为 0 或 1。

把 \(s\) 按式 (1) 规范化成实际数位，再计算对称数位和，所得映射记作 \(F\)。因此

\[
q(T(N))=F(q(N)).
\tag{2}
\]

以下两个工具已在上一份推导中证明，这里重述其内容和证明要点。

**一步回文判据。**

\[
T(N)\text{ 为回文}
\iff
(\forall i,\ s_i\le9)
\quad\text{或}\quad
(\forall i,\ s_i\in\{0,11\}).
\tag{3}
\]

前一种情形完全无进位；后一种情形增位，输出为 \(11U\)，其中 \(U\) 是只含 0、1 的回文。证明从首尾输出数位相等开始向中央推进：不增位时逐层迫使进位全为零；增位时有
\(s_i=10c_{i+1}+c_{n-i}\)，两个进位不相等分别导致“列和 1 产生进位”或“列和 10 不产生进位”的矛盾。

**增位后无进位的工具。**若 \(N\to M\) 增位，而 \(M\to P\) 完全无进位，则

\[
c_{i+1}=c_{n-i},\qquad
u_i=s_i-9c_{i+1}
\tag{4}
\]

组成一个合法回文 \(U\)，且 \(P=11U\)。

简述式 (4) 中进位对称性的证明。第二次无进位给出
\(b_i+b_{n-i}\le9\)，其中 \(b_n=1\)。外层先迫使 \(c_1=c_n=1\)。令
\(\delta_i=c_{i+1}-c_{n-i}\)，首尾均为零。第一个负缺陷迫使 \(b_i=9\) 而相对数位至少为 1，矛盾；第一个正缺陷则迫使下一层仍为正缺陷，并持续传播到已知为零的边界，也矛盾。具体地，正缺陷给出
\(s_i=9,c_i=1,c_{n-i-1}=0\)，于是 \(b_{n-i-1}=9\)，第二次无进位要求 \(b_{i+1}=0\)，从而
\(s_{i+1}=9,c_{i+2}=1\)。得到进位对称性后，令 \(u_{-1}=u_n=0\)，直接代入式 (1) 可得
\(b_i+b_{n-i}=u_i+u_{i-1}\)，故 \(P=11U\)。

两个轨道事实也会反复使用：

\[
N_0,\ldots,N_4=196,887,1675,7436,13783,
\]

\[
11\mid N_t\quad(t\ge3),\qquad 3\nmid N_t\quad(t\ge0).
\tag{5}
\]

第一项来自 \(11\mid7436\) 及
\(\operatorname{rev}(N)\equiv(-1)^{n-1}N\pmod{11}\)；
第二项来自 \(N_t\equiv2^t196\pmod3\)。

## 2. 新的进位段计数定理

对任意正整数回文 \(V\)，定义 \(D(V)\) 为把每个十进制数位重复两次得到的数。例如

\[
D(10201)=1100220011.
\]

设：

- \(w\) 为 \(V\) 的数位和；
- \(a\) 为 \(V\) 严格位于中央左侧的非零数位个数；
- \(c\) 为 \(V\) 的中央数位；偶数位数时定义 \(c=0\)。

**定理 1。**存在 \(11\) 的正倍数 \(N\)，使

\[
N\longrightarrow T(N)\longrightarrow D(V)
\]

第一步增位、第二步不增位，当且仅当存在整数 \(k\) 满足

\[
w-2k\equiv0\pmod{11},
\tag{6}
\]

其中

\[
\begin{cases}
k\in\{1,3,\ldots,2a+1\},&c\text{ 为奇数},\\
k\in\{2,4,\ldots,2a\},&c\text{ 为偶数}.
\end{cases}
\tag{7}
\]

第二个集合在 \(a=0\) 时为空。定理不要求中间项非回文，因而可以用于轨道中的任意出现时刻。

**证明。**设 \(V\) 有 \(m\) 位。从低到高记其数位为 \(v_j\)，令

\[
U=\sum_{j=0}^{m-1}v_j10^{2j}.
\]

于是 \(D(V)=11U\)，\(U\) 有 \(2m-1\) 位，是回文，所有奇数位置的数位都是零。乘以 11 没有进位。

由式 (3) 和 (4)，任意符合增长模式的来源都具有

\[
s_i=u_i+9e_i,\qquad e_i=c_{i+1}\in\{0,1\},
\tag{8}
\]

其中 \(e\) 对称，首尾为 1。零到一的进位转换只能发生在 \(u_i>0\) 的位置。由对称性，每个连续的 1 段的终点也在 \(u_i>0\) 的位置。

这些起点、终点都是偶数位置，所以每一个 1 段长度为奇数，对交错和
\(\sum_i(-1)^ie_i\) 的贡献恰好为 1。若共有 \(k\) 个 1 段，则

\[
\sum_i(-1)^ie_i=k,\qquad
\sum_i(-1)^iu_i=w.
\tag{9}
\]

中央原始和必须为偶数，故 \(e_{\mathrm{mid}}\equiv c\pmod2\)。
当 \(c\) 为奇数时，有一个跨中央的 1 段，其余成对出现，可能的段数恰为
\(1,3,\ldots,2a+1\)。
当 \(c\) 为偶数时，中央进位为零，所有段成对出现，可能的段数恰为
\(2,4,\ldots,2a\)。

来源 \(N\) 的位数为奇数 \(2m-1\)，因此

\[
2N\equiv T(N)
\equiv\sum_i(-1)^is_i
=w+9k
\equiv w-2k\pmod{11}.
\tag{10}
\]

于是 \(11\mid N\) 等价于式 (6)，必要性得证。

反过来，给定满足式 (6)、(7) 的 \(k\)，可以把左半部的非零位置分组，取每组首末位置之间为一个 1 段，再镜像到右半部。\(k\) 为奇数时另取一个跨中央的段；\(k\) 为偶数时不跨中央。每段首末位置的 \(u_i\) 均非零，因而进位可以在段首启动，在段末之后的零位置结束。这构造了合法的对称进位字 \(e\)。

令 \(s=u+9e\)。其每项在 0 至 18 之间，中央项为偶数，所以可由正整数 \(N\) 实现；式 (1) 的实际进位正是所构造的 \(e\)。式 (10) 保证 \(11\mid N\)，式 (4) 保证 \(T^2(N)=D(V)\)。充分性得证。∎

这个定理把任意长度的进位结构归约成一个小整数 \(k\)，而 \(k\) 有精确的允许范围；这里没有假设进位随机或独立。

## 3. 一个完整的二进制数位特例

若 \(B\) 是只含 0、1 的正回文，记 \(h\) 为其中 1 的个数。这里“二进制数位”只描述十进制展开中允许出现的数字，并不是改变进制。

**定理 2。**存在 \(11\) 的正倍数 \(N\) 使 \(T^2(N)=D(B)\)，当且仅当下列至少一项成立：

1. 存在 \(1\le k\le h\)，满足 \(k\equiv h\pmod2\) 且 \(h-2k\equiv0\pmod{11}\)；
2. \(B\) 的每个极大连续 1 段长度都是偶数。

在第 1 项中，最后两步的增长模式为“增位、不增位”；第 2 项给出“不增位、增位”。

第一项就是定理 1。若最后一步不增位，目标首尾和为 1，前一步不可能也不增位，因为不增位输出的首尾和至少为 2。

若最后一步增位，式 (3) 强制中间项的对称和为 \(11u_i\)，其中
\(u_{2j}=b_j,u_{2j+1}=0\)。前一步不能增位，否则中间项首位为 1，首尾和至多为 10，不能是 11。

下面是“不增位”的准确反推方程。状态 \((x,y)\) 表示低端输入进位与高端输出进位；读入当前目标对称和 \(p\)，来源当前和为 \(s\)，内侧进位为 \((x',y')\)，则

\[
x'=\lfloor(s+x)/10\rfloor,\quad
y=\lfloor(s+y')/10\rfloor,\quad
p=2s+x+y'-10(x'+y).
\tag{11}
\]

从状态 \(00\) 开始，对交替出现的“\(11b_j\)、0”使用式 (11)，得到：

- 在状态 \(00\) 遇到非零位置：先读 11 到 \(01\)，再读 0 到 \(10\)；
- 在状态 \(10\) 时，下一个非零位置必须紧邻：读 11 回到 \(00\)，再读 0 保持 \(00\)；
- 在状态 \(10\) 读入额外的 0 不可能。

最终回到边界状态 \(00\) 恰好要求 \(B\) 的每个 1 段长度为偶数。这也可在完整对称和字上从两端同时推进，中央条件不会另产生例外。

充分性有直接构造：把 \(B\) 每段中的 1 两两配对，在对应的 \(U\) 位置放置原始和块 \((5,10,5)\)，其余位置放零。块之间至少隔一个零；整个字对称，中央项为 0 或 10，因此可实现。每块的交错和 \(5-10+5=0\)，所以来源为 11 的倍数；规范化与再次反转相加给出 \(D(B)\)。∎

第一项失败的全部正整数 \(h\) 恰为

\[
\{1,2,3,5,6,7,9,10,14,18\}.
\tag{12}
\]

有限部分逐一代入即可核对；当 \(h\ge21\) 时，允许的同奇偶 \(k\) 中至少有连续的 11 个模 11 余数，必有解。式 (12) 特别给出许多零串长度任意的两步障碍。

## 4. 七对同数字：证明式 (A)

令 \(B\) 为任意恰含 7 个 1 的十进制回文，其余数位为零。它必为奇数位数，中央数位为 1。式 (A) 正是

\[
P_d=D(dB),
\]

其中 \(dB\) 表示把 \(B\) 的每个 1 换成数字 \(d\)，不产生进位。

假设 \(N_t=P_d\)。目标至少有 14 位，而 \(N_8=1067869\) 只有 7 位；\(T\) 严格递增，所以只需讨论 \(t\ge9\)。特别地，\(N_{t-2}\) 是 11 的倍数。

### 4.1 排除最后一步增位

只有 \(d=1\) 可能增位到目标。此时 \(U=P_1/11\) 的中央数位为 1；式 (3) 要求中间项的中央对称和为 11。然而中央对称和必须是偶数，矛盾。

因此最后一步总是不增位，并且完全没有进位。

### 4.2 两步都不增位时

若 \(d\in\{1,3,5,7\}\)，目标数位只含 0 和 \(d\)，不含 9。式 (11) 的常规解满足

\[
x'=y,\qquad y'=x\mathbin\oplus(p\bmod2).
\]

所以 \(x\oplus y\) 恰在读到奇数目标数位时翻转。读完整个目标的一半，遇到的非零数位恰有 7 个；最终 \(x\oplus y=1\)，但偶数长度接合要求 \(x=y\)。矛盾。

若 \(d\in\{2,4,6,8\}\)，所有目标数位都是偶数，从状态 \(00\) 出发始终停在 \(00\)。于是中间项本身回文，而且

\[
N_{t-1}=P_d/2=P_{d/2}.
\tag{13}
\]

### 4.3 增位后不增位时

定理 1 中 \(w=7d,a=3,c=d\)。对不被 3 整除的六个数字，允许的 \(k\) 为：

| \(d\) | 满足定理 1 的 \(k\) |
|---:|---:|
| 1 | 无 |
| 2 | 无 |
| 4 | 无 |
| 5 | 1 |
| 7 | 无 |
| 8 | 6 |

于是 \(d=1,7\) 的全部分支已经被排除；再用式 (13) 依次排除 \(d=2,4\)。

\(d=3,6,9\) 时目标数位和 \(14d\) 被 3 整除，直接违反式 (5)。只余 \(d=5,8\)。

### 4.4 排除 \(d=8\)

若两步都不增位，式 (13) 已归约到被排除的 \(d=4\)。

若增位后不增位，则 \(k=6\)。除中央以外恰有六个非零 \(u_i\)，所以六个进位 1 段必须各自只占一个这样的非零位置。于是 \(X=N_{t-2}\) 的对称和字只能是：

- 六个非中央非零位置为 17；
- 中央为 8；
- 其余位置为 0。

这个 \(X\) 根本不可能是任何 \(T(Y)\)。

证明如下。\(q(X)_0=17>10\)，所以 \(Y\to X\) 不能增位。对式 (11) 从外向内反推；每个非中央 17 后面都有一个零，因为 \(U\) 的非零位置只在偶数位置。边界状态只可能在

\[
00\xrightarrow{17}01\xrightarrow{0}10,\qquad
10\xrightarrow{17}00\xrightarrow{0}00
\]

之间交替；在 \(10\) 状态插入额外的零会立即失败。左侧有三个 17，因此若没有提前失败，到中央时状态必为 \(10\)。

中央目标和为 8，故 \(X\) 中央实际数位为 4。来源中央和必须为

\[
4-x+10y=4-1=3,
\]

却又必须为偶数，矛盾。故 \(d=8\) 排除。

### 4.5 排除 \(d=5\)

这里只可能增位后不增位，且 \(k=1\)。对称进位字首尾为 1、只有一个 1 段，故全为 1。于是 \(X=N_{t-2}\) 的对称和为

\[
q(X)_i=
\begin{cases}
14,&u_i=5,\\
9,&u_i=0.
\end{cases}
\tag{14}
\]

这是一个奇数长度对称字，首尾和中央均为 14，奇数位置全为 9，其他偶数位置为 9 或 14。

下一节证明：任何具有这个结构的整数，都不可能有七层前驱。但 \(t\ge9\) 时

\[
X=N_{t-2}=T^7(N_{t-9}),
\]

恰好给出了七层前驱，矛盾。这完成了式 (A) 全部九个数字、所有参数以及所有时刻的排除。∎

## 5. 七层前驱障碍及有限证书

**引理 3。**设正整数 \(X\) 的对称和字满足：

1. 长度为 \(4j+1\)；
2. 首尾和中央为 14；
3. 奇数位置均为 9，偶数位置为 9 或 14。

则不存在正整数 \(Y\) 使 \(T^7(Y)=X\)。

### 5.1 任意长字的前缀覆盖

若字长至少为 23，它的前 11 项属于固定的 32 个前缀：

\[
(14,9,x_1,9,x_2,9,x_3,9,x_4,9,x_5),
\qquad x_i\in\{9,14\}.
\tag{15}
\]

现在只保留外侧前缀，允许内部任意延续。因此获得的是实际前驱集合的超集；若这个超集已经为空，实际前驱当然不存在。

对长度 \(K\) 的目标前缀，枚举来源前缀的列和及二进制进位，并保留前 \(K-1\) 项。

不增位分支使用式 (11)，初始状态为 \(00\)。增位分支的准确规则是：

- 若首个目标和 \(p_0>10\)，不可能增位；
- 若 \(p_0\le9\)，来源首和 \(s_0=p_0+9\)；
- 若 \(p_0=10\)，来源首和 \(s_0=9\)；
- 此后若上一列来源和为 \(v\)，当前低端进位为 \(x\)、高端出进位为 \(y\)，选择高端内进位 \(y'\)，必须满足

\[
\lfloor(v+y')/10\rfloor=y.
\]

当前低端输出数位只能为

\[
b=p-v-y'+10y,\qquad 0\le b\le9.
\]

再选择低端出进位 \(x'\)，来源当前和为

\[
s=b+10x'-x,\qquad 0\le s\le18.
\tag{16}
\]

末端还检查是否存在下一进位使高端列合法，然后舍去最后一项。

这些规则直接来自式 (1)，不存在估计误差。每次都舍去一层，确保只保留已经有外侧列约束支持的前缀。对于原来至少 23 位的字，七次回溯所涉及的外层位置都不会在中央相撞，因此覆盖论证适用。

对式 (15) 应用上述有限规则，得到：

| 反推次数 | 保留前缀长度 | 不同前缀个数 |
|---:|---:|---:|
| 0 | 11 | 32 |
| 1 | 10 | 377 |
| 2 | 9 | 1,014 |
| 3 | 8 | 1,181 |
| 4 | 7 | 136 |
| 5 | 6 | 45 |
| 6 | 5 | 13 |
| 7 | 4 | 0 |

第六层的 13 个前缀全部以 \((1,12)\) 开头。

但任何 \(T(Z)\) 的对称和都不可能以 \((1,12)\) 开头：不增位时首尾和至少为 2；增位时首尾和 1 迫使最高位为 1、最低位为 0，来源首和为 10，输出次高位至多为 1，所以第二层对称和至多为 10。

这一有限表的每个条目由附录中的整数代码精确复现。证明依赖的是“所有长字均被 32 个前缀覆盖”，而不是某个长度上限的数值试验。

### 5.2 短字边界

小于 23 位时，可取长度仅为

\[
1,5,9,13,17,21.
\]

利用对称性、中央 14 和奇数位置 9，符合条件的完整字总共只有

\[
1+1+2+4+8+16=32
\]

个。对这 32 个字，附录使用完整逆像枚举，逐次保留所有可能的来源长度、进位和中央偶性，最后再按式 (1) 正向检验。它们的七层逆像也全部为空。

枚举没有删除途中出现回文的路径。因此引理适用于任意出现时刻，不是仅仅适用于首次回文。引理得证。∎

另以完整的有限状态逆像方法独立核对了所有长度。除去单字 \((14)\) 的立即无前驱情形，对其余字进行七次无条件逆像，最小化状态数依次为

\[
4,\ 10,\ 34,\ 416,\ 1052,\ 4424,\ 19831,\ 1,
\]

最后一个状态没有任何接受终点。这个检查支持同一结论；附录保留了更短的前缀证书版本。

### 5.3 界限不能随意再减少

存在 11 的倍数

\[
A=13310020608909159190
\]

满足

\[
T^8(A)=5500555500550055550055,
\]

右侧正是式 (A) 中 \(d=5,a=1,b=0,c=1\) 的目标，且第 0 至 7 步都不是回文。

其轨道为

\[
\begin{aligned}
13310020608909159190
&\to22505211589511160521\\
&\to35011323188022411043\\
&\to69022745276154722096\\
&\to138045490443409444192\\
&\to429490394787503985023\\
&\to750079700574997079947\\
&\to1500050500050005050004\\
&\to5500555500550055550055.
\end{aligned}
\]

这不是 196 的轨道。它说明：不能把上述证明误读成“任何 11 的倍数都永远到不了这些目标”，也不能把这条分支的统一八步上界擅自改成七步。196 的排除还使用了它的实际初始段。

## 6. 五对同数字的八个分支

式 (B) 对应 \(P_d=D(dB)\)，其中 \(B\) 是恰含 5 个 1 的回文。此时定理 1 给出 \(w=5d,a=2,c=d\)。

对 \(d\in\{1,2,4,5,7,8\}\)，只有 \(d=7\) 有解，且 \(k=1\)。最后一步增位在 \(d=1\) 时仍因中央和为 11 而不可能；两步都不增位的奇数字分支仍因半边有奇数个奇数位而不可能；偶数字分支仍按式 (13) 递降。加上模 3 排除 \(d=3,6,9\)，便得到式 (B) 的八个数字分支。

剩余 \(d=7\) 对应来源和字在非零位置为 16、其余位置为 9。它不满足引理 3；本轮的深入逆像搜索没有取得排除证明。

## 7. 验证范围与未完成部分

本轮已完成：

- 对位数不超过 7 的全部 10,998 个正回文 \(V\)，用独立的完整逆像方法核对定理 1，并实际构造所有允许段数对应的来源。
- 对位数不超过 19 的全部 1,534 个只含 0、1 的正回文，核对定理 2 的两个分支。
- 复现引理 3 的前缀数表及全部 32 个短字边界。
- 用 3,000 个实际整数来源检查前缀反推覆盖关系。
- 核对 196 的初始段和八步界限的具体例子。
- 对 \(d=8\)、七个非零位置的中央偶性障碍，另检验了 125 组零串参数。
- 用全长有限状态逆像方法独立核对引理 3。

这些有限交叉检查与证明中的有限证书作用不同：前者用于发现实现或转录错误；后者在已证明覆盖任意长度的前提下，完成固定有限分支的排除。

当前尚未完成的部分至少包括：

- 完整 196 猜想，即对所有可能形状的回文统一排除；
- 上一轮剩余的两对数字族 \(55\,0^{2r}\,55\)；
- 本轮五对数字族的 \(d=7\) 分支；
- 把引理 3 中的有限枚举进一步压缩成更短的纯手算证明，或将整份证明交给形式化证明器核验。

因此，本轮的结论是一个新的、全部参数无界的局部排除定理，而不是完整猜想的证明。

## 附录：自包含复核代码

下面程序仅依赖 Python 3 标准库。完整逆像枚举不会过滤途中回文。它复现前缀证书、短字边界、两个充要条件的交叉检查，以及具体轨道例子。



```python
from itertools import product
from functools import lru_cache

def digits(s):
 d=[];c=0
 for a in s:
  a+=c;d.append(a%10);c=a//10
 if c:d.append(c)
 return d

def step(s):
 d=digits(s)
 return tuple(x+y for x,y in zip(d,d[::-1]))

@lru_cache(maxsize=200000)
def inverse_all(q):
 L=len(q);ans=set()
 for grow in (False,True):
  m=L-int(grow)
  if m<1:continue
  h=(m+1)//2
  if not grow:
   states=[((),0,0)]
   for i in range(h):
    nxt=[]
    for p,x,y in states:
     for u in range(1 if i==0 else 0,19):
      xp=(u+x)//10
      for yp in (0,1):
       if (u+yp)//10==y and 2*u+x+yp-10*(xp+y)==q[i]:nxt.append((p+(u,),xp,yp))
    states=nxt
   ps=[p for p,x,y in states]
  else:
   if q[0]>10:continue
   u0=q[0]+9 if q[0]<=9 else 9
   states=[((u0,),u0//10,1)]
   for i in range(1,h):
    nxt=[]
    for p,x,y in states:
     for yp in (0,1):
      if (p[-1]+yp)//10!=y:continue
      digit=q[i]-p[-1]-yp+10*y
      if not 0<=digit<=9:continue
      for xp in (0,1):
       u=digit+10*xp-x
       if 0<=u<=18:nxt.append((p+(u,),xp,yp))
    states=nxt
   ps=[p for p,x,y in states]
  for p in ps:
   if m%2 and p[-1]%2:continue
   s=p+p[:m//2][::-1]
   d=digits(s)
   if tuple(x+y for x,y in zip(d,d[::-1]))==q:ans.add(s)
 return tuple(sorted(ans))

def depth_path(q,depth):
 if depth==0:return [q]
 for p in inverse_all(q):
  ans=depth_path(p,depth-1)
  if ans:return ans+[q]
 return None

def represent(s):
 L=len(s);a=[0]*L
 for i in range(L//2):
  a[L-1-i]=max(1 if i==0 else 0,s[i]-9)
  a[i]=s[i]-a[L-1-i]
 if L%2:a[L//2]=s[L//2]//2
 return int(''.join(map(str,a[::-1])))


from itertools import product
from functools import lru_cache

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

def initial(K):
 return {(14,)+tuple(u for b in bits for u in (9,b))+(9,)*(K%2==0) for bits in product((9,14),repeat=(K-1)//2)}


def T(n): return n+int(str(n)[::-1])
def pal(n): return str(n)==str(n)[::-1]
def D(v): return int(''.join(x*2 for x in str(v)))
def gn_options(v):
 s=str(v);c=int(s[len(s)//2]) if len(s)%2 else 0
 a=sum(x!='0' for x in s[:len(s)//2]);w=sum(map(int,s))
 ks=range(1,2*a+2,2) if c%2 else range(2,2*a+1,2)
 return [k for k in ks if (w-2*k)%11==0]

def construct_gn(v,k):
 u=[]
 for x in str(v)[::-1]:u.extend((int(x),0))
 u.pop();n=len(u);mid=n//2
 support=[i for i,d in enumerate(u) if d]
 left=[i for i in support if i<mid];e=[0]*n
 intervals=[]
 if k%2:
  r=(k-1)//2
  intervals.extend((i,i) for i in left[:r])
  start=left[r] if r<len(left) else mid
  intervals.append((start,n-1-start))
 else:
  r=k//2
  intervals.extend((i,i) for i in left[:r-1])
  intervals.append((left[r-1],left[-1]))
 for lo,hi in intervals:
  for i in range(lo,hi+1):e[i]=e[n-1-i]=1
 s=tuple(d+9*x for d,x in zip(u,e));n0=represent(s)
 assert n0%11==0 and len(str(T(n0)))==len(str(n0))+1
 assert T(T(n0))==D(v)
 return n0

def palindromes(maxlen,alphabet='0123456789'):
 for m in range(1,maxlen+1):
  for first in alphabet[1:]:
   for rest in product(alphabet,repeat=(m+1)//2-1):
    h=first+''.join(rest)
    yield int(h+h[::-1][m%2:])

@lru_cache(None)
def has_ancestor(q,k):
 return k==0 or any(has_ancestor(p,k-1) for p in inverse_all(q))

def check_certificate():
 a=initial(11);counts=[len(a)]
 for _ in range(6):
  a={p for q in a for p in inverse_prefix(q)};counts.append(len(a))
 assert all(q[:2]==(1,12) for q in a)
 a={p for q in a for p in inverse_prefix(q)};counts.append(len(a))
 assert counts==[32,377,1014,1181,136,45,13,0],counts
 short=0
 for halfsize in range(0,11,2):
  words=[()] if halfsize==0 else [(14,)+tuple(u for b in bits for u in (9,b))+(9,) for bits in product((9,14),repeat=halfsize//2-1)]
  for w in words:
   q=w+(14,)+w[::-1]
   assert not has_ancestor(q,7),q
   short+=1
 assert short==32
 print('Universal prefix certificate:',counts,'short words:',short)

def check_general():
 count=0
 for v in palindromes(7):
  q=tuple(map(int,str(D(v))));options=gn_options(v)
  actual=any(len(s)==len(q)-1 and represent(s)%11==0 for s in inverse_all(q))
  assert bool(options)==actual,(v,options,actual)
  for k in options:construct_gn(v,k)
  count+=1
 print('General growth criterion and constructions:',count,'palindromes')

# Independent tests of the two-step binary specialization, both branches.
def check_binary():
 count=0
 for v in palindromes(19,'01'):
  p=D(v);q=tuple(map(int,str(p)));h=str(v).count('1')
  a=bool(gn_options(v));b=all(len(s)%2==0 for s in str(v).split('0') if s)
  gn=any(len(s)==len(q)-1 and represent(s)%11==0 for s in inverse_all(q))
  u=p//11;raw=tuple(11*int(x) for x in str(u));ng=False
  if raw[len(raw)//2]%2==0:
   ng=any(represent(s)%11==0 for s in inverse_all(raw))
  assert (a,b)==(gn,ng),(v,a,b,gn,ng)
  count+=1
 fails=[h for h in range(1,101) if not any((h-k)%2==0 and (h-2*k)%11==0 for k in range(1,h+1))]
 assert fails==[1,2,3,5,6,7,9,10,14,18]
 print('Binary complete criterion:',count,'targets')

# Validate the prefix over-approximation against actual integer addition.
def check_prefix_soundness():
 import random
 rng=random.Random(196)
 for _ in range(3000):
  n=rng.randrange(10**25,10**29);s0=str(n);s=tuple(int(x)+int(y) for x,y in zip(s0,s0[::-1]))
  q=step(s)
  assert s[:10] in inverse_prefix(q[:11])
 print('Prefix soundness cross-check: 3000 integer sources')

def check_orbit_and_sharpness():
 n=196;first=[]
 for t in range(9):first.append(n);assert not pal(n);n=T(n)
 assert first==[196,887,1675,7436,13783,52514,94039,187088,1067869]
 n=13310020608909159190
 assert n%11==0
 for _ in range(8):assert not pal(n);n=T(n)
 assert n==5500555500550055550055 and pal(n)
 print('196 initial segment and sharp eight-step example passed')

if __name__=='__main__':
 check_certificate()
 check_general()
 check_binary()
 check_prefix_soundness()
 check_orbit_and_sharpness()
 print('All checks passed. This is not a proof of the full 196 conjecture.')

```
