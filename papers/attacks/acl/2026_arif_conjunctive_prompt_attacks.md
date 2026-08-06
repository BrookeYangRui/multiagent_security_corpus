# Conjunctive Prompt Attacks in Multi-Agent LLM Systems

> **Source-review correction:** The Source Review section at the end supersedes inconsistent automated coding in this note. It still requires author signoff.

## Citation

- Authors: Nokimul Hasan Arif, Qian Lou, Mengxin Zheng
- Year: 2026
- Venue: ACL 2026
- DOI: 10.18653/v1/2026.acl-long.1577
- Primary URL: https://aclanthology.org/2026.acl-long.1577/
- Open access URL: https://aclanthology.org/2026.acl-long.1577.pdf
- BibTeX key: `arif2026conjunctive`

## Paper Type

Attack; Evaluation

- Primary category: `attack`
- Scope relation: `core_security`

## Scope

### System Studied

Agentic LLM pipelines with a client agent, remote agents, and star, chain, or DAG
routing structures.

### Multi-Agent Dependency

A trigger in the user query and a template in one compromised remote agent are
benign in isolation but become harmful when routing composes them.

### Application Domain

General-purpose routed agent pipelines.

## Security Model

- Protected assets: action and output safety of the composed pipeline.
- Threat actor: attacker controlling trigger placement and one remote template.
- Trusted components: model weights and client agent remain unchanged.
- Attacker capabilities: insert two fragments but not alter model weights.
- Security assumptions: routing eventually brings the fragments into one context.

## Main Contribution

The paper introduces conjunctive prompt attacks and routing-aware optimization
for cross-agent composition across star, chain, and DAG topologies.

## Attack or Failure

- Attack surface: segmented prompts, remote-agent templates, and routing.
- Attack mechanism: composition activates a harmful instruction that is absent
  from every isolated component.
- System-level failure: compositional action and safety-integrity failure.
- Security consequence: harmful behavior with low false activation.

## Defense

- Defense mechanism: PromptGuard, Llama-Guard variants, and tool restrictions are
  evaluated rather than introduced.
- Intervention point: local inputs/outputs and tool boundary.
- Required observability: tested guards see components locally.
- Assumptions: local defenses do not reconstruct full routing provenance.
- Limitations: evaluated defenses do not reliably stop the attack.

## Evaluation

- Evaluated systems: multi-agent LLM pipelines.
- Agent configuration: client plus remote agents under star, chain, and DAG.
- Dataset or environment: attack scenarios specified in the paper.
- Baselines: non-optimized attacks and existing guards/system controls.
- Metrics: attack success and false activation.
- Main results: routing-aware optimization improves success while retaining low
  false activation across evaluated topologies.

## Relation to Existing Work

- Claimed research gap: single-agent evaluation misses prompt segmentation and
  routing composition.
- Closest related work: prompt injection and fragmented/decomposed attacks.
- Difference from prior work: neither fragment is malicious by itself.

## Relevance to Our SoK

- Included concepts: compromised remote agent, routing, fragmented intent,
  provenance gap.
- Taxonomy implications: vulnerability/precondition is cross-component context;
  mechanism is conjunctive activation.
- Supported research questions: whether local monitors can enforce global
  policies.
- Important limitations: evaluated topologies and system controls are bounded.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Trigger and hidden template appear benign alone but activate harm together. | Explicit author claim | Paper | Abstract | PDF 1 | Not applicable | Official abstract defines conjunctive attack. |
| Attacker changes neither weights nor client agent. | Explicit author claim | Paper | Abstract; threat model | PDF 1 onward | Not applicable | Official abstract states attacker constraints. |
| Evaluated topologies are star, chain, and DAG. | Explicit author claim | Paper | Abstract; experiments | PDF 1; evaluation | Not applicable | Listed in official abstract. |

## Provenance

- Discovery source: ACL Anthology; prior systematic search
- Discovery query: `site:aclanthology.org multi-agent LLM attack security`
- Accessed version: published ACL 2026 version
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

<!-- SOURCE_REVIEW_START -->
## Source Review

**Status:** `source_reviewed_pending_author_signoff`

**Outcome:** Ready after major patch

**Review source:** `reviews/load_bearing/load_bearing_source_review.csv`

This section supersedes inconsistent automated coding elsewhere in this note.
It is a source-level review, not human verification. Manuscript-facing claims
still require author or designated-reviewer signoff.

### Identity and Scope

- Identity: Canonical ACL 2026 version confirmed. Metadata is correct.
- Recommended scope: `core_security`
- Multi-agent dependency: A user trigger and a compromised remote-agent template are benign in isolation and become harmful only when routing composes them.
- Recommended roles: attack; evaluation
- Maturity: Archival peer-reviewed primary attack evidence.

### Threat and Failure Coding

- Attacker or fault actor: Adversary controlling trigger placement and one remote-agent template while leaving model weights and the client agent unchanged.
- Capabilities: Places two fragments and relies on system routing to combine them.
- Preconditions: Star, chain, or DAG routing eventually joins the trigger and hidden template in one effective context.
- Surfaces: User query; remote-agent template; routing and provenance; local guards.
- Mechanism: Conjunctive activation of individually benign fragments.
- Primary system-level failure: F3 communication, context, or action integrity failure.
- Impact: Harmful action or unsafe output. F6 authority integrity should be secondary only when an explicit privileged action or permission escalation is demonstrated.

### Evaluation Contract

- Configuration: Client plus remote agents under star, chain, and DAG topologies.
- Topology: Star, chain, DAG.
- Baseline or ablation: Clean, key-only, template-only, both-fragment, nonoptimized attacks, local guards, and tool restrictions.
- Metric: ASR and false activation across topologies and control conditions.
- Unit: Attack scenario or routed task.
- Denominator: Evaluated scenarios for each topology and fragment condition.
- Result boundary: Routing-aware optimization improves attack success while maintaining low false activation in evaluated configurations.

### Evidence and Boundaries

- Evidence locations: Abstract, PDF p. 1; threat model and routing composition, PDF p. 1 onward; experimental tables for clean, single-fragment, and combined conditions; topology tables for star, chain, and DAG.
- Author claim versus corpus interpretation: Two-fragment construction, attacker constraints, topologies, and metrics are author claims. F3 versus F6 classification is a corpus judgment.
- Limitations: Bounded static topologies; abstracted or probabilistic routing; selected guards; no production router, dynamic membership, or broad authorization model.

### Required Corrections

- **CRITICAL - Primary failure:** Use F3 context/action integrity as primary unless the source explicitly demonstrates privilege escalation.
- **HIGH - Baseline coding:** Record clean, key-only, template-only, and both-fragment controls separately.
- **MEDIUM - Metric evidence:** Tie ASR and false activation to exact topology tables.
<!-- SOURCE_REVIEW_END -->
