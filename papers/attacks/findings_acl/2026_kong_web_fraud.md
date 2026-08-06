# Web Fraud Attacks Against LLM-Driven Multi-Agent Systems

## Citation

Title: Web Fraud Attacks Against LLM-Driven Multi-Agent Systems

Authors: Dezhang Kong; Hujin Peng; Yilun Zhang; Lele Zhao; Zhenhua Xu; Shi Lin; Changting Lin; Meng Han

Year: 2026

Venue: Findings of ACL

DOI: 10.18653/v1/2026.findings-acl.686

Primary URL: https://aclanthology.org/2026.findings-acl.686/

Open access URL: https://aclanthology.org/2026.findings-acl.686.pdf

BibTeX key: kong2026webfraud

## Paper Type

- Attack
- Evaluation
- Empirical study

## Scope

### System Studied

MetaGPT-based LLM multi-agent systems that recommend and review web links through linear, review, debate, and voting workflows.

### Multi-Agent Dependency

A malicious member supplies a structurally disguised URL and relies on downstream reviewers, debaters, voters, or an auditor to accept and propagate that recommendation. Attack success therefore depends on the communication and aggregation workflow rather than URL classification by one isolated model alone.

### Application Domain

Web recommendation and agent-mediated browsing.

## Security Model

### Protected Assets

Integrity of collective link recommendations and user or tool navigation.

### Threat Actor

One low-privilege malicious member agent.

### Trusted Components

Other member agents, fixed communication channels, and the final auditor are not compromised.

### Attacker Capabilities

The attacker sends a malicious URL through its assigned channel and can insist on it during review, but does not know the architecture, other agents' capabilities, or deployed defenses.

### Security Assumptions

The attacker controls a registered malicious domain and can choose URL subdomains, paths, parameters, or representations; the workflow permits the member's recommendation to influence a final decision.

## Main Contribution

The paper defines 12 Web Fraud Attack variants that disguise malicious destinations using URL structure rather than complex prompt optimization. It evaluates them across four architectures, four model families, and traditional and LLM-based defenses.

## Attack or Failure

### Attack Surface

Agent-produced web links carried through inter-agent recommendations and collective review.

### Attack Mechanism

Variants use IP or domain registration, typos, homoglyphs, subdomains, paths, and parameters to place benign-looking tokens around an attacker-controlled destination.

### System-Level Failure

The MAS accepts a malicious destination as low risk and recommends or visits it.

### Security Consequence

Collective decision-integrity failure that can expose users or tool-using agents to phishing, malware, or subsequent prompt injection.

## Defense

### Defense Mechanism

The evaluation tests Google Safe Browsing, VirusTotal, PhishTank, and three prompt-based defenses; the paper discusses DNS traceability, fine-tuning, and whitelists as future directions.

### Intervention Point

URL reputation service, agent prompt, or final auditor.

### Required Observability

Defenses see the candidate URL and, for LLM defenses, the recommendation context.

### Assumptions

Reputation defenses require prior observations of malicious domains; prompt defenses assume the model can parse URL ownership correctly.

### Limitations

No new preventive defense is implemented, and newly registered domains intentionally evade history-based services.

## Evaluation

### Evaluated Systems

MetaGPT with Gemini-2.5-Flash, GPT-4o-mini, DeepSeek-Reasoner, and Llama-3-8B.

### Agent Configuration

Linear, iterative review, three-round debate, and voting architectures with one malicious recommender.

### Dataset or Environment

Synthetic travel-site recommendation tasks plus three additional application scenarios in the appendix.

### Baselines

A plain malicious URL and six traditional or LLM-based defenses.

### Metrics

Attack success rate based on the final auditor's risk label; ten repetitions per attack configuration; coefficient of variation in selected analyses.

### Main Results

The paper reports 57.6% average ASR across the main WFA variants, with substantial variation by URL construction, model, defense, and architecture.

## Relation to Existing Work

### Papers Compared by the Authors

MAS communication attacks, contagious attacks, Agent Security Tax, PeerGuard, and phishing or malicious-URL detection work.

### Claimed Research Gap

Prior MAS security work had not isolated malicious URL structure as an interaction-carried attack surface.

### Closest Related Work

Agent-mediated web fraud and communication attacks on LLM-MAS.

### Difference From Prior Work

The attack requires only one member's URL recommendation and manipulates URL syntax rather than compromising privileged agents or optimizing adversarial prompts.

## Relevance to Our SoK

### Included Concepts

Malicious member, fixed-channel access, URL provenance, collective recommendation, architecture-dependent amplification, and web-tool boundary.

### Taxonomy Implications

The mechanism is a communication-carried representation attack; the failure is collective recommendation integrity, with downstream execution risk at the web boundary.

### Supported Research Questions

How do review and voting structures transform a low-privilege member's malicious resource recommendation, and what context must URL defenses observe?

### Important Limitations

The task is narrow, ASR is defined by an LLM auditor rather than verified website execution, and the authors assume one attacker-controlled domain and one malicious agent.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| One malicious member with no architecture or defense knowledge supplies the URL. | Explicit author claim | Paper | 3.1 | 14021 | Figure 1 | Threat identity, workflow, and capabilities. |
| The attack family contains 12 URL-structure variants. | Explicit author claim | Paper | 3.2 | 14022-14023 | Table 2 | Formal definitions and examples. |
| Four MAS workflows and six defenses are evaluated. | Explicit author claim | Paper | 4.1 | 14023-14024 | Figure 3 | Experimental setup. |
| ASR is the fraction of runs the auditor does not label high risk, with ten repetitions. | Explicit author claim | Paper | 4.1 | 14024 | - | Metric definition. |
| The reported overall average ASR is 57.6%. | Explicit author claim | Paper | 4.2 | 14024-14025 | Figure 4; Table 3 | Main attack results. |

## Provenance

### Discovery Source

ACL Anthology; prior corpus completeness scan.

### Discovery Query

`site:aclanthology.org multi-agent security attack URL`

### Accessed Version

Published Findings of ACL version.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05

