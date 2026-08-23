#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
target = root / "scripts" / "restore_two_papers.py"
text = target.read_text(encoding="utf-8")
marker = "# Update validator invariants to the restored 189-work corpus."
if marker not in text:
    raise SystemExit("restore helper marker missing")
text = text.split(marker, 1)[0] + marker + r'''
validator = ROOT / "scripts" / "validate_corpus.py"
vtext = validator.read_text(encoding="utf-8")
repls = [
    ('EXPECTED_COUNTS = {"set1_core": 91, "set2_emerging": 96, "total_corpus": 187}',
     'EXPECTED_COUNTS = {"set1_core": 92, "set2_emerging": 97, "total_corpus": 189}'),
    ('EXPECTED_CONTRIB = {"attack": 44, "defense": 80, "evaluation": 44, "general": 12, "survey": 7}',
     'EXPECTED_CONTRIB = {"attack": 45, "defense": 80, "evaluation": 45, "general": 12, "survey": 7}'),
    ('(len(s1), len(s2)) != (91, 96)', '(len(s1), len(s2)) != (92, 97)'),
    ('if len(all_rows) != 187:', 'if len(all_rows) != 189:'),
    ('active corpus is not 187', 'active corpus is not 189'),
    ('exact materialized view of the active 187 corpus', 'exact materialized view of the active 189 corpus'),
    ('if len(index) != 187:', 'if len(index) != 189:'),
    ('papers/index.csv must have 187 rows', 'papers/index.csv must have 189 rows'),
    ('!= 187:\n        raise SystemExit("duplicate work_key in papers/index.csv")', '!= 189:\n        raise SystemExit("duplicate work_key in papers/index.csv")'),
    ('if len(notes) != 187:', 'if len(notes) != 189:'),
    ('expected exactly 187 paper notes', 'expected exactly 189 paper notes'),
    ('Supporting SoK comparators may overlap the 201 corpus', 'Supporting SoK comparators may overlap the active corpus'),
    ('Final corpus valid: Set1=91 Set2=96 total=187; papers=187;', 'Final corpus valid: Set1=92 Set2=97 total=189; papers=189;'),
]
for old, new in repls:
    vtext = vtext.replace(old, new)
validator.write_text(vtext, encoding="utf-8")

print("Prepared restored corpus: Set1=92 Set2=97 total=189")
'''
target.write_text(text, encoding="utf-8")
subprocess.run([sys.executable, str(target)], check=True, cwd=root)
