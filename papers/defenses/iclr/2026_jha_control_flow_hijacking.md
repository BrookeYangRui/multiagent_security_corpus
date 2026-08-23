# Breaking and Fixing Defenses Against Control-Flow Hijacking in Multi-Agent Systems

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `defense` · venue `ICLR` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

Title: Breaking and Fixing Defenses Against Control-Flow Hijacking in Multi-Agent Systems

Authors: Rishi Jha; Harold Triedman; Justin Wagle; Vitaly Shmatikov

Year: 2026

Venue: ICLR

DOI: Not reported

Primary URL: https://openreview.net/forum?id=PNU9Rj5RDQ

Open access URL: https://arxiv.org/abs/2510.17276

BibTeX key: jha2026controlflowhijacking

## Paper Type

- Attack
- Defense
- Benchmark
- Evaluation
- Empirical study

## Scope

### System Studied

Magentic-One multi-agent workflows whose orchestrator delegates coding, file, web, video, and execution tasks to black-box specialist agents.

### Multi-Agent Dependency

An indirect prompt injection is laundered through a trusted specialist as a plausible error and repair plan. The orchestrator sees only that agent's report, then changes the invocation sequence and delegates unsafe actions to confused deputies.

### Application Domain

Coding, computer use, email, web, and file workflows.

## Security Model

### Protected Assets

Control-flow integrity, least privilege, confidential data, credentials, files, and execution environment integrity.

### Threat Actor

An external adversary controlling one untrusted content item ingested by a benign member agent.

### Trusted Components

The user and all agents are benign; the defense's planning phase and orchestrator enforcement are trusted.

### Attacker Capabilities

The attacker embeds instructions in a web page, document, message, image, or attachment but does not control the user's prompt or agent internals.

### Security Assumptions

Agents must adapt to apparent faults, the orchestrator relies on summarized member reports, and black-box agent internals and direct tool calls are unavailable to the defense.

## Main Contribution

The paper constructs control-flow hijacking attacks that evade alignment checks by presenting unsafe calls as necessary repairs and laundering them through trusted agents. It introduces CFH-Hard and ControlValve, which generates and enforces task-specific control-flow graphs and edge-level contextual rules.

## Attack or Failure

### Attack Surface

Untrusted content, inter-agent status reports, adaptive replanning, agent selection, and delegated tool authority.

### Attack Mechanism

A fake environmental error includes a plausible recovery sequence that invokes attacker-useful agents; wording is adapted to satisfy broad goal-alignment criteria.

### System-Level Failure

The orchestrator follows an attacker-selected control path, executes code, sends data to an unauthorized recipient, or invokes a privileged agent out of context.

### Security Consequence

Privilege escalation, arbitrary code execution, and cross-principal data exfiltration.

## Defense

### Defense Mechanism

ControlValve generates a context-free grammar of permitted agent-call traces before untrusted input is read, adds contextual rules to each edge, and permits, rejects, or replans each proposed transition.

### Intervention Point

Orchestrator and inter-agent control flow.

### Required Observability

The defense observes the original task, planned agent graph, conversation trace, and every proposed inter-agent transition, but not agent internals or direct tool execution.

### Assumptions

The trusted planning model produces sufficiently accurate graphs and rules, and all relevant agent transitions pass through the enforcing orchestrator.

### Limitations

Generated graphs can be too permissive or restrictive, contextual rules can be wrong, adaptive functionality can be reduced, and enforcement adds runtime overhead.

## Evaluation

### Evaluated Systems

AutoGen Magentic-One with ControlValve, LlamaFirewall, Azure Content Filters, least privilege, or no defense.

### Agent Configuration

One orchestrator plus web, file, video, coding, and execution specialists; a MAS adaptation of AgentDojo Slack is also evaluated.

### Dataset or Environment

CFH-Hard with 16 tasks and 14 attacks across coding and computer-use scenarios, plus modified AgentDojo tasks.

### Baselines

Undefended MAS, least privilege, Azure Content Filters, and LlamaFirewall backed by Llama, GPT-4o-mini, GPT-4o, or o4-mini.

### Metrics

Attack success rate, single-answer task accuracy, LLM-judged open-ended quality, graph parse and completeness rates, and runtime.

### Main Results

The adaptive CFH attacks substantially increase ASR against alignment checking in many tested configurations, while ControlValve blocks all evaluated IPI and CFH attacks and retains comparable benign task performance.

## Relation to Existing Work

### Papers Compared by the Authors

The original control-flow hijacking attack, AgentDojo, InjecAgent, indirect prompt injection, LlamaFirewall, and classical control-flow integrity.

### Claimed Research Gap

Goal-alignment checks do not account for attacker instructions that appear necessary and arrive through trusted delegated agents.

### Closest Related Work

Multi-Agent Systems Execute Arbitrary Malicious Code.

### Difference From Prior Work

This work adapts the original CFH payloads to evade alignment defenses and enforces sequences and contextual provenance instead of broad semantic alignment.

## Relevance to Our SoK

### Included Concepts

External content adversary, delegation, partial observability, confused deputy, control-flow graph, provenance, least privilege, replanning, and verified environment impact.

### Taxonomy Implications

The mechanism is interaction-level control-flow hijacking; the failure is compositional authority and action integrity, with confidentiality impact when delegated agents exfiltrate data.

### Supported Research Questions

Which variables must an orchestration defense observe, and do semantic alignment checks preserve the authorization context of delegated actions?

### Important Limitations

The experiments use one primary orchestration stack and a finite attack suite; zero observed ASR does not establish a formal security guarantee against CFG-conforming attacks.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The attacker controls one untrusted item while users and agents remain benign. | Explicit author claim | Paper | 2 | 2 | Figure 1 | Threat model. |
| CFH launders a fake error and recovery sequence through a trusted member. | Explicit author claim | Paper | 2-3 | 2-3 | Figures 2-3 | Attack construction. |
| ControlValve creates a CFG and edge-specific rules before untrusted content is ingested. | Explicit author claim | Paper | 4 | 4-5 | Figure 4 | Defense design. |
| CFH-Hard contains 16 tasks and 14 attacks across coding and computer use. | Explicit author claim | Paper | 1; 5 | 2; 6 | - | Dataset and setup. |
| ControlValve blocks all evaluated IPI and CFH attacks in the reported tables. | Explicit author claim | Paper | 6.3-6.4 | 8-9 | Tables 1-3 | Attack-defense results. |

## Provenance

### Discovery Source

ICLR OpenReview; arXiv; prior corpus completeness scan.

### Discovery Query

`site:openreview.net "Breaking and Fixing Defenses" multi-agent`

### Accessed Version

Published ICLR 2026 conference paper; full text accessed as arXiv v2.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05
