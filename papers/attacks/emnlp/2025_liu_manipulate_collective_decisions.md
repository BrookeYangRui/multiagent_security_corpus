# Can an Individual Manipulate the Collective Decisions of Multi-Agents?

## Citation

Title: Can an Individual Manipulate the Collective Decisions of Multi-Agents?

Authors: Fengyuan Liu; Rui Zhao; Shuo Chen; Guohao Li; Philip Torr; Lei Han; Jindong Gu

Year: 2025

Venue: EMNLP

DOI: 10.18653/v1/2025.emnlp-main.611

Primary URL: https://aclanthology.org/2025.emnlp-main.611/

Open access URL: https://aclanthology.org/2025.emnlp-main.611.pdf

BibTeX key: liu2025manipulatecollective

## Paper Type

- Attack
- Defense
- Evaluation
- Empirical study

## Scope

### System Studied

LLM multi-agent systems that exchange messages and aggregate individual answers into a collective decision.

### Multi-Agent Dependency

An attacker knows and manipulates only one target agent but optimizes inputs by simulating how that agent's messages influence the rest of the group. Success is defined by changing the collective decision.

### Application Domain

Collaborative reasoning and collective decision-making.

## Security Model

### Protected Assets

Integrity of the final group decision.

### Threat Actor

An external attacker with incomplete information about the collective.

### Trusted Components

Non-target agents, the decision protocol, and evaluation labels are not directly compromised.

### Attacker Capabilities

The attacker can query or model one target agent and construct adversarial inputs for it, but lacks full knowledge of other agents and the complete collaboration process.

### Security Assumptions

The target participates in group communication and its response can influence aggregation.

## Main Contribution

The paper formulates single-member manipulation of a collective as an incomplete-information game and proposes M-Spoiler, which simulates interactions to optimize adversarial examples through a stubborn proxy agent. It evaluates attacks and defenses across collaborative decision tasks.

## Attack or Failure

### Attack Surface

One member's input and its outgoing messages during collective deliberation.

### Attack Mechanism

M-Spoiler optimizes adversarial samples using simulated group interactions and a stubborn agent that persistently advocates the attacker's desired answer.

### System-Level Failure

The final collective decision changes despite the attacker directly targeting only one participant.

### Security Consequence

Collective decision-integrity failure.

## Defense

### Defense Mechanism

The paper evaluates input transformations and collaboration-level mitigation strategies.

### Intervention Point

Target-agent input processing and collective aggregation.

### Required Observability

Input defenses require the target prompt; collaboration defenses require access to member responses.

### Assumptions

The defender can alter input processing or the decision procedure.

### Limitations

The attacker and evaluation operate on tasks with measurable final answers; applicability to open-ended work is less clear.

## Evaluation

### Evaluated Systems

Multiple LLM backbones and multi-agent collaboration configurations.

### Agent Configuration

A directly targeted member, simulated proxy participants, and honest agents exchanging answers before aggregation.

### Dataset or Environment

Question answering, reasoning, and classification tasks listed in the experimental setup.

### Baselines

Standard adversarial attacks that optimize against the target agent without group-interaction simulation.

### Metrics

Target-agent and collective attack success, transferability, and clean-task performance.

### Main Results

The authors report that M-Spoiler manipulates collective decisions more effectively than attacks optimized only for an individual target and transfers under incomplete system knowledge.

## Relation to Existing Work

### Papers Compared by the Authors

Adversarial examples for LLMs, malicious debate agents, and multi-agent robustness studies.

### Claimed Research Gap

Prior work generally assumes direct control of malicious members or broad system knowledge rather than manipulation through one known participant.

### Closest Related Work

MultiAgent Collaboration Attack.

### Difference From Prior Work

M-Spoiler treats influence on unknown peers and the final decision as the optimization target under incomplete information.

## Relevance to Our SoK

### Included Concepts

Indirect member compromise, partial system knowledge, simulated interaction, stubborn advocacy, and collective decision integrity.

### Taxonomy Implications

The paper separates adversary position from compromised fraction: one externally manipulated member can have population-level effects without being a malicious agent by construction.

### Supported Research Questions

How much system knowledge and member control are required to corrupt collective aggregation?

### Important Limitations

The notes should not equate collective misclassification with a general Byzantine agreement violation; the paper evaluates task decisions rather than formal consensus guarantees.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The attacker has information about one target agent rather than the full collective. | Explicit author claim | Paper | 3 | 3-4 | Threat-model diagram | Problem formulation. |
| M-Spoiler models manipulation as an incomplete-information game. | Explicit author claim | Paper | 3 | 3-5 | - | Formal setup. |
| A stubborn proxy simulates persistent influence during attack optimization. | Explicit author claim | Paper | 4 | 5-7 | Method figure | Attack method. |
| Evaluation compares individual-target and collective attack outcomes. | Explicit author claim | Paper | 5 | 7-10 | Main result tables | Experimental design. |
| The outcome is task-decision corruption rather than formal Byzantine agreement. | Interpretation | Paper | 3, 5 | 3-10 | - | Evaluated correctness predicate is the final task answer. |

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
