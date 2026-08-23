# Strict MAS Security Scope Audit

Date: `2026-08-23`

This pass re-checks all 201 manuscript-corpus works against a stricter paper-level boundary. A retained work must substantively study security or privacy of interacting LLM-backed agents, or a security mechanism/evaluation whose claim materially depends on an inter-agent relation such as communication, shared state, delegation, aggregation, topology, or identity. Merely using multiple agents as a generic safety, reliability, alignment, or security tool is not sufficient.

## Proposed result

- Re-screened: **201** works
- Keep as strict MAS-security evidence: **184**
- Move to contextual literature: **13**
- Remove as first-public after the `2026-07-01` cutoff: **3**
- Hold out pending recoverable primary-source evidence: **1**

This audit does not yet mutate `main` Set 1/Set 2 membership. The denominator change is intentionally isolated for review before applying it.

## Move to context

| Work | Why it is not strict MAS-security evidence |
| --- | --- |
| DAWN: Distributed LLM Multi-Agent Workflow Synthesis | Distributed workflow synthesis under privacy constraints; privacy is a deployment constraint rather than a MAS security property or adversarial evaluation. |
| CoMet: Metaphor-Driven Covert Communication for Multi-Agent Language Games | Studies metaphor-enabled covert/strategic communication capability, but does not formulate or evaluate a MAS security property, attack, or defense. |
| Supervisor Alignment Framework: Enhancing LLM Alignment with Query-Ignoring Strategy and Multi-Agent Interaction | Uses multiple agents to improve generic model alignment; the protected object is the target LLM rather than a security failure created by MAS interaction. |
| A Multi-Agent LLM Defense Pipeline Against Prompt Injection Attacks | Uses a chain/coordinator of agents as a detector for prompt injection against ordinary LLM deployments; MAS is the security tool, not the security object. |
| MAJD: Intent-Aware Multi-Agent Framework for Jailbreak Defense | Multi-agent architecture for generic jailbreak defense rather than interaction-native MAS security. |
| Hierarchical Pedagogical Oversight: A Multi-Agent Adversarial Framework for Reliable AI Tutoring | Pedagogical reliability/sycophancy mitigation, not MAS security. |
| RedDebate: Safer Responses through Multi-Agent Red Teaming Debates | Uses multi-agent debate to improve generic output safety on HarmBench; does not study security created by the MAS relation. |
| Dynamic Attentional Context Scoping: Agent-Triggered Focus Sessions for Isolated Per-Agent Steering in Multi-Agent LLM Orchestration | Context isolation and orchestration reliability without a concrete adversarial MAS security model. |
| No Action Without a NOD: A Heterogeneous Multi-Agent Architecture for Reliable Service Agents | Reliability architecture targeting policy errors, hallucinated tools, and misalignment rather than adversarial MAS security. |
| EncGPT: A Multi-Agent Workflow for Dynamic Encryption Algorithms | Uses MAS to construct/apply encryption; security is the application task rather than the security of the multi-agent system. |
| A Systematic Survey of Security Threats and Defenses in LLM-Based AI Agents: A Layered Attack Surface Framework | Broad agentic-security survey; multi-agent coordination is one layer of a seven-layer taxonomy, not the paper-level scope. |
| Cross-Domain Query Translation for Network Troubleshooting: A Multi-Agent LLM Framework with Privacy Preservation and Self-Reflection | Telecommunications architecture with privacy-preserving anonymization as one feature; no MAS threat model or interaction-induced security failure. |
| A Survey on the Unique Security of Autonomous and Collaborative LLM Agents: Threats, Defenses, and Futures | Broad LLM-agent security survey spanning external, cognitive, and multi-agent paradigms; MAS security is one branch rather than the paper-level boundary. |

## Remove for cutoff

| Work | Evidence |
| --- | --- |
| Robotic Environment Manipulation Agents (REMA): A Proactive Multi-Agent Framework for Robust | SSRN first posted `2026-07-06`. |
| MedAgentNet: Federated Multi-Agent AI for Privacy-Preserving Cross-Departmental Clinical Intelligence | SSRN first posted `2026-07-31`. |
| Vulnerabilities in Autonomous Execution: A Survey of Security Threats and Defenses in LLM-driven Multi-Agent Systems | SSRN first posted `2026-08-01`. |

## Hold out pending source

`Governance Effectiveness in Distributed Multi-Agent LLM Systems: Confound Isolation, Diversity Erosion, and the Accidental Governance Effect` currently has only a metadata-level repository note and the primary source could not be reliably recovered in this pass. Under the repository's own source-evidence rule, it should not be certified as strict in-scope until the primary source is recovered.

## Borderline works retained deliberately

Several papers are not security-primary but remain in scope because they contain a substantive interaction-specific security experiment or mechanism. Examples include G-Designer, Cut the Crap/AgentPrune, MPAS, SafeSieve, Free-MAD, AgentMonitor, and 1-2-3 Check. Their security evidence directly changes with communication topology, malicious-agent messages, information-flow structure, or another MAS relation; therefore they are not treated like generic MAS-as-a-tool papers above.

The full 201-row audit is in `MAS_SCOPE_FINAL_AUDIT_2026-08-23.csv`.