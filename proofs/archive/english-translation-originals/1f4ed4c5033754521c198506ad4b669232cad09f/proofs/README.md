# 当前研究入口

本目录保留经过本次分类的当前源码；每个来源版本另有字节一致的历史原件。历史树不等于当前证明，时间戳不等于有效性。

[结果目录](RESULTS.md) · [状态](STATUS.md) · [问题](OPEN_PROBLEMS.md) · [源码映射](SOURCE_MAP.json)

原始主线基点：`2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`。

## 原布局兼容核验

现有脚本可能依赖原始路径。`replay_original_layout.py` 在仓库外的新临时目录重建原布局，优先使用本目录中匹配的当前源码，且逐文件检查哈希，不修改当前工作区。

```sh
python3 proofs/verify_project.py --lean /absolute/path/to/lean --project consolidation-core --output /absolute/new/output/directory
python3 proofs/verify_release.py
```

这些命令重放原始主线的对应检查，不声称覆盖新增当前来源或全部历史项目。每个其他当前来源必须在迁移检查记录中保留自己的独立验证命令和依赖。清理工具的独立 preservation verifier 另行验证整个迁移树，不能由旧 release 检查代替。
