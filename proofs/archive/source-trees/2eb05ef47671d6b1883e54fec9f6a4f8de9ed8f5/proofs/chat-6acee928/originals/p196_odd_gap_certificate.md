# 196 猜想的一项计算机辅助局部证明

日期：2026-10-14。

**结论范围。** 本文没有证明完整的 196 猜想。本文证明：若从 196 出发的十进制“倒序相加”轨道最终出现回文，则其**第一个回文**不可能属于

\[
P_r=\overline{1111\,0^{2r+1}\,1111}
    =1111(10^{2r+5}+1),\qquad r\ge0.
\]

横线表示十进制数字串，字符串中的指数表示重复次数。证明对所有非负整数 r 同时成立。关键的逆像语言消元由有限自动机精确完成，是一项可复核的计算机辅助证明；它不是把有限长度的实验外推到无限长度。文末提供完整的 Python 3 标准库程序和本轮运行输出。本文不主张相关一阶判据或这一局部排除的文献首创性。

## 1. 数位对之和是一个精确状态

令

\[
T(N)=N+\operatorname{rev}(N),\quad N_0=196,\quad N_{t+1}=T(N_t).
\]

对 L 位正整数 N，按低位到高位记数字为 a_0,...,a_{L-1}，定义

\[
s_i=a_i+a_{L-1-i}.
\]

可行的 s 是回文词，字母属于 {0,...,18}，首字母非零；若长度为奇数，则中央字母必须为偶数。反过来，每个满足这些条件的词都能由某个正整数实现。

令 c_0=0，逐列计算

\[
c_{i+1}=\left\lfloor\frac{s_i+c_i}{10}\right\rfloor,
\qquad b_i=s_i+c_i-10c_{i+1}.
\]

若 c_L=1，在输出数字串高端添加数字 1。设这个输出串为 d，则

\[
F(s)_i=d_i+d_{|d|-1-i}
\]

正是 T(N) 的数位对和。因此，s 的演化完全由 F 决定，无须记住同一数位对怎样分拆成两个数字。

## 2. 单步回文判据

\[
T(N)\text{ 是回文}
\quad\Longleftrightarrow\quad
\bigl(\forall i,\ s_i\le9\bigr)
\ \lor\
\bigl(\forall i,\ s_i\in\{0,11\}\bigr).
\tag{1}
\]

第一种情况没有增加位数；第二种情况增加一位，且 s_0=11。

证明要点如下。若输出不增位，回文的最外两列给出 c_{L-1}=10c_1，因此二者均为零。向内归纳得到所有进位均为零。

若输出增位，最高位为 1，回文迫使最低位也为 1。由最外列可得 s_0=11、c_1=c_L=1。假设上一层 s_{i-1}=11u，c_i=c_{L-i+1}=u，其中 u∈{0,1}。输出回文等式 b_i=b_{L-i} 给出

\[
s_i=10c_{i+1}+c_{L-i}.
\]

结合镜像列的进位规则，c_{i+1} 与 c_{L-i} 不可能不同：两种不同的选择分别要求数位和 1 产生进位或数位和 10 不产生进位。于是 s_i 只能为 0 或 11。归纳完成必要性。充分性直接代入递推；写 s_i=11u_i，并令 u_{-1}=u_L=0，则输出数字为 u_{i-1}+u_i，自然对称。

记“下一步不是回文”的状态集合为

\[
\mathcal H=\{s:\exists i\ s_i\ge10\}\cap
\{s:\exists j\ s_j\notin\{0,11\}\}.
\]

## 3. 目标回文只有两个前驱类型

若 T(N)=P_r，则由 (1) 可知，N 的数位对和必为以下两者之一：

\[
A_r=(1,1,1,1,0^{2r+1},1,1,1,1),
\]

\[
B_r=(11,0,11,0^{2r+2},11,0,11).
\]

A_r 对应末步不增位。B_r 对应末步增位，可由 u_{i-1}+u_i 的递推唯一恢复。

令

