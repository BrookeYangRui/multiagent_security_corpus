#!/usr/bin/env python3
"""Render growth of the broad pre-taxonomy multi-agent security corpus."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "corpus/sets/02_broad_included/yearly_distribution.csv"
OUTPUT = ROOT / "reports/figures"
SERIES = ["peer_reviewed", "non_peer_or_unverified"]
LABELS = {
    "peer_reviewed": "Peer-reviewed",
    "non_peer_or_unverified": "Non-peer or unverified",
}
COLORS = {
    "peer_reviewed": "#2F7D6D",
    "non_peer_or_unverified": "#D98B3A",
}


def read_years() -> list[dict[str, int]]:
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        source = list(csv.DictReader(handle))
    rows = []
    for row in source:
        rows.append(
            {
                "year": int(row["year"]),
                "total": int(row["total"]),
                "peer_reviewed": int(row["peer_reviewed"]),
                "non_peer_or_unverified": int(row["non_peer_or_unverified"]),
                "cumulative": int(row["cumulative_total"]),
            }
        )
    return rows


def main() -> None:
    rows = read_years()
    years = [row["year"] for row in rows]
    year_labels = [f"{year}*" if year == 2026 else str(year) for year in years]

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titleweight": "bold",
            "axes.edgecolor": "#B8B8B8",
            "axes.labelcolor": "#333333",
            "xtick.color": "#444444",
            "ytick.color": "#444444",
        }
    )
    figure, (annual, cumulative) = plt.subplots(
        2,
        1,
        figsize=(10.5, 8),
        gridspec_kw={"height_ratios": [2.2, 1], "hspace": 0.35},
    )
    figure.patch.set_facecolor("white")
    figure.suptitle(
        "Growth of the Broad Multi-Agent Security Literature Frame",
        fontsize=18,
        fontweight="bold",
        x=0.08,
        ha="left",
        y=0.985,
    )
    figure.text(
        0.08,
        0.947,
        "325 deduplicated works before strict taxonomy screening",
        fontsize=10.5,
        color="#555555",
    )

    bottoms = [0] * len(rows)
    for series in SERIES:
        values = [row[series] for row in rows]
        annual.bar(
            years,
            values,
            bottom=bottoms,
            width=0.68,
            color=COLORS[series],
            label=LABELS[series],
            edgecolor="white",
            linewidth=0.7,
        )
        bottoms = [bottom + value for bottom, value in zip(bottoms, values)]
    for year, total in zip(years, bottoms):
        annual.text(
            year,
            total + 4,
            str(total),
            ha="center",
            va="bottom",
            fontweight="bold",
        )
    annual.set_title("New broad-screen works by year", loc="left", fontsize=12)
    annual.set_ylabel("Works")
    annual.set_xticks(years, year_labels)
    annual.set_ylim(0, max(bottoms) * 1.18)
    annual.grid(axis="y", color="#E5E5E5", linewidth=0.8)
    annual.set_axisbelow(True)
    annual.spines[["top", "right"]].set_visible(False)
    annual.legend(frameon=False, loc="upper left", ncols=2)

    cumulative_values = [row["cumulative"] for row in rows]
    cumulative.plot(
        years,
        cumulative_values,
        color="#252525",
        linewidth=2.4,
        marker="o",
        markersize=6,
    )
    cumulative.fill_between(years, cumulative_values, color="#4C78A8", alpha=0.12)
    for year, value in zip(years, cumulative_values):
        cumulative.text(
            year,
            value + 9,
            str(value),
            ha="center",
            va="bottom",
            fontweight="bold",
        )
    cumulative.set_title("Cumulative broad-screen size", loc="left", fontsize=12)
    cumulative.set_ylabel("Works")
    cumulative.set_xticks(years, year_labels)
    cumulative.set_ylim(0, max(cumulative_values) * 1.2)
    cumulative.grid(axis="y", color="#E5E5E5", linewidth=0.8)
    cumulative.set_axisbelow(True)
    cumulative.spines[["top", "right"]].set_visible(False)

    figure.text(
        0.08,
        0.018,
        "* 2026 is a partial year through the frozen literature cutoff, 2026-07-01. Broad-screen counts are not strict-core decisions.",
        fontsize=9,
        color="#555555",
    )
    OUTPUT.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        OUTPUT / "broad_corpus_growth_by_year.png", dpi=200, bbox_inches="tight"
    )
    figure.savefig(OUTPUT / "broad_corpus_growth_by_year.svg", bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
