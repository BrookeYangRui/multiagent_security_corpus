# Benchmarking the Robustness of Agentic Systems to Adversarially-Induced Harmful Behaviors

## Citation

Title: Benchmarking the Robustness of Agentic Systems to Adversarially-Induced Harmful Behaviors

Authors: Jonathan Nöther; Adish Singla; Goran Radanovic

Year: 2026

Venue: COLM

DOI: Not reported

Primary URL: https://colmweb.org/AcceptedPapers.html

Open access URL: https://openreview.net/forum?id=WGOj26QIlR

BibTeX key: nother2026badacts

## Paper Type

Benchmark; Evaluation; Attack; Defense; Empirical study

## Scope

### System Studied

LLM-backed agentic systems for travel planning, personal assistance, financial article writing, code generation, and multi-agent debate.

### Multi-Agent Dependency

An attacker controls one member and uses ordinary inter-agent communication to manipulate other agents into executing a target harmful action.

### Application Domain

Travel, personal assistance, finance, software engineering, and debate.

## Security Model

### Protected Assets

Authorization, data confidentiality, safe tool execution, resources, and integrity of the collective task.

### Threat Actor

A compromised member agent inside the system's communication graph.

### Trusted Components

Emulated tools, benchmark evaluators, task harness, and optional guardian monitor.

### Attacker Capabilities

The malicious member sends persuasive or deceptive messages through its legitimate communication interfaces but does not directly control honest agents.

### Security Assumptions

All actions occur in emulated environments and each target harm has an executable evaluation function.

## Main Contribution

BAD-ACTS provides a harm taxonomy, five agentic-system environments, and 937 harmful actions with environment-specific evaluators. It evaluates malicious-member attacks and two baseline defenses, including a message-monitoring guardian.

## Attack or Failure

### Attack Surface

Inter-agent messages, role trust, tool delegation, and shared task execution.

### Attack Mechanism

A controlled member persuades honest peers to perform a specified harmful target action.

### System-Level Failure

The system executes unauthorized, unsafe, privacy-violating, or resource-abusing actions.

### Security Consequence

Loss of action integrity, confidentiality, availability, and user authorization.

## Defense

### Defense Mechanism

Safety warnings in agent prompts and a guardian agent that monitors messages and may block adversarial influence.

### Intervention Point

Agent instruction and inter-agent message layers.

### Required Observability

The guardian requires access to messages crossing the monitored communication boundary.

### Assumptions

The monitor is trusted and can intervene before a harmful action executes.

### Limitations

Tools and harms are emulated; the benchmark covers selected applications, communication structures, and target-action definitions rather than open-world deployment.

## Evaluation

### Evaluated Systems

Open and proprietary LLM backbones instantiated in the five BAD-ACTS environments.

### Agent Configuration

Environment-specific decentralized, hierarchical, centralized, and sequential communication structures with one adversarial member.

### Dataset or Environment

Five environments and 937 curated harmful actions in the accepted version.

### Baselines

Undefended execution, safety-warning prompts, and zero-shot guardian message monitoring.

### Metrics

Environment-specific harmful-action success and task outcomes; the benchmark aggregates attack success across models, roles, harm categories, and communication structures.

### Main Results

The accepted paper reports that all tested model families are regularly manipulated into harmful actions and that message monitoring is more effective than prompt-only warnings.

## Relation to Existing Work

### Papers Compared by the Authors

AgentHarm and prior agent-security evaluation work.

### Claimed Research Gap

Existing safety benchmarks emphasize harmful text or single-agent behavior rather than harmful tool-mediated actions induced by a malicious peer.

### Closest Related Work

TAMAS, ACIARena, AgentHarm, and malicious-member attack studies.

### Difference From Prior Work

BAD-ACTS evaluates concrete harmful actions across multiple agent topologies and application environments with per-action executable checks.

## Relevance to Our SoK

### Included Concepts

Compromised member, communication topology, tool authority, action-level impact, message monitoring, and evaluation denominator.

### Taxonomy Implications

It operationalizes compositional action-integrity failure rather than treating unsafe text as the endpoint.

### Supported Research Questions

How often can one malicious member induce a system-level action, and where must a defense observe and intervene?

### Important Limitations

The formal accepted version expands and renames the earlier arXiv record; counts from the two versions must not be mixed.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| BAD-ACTS contains five environments and 937 harmful actions in the accepted version. | Explicit author claim | Paper | 1 | 2 | - | Accepted-version contribution list. |
| The threat model gives one adversarial agent control of messages sent through its ordinary role. | Explicit author claim | Paper | 1; threat model | 1-2 | Figure 1 | Malicious-member setting. |
| Tools are emulated and target actions have evaluation functions. | Explicit author claim | Paper | Ethics; reproducibility; benchmark design | - | - | Evaluation containment and verification contract. |
| COLM lists the renamed paper as accepted. | Metadata verification | Conference program | Accepted papers | - | - | Official COLM 2026 accepted-paper list. |

## Provenance

### Discovery Source

COLM accepted-paper list; OpenReview; arXiv; benchmark repository.

### Discovery Query

BAD-ACTS multi-agent security benchmark official publication

### Accessed Version

Accepted COLM 2026 version; arXiv v2 retained only for version provenance.

### Access Date

2026-08-06

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-06
