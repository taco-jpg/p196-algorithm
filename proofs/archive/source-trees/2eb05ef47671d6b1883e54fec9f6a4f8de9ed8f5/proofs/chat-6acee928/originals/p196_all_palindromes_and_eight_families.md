# P196 的继续推进：所有回文的两步判据与八个无限排除族

本文得到两个严格的局部结果：一是对所有十进制回文给出“存在两步前驱且中间项非回文”的充要条件；二是证明 196 的轨道永不出现

\[
11d\bigl(10^{2r+2}+1\bigr),\qquad
r\ge0,\quad d\in\{1,2,3,4,6,7,8,9\}.
\]

第二个结论针对轨道中的任何时刻，不只是首次回文时刻。该族的十进制形式是两端各两个相同数字、中间偶数个零，例如 \(4444,440044,44000044\)。\(d=5\) 的情形仍未排除。

这些结果没有证明完整的 196 猜想，也不主张文献首创。下面的无限范围结论来自数位推导；末尾程序只作独立交叉检查，不把有限计算当成无限证明。

## 1. 定义及已证明的进位工具

定义

\[
T(N)=N+\operatorname{rev}(N),\qquad N>0.
\]

反转忽略前导零。记 \(\mathcal P\) 为正整数十进制回文集合。

若 \(N\) 有 \(n\) 位，按从低到高记数位 \(a_i\)，定义对称和

\[
s_i=a_i+a_{n-1-i}.
\]

它们满足 \(0\le s_i\le18\)、\(s_i=s_{n-1-i}\)、\(s_0>0\)，且奇数长度时中间项为偶数。这些条件也是一个对称和字可以由正整数实现的充分条件。

计算 \(T(N)\) 的进位与输出数位满足

\[
c_0=0,\qquad
c_{i+1}=\left\lfloor\frac{s_i+c_i}{10}\right\rfloor,
\qquad b_i=s_i+c_i-10c_{i+1}.
\tag{1}
\]

每个进位是 \(0\) 或 \(1\)。\(c_n=1\) 时再添最高位 \(b_n=1\)，称这一步“增位”。

**工具一：一步回文判据。**

\[
T(N)\in\mathcal P
\iff
\bigl(\forall i:s_i\le9\bigr)
\ \text{或}\
\bigl(\forall i:s_i\in\{0,11\}\bigr).
\tag{2}
\]

第一种情形没有任何进位；第二种情形增位，且 \(T(N)=11U\)，其中 \(U\) 是只含 \(0,1\) 的回文。

证明的核心是从首尾向中间比较。若不增位，\(c_n=0\) 先迫使 \(c_1=0\)，首尾相等再迫使 \(c_{n-1}=0\)；随后每一层的等式给出 \(10c_{i+1}+c_{n-1-i}=0\)，所有进位均为零。若增位，首尾输出均为 \(1\)，故 \(s_0=11\)。逐层比较得到 \(s_i=10c_{i+1}+c_{n-i}\)。两个进位不相等会分别导致“列和 1 产生进位”或“列和 10 不产生进位”的矛盾，所以 \(s_i\) 为 \(0\) 或 \(11\)。逆命题直接逐列验证。

这一判据也见 Ando 的公开草稿《Carry Asymmetry, Palindrome Characterization, and Conditional Non-Convergence in the Reverse-and-Add Process》（2026）第 3 节；本文不采用该稿中的条件性非收敛结论。来源：https://github.com/nkc-daiki/196-carry-asymmetry 。

**工具二：增位后的无进位相加。**若 \(M=T(N)\) 增位，而 \(T(M)\) 没有任何进位，则上一步的进位满足

\[
c_{i+1}=c_{n-i}\qquad(0\le i<n).
\tag{3}
\]

因此

\[
u_i=s_i-9c_{i+1}
\tag{4}
\]

是合法的对称数位，组成一个 \(n\) 位回文 \(U\)，并有

\[
T(M)=11U.
\tag{5}
\]

