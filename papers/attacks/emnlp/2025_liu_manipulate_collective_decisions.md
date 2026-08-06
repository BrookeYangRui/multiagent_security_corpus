# Can an Individual Manipulate the Collective Decisions of Multi-Agents?

> **Source-review correction:** The Source Review section at the end supersedes inconsistent automated coding in this note. It still requires author signoff.

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

Attack; Defense evaluation; Empirical study

- Primary category: `attack`
- Scope relation: `core_security`

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

<!-- SOURCE_REVIEW_START -->
## Source Review

**Status:** `source_reviewed_pending_author_signoff`

**Outcome:** Ready after minor patch

**Review source:** `reviews/universal/universal_114_source_review.csv`

This section supersedes inconsistent automated coding elsewhere in this note.
It is a source-level review, not human verification. Manuscript-facing claims
still require author or designated-reviewer signoff.

### Identity and Scope

- Identity: Canonical EMNLP 2025 version confirmed. Metadata is correct.
- Recommended scope: `core_security`
- Multi-agent dependency: The attacker manipulates one known member and optimizes for a change in the collective decision under incomplete information about the rest of the group.
- Recommended roles: attack; defense evaluation; empirical study
- Maturity: Archival peer-reviewed primary attack evidence.

### Threat and Failure Coding

- Attacker or fault actor: External attacker with information about one target participant rather than the full collective.
- Capabilities: Constructs adversarial inputs for the target and simulates group interactions through a stubborn proxy.
- Preconditions: The targeted member participates in communication and can influence majority or consensus-like aggregation.
- Surfaces: Target-agent input; outgoing messages; collective aggregation.
- Mechanism: M-Spoiler optimizes a persistent adversarial influence using simulated group interactions.
- Primary system-level failure: F4 collective task-decision integrity failure.
- Impact: Incorrect or attacker-chosen group answer.

### Evaluation Contract

- Configuration: Multiple LLM backbones and collaboration sizes, including experiments scaling to 101 agents.
- Topology: Communication and majority aggregation settings specified by the paper.
- Baseline or ablation: Individual-target adversarial attacks without group-interaction simulation and evaluated mitigation variants.
- Metric: Targeted and untargeted collective attack success, transferability, and clean-task performance.
- Unit: Task and final group decision.
- Denominator: Evaluated tasks across three seeds; targeted success uses all-agree for two agents or majority target output for larger groups.
- Result boundary: M-Spoiler outperforms attacks optimized only for the individual target in evaluated tasks and transfers under incomplete system knowledge.

### Evidence and Boundaries

- Evidence locations: Threat model and incomplete-information game in Sec. 3, PDF pp. 3 to 5; stubborn proxy in Sec. 4, PDF pp. 5 to 7; main result tables in Sec. 5, PDF pp. 7 to 10; metric definition and three-seed reporting in evaluation.
- Author claim versus corpus interpretation: Threat model, method, and task decision results are author claims. The statement that this is not formal Byzantine agreement is a corpus interpretation based on the correctness predicate.
- Limitations: Simplified collaboration and measurable-answer tasks; majority voting; open-ended systems less clear; no classical agreement, validity, or termination guarantee.

### Required Corrections

- **HIGH - Metric definition:** Store targeted and untargeted collective predicates exactly.
- **HIGH - BFT boundary:** Do not describe this as Byzantine agreement or a fault-threshold result.
- **MEDIUM - Scale:** Record the up-to-101-agent result with its specific task and aggregation assumptions.
<!-- SOURCE_REVIEW_END -->
