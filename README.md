<div align='center'>
    <img src="./docs/images/diy-llm.png" alt="LLM Notebook Lab" width="100%">
    <h1>LLM Notebook Lab</h1>
</div>

<div align="center">
  <img src="https://img.shields.io/badge/language-Chinese-brightgreen?style=flat" alt="Language"/>
  <img src="https://img.shields.io/badge/format-Jupyter%20Notebook-orange?style=flat&logo=jupyter" alt="Jupyter Notebook"/>
  <img src="https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey?style=flat" alt="License"/>
  <a href="https://github.com/tandede/llm-notebook-lab"><img src="https://img.shields.io/badge/GitHub-tandede%2Fllm--notebook--lab-blue?style=flat&logo=github" alt="GitHub Project"></a>
</div>

<div align="center">
  <h3>可边读边运行的大语言模型学习笔记</h3>
  <p><em>基于 Datawhale Diy-LLM 的个人非商业学习改编版</em></p>
</div>

本仓库是我在学习 [Datawhale Diy-LLM](https://github.com/datawhalechina/diy-llm) 过程中的个人改编版，核心目标是把章节内容整理为可运行的 Jupyter Notebook，让阅读、实验、调试和复盘可以在同一个环境里完成。

本项目仅用于个人学习与非商业分享，不是原项目的官方版本，也不代表原作者或 Datawhale 对本改编版背书。二次传播或继续改编时，请继续遵守原项目采用的 [CC BY-NC-SA 4.0](http://creativecommons.org/licenses/by-nc-sa/4.0/) 许可证。

## 改编说明

- 将主要章节从 Markdown 改为 `.ipynb`，方便边学习边运行代码。
- 保留原课程的章节结构、作业目录和大部分原始内容。
- 增加了部分 notebook 运行辅助文件，例如第三章的辅助函数与示例输出文件。
- 调整 README 与入口链接，使仓库更适合作为个人学习版使用。

## 前置要求

- **Python 编程**：熟悉 Python 与基本软件工程实践
- **深度学习基础**：熟悉 PyTorch，了解神经网络基本原理
- **数学基础**：线性代数、概率统计、微积分
- **机器学习基础**：理解常见机器学习与深度学习概念
- **GPU 编程（可选）**：了解 CUDA 会更有帮助，但不是阅读全部内容的必要条件

## 课程目录

| 章节 | 关键内容 | 配套作业 | 入口 |
|------|----------|----------|------|
| 前言 | 项目背景与学习建议 | - | [Notebook](docs/前言.ipynb) |
| 第1章 工具使用 | W&B 使用与实验追踪 | - | [Notebook](docs/chapter1/wandb使用介绍.ipynb) |
| 第2章 分词器 | 分词器原理与 BPE 实现 | [作业1](coursework/assignment1-basics/) | [Notebook](docs/chapter2/chapter2_分词器.ipynb) |
| 第3章 PyTorch 与资源核算 | 训练原语、算力/显存估算 | - | [Notebook](docs/chapter3/chapter3_pytorch与资源核算.ipynb) |
| 第4章 语言模型架构与训练细节 | Transformer 架构与训练要点 | [作业1](coursework/assignment1-basics/) | [Notebook](docs/chapter4/chapter4_第四章语言模型架构和训练的技术细节.ipynb) |
| 第5章 混合专家模型 | MoE 原理、路由与工程实践 | - | [Notebook](docs/chapter5/chapter5_混合专家模型.ipynb) |
| 第6章 GPU 与相关优化 | GPU 基础与优化技巧 | [作业2](coursework/assignment2-systems/) | [Notebook](docs/chapter6/chapter6_第六章GPU和GPU相关的优化.ipynb) |
| 第7章 GPU 高性能编程 | CUDA 与高性能编程 | [作业2](coursework/assignment2-systems/) | [Notebook](docs/chapter7/chapter7_第七章GPU高性能编程.ipynb) |
| 第8章 分布式训练 | 并行范式与跨机训练 | [作业2](coursework/assignment2-systems/) | [Notebook](docs/chapter8/chapter8_第八章分布式训练.ipynb) |
| 第9章 Scaling Laws | 扩展定律与实验 | [作业3](coursework/assignment3-scaling/) | [Notebook](docs/chapter9/chapter9_Scaling_Laws.ipynb) |
| 第10章 推理 | 推理性能与落地优化 | [作业6](coursework/assignment6-evaluation/) | [Notebook](docs/chapter10/推理.ipynb) |
| 第11章 数据工程 | 数据清洗、构建与管理 | [作业4](coursework/assignment4-data/) | [Notebook](docs/chapter11/chapter11_数据工程.ipynb) |
| 第12章 评估与基准测试 | 指标体系与评测方法 | [作业6](coursework/assignment6-evaluation/) | [Notebook](docs/chapter12/chapter12_评估与基准测试.ipynb) |
| 第13章 大模型的基本训练流程 | 预训练、SFT、RL 流程 | [作业5](coursework/assignment5-alignment/) | [Notebook](docs/chapter13/chapter13_第十三章大模型的基本训练流程.ipynb) |
| 第14章 可验证奖励的强化学习 | RLVR 思想与实践 | [作业5](coursework/assignment5-alignment/) | [Notebook](docs/chapter14/chapter14_可验证奖励的强化学习.ipynb) |
| 第15章 扩展内容 | LLM 推理相关扩展 | - | [Notebook](docs/chapter15/什么是LLM推理.ipynb) |

## 作业概览

| 作业 | 核心任务 | 目录 |
|------|----------|------|
| 作业1：手搓大模型 | 实现 tokenizer、model architecture、optimizer，训练极简语言模型 | [assignment1-basics](coursework/assignment1-basics/) |
| 作业2：系统优化 | 性能分析、FlashAttention-2、分布式训练 | [assignment2-systems](coursework/assignment2-systems/) |
| 作业3：扩展定律 | 理解 Transformer 组件，拟合 scaling law | [assignment3-scaling](coursework/assignment3-scaling/) |
| 作业4：数据处理 | Common Crawl 数据清洗、过滤与去重 | [assignment4-data](coursework/assignment4-data/) |
| 作业5：模型对齐 | SFT 与强化学习训练数学推理模型 | [assignment5-alignment](coursework/assignment5-alignment/) |
| 作业6：模型评估 | 使用 lm-evaluation-harness 和 evalscope 做评测 | [assignment6-evaluation](coursework/assignment6-evaluation/) |

## 快速开始

```bash
git clone https://github.com/tandede/llm-notebook-lab.git
cd llm-notebook-lab

# 安装 Jupyter 环境
pip install jupyterlab notebook

# 启动 notebook
jupyter lab
```

不同章节和作业可能需要额外依赖。建议进入对应目录后，优先查看该目录的 README、`pyproject.toml`、`requirements.txt` 或 notebook 开头的说明。

## 项目结构

```text
llm-notebook-lab/
├── docs/                    # 章节 notebook 与图片资源
│   ├── 前言.ipynb
│   ├── chapter1/
│   ├── chapter2/
│   ├── chapter3/
│   ├── chapter4/
│   ├── chapter5/
│   ├── chapter6/
│   ├── chapter7/
│   ├── chapter8/
│   ├── chapter9/
│   ├── chapter10/
│   ├── chapter11/
│   ├── chapter12/
│   ├── chapter13/
│   ├── chapter14/
│   └── chapter15/
├── coursework/              # 配套作业与实验代码
├── scripts/                 # 文档转 notebook 的辅助脚本
├── README.md
└── .gitignore
```

## 相关链接

- 原项目仓库：[datawhalechina/diy-llm](https://github.com/datawhalechina/diy-llm)
- 原项目在线阅读：[Datawhale Diy-LLM](https://datawhalechina.github.io/diy-llm/)
- 原版课程主页：[Stanford CS336 (Spring 2025)](https://stanford-cs336.github.io/spring2025/)
- 原版课程项目：[stanford-cs336/spring2025-lectures](https://github.com/stanford-cs336/spring2025-lectures/tree/main)

## 许可证

本改编版延续原项目的许可方式，采用 [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/)。

简单来说：可以分享和改编，但需要署名、仅限非商业用途，并且改编后的内容也需要使用相同许可证发布。正式条款以许可证全文为准。

## 致谢

- 感谢 [Datawhale Diy-LLM](https://github.com/datawhalechina/diy-llm) 项目提供系统性的中文 LLM 学习材料，本仓库是在其基础上的个人学习改编版。
- 感谢 Diy-LLM 的项目负责人、贡献者和社区参与者，原始贡献者信息请以原项目 README 为准。
- 感谢 Stanford CS336 课程团队提供优秀的原版课程与公开资料。
- 感谢开源社区中所有分享大语言模型训练、评估、推理和系统优化经验的研究者与开发者。

---

<div align="center">
  <p>边读、边改、边运行，系统性学习大语言模型构建技术。</p>
</div>
