#!/usr/bin/env python3
import csv, json
from collections import Counter
from pathlib import Path

R=Path(__file__).resolve().parents[1]
C=R/'corpus'; P=R/'papers'
REMOVE={
 'doi:10.2139/ssrn.7067276':'post-cutoff first public availability (2026-07-06)',
 'doi:10.2139/ssrn.7181662':'post-cutoff first public availability (2026-07-31)',
 'doi:10.2139/ssrn.7218206':'post-cutoff first public availability (2026-08-01)',
 'arxiv:2604.23338':'broad agent-security survey; retain only as related-work comparator',
 'doi:10.20944/preprints202602.1655.v1':'broad autonomous/collaborative agent-security survey; retain only as related-work comparator',
 'doi:10.5281/zenodo.19477187':'primary source and DOI could not be independently recovered; remove until verifiable',
}

def read_csv(p):
    with p.open(encoding='utf-8-sig', newline='') as f: return list(csv.DictReader(f)), None

def write_csv(p, rows):
    if not rows: raise SystemExit(f'empty rows for {p}')
    with p.open('w', encoding='utf-8', newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

s1,_=read_csv(C/'set1_core.csv'); s2,_=read_csv(C/'set2_emerging.csv')
found={r['work_key'] for r in s2 if r['work_key'] in REMOVE}
if found != set(REMOVE):
    raise SystemExit(f'removal keys mismatch missing={set(REMOVE)-found}')
s2=[r for r in s2 if r['work_key'] not in REMOVE]
write_csv(C/'set2_emerging.csv', s2)

idx,_=read_csv(P/'index.csv')
removed_index=[r for r in idx if r['work_key'] in REMOVE]
if len(removed_index)!=6: raise SystemExit(f'expected 6 index rows, got {len(removed_index)}')
for r in removed_index:
    p=R/r['paper_path']
    if p.exists(): p.unlink()
idx=[r for r in idx if r['work_key'] not in REMOVE]
write_csv(P/'index.csv', idx)

# comparator view: Chu and Sun remain as related-work comparators but are no longer corpus members
sp=C.parent/'sok_related'/'papers.csv'
comparators,_=read_csv(sp)
for r in comparators:
    if r['sok_id'] in {'chu2026layered','sun2026unique_security'}:
        r['in_final_201']='no'
        r['final_paper_path']=''
write_csv(sp, comparators)

all_rows=s1+s2
counts=Counter(r['dominant_contribution'] for r in all_rows)
expected={'attack':44,'defense':84,'evaluation':46,'general':14,'survey':7}
if len(s1)!=96 or len(s2)!=99 or len(all_rows)!=195 or dict(counts)!=expected:
    raise SystemExit(f'count mismatch s1={len(s1)} s2={len(s2)} total={len(all_rows)} contrib={dict(counts)}')

manifest=json.loads((C/'manifest.json').read_text())
manifest['counts']={'set1_core':96,'set2_emerging':99,'total_corpus':195}
manifest['contributions']=expected
(C/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')

# Rewrite concise active-corpus docs.
(R/'README.md').write_text('''# Multi Agent Security Corpus\n\nAuditable literature corpus for security of interacting LLM agents. Literature cutoff: `2026-07-01`.\n\n## Authoritative manuscript corpus\n\nThere is one active manuscript corpus: **195 works**.\n\n| Set | Count | Meaning |\n| --- | ---: | --- |\n| Set 1 | 96 | In scope mature MAS security work |\n| Set 2 | 99 | In scope emerging MAS security work |\n| **Total** | **195** | **Authoritative MAS security corpus** |\n\nThe authoritative row level files are `corpus/set1_core.csv` and `corpus/set2_emerging.csv`. Together they contain exactly 195 unique works.\n\nSix records were removed on 2026-08-23 after cutoff and source-boundary checks: three were first public after the 2026-07-01 cutoff, two broad agent-security surveys were moved to the related-work comparator view, and one Zenodo record was removed because its primary source could not be independently recovered. CoMet, DACS, and NOD remain in the active corpus.\n\n## Paper organization\n\n`papers/` stores exactly the active corpus notes by dominant contribution and venue. Current totals are **44 attacks**, **84 defenses**, **46 evaluations**, **14 general works**, and **7 surveys**.\n\n## Validation\n\nRun `scripts/validate_all.sh`.\n''')
(C/'README.md').write_text('''# Authoritative 195 work corpus\n\nOnly Set 1 and Set 2 are active manuscript evidence sets.\n\n| File | Count | Meaning |\n| --- | ---: | --- |\n| `set1_core.csv` | 96 | Mature in scope MAS security work |\n| `set2_emerging.csv` | 99 | Emerging in scope MAS security work |\n| **Union** | **195** | **Exact manuscript corpus** |\n\nSet 1 and Set 2 share the same MAS-security scope gate. Set 1 additionally satisfies the frozen maturity rule: peer reviewed or at least 10 frozen citations.\n''')
(R/'FROZEN_SNAPSHOT.md').write_text('''# Frozen corpus snapshot\n\nLiterature cutoff: `2026-07-01`\n\nFinal classification corrections: `2026-08-23`\n\n| Partition | Count |\n| --- | ---: |\n| Set 1 | 96 |\n| Set 2 | 99 |\n| **Authoritative corpus** | **195** |\n\nThe 195 work union is the sole manuscript-facing corpus.\n''')
(R/'CORPUS_SET_POLICY.md').write_text('''# Corpus policy\n\n## Scope gate\n\nA work enters the active corpus only if all of the following hold:\n\n1. It studies at least two separately addressable LLM backed agents or principals.\n2. A material inter agent relation or interaction path is present.\n3. It studies a concrete security property, attack, defense, guarantee, adversary, or security evaluation.\n4. Source evidence is sufficient to support the membership decision.\n5. The work was publicly available before the frozen literature cutoff `2026-07-01`.\n\nInteraction dependence strength is evidence characterization, not a membership gate. Multi-agent systems used merely as a tool for generic single-agent security are not automatically MAS-security evidence. Broad agent-security surveys may be retained in `sok_related/` without entering the active corpus.\n\n## Set 1 and Set 2\n\nBoth sets are in scope. Set 1 is the mature subset and uses `peer_reviewed == yes OR frozen_citation_count >= 10`. Set 2 contains the remaining in-scope emerging work.\n\nThe current manuscript corpus is **96 Set 1 works plus 99 Set 2 works, for 195 total**.\n''')

(P/'README.md').write_text('''# Final 195 paper corpus\n\nThis directory contains exactly the **195 works** in the manuscript corpus: **96 Set 1** and **99 Set 2**.\n\n| Contribution | Count | Directory |\n| --- | ---: | --- |\n| attack | 44 | [`attacks/`](attacks/) |\n| defense | 84 | [`defenses/`](defenses/) |\n| evaluation | 46 | [`evaluations/`](evaluations/) |\n| general | 14 | [`general/`](general/) |\n| survey | 7 | [`surveys/`](surveys/) |\n\n[`index.csv`](index.csv) is the exact one-to-one mapping from all 195 corpus work keys to paper paths.\n''')

# Regenerate category readmes from index.
for category, dirname in {'attack':'attacks','defense':'defenses','evaluation':'evaluations','general':'general','survey':'surveys'}.items():
    rows_cat=[r for r in idx if r['dominant_contribution']==category]
    by={}
    for r in rows_cat: by.setdefault(r['venue_folder'],[]).append(r)
    lines=[f'# {category.title()} papers','',f'Final 195-corpus dominant-contribution count: **{len(rows_cat)}**.','']
    for venue in sorted(by):
        lines += [f'## {venue}','']
        for r in sorted(by[venue], key=lambda x:x['title'].lower()):
            rel=Path(r['paper_path']).relative_to(P/dirname)
            lines.append(f"* [{r['title']}]({rel.as_posix()})  `{r['evidence_set']}`")
        lines.append('')
    (P/dirname/'README.md').write_text('\n'.join(lines)+'\n')

(R/'related_work'/'surveys_and_soks.md').write_text('''# Multi Agent Security Surveys and SoKs\n\nThis synthesis uses the **195 work** manuscript corpus as the active evidence denominator. The active corpus contains **7 survey-primary works**.\n\nTwo broad agent-security surveys, `chu2026layered` and `sun2026unique_security`, are intentionally outside the strict MAS-security corpus and remain in `sok_related/` as strongly related comparators. Their broader unit of analysis covers agent security beyond interaction-dependent MAS security.\n\n`sok_related/` is a separate supporting comparator view and is never added to the 195-work denominator. Use primary attack, defense, and evaluation papers for empirical claims whenever possible.\n''')
(R/'sok_related'/'README.md').write_text('''# Strongly Related Multi Agent Security SoKs\n\nThis directory is a supporting comparator view for related SoKs, surveys, and framework papers. It is not an active corpus partition.\n\nThe active manuscript corpus contains **195 works**. Comparator records may overlap the corpus or may be contextual only. Broad agent-security surveys such as Chu et al. and Sun et al. remain here even though they are outside the strict MAS-security corpus.\n\nNever add the number of rows in this directory to the manuscript corpus denominator.\n''')

# Update validator constants and exact paper cardinality.
v=(R/'scripts'/'validate_corpus.py').read_text()
v=v.replace('EXPECTED_COUNTS = {"set1_core": 96, "set2_emerging": 105, "total_corpus": 201}', 'EXPECTED_COUNTS = {"set1_core": 96, "set2_emerging": 99, "total_corpus": 195}')
v=v.replace('EXPECTED_CONTRIB = {"attack": 44, "defense": 85, "evaluation": 46, "general": 16, "survey": 10}', 'EXPECTED_CONTRIB = {"attack": 44, "defense": 84, "evaluation": 46, "general": 14, "survey": 7}')
v=v.replace('(len(s1), len(s2)) != (96, 105)', '(len(s1), len(s2)) != (96, 99)')
v=v.replace('if len(all_rows) != 201:', 'if len(all_rows) != 195:')
v=v.replace('active corpus is not 201', 'active corpus is not 195')
v=v.replace('materialized view of the signed 201 corpus', 'materialized view of the active 195 corpus')
v=v.replace('if len(index) != 201:', 'if len(index) != 195:')
v=v.replace('must have 201 rows', 'must have 195 rows')
v=v.replace('!= 201:\n    raise SystemExit("duplicate work_key in papers/index.csv")', '!= 195:\n    raise SystemExit("duplicate work_key in papers/index.csv")')
v=v.replace('if len(notes) != 201:', 'if len(notes) != 195:')
v=v.replace('expected exactly 201 paper notes', 'expected exactly 195 paper notes')
v=v.replace('final 201 corpus', 'active 195 corpus')
v=v.replace('Final corpus valid: Set1=96 Set2=105 total=201; papers=201;', 'Final corpus valid: Set1=96 Set2=99 total=195; papers=195;')
(R/'scripts'/'validate_corpus.py').write_text(v)

print('Removed six records; active corpus is Set1=96 Set2=99 total=195')
