"""
Script 3 v2: Analysis with repetition support
"""
import sys
from pathlib import Path

try:
    import openpyxl
    import pandas as pd
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "--quiet", "--break-system-packages", "openpyxl", "pandas"])
    import openpyxl
    import pandas as pd

EXCEL_FILE = "medical_llm_disparity_experiments_v2.xlsx"

def main():
    print("\n📂 Loading data...")
    df = pd.read_excel(EXCEL_FILE, sheet_name="Experiments")
    total = len(df)
    judged = df['judge_overall'].notna().sum()
    print(f"   Loaded {total} rows total, {judged} judged.")
    if judged == 0:
        print("   No judged rows. Run script_2_judge.py first.")
        return
    df_j = df[df['judge_overall'].notna()].copy()

    print("\n📊 ANALYSIS 1: Hallucination Rate by Demographic")
    print("-" * 60)
    demo_stats = df_j.groupby('demographic').agg(
        total=('judge_overall', 'count'),
        hallucinations=('judge_overall', 'sum'),
        factual=('judge_factual', 'sum'),
        reasoning=('judge_reasoning', 'sum'),
        evidence=('judge_evidence', 'sum'),
    ).reindex(["Black woman", "Black man", "White woman", "White man"])
    demo_stats['overall_rate'] = (demo_stats['hallucinations'] / demo_stats['total'] * 100).round(1)
    demo_stats['factual_rate'] = (demo_stats['factual'] / demo_stats['total'] * 100).round(1)
    demo_stats['reasoning_rate'] = (demo_stats['reasoning'] / demo_stats['total'] * 100).round(1)
    demo_stats['evidence_rate'] = (demo_stats['evidence'] / demo_stats['total'] * 100).round(1)
    print(demo_stats.to_string())

    print("\n\n📊 ANALYSIS 2: Neutral vs Sensitive Question Sets")
    print("-" * 60)
    for qtype in ['neutral', 'sensitive']:
        subset = df_j[df_j['question_type'] == qtype]
        stats = subset.groupby('demographic').agg(
            n=('judge_overall', 'count'), hall=('judge_overall', 'sum'),
        ).reindex(["Black woman", "Black man", "White woman", "White man"])
        stats['rate'] = (stats['hall'] / stats['n'] * 100).round(1)
        print(f"\n  {qtype.upper()} set:")
        print(stats.to_string())

    print("\n\n📊 ANALYSIS 3: Hallucination Type (Neutral only)")
    print("-" * 60)
    neutral = df_j[df_j['question_type'] == 'neutral']
    nt = neutral.groupby('demographic').agg(
        n=('judge_overall', 'count'),
        factual_rate=('judge_factual', lambda x: round(x.sum()/len(x)*100, 1)),
        reasoning_rate=('judge_reasoning', lambda x: round(x.sum()/len(x)*100, 1)),
        evidence_rate=('judge_evidence', lambda x: round(x.sum()/len(x)*100, 1)),
    ).reindex(["Black woman", "Black man", "White woman", "White man"])
    print(nt.to_string())

    print("\n\n📊 ANALYSIS 4: Per-Question Disparity (Top 10)")
    print("-" * 60)
    q_demo = df_j.groupby(['question_id', 'topic', 'demographic'])['judge_overall'].mean().unstack(fill_value=0)
    q_demo['disparity'] = q_demo.max(axis=1) - q_demo.min(axis=1)
    q_demo = q_demo.sort_values('disparity', ascending=False)
    print(q_demo.head(10).round(2).to_string())

    if 'repetition' in df_j.columns:
        print("\n\n📊 ANALYSIS 5: Repetition Consistency")
        print("-" * 60)
        rep = df_j.groupby(['question_id', 'demographic']).agg(
            reps=('repetition', 'nunique'), hall=('judge_overall', 'sum'), n=('judge_overall', 'count'))
        print(f"  Always clean: {len(rep[rep['hall']==0])}")
        print(f"  Sometimes hallucinated: {len(rep[(rep['hall']>0)&(rep['hall']<rep['n'])])}")
        print(f"  Always hallucinated: {len(rep[rep['hall']==rep['n']])}")

    print("\n\n📊 ANALYSIS 6: Case Studies")
    print("-" * 60)
    for qid in df_j['question_id'].unique():
        q = df_j[df_j['question_id'] == qid]
        topic = q['topic'].iloc[0]
        rates = q.groupby('demographic')['judge_overall'].mean()
        if rates.max() > 0 and rates.min() == 0:
            mx = rates.idxmax()
            notes = q[q['judge_overall'] == 1]['judge_notes'].values
            nt = notes[0][:150] if len(notes) > 0 else ""
            print(f"\n  • {qid} ({topic}) — {mx} hallucinated, others clean")
            print(f"    Note: {nt}")

    print("\n\n💾 Saving analysis...")
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as w:
        demo_stats.to_excel(w, sheet_name='Analysis')
    print(f"✅ Saved to '{EXCEL_FILE}' (Analysis sheet)")
    print("\nNext: python3 script_4_charts.py")

if __name__ == "__main__":
    main()
