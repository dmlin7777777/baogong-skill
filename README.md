<div align="center">

# 包公.skill

> _「卷宗未到，不开堂。陈词未清，不结案。能扛住追问的，才上终稿。」_

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-blue)](https://skills.sh)
[![Multi-Runtime](https://img.shields.io/badge/Runtime-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20Gemini%20CLI%20%C2%B7%20Cursor-blueviolet)](#安装)

**别的工具给你润色。包公开堂——**
**从卷宗调阅到应对回话，一条龙审完，才上终稿。**

JD 驱动的简历定制教练：调卷宗 → 当堂陈词 → 案卷归档 → 应对回话。
编造一条打回一条。HTML + Markdown 双交付，每版可进 Git 审计。

**其他语言：** [English](README.en.md) · 简体中文

</div>

---

<div align="center">

<img src="assets/before.png" alt="Before: 典型 AI 润色 — 空泛形容词堆砌" width="100%">

<img src="assets/after.png" alt="After: 包公四幕审完后终稿 — 量化到人、事、数 + 瑞士风排版" width="100%">

▲ 上：典型 AI 润色（空泛形容词堆砌）　→　下：包公审完后终稿（量化 + 瑞士风排版）

</div>

---

## 四幕审什么

| 幕 | 你的经历在包公这儿过哪一关 | 你最终拿到 |
|---|---|---|
| **调卷宗** | 联网搜面经 + 查公司 + 抓岗位隐性要求（4 级降级链） | `interview_intel` 情报卡：高频考点、面试官风格、隐性要求 |
| **当堂陈词** | 经历匹配 + 2 轮量化追问（最多），说不出保留原文 | 每条 `**前缀**：内容` 格式的 STAR bullet，前缀命中 JD 关键词 |
| **案卷归档** | Writer 出稿 → Auditor 独立审计（物理隔离）→ 历史版本对比 | snapshot + Markdown + 瑞士风 HTML + 审计日志 |
| **应对回话** | 基于面经的 mock 问题 + STAR 笔记 | `{date}_{company}_{role}_interview_prep.md` |

---

## 安装

```bash
npx skills add dmlin7777777/baogong-skill
```

装好后一句话启动：

```
帮我针对这个 JD 调简历
```

<details>
<summary>其他安装方式</summary>

**手动安装（Claude Code）：**
```bash
git clone https://github.com/dmlin7777777/baogong-skill.git ~/.claude/skills/baogong-skill
```

**Cursor / Codex / 其他 runtime：** 将 `SKILL.md` 放到对应 skills 目录即可。

</details>

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

<details>
<summary><strong>开发者文档</strong></summary>

### 文件结构

```
baogong-skill/
├── SKILL.md              # Skill 定义（58K，全部工作流）
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