\[
\mathcal A_0=\{A_r:r\ge0\},\qquad
\mathcal B_0=\{B_r:r\ge0\},
\]

并递推

\[
\mathcal A_{k+1}=\mathcal H\cap F^{-1}(\mathcal A_k),
\qquad
\mathcal B_{k+1}=\mathcal H\cap F^{-1}(\mathcal B_k).
\tag{2}
\]

这里与 H 取交集至关重要：它排除了在目标回文之前已经出现回文的历史。

计算机辅助部分的两个精确结论是

\[
\boxed{\mathcal A_7=\varnothing,\qquad\mathcal B_3=\varnothing.}
\tag{3}
\]

因此，任意正整数轨道若以某个 P_r 为第一个回文，则最后一步不增位时最多用 7 步；最后一步增位时最多用 3 步。

## 4. 为什么 (3) 覆盖任意位数

一个可行的对称词只须编码从外到内的前半部分。若长度为偶数，以 E 结束；若长度为奇数、中央数位和为 2j，以 O_j 结束。非中央字母为 0,...,18。首个数位对和必须大于零。

在这个编码下，初始语言分别为

\[
\mathcal A_0:\quad 1,1,1,1,\underbrace{0,\ldots,0}_{r\text{ 个}},O_0,
\]

\[
\mathcal B_0:\quad 11,0,11,\underbrace{0,\ldots,0}_{r+1\text{ 个}},E.
\]

任意长的零串由状态的自循环表示，而不是设置长度上限。

现给出 F 的精确有限状态转移。字母 u 表示当前输入数位对和；低端进位记 x，高端向外进位记 y，均属于 {0,1}。另存上一列字母 p，以及目标语言自动机当前状态 q。

**不增位分支。** 从 x=y=0 开始。任选 y'∈{0,1}，要求

\[
\left\lfloor\frac{u+y'}{10}\right\rfloor=y.
\]

令

\[
x'=\left\lfloor\frac{u+x}{10}\right\rfloor,
\qquad v=2u+x+y'-10(x'+y).
\tag{4}
\]

向目标自动机输入字母 v，更新进位为 (x',y')。输入 E 时要求 x=y，并向目标输入 E。输入 O_j 时令 u=2j，要求 floor((u+x)/10)=y，并向目标输入 O_b，其中 b=(u+x) mod 10。

**增位分支。** 第一个字母 u≥9，向目标输入 u mod 10+1，置 x=floor(u/10)、y=1、p=u。后续读到 u，任选 y'∈{0,1}，要求

