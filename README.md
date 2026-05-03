# Intersectional Demographic Disparities in Medical LLM Hallucinations

A two-phase study examining demographic disparities in GPT-4o-mini hallucinations.

## Phase 1: Pilot (n=80)

| Demographic | Rate |
|---|---|
| Black woman | 10.0% |
| Black man | 5.0% |
| White woman | 5.0% |
| White man | 0.0% |

## Phase 2: Full Study (n=600)

| Demographic | Overall | Neutral | Sensitive |
|---|---|---|---|
| Black man | 10.0% | 5.6% | 16.7% |
| White man | 8.0% | 4.4% | 13.3% |
| Black woman | 4.0% | 2.2% | 6.7% |
| White woman | 3.3% | 3.3% | 3.3% |

## Key Findings

1. Demographic disparities confirmed across both phases
2. Phase 1: intersectional gradient. Phase 2: gender-based pattern (men 2-3x > women)
3. Sensitive questions amplify disparities: 5x gap (Black man 16.7% vs White woman 3.3%)
4. Small-sample bias audits (n<100) can produce unstable conclusions

## Structure

- phase1_pilot/ - Pilot (n=80): scripts, data, charts
- phase2_full/ - Full study (n=600): scripts, data, charts
- presentation/ - Slides + speaker script
- report/ - English + Chinese report
- proposal/ - Original proposal
