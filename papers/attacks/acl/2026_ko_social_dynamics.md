# Social Dynamics as Critical Vulnerabilities that Undermine Objective Decision-Making in LLM Collectives

## Citation

Title: Social Dynamics as Critical Vulnerabilities that Undermine Objective Decision-Making in LLM Collectives

Authors: Changgeon Ko; Jisu Shin; Hoyun Song; Huije Lee; Eui Jun Hwang; Jong C. Park

Year: 2026

Venue: ACL

DOI: 10.18653/v1/2026.acl-long.1756

Primary URL: https://aclanthology.org/2026.acl-long.1756/

Open access URL: https://aclanthology.org/2026.acl-long.1756.pdf

BibTeX key: ko2026socialdynamics

## Paper Type

- Attack
- Evaluation
- Empirical study

## Scope

### System Studied

A representative LLM agent integrates answers and arguments from separately instantiated peer agents before producing an objective final decision.

### Multi-Agent Dependency

Adversarial peers create social pressure through coalition size, perceived expertise, message length, and rhetoric. The measured vulnerability is the representative agent's response to the surrounding group configuration.

### Application Domain

Collective question answering and delegated decision-making.

## Security Model

### Protected Assets

Accuracy and independence of the representative agent's final decision.

### Threat Actor

One or more adversarial peer agents.

### Trusted Components

The representative agent and task labels are not directly modified.

### Attacker Capabilities

Adversaries provide incorrect positions and vary coalition size, apparent capability, argument length, speaking dominance, and rhetorical style.

### Security Assumptions

The representative consumes peer outputs as decision evidence and lacks authenticated expertise or independent evidence weighting.

## Main Contribution

The paper operationalizes four social vulnerabilities in LLM collectives: conformity, perceived expertise, dominant-speaker influence, and rhetorical persuasion. It runs controlled interventions on adversarial group composition and message characteristics to measure effects on a representative decision-maker.

## Attack or Failure

### Attack Surface

Peer messages and the aggregation context presented to a representative agent.

### Attack Mechanism

Adversarial peers coordinate incorrect recommendations and manipulate social cues such as majority, expertise, verbosity, and rhetoric.

### System-Level Failure

The representative abandons the correct answer and follows adversarial peers.

### Security Consequence

Collective decision-integrity failure through social influence.

## Defense

### Defense Mechanism

No primary defense; the controlled study motivates provenance, expertise verification, and aggregation rules that resist social-pressure cues.

### Intervention Point

Peer-message presentation and collective aggregation.

### Required Observability

A defense would need member identity, evidence quality, coalition structure, and the full set of peer contributions.

### Assumptions

Not reported.

### Limitations

The experiments use a representative-agent architecture and objective-answer tasks; results may not generalize to decentralized systems or open-ended collective work.

## Evaluation

### Evaluated Systems

Multiple LLM families serving as representative and peer agents.

### Agent Configuration

One representative receives five peer responses while the number and properties of adversarial peers are systematically varied.

### Dataset or Environment

Objective question-answering datasets described in the experimental setup.

### Baselines

No-peer and benign-peer controls plus interventions on coalition size, capability, length, order, and rhetorical strategy.

### Metrics

Representative-agent accuracy and decision-change rates.

### Main Results

Accuracy declines with larger adversarial coalitions, more capable peers, and longer arguments. Credibility- and logic-oriented rhetoric also changes decisions in context-dependent ways.

## Relation to Existing Work

### Papers Compared by the Authors

Multi-agent debate, conformity in LLMs, persuasion attacks, and social-psychology studies.

### Claimed Research Gap

Prior collective-agent work emphasizes reasoning performance rather than controlled security analysis of social configuration cues.

### Closest Related Work

MultiAgent Collaboration Attack and persuasion-driven adversarial debate.

### Difference From Prior Work

The paper decomposes social influence into experimentally manipulated group-level factors instead of proposing one prompt attack.

## Relevance to Our SoK

### Included Concepts

Adversarial coalition, majority influence, claimed expertise, speaking dominance, persuasion, and collective decision integrity.

### Taxonomy Implications

Social configuration is an attack mechanism and precondition, not a separate security property; the violated property remains decision integrity.

### Supported Research Questions

Which coalition and message features amplify malicious-member influence on collective decisions?

### Important Limitations

This paper sits near the security/safety boundary; it is included because adversarial peers intentionally manipulate an objective decision, not merely because social behavior is undesirable.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Four social vulnerabilities are explicitly operationalized. | Explicit author claim | Paper | 3 | 3-5 | Framework figure | Study design. |
| Coalition size, peer capability, argument length, and rhetoric are controlled. | Explicit author claim | Paper | 3-4 | 4-8 | Experiment tables | Independent variables. |
| Larger adversarial groups reduce representative accuracy. | Explicit author claim | Paper | 5 | 8-12 | Main results | Conformity finding. |
| Expertise and longer arguments increase adversarial influence. | Explicit author claim | Paper | 5 | 10-15 | Result figures | Social-context findings. |
| Inclusion as security depends on intentional adversarial manipulation of objective decisions. | Interpretation | Paper | 3-5 | 3-15 | - | Scope boundary. |

## Provenance

### Discovery Source

ACL Anthology; systematic search.

### Discovery Query

site:aclanthology.org/2026.acl-long multi-agent attack security LLM collusion topology

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