\[
\left\lfloor\frac{p+y'}{10}\right\rfloor=y.
\]

令

\[
x'=\left\lfloor\frac{u+x}{10}\right\rfloor,
\quad
v=((u+x)\bmod10)+((p+y')\bmod10).
\tag{5}
\]

向目标输入 v，更新为 (x',y',p'=u)。

输入 E 时，要求 floor((p+x)/10)=y，向目标输入 O_b，其中 b=(p+x) mod 10。输入 O_j 时，令 u=2j、x'=floor((u+x)/10)，要求 floor((p+x')/10)=y，先向目标输入 (u+x) mod 10+(p+x') mod 10，再输入 E。只有中央数位、没有外层数位对的情形，在程序中单独处理。

在两种分支中都记录两项布尔标志：是否已经读到 ≥10 的字母，是否已经读到不属于 {0,11} 的字母。接受时要求两项都成立，正好实现与 H 的交集。

以上状态量均为有限集合。与任意有限自动机相乘、确定化并最小化，就精确计算了 (2) 的下一层语言。这是对所有有限词的运算，不是对有限位数的枚举。

本轮完成的状态数如下，包括拒绝状态：

| 逆推层数 k | A_k 的最小确定自动机状态数 | B_k 的最小确定自动机状态数 |
|---:|---:|---:|
| 0 | 6 | 6 |
| 1 | 9 | 6 |
| 2 | 17 | 9 |
| 3 | 43 | 1，仅拒绝状态 |
| 4 | 122 | 已为空 |
| 5 | 155 | 已为空 |
| 6 | 637 | 已为空 |
| 7 | 1，仅拒绝状态 | 已为空 |

状态数本身不是证明；证明的可复核对象是式 (4)、(5)、中央接受条件以及文末实际执行全部转移的程序。

还有一个便于人工检查的末端证据：A_6 中每个词的前两个字母均为 (1,16)。这个包含关系由有限状态图完整验证。这样的词不可能是 F 的输出：

- 不增位时，输出最外数位对和至少为 2，不可能为 1。
- 增位且最外数位对和为 1 时，输入最外数位对和必为 10。输出第二高位至多为 1，第二低位至多为 9，所以第二个数位对和至多为 10，不可能为 16。

这也解释了 A 的逆推为什么必在下一层终止。

## 5. 对 196 的数论排除

倒序不改变模 9 余数，因此

\[
N_t\equiv196\cdot2^t\equiv7\cdot2^t\pmod9.
\]

P_r 的数位和始终为 8。若 N_t=P_r，则

\[
7\cdot2^t\equiv8\pmod9,
\qquad\text{即}\qquad t\equiv5\pmod6.
\]

若它是第一个回文，(3) 又给出 t≤7，故只能 t=5。

每一步倒序相加最多增加一位，从三位数 196 出发，第 5 步至多有 8 位；而每个 P_r 至少有 9 位。矛盾。

所以，没有任何 P_r 能成为 196 轨道的第一个回文。

## 6. 边界、校验与剩余问题

7 步这个上界确实可达到；以下轨道的前七项均不是回文，第 7 步才得到目标族成员：

```
0  1700006609290
1  2629072609361
2  4268135318623
3  7536270637247
4  14963631363604
5  55599945000545
6  110100000000100
7  111100000001111
```

程序还对长度不超过 7 的全部 75,447 个可行数位对和词，用直接逐列加法独立核对了各层逆像成员关系。这项有限核对用于发现实现错误；它不是无限族结论的依据。无限族结论来自完整有限自动机的空语言判定。

本文没有给出其他回文形状的逆推上界，也没有证明所有危险状态都被排除。对完整 196 猜想，仍缺少覆盖所有潜在第一个回文的统一论证。

## 7. 可复核程序

将以下代码保存为 `verify_p196.py`，使用 Python 3 运行。无需第三方依赖。`forward` 使用直接逐列加法，独立于有限自动机的逆向转移。程序只核验本文局部命题，不应把输出解读为完整 196 猜想的证明。

```python
from collections import deque
from itertools import product

class DFA:
 def __init__(self,tr,end):self.tr=tr;self.end=end
 def accepts(self,s):
  q=0
  for u in s[:len(s)//2]:q=self.tr[q][u]
  term=0 if len(s)%2==0 else 1+s[len(s)//2]//2
  return bool(self.end[q]>>term&1)
 def minimize(self):
  # Moore partition refinement; end masks distinguish all terminal conditions.
  cls=[];d={}
  for v in self.end:
   if v not in d:d[v]=len(d)
   cls.append(d[v])
  while True:
   nc=[];ids={}
   for i,row in enumerate(self.tr):
    key=(self.end[i],tuple(cls[v] for v in row))
    if key not in ids:ids[key]=len(ids)
    nc.append(ids[key])
   if nc==cls:break
   cls=nc
  reps={}
  for i,c in enumerate(cls):reps.setdefault(c,i)
  # BFS to put initial class first and discard unreachable.
  start=cls[0];index={start:0};queue=[start];rows=[];ends=[]
  for c in queue:
   old=reps[c];row=[]
   for j in self.tr[old]:
    cc=cls[j]
    if cc not in index:index[cc]=len(queue);queue.append(cc)
    row.append(index[cc])
   rows.append(row);ends.append(self.end[old])
  return DFA(rows,ends)
 def witness(self):
  queue=deque([(0,())]);seen={0}
  while queue:
   q,p=queue.popleft()
   if self.end[q]:
    e=(self.end[q]&-self.end[q]).bit_length()-1
    return p+p[::-1] if e==0 else p+(2*(e-1),)+p[::-1]
   for u,r in enumerate(self.tr[q]):
    if r not in seen:seen.add(r);queue.append((r,p+(u,)))
  return None

# state: mode, target state, low carry, high carry, previous sum, flags
# flags encode at least one >=10, and at least one outside {0,11}.
def preimage(dfa, safe=True):
 def fl(u):return int(u>=10)+2*int(u not in (0,11))
 initial=frozenset([(0,0,0,0,-1,0),(1,0,0,1,-1,0)])
 def advance(st,u):
  mode,q,x,y,prev,flags=st
  if prev==-1 and u==0:return []
  nf=flags|fl(u);out=[]
  if mode==0:
   xp=(u+x)//10
   for yp in (0,1):
    if (u+yp)//10==y:
     r=2*u+x+yp-10*(xp+y)
     out.append((0,dfa.tr[q][r],xp,yp,u,nf))
  elif prev==-1:
   if u>=9:out.append((1,dfa.tr[q][u%10+1],u//10,1,u,nf))
  else:
   xp=(u+x)//10
   for yp in (0,1):
    if (prev+yp)//10==y:
     r=(u+x)%10+(prev+yp)%10
     out.append((1,dfa.tr[q][r],xp,yp,u,nf))
  return out
 def mask(st):
  mode,q,x,y,prev,flags=st;m=0
  def okay(f):return not safe or f==3
  if prev!=-1 and okay(flags):
   if mode==0 and x==y and dfa.end[q]&1:m|=1
   if mode==1 and (prev+x)//10==y:
    term=1+(prev+x)%10
    if dfa.end[q]>>term&1:m|=1
  for center in range(0 if prev!=-1 else 2,19,2):
   if not okay(flags|fl(center)):continue
   if mode==0:
    if (center+x)//10!=y:continue
    term=1+(center+x)%10
    if dfa.end[q]>>term&1:m|=1<<(1+center//2)
   elif prev==-1:
    if center>=10:
     r=center-9
     if dfa.end[dfa.tr[q][r]]&1:m|=1<<(1+center//2)
   else:
    xp=(center+x)//10
    if (prev+xp)//10!=y:continue
    r=(center+x)%10+(prev+xp)%10
    if dfa.end[dfa.tr[q][r]]&1:m|=1<<(1+center//2)
  return m
 # NFA states that can never reach target acceptance can be omitted using target liveness.
 live={i for i,e in enumerate(dfa.end) if e}
 while True:
  nxt=live|{i for i,row in enumerate(dfa.tr) if any(j in live for j in row)}
  if nxt==live:break
  live=nxt
 index={initial:0};queue=[initial];rows=[];ends=[]
 for subset in queue:
  end=0
  for st in subset:end|=mask(st)
  ends.append(end);row=[]
  for u in range(19):
   ss=frozenset(t for st in subset for t in advance(st,u) if t[1] in live)
   if ss not in index:
    index[ss]=len(queue);queue.append(ss)
    if len(queue)>100000:raise RuntimeError('State bound exceeded')
   row.append(index[ss])
  rows.append(row)
 return DFA(rows,ends).minimize()

def target_b():
 tr=[[1 if u==11 else 2 for u in range(19)],[1 if u in (0,11) else 2 for u in range(19)],[2]*19]
 return DFA(tr,[0,3,0])

def single_word(s):
 p=s[:len(s)//2];h=len(p);tr=[[h+1]*19 for _ in range(h+2)];end=[0]*(h+2)
 for i,u in enumerate(p):tr[i][u]=i+1
 end[h]=1<<(0 if len(s)%2==0 else 1+s[h]//2)
 return DFA(tr,end)


def family(prefix, minimum_zeros, terminal):
 p=list(prefix)+[0]*minimum_zeros
 n=len(p)
 tr=[[n+1]*19 for _ in range(n+2)]
 end=[0]*(n+2)
 for i,u in enumerate(p):tr[i][u]=i+1
 tr[n][0]=n
 end[n]=1<<terminal
 return DFA(tr,end)

def forward(s):
 digits=[]
 carry=0
 for u in s:
  total=u+carry
  digits.append(total%10)
  carry=total//10
 if carry:digits.append(carry)
 q=tuple(a+b for a,b in zip(digits,digits[::-1]))
 return q,digits!=digits[::-1]

def live_states(a):
 rev=[set() for _ in a.tr]
 for i,row in enumerate(a.tr):
  for j in row:rev[j].add(i)
 live={i for i,e in enumerate(a.end) if e}
 todo=list(live)
 for i in todo:
  for j in rev[i]:
   if j not in live:live.add(j);todo.append(j)
 return live

def prefixes(a,k):
 live=live_states(a)
 states=[(0,())]
 for _ in range(k):
  assert all(a.end[q]==0 for q,p in states), 'An earlier terminal needs separate handling'
  states=[(a.tr[q][u],p+(u,)) for q,p in states for u in range(19) if a.tr[q][u] in live]
 return sorted(p for q,p in states)

def main():
 all_chains=[]
 expected={'A':[6,9,17,43,122,155,637,1],'B':[6,6,9,1]}
 for name,start in [('A',family([1,1,1,1],0,1)),('B',family([11,0,11],1,0))]:
  chain=[start]
  for depth in range(1,len(expected[name])):
   chain.append(preimage(chain[-1]))
  sizes=[len(a.tr) for a in chain]
  assert sizes==expected[name],(name,sizes)
  assert chain[-1].witness() is None
  assert all(a.witness() is not None for a in chain[:-1])
  print(name,'DFA state counts:',sizes)
  if name=='A':
   for i,a in enumerate(chain[:-1]):print('A depth',i,'outer triples:',prefixes(a,3))
   assert prefixes(chain[6],2)==[(1,16)]
  all_chains.append(chain)
 # Independent bounded consistency check against literal column addition.
 # This is a software sanity check, NOT the all-length emptiness certificate.
 checked=0
 for L in range(1,8):
  for p in product(range(19),repeat=(L+1)//2):
   if p[0]==0 or (L%2 and p[-1]%2):continue
   s=p+p[:L//2][::-1]
   q,safe=forward(s)
   for chain in all_chains:
    for i in range(len(chain)-1):
     assert chain[i+1].accepts(s)==(safe and chain[i].accepts(q)),(s,i)
   checked+=1
 print('Independent literal-addition checks:',checked,'feasible pair words, length <= 7')
 # Small arithmetic conclusion independent of the automaton code.
 assert [t for t in range(8) if 7*pow(2,t,9)%9==8]==[5]
 assert 3+5<9
 print('Certified partial conclusion: no 1111 0^(2r+1) 1111 is the FIRST palindrome of the 196 trajectory.')
 print('This does not prove the full 196 conjecture.')

if __name__=='__main__':
 main()
```

## 8. 本轮实际运行输出

```text
A DFA state counts: [6, 9, 17, 43, 122, 155, 637, 1]
A depth 0 outer triples: [(1, 1, 1)]
A depth 1 outer triples: [(10, 0, 1), (10, 0, 10), (10, 9, 10)]
A depth 2 outer triples: [(5, 0, 5), (5, 4, 15), (9, 10, 0), (9, 10, 18)]
A depth 3 outer triples: [(2, 10, 2), (2, 12, 7), (4, 15, 8), (14, 9, 5)]
A depth 4 outer triples: [(1, 5, 1), (1, 6, 3), (2, 7, 14), (7, 4, 12)]
A depth 5 outer triples: [(3, 12, 5)]
A depth 6 outer triples: [(1, 16, 2)]
B DFA state counts: [6, 6, 9, 1]
Independent literal-addition checks: 75447 feasible pair words, length <= 7
Certified partial conclusion: no 1111 0^(2r+1) 1111 is the FIRST palindrome of the 196 trajectory.
This does not prove the full 196 conjecture.
```
