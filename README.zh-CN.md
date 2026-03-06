# RepoCheck

[English](./README.md) / [简体中文](./README.zh-CN.md)

RepoCheck 是一个面向 Python 与 PyTorch 研究仓库的本地优先可复现性审计器。仓库帮你回答四个非常具体的问题：

- 复现所需的信息到底有没有交代完整？
- 代码、配置和文档之间是否一致？
- 是否存在明显的不可复现风险？
- 新用户最应该先执行哪条最小验证命令？


## 为什么做 RepoCheck

研究仓库的“不可复现”通常不是抽象问题，而是这些非常具体的落点：

- 依赖没有锁版本
- Python 或 CUDA 版本没写
- 主入口不明确
- README 命令和代码默认值漂移
- 数据路径写死在私人机器上
- seed 设置不完整
- checkpoint 必须要有，但来源没说明

RepoCheck 会把这些问题转成结构化审计结果，包含严重级别、证据链和建议的最小复现命令。

## 能做什么

- 扫描本地目录、Git URL 或解压后的 zip 仓库
- 从仓库结构和 Python AST 推断框架与配置风格
- 从 README 代码块、脚本和 CI workflow 中抽取可执行命令
- 审计环境、入口、配置漂移、数据路径、随机性、文档和 checkpoint 风险
- 输出终端、JSON 和 HTML 报告
- 可选执行轻量 smoke 检查，并在隔离虚拟环境中验证命令可达性

## 快速开始

最快路径，直接从源码运行：

```bash
python -m repocheck check .
```

常用命令：

```bash
python -m repocheck check .
python -m repocheck check path/to/repo --report all
python -m repocheck check path/to/repo --smoke
python -m repocheck run path/to/repo --mode smoke
```

如果你希望安装成 CLI：

```bash
python -m venv .venv
```

macOS / Linux：

```bash
.venv/bin/python -m pip install -e .
repocheck check .
```

Windows PowerShell：

```powershell
.venv\Scripts\python -m pip install -e .
repocheck check .
```

## 输出示例

```text
Reproducibility Score: 47/100
Risk Summary: 3 high, 1 medium, 0 low

Suggested minimal command
python train.py --batch-size 64 --data-root ./data --epochs 1 --seed 42

Findings
[HIGH] ENV001: Dependency versions are not pinned
[HIGH] DATA001: Hardcoded absolute data path detected
[HIGH] SEED001: No reproducibility seed found
[MEDIUM] CFG001: README, config, and code values disagree
```

## 首批规则

当前 MVP 版本优先覆盖高价值审计项：

- `ENV001`：依赖未锁定精确版本
- `ENV002`：未声明 Python 版本
- `CUDA001`：未说明 CUDA 或 cuDNN 要求
- `RUN001`：缺少可执行入口或入口失效
- `DOC001`：README 缺少最小可执行示例
- `DATA001`：检测到硬编码绝对数据路径
- `DATA002`：缺少数据下载或准备说明
- `SEED001`：未发现随机种子设置
- `SEED002`：DataLoader 或 CUDA 确定性设置不完整
- `CFG001`：README、配置和代码参数不一致
- `ART001`：checkpoint 来源未说明

## 仓库结构

```text
repocheck/
 __main__.py
 cli.py
 core.py
tests/
 fixtures/
 test_cli.py
```

## 当前范围

- 先聚焦 Python 仓库
- 对 PyTorch、argparse、Click、Hydra 风格项目做尽力支持
- 默认优先静态分析，这是最快也最稳的入口
- smoke 模式刻意保持轻量，重点验证 `--help` 与 `--dry-run` 的可达性

## 开发

运行测试：

```bash
python -m unittest discover -s tests -v
```

本地运行 CLI：

```bash
python -m repocheck check tests/fixtures/sample_project --report all
```

## 贡献

如果有什么很重要的判定要素没有提及，欢迎PR！

