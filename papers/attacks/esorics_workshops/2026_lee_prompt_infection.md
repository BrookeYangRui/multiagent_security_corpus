# Prompt Infection: LLM-to-LLM Prompt Injection within Multi-agent Systems

## Citation

Title: Prompt Infection: LLM-to-LLM Prompt Injection within Multi-agent Systems

Authors: Donghyun Lee; Mo Tiwari; Brando Miranda

Year: 2026

Venue: ESORICS 2025 International Workshops

DOI: 10.1007/978-3-032-16092-8_28

Primary URL: https://link.springer.com/chapter/10.1007/978-3-032-16092-8_28

Open access URL: https://arxiv.org/abs/2410.07283

BibTeX key: lee2026promptinfection

## Paper Type

- Attack
- Defense
- Benchmark
- Evaluation
- Empirical study

## Scope

### System Studied

Tool-using LLM workflows with global or local message histories and agent societies with changing pairwise conversations.

### Multi-Agent Dependency

One externally injected prompt forces each compromised agent to append a self-replicating payload to downstream messages. Infection spreads through communication even to agents that never read the original untrusted content.

### Application Domain

Document, email, and web workflows; data access; coding; and agent-society simulation.

## Security Model

### Protected Assets

Agent role integrity, sensitive database contents, tool authority, output integrity, and population containment.

### Threat Actor

An external adversary able to place one infectious prompt in a PDF, email, or web page.

### Trusted Components

Agents are initially benign; downstream agents and tools are not directly controlled before propagation.

### Attacker Capabilities

The payload hijacks the first reader, assigns role-specific malicious tasks, carries stolen state, and tells each agent to reproduce it in the next message.

### Security Assumptions

Agents follow instructions embedded in untrusted content and pass attacker-controlled text through global or predecessor-local communication.

## Main Contribution

The paper introduces Prompt Infection, a self-replicating LLM-to-LLM injection that propagates through role-specialized workflows and dynamic agent societies. It evaluates data theft, scams, content manipulation, malware, and LLM Tagging combined with existing prompt defenses.

## Attack or Failure

### Attack Surface

External content, inter-agent messages, partial histories, memory retrieval, and tool-bearing roles.

### Attack Mechanism

Prompt hijacking changes the current role, a payload assigns malicious subtasks and carries data, and a self-replication instruction preserves the infection across agent edges.

### System-Level Failure

Multiple agents abandon their intended roles, collaborate to retrieve and exfiltrate data, emit manipulated content, or infect a population.

### Security Consequence

Behavioral contagion with confidentiality, integrity, and action-authority impact.

## Defense

### Defense Mechanism

LLM Tagging prepends the producing agent's identity to downstream messages and is combined with marking, instruction, reminder, and sandwich defenses.

### Intervention Point

Inter-agent message provenance and receiving-agent prompt.

### Required Observability

The defense must know which principal produced each message and preserve that marker downstream.

### Assumptions

Receiving models treat tagged agent content as less authoritative and tags cannot be forged or stripped.

### Limitations

LLM Tagging and each tested prompt defense are weak in isolation; the mechanism is not cryptographically authenticated.

## Evaluation

### Evaluated Systems

Multi-agent applications and societies using GPT-4o and GPT-3.5-class models.

### Agent Configuration

Role-specialized chains with global or local messaging and random pairwise populations of 10 to 50 agents.

### Dataset or Environment

120 user instructions across email, PDF, and web inputs, with synthetic malicious documents and multiple attack objectives.

### Baselines

Non-replicating injection and four established prompt-defense families, with and without LLM Tagging.

### Metrics

Scenario-specific attack success, fraction or count of infected agents over turns, time to full infection, and defense ASR.

### Main Results

The paper reports successful multi-hop infection under global and local messaging and full population spread in tested societies; combining message marking with LLM Tagging blocks all tested attacks, while tagging alone reduces ASR only slightly.

## Relation to Existing Work

### Papers Compared by the Authors

Indirect prompt injection, AI worms, Agent Smith, prompt-defense methods, and multi-agent safety evaluations.

### Claimed Research Gap

Prior prompt-injection work focused on one victim or users sharing an application rather than self-replication between role-specialized agents.

### Closest Related Work

Agent Smith and Morris II.

### Difference From Prior Work

The payload propagates through ordinary inter-agent text and assigns different malicious actions according to each recipient's role and tools.

## Relevance to Our SoK

### Included Concepts

External seed, replication, global versus local history, role-specific payload, message provenance, population size, tool composition, and containment.

### Taxonomy Implications

Self-replication is the attack mechanism; the system-level failure is propagation and containment, with separate impact fields for theft, manipulation, or execution.

### Supported Research Questions

Which topology and provenance assumptions control infection, and how should infection severity distinguish per-hop compromise from final system impact?

### Important Limitations

The evaluated population uses simplified random dialogues, the prompt marker is forgeable text, and attack metrics differ across workflow and society experiments.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Prompt Infection contains hijacking, role-specific payload, and self-replication components. | Explicit author claim | Paper | 3 | 3-4 | Figure 1 | Attack definition. |
| The workflow dataset has 120 instructions across email, PDF, and web inputs. | Explicit author claim | Paper | 4.1 | 5 | - | Application setup. |
| Global and local message-history settings are evaluated. | Explicit author claim | Paper | 4.1 | 5 | Figure 4 | Communication comparison. |
| Populations of 10 to 50 agents use random pairwise dialogues. | Explicit author claim | Paper | 4.2 | 6-7 | Figure 6 | Society evaluation. |
| Tagging is most effective when combined with other prompt defenses. | Explicit author claim | Paper | 6 | 8-9 | Table 2; Figure 7 | Defense results. |

## Provenance

### Discovery Source

Springer proceedings; Crossref; arXiv; prior corpus completeness scan.

### Discovery Query

`Prompt Infection LLM-to-LLM Springer ESORICS`

### Accessed Version

Published ESORICS workshop chapter metadata; technical extraction from arXiv v1. The published version adds Brando Miranda to the author list.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05

