# Lying with Truths: Open-Channel Multi-Agent Collusion for Belief Manipulation via Generative Montage

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `attack` · venue `ACL` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

> **Source-review correction:** The Source Review section at the end supersedes inconsistent automated coding in this note. It still requires author signoff.

## Citation

Title: Lying with Truths: Open-Channel Multi-Agent Collusion for Belief Manipulation via Generative Montage

Authors: Jinwei Hu; Xinmiao Huang; Youcheng Sun; Yi Dong; Xiaowei Huang

Year: 2026

Venue: ACL

DOI: 10.18653/v1/2026.acl-long.270

Primary URL: https://aclanthology.org/2026.acl-long.270/

Open access URL: https://aclanthology.org/2026.acl-long.270.pdf

BibTeX key: hu2026lyingtruths

## Paper Type

Attack; Benchmark; Evaluation

- Primary category: `attack`
- Scope relation: `core_security`

## Scope

### System Studied

Agent populations consuming public evidence posts and making belief judgments about rumor events.

### Multi-Agent Dependency

Several colluding agents coordinate truthful evidence fragments in an open channel; victim agents synthesize the distributed fragments into a false narrative and may pass that belief to downstream judges.

### Application Domain

Dynamic information environments, rumor assessment, and social-agent decision-making.

## Security Model

### Protected Assets

Integrity of victim beliefs and downstream collective judgments.

### Threat Actor

A coalition of writer, editor, and director agents.

### Trusted Components

Underlying evidence documents are factual; victim and downstream judge models are not directly compromised.

### Attacker Capabilities

Colluders select, rewrite, order, and publicly post individually truthful evidence fragments and coordinate their narrative through adversarial debate.

### Security Assumptions

Victims aggregate public posts, and no monitor rejects the messages merely for falsity because the fragments are individually truthful.

## Main Contribution

The paper formalizes cognitive collusion through public truthful evidence and proposes Generative Montage, a writer-editor-director pipeline that constructs a misleading joint narrative. It introduces CoPHEME, derived from real rumor events, and evaluates victim and downstream belief propagation across 14 model families.

## Attack or Failure

### Attack Surface

Public multi-agent information channels and victim evidence aggregation.

### Attack Mechanism

Colluders select and arrange true fragments so that their composition implies an unsupported false conclusion.

### System-Level Failure

Victim agents internalize the fabricated conclusion and propagate it to later decision-makers.

### Security Consequence

Collective epistemic and decision-integrity failure despite message-level factuality.

## Defense

### Defense Mechanism

The paper evaluates reasoning prompts and model-based safeguards but does not establish a complete defense against compositional narrative manipulation.

### Intervention Point

Victim reasoning and evidence aggregation.

### Required Observability

A defense needs cross-message provenance, event context, and the joint implication of the evidence set.

### Assumptions

Individual-fragment truth can be checked, but the global narrative requires contextual analysis.

### Limitations

The simulation uses a fixed writer-editor-director attack pipeline and curated rumor events rather than a live open agent network.

## Evaluation

### Evaluated Systems

Fourteen proprietary and open-weight LLM families, including reasoning-specialized variants.

### Agent Configuration

Writer, editor, and director attackers; victim belief agents; and downstream judge agents.

### Dataset or Environment

CoPHEME, constructed from real-world rumor events and supporting evidence.

### Baselines

Base prompts, reasoning variants, alternative attack constructions, and model families.

### Metrics

Victim attack success and downstream deception rate.

### Main Results

The authors report attack success up to 74.4% for proprietary models and 70.6% for open-weight models, with downstream deception above 60%. Reasoning-specialized models are reported as more susceptible in this setting.

## Relation to Existing Work

### Papers Compared by the Authors

Steganographic collusion, misinformation attacks, persuasion, and adversarial debate.

### Claimed Research Gap

Prior collusion work relies on covert channels, falsified content, or hidden backdoors rather than openly coordinating individually true evidence.

### Closest Related Work

Secret Collusion among AI Agents and multi-agent belief-manipulation attacks.

### Difference From Prior Work

The channel is public and fragments are factual; harmful meaning emerges only from coalition-level selection and composition.

## Relevance to Our SoK

### Included Concepts

Colluding coalition, public channel, truthful fragments, cross-message composition, provenance, victim belief, and downstream propagation.

