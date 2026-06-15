# Scenario A: JD + Resume

## Prompt

```
帮我针对这个 JD 调简历

JD:
高级数据分析师 — 美团（上海）
要求：
- 3年以上数据分析经验
- 精通 Python、SQL
- 熟悉 AB 实验设计与分析
- 有数据仓库建设经验优先
- 较强的跨部门沟通能力

我的简历在 resume_master.md
```

## Expected Routing

- Scenario: **A** (JD + resume both provided)
- Pipeline: Scout → Architect → Auditor → Render

## Expected Behaviors

1. **Scout phase**: Extracts 5 capability clusters from JD, searches for 美团 interview experiences
2. **Matching**: Maps resume experiences to JD requirements with confidence levels
3. **Bullet format**: Every output bullet follows `**Prefix**: detail` format
4. **Quantification**: Probes for missing metrics (max 2 rounds), keeps original wording if user can't quantify
5. **Fabrication gate**: No invented metrics, no upgraded role verbs without evidence
6. **Info status**: All claims marked `[✓]`, `[?]`, or `[~]`
7. **Deliverables**: HTML + Markdown resume, audit log, interview prep pack

## Red Flags (should NOT happen)

- Bullet without `**Prefix**:` format
- Invented percentages or metrics
- "主导" verb without decision-maker evidence
- Missing interview prep pack
- Skipped checkpoints (CP1-CP5)
