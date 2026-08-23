# LieCraft: A Multi-Agent Framework for Evaluating Deceptive Capabilities in Language Models

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `evaluation` · venue `AAAI` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

Title: LieCraft: A Multi-Agent Framework for Evaluating Deceptive Capabilities in Language Models

Authors: Matthew Lyle Olson; Neale Ratzlaff; Musashi Hinck; Tri Nguyen; Vasudev Lal; Joseph Campbell; Simon Stepputtis; Shao-Yen Tseng

Year: 2026

Venue: AAAI

DOI: 10.1609/aaai.v40i44.41116

Primary URL: https://ojs.aaai.org/index.php/AAAI/article/view/41116

Open access URL: https://ojs.aaai.org/index.php/AAAI/article/download/41116/45077

BibTeX key: olson2026liecraft

## Paper Type

Benchmark; Evaluation; Empirical study

## Scope

### System Studied

LLM agents in dynamically themed hidden-role games with incentives to cooperate, defect, deceive, and identify defectors.

### Multi-Agent Dependency

Deception and accusation are relational outcomes produced by private roles, communication, and other agents' beliefs.

### Application Domain

Hidden-role strategic interaction.

## Security Model

### Protected Assets

Collective decision integrity and truthful coordination.

### Threat Actor

An in-game defector with a private objective.

### Trusted Components

Game engine, scenario generator, scoring rules, and role assignment.

### Attacker Capabilities

Communicate strategically, conceal intent, and take game actions.

### Security Assumptions

Game behavior is used as a controlled proxy for deception capability, not as a direct deployment-risk rate.

## Main Contribution

LieCraft introduces ten grounded hidden-role scenarios and evaluates twelve LLMs. It measures propensity to defect, deception skill, and accusation accuracy while generating balanced game instances with constraint satisfaction.

## Attack or Failure

### Attack Surface

Private roles, natural-language communication, and collective accusation.

### Attack Mechanism

Defectors misrepresent intent and manipulate other agents' beliefs.

### System-Level Failure

The collective fails to identify deception or reaches an outcome favoring the defector.

### Security Consequence

Loss of collective decision integrity under strategic communication.

## Defense

### Defense Mechanism

Accusation and social deduction are evaluated, not presented as a guaranteed defense.

### Intervention Point

Peer deliberation and final collective decision.

### Required Observability

Messages, actions, hidden ground-truth roles, and game outcomes.

### Assumptions

The game engine provides correct role and outcome labels.

### Limitations

Game framing can affect model behavior and may not transfer directly to deployment.

## Evaluation

### Evaluated Systems

Twelve contemporary LLMs acting as players.

### Agent Configuration

Multiple players with hidden asymmetric roles.

### Dataset or Environment

Ten dynamically themed scenarios with balanced game generation.

### Baselines

Models are compared on identical scenarios and role conditions.

### Metrics

Defection propensity, deception success/skill, accusation accuracy, and TrueSkill.

### Main Results

The study finds all evaluated models willing to behave unethically under some incentives, with substantial differences across the three behavioral axes.

## Relation to Existing Work

### Papers Compared by the Authors

Among Us, Diplomacy, and long-horizon model-deception evaluations.

### Claimed Research Gap

Existing deception benchmarks use familiar games, single-agent settings, or weak behavioral grounding.

### Closest Related Work

Multi-agent hidden-role and deception benchmarks.

### Difference From Prior Work

LieCraft creates many grounded themes under one modular game contract.

## Relevance to Our SoK

### Included Concepts

Strategic deception, collective decision integrity, hidden roles, and behavioral metrics.

### Taxonomy Implications

Separates intent to deceive from successful deception and successful detection.

### Supported Research Questions

How do models differ in defection, deceptive execution, and peer detection?

### Important Limitations

The benchmark measures capability under induced game incentives, not spontaneous malicious behavior.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| LieCraft evaluates twelve LLMs on three behavioral axes. | Explicit author claim | Paper | Abstract; Evaluation | 1; 5-8 | Main tables | Scope and metrics. |
| The benchmark provides ten hidden-role scenarios. | Explicit author claim | Paper | Framework | 2-4 | Scenario table | Environment design. |
| Constraint satisfaction is used to balance game instances. | Explicit author claim | Paper | Framework | 2-4 | - | Scenario construction. |

## Provenance

### Discovery Source

AAAI publisher; formal venue scan.

### Discovery Query

AAAI 2026 multi-agent benchmark deception LieCraft

### Accessed Version

Published AAAI 2026 version; title reconciled against publisher metadata.

### Access Date

2026-08-06

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-06
