#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'corpus' / 'MAS_SCOPE_AUDIT_2026-08-23.csv'
OUT = ROOT / 'corpus' / 'MAS_SCOPE_TRIAGE_2026-08-23.csv'

SEC = [
    'attack','adversar','security','secure','privacy','leak','jailbreak','poison','malicious',
    'byzantine','collusion','deception','threat','compromis','authorization','authentication',
    'credential','integrity','confidential','denial','dos','worm','hijack','backdoor','taint',
    'trust boundary','sabot','injection','exploit','tamper','steal','propagation','vulnerab'
]
WEAK = ['safety','robust','reliab','hallucination','governance','ethical','alignment','compliance','drift','misinformation']

with SRC.open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))

fields = ['work_key','title','evidence_set','dominant_contribution','note_depth','security_signal','weak_signal','has_threat_actor','has_attack_failure','has_defense','prelim_tier','paper_path']
with OUT.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in rows:
        blob = ' '.join([r.get('title',''),r.get('main_contribution',''),r.get('attack_or_failure',''),r.get('defense_mechanism',''),r.get('sok_relevance',''),r.get('risk_or_property','')]).lower()
        sec = ';'.join(k for k in SEC if k in blob)
        weak = ';'.join(k for k in WEAK if k in blob)
        threat = bool(r.get('threat_actor','').strip())
        failure = bool(r.get('attack_or_failure','').strip())
        defense = bool(r.get('defense_mechanism','').strip())
        if sec and (threat or failure or defense or r.get('dominant_contribution') in {'attack','survey'}):
            tier = 'strong_direct_signal'
        elif sec:
            tier = 'security_named_needs_source_check'
        elif weak:
            tier = 'weak_safety_reliability_signal'
        else:
            tier = 'no_direct_security_signal'
        if r.get('note_depth') == 'metadata_only' and tier != 'strong_direct_signal':
            tier = 'metadata_only_needs_source_check'
        w.writerow({
            'work_key':r['work_key'],'title':r['title'],'evidence_set':r['evidence_set'],
            'dominant_contribution':r['dominant_contribution'],'note_depth':r['note_depth'],
            'security_signal':sec,'weak_signal':weak,'has_threat_actor':'yes' if threat else 'no',
            'has_attack_failure':'yes' if failure else 'no','has_defense':'yes' if defense else 'no',
            'prelim_tier':tier,'paper_path':r['paper_path']
        })
print('wrote', OUT, len(rows))
