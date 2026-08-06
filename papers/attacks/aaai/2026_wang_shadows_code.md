# Shadows in the Code: Exploring the Risks and Defenses of LLM-based Multi-Agent Software Development Systems

## Citation

Title: Shadows in the Code: Exploring the Risks and Defenses of LLM-based Multi-Agent Software Development Systems

Authors: Xiaoqing Wang; Keman Huang; Bin Liang; Hongyu Li; Xiaoyong Du

Year: 2026

Venue: AAAI

DOI: 10.1609/aaai.v40i44.41134

Primary URL: https://ojs.aaai.org/index.php/AAAI/article/view/41134

Open access URL: https://ojs.aaai.org/index.php/AAAI/article/download/41134/45095

BibTeX key: wang2026shadowscode

## Paper Type

- Attack
- Defense
- Benchmark
- Evaluation
- Empirical study

## Scope

### System Studied

End-to-end multi-agent software-development systems using design, coding, and testing roles in ChatDev, MetaGPT, and AgentVerse.

### Multi-Agent Dependency

The paper studies malicious requirements entering through a user and benign requirements interacting with compromised role agents. It varies which development phase is compromised or defended and measures the final software assembled through the workflow.

### Application Domain

Software engineering.

## Security Model

### Protected Assets

Integrity, executability, and benign functionality of generated software.

### Threat Actor

A malicious user or compromised third-party development agent.

### Trusted Components

Uncompromised agents, evaluation sandboxes, and result judges are trusted.

### Attacker Capabilities

A user can mix malicious behavior with benign requirements, or an adversary can alter selected agent profiles in design, coding, or testing stages.

### Security Assumptions

Agents exchange artifacts through the framework workflow and generated software is executed only in a controlled evaluation environment.

## Main Contribution

The paper introduces Implicit Malicious Behavior Injection Attack (IMBIA), a software-oriented test set, and Adv-IMBIA defenses. It distinguishes malicious-user/benign-agent and benign-user/malicious-agent scenarios and identifies critical attack and intervention stages.

## Attack or Failure

### Attack Surface

User requirements, agent role profiles, and cross-stage software artifacts.

### Attack Mechanism

IMBIA combines a benign software request with an implicit malicious behavior; in the compromised-agent scenario, malicious instructions are embedded in selected role profiles.

### System-Level Failure

The team produces executable software that satisfies benign requirements while covertly implementing malicious operations.

### Security Consequence

Compositional action-integrity failure and malicious code generation.

## Defense

### Defense Mechanism

Adv-IMBIA adds security instructions at the user interface or selected agent-profile stages.

### Intervention Point

User input and design, coding, or testing role prompts.

### Required Observability

The defense needs software requirements or the protected role's prompt and generated artifacts.

### Assumptions

The operator can harden selected profiles and retain control of the framework prompts.

### Limitations

Prompt hardening does not provide a formal authorization guarantee, and evaluation covers three research frameworks and a synthetic malicious-requirement set.

## Evaluation

### Evaluated Systems

ChatDev, MetaGPT, and AgentVerse across multiple base models.

### Agent Configuration

Design, coding, and testing stages are attacked or defended individually and in combinations.

### Dataset or Environment

Benign tasks from the Software Requirement Description Dataset paired with malicious software behaviors such as trojan, spyware, and adware functions.

### Baselines

Different attacked stages, defense placements, frameworks, and base models.

### Metrics

Benign utility, utility under attack, consistency, refusal rate, Attack Success Rate, and defense-adjusted ASR/refusal.

### Main Results

IMBIA succeeds across all three systems. The most influential attack and defense stage differs by framework, and hardening only the identified critical stage approaches the effectiveness of defending all agents.

## Relation to Existing Work

### Papers Compared by the Authors

Single coding-agent security benchmarks, jailbreak attacks, and multi-agent software-development frameworks.

### Claimed Research Gap

Prior code-agent security work does not evaluate distributed attack points and cross-stage propagation in end-to-end software teams.

### Closest Related Work

Security evaluation of code agents and prompt attacks against multi-agent workflows.

### Difference From Prior Work

The study localizes attack and defense effects to role stages and includes compromised-agent supply-chain scenarios.

## Relevance to Our SoK

### Included Concepts

Heterogeneous roles, distributed authority, malicious user, compromised member, cross-stage artifacts, action integrity, and defense placement.

### Taxonomy Implications

It illustrates how individually scoped role capabilities compose into unauthorized final software behavior.

### Supported Research Questions

Which role positions dominate attack propagation and where can limited defense resources be placed most effectively?

### Important Limitations

Its benchmark and dataset should later be indexed under evaluations without duplicating this canonical attack record.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| IMBIA covers malicious-user and compromised-agent scenarios. | Explicit author claim | Paper | Methodology | 3-4 | Figure 2 | Attack scenarios. |
| Attacks and defenses are localized to design, code, and test stages. | Explicit author claim | Paper | Methodology | 4-5 | Figure 2 | Stage formalization. |
| Three software-development MAS frameworks are evaluated. | Explicit author claim | Paper | Experiment | 5 | - | System setup. |
| The critical stage differs across ChatDev, MetaGPT, and AgentVerse. | Explicit author claim | Paper | Attack/Defense Results | 6-8 | Figures 4-5 | Cross-framework analysis. |
| Targeted critical-stage defense nearly matches all-stage defense. | Explicit author claim | Paper | Defense Results | 8 | Figure 5 | Resource-efficient defense result. |

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
