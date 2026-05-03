"""
Script 4: Chart Generator
================================
Generates presentation-ready PNG charts from your data.

USAGE:
    Run after script_3_analysis.py
    python3 script_4_charts.py

OUTPUTS (PNG files, 300 DPI, ready for slides):
    - chart_1_overall_disparity.png
    - chart_2_neutral_vs_sensitive.png
    - chart_3_hallucination_types.png
    - chart_4_intersectional_heatmap.png

ESTIMATED TIME: < 1 minute
"""

import sys
from pathlib import Path

def install_dependencies():
    try:
        import pandas
        import matplotlib
        import openpyxl
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install",
                               "--quiet", "pandas", "matplotlib", "openpyxl"])

install_dependencies()

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

EXCEL_FILE = "medical_llm_disparity_experiments.xlsx"
OUTPUT_DIR = Path("charts")
OUTPUT_DIR.mkdir(exist_ok=True)

# Color palette (colorblind-safe, professional)
COLORS = {
    "Black woman": "#C44E52",   # Red
    "Black man": "#DD8452",     # Orange  
    "White woman": "#4C72B0",   # Blue
    "White man": "#55A868",     # Green
}

DEMO_ORDER = ["Black woman", "Black man", "White woman", "White man"]

# Load data
print("📂 Loading data...")
df = pd.read_excel(EXCEL_FILE, sheet_name="Experiments")
judged = df[df["judge_overall"].notna()].copy()

if len(judged) == 0:
    print("⚠️  No data to chart. Run script_2_judge.py first.")
    sys.exit(0)

for col in ["judge_factual", "judge_reasoning", "judge_evidence", "judge_overall"]:
    judged[col] = pd.to_numeric(judged[col], errors="coerce").fillna(0).astype(int)

judged["demographic"] = judged["race"] + " " + judged["gender"]

# ============================================================
# CHART 1: Overall Hallucination Rate by Demographic
# ============================================================
print("📊 Generating Chart 1: Overall Disparity...")

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

overall = judged.groupby("demographic").agg(
    rate=("judge_overall", lambda x: x.sum() / len(x) * 100),
    n=("judge_overall", "count")
).reset_index()

# Sort by predefined order
overall = overall.set_index("demographic").reindex(DEMO_ORDER).reset_index()

bars = ax.bar(overall["demographic"], overall["rate"],
              color=[COLORS[d] for d in overall["demographic"]],
              edgecolor="black", linewidth=0.8)

# Value labels on top
for bar, rate, n in zip(bars, overall["rate"], overall["n"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f"{rate:.1f}%\n(n={n})",
            ha="center", va="bottom", fontsize=10, fontweight="bold")

ax.set_ylabel("Hallucination Rate (%)", fontsize=12, fontweight="bold")
ax.set_title("Hallucination Rate by Patient Demographic\n(All 20 questions, GPT-4o-mini)",
             fontsize=13, fontweight="bold", pad=15)
ax.set_ylim(0, max(overall["rate"]) * 1.3 + 5)
ax.grid(axis="y", alpha=0.3, linestyle="--")
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "chart_1_overall_disparity.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"   ✓ Saved chart_1_overall_disparity.png")

# ============================================================
# CHART 2: Neutral vs Sensitive Comparison
# ============================================================
print("📊 Generating Chart 2: Neutral vs Sensitive...")

fig, ax = plt.subplots(figsize=(11, 6), dpi=300)

by_set = judged.groupby(["set_type", "demographic"]).agg(
    rate=("judge_overall", lambda x: x.sum() / len(x) * 100)
).reset_index()

x = np.arange(len(DEMO_ORDER))
width = 0.35

neutral_rates = []
sensitive_rates = []
for d in DEMO_ORDER:
    n_row = by_set[(by_set["set_type"] == "neutral") & (by_set["demographic"] == d)]
    s_row = by_set[(by_set["set_type"] == "sensitive") & (by_set["demographic"] == d)]
    neutral_rates.append(n_row["rate"].iloc[0] if len(n_row) > 0 else 0)
    sensitive_rates.append(s_row["rate"].iloc[0] if len(s_row) > 0 else 0)

bars1 = ax.bar(x - width/2, neutral_rates, width, label="Neutral questions (n=12)",
               color="#4C72B0", edgecolor="black", linewidth=0.8)
bars2 = ax.bar(x + width/2, sensitive_rates, width, label="Sensitive questions (n=8)",
               color="#C44E52", edgecolor="black", linewidth=0.8)

for bars in [bars1, bars2]:
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.5,
                f"{h:.0f}%", ha="center", va="bottom", fontsize=9)

