"""
Script 4 v2: Generate charts from v2 Excel (with repetition support)
Ocean Professional palette
"""
import sys
from pathlib import Path

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "--quiet", "--break-system-packages",
                           "pandas", "matplotlib", "openpyxl"])
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap

EXCEL_FILE = "medical_llm_disparity_experiments_v2.xlsx"
OUT = Path("charts")
OUT.mkdir(exist_ok=True)

NAVY = "#0F4C75"
TEAL = "#3282B8"
SEAFOAM = "#86C5DA"
MINT = "#00A896"
DARK = "#1B2A41"
GREY = "#5A6F84"
LIGHT = "#F5F9FC"

DEMO_COLORS = {"Black woman": NAVY, "Black man": TEAL, "White woman": SEAFOAM, "White man": "#C8DEE8"}

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

def main():
    print("📂 Loading data...")
    df = pd.read_excel(EXCEL_FILE, sheet_name="Experiments")
    df_j = df[df['judge_overall'].notna()].copy()
    n_total = len(df_j)
    print(f"   {n_total} judged rows loaded.")
    groups = ["Black woman", "Black man", "White woman", "White man"]

    # Chart 1: Overall
    print("📊 Chart 1: Overall Disparity...")
    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor='white')
    rates = [df_j[df_j['demographic']==g]['judge_overall'].mean()*100 for g in groups]
    ns = [len(df_j[df_j['demographic']==g]) for g in groups]
    bars = ax.bar(groups, rates, color=[DEMO_COLORS[g] for g in groups], edgecolor=DARK, linewidth=1, width=0.62)
    for bar, rate, n in zip(bars, rates, ns):
        ax.text(bar.get_x()+bar.get_width()/2., bar.get_height()+0.3,
                f"{rate:.1f}%\n(n={n})", ha='center', va='bottom', fontsize=12, fontweight='bold', color=DARK)
    ax.set_ylabel("Hallucination Rate (%)", fontsize=13, fontweight='bold')
    ax.set_title(f"Hallucination Rate by Patient Demographic\n(All {len(df['question_id'].unique())} questions, GPT-4o-mini, {n_total} responses)",
                 fontsize=14, fontweight='bold', color=DARK, pad=12)
    ax.set_ylim(0, max(rates)*1.4+1)
    ax.grid(axis='y', alpha=0.25, linestyle='--')
    plt.tight_layout()
    plt.savefig(OUT/"chart_1_overall_disparity.png", dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✓ Saved chart_1")

    # Chart 2: Neutral vs Sensitive
    print("📊 Chart 2: Neutral vs Sensitive...")
    fig, ax = plt.subplots(figsize=(11, 5.8), facecolor='white')
    neutral_rates = [df_j[(df_j['demographic']==g)&(df_j['question_type']=='neutral')]['judge_overall'].mean()*100 for g in groups]
    sensitive_rates = [df_j[(df_j['demographic']==g)&(df_j['question_type']=='sensitive')]['judge_overall'].mean()*100 for g in groups]
    x = np.arange(len(groups)); w = 0.38
    b1 = ax.bar(x-w/2, neutral_rates, w, label='Neutral questions', color=NAVY, edgecolor=DARK, linewidth=1)
    b2 = ax.bar(x+w/2, sensitive_rates, w, label='Sensitive questions', color=MINT, edgecolor=DARK, linewidth=1)
    for bars in [b1, b2]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x()+bar.get_width()/2., h+0.2, f"{h:.1f}%", ha='center', va='bottom', fontsize=11, fontweight='bold', color=DARK)
    ax.set_ylabel("Hallucination Rate (%)", fontsize=13, fontweight='bold')
    ax.set_title("Neutral vs Sensitive Question Sets\nNeutral set isolates pure demographic bias", fontsize=14, fontweight='bold', color=DARK, pad=12)
    ax.set_xticks(x); ax.set_xticklabels(groups, fontsize=11)
    ax.set_ylim(0, max(max(neutral_rates), max(sensitive_rates))*1.3+1)
    ax.grid(axis='y', alpha=0.25, linestyle='--')
    ax.legend(fontsize=11, frameon=True, facecolor='white')
    plt.tight_layout()
    plt.savefig(OUT/"chart_2_neutral_vs_sensitive.png", dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✓ Saved chart_2")

    # Chart 3: Type breakdown (neutral)
    print("📊 Chart 3: Hallucination Types...")
    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor='white')
    neutral = df_j[df_j['question_type']=='neutral']
    fact_r = [neutral[neutral['demographic']==g]['judge_factual'].mean()*100 for g in groups]
    reas_r = [neutral[neutral['demographic']==g]['judge_reasoning'].mean()*100 for g in groups]
    evid_r = [neutral[neutral['demographic']==g]['judge_evidence'].mean()*100 for g in groups]
    x = np.arange(len(groups)); w = 0.27
    ax.bar(x-w, fact_r, w, label='Factual', color=NAVY, edgecolor=DARK, linewidth=0.8)
    ax.bar(x, reas_r, w, label='Reasoning', color=TEAL, edgecolor=DARK, linewidth=0.8)
    ax.bar(x+w, evid_r, w, label='Evidence', color=MINT, edgecolor=DARK, linewidth=0.8)
    for i, (f, r, e) in enumerate(zip(fact_r, reas_r, evid_r)):
        for val, offset in [(f, -w), (r, 0), (e, w)]:
            if val > 0:
                ax.text(i+offset, val+0.2, f"{val:.1f}%", ha='center', va='bottom', fontsize=10, fontweight='bold', color=DARK)
    ax.set_ylabel("Hallucination Rate (%)", fontsize=13, fontweight='bold')
    ax.set_title("Hallucination Type Breakdown (Neutral set only)", fontsize=14, fontweight='bold', color=DARK, pad=12)
    ax.set_xticks(x); ax.set_xticklabels(groups, fontsize=11)
    ax.set_ylim(0, max(max(fact_r), max(reas_r), max(evid_r))*1.4+1)
    ax.grid(axis='y', alpha=0.25, linestyle='--')
    ax.legend(fontsize=10.5, frameon=True, title='Hallucination Type', facecolor='white')
    plt.tight_layout()
    plt.savefig(OUT/"chart_3_hallucination_types.png", dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✓ Saved chart_3")

    # Chart 4: Heatmap
    print("📊 Chart 4: Heatmap...")
    fig, ax = plt.subplots(figsize=(7.5, 5.2), facecolor='white')
    cmap = LinearSegmentedColormap.from_list("ocean", [LIGHT, SEAFOAM, TEAL, NAVY], N=256)
    bw = df_j[df_j['demographic']=='Black woman']['judge_overall'].mean()*100
    bm = df_j[df_j['demographic']=='Black man']['judge_overall'].mean()*100
    ww = df_j[df_j['demographic']=='White woman']['judge_overall'].mean()*100
    wm = df_j[df_j['demographic']=='White man']['judge_overall'].mean()*100
    data = np.array([[bw, bm], [ww, wm]])
    vmax = max(bw, bm, ww, wm) if max(bw, bm, ww, wm) > 0 else 10
    im = ax.imshow(data, cmap=cmap, vmin=0, vmax=vmax, aspect='auto')
    n_per = len(df_j)//4
    for i in range(2):
        for j in range(2):
            v = data[i, j]
            tc = "white" if v >= vmax*0.6 else DARK
            ax.text(j, i, f"{v:.1f}%\n(n={n_per})", ha='center', va='center', fontsize=18, fontweight='bold', color=tc)
    ax.set_xticks([0,1]); ax.set_yticks([0,1])
    ax.set_xticklabels(["woman", "man"], fontsize=13)
    ax.set_yticklabels(["Black", "White"], fontsize=13)
    ax.set_xlabel("Gender", fontsize=13, fontweight='bold')
    ax.set_ylabel("Race", fontsize=13, fontweight='bold')
    ax.set_title("Intersectional Hallucination Rate (Race × Gender)", fontsize=13, fontweight='bold', color=DARK, pad=12)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04).set_label("Hallucination Rate (%)", fontsize=11, fontweight='bold')
    ax.tick_params(top=False, right=False)
    plt.tight_layout()
    plt.savefig(OUT/"chart_4_intersectional_heatmap.png", dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✓ Saved chart_4")

    print(f"\n{'='*60}")
    print("  ALL CHARTS GENERATED!")
    print(f"{'='*60}")
    print(f"  📁 Folder: {OUT.resolve()}")
    print(f"  📊 4 PNG files at 300 DPI")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
