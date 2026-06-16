<div align="center">

# 包公.skill

> _「卷宗未到，不开堂。陈词未清，不结案。能扛住追问的，才上终稿。」_

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-blue)](https://skills.sh)
[![Multi-Runtime](https://img.shields.io/badge/Runtime-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20Gemini%20CLI%20%C2%B7%20Cursor-blueviolet)](#安装)

**针对 JD 交互式定制简历的求职教练。**
**每条经历经得起面试追问，编造自动阻断。HTML + Markdown 双交付。**

**其他语言：** [English](README.en.md) · 简体中文

</div>

---

## 你的简历写完了，面试官一追问就穿帮

<div align="center">

| 维度 | 传统 AI 润色 | 包公 |
|:----:|:----------:|:----:|
| **输入** | "帮我优化一下简历" | "帮我针对这个 JD 调简历" |
| **量化数据** | 编一个好看的数字 | 追问 2 轮，问不出就写过程描述，绝不编造 |
| **动词等级** | "参与"全改"主导" | 根据故事库证据定级，没决策权就写"协同" |
| **JD 匹配** | 塞满关键词 | 5 状态分类，缺口诚实告知（含"不建议硬凑"） |
| **面试准备** | 无 | 每条显著变化 bullet 生成 STAR 应答 + mock 追问 |
| **造假请求** | "好的，帮你写上" | 🔴 硬阻断 + 三重风险解释 + 正向引导 |
| **审计** | 自己写自己审 | Writer / Auditor 物理隔离，两次独立 LLM 调用 |

</div>

<div align="center">

<img src="assets/before.png" alt="Before: 典型 AI 润色 — 空泛形容词堆砌" width="100%">

<img src="assets/after.png" alt="After: 包公四幕审完后终稿 — 量化到人、事、数 + 瑞士风排版" width="100%">

▲ 上：典型 AI 润色（空泛形容词堆砌）　→　下：包公审完后终稿（量化 + 瑞士风排版）

</div>

---

## 安装

```bash
npx skills add dmlin7777777/baogong-skill
```

装好后一句话启动：

```
帮我针对这个 JD 调简历
```

没有简历文件？包公会自动引导你从零创建 `resume_master.md`。

<details>
<summary>其他安装方式</summary>

**手动安装（Claude Code）：**
```bash
git clone https://github.com/dmlin7777777/baogong-skill.git ~/.claude/skills/baogong-skill
```

**Cursor / Codex / 其他 runtime：** 将 `SKILL.md` 放到对应 skills 目录即可。

</details>

---

## 四幕审什么

| 幕 | 你的经历在包公这儿过哪一关 | 你最终拿到 |
|---|---|---|
| **调卷宗** | 联网搜面经 + 查公司 + 抓岗位隐性要求（4 级降级链） | `interview_intel` 情报卡：高频考点、面试官风格、隐性要求 |
| **当堂陈词** | 经历匹配 + 2 轮量化追问（最多），说不出保留原文 | 每条 `**前缀**：内容` 格式的 STAR bullet，前缀命中 JD 关键词 |
| **案卷归档** | Writer 出稿 → Auditor 独立审计（物理隔离）→ 历史版本对比 | snapshot + Markdown + 瑞士风 HTML + 审计日志 |
| **应对回话** | 基于面经的 mock 问题 + STAR 笔记 | `{date}_{company}_{role}_interview_prep.md` |

---

## 一次完整运行长什么样

```
用户  ❯ 帮我针对这个高级数据分析师 JD 调简历

Scout ❯ ✅ JD 解析完成。提取 5 个能力簇：
        Python/SQL · AB实验 · 数据仓库 · 跨部门协作 · 指标体系
        📡 搜索该公司面经中... 找到 12 条高频问题。

Arch  ❯ 匹配你的 3 段经历，置信度：
        星辰科技 92% · 毕设数据项目 71% · 社团财务 34%
        ⏸ CP1：保留前两段，隐藏第三段？

用户  ❯ 可以

Arch  ❯ 量化追问（CP3）：
        "搭建数据看板"——覆盖多少业务线？异常响应时间？

用户  ❯ 12 条业务线，之前人工抽查大概两天，现在实时告警
```
```diff
- 负责数据分析相关工作，得到领导认可
+ **数据监控体系**：搭建核心指标看板，覆盖 12 条业务线，
+   异常检出从人工抽查（~2天）→ 实时告警
```
```
Audit ❯ 铡刀门通过。三色签：[✓] 12条业务线  [✓] 实时告警
        📋 面试准备包已生成：
        Q1: "看板指标怎么选的？谁定的？"
        Q2: "实时告警误报率多少？怎么处理？"
```

---

## 六堂会审：自动路由

你只需说你要什么，包公判断走哪条路。

| 堂 | 输入条件 | 产出 |
|---|---------|------|
| **Mode A** | 简历 + 单个 JD | 定制简历 + 审计报告 + 面试准备包 |
| **Mode A2** | 简历 + 多个 JD | 多份定制简历 + 跨 JD 差异对比表 |
| **Mode B** | 仅简历（无 JD） | 通用方向简历（故事库为唯一事实来源） |
| **Scenario C** | 仅 JD（无简历） | JD 需求分析 → 引导建简历 → 进入 Mode A |
| **Scenario D** | 信息不足 | 信息收集 → 重新路由 |
| **Scenario E** | 用户要求造假 | 🔴 铡刀门阻断 + 正向引导 |

---

## 你拿到什么

不只一份简历——一套**求职攻防包**：

| 交付物 | 说明 |
|---|---|
| **定制简历** | 瑞士国际主义风 HTML + Markdown，A4 打印优化，单文件零依赖 |
| **审计日志** | 每条修改的置信度 + 三色签溯源，Writer/Auditor 物理隔离 |
| **面试准备包** | 基于真实面经的 mock 问题 + STAR 应答笔记 |
| **状态快照** | JSON 完整决策记录，可追溯每个 checkpoint 的用户确认 |

<div align="center">

<img src="assets/showcase-swiss.png" alt="瑞士国际主义风简历渲染效果" width="700">

▲ 渲染产物：瑞士国际主义风 HTML，浏览器 Ctrl+P 即 PDF

</div>

---

## 铡刀门：三层防伪体系

简历上的每个字都必须经得起面试追问。三层机制保障：

**1. 编造阻断（Scenario E）**

用户请求编造经历 → 硬拒绝，不进入任何工作流。解释三重风险（面试追穿、背调撤 offer、部分地区刑事责任），引导用真实经历竞争。"帮我美化措辞" ≠ 造假，正常放行。

**2. 三色签标记体系**

| 签 | 含义 | 处理 |
|:--:|------|------|
| `[✓]` | 用户确认，或来自源简历原文 | 可直接使用 |
| `[?]` | 提取但未经本轮确认 | 需在 CP 中确认 |
| `[~]` | 模型推断，用户未提供 | 必须转为 `[✓]` 或删除，禁止进入终稿 |

**3. Writer / Auditor 物理隔离**

Writer 只写不审，Auditor 重新阅读源简历和 JD 独立审计。审计发现 🔴 MAJOR → 整份草稿打回重审。

---

## 量化追问：Anti-Filler Rule

```
Round 1（范围）："影响了多少人/多少业务线？"
Round 2（对比）："改造前后分别是什么状态？"
    ↓ 2 轮后仍无数字 → 写过程描述，绝不编造

❌ "实现智能化"  ❌ "显著提升效率"  ❌ "大幅优化流程"
✅ "搭建实时告警系统，替代人工抽查流程"
✅ "设计并实施 AB 实验分析框架，支撑产品决策"
```

---

## Limitations

- **需要用户参与** — 4 个交互检查点（CP1-CP4）都需要用户回复。包公是教练，不是代笔
- **面经搜索依赖网络** — 网络受限时会降级（WebFetch → agent-browser → Chrome MCP → 搜索摘要）
- **量化数据依赖用户记忆** — 你记不清的数字，包公也变不出来
- **PDF 非自动生成** — HTML 输出需手动 Ctrl+P 保存为 PDF
- **故事库需要前期投入** — Mode B 首次录入约需 10-20 分钟
- **单 Agent 环境审计降级** — Writer/Auditor 无法真正物理隔离时标注 `isolation_mode: degraded`
- **v3.3 起不再支持 DOCX** — 只输出 MD + HTML，零外部依赖

---

## 为什么叫包公

每个用 AI 写过简历的人都经历过同一个场景：

工具帮你把"参与了数据分析"改成"主导端到端数据分析体系建设，赋能业务增长 300%"。读起来很唬人。然后面试官问："这个 300% 怎么算的？"你哑了。

问题不是 AI 写得不好——而是它写得太好了，好到你自己都不认识了。

包公的名字来自包青天——铁面无私，不造假。它的第一条规则不是"帮你写得更好"，而是**"每条 bullet 都必须经得起面试追问"**。宁可少写一条真实的，也不多编一条好看的。

---

<details>
<summary><strong>开发者文档</strong></summary>

### 文件结构

```
baogong-skill/
├── SKILL.md              # Skill 定义（全部工作流）
├── scripts/
│   ├── engine.py         # 状态管理（Snapshot）
│   ├── renderer.py       # MD → HTML（零依赖）
│   ├── jd_parser.py      # JD + 简历结构化提取
│   ├── diff_audit.py     # 源 vs 定制变更分析
│   └── main.py           # 统一 CLI
├── templates/
│   └── resume_swiss.html # 瑞士风模板（CSS 变量驱动）
├── schemas/
│   └── snapshot_schema_v1.json
└── references/           # 节点指令 + 审计清单
```

### 渲染

```bash
python -X utf8 scripts/renderer.py --md draft.md --output output/
```

零外部依赖。`renderer.py` 仅用 `json`、`re`、`pathlib`。

### Dependencies

渲染管线零外部依赖（仅 Python 标准库）。简历读取需要：
- `python-docx`（解析 .docx 源文件）
- `pdfplumber`（解析 .pdf 源文件）

Agent 权限：Read, Write, Glob, WebFetch, WebSearch。

</details>

---

## 版本历史

见 [CHANGELOG.md](CHANGELOG.md)。

| 版本 | 日期 | 要点 |
|---|---|---|
| **v3.4** | 2026-06 | 6 场景路由、编造阻断门、信息状态标记、面试准备包 |
| **v3.3** | 2026-06 | 三层联网搜索、零依赖渲染、瑞士风 HTML 模板 |
| **v3.2** | 2026-05 | 初始化系统、Agent 反模式、Darwin 76→92 |

---

<div align="center">

MIT License

</div>
