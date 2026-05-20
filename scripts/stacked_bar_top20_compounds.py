from pathlib import Path
from textwrap import fill

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------- 1) Load data ----------
# Preferred clean dataset name. The legacy filename is kept as a fallback
# so the script still runs before/while files are being renamed.
preferred_file = Path("rafflesia_lcms_group_average_feature_table.xlsx")
legacy_file = Path("RaffseedG5k.xlsx")

if preferred_file.exists():
    file_path = preferred_file
elif legacy_file.exists():
    file_path = legacy_file
else:
    raise FileNotFoundError(
        "Input Excel file not found. Expected either "
        "'rafflesia_lcms_group_average_feature_table.xlsx' or 'RaffseedG5k.xlsx'."
    )

df = pd.ExcelFile(file_path).parse(0)   # first sheet

# ---------- 2) Keep group-average columns + Feature_Label ----------
df.columns = df.columns.str.strip()
ave_cols = [c for c in df.columns if c.lower().startswith("ave")]
df = df[["Feature_Label"] + ave_cols].copy()

# ---------- 3) Replace negatives with 0 ----------
df[ave_cols] = df[ave_cols].clip(lower=0)

# ---------- 4) Extract compound names (after the '|') ----------
df["Compound"] = df["Feature_Label"].astype(str).str.split("|").str[-1].str.strip()

# ---------- 5) Collapse duplicates by averaging intensities ----------
# (mean across rows for each compound name)
compound_avg = df.groupby("Compound", as_index=True)[ave_cols].mean()

# ---------- 6) Rank compounds and keep top 20 ----------
# Default: rank by overall abundance across all groups
overall = compound_avg.sum(axis=1)
top20_names = overall.nlargest(20).index

# If you instead want to rank by RAFFSEED only, uncomment:
# raff_col = [c for c in ave_cols if "raffseed" in c.lower()][0]
# top20_names = compound_avg[raff_col].nlargest(20).index

top20 = compound_avg.loc[top20_names]

# ---------- 7) Total Sum Scaling (normalize each group column to sum=1) ----------
tss = top20.div(top20.sum(axis=0), axis=1)

# (Optional) choose a specific order for the x-axis:
# order = ["averaffseed","aveRaffbudspec","aveinfectedILO","aveUNinfectedILO",
#          "aveuninfecraffspec-stemleaf","avenonhostILO"]
# cols_to_plot = [c for c in order if c in tss.columns]
# Otherwise, keep whatever columns exist in the file:
cols_to_plot = list(tss.columns)

# ---------- 8) Plot stacked bar ----------
fig, ax = plt.subplots(figsize=(15, 7))
tss[cols_to_plot].T.plot(kind="bar", stacked=True, ax=ax, width=0.85, colormap="tab20")

ax.set_ylabel("Normalized Abundance (Total Sum Scaling)")
ax.set_xlabel("Sample Group")
ax.set_title("Top 20 Compound Names across Rafflesia and Host Tissues")

# Tilt x-axis labels for readability.
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Wrap long compound names in the legend so the legend box is less cursed.
handles, labels = ax.get_legend_handles_labels()
wrapped_labels = [fill(label, width=42, break_long_words=False) for label in labels]
ax.legend(
    handles,
    wrapped_labels,
    title="Compound Name",
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    fontsize=7,
    title_fontsize=8,
    frameon=True,
    borderaxespad=0.0,
    handlelength=1.2,
    labelspacing=0.55,
)

# Fixed margins keep the plot area and legend layout stable across exports.
fig.subplots_adjust(left=0.08, right=0.66, bottom=0.26, top=0.88)

# Save figure (PNG/SVG)
fig.savefig("top20_compounds_stacked_TSS.png", dpi=300, bbox_inches="tight")
fig.savefig("top20_compounds_stacked_TSS.svg", bbox_inches="tight")

# ---------- 9) Export the numbers used in the figure ----------
# Raw means (averaged duplicates) for the top 20:
top20.to_csv("top20_compounds_raw_means.csv")
# TSS-normalized values used for plotting:
tss.to_csv("top20_compounds_TSS.csv")

print(
    "Saved: top20_compounds_stacked_TSS.png/.svg, "
    "top20_compounds_raw_means.csv, top20_compounds_TSS.csv"
)

plt.show()
plt.close(fig)
