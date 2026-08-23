# Defense Dominant-Contribution Re-Audit

Date: `2026-08-23`

## Rule

The previous `defense` bucket was re-screened under a stricter dominant-contribution rule. A work is defense-primary only when its main contribution is a mechanism, protocol, or system intended to prevent, detect, contain, or recover from a concrete MAS security threat or system-level security failure. A paper is not defense-primary merely because it contains privacy-preserving, robust, safe, trustworthy, or governance-oriented features.

This pass reviews the full **94-work previous defense bucket** as a contribution-classification audit. It does **not** upgrade the source-verification state of papers whose notes remain metadata-only.

## Result

* Previous defense-primary count: **94**
* Retained as defense-primary: **85**
* Reclassified: **9**
* Final 201-work contribution counts: **44 attack, 85 defense, 46 evaluation, 16 general, 10 survey**

## Reclassified works

| Work | New category | Reason |
| --- | --- | --- |
| Cross-Domain Query Translation for Network Troubleshooting: A Multi-Agent LLM Framework with Privacy Preservation and Self-Reflection | `general` | The paper's primary contribution is a cross-domain network-troubleshooting architecture; privacy-preserving anonymization is one of several system features rather than the main security-defense contribution. |
| Dynamic Attentional Context Scoping: Agent-Triggered Focus Sessions for Isolated Per-Agent Steering in Multi-Agent LLM Orchestration | `general` | DACS primarily addresses context pollution and steering accuracy in multi-agent orchestration. Its core problem is reliability and context isolation rather than an adversarial security defense. |
| No Action Without a NOD: A Heterogeneous Multi-Agent Architecture for Reliable Service Agents | `general` | NOD is primarily a reliable service-agent architecture for policy compliance, tool hallucination, and long-horizon execution; it does not center an adversarial threat model. |
| MedAgentNet: Federated Multi-Agent AI for Privacy-Preserving Cross-Departmental Clinical Intelligence | `general` | MedAgentNet is primarily a federated clinical-intelligence architecture. Privacy-preserving disclosure is an architectural requirement, not a threat-driven defense contribution. |
| Robotic Environment Manipulation Agents (REMA): A Proactive Multi-Agent Framework for Robust | `general` | REMA is primarily a proactive robotic-manipulation architecture for reliable execution and semantic validation, not a security defense against a concrete adversary. |
| The Trust Paradox in LLM-Based Multi-Agent Systems: When Collaboration Becomes a Security Vulnerability | `evaluation` | The main contribution is formalization and empirical measurement of the Trust-Vulnerability Paradox with OER and Authorization Drift; mitigation mechanisms are secondary evaluations. |
| MESA: Prioritizing Vulnerable Communication Channels for Securing Multi-Agent Systems | `evaluation` | MESA's primary artifact is a label-free framework for ranking and measuring security-critical communication edges. It prioritizes where defenses should be deployed rather than providing the defense itself. |
| Autonomous LLM Agent Worms: Cross-Platform Propagation, Automated Discovery and Temporal Re-Entry Defense | `attack` | The paper's central contribution is the first systematic automated analysis and demonstration of persistent cross-platform LLM-agent worm propagation; RTW-A is a substantial but subsequent defense contribution. |
| The Sum Leaks More Than Its Parts: Compositional Privacy Risks and Mitigations in Multi-Agent Collaboration | `attack` | The paper introduces and systematically studies compositional privacy leakage as a new multi-agent vulnerability class; ToM and CoDef are mitigation follow-ons to the risk contribution. |


## Important source-status notes

`Governance Effectiveness in Distributed Multi-Agent LLM Systems: Confound Isolation, Diversity Erosion, and the Accidental Governance Effect` remains provisionally defense-primary because the primary source could not be recovered during this pass. Its current metadata-only note is not enough to justify a category change in either direction.

Two reclassified application/reliability papers also expose a separate cutoff question. The currently discoverable SSRN records for `MedAgentNet` and `REMA` report posting dates after the repository's 2026-07-01 literature cutoff. This audit intentionally leaves the 201-work membership frozen and records the anomaly for a separate identity and first-public-date review rather than silently changing the denominator here.
