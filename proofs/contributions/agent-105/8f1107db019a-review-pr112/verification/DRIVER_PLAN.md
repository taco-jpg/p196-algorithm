# PR112 独立核心验证计划

实际执行者：`/root/lean_runtime`（Agent105）；作者是 Agent111。本次固定作者源码提交 `01ecb6aa6bc555335ff6cb628d08e84133888307`，claim `fa964a32b14a9f949ee2dc7e2eb209c5aa7f0cf2`。

当前状态：仅冻结验证方案和原验证器材料，尚未报告数学验证通过。语义审查由另一个真实子代理 `/root/ownership_audit` 独立完成。

## 编译与证据

1. 使用精确来源映射恢复原模块名、原 import 和原字节，验证 SHA256、Git blob 与递归闭包。拒绝 adapter、未登记外部依赖及禁用证明原语。
2. 每次主构建选择此前不存在的外部目录，复制13份 Lean 源；不复制、不搜索、不加载既有项目 `.olean`。`LEAN_PATH` 仅指向本次目录，Lean标准库来自已核对官方工具链。
3. 逐模块执行官方 Lean4.19.0：`--trust=0 -j1 -DElab.async=false -o MODULE.olean MODULE.lean`。真实记录版本、完整命令、cwd、受控环境、起止时间、退出码、原始log与hash。仅此验证链执行重Lean。
4. 原module-origin定理审计body从未修改的仓库验证器提取并逐字保存；原body允许公理集合仍为 `propext`、`Classical.choice`、`Quot.sound`。选择13模块、imports和显式端点是本次新driver生成。
5. 另外运行自写safe-definition/opaque审计：按真实定义模块遍历所有安全定义，并收集其全部公理依赖；unsafe或partial声明独立列出，不纳入安全证明通过数量。显式公开端点执行 `#check` 和 `#print axioms`。
6. 以实际日志核对声明唯一性、模块覆盖、计数与公理并集；作者报告的13模块1012定理只作对照，不作为判定输出。保留全部失败尝试，未通过不掩盖为通过。

## 与原验证器的区别

原验证器完整快照在 `provenance/OriginalVerifier.py`，SHA256 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`。本次使用独立作者标识的fresh runner，不宣称执行了原脚本未修改版本。原module-origin定理审计body逐字复用；新runner显式加 `--trust=0`，只使用本次选定13源，新增安全定义审计与逐端点 `#print axioms`。完整命令和全部driver源均保留。

审查写入范围仅为分配的 registry 与本 verification 目录；不改 Agent111 源、原验证器或他人数学文件，不执行 Git 写。
