# Deception and Communication in Autonomous Multi-Agent Systems: An Experimental Study with Among Us

## Citation

Title: Deception and Communication in Autonomous Multi-Agent Systems: An Experimental Study with Among Us

Authors: Maria Milkowski; Tim Weninger

Year: 2026

Venue: AAMAS

DOI: 10.65109/FRXL8789

Primary URL: https://doi.org/10.65109/FRXL8789

Open access URL: https://arxiv.org/abs/2603.26635

BibTeX key: milkowski2026amongus

## Paper Type

Evaluation; Empirical study

## Scope

### System Studied

Autonomous LLM players communicating and acting in an Among Us environment with hidden asymmetric roles.

### Multi-Agent Dependency

Deception, trust, accusation, and winning depend on messages and beliefs among multiple role-bearing agents.

### Application Domain

Hidden-role social deduction.

## Security Model

### Protected Assets

Truthful coordination and collective identification of malicious participants.

### Threat Actor

Impostor agents whose game objective conflicts with the crew.

### Trusted Components

Game engine, role assignment, event log, and behavioral coding procedure.

### Attacker Capabilities

Act strategically and communicate using falsification or equivocation.

### Security Assumptions

The game provides ground truth for roles, actions, and final outcomes.

## Main Contribution

The study analyzes approximately 1,100 autonomous games and more than one million generated tokens. It connects speech-act and interpersonal-deception coding with behavioral outcomes such as detection and win rate.

## Attack or Failure

### Attack Surface

Natural-language discussion, accusations, voting, and hidden role information.

### Attack Mechanism

Impostors falsify claims or equivocate to influence group belief and voting.

### System-Level Failure

The group fails to identify the impostor or makes an incorrect collective decision.

### Security Consequence

Collective decision-integrity failure under deceptive communication.

## Defense

### Defense Mechanism

No deployed defense; peer detection and accusation behavior are measured.

### Intervention Point

Discussion and voting.

### Required Observability

Full dialogue, ground-truth roles, actions, and outcomes.

### Assumptions

Behavior in the game is a proxy for autonomous-agent deception.

### Limitations

Results from one game environment may not generalize to open-ended workflows.

## Evaluation

### Evaluated Systems

LLM-controlled Among Us players.

### Agent Configuration

Crew and impostor roles interacting over repeated game phases.

### Dataset or Environment

Approximately 1,100 games and over one million generated tokens.

### Baselines

Roles, model configurations, and communication behaviors are compared.

### Metrics

Win rate, deception categories, speech acts, and detection outcomes.

### Main Results

Models exhibit distinguishable falsification and equivocation patterns, with communication behavior associated with game outcomes.

## Relation to Existing Work

### Papers Compared by the Authors

LLM game agents, social deduction, and deception studies.

### Claimed Research Gap

Prior work rarely links large-scale autonomous interaction logs to structured deception behavior.

### Closest Related Work

LieCraft and other hidden-role evaluations.

### Difference From Prior Work

This work emphasizes empirical communication analysis in a fixed autonomous game environment.

## Relevance to Our SoK

### Included Concepts

Deception, hidden roles, communication, collective decisions, and full-trace observation.

### Taxonomy Implications

Distinguishes deception mechanism from decision outcome.

### Supported Research Questions

Which communicative deception strategies occur in autonomous multi-agent play?

### Important Limitations

The adversarial objective is explicitly assigned by the game.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The study analyzes about 1,100 games and more than one million tokens. | Explicit author claim | Paper | Abstract; Methods | 1; 3-5 | - | Evaluation scale. |
| Falsification and equivocation are coded separately. | Explicit author claim | Paper | Methods | 4-6 | Coding table | Deception construct. |
| Game outcomes and communication behavior are analyzed together. | Explicit author claim | Paper | Results | 6-10 | Results figures | Evaluation contract. |

## Provenance

### Discovery Source

AAMAS DOI record; arXiv; formal venue scan.

### Discovery Query

AAMAS 2026 deception communication autonomous multi-agent Among Us

### Accessed Version

Published AAMAS 2026 metadata with arXiv full text.

### Access Date

2026-08-05
### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05
