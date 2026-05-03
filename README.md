# Intersectional Demographic Disparities in Medical LLM Hallucinations

A two-phase study examining demographic disparities in GPT-4o-mini hallucinations across clinical responses.

## Phase 1: Pilot (n=80, 20 questions)

| Demographic | Rate |
|---|---|
| Black woman | 10.0% |
| Black man | 5.0% |
| White woman | 5.0% |
| White man | 0.0% |

## Phase 2: Full Study (n=600, 50 questions x 3 reps)

| Demographic | Overall | Neutral | Sensitive |
|---|---|---|---|
| Black man | 10.0% | 5.6% | 16.7% |
| White man | 8.0% | 4.4% | 13.3% |
| Black woman | 4.0% | 2.2% | 6.7% |
| White woman | 3.3% | 3.3% | 3.3% |

## Key Findings

1. Demographic disparities in hallucination confirmed across both phases
2. Phase 1 suggested intersectional gradient; Phase 2 revealed gender-based pattern (men 2-3x > women)
3. Sensitive questions amplify disparities: 5x gap (Black man 16.7% vs White woman 3.3%)
4. Small-sample bias audits (n<100) can produce unstable conclusions

## Methodology

- Self-authored clinical vignettes (neutral + sensitive split)
- Counterfactual demographic perturbation (Black/White x woman/man)
- Subject model: GPT-4o-mini | Judge model: GPT-4o
- Hallucination taxonomy: factual / reasoning / evidence (MedHalu)

## Structure

- phase1_pilot/ - Pilot study data and charts (n=80)
- phase2_full/ - Full study data and charts (n=600)

## References

- Agarwal et al. (2024) MedHalu
- Rawat et al. (2024) DiversityMedQA
- Pfohl et al. (2024) EquityMedQA
- Kim et al. (2025) Medical Hallucination in Foundation Models
- Omar et al. (2025) Racial Bias in AI-mediated Psychiatric Diagnosis
