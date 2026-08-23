#!/usr/bin/env python3
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'corpus'
PAPERS = ROOT / 'papers'
OUT = CORPUS / 'MAS_SCOPE_AUDIT_2026-08-23.csv'


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def section(text, heading):
    m = re.search(rf'(?ms)^###?\s+{re.escape(heading)}\s*\n(.*?)(?=^##|^###|\Z)', text)
    if not m:
        return ''
    value = re.sub(r'\s+', ' ', m.group(1)).strip()
    return value[:1200]


def first_nonempty(text, headings):
    for h in headings:
        v = section(text, h)
        if v:
            return v
    return ''

rows = read_csv(CORPUS / 'set1_core.csv') + read_csv(CORPUS / 'set2_emerging.csv')
index = {r['work_key']: r for r in read_csv(PAPERS / 'index.csv')}
assert len(rows) == 201 and len(index) == 201

fields = [
    'work_key','title','evidence_set','dominant_contribution','venue','primary_url',
    'interaction_interfaces','risk_or_property','interaction_dependence','paper_path',
    'note_depth','system_studied','multi_agent_dependency','threat_actor','attacker_capabilities',
    'main_contribution','attack_or_failure','defense_mechanism','evaluation','sok_relevance',
    'source_review_status','current_scope_reason','current_membership_reason'
]

with OUT.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in rows:
        idx = index[r['work_key']]
        path = ROOT / idx['paper_path']
        text = path.read_text(encoding='utf-8', errors='replace')
        detailed = ('## Security Model' in text or '## Source Review' in text or '### Multi-Agent Dependency' in text)
        source_status = ''
        m = re.search(r'\*\*Status:\*\*\s*`?([^`\n]+)', text)
        if m:
            source_status = m.group(1).strip()
        w.writerow({
            'work_key': r['work_key'],
            'title': r['title'],
            'evidence_set': r['evidence_set'],
            'dominant_contribution': r['dominant_contribution'],
            'venue': r.get('venue',''),
            'primary_url': r.get('primary_url',''),
            'interaction_interfaces': r.get('interaction_interfaces',''),
            'risk_or_property': r.get('risk_or_property',''),
            'interaction_dependence': r.get('interaction_dependence',''),
            'paper_path': idx['paper_path'],
            'note_depth': 'detailed' if detailed else 'metadata_only',
            'system_studied': first_nonempty(text, ['System Studied']),
            'multi_agent_dependency': first_nonempty(text, ['Multi-Agent Dependency']),
            'threat_actor': first_nonempty(text, ['Threat Actor', 'Attacker or fault actor']),
            'attacker_capabilities': first_nonempty(text, ['Attacker Capabilities', 'Capabilities']),
            'main_contribution': first_nonempty(text, ['Main Contribution']),
            'attack_or_failure': first_nonempty(text, ['Attack Mechanism', 'Attack Surface', 'System-Level Failure']),
            'defense_mechanism': first_nonempty(text, ['Defense Mechanism']),
            'evaluation': first_nonempty(text, ['Evaluated Systems', 'Evaluation Contract']),
            'sok_relevance': first_nonempty(text, ['Taxonomy Implications', 'Included Concepts', 'Relevance to Our SoK']),
            'source_review_status': source_status,
            'current_scope_reason': r.get('scope_reason',''),
            'current_membership_reason': r.get('membership_reason',''),
        })
print(f'wrote {OUT} with {len(rows)} rows')