ax.set_xticks(x)
ax.set_xticklabels(DEMO_ORDER)
ax.set_ylabel("Hallucination Rate (%)", fontsize=12, fontweight="bold")
ax.set_title("Hallucination Rate: Neutral vs Sensitive Question Sets\nNeutral set isolates pure demographic bias",
             fontsize=13, fontweight="bold", pad=15)
ax.legend(loc="upper right", fontsize=10)
ax.grid(axis="y", alpha=0.3, linestyle="--")
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "chart_2_neutral_vs_sensitive.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"   ✓ Saved chart_2_neutral_vs_sensitive.png")

# ============================================================
# CHART 3: Hallucination Types Breakdown (Neutral set)
# ============================================================
print("📊 Generating Chart 3: Hallucination Types...")

fig, ax = plt.subplots(figsize=(11, 6), dpi=300)

neutral = judged[judged["set_type"] == "neutral"]

types_data = []
for d in DEMO_ORDER:
    subset = neutral[neutral["demographic"] == d]
    if len(subset) == 0:
        continue
    n = len(subset)
    types_data.append({
        "demographic": d,
        "factual": subset["judge_factual"].sum() / n * 100,
        "reasoning": subset["judge_reasoning"].sum() / n * 100,
        "evidence": subset["judge_evidence"].sum() / n * 100,
    })

types_df = pd.DataFrame(types_data)

x = np.arange(len(types_df))
width = 0.27

bars1 = ax.bar(x - width, types_df["factual"], width,
               label="Factual", color="#E76F51", edgecolor="black", linewidth=0.6)
bars2 = ax.bar(x, types_df["reasoning"], width,
               label="Reasoning", color="#F4A261", edgecolor="black", linewidth=0.6)
bars3 = ax.bar(x + width, types_df["evidence"], width,
               label="Evidence", color="#2A9D8F", edgecolor="black", linewidth=0.6)

ax.set_xticks(x)
ax.set_xticklabels(types_df["demographic"])
ax.set_ylabel("Hallucination Rate (%)", fontsize=12, fontweight="bold")
ax.set_title("Hallucination Type Breakdown by Demographic\n(Neutral question set only — n=12 per demographic)",
             fontsize=13, fontweight="bold", pad=15)
ax.legend(title="Hallucination Type", loc="upper right", fontsize=10)
ax.grid(axis="y", alpha=0.3, linestyle="--")
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "chart_3_hallucination_types.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"   ✓ Saved chart_3_hallucination_types.png")

# ============================================================
# CHART 4: Intersectional Heatmap (Race × Gender)
# ============================================================
print("📊 Generating Chart 4: Intersectional Heatmap...")

fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

# Build 2x2 matrix: rows = Race (Black, White), cols = Gender (woman, man)
matrix_data = np.zeros((2, 2))
counts = np.zeros((2, 2), dtype=int)

races = ["Black", "White"]
genders = ["woman", "man"]

for i, race in enumerate(races):
    for j, gender in enumerate(genders):
        subset = judged[(judged["race"] == race) & (judged["gender"] == gender)]
        if len(subset) > 0:
            matrix_data[i, j] = subset["judge_overall"].sum() / len(subset) * 100
            counts[i, j] = len(subset)

im = ax.imshow(matrix_data, cmap="Reds", aspect="auto", vmin=0, vmax=max(matrix_data.max(), 1))

# Annotations
for i in range(2):
    for j in range(2):
        text_color = "white" if matrix_data[i, j] > matrix_data.max() * 0.6 else "black"
        ax.text(j, i, f"{matrix_data[i, j]:.1f}%\n(n={counts[i, j]})",
                ha="center", va="center", fontsize=14, fontweight="bold",
                color=text_color)

ax.set_xticks([0, 1])
ax.set_xticklabels(genders, fontsize=12)
ax.set_yticks([0, 1])
ax.set_yticklabels(races, fontsize=12)
ax.set_xlabel("Gender", fontsize=12, fontweight="bold")
ax.set_ylabel("Race", fontsize=12, fontweight="bold")
ax.set_title("Intersectional Hallucination Rate (Race × Gender)\nAll questions",
             fontsize=13, fontweight="bold", pad=15)

cbar = plt.colorbar(im, ax=ax)
cbar.set_label("Hallucination Rate (%)", fontsize=11)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "chart_4_intersectional_heatmap.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"   ✓ Saved chart_4_intersectional_heatmap.png")

# ============================================================
# Done
# ============================================================
print("\n" + "="*60)
print("  ALL CHARTS GENERATED!")
print("="*60)
print(f"  📁 Folder: {OUTPUT_DIR.absolute()}")
print(f"  📊 4 PNG files at 300 DPI (presentation quality)")
print("="*60)
print("\nThese charts are ready to drop into your slides.")
print("Suggested placement:")
print("  - Slide 7 (Results 1):  chart_1 + chart_4")
print("  - Slide 8 (Results 2):  chart_2 + chart_3")
