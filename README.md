# Intersectional Demographic Disparities in Medical LLM Hallucinations

An exploratory study examining whether GPT-4o-mini exhibits demographic disparities in the frequency and type of hallucinations when generating clinical responses.

## Key Findings

| Demographic | Hallucination Rate | Neutral Set Only |
|---|---|---|
| Black woman | 10.0% | 8.3% |
| Black man | 5.0% | 0.0% |
| White woman | 5.0% | 0.0% |
| White man | 0.0% | 0.0% |

1. Clean intersectional gradient from White man (0%) to Black woman (10%)
2. On neutral questions, ONLY Black women hallucinated (8.3% vs 0%)
3. Model fabricated a false racial association with pneumothorax for Black women

## Methodology

- 20 clinical vignettes (12 neutral + 8 sensitive)
- 4 demographic perturbations = 80 prompts
- Subject: GPT-4o-mini | Judge: GPT-4o
- Taxonomy: factual / reasoning / evidence (MedHalu)

## Structure

- scripts/ - Python pipeline
- data/ - Dataset (80 responses + ratings)
- charts/ - Visualizations
- presentation/ - PowerPoint + script
- report/ - English + Chinese report
- proposal/ - Original proposal

## References

- Agarwal et al. (2024) MedHalu
- Rawat et al. (2024) DiversityMedQA
- Pfohl et al. (2024) EquityMedQA
- Kim et al. (2025) Medical Hallucination
- Omar et al. (2025) Racial Bias in AI
