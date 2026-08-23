# Tool Use Enables Undetectable Steganography in Multi-Agent LLM Systems

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set2_emerging` · `attack` · venue `arXiv` · restoration `2026-08-23`.
> This banner is authoritative for current corpus membership.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

- Authors: Jimmy Laurence Rippin, Simon C. Marshall, David Demitri Africa, Christian Schroeder de Witt
- Year: 2026
- Venue: arXiv
- DOI: 10.48550/arXiv.2606.28425
- arXiv: 2606.28425
- Primary URL: https://arxiv.org/abs/2606.28425

## Paper Type

Attack capability study; covert communication; security evaluation

- Primary category: `attack`
- Scope relation: `core_security`

## Scope

### System Studied

A multi-agent system with at least a sender and receiver connected by a monitored natural-language channel, plus realistic agentic tool access such as code execution, files, model sampling, and web search.

### Multi-Agent Dependency

The security failure is covert information transfer from one principal to another despite complete observation of the overt message channel. The paper separately studies whether agents can tacitly converge on compatible steganographic schemes without explicit agreement.

## Security Model

- Protected property: information-flow confidentiality and effectiveness of content-level monitoring.
- Threat actor: an agent attempting to transmit restricted information covertly to a cooperating receiver.
- Defender: a monitor that sees agent outputs but lacks the secret key and may lack visibility into tools and intermediate artifacts.

## Main Contribution

The paper introduces an agentic covert-channel construction benchmark, shows that tool-using agents can operationalize sophisticated stegosystems, and frames tacit steganographic agreement as a Schelling-point coordination problem.

## Attack or Failure

Agents use tools to construct hidden natural-language channels that can carry prohibited information through apparently benign text, defeating the assumption that readable inter-agent messages are sufficient for information-flow enforcement.

## Evaluation

The paper evaluates implementation success under progressively restricted tool environments and measures algorithmic, hyperparameter, and complete coordination between independently acting agents.

## Relevance to Our SoK

This is direct interaction-dependent MAS-security evidence for covert communication, collusion, information-flow violations, and monitor evasion. The sender-receiver relation and monitored channel are part of the threat model rather than incidental experimental machinery.

## Source Review

Primary source checked for restoration: arXiv 2606.28425, first posted 2026-06-25, before the 2026-07-01 literature cutoff. It remains Set 2 because it is a non-peer-reviewed preprint under the frozen maturity rule.
