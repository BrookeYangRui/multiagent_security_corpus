#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, re, shutil
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'artifact/search/v2'
C=ROOT/'corpus'

ROLE_VALUES=('attack','defense','evaluation','other')

def read(name):
    with (SRC/name).open(encoding='utf-8-sig', newline='') as h:
        return list(csv.DictReader(h))

def write(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as h:
        w=csv.DictWriter(h, fieldnames=fields); w.writeheader(); w.writerows(rows)

def existing_role(value):
    c=(value or '').strip().lower()
    if not c: return None
    if 'attack' in c: return 'attack'
    if 'defense' in c: return 'defense'
    if 'evaluation' in c or 'benchmark' in c: return 'evaluation'
    return 'other'

def title_role(title):
    t=(title or '').lower()
    defense=[r'\bdefen[cs]e\b',r'\bmitigat',r'\bprevent',r'\bprotect',r'guard',r'firewall',r'\bsecure\b',r'\bsecuring\b',r'\bsafeguard',r'\bsafe\b',r'\brobust\b',r'\bresilien',r'fault[- ]tolerant',r'privacy[- ]preserv',r'zero[- ]trust',r'authentication',r'authorization',r'delegation protocol',r'provenance',r'governance',r'oversight',r'monitor',r'healing',r'hardening',r'remediation',r'control framework',r'trust mechanism',r'security framework']
    evaluation=[r'\bbenchmark',r'\bevaluat',r'\bmeasur',r'\bauditing?\b',r'\baudit\b',r'empirical study',r'controlled experiment',r'characteriz',r'comparing',r'comparison',r'study of',r'analy[sz]ing',r'analysis of',r'testing',r'assess',r'understanding',r'investigat',r'what do',r'when does',r'reliability challenges']
    attack=[r'\battack',r'jailbreak',r'poison',r'prompt injection',r'adversar',r'\bmalicious\b',r'\bexploit',r'vulnerab',r'\bleak',r'exfiltrat',r'collusion',r'deception',r'misinformation',r'sycophancy',r'contamination',r'hijack',r'\bworm\b',r'backdoor',r'\bdenial\b',r'stealthy',r'\bbreaking\b',r'compromis',r'sabot',r'manipulat',r'propagation',r'false consensus',r'\blying\b',r'gaslighting',r'steganograph']
    d=sum(bool(re.search(x,t)) for x in defense); e=sum(bool(re.search(x,t)) for x in evaluation); a=sum(bool(re.search(x,t)) for x in attack)
    if d and (d>=a or re.search(r'defen[cs]e|mitigat|guard|secure|safeguard|safe\b|robust|resilien|privacy-preserv|fault[- ]tolerant',t)):
        if e>=2 and not re.search(r'framework|protocol|guard|defen[cs]e',t): return 'evaluation'
        return 'defense'
    if e and (e>=a or not a): return 'evaluation'
    if a: return 'attack'
    return 'other'

def enrich(rows):
    out=[]
    for row in rows:
        row=dict(row)
        role=existing_role(row.get('current_primary_category'))
        if role:
            source='existing_corpus_role'; status='source_reviewed_or_imported'
        else:
            role=title_role(row.get('title','')); source='title_rule_v2'; status='assistant_derived_pending_author_signoff'
        row.update(broad_role=role, role_source=source, role_status=status)
        out.append(row)
    return out

def digest(path):
    h=hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()

primary=enrich(read('review_primary.csv')); secondary=enrich(read('review_secondary.csv'))
exclude=read('review_exclude.csv'); pending=read('review_pending.csv'); queue=read('review_candidate_queue.csv'); routes=read('review_candidate_routes.csv'); ledger=read('review_decision_ledger.csv'); aliases=read('review_identifier_aliases.csv'); overrides=read('identifier_alias_overrides.csv')

# Remove superseded paper-population views. Paper notes remain supporting evidence only.
for path in [C/'final',C/'sets',C/'source_packages',ROOT/'reports',ROOT/'reviews',SRC]:
    if path.exists(): shutil.rmtree(path)
for path in [C/'papers.csv',C/'references.bib',C/'canonical_field_overrides.csv']:
    if path.exists(): path.unlink()

files={
 'primary.csv':primary,'secondary.csv':secondary,'exclude.csv':exclude,'pending.csv':pending,
 'review_queue.csv':queue,'routes.csv':routes,'decision_ledger.csv':ledger,
 'identifier_aliases.csv':aliases,'identifier_alias_overrides.csv':overrides,
}
for name,rows in files.items(): write(C/name,rows,list(rows[0].keys()))

summary=[]
def add(pop,dim,val,count,note=''): summary.append({'population':pop,'dimension':dim,'value':val,'count':count,'note':note})
for name,rows in [('primary',primary),('secondary',secondary),('exclude',exclude),('pending',pending)]: add('all_work_queue','decision',name,len(rows))
for role,count in sorted(Counter(r['broad_role'] for r in primary).items()): add('primary','broad_role',role,count,'Descriptive dominant-role coding; mixed works receive one broad role.')
for role,count in sorted(Counter(r['broad_role'] for r in secondary).items()): add('secondary','broad_role',role,count,'Descriptive role coding; not an inclusion decision.')
for year,count in sorted(Counter(r['year'] for r in primary).items()): add('primary','year',year,count)
targeted=[r for r in routes if r.get('route_type')=='targeted']; add('targeted_route','records','cutoff_candidate_records',len(targeted)); add('targeted_route','works','canonical_works',len({r['work_key'] for r in targeted}))
write(C/'summary.csv',summary,['population','dimension','value','count','note'])

(C/'README.md').write_text('''# Authoritative review corpus\n\nThese files are the only paper-population tables used by the SoK. The fixed 1 July 2026 review universe contains 2,217 deduplicated works: 303 primary, 177 secondary, 1,396 exclude, and 341 pending. The four decision files partition the queue exactly. Pending rows remain visible but never enter a final evidence set.\n\nThe targeted route contains 318 cutoff-eligible records resolving to 317 works. `primary.csv` and `secondary.csv` add a descriptive `broad_role` (`attack`, `defense`, `evaluation`, `other`). Existing source-reviewed/imported roles are preserved; rows without a prior role use a title-level rule and are marked `assistant_derived_pending_author_signoff`. Role coding never changes inclusion.\n\n`papers/` contains partial source notes and is not a corpus-membership list. Historical source paths retained in provenance fields explain how a row entered review; the superseded broad-screen, canonical-142, taxonomy-115, and source-package tables themselves have been removed.\n''',encoding='utf-8')

manifest={'schema_version':3,'cutoff':'2026-07-01','candidate_unit':'canonical work','authoritative_counts':{'total':2217,'primary':303,'secondary':177,'exclude':1396,'pending':341},'targeted_route':{'records':318,'canonical_works':317},'primary_broad_role_counts':dict(sorted(Counter(r['broad_role'] for r in primary).items())),'secondary_broad_role_counts':dict(sorted(Counter(r['broad_role'] for r in secondary).items())),'decision_precedence':['persistent human adjudication','canonical/source review','peer-first reviewed gate','structured exclusion','full-text search screen','weaker discovery routes'],'role_coding_note':'Broad roles are descriptive. Imported/source-reviewed roles are preserved; otherwise a title-level rule supplies a provisional dominant role pending author signoff.','files':{}}
for path in sorted(C.glob('*')):
    if path.is_file() and path.name!='manifest.json':
        rows=sum(1 for _ in path.open(encoding='utf-8',errors='ignore'))-1 if path.suffix=='.csv' else None
        manifest['files'][path.name]={'rows':rows,'sha256':digest(path)}
(C/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')

ROOT.joinpath('README.md').write_text('''# Multi-Agent Security Corpus\n\nAuditable literature corpus for security of interacting LLM agents. Search cutoff: `2026-07-01 00:00 UTC`.\n\n## One authoritative review universe\n\n| File | Count |\n| --- | ---: |\n| `corpus/review_queue.csv` | 2,217 works |\n| `corpus/primary.csv` | 303 primary |\n| `corpus/secondary.csv` | 177 secondary |\n| `corpus/exclude.csv` | 1,396 exclude |\n| `corpus/pending.csv` | 341 pending |\n| targeted route | 318 records / 317 works |\n\nOlder broad-screen, canonical-142, taxonomy-115, and source-package denominators were removed rather than archived so that counts cannot be mixed across versions. `primary` is the direct interaction-security evidence pool; `secondary` is security-relevant context; `exclude` is outside the evidence boundary; `pending` remains unresolved and is never counted as final evidence.\n\n`corpus/routes.csv` preserves route-level provenance and `corpus/decision_ledger.csv` preserves review decisions. Discovery-route membership alone cannot promote a work. Stronger source or human review overrides weaker discovery evidence, and equal-strength conflicts remain pending.\n\n`papers/` contains source notes where available, not a denominator. `related_work/` contains synthesis notes. `corpus/evidence/` contains non-paper evidence such as CVEs and industry reports and never enters the academic-work counts above.\n\n## Validate\n\n```bash\nscripts/validate_all.sh\n```\n''',encoding='utf-8')

# Remove obsolete generators/validators tied to retired denominators.
for name in ['build_corpus_sets.py','build_peer_first_eligibility.py','import_authoritative_142.py','build_final_exports.py','plot_yearly_growth.py','plot_broad_yearly_growth.py','validate_corpus.py','validate_corpus_sets.py','build_universal_review_queue.py']:
    path=ROOT/'scripts'/name
    if path.exists(): path.unlink()
(ROOT/'scripts'/'validate_all.sh').write_text('#!/usr/bin/env bash\nset -euo pipefail\ncd "$(git rev-parse --show-toplevel)"\npython3 scripts/validate_authoritative_corpus.py\n',encoding='utf-8')
print('migration complete')
