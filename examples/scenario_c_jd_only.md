# Scenario C: JD Only (No Resume)

## Prompt

```
这个岗位需要什么能力？

JD:
Senior Backend Engineer — Stripe (San Francisco)
Requirements:
- 5+ years backend development
- Proficiency in Go, Ruby, or Java
- Experience with distributed systems and payment infrastructure
- Strong understanding of database design and optimization
- Track record of mentoring junior engineers
```

## Expected Routing

- Scenario: **C** (JD only, no resume)
- Pipeline: Advisory output (gap analysis + preparation guidance)

## Expected Behaviors

1. **JD parsing**: Extracts capability clusters and requirement tiers
2. **Advisory output**: Produces gap analysis, NOT a tailored resume
3. **Preparation guidance**: Suggests what experiences/skills to develop
4. **No fabrication**: Does not generate fake resume content
5. **Resume request**: Asks user to provide resume for full tailoring

## Red Flags (should NOT happen)

- Generating a resume without source material
- Inventing work experiences to fill gaps
- Proceeding to Architect phase without resume
