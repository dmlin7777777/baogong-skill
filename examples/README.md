# Examples

Test prompts and expected behaviors for 包公.skill.

Each `.md` file contains a prompt and the expected routing/behavior.

## Scenarios

| File | Scenario | Tests |
|------|----------|-------|
| `scenario_a_jd_resume.md` | JD + resume provided | Full pipeline routing, bullet format compliance |
| `scenario_b_resume_only.md` | Resume only, no JD | Story-library polish mode |
| `scenario_c_jd_only.md` | JD only, no resume | Advisory output, gap analysis |
| `scenario_e_fabrication.md` | User asks to fabricate | Hard refusal + explanation |

## How to use

Copy the prompt from any example file and paste it into a Claude Code session with the baogong-skill skill loaded.