### Taxonomy Implications

The mechanism is cognitive collusion, while the failed system property is collective decision integrity; it also exposes why per-message truth checks are insufficient.

### Supported Research Questions

Which observer scope is required to detect harmful coordination when no individual message is false or covert?

### Important Limitations

CoPHEME should later be indexed as an evaluation artifact without adding a second canonical paper record.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The attack uses truthful fragments in public channels rather than a covert code. | Explicit author claim | Paper | 1, 3 | 1-5 | Framework figure | Threat definition. |
| Generative Montage assigns writer, editor, and director roles. | Explicit author claim | Paper | 3 | 4-6 | Method figure | Attack pipeline. |
| CoPHEME derives attacks from real-world rumor events. | Explicit author claim | Paper | 4 | 6-8 | Dataset table | Evaluation resource. |
| Peak victim ASR is 74.4%/70.6% for proprietary/open models. | Explicit author claim | Paper | 5 | 8-11 | Main results | Reported effectiveness. |
| Downstream judges show deception rates above 60%. | Explicit author claim | Paper | 5 | 10-12 | Propagation table | Downstream impact. |

## Provenance

### Discovery Source

ACL Anthology; systematic search.

### Discovery Query

site:aclanthology.org/2026.acl-long multi-agent attack security LLM collusion topology

### Accessed Version

Published conference version.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05

<!-- SOURCE_REVIEW_START -->
## Source Review

**Status:** `source_reviewed_pending_author_signoff`

**Outcome:** Ready after minor patch

**Review source:** `reviews/universal/universal_114_source_review.csv`

This section supersedes inconsistent automated coding elsewhere in this note.
It is a source-level review, not human verification. Manuscript-facing claims
still require author or designated-reviewer signoff.

### Identity and Scope

- Identity: Canonical ACL 2026 version confirmed. Metadata and title are correct.
- Recommended scope: `core_security`
- Multi-agent dependency: A writer-editor-director coalition coordinates public, individually truthful fragments whose composition manipulates victim agents and downstream judges.
- Recommended roles: attack; benchmark; evaluation
- Maturity: Archival peer-reviewed primary attack evidence.

### Threat and Failure Coding

- Attacker or fault actor: Coalition of writer, editor, and director agents.
- Capabilities: Select, rewrite, order, and publicly post factual fragments and coordinate their narrative construction.
- Preconditions: Victims aggregate public posts, while message-level truth checks cannot reject individually factual fragments.
- Surfaces: Public multi-agent information channel; aggregation; provenance and cross-message context.
- Mechanism: Open-channel cognitive collusion through generative montage.
- Primary system-level failure: F4 collective decision or belief integrity failure.
- Impact: Downstream propagation of a fabricated conclusion.

### Evaluation Contract

- Configuration: Coalition attackers, victim belief agents, downstream judge agents, and 14 proprietary and open-weight model families.
- Topology: Fixed writer-editor-director attack pipeline plus victim and judge stages.
- Baseline or ablation: Base prompts, reasoning variants, alternate constructions, and model families.
- Metric: Victim attack success and downstream deception rate.
- Unit: Rumor-event case or victim/judge decision.
- Denominator: CoPHEME cases used in each evaluated split.
- Result boundary: The authors report peak victim ASR of 74.4% for proprietary and 70.6% for open-weight models, with downstream deception above 60% in evaluated settings.

### Evidence and Boundaries

- Evidence locations: Secs. 1 and 3, PDF pp. 1 to 6 for threat and method; Sec. 4, PDF pp. 6 to 8 for CoPHEME; Sec. 5, PDF pp. 8 to 12 for main result and propagation tables.
- Author claim versus corpus interpretation: Open-channel truthful-fragment attack, role pipeline, dataset, and results are author claims. Labeling it F4 and using it as an observer-scope example are corpus interpretations.
- Limitations: Fixed attack pipeline; curated rumor events; simulated open channel; no live open-agent network; model susceptibility results are setting-specific.

### Required Corrections

- **MEDIUM - Mechanism label:** Do not label the channel covert or the fragments false; the novelty is public composition of individually true fragments.
- **MEDIUM - Evidence locator:** Tie ASR and downstream rates to the exact Sec. 5 tables and CoPHEME denominator.
<!-- SOURCE_REVIEW_END -->
