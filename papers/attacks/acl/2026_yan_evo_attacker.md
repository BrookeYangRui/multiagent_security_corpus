# Evo-Attacker: Memory-Augmented Reinforcement Learning for Long-Horizon Tool Attacks on LLM-MAS

## Citation

Title: Evo-Attacker: Memory-Augmented Reinforcement Learning for Long-Horizon Tool Attacks on LLM-MAS

Authors: Bingyu Yan; Xiaoming Zhang; JinYu Hou; Chaozhuo Li; Ziyi Zhou; Yiming Hei; Litian Zhang

Year: 2026

Venue: ACL

DOI: 10.18653/v1/2026.acl-long.330

Primary URL: https://aclanthology.org/2026.acl-long.330/

Open access URL: https://aclanthology.org/2026.acl-long.330.pdf

BibTeX key: yan2026evoattacker

## Paper Type

- Attack
- Evaluation
- Empirical study

## Scope

### System Studied

Tool-using LLM multi-agent systems with flat, chain, or hierarchical communication architectures across coding, research, and web tasks.

### Multi-Agent Dependency

The attacker modifies one target agent's tool returns at strategically selected times; those perturbations then alter downstream inter-agent messages and global workflow decisions over a long trajectory.

### Application Domain

Code generation, deep research, and web interaction.

## Security Model

### Protected Assets

Correct tool results, task completion, and integrity of the global multi-agent trajectory.

### Threat Actor

An attacker that has compromised a single tool channel.

### Trusted Components

Agent model parameters, inter-agent messages, non-target tools, and the final task oracle remain outside attacker control.

### Attacker Capabilities

The attacker observes the target's tool calls and returns, may replace selected returns under a budget, and can retain successful attack experiences. It cannot read inter-agent messages or internal agent states.

### Security Assumptions

The target agent invokes a compromised external tool and accepts its returned content; system failure can be verified at episode end.

## Main Contribution

Evo-Attacker treats long-horizon tool attacks as a memory-augmented reinforcement-learning process. It retrieves prior attack experiences, reflects on transferability, modifies selected returns, and uses Attack-Flow GRPO to assign terminal failure reward across the attacker's reasoning trajectory.

## Attack or Failure

### Attack Surface

Third-party tool-return channels used by one agent within a collaborative workflow.

### Attack Mechanism

Retrieve a relevant adversarial pattern from dynamic memory, decide whether and when to intervene, and synthesize a schema-valid malicious replacement for a selected tool result.

### System-Level Failure

One corrupted tool observation propagates through downstream agents and degrades the final workflow outcome.

### Security Consequence

Collective task and action-integrity failure.

## Defense

### Defense Mechanism

No new defense; stealth is tested against LLM-based detectors, and cryptographic signing or strict argument allowlists are discussed as orthogonal defenses.

### Intervention Point

Tool boundary and semantic monitoring.

### Required Observability

An LLM monitor observes tool content; deterministic defenses would require trusted tool identity and structured arguments.

### Assumptions

Detection baselines can inspect the modified return.

### Limitations

Training and reasoning are computationally expensive, and the defense analysis does not extensively test signatures or strict allowlists.

## Evaluation

### Evaluated Systems

Qwen3-14B victim agents and a Qwen3-8B attacker across flat, chain, and hierarchical MAS architectures, with additional victim-model tests.

### Agent Configuration

Domain-specialized agents with structured communication and toolkits; one target's tool channel is compromised with an attack budget of three.

### Dataset or Environment

HumanEval, MultiAgentBench coding and research subsets, DeepResearch Bench, WebArena, and WebShop.

### Baselines

Forced Output, InjecAgent, Web Fraud, and Prompt Infection.

### Metrics

Official task metrics: Pass@1, RACE, WebShop score, MultiAgentBench task success, WebArena success rate, and attack-induced degradation.

### Main Results

The authors report the largest performance degradation for Evo-Attacker across all six tasks and three architectures in the main table. Ablations attribute gains to retrieval, reflection, and Attack-Flow GRPO.

## Relation to Existing Work

### Papers Compared by the Authors

InjecAgent, Forced Output, Web Fraud, Prompt Infection, and communication-level MAS attacks.

### Claimed Research Gap

Existing tool attacks use static or domain-specific injections that do not adapt to evolving long-horizon workflows and novel tool schemas.

### Closest Related Work

Web Fraud and Prompt Infection.

### Difference From Prior Work

The attack learns when and how to alter tool returns using reusable attack memory and trajectory-level reinforcement learning.

## Relevance to Our SoK

### Included Concepts

Malicious tool, partial observation, long-horizon attack memory, tool-result integrity, topology, authority distribution, and downstream propagation.

### Taxonomy Implications

The paper distinguishes adversary position at a tool boundary from member-agent compromise and shows how local tool corruption becomes a system-level action-integrity failure.

### Supported Research Questions

How do tool authority, communication architecture, and long-horizon adaptation affect attack transfer across MAS workflows?

### Important Limitations

The experiments use simulated controlled environments, one compromised tool channel, and a learned attacker with substantial computational cost.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The attacker controls one tool channel but cannot inspect inter-agent messages or internal states. | Explicit author claim | Paper | 2.2 | 3 | - | Threat model. |
| Evo-Attacker retrieves, reflects, and modifies tool returns using dynamic attack memory. | Explicit author claim | Paper | 3.1-3.2 | 3-4 | Figure 1 | Attack pipeline. |
| Attack-Flow GRPO applies terminal outcome credit to attacker-generated reasoning steps. | Explicit author claim | Paper | 3.3 | 4-5 | Equations 6-8 | Optimization method. |
| Evaluation spans six tasks, three domains, and three architectures. | Explicit author claim | Paper | 4.1 | 5 | - | Experimental setup. |
| Evo-Attacker produces the largest reported degradation in every main-table setting. | Explicit author claim | Paper | 4.2 | 6 | Table 1 | Main results. |
| High compute cost and limited non-semantic defense evaluation are acknowledged. | Explicit author claim | Paper | Limitations | 9 | - | Limitations statement. |

## Provenance

### Discovery Source

ACL Anthology; prior corpus.

### Discovery Query

Not applicable.

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
