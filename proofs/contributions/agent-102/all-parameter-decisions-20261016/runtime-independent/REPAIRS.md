# 完整失败与修复记录

本任务共进行两次实质源码编译尝试；没有遗弃失败的数学源或编译日志。

## attempt-001：真实失败

首版 Controls SHA256：
`1d2699beb16ba976f747c87fb2eb0fc653ce6614abe4d9ea79c6169dec910904`，9085 字节。

九个依赖模块依次清洁编译成功，包括冻结的 RunDecision 与 AllParameters。
Controls 的八个小参数 Bool 闭证书在 `decide` 展开时达到默认 `maxRecDepth` 限制。
任意 `k` 的列表和边界证明，以及三个巨大参数的 `equalAt` 闭证书均已通过。

完整日志含八条 `maximum recursion depth has been reached` 错误。
Lean 在出错命令处恢复 elaboration 时生成了 `sorryAx`，随后 literal 公理输出
也如实显示失败声明及其应用依赖 `sorryAx`。这不是手写的 sorry，更不是可接受的证明。
此尝试被明确标记 FAILED。

原控制包装脚本按模块保存实际子进程退出码，遇到失败停止；它本身结束时的 shell 退出码
不能替代所保存的 Lean 退出码。`verification.json` 中 Controls 的 `returncode` 为 1，
没有根据外层脚本退出成功把这次尝试误记为通过。

## 唯一修复

在 Controls namespace 中加入：

```lean
-- 压缩布尔项的内核归约需要比默认值更深的递归栈。
set_option maxRecDepth 8192
```

除此以外没有改动任何定义、定理声明、证明或 literal 审计命令。
精确差异在 `REPAIR.diff`。
该选项只提高 elaboration/归约资源限制，没有改变信任级别或跳过 kernel checking。

## attempt-002：冻结版本成功

Controls SHA256：
`a1bb882b1b8396406f82e9814bc4522d2f2d13b96c7e859fad0d6d650c1914d2`，9187 字节。

在全新输出目录再次从源码重建十个项目模块，随后编译三个审计模块，全部成功。
32 条作者定理的 literal 公理输出全部不含 `sorryAx`。
完整 module-origin 公理审计和 Bool 定义依赖审计也成功。

本次 `reproduce.py` 的原始脚本、执行参数、源码散列与 stdout/stderr 全部保留。
首版和修复版都可以在独立新目录重新运行。
