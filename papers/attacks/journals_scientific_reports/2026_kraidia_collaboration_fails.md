# When collaboration fails: persuasion driven adversarial influence in multi agent large language model debate

## Citation

Title: When collaboration fails: persuasion driven adversarial influence in multi agent large language model debate

Authors: Insaf Kraidia; Iyas Qaddara; Alhanof Almutairi; Nada Alzaben; Samir Brahim Belhouari

Year: 2026

Venue: Scientific Reports

DOI: 10.1038/s41598-026-42705-7

Primary URL: https://www.nature.com/articles/s41598-026-42705-7

Open access URL: https://www.nature.com/articles/s41598-026-42705-7.pdf

BibTeX key: kraidia2026collaborationfails

## Paper Type

- Attack
- Defense
- Evaluation
- Empirical study

## Scope

### System Studied

Multi-round LLM debate systems that aggregate independent answers and revisions by majority vote.

### Multi-Agent Dependency

A malicious participant reads peer arguments and repeatedly persuades cooperative agents toward a selected wrong answer. The measured failure is increased agreement with the attacker across debate rounds and a corrupted group vote.

### Application Domain

General knowledge, truthfulness, medical reasoning, and legal reasoning.

## Security Model

### Protected Assets

Accuracy and epistemic integrity of collective decisions.

### Threat Actor

One or more adversarial debate members in an otherwise cooperative group.

### Trusted Components

The dataset labels, experiment controller, and cooperative agents are not directly modified.

### Attacker Capabilities

The adversary sees debate history, targets an incorrect answer, and uses multi-layer arguments, counterarguments, RAG, Best-of-N selection, and persuasive polishing.

### Security Assumptions

All messages are visible within the debate protocol; the controlled attacker receives a designated wrong target for reproducible evaluation.

## Main Contribution

The paper treats persuasion as an inference-time adversarial vector in LLM-to-LLM debate and evaluates a four-stage persuasive attacker. It measures both collective accuracy loss and movement of individual agents toward the adversarial answer.

## Attack or Failure

### Attack Surface

Shared multi-round debate transcript and majority-vote aggregation.

### Attack Mechanism

The malicious member builds multiple supporting narratives, rebuts peers, fuses the material, and selects rhetorically strong arguments for a false conclusion.

### System-Level Failure

Cooperative agents revise toward the adversary and the final majority answer becomes less accurate.

### Security Consequence

Collective decision-integrity failure through adversarial social influence.

## Defense

### Defense Mechanism

The paper evaluates prompt warnings intended to make cooperative agents resist persuasive manipulation.

### Intervention Point

Agent prompt and debate reasoning.

### Required Observability

Each agent sees the warning and dialogue history; no trusted external verifier is added.

### Assumptions

Cooperative models can recognize persuasive manipulation from instructions and transcript content.

### Limitations

Prompt-only mitigation is inconsistent across models and does not reliably stop multi-round influence.

## Evaluation

### Evaluated Systems

Debate groups built from GPT-4o, GPT-3.5, Llama, Mistral, Qwen, and Yi model families.

### Agent Configuration

Multiple cooperative agents and one persuasive adversary over several rounds with final majority vote; group size and round count are varied.

### Dataset or Environment

MMLU, TruthfulQA, MedMCQA, and SCALR from LegalBench.

### Baselines

Honest debate, a lower-capability vanilla adversary, and prompt-warning mitigation.

### Metrics

Change in final majority accuracy and change in the fraction of agents agreeing with the adversarial answer; success requires accuracy loss and increased adversary agreement.

### Main Results

The authors report 10-40% accuracy reductions and more than 30% increases in wrong-answer consensus in tested settings; more agents or rounds and prompt warnings do not consistently remove the effect.

## Relation to Existing Work

### Papers Compared by the Authors

Multi-agent debate, LLM persuasion, RAG, adversarial collaboration, and prompt attacks.

### Claimed Research Gap

Persuasion between LLM agents had not been systematically evaluated as an attack on collaborative debate.

### Closest Related Work

MultiAgent Collaboration Attack and adversarial social-influence studies.

### Difference From Prior Work

The attack optimizes rhetoric and selectively retrieved support at inference time rather than changing model parameters or directly injecting a jailbreak.

## Relevance to Our SoK

### Included Concepts

Malicious member, debate history, adaptive persuasion, RAG credibility, group size, rounds, majority vote, and agreement dynamics.

### Taxonomy Implications

Persuasion is the mechanism; the system-level failure is collective decision integrity, not a separate generic category of unsafe coordination.

### Supported Research Questions

How should evaluations separate local belief change from final system failure, and do more interaction rounds amplify or contain a malicious member?

### Important Limitations

The adversary is explicitly assigned a wrong target, outcomes are benchmark votes rather than real-world actions, and the reported effect sizes depend on model and prompting conditions.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| A malicious member adaptively promotes an incorrect target through debate. | Explicit author claim | Paper | Threat model and attack design | 4-5 | Figure 1; Algorithm 1 | Threat and protocol. |
| The attack uses argument diversification, counterarguments, fusion, and polishing. | Explicit author claim | Paper | Adversarial agent design | 5-9 | Figures 3-5 | Attack stages. |
| Four reasoning datasets are evaluated. | Explicit author claim | Paper | Experimental setup | 10-11 | - | Dataset definitions. |
| Success combines decreased group accuracy and increased adversary agreement. | Explicit author claim | Paper | Metrics | 11 | Equations 8-9 | Metric contract. |
| Prompt mitigation is inconsistent over models and rounds. | Explicit author claim | Paper | Results | 14-16 | Figures 11-13 | Defense evaluation. |

## Provenance

### Discovery Source

Scientific Reports; Crossref; prior corpus completeness scan.

### Discovery Query

`multi-agent LLM persuasion attack Scientific Reports`

### Accessed Version

Published journal version.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05

