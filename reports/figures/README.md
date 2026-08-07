# Corpus Figures

`corpus_growth_by_year.png` and `corpus_growth_by_year.svg` visualize all 142
canonical multi-agent security works by publication year and primary category.
The upper panel reports annual additions; the lower panel reports cumulative
corpus size. The 2026 point is explicitly marked as a partial year through the
frozen `2026-07-01` cutoff.

Regenerate the figure after rebuilding final exports:

```bash
python3 scripts/build_final_exports.py
python3 scripts/plot_yearly_growth.py
```
