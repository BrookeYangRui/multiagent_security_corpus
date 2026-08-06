# WeClawArena: An Auditable Sandbox and Benchmark for Cross-User Agents Collaboration and Security in Human-Centered Agent Networks

## Citation

Title: WeClawArena: An Auditable Sandbox and Benchmark for Cross-User Agents Collaboration and Security in Human-Centered Agent Networks

Authors: Prince Zizhuang Wang; Aojie Yuan; Haiyue Zhang; Xiyang Hu; Yue Zhao; Shuli Jiang

Year: 2026

Venue: arXiv

DOI: 10.48550/arXiv.2608.03499

Primary URL: https://arxiv.org/abs/2608.03499

Open access URL: https://arxiv.org/pdf/2608.03499

BibTeX key: wang2026weclawarena

## Paper Type

Benchmark; Evaluation; Attack; Empirical study

## Scope

### System Studied
Persistent personal agents acting for separate users over private workspaces and communicating through social and task relations.

### Multi-Agent Dependency
No agent can directly inspect another owner's workspace; collaboration, authority, and harmful propagation cross user-agent boundaries.

### Application Domain
Bargaining, trading, clinical work, software engineering, bidding, and travel.

## Security Model

### Protected Assets
Personal workspace data, resource authorization, evidence integrity, and collaborative utility.

### Threat Actor
Malicious user, agent, message, or resource along the cross-user path.

### Trusted Components
Runtime sandbox, governed-decision layer, task oracle, and bounded evidence recorder.

### Attacker Capabilities
Four attack-vector variants per base task can induce privacy leakage, poisoned evidence, invalid authority paths, or task breakdown.

### Security Assumptions
Workspace operations and governed decisions are completely logged by the sandbox.

## Main Contribution

WeClawArena provides 124 base tasks in six cross-user domains and expands them into 620 variants: one benign control and four attack variants per task. Its sandbox records peer messages, tool calls, resource operations, governed decisions, and final workspace state for bounded-evidence auditing.

## Attack or Failure

### Attack Surface
Peer messages, private workspaces, tools, resources, and delegated decisions.

### Attack Mechanism
Harmful content or invalid authority travels across user-agent collaboration paths.

### System-Level Failure
Task breakdown, privacy leakage, poisoned evidence, or unauthorized action.

### Security Consequence
Cross-principal confidentiality, integrity, and compositional authority failure.

## Defense

### Defense Mechanism
Governed decisions and trace auditing; the benchmark is not a complete preventive defense.

### Intervention Point
Message, tool, resource, decision, and final-state boundaries.

### Required Observability
Full cross-user trace and final workspace state.

### Assumptions
Bounded runtime evidence is sufficient to verify attack success.

### Limitations
The OpenClaw-style sandbox and synthetic task variants do not establish real-world prevalence.

## Evaluation

### Evaluated Systems
Multiple frontier and open LLM agents.

### Agent Configuration
Human-owned agents with private workspaces and A2A collaboration.

### Dataset or Environment
124 base tasks, six domains, and 620 benign/adversarial variants.

### Baselines
Benign controls paired with four attack-vector variants.

### Metrics
Utility and Attack Success Rate reported separately, verified from runtime evidence.

### Main Results
The benchmark reports substantial model-level variation in attack resistance and diagnoses several cross-user failure types.

## Relation to Existing Work

### Papers Compared by the Authors
Tool-use, collaboration, privacy, and agent-security benchmarks.

### Claimed Research Gap
Existing benchmarks lack end-to-end cross-user workspaces and verifiable harmful propagation.

### Closest Related Work
A2ASecBench, AgentLeak, and CalBench.

### Difference From Prior Work
Each task is grounded in separately owned workspaces and audited resource operations.

## Relevance to Our SoK

### Included Concepts
Principals, private state, authority, A2A messaging, tool use, provenance, and global traces.

### Taxonomy Implications
Makes principal and authority boundaries first-class evaluation fields.

### Supported Research Questions
How do attacks cross user-owned agent and workspace boundaries?

### Important Limitations
Released after the earlier 2026-07-01 manuscript cutoff and should be labeled as a post-cutoff update if used in that paper.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The benchmark has 124 base tasks, six domains, and 620 variants. | Explicit author claim | Paper | Abstract; 3 | 1; 5-8 | Dataset tables | Benchmark scale. |
| Each base task has one benign and four attack variants. | Explicit author claim | Paper | Abstract; 3 | 1; 5-8 | - | Pairing contract. |
| The sandbox records messages, tools, resources, decisions, and final states. | Explicit author claim | Paper | Abstract; 4 | 1; 8-11 | System figure | Observer scope. |

## Provenance

### Discovery Source
arXiv; final completeness audit.

### Discovery Query
multi-agent security benchmark cross-user collaboration 2026

### Accessed Version
arXiv v1.

### Access Date
2026-08-06

### Prepared By
Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status
agent_unverified

### Last Updated
2026-08-06