简述进位对称性的证明。第二次无进位意味着 \(b_i+b_{n-i}\le9\)。由最外层得 \(c_1=c_n=1\)。令 \(\delta_i=c_{i+1}-c_{n-i}\)，首尾的 \(\delta_i\) 都为零。若 \(j\) 是首个非零位置，\(\delta_j=-1\) 会迫使 \(b_j=9\)、\(b_{n-j}\ge1\)，产生矛盾；\(\delta_j=1\) 则迫使 \(b_{n-j-1}=9\)、\(b_{j+1}=0\)，继而 \(\delta_{j+1}=1\)。后一个推导可以持续到边界，也产生矛盾。具体地，正缺陷要求 \(s_j=9,c_j=1,c_{n-j-1}=0\)；由 \(b_{j+1}=0,c_{j+1}=1\) 得 \(s_{j+1}=9,c_{j+2}=1\)。负缺陷的计算则利用首个缺陷之前的 \(c_j=c_{n-j+1}\)。因此式 (3) 成立。

式 (4) 的数位范围由进位阈值保证，对称性来自式 (3)。令 \(u_{-1}=u_n=0\)，代入式 (1) 得

\[
b_i+b_{n-i}=u_{i-1}+u_i.
\tag{6}
\]

这就是式 (5)。只要前一步增位且进位对称，恒等式 (5) 本身就成立，不要求下一次加法没有进位。

**辅助事实。**如果 \(U\) 与 \(11U\) 都是回文，则乘以 \(11\) 时没有进位。

这是因为原始系数列

\[
(u_0,u_0+u_1,\ldots,u_{n-2}+u_{n-1},u_{n-1})
\]

对称，取值在 \(0\) 至 \(18\) 之间，奇数长度时中央系数为偶数。因此它可作为某个正整数的对称和字。最外项不超过 \(9\)，式 (2) 中的第二种情况不可能，故只能无进位。特别地，所有相邻 \(u_i\) 之和均不超过 \(9\)。

## 2. 覆盖所有回文的两步充要条件

这里精确判定的是

\[
\exists N>0:\quad T(N)\notin\mathcal P,\qquad T^2(N)=P.
\tag{7}
\]

不要求 \(N\) 本身非回文。因此“首次”若用于这一表述，指从初始数之后开始计数的正整数时刻。196 的首次回文若存在且发生在第 2 步以后，必满足式 (7)。

定义例外集

\[
\mathcal E=
\{22,44,66,88,242\}
\ \cup\
\{\underbrace{22\,00\cdots00\,22}_{\text{中间 }2r\text{ 个零}}:r\ge0\}.
\tag{8}
\]

特别地，后一族包括 \(2222,220022,22000022,\ldots\)。

**完整判据。**对任意正整数回文 \(P\)，式 (7) 成立，当且仅当以下两项至少有一项成立：

- **条件 A：**\(11\mid P\)，\(P/11\) 是回文，且 \(P\notin\mathcal E\)。
- **条件 B：**\(P\) 含有至少一个奇数数位，且通过下面的四状态判定。

### 四状态判定

把 \(P\) 从两端向中间折叠，只读一侧的 \(\lfloor L/2\rfloor\) 个数位，其中 \(L\) 是位数。状态为两个二进制进位 \((x,y)\)，初始状态 \(00\)。表中的大括号表示保留所有可能状态；空集表示该路径失败。

| 当前状态 | 读 0 | 读 2、4、6、8 | 读 1、3、5、7 | 读 9 |
|---|---|---|---|---|
| 00 | 00 | 00 | 01 | 01 |
| 01 | 10 | 10 | 11 | \(\{11,01\}\) |
| 10 | \(\varnothing\) | 01 | 00 | \(\{00,10\}\) |
| 11 | 11 | 11 | 10 | 10 |

当 \(L\ge2\) 时，第一位不能是 \(1\)。读完后：

- 若 \(L\) 为偶数，有一条路径终止于 \(00\) 或 \(11\) 即接受。
- 若 \(L\) 为奇数，中间数位 \(m\) 必须为偶数，且有一条路径满足 \(x\equiv m/2\pmod2\)。\(y\) 不再另受限制。

一位数的接受值是 \(4,8\)，不过它们没有奇数数位，不满足条件 B。

### 2.1 增位后不增位的分支

设 \(N\to M\to P\)，第一步增位、第二步不增位。由于第二步输出回文，由式 (2) 知它没有任何进位。工具二遂给出 \(P=11U\)，\(U\) 回文。

