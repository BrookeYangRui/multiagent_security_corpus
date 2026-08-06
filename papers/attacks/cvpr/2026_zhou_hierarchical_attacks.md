# Hierarchical Attacks for Multi-Modal Multi-Agent Reasoning

## Citation

Title: Hierarchical Attacks for Multi-Modal Multi-Agent Reasoning

Authors: Hao Zhou; Tiru Wu; Yan Jiang; Wanqi Zhou; Junxing Hu; Ai Han

Year: 2026

Venue: CVPR

DOI: Not reported

Primary URL: https://openaccess.thecvf.com/content/CVPR2026/html/Zhou_Hierarchical_Attacks_for_Multi-Modal_Multi-Agent_Reasoning_CVPR_2026_paper.html

Open access URL: https://openaccess.thecvf.com/content/CVPR2026/papers/Zhou_Hierarchical_Attacks_for_Multi-Modal_Multi-Agent_Reasoning_CVPR_2026_paper.pdf

BibTeX key: zhou2026hierarchicalattacks

## Paper Type

- Attack
- Benchmark
- Evaluation
- Empirical study

## Scope

### System Studied

A multimodal MAS with one master, six specialized sub-agents, thirteen tools, shared and private memory, and ReAct, Plan-and-Solve, or Reflexion reasoning.

### Multi-Agent Dependency

HAM3 attacks not only perception but also agent identity, communication links, shared memory, shared context, and reasoning traces whose errors propagate through the hierarchy and final root-agent decision.

### Application Domain

Visual question answering and multimodal reasoning.

## Security Model

### Protected Assets

Integrity and availability of multimodal perception, communication topology, shared memory, reasoning traces, and final answers.

### Threat Actor

An adversary able to perturb one or more system layers.

### Trusted Components

The clean-task oracle and evaluation harness are trusted.

### Attacker Capabilities

Depending on the attack, the adversary perturbs images/text, forges agents, blocks links, pollutes shared memory, modifies shared system context, spoofs tools, or injects reasoning instructions.

### Security Assumptions

The study evaluates a broad capability menu rather than one uniform least-privilege attacker; capability must be interpreted per attack variant.

## Main Contribution

HAM3 organizes multimodal MAS attacks across perception, communication, and reasoning layers and supplies attack implementations for each. It evaluates how local perturbations become local or systemic errors across multiple models and reasoning paradigms.

## Attack or Failure

### Attack Surface

Inputs, communication graph, agent identities, shared memory/context, tools, and intermediate reasoning.

### Attack Mechanism

Cross-modal injection; agent spoofing; structural blocking; shared-memory pollution; shared-context injection; tool spoofing; role manipulation; and chain-of-thought injection.

### System-Level Failure

Attacks disrupt expertise flow or cause several agents to converge on consistent wrong outputs.

### Security Consequence

Collective decision integrity, topology integrity, shared-state integrity, and availability failure.

## Defense

### Defense Mechanism

No implemented defense.

### Intervention Point

Not applicable.

### Required Observability

The findings imply that defense requires visibility across perception, graph structure, shared state, and reasoning rather than one output filter.

### Assumptions

Not applicable.

### Limitations

Attack variants assume different privileges, use one main OxyGent configuration, and primarily evaluate sampled GQA plus supplementary EvoChart-QA.

## Evaluation

### Evaluated Systems

OxyGent with Qwen2.5-VL-7B/32B, GLM-4V-Plus, o1-mini, and GPT-4o.

### Agent Configuration

One master, six specialized sub-agents, thirteen tools, shared/private memory, and three reasoning paradigms.

### Dataset or Environment

5,984 sampled GQA image-question pairs across ten semantic categories, with supplementary EvoChart-QA results.

### Baselines

Visual injection, textual injection, tool spoofing, and role manipulation, plus clean configurations.

### Metrics

Task Success Rate, Attack Success Rate over clean-correct samples, Hallucination Error Rate, Cross-Modal Consistency, and local/systemic error shares.

### Main Results

Chain-of-thought injection reaches the highest reported ASR, 78.3%, in the ReAct/Qwen-7B setting. Structural blocking is the strongest communication-layer attack in the corresponding analysis, and more than half of successful perception and reasoning attacks are systemic errors.

## Relation to Existing Work

### Papers Compared by the Authors

Communication attacks, faulty-agent collaboration, prompt injection, tool spoofing, and multimodal-agent attacks.

### Claimed Research Gap

Earlier work treats isolated content or single-agent vulnerabilities without jointly analyzing multimodal perception, structural communication, and collective reasoning.

### Closest Related Work

Red-Teaming LLM Multi-Agent Systems via Communication Attacks.

### Difference From Prior Work

HAM3 compares attack effects across multiple system layers and distinguishes localized from coordinated failures.

## Relevance to Our SoK

### Included Concepts

Multimodal inputs, topology modification, Sybil-like agent spoofing, shared-memory poisoning, tool compromise, reasoning corruption, and systemic-error measurement.

### Taxonomy Implications

The paper's three layers are attack loci, while its variants cause several distinct system-property violations; they should not become one undifferentiated risk category.

### Supported Research Questions

Where do attacks enter multimodal MAS, which privileges do they assume, and when does a local perturbation become a coordinated failure?

### Important Limitations

This attack-and-benchmark paper should be referenced from evaluations later without duplicating its canonical record.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| HAM3 separates perception, communication, and reasoning attack loci. | Explicit author claim | Paper | 3 | 42333-42335 | Figure 2 | Framework. |
| Communication attacks include spoofing, blocking, shared-memory pollution, and context injection. | Explicit author claim | Paper | 3.3 | 42334-42335 | - | Attack definitions. |
| The MAS has one master, six sub-agents, thirteen tools, and shared/private memory. | Explicit author claim | Paper | 4.1 | 42335 | - | System setup. |
| Chain-of-thought injection reaches 78.3% ASR in the reported setting. | Explicit author claim | Paper | 4.2 | 42336 | Table 2 | Main result. |
| Systemic errors exceed local errors for perception and reasoning attacks. | Explicit author claim | Paper | 4.3 | 42338 | Figure 5 | Error propagation analysis. |

## Provenance

### Discovery Source

CVF Open Access; systematic search.

### Discovery Query

site:openaccess.thecvf.com CVPR 2026 multi-agent LLM attack

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
