# Whispering Agents: A Event-Driven Covert Communication Protocol for the Internet of Agents

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `attack` · venue `AAAI` · restoration `2026-08-23`.
> This banner is authoritative for current corpus membership.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

- Authors: Kaibo Huang, Yukun Wei, Wansheng Wu, Tianhua Zhang, Zhongliang Yang, Linna Zhou
- Year: 2026
- Venue: AAAI 2026
- DOI: 10.1609/aaai.v40i37.40380
- arXiv: 2508.02188
- Primary URL: https://ojs.aaai.org/index.php/AAAI/article/view/40380

## Paper Type

Attack; covert-channel protocol; empirical security evaluation

- Primary category: `attack`
- Scope relation: `core_security`

## Scope

### System Studied

Internet-of-Agents settings where LLM-backed agents communicate through event-driven A2A interactions while a warden observes their overt behavior.

### Multi-Agent Dependency

The covert channel exists across interacting agents and encodes a hidden dialogue through storage, timing, and behavioral event patterns. The protected and violated property is therefore relational: whether communication between agents can be observed and controlled.

## Security Model

- Protected property: communication privacy, traffic-analysis resistance, and monitoring integrity.
- Threat capability: agents coordinate a covert event channel within otherwise benign-looking interactions.
- Defender: an LLM-based warden monitoring the observable agent interaction.

## Main Contribution

The paper formalizes the Covert Event Channel and engineers Pi-CCAP, an event-driven covert communication protocol spanning storage, timing, and behavioral channels.

## Attack or Failure

The protocol hides the existence and content of inter-agent communication inside normal-looking agent events, creating a covert channel that can evade traffic analysis and LLM-based monitoring.

## Evaluation

The official AAAI paper reports that Pi-CCAP provides high capacity and robustness while remaining imperceptible to strong LLM-based wardens in the evaluated settings.

## Relevance to Our SoK

This is direct MAS-security evidence for covert communication and monitoring-evasion attacks at the communication and observation interfaces. It is not merely a multi-agent application used to solve a separate security task.

## Source Review

Primary sources checked for restoration: AAAI 2026 proceedings article and extended arXiv version 2508.02188. The paper is peer reviewed and predates the 2026-07-01 literature cutoff through its published AAAI version.
