#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
C=ROOT/'corpus'
IN=C/'REMAINING_189_SCOPE_AUDIT.csv'
OUT=C/'REMAINING_189_BOUNDARY_PRIORITY.md'

def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

r=rows(IN)
strong_title=('attack','security','secure','privacy','leak','confidential','integrity','authorization','authentication','byzantine','collusion','jailbreak','injection','poison','comprom','tamper','exploit','backdoor','worm','threat','stegan','covert','zero-trust')
weak=('safety','safe ','robust','reliab','alignment','hallucination','ethical','governance','trustworthy','trust ','coordination','reasoning','compliance','drift','framework')
priority=[]
for x in r:
    if x['note_status']!='metadata_only':continue
    t=x['title'].lower()
    has_strong=any(k in t for k in strong_title)
    has_weak=any(k in t for k in weak)
    broad_agent=('multi-agent' not in t and 'multi agent' not in t and 'agent-to-agent' not in t and 'agent to agent' not in t and 'cross-agent' not in t and 'agentic network' not in t)
    if (not has_strong) or has_weak or broad_agent:
        priority.append((0 if broad_agent else 1 if not has_strong else 2,x))
priority.sort(key=lambda z:(z[0],z[1]['dominant_contribution'],z[1]['title'].lower()))
lines=['# Strict Scope Boundary Priority','',f'Metadata-only rows needing the closest source-level attention: **{len(priority)}**.','']
for _,x in priority:
    lines += [f"## {x['title']}",f"* work_key: `{x['work_key']}`",f"* set/category: `{x['evidence_set']}` / `{x['dominant_contribution']}`",f"* venue: {x['venue']}",f"* primary: {x['primary_url']}",f"* current scope reason: {x['scope_reason_current']}",f"* current interaction: `{x['interaction_dependence_current']}`",'']
OUT.write_text('\n'.join(lines),encoding='utf-8')
print('priority',len(priority))
