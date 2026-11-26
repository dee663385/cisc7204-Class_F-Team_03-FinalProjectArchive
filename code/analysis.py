"""Reproducible analysis for CISC7204 Class F Team 03.

Run from any directory with:
    python code/analysis.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "macao_tourism_gdp_clean.csv"
RESULT_DIR = ROOT / "results"
VISUAL_DIR = ROOT / "visuals"

COLORS = {
    "blue": "#0072B2",
    "orange": "#D55E00",
    "green": "#009E73",
    "purple": "#CC79A7",
    "amber": "#E69F00",
    "grey": "#6B7280",
    "light_grey": "#E5E7EB",
}
PERIOD_COLORS = {
    "Pre-pandemic (2000-2019)": COLORS["blue"],
    "Pandemic (2020-2022)": COLORS["orange"],
    "Recovery (2023-2024)": COLORS["purple"],
}


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["year"] = df["year"].astype(int)
    df = df.sort_values("year").reset_index(drop=True)
    return df


def validate_data(df: pd.DataFrame) -> None:
    assert len(df) == 25, "Expected 25 annual observations"
    assert df["year"].is_unique, "Year must be unique"
    assert not df[["arrivals", "gdp_pc"]].isna().any().any(), "Missing core values"
    assert df["year"].min() == 2000 and df["year"].max() == 2024
    assert df.loc[df["year"] == 2000, "arrivals_index"].iloc[0] == 100.0
    assert df.loc[df["year"] == 2000, "gdp_index"].iloc[0] == 100.0


def correlation_record(x: pd.Series, y: pd.Series) -> dict:
    pearson = stats.pearsonr(x, y)
    spearman = stats.spearmanr(x, y)
    return {
        "n": int(len(x)),
        "pearson": float(pearson.statistic),
        "pearson_p": float(pearson.pvalue),
        "spearman": float(spearman.statistic),
        "spearman_p": float(spearman.pvalue),
    }


def compute_correlations(df: pd.DataFrame) -> dict:
    pre = df[df["year"] < 2020]
    growth = df.dropna(subset=["arrivals_yoy", "gdp_yoy"])
    growth_pre = growth[growth["year"] < 2020]
    return {
        "full_levels": correlation_record(df["arrivals"], df["gdp_pc"]),
        "pre_pandemic_levels": correlation_record(pre["arrivals"], pre["gdp_pc"]),
        "full_growth": correlation_record(growth["arrivals_yoy"], growth["gdp_yoy"]),
        "pre_pandemic_growth": correlation_record(
            growth_pre["arrivals_yoy"], growth_pre["gdp_yoy"]
        ),
    }


def compute_summary(df: pd.DataFrame, correlations: dict) -> dict:
    row_2019 = df.loc[df["year"] == 2019].iloc[0]
    row_2020 = df.loc[df["year"] == 2020].iloc[0]
    row_2024 = df.loc[df["year"] == 2024].iloc[0]

    slope = float(
        np.polyfit(np.log(df["arrivals"]), np.log(df["gdp_pc"]), 1)[0]
    )
    arrivals_recovery = float(row_2024["arrivals"] / row_2019["arrivals"] * 100)
    gdp_recovery = float(row_2024["gdp_pc"] / row_2019["gdp_pc"] * 100)

    return {
        "window": [int(df["year"].min()), int(df["year"].max())],
        "n_years": int(len(df)),
        "arrivals_2019_m": round(float(row_2019["arrivals"]) / 1_000_000, 3),
        "arrivals_2020_m": round(float(row_2020["arrivals"]) / 1_000_000, 3),
        "arrivals_2024_m": round(float(row_2024["arrivals"]) / 1_000_000, 3),
        "gdp_2019": round(float(row_2019["gdp_pc"]), 2),
        "gdp_2020": round(float(row_2020["gdp_pc"]), 2),
        "gdp_2024": round(float(row_2024["gdp_pc"]), 2),
        "arrivals_drop_2019_2020_pct": round(
            float((row_2020["arrivals"] / row_2019["arrivals"] - 1) * 100), 2
        ),
        "gdp_drop_2019_2020_pct": round(
            float((row_2020["gdp_pc"] / row_2019["gdp_pc"] - 1) * 100), 2
        ),
        "arrivals_recovery_2024_vs_2019_pct": round(arrivals_recovery, 1),
        "gdp_recovery_2024_vs_2019_pct": round(gdp_recovery, 1),
        "recovery_gap_percentage_points": round(arrivals_recovery - gdp_recovery, 1),
        "log_log_slope": round(slope, 4),
        "ten_percent_arrivals_associated_gdp_pct": round(
            (1.10 ** slope - 1) * 100, 2
        ),
        "correlations": correlations,
    }


def save_analysis_table(correlations: dict) -> pd.DataFrame:
    labels = {
        "full_levels": "Full-sample levels",
        "pre_pandemic_levels": "Pre-pandemic levels",
        "full_growth": "Full-sample annual growth",
        "pre_pandemic_growth": "Pre-pandemic annual growth",
    }
    rows = []
    for key, label in labels.items():
        row = correlations[key]
        rows.append(
            {
                "analysis": label,
                "n": row["n"],
                "pearson_r": round(row["pearson"], 3),
                "pearson_p": row["pearson_p"],
                "spearman_rho": round(row["spearman"], 3),
                "spearman_p": row["spearman_p"],
            }
        )
    table = pd.DataFrame(rows)
    table.to_csv(RESULT_DIR / "analysis_summary.csv", index=False)
    return table


def add_source_note(fig, text: str) -> None:
    fig.text(0.01, 0.01, text, fontsize=8, color=COLORS["grey"], ha="left")


def plot_index_and_scatter(df: pd.DataFrame, correlations: dict) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), constrained_layout=True)

    ax = axes[0]
    ax.axvspan(2020, 2022, color="#EFE8D8", alpha=0.85, zorder=0)
    ax.plot(df["year"], df["arrivals_index"], marker="o", linewidth=2.2,
            color=COLORS["blue"], label="Overnight tourist arrivals")
    ax.plot(df["year"], df["gdp_index"], marker="o", linewidth=2.2,
            color=COLORS["orange"], label="Real GDP per capita")
    peak_arrivals = df.loc[df["arrivals_index"].idxmax()]
    peak_gdp = df.loc[df["gdp_index"].idxmax()]
    ax.scatter([peak_arrivals["year"], peak_gdp["year"]],
               [peak_arrivals["arrivals_index"], peak_gdp["gdp_index"]],
               s=70, color=["#FFFFFF", "#FFFFFF"], edgecolor=[COLORS["blue"], COLORS["orange"]],
               linewidth=2, zorder=5)
    ax.annotate("Tourism peak\n2019", (2019, peak_arrivals["arrivals_index"]),
                xytext=(-48, -23), textcoords="offset points", fontsize=8,
                color=COLORS["blue"], arrowprops={"arrowstyle": "-", "color": COLORS["blue"]})
    ax.annotate("GDP peak\n2013", (2013, peak_gdp["gdp_index"]),
                xytext=(-35, 22), textcoords="offset points", fontsize=8,
                color=COLORS["orange"], arrowprops={"arrowstyle": "-", "color": COLORS["orange"]})
    ax.set_title("Indexed paths diverge before the pandemic", fontweight="bold", loc="left")
    ax.set_xlabel("Year")
    ax.set_ylabel("Index (2000 = 100)")
    ax.grid(axis="y", color=COLORS["light_grey"], linewidth=0.8)
    ax.legend(frameon=False, fontsize=8, loc="upper left")

    ax = axes[1]
    for period, group in df.groupby("period", sort=False):
        ax.scatter(group["arrivals"] / 1_000_000, group["gdp_pc"] / 1_000,
                   s=42, color=PERIOD_COLORS[period], label=period, alpha=0.9,
                   edgecolor="white", linewidth=0.6)
    coef = np.polyfit(df["arrivals"] / 1_000_000, df["gdp_pc"] / 1_000, 1)
    x_line = np.linspace((df["arrivals"] / 1_000_000).min(),
                         (df["arrivals"] / 1_000_000).max(), 100)
    ax.plot(x_line, coef[0] * x_line + coef[1], color=COLORS["grey"],
            linewidth=1.5, linestyle="--", label="Linear fit")
    r = correlations["full_levels"]["pearson"]
    ax.set_title(f"Levels association: r = {r:.3f}, n = 25", fontweight="bold", loc="left")
    ax.set_xlabel("Overnight tourist arrivals (millions)")
    ax.set_ylabel("Real GDP per capita (thousand 2021 intl. dollars)")
    ax.grid(color=COLORS["light_grey"], linewidth=0.8)
    ax.legend(frameon=False, fontsize=8, loc="lower right")

    add_source_note(fig, "Source: UN Tourism via Our World in Data; World Bank NY.GDP.PCAP.PP.KD. Shaded band marks 2020-2022.")
    fig.savefig(VISUAL_DIR / "fig1_index_and_scatter.png", dpi=220)
    plt.close(fig)


def plot_growth(df: pd.DataFrame, correlations: dict) -> None:
    growth = df.dropna(subset=["arrivals_yoy", "gdp_yoy"]).copy()
    pre = growth[growth["year"] < 2020]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), constrained_layout=True)

    ax = axes[0]
    for period, group in growth.groupby("period", sort=False):
        ax.scatter(group["arrivals_yoy"], group["gdp_yoy"], s=45,
                   color=PERIOD_COLORS[period], label=period, alpha=0.9,
                   edgecolor="white", linewidth=0.6)
    row_2023 = growth.loc[growth["year"] == 2023].iloc[0]
    ax.annotate("2023 base effect\narrivals +472.7%", (row_2023["arrivals_yoy"], row_2023["gdp_yoy"]),
                xytext=(-140, 14), textcoords="offset points", fontsize=8,
                color=COLORS["purple"], arrowprops={"arrowstyle": "-", "color": COLORS["purple"]})
    r_full = correlations["full_growth"]["pearson"]
    ax.set_title(f"All annual changes: r = {r_full:.3f}, n = 24", fontweight="bold", loc="left")
    ax.set_xlim(-100, 520)
    ax.set_ylim(-80, 100)
    ax.axhline(0, color=COLORS["grey"], linewidth=0.8)
    ax.axvline(0, color=COLORS["grey"], linewidth=0.8)
    ax.set_xlabel("Arrivals growth (%)")
    ax.set_ylabel("GDP per capita growth (%)")
    ax.grid(color=COLORS["light_grey"], linewidth=0.8)
    ax.legend(frameon=False, fontsize=8, loc="upper left")

    ax = axes[1]
    ax.scatter(pre["arrivals_yoy"], pre["gdp_yoy"], s=45, color=COLORS["blue"],
               alpha=0.9, edgecolor="white", linewidth=0.6)
    coef = np.polyfit(pre["arrivals_yoy"], pre["gdp_yoy"], 1)
    x_line = np.linspace(pre["arrivals_yoy"].min(), pre["arrivals_yoy"].max(), 100)
    ax.plot(x_line, coef[0] * x_line + coef[1], color=COLORS["grey"],
            linewidth=1.5, linestyle="--", label="Linear fit")
    r_pre = correlations["pre_pandemic_growth"]["pearson"]
    ax.set_title(f"Pre-pandemic changes: r = {r_pre:.3f}, n = 19", fontweight="bold", loc="left")
    ax.axhline(0, color=COLORS["grey"], linewidth=0.8)
    ax.axvline(0, color=COLORS["grey"], linewidth=0.8)
    ax.set_xlabel("Arrivals growth (%)")
    ax.set_ylabel("GDP per capita growth (%)")
    ax.grid(color=COLORS["light_grey"], linewidth=0.8)
    ax.legend(frameon=False, fontsize=8, loc="upper left")

    add_source_note(fig, "Source: author calculations from UN Tourism/OWID and World Bank data. Growth uses year-on-year percent change; 2000 has no prior year.")
    fig.savefig(VISUAL_DIR / "fig2_yoy_growth.png", dpi=220)
    plt.close(fig)


def plot_recovery(summary: dict) -> None:
    labels = ["Overnight tourist\narrivals", "Real GDP\nper capita"]
    values = [
        summary["arrivals_recovery_2024_vs_2019_pct"],
        summary["gdp_recovery_2024_vs_2019_pct"],
    ]
    fig, ax = plt.subplots(figsize=(7.2, 4.8), constrained_layout=True)
    bars = ax.bar(labels, values, color=[COLORS["blue"], COLORS["orange"]], width=0.58)
    ax.axhline(100, color=COLORS["grey"], linestyle="--", linewidth=1.2)
    ax.text(1.34, 101.5, "2019 baseline = 100%", ha="right", va="bottom", fontsize=8, color=COLORS["grey"])
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 2.0, f"{value:.1f}%",
                ha="center", va="bottom", fontsize=11, fontweight="bold", color="#203F40")
    ax.set_ylim(0, 110)
    ax.set_ylabel("2024 level as % of 2019")
    ax.set_title("Recovery remains incomplete", fontweight="bold", loc="left")
    ax.text(0.5, 72,
            f"Gap = {summary['recovery_gap_percentage_points']:.1f} percentage points",
            ha="center", fontsize=10, color=COLORS["grey"])
    ax.grid(axis="y", color=COLORS["light_grey"], linewidth=0.8)
    add_source_note(fig, "Source: UN Tourism via Our World in Data; World Bank. Both series normalised to their own 2019 level.")
    fig.savefig(VISUAL_DIR / "fig3_recovery_2024_vs_2019.png", dpi=220)
    plt.close(fig)


def plot_correlation_comparison(correlations: dict) -> None:
    labels = ["Full levels", "Pre-pandemic\nlevels", "Full growth", "Pre-pandemic\ngrowth"]
    keys = ["full_levels", "pre_pandemic_levels", "full_growth", "pre_pandemic_growth"]
    pearson = [correlations[key]["pearson"] for key in keys]
    spearman = [correlations[key]["spearman"] for key in keys]
    x = np.arange(len(labels))
    width = 0.34

    fig, ax = plt.subplots(figsize=(9.2, 4.8), constrained_layout=True)
    bars1 = ax.bar(x - width / 2, pearson, width, label="Pearson r", color=COLORS["blue"])
    bars2 = ax.bar(x + width / 2, spearman, width, label="Spearman rho", color=COLORS["orange"])
    for bars in (bars1, bars2):
        for bar in bars:
            value = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, value + 0.02,
                    f"{value:.3f}", ha="center", va="bottom", fontsize=8, color="#203F40")
    ax.set_xticks(x, labels)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("Correlation coefficient")
    ax.set_title("Association weakens when the shared trend is removed", fontweight="bold", loc="left")
    ax.grid(axis="y", color=COLORS["light_grey"], linewidth=0.8)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    add_source_note(fig, "Source: author calculations from the 25-year Macao annual dataset. All coefficients are descriptive.")
    fig.savefig(VISUAL_DIR / "fig4_correlation_comparison.png", dpi=220)
    plt.close(fig)


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    VISUAL_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data()
    validate_data(df)
    correlations = compute_correlations(df)
    summary = compute_summary(df, correlations)
    table = save_analysis_table(correlations)

    (RESULT_DIR / "correlation_results.json").write_text(
        json.dumps(correlations, indent=2), encoding="utf-8"
    )
    (RESULT_DIR / "summary_stats.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    plot_index_and_scatter(df, correlations)
    plot_growth(df, correlations)
    plot_recovery(summary)
    plot_correlation_comparison(correlations)

    print(table.to_string(index=False))
    print(f"Log-log slope: {summary['log_log_slope']:.4f}")
    print(
        "2024 recovery: arrivals "
        f"{summary['arrivals_recovery_2024_vs_2019_pct']:.1f}% vs GDP "
        f"{summary['gdp_recovery_2024_vs_2019_pct']:.1f}%"
    )


if __name__ == "__main__":
    main()
