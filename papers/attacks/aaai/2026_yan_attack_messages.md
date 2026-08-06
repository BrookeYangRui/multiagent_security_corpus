# Attack the Messages, Not the Agents: A Multi-round Adaptive Stealthy Tampering Framework for LLM-MAS

## Citation

Title: Attack the Messages, Not the Agents: A Multi-round Adaptive Stealthy Tampering Framework for LLM-MAS

Authors: Bingyu Yan; Xiaoming Zhang; Ziyi Zhou; Chaozhuo Li; Ruilin Zeng; Yirui Qi; Tianbo Wang; Litian Zhang

Year: 2026

Venue: AAAI

DOI: 10.1609/aaai.v40i35.40224

Primary URL: https://ojs.aaai.org/index.php/AAAI/article/view/40224

Open access URL: https://ojs.aaai.org/index.php/AAAI/article/download/40224/44185

BibTeX key: yan2026mast

## Paper Type

- Attack
- Evaluation
- Empirical study

## Scope

### System Studied

LLM multi-agent systems using flat, chain, or hierarchical message-passing architectures.

### Multi-Agent Dependency

The adversary controls some communication links, observes messages across rounds, and adaptively rewrites them while leaving agent states unchanged. The attack objective is deviation of the joint task outcome through the communication transcript.

### Application Domain

Collaborative coding, research, and knowledge reasoning.

## Security Model

### Protected Assets

Integrity of inter-agent messages and the final collective task outcome.

### Threat Actor

An on-path communication adversary.

### Trusted Components

Agent internal states and the message-tampering detector are not directly controlled by the attacker.

### Attacker Capabilities

The attacker intercepts and modifies messages on a subset of links, forwards replacements to the intended recipient, knows the graph, and monitors the system over multiple rounds.

### Security Assumptions

Message links lack strong authentication; the attacker cannot directly alter agent memory or role state; an LLM detector can inspect every transmitted message.

## Main Contribution

MAST learns adaptive multi-round message-tampering plans from MCTS preference pairs using DPO. It decomposes a global attack objective into round-level subgoals and constrains both semantic and embedding similarity to preserve stealth.

## Attack or Failure

### Attack Surface

In-transit inter-agent messages.

### Attack Mechanism

An attack-policy model chooses whether, where, and how to rewrite intercepted messages across rounds while satisfying two similarity thresholds.

### System-Level Failure

Incremental message changes steer the final joint output toward an attacker-selected goal.

### Security Consequence

Communication and collective task-integrity failure.

## Defense

### Defense Mechanism

No new defense; an LLM tamper detector is part of the threat/evaluation model.

### Intervention Point

Message channel.

### Required Observability

The detector sees each original or modified in-transit message and evaluates sender consistency, task relevance, and malicious content.

### Assumptions

The detector is trusted and has enough role/task context to judge individual messages.

### Limitations

The detector is semantic rather than cryptographic, experiments use small fixed architectures, and the attacker assumes continuous link monitoring.

## Evaluation

### Evaluated Systems

Llama-3.1-70B-Instruct agents and detector, a Llama-3.1-8B attack policy, and GPT-4o as process reward model; transfer tests include other LLMs.

### Agent Configuration

Flat and chain systems use three agents; hierarchical systems use two child agents per parent.

### Dataset or Environment

MultiAgentBench code and research, HumanEval, and physics, biology, and mathematics subsets of MMLU.

### Baselines

Debate-Attack, AutoInject, AiTM-Target, and AiTM-DoS.

### Metrics

Attack Success Rate and message-level stealthiness under the tamper detector.

### Main Results

MAST has the highest reported ASR and stealthiness across the main table's six tasks and three architectures. Similarity ablations show that stealth drops when either constraint is removed.

## Relation to Existing Work

### Papers Compared by the Authors

MultiAgent Collaboration Attack, communication attacks/AiTM, AutoInject, and topology-aware MAS security work.

### Claimed Research Gap

Earlier MAS attacks compromise agents, use overt persuasion, or apply static task-specific message templates.

### Closest Related Work

Red-Teaming LLM Multi-Agent Systems via Communication Attacks.

### Difference From Prior Work

MAST plans coordinated, low-salience modifications over multiple communication rounds.

## Relevance to Our SoK

### Included Concepts

On-path adversary, message read/write capability, graph knowledge, partial link control, multi-round adaptation, and message-local detection.

### Taxonomy Implications

The paper separates an exposed communication surface and attack mechanism from the resulting system-level task-integrity violation.

### Supported Research Questions

What can an on-path attacker accomplish without compromising agent internals, and can local message monitors detect trajectory-level manipulation?

### Important Limitations

ASR is defined by observing the attack goal in the final output, and stealth is tied to one LLM detector rather than authenticated-channel guarantees.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The attacker modifies some links but cannot directly alter agent states. | Explicit author claim | Paper | 3.2 | 3 | - | Adversary capabilities. |
| MAST uses MCTS preference pairs, DPO, and multi-round subgoals. | Explicit author claim | Paper | 4.1 | 3-5 | Figure 2 | Attack-policy training. |
| Semantic and embedding constraints enforce message similarity. | Explicit author claim | Paper | 4.2 | 5 | Equations 10-11 | Stealth constraints. |
| Evaluation spans six tasks and three architectures. | Explicit author claim | Paper | 5.1 | 5-6 | Table 1 | Experimental setup. |
| MAST leads the reported ASR and stealth metrics in the main comparison. | Explicit author claim | Paper | 5.2 | 6 | Table 1 | Main results. |

## Provenance

### Discovery Source

AAAI proceedings; prior corpus.

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
