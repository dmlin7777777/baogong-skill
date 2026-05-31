# Phase 2.5 Refactor Design

**Date**: 2026-04-20
**Scope**: renderer.py Phase 2.5 + CSS compact preset
**Trigger**: 复盘 5 个渲染 bug，根因集中在 `_map_html_to_css_classes()` 单体函数

## Problem Summary

| # | Bug | Root Cause |
|---|-----|-----------|
| 1 | HTML 与 CSS 结构脱节 | 缺少 markdown→CSS 的结构映射层 |
| 2 | Skills bullet-summary 未拆分 | 正则缺少 DOTALL，未覆盖 `<li>` 容器 |
| 3 | Experience bullets 丢失 | 逐行扫描时 `<div>` 被提前关闭 |
| 4 | Dept/Location 颠倒 | 用位置而非分隔符解析字段 |
| 5 | 一页限制无强制控制 | 无 compact CSS preset + 无自动切换 |

## Refactor Architecture

### Token → Section → Renderer 三层解耦

```
_map_html_to_css_classes(html_fragment) -> str
│
├─ _tokenize(html_fragment) -> list[HtmlToken]
│     将 HTML 片段切分为有语义的 token 流
│
├─ _group_into_sections(tokens) -> list[Section]
│     按 h2 边界分组为 Section 对象
│
└─ 对每个 Section 分派到独立解析器：
     ├─ _render_header_section(tokens) -> str
     ├─ _render_education_items(tokens) -> str
     ├─ _render_experience_items(tokens) -> str
     ├─ _render_skills_section(tokens) -> str
     └─ _render_paragraph(token) -> str
```

### Data Structures

```python
@dataclass
class HtmlToken:
    type: str                    # "h1" | "h2" | "h3" | "paragraph" | "list" | "empty"
    raw_lines: list[str]         # 原始 HTML 行
    text: str = ""               # 提取的纯文本（heading 标题等）

@dataclass
class Section:
    title: str                   # h2 文本
    type: str                    # "header" | "education" | "experience" | "skills" | "projects" | "summary"
    tokens: list[HtmlToken]
```

### Section Type Routing

| h2 关键词 | Section type | 渲染器 |
|-----------|-------------|--------|
| (h2 之前) | header | `_render_header_section` |
| 教育 | education | `_render_education_items` |
| 经历/实习 | experience | `_render_experience_items` |
| 技能/证书 | skills | `_render_skills_section` |
| 学术/项目 | projects | `_render_experience_items`（复用） |
| 其余 | summary | `_render_paragraph` |

### Per-Section Parser Contracts

- **输入**: `list[HtmlToken]`（该 section 内的所有 token）
- **输出**: `str`（映射后的 HTML 片段）
- **约束**: 不依赖外部状态，独立可测试

### Key Parsing Conventions

1. **字段分隔**: 统一用 `|` 作为字段分隔符
2. **地点定位**: 最后一个 `|` 后面匹配城市名 pattern → 地点
3. **日期匹配**: `\d{4}[\.\s]*\d*[\.\s]*\s*[–\-]\s*(?:至今|\d{4}[\.\s]*\d*)`
4. **部门**: 去掉日期和地点后的剩余文本
5. **跨行处理**: 所有正则默认 `re.DOTALL`

## Compact CSS Preset

### Implementation

单文件双模式，通过 `<body class="compact">` 切换：

```css
/* normal (default) */
:root { --fs-body: 9.5pt; --lh-body: 1.38; --gap-section: 7pt; ... }

/* compact */
body.compact { --fs-body: 9pt; --lh-body: 1.3; --gap-section: 4pt; ... }
```

### Auto-Switch Logic

```
render()
  Phase 1: preprocess
  Phase 2: markdown → HTML
  Phase 2.5: structure mapping
  Phase 3: render_html_layout(mode="normal")
  Phase 4a: PDF render
    if pages > 1 and page_limit == 1:
      Phase 3: render_html_layout(mode="compact")  # 重渲染
      Phase 4a: PDF render (verify)
      if still overflow: warning, return
```

最多 2 次 PDF 渲染，不无限循环。

### Jinja2 Template Change

```html
<body class="{{ body_class }}">
```

## Files Changed

| File | Change |
|------|--------|
| `scripts/renderer.py` | 重写 Phase 2.5 (tokenize + section routing + per-section parsers) |
| `templates/resume_template.css` | 新增 `body.compact` CSS 变量覆盖 |
| `templates/resume_layout.html.j2` | `body` 标签增加 `class="{{ body_class }}"` |

## Testing Strategy

每个 `_render_*` 函数应有独立的输入/输出 fixture：
- 正常输入 → 期望输出
- 边界输入（空内容、跨行 p 标签、缺少日期）→ 期望输出