反过来，设 \(P=11U\) 且二者回文。我们构造一个对称的二进制字 \(e_i\)，并令

\[
s_i=u_i+9e_i.
\tag{9}
\]

构造使得它恰好产生进位 \(c_{i+1}=e_i\)，且 \(e_0=e_{n-1}=1\)。

若 \(n\) 为偶数，或 \(n\) 为奇数且中央 \(u_i\) 为奇数，先取所有 \(e_i=1\)。第一列因 \(u_0>0\) 产生进位，其后每列都会保持进位；奇数长度时中央 \(s_i=u_i+9\) 为偶数，满足可实现性。由式 (5)，输出两步后恰为 \(11U\)。其中间项是回文，当且仅当全部 \(s_i=11\)，即全部 \(u_i=2\)。若 \(n\ge4\) 为偶数，可改用只在首尾取 1 的 \(e_i\)，使内部出现 \(s_i=2\)，中间项就不再回文。只剩 \(n=2,U=22,P=242\) 无法这样处理。

若 \(n\ge3\) 为奇数、中央 \(u_i\) 为偶数，取首尾 \(e_i=1\)，其余为零。辅助事实保证 \(u_1\le8\)，所以最初的进位在第二列消失，直到最高列再次产生进位。这确为实际进位字，中央 \(s_i\) 也为偶数。中间项回文当且仅当 \(u_0=2\)、所有内部 \(u_i=0\)，即

\[
U=2\,0^{2r+1}\,2,\qquad P=22\,0^{2r}\,22.
\]

若 \(n=1\)，可行的增位来源要求原始和 \(s_0=u_0+9\) 为偶数，即 \(u_0\) 为奇数。被排除的恰为 \(P=22,44,66,88\)。

以上不仅给出例外，还证明例外确实不可用：\(U=22\) 时首尾进位都为 1，强制 \(s=(11,11)\)，中间项回文；\(U=2\,0^{2r+1}\,2\) 时，中央可实现性强制中央进位为零。零数位区域中进位只能由 1 降为 0，不能由 0 升为 1；结合进位对称性，所有内部进位均为零。因此 \(s=(11,0,\ldots,0,11)\)，中间项仍必回文。单数位偶数 \(U\) 则直接违反 \(s_0\) 的偶性。

所以，存在“第一步增位、第二步不增位、中间项非回文”的来源，恰好等价于条件 A。

### 2.2 两步都不增位的分支

第二步无进位，故 \(P\) 的数位 \(p_i\) 就是 \(M\) 的对称数位和。

从外向内处理原数 \(N\)。在某层保存 \(x=c_i,y=c_{n-i}\)，读入原始对称和 \(s\)，设下一层进位为 \(x',y'\)。准确的列条件是

\[
x'=\lfloor(s+x)/10\rfloor,\qquad
y=\lfloor(s+y')/10\rfloor,
\]

\[
p=2s+x+y'-10(x'+y).
\tag{10}
\]

除 \(s=9\) 的进位临界情况外，必有

