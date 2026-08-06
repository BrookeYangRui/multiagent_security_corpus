# Multi-Agent Systems Execute Arbitrary Malicious Code

## Citation

- Authors: Harold Triedman, Rishi Dev Jha, Vitaly Shmatikov
- Year: 2025
- Venue: COLM 2025
- DOI: Not reported
- Primary URL: https://openreview.net/forum?id=DAozI4etUp
- Open access URL: https://openreview.net/pdf?id=DAozI4etUp
- BibTeX key: `triedman2025maliciouscode`

## Paper Type

Attack; Evaluation; Empirical study

## Scope

### System Studied

Deployed and research multi-agent frameworks that route tasks and messages among
specialized LLM agents.

### Multi-Agent Dependency

The attack hijacks control flow and inter-agent communication to invoke an
otherwise unreachable unsafe agent or functionality.

### Application Domain

General-purpose orchestration, web interaction, and code-capable agent workflows.

## Security Model

- Protected assets: control-flow integrity, tool authorization, and host-system
  integrity.
- Threat actor: an external party controlling untrusted web or document content.
- Trusted components: framework orchestration and nominally safe routing logic.
- Attacker capabilities: place indirect prompt injection in content processed by
  one agent.
- Security assumptions: agents and orchestrators use LLM-generated text to make
  routing or invocation decisions.

## Main Contribution

The paper formalizes and demonstrates control-flow hijacking attacks that use
untrusted content to redirect multi-agent execution toward unsafe agents and
functions, including arbitrary malicious code execution.

## Attack or Failure

- Attack surface: untrusted content, inter-agent messages, and orchestrator
  routing.
- Attack mechanism: indirect prompt injection changes control and communication
  flow.
- System-level failure: compositional authority and action-integrity failure.
- Security consequence: unauthorized invocation and arbitrary code execution.

## Defense

- Defense mechanism: framework-level mitigations are analyzed in the paper.
- Intervention point: routing, communication, and tool invocation boundaries.
- Required observability: system control flow and invoked functionality.
- Assumptions: defenses must mediate LLM-decided routing and execution.
- Limitations: protection is framework-dependent and does not follow from
  content filtering alone.

## Evaluation

- Evaluated systems: several deployed or proposed LLM multi-agent frameworks.
- Agent configuration: orchestrated specialist agents, including code-capable
  functions.
- Dataset or environment: malicious web and other untrusted-content scenarios.
- Baselines: direct and indirect prompt-injection attacks.
- Metrics: attack success and successful unsafe/code invocation.
- Main results: the authors report arbitrary-code attack success across evaluated
  systems, with rates depending on framework and model.

## Relation to Existing Work

- Claimed research gap: indirect prompt-injection work did not capture
  multi-agent control-flow and communication hijacking.
- Closest related work: indirect prompt injection and tool-using agent attacks.
- Difference from prior work: system routing composes local agent capabilities
  into an unauthorized global action.

## Relevance to Our SoK

- Included concepts: orchestration, control-flow hijacking, distributed
  authority, unsafe tool invocation.
- Taxonomy implications: separates initial prompt injection from the resulting
  compositional authorization failure.
- Supported research questions: how local content compromise crosses agent and
  tool trust boundaries.
- Important limitations: exact exploitability depends on framework architecture
  and enabled functions.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Adversarial content can hijack control and communication to invoke unsafe agents and functions. | Explicit author claim | Paper | Abstract; Introduction | PDF 1-2 | Not applicable | Stated in the official COLM record and paper. |
| The paper compares against direct and indirect prompt injection. | Explicit author claim | Paper | Abstract; evaluation | PDF 1; experiments | Not applicable | The official record describes the comparison. |
| Arbitrary code execution is a compositional authority failure. | Corpus interpretation | Paper | Attack design | PDF 2 onward | Not applicable | Classification follows cross-agent routing to unsafe functionality. |

## Provenance

- Discovery source: prior corpus; COLM OpenReview record
- Discovery query: exact-title search
- Accessed version: published COLM 2025 version
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

