# Scenario B: Resume Only (No JD)

## Prompt

```
帮我优化简历，没有特定的目标岗位

我的简历在 resume_master.md
```

## Expected Routing

- Scenario: **B** (resume only, no JD)
- Pipeline: Story-library polish mode (no JD matching phase)

## Expected Behaviors

1. **No JD matching**: Skips Scout research phase, no capability cluster extraction
2. **Story library**: Builds/references project-story-library.md
3. **General polish**: Focuses on bullet clarity, quantification, format compliance
4. **Bullet format**: Still enforces `**Prefix**: detail` format
5. **Quantification probing**: Same 2-round max rule applies
6. **Regional default**: Asks user for target region before adjusting tone

## Red Flags (should NOT happen)

- Attempting JD keyword matching without a JD
- Fabricating a "target role" to match against
- Skipping quantification probing