\[
x'=y,\qquad y'=x\mathbin\oplus(p\bmod2),
\qquad s=10y+\frac{p-x-y'}2.
\tag{11}
\]

在 \(0\le p\le9\) 内，式 (11) 只有状态 \(10\) 读入 \(0\) 会产生非法的 \(s=-1\)。当 \(s=9,x\ne y\) 时，另有读入 \(p=9\) 并停留原状态的路径。所有情形恰为上面的四状态表。第一位 \(p=1\) 会令外层原始和为零，故必须排除。

中央条件也准确：偶数长度要求两条进位接合，即 \(x=y\)；奇数长度有 \(p=2b\)、\(b=2a+x-10y\)，所以必须且只需 \(p\) 为偶数及 \(x\equiv p/2\pmod2\)。

最后确定中间项是否非回文。如果 \(P\) 有奇数数位，\(M\) 不可能回文，否则其所有对称和均为偶数。反过来，若 \(P\) 的所有数位为偶数，从状态 \(00\) 开始读偶数始终停在 \(00\)，中央也只能无进位；原始和全部不超过 \(9\)，由式 (2) 知 \(M\) 回文。因此中间项非回文恰好要求至少一个奇数数位，条件 B 得证。

### 2.3 最后一步增位的分支

这时 \(P\) 首位为 \(1\)，式 (2) 给出 \(P=11U\)，其中 \(U\) 是只含 \(0,1\) 的回文。这样的 \(P\) 不属于 \(\mathcal E\)，所以已被条件 A 覆盖。条件 A 还提供一条最后一步不增位的替代来源。

三个分支穷尽所有情况，完整判据得证。

**直接推论。**若回文 \(P\) 的数位全部属于 \(\{0,2,4,6,8\}\)，则式 (7) 成立当且仅当

\[
11\mid P,\qquad P/11\in\mathcal P,\qquad P\notin\mathcal E.
\]

例如 \(220022\) 必然更早出现回文，而 \(22022\) 可以两步首次到达：

\[
2099\to12001\to22022.
\]

## 3. 196 轨道的八个无限排除族

令 \(N_t=T^t(196)\)，并定义

\[
R_r=10^{2r+2}+1,\qquad P_{d,r}=11dR_r,\qquad r\ge0,\quad1\le d\le9.
\]

**定理。**对所有 \(t\ge0,r\ge0\) 及

\[
d\in\{1,2,3,4,6,7,8,9\},
\]

都有 \(N_t\ne P_{d,r}\)。

### 3.1 两个整除不变量

模 \(3\) 下，反转不改变余数，故

\[
N_t\equiv2^t\cdot196\not\equiv0\pmod3.
\tag{12}
\]

又因为 \(N_3=7436=11\cdot676\)，而任意 \(L\) 位数满足

\[
\operatorname{rev}(N)\equiv(-1)^{L-1}N\pmod{11},
\]

所以

\[
11\mid N_t\qquad(t\ge3).
\tag{13}
\]

\(N_0,\ldots,N_4\) 为 \(196,887,1675,7436,13783\)，均不在任何 \(P_{d,r}\) 族中。以下只需考虑 \(t\ge5\)，于是 \(11\mid N_{t-2}\)。

### 3.2 最后一步不增位、前一步增位时的精确形式

设 \(P_{d,r}=T(M)\)，\(M=T(X)\)，其中 \(X\to M\) 增位而 \(M\to P_{d,r}\) 不增位。

工具二的商是

\[
U=P_{d,r}/11=dR_r=d\,0^{2r+1}\,d.
\]

其位数为奇数，中间数位为零。由式 (4)，中央原始和为 \(9c\)，但必须是偶数，所以中央进位为零。内部所有 \(u_i=0\) 的列中，输出进位为 1 必须以前一列已有进位为条件。结合进位字对称性，所有内部进位均为零。因此 \(X\) 的对称和字只能是

\[
(d+9,0^{2r+1},d+9).
\tag{14}
\]

\(X\) 的内部数位全为零，首尾和为 \(d+9\)。由于其位数为奇数，

\[
X\equiv d+9\pmod{11}.
\tag{15}
\]

结合式 (13)，只有 \(d=2\) 可能。在这个例外中

\[
M=11R_r=P_{1,r},
\tag{16}
\]

而且 \(M\) 本身回文。以上论证不假设此前从未出现过回文。

### 3.3 排除 \(d=1\)

最后一步不增位时，\(M\) 的首尾和为 1。若 \(X\to M\) 也不增位，首尾和至少为 2，矛盾；若增位，式 (15) 给出 \(X\equiv10\pmod{11}\)，也矛盾。

还需处理最后一步增位。由一步判据，\(M\) 的对称和字必须为

\[
(11,0^{2r+1},11).
\tag{17}
\]

\(M=T(X)\) 不能增位，否则它的首位为 1，首尾和至多为 10。因此 \(X\to M\) 不增位。最外层给出原始和 \(s_0=5\)、低端进位 \(c_1=0\)、高端内侧进位 \(c_{n-1}=1\)。

当 \(r\ge1\) 时，\(M\) 至少有五位，并且所有内部数位均为零。下一层两端零数位迫使

\[
s_1=10,\qquad c_2=1,\qquad c_{n-2}=0.
\]

再下一层，低端数位为零要求 \(s_2=9\) 且产生进位，高端数位为零却要求 \(s_2=0\)，矛盾。五位时两个位置在中央相遇，进位要求直接相互矛盾，结论相同。

当 \(r=0\) 时目标为 \(1111\)，而轨道已在第三步达到 \(7436>1111\)。由于 \(T(N)>N\)，它以后也不可能出现。故全部 \(P_{1,r}\) 被排除。

### 3.4 排除 \(d=2,4,8\)

这些目标首位不为 1，故最后一步不增位。若前一步增位，式 (15) 排除 \(d=4,8\)；\(d=2\) 则由式 (16) 必须先出现已经排除的 \(P_{1,r}\)。

若两步都不增位，因为目标的每个数位都是偶数，第 2.2 节证明中间项 \(M\) 必须回文。因此

\[
M=P_{d,r}/2=P_{d/2,r}.
\]

依次利用 \(P_{1,r}\) 不出现，排除 \(P_{2,r}\)；再排除 \(P_{4,r}\)；最后排除 \(P_{8,r}\)。这里的除以 2 确实沿原轨道退了一步，与此前未经证明的除以 11 递降有本质区别。

### 3.5 排除 \(d=3,6,9\)

它们的目标数位和为 \(4d\)，均被 3 整除，违反式 (12)。

### 3.6 排除 \(d=7\)：一个不能有前驱的外层结构

最后一步不能增位。前一步增位也已被式 (15) 排除，所以最后两步都不增位。

设 \(X=N_{t-2}\)。从目标最外两位 \(7,7\) 解列进位方程，得到 \(X\) 的最外两层对称和为

\[
(3,13).
\tag{18}
\]

具体地，第一层是 \(7=2\cdot3+1\)，第二层有相反方向的边界进位，故为 \(7=2\cdot13-20+1\)。

因为 \(X=T(Y)\)，考虑这一步是否增位。

若增位，\(X\) 首位为 1，而首尾和为 3，故末位为 2，\(Y\) 的外层原始和为 12。\(X\) 的次高位至多为 3，次低位至多为 9，所以第二层对称和至多为 12，不能等于 13。

若不增位，由 \(X\) 的外层和为 3 得 \(Y\) 的外层原始和为 1，低端内侧进位为 0，高端内侧进位为 1。再由第二层和为 13 解方程，\(Y\) 的第二层原始和只能为 16。因此 \(Y\) 的对称和以

\[
(1,16)
\tag{19}
\]

开头。

但任何 \(T(Z)\) 都不可能具有式 (19) 的开头。若 \(Z\to Y\) 不增位，外层和至少为 2；若增位，外层和为 1 强制首位 1、末位 0，\(Z\) 的外层原始和为 10。于是 \(Y\) 的次高位至多为 1，次低位至多为 9，第二层和至多为 10，也不可能为 16。

这与 \(Y=N_{t-3}=T(N_{t-4})\) 矛盾。因此全部 \(P_{7,r}\) 也被排除。八个数字分支的证明完成。

## 4. 剩下的 \(d=5\) 与实际障碍

对 \(P_{5,r}\)，模 11 已排除“增位后不增位”的最后两步，所以只剩两步均不增位的分支。准确的最后一个前驱为

\[
N_{t-1}=33\,0^{2r}\,22.
\tag{20}
\]

前两个步骤的对称和字则为

\[
(2,12,9^{2r},12,2).
\tag{21}
\]

继续向前推一层会出现可行的外层结构 \((1,6)\)，不会产生 \(d=7\) 分支中的 \((1,16)\) 矛盾。模 9 还给出必要的时刻条件 \(t\equiv3\pmod6\)，但没有矛盾。

不能仅靠已知模 99 循环排除此分支。以下轨道的初值模 99 为 11，与 \(N_3=7436\) 相同，其后余数依次为 \(22,44,88,77,55,11\)，并在第六步首次得到 \(P_{5,15}\)：

\[
\begin{aligned}
71647625487907287180977453773517
&\to143185360965815465451955906448134\\
&\to575029970524970029970524970029475\\
&\to1149950049950049950049950049950050\\
&\to1650549450549450549450549450549461\\
&\to3300000000000000000000000000000022\\
&\to5500000000000000000000000000000055.
\end{aligned}
\]

最后一项等于 \(55(10^{32}+1)\)。这不是 196 的轨道，而是说明“同样的模 99 条件”本身不足以排除剩余目标。

对 \(d=5\) 的无限族，还进行了排除途中回文的逆像语言搜索。到第 10 层逆像仍非空，最小化自动机有 219,139 个状态；下一次构造达到所设资源上限，未获得空语言证书。这里不能据此断言逆像深度无界，更不能断言 196 将达到这一族。

同样，排除八个无限族并不等于排除所有回文。其余任意形状的回文、以及 \(P_{5,r}\)，仍需与 196 的整条轨道建立更强的排斥关系。这是当前尚未完成的部分。

## 5. 独立检查及可复核程序

本轮已完成的检查包括：

- 对位数 1 至 9 的全部 109,998 个正回文，分别用独立的原始数位逆像搜索核对条件 A 和条件 B。条件 A 接受 4,260 个目标，条件 B 接受 25,496 个，交集为 1,732 个，共接受 28,024 个。
- 对每个接受目标，实际构造整数前驱，检查中间项非回文、增长模式正确、第二次输出恰为目标。
- 对全部 31,248 个不超过 12 位的全偶数位回文，另行核对其简化判据，接受 2,852 个。
- 对 \(0\le r\le30\) 和全部九个 \(d\)，核对族 \(P_{d,r}\) 的中间项非回文的精确两步逆像形状。
- 枚举长度不超过 7 的全部 75,447 个可实现对称和字，检查外层和为 1 时下一层至多为 10。
- 检查 196 的前 1,000 步，以防族表达式或转录有误；另逐步核对上述六步反例。

下面代码自包含，只依赖 Python 3 标准库。它复现主要交叉检查；全偶数位至 12 位的独立扩展检查已单独执行。将代码保存为 `p196_verify.py` 后运行即可。无限范围的证明在前文，不依赖这些检查的上限。

```python
# Python 3; standard library only.
# This verifies the stated finite cross-checks, not the complete 196 conjecture.
from itertools import product
import re

def digits(s):
 d=[];c=0
 for a in s:
  a+=c;d.append(a%10);c=a//10
 if c:d.append(c)
 return d

def step(s):
 d=digits(s)
 return tuple(x+y for x,y in zip(d,d[::-1]))

def inverse(q):
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
   if tuple(x+y for x,y in zip(d,d[::-1]))==q and d!=d[::-1]:ans.add(s)
 return tuple(sorted(ans))

def represent(s):
 L=len(s);a=[0]*L
 for i in range(L//2):
  a[L-1-i]=max(1 if i==0 else 0,s[i]-9)
  a[i]=s[i]-a[L-1-i]
 if L%2:a[L//2]=s[L//2]//2
 return int(''.join(map(str,a[::-1])))

from itertools import product
import re

def T(n):return n+int(str(n)[::-1])
def pal(n):return str(n)==str(n)[::-1]
def exception(p):
 return p in (22,44,66,88,242) or re.fullmatch(r'22(?:00)*22',str(p)) is not None

def growth_condition(p):return p%11==0 and pal(p//11) and not exception(p)

def nongrowth_source(p):
 digits=tuple(map(int,str(p)))
 L=len(digits)
 states={(0,0):()}
 for i,d in enumerate(digits[:L//2]):
  nxt={}
  for (x,y),word in states.items():
   xx=y;yy=x^(d%2)
   u=10*y+(d-x-yy)//2
   if 0<=u<=18 and (i>0 or u>0):
    assert (u+x)//10==xx and (u+yy)//10==y
    nxt[(xx,yy)]=word+(u,)
   if d==9 and x!=y:
    nxt[(x,y)]=word+(9,)
  states=nxt
 for (x,y),word in states.items():
  if L%2==0:
   if x==y:return represent(word+word[::-1])
  else:
   d=digits[L//2]
   if d%2==0 and x==(d//2)%2:
    u=d//2-x+10*y
    if L>1 or u>0:return represent(word+(u,)+word[::-1])
 return None

def nongrowth_condition(p):
 return any(int(d)%2 for d in str(p)) and nongrowth_source(p) is not None

def growth_source(p):
 u=tuple(map(int,str(p//11)[::-1]));n=len(u)
 if n%2==0 or u[n//2]%2:
  c=[1]*n
  if all(d==2 for d in u):
   assert n>=4
   c=[1]+[0]*(n-2)+[1]
 else:
  assert n>=3
  c=[1]+[0]*(n-2)+[1]
 s=tuple(d+9*e for d,e in zip(u,c))
 return represent(s)

def pals(max_len):
 for L in range(1,max_len+1):
  for d in '123456789':
   for rest in product('0123456789',repeat=(L+1)//2-1):
    h=d+''.join(rest)
    yield int(h+h[::-1][L%2:])

if __name__=='__main__':
 count=0;g_count=0;ng_count=0;both_count=0
 for p in pals(9):
  inv=inverse(tuple(map(int,str(p)[::-1])))
  actual_g=any(len(s)==len(str(p))-1 for s in inv)
  actual_ng=any(len(s)==len(str(p)) for s in inv)
  g=growth_condition(p);ng=nongrowth_condition(p)
  assert g==actual_g,('G',p,p//11,g,inv)
  assert ng==actual_ng,('NG',p,ng,inv)
  if g:
   n=growth_source(p);m=T(n)
   assert len(str(m))==len(str(n))+1 and not pal(m) and T(m)==p,(p,n,m)
  if ng:
   n=nongrowth_source(p);m=T(n)
   assert len(str(m))==len(str(n)) and not pal(m) and T(m)==p,(p,n,m)
  g_count+=g;ng_count+=ng;both_count+=(g and ng);count+=1
 print('Targets',count,'growth branch',g_count,'nongrowth branch',ng_count,'overlap',both_count,'union',g_count+ng_count-both_count)
 for p in [11,22,121,242,303,3113,3223,4444,22022,220022,2442,545,9999,99999,11111111011111111]:
  print(p,'growth',growth_condition(p),'nongrowth',nongrowth_condition(p))
 print('All targets, both branches, and constructive sources passed.')

 # Verify the exact two-step predecessor shapes of the infinite family
 # on a finite range. The text gives a proof for all r.
 for r in range(31):
  for d in range(1,10):
   p=11*d*(10**(2*r+2)+1)
   actual=set(inverse(tuple(map(int,str(p)[::-1]))))
   expected=set()
   if d!=2:expected.add((d+9,)+(0,)*(2*r+1)+(d+9,))
   if d in (3,5,7,9):
    a=(d-1)//2
    expected.add((a,a+10)+(9,)*(2*r)+(a+10,a))
   assert actual==expected,(d,r,actual,expected)
 print('Family predecessor shapes checked for all 9 digits and 0 <= r <= 30.')

 # Enumerate all feasible pair-sum words through length 7 and check
 # the universal prefix obstruction (1, 16) used in the proof.
 checked=0
 for L in range(1,8):
  h=L//2
  halves=[()] if h==0 else (
   (a,)+tail for a in range(1,19) for tail in product(range(19),repeat=h-1))
  for half in halves:
   centers=[None] if L%2==0 else range(2 if h==0 else 0,19,2)
   for center in centers:
    s=half+(() if center is None else (center,))+half[::-1]
    q=step(s)
    if len(q)>=2 and q[0]==1:assert q[1]<=10,(s,q)
    checked+=1
 assert checked==75447,checked
 print('Universal prefix obstruction cross-check:',checked,'pair-sum words.')

 # Check the actual 196 orbit over a modest finite range as a guard
 # against a transcription error. This is not the infinite proof.
 n=196
 excluded=set((1,2,3,4,6,7,8,9))
 for t in range(1,1001):
  n=T(n)
  if t>=3:assert n%11==0
  assert n%3!=0
  s=str(n)
  match=re.fullmatch(r'([1-9])\1(?:00)*\1\1',s)
  assert match is None or int(match.group(1)) not in excluded,(t,n)
 print('196 orbit cross-check: 1000 steps.')

 # A remaining d=5 target is compatible with the same mod-99 cycle.
 n=71647625487907287180977453773517
 assert n%99==11
 for t in range(6):
  assert not pal(n)
  assert n%99==(11*pow(2,t,9))%99
  n=T(n)
 assert n==55*(10**32+1) and pal(n) and n%99==11
 print('Six-step d=5 example verified:',n)
 print('All checks passed. These results do not prove the complete 196 conjecture.')

```
