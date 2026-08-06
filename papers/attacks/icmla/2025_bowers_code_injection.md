# Analyzing Code Injection Attacks on LLM-based Multi-Agent Systems in Software Development

## Citation

Title: Analyzing Code Injection Attacks on LLM-based Multi-Agent Systems in Software Development

Authors: Brian Bowers; Smita Khapre; Jugal Kalita

Year: 2025

Venue: ICMLA

DOI: 10.1109/ICMLA66185.2025.00174

Primary URL: https://doi.org/10.1109/ICMLA66185.2025.00174

Open access URL: https://arxiv.org/abs/2512.21818

BibTeX key: bowers2025codeinjection

## Paper Type

- Attack
- Defense
- Evaluation
- Empirical study

## Scope

### System Studied

AutoGen software-development workflows containing coder, tester, reviewer, and optional security-analysis agents.

### Multi-Agent Dependency

Injected code is written to shared storage and then consumed, tested, reviewed, or approved by other specialized agents. Architecture changes which agents can stop the injected function before final output.

### Application Domain

LLM-assisted software development.

## Security Model

### Protected Assets

Integrity and confidentiality of generated software and data processed by it.

### Threat Actor

An insider or party able to modify generated code after an agent writes it.

### Trusted Components

Other agents are initially honest; the optional security-analysis agent is intended to be trusted but is itself attacked in advanced variants.

### Attacker Capabilities

The attacker has one-time or continuous access to shared generated code and inserts a proof-of-concept exfiltration function plus optional obfuscation or misleading comments.

### Security Assumptions

Agents exchange code through a writable shared database, and malicious code is considered successful if retained in final output for production execution.

## Main Contribution

The paper compares code-injection resilience across coder, coder-tester, and coder-reviewer-tester architectures, then adds a security-analysis agent. It demonstrates that poisoned few-shot examples in code comments can undermine that security reviewer.

## Attack or Failure

### Attack Surface

Shared generated code between specialized development agents.

### Attack Mechanism

An exfiltration function is injected once or repeatedly; advanced variants obfuscate it or add natural-language comments that mislabel malicious code and provide poisoned examples.

### System-Level Failure

Review and testing stages approve code containing the exfiltration behavior.

### Security Consequence

Software supply-chain integrity failure and potential data exfiltration.

## Defense

### Defense Mechanism

A reviewer checks correctness, and a dedicated final security-analysis agent checks the completed code for security concerns.

### Intervention Point

Shared-code review before output.

### Required Observability

The reviewer sees the generated function; the security agent sees the final code but not necessarily the write history or provenance.

### Assumptions

Static inspection of the final function is sufficient to recognize the injected behavior.

### Limitations

Natural-language comments can manipulate the reviewer, and the defense lacks provenance or execution-based verification.

## Evaluation

### Evaluated Systems

AutoGen architectures using Code Llama 7B, Mistral 7B, and GPT-4.1-mini.

### Agent Configuration

Coder, coder-tester, coder-reviewer-tester, and coder-tester plus security-analysis agent.

### Dataset or Environment

HumanEval's 164 Python function tasks.

### Baselines

No attack, one-time and continuous basic injection, and six advanced attack variants.

### Metrics

Pass@1, attack effectiveness, model calls, and detection true-positive or true-negative behavior.

### Main Results

The dedicated security agent blocks the basic attack for Mistral and GPT-4.1-mini in the tested setting, while poisoned few-shot comments raise attack effectiveness to 86.59% and 71.95%, respectively.

## Relation to Existing Work

### Papers Compared by the Authors

LLM code generation, AutoGen development agents, communication attacks, and agent threat-model frameworks.

### Claimed Research Gap

Few studies had empirically compared code injection and security review across realistic specialized MAS development architectures.

### Closest Related Work

Red-Teaming LLM Multi-Agent Systems via Communication Attacks and multi-agent code-generation systems.

### Difference From Prior Work

The attack modifies shared code between development stages and then targets a security-review agent through comments embedded in that artifact.

## Relevance to Our SoK

### Included Concepts

Insider write access, shared artifact, one-time versus persistent corruption, role composition, review boundary, provenance loss, and comment-based reviewer manipulation.

### Taxonomy Implications

The exposed surface is a shared code artifact; the mechanism is injection and reviewer deception; the final property violation is compositional action and software integrity.

### Supported Research Questions

Does adding reviewer agents improve security when they consume attacker-controlled artifacts without trusted provenance?

### Important Limitations

Only HumanEval functions, three trials, three model backbones, and one proof-of-concept exfiltration function are tested; the authors note that repository-scale code may be harder to review.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| One-time or continuous access injects an exfiltration function into shared code. | Explicit author claim | Paper | 4-5 | 3-4 | Figure 1; Listing 1 | Threat and attack model. |
| Four development architectures and three LLM backbones are evaluated. | Explicit author claim | Paper | 5 | 4 | Figure 1 | System setup. |
| HumanEval and Pass@1 are used for functional evaluation. | Explicit author claim | Paper | 5.3-6 | 4 | - | Dataset and metrics. |
| Poisoned examples in comments bypass the security-analysis agent. | Explicit author claim | Paper | 7 | 5-6 | Table III | Advanced attack results. |
| Evaluation is limited to one dataset and three trials. | Explicit author claim | Paper | 8 | 6 | - | Limitations. |

## Provenance

### Discovery Source

IEEE DOI metadata; arXiv; prior corpus completeness scan.

### Discovery Query

`multi-agent code injection ICMLA 2025`

### Accessed Version

Published ICMLA metadata; full text accessed as arXiv v1.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05

