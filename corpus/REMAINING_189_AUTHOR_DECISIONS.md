# Author Decisions for the 189-Work Scope Audit

This file records explicit author adjudications and source-level corrections that override provisional recommendations in `REMAINING_189_SCOPE_FINAL_REVIEW.md`. These decisions do not change the active denominator because all listed works are already in the 189-work corpus.

## Confirmed KEEP

### From Debate to Decision: Conformal Social Choice for Safe Multi-Agent Deliberation

* Work key: `arxiv:2604.07667`
* Decision: **KEEP**
* Rationale: wrong consensus is converted into a system-level act-versus-escalate decision. The relevant property is collective decision integrity and safe action gating at the aggregation boundary, not generic single-model accuracy. The effect is intrinsically tied to multi-agent deliberation and aggregation.

### LieCraft: A Multi-Agent Framework for Evaluating Deceptive Capabilities in Language Models

* Work key: `olson2026liecraft`
* Decision: **KEEP**
* Rationale: deception, defection, sabotage, accusation, and detection are structurally relational behaviors between separately acting agents. The multi-agent game defines the adversarial interaction and the measured security-relevant capability rather than serving as an incidental wrapper.

### The Subtle Art of Defection: Understanding Uncooperative Behaviors in LLM based Multi-Agent Systems

* Work key: `supp_the_subtle_art_of_defection_understanding_uncooperative_behaviors_in_llm_based_m`
* Decision: **KEEP**
* Rationale: the primary paper studies strategic deception, greed, threats, punishment, and other uncooperative behaviors among LLM agents, measures system collapse and resource overuse, and evaluates detection defenses. Availability, resource abuse, and resilience against strategically uncooperative participants are system-level security-relevant properties.

### Multi-Agent Orchestration: Coordination, Trust, and Cascading Failures

* Work key: `doi:10.2139/ssrn.6734798`
* Decision: **KEEP**
* Rationale: although the survey discusses broader agentic-AI architecture, coordination, trust, and cascading failures are substantive analysis targets rather than incidental mentions. It remains useful evidence for the MAS-security synthesis and corpus-level survey coverage.

### Architectural Resilience in AI-Driven Decision Systems under Adversarial Conditions

* Work key: `doi:10.1109/icaic67076.2026.11395749`
* Decision: **KEEP**
* Rationale: the paper evaluates a self-healing architecture across 20 cooperative agents under adversarial/failure conditions and measures cross-agent failure propagation, recovery latency, and collective stability. Quarantine Isolation, Cognitive Rollback, Semantic Checkpointing, and Adaptive Consensus Reset intervene on interaction-dependent propagation and recovery. The source explicitly situates the current system in LLM-based agent settings while describing future extensions beyond LLM agents.
* Source: `https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11395749`.

### Memetic Cascade Detection and Symbolic Immunity in Multi-Agent LLM Systems

* Work key: `doi:10.5281/zenodo.19244877`
* Decision: **KEEP**
* Rationale: this is direct MAS-security defense work on symbolic payload propagation, trust exploitation, quarantine, recursive provenance auditing, and integrity verification across multi-agent LLM systems.
* Source correction: `10.5281/zenodo.19244877` is the all-versions DOI. Version 2 is `10.5281/zenodo.19245513`, published 26 March 2026, with `paper_04.pdf` available.

### Pratyahara: A Neural Tissue Defense Model for Detecting Compromised Agents in Multi-Agent Networks

* Work key: `doi:10.5281/zenodo.19628588`
* Decision: **KEEP**
* Rationale: NERVE explicitly extends A2A and MCP to detect and respond to compromised or behaviorally drifting agents inside the network boundary. Its threat set includes session smuggling, tool poisoning, emergent collusion, and inter-agent manipulation. The protected properties are agent integrity, trust dynamics, and containment inside an interacting agent network, not generic single-model reliability.
* Source correction: `10.5281/zenodo.19628588` is the all-versions DOI. Version 1 was public 17 April 2026 and version 2 (`10.5281/zenodo.20652907`) was published 12 June 2026, both before the literature cutoff.

### Semantic Taint Propagation: Embedding-Based Semantic Flow Monitoring for Multi-Agent Large Language Model Systems

* Work key: `doi:10.5281/zenodo.20834834`
* Decision: **KEEP**
* Rationale: the primary source defines a structural vulnerability in multi-agent LLM deployments in which adversarial content from retrieved documents or inter-agent messages can cause data-access agents to disclose sensitive records. STP monitors semantic information flow against sensitive and authorized concept regions and is evaluated on adversarial prompt, indirect injection, and scope-control scenarios. This supports confidentiality and cross-agent information-flow security, even though the detector primitive may also be reusable in single-agent systems.
* Source correction: `10.5281/zenodo.20834834` is the all-versions DOI; version 1 is `10.5281/zenodo.20834835`, published 24 June 2026.

### A Literature Survey on Privacy-Preserving Multi-Agent RAG Systems with an Intelligent Tag-Inference Routing System

* Work key: `doi:10.56726/irjmets98584`
* Decision: **KEEP**
* Rationale: the full paper explicitly studies a five-agent LLM architecture and makes privacy-aware routing a first-class multi-agent design concern. Sensitive-query classification controls local-versus-cloud LLM selection and is described as mandatory access control at query level. Privacy therefore governs the multi-agent execution path rather than appearing as an incidental feature.
* Source: `https://www.irjmets.com/upload_newfiles/irjmets80500183032/paper_file/irjmets80500183032.pdf`, May 2026.

### Nexus Protocol: A Cryptographically Secure, Zero-Latency Semantic Routing Engine for Multi-Agent Systems

* Work key: `doi:10.2139/ssrn.7127218`
* Decision: **KEEP**
* Rationale: the full paper explicitly models an LLM-enabled multi-agent swarm as a directed graph of autonomous agents and inter-agent communication channels. It uses an LLM compiler for agent intents and defines a Dolev-Yao adversary that can intercept, synthesize, and replay messages. HMAC-SHA256, TTL replay protection, payload-digest verification, and risk-calibrated semantic-cache thresholds protect inter-agent message integrity and state-changing actions. This is direct interaction-native MAS security rather than generic routing efficiency.

### Security of LLM Agents: A Case Study Approach

* Work key: `doi:10.1109/trustcom66490.2025.00226`
* Decision: **KEEP**
* Rationale: the full TrustCom paper implements six attacks on two real-world MASs. GPMS uses AutoGen Swarm agents with shared context and handoffs and is attacked through function-enumeration propagation and privilege escalation across the agent graph. The AI Hedge Fund uses communicating graph nodes and shared state and is tested against compromised-agent, intercepted-agent/MITM, compromised-tool, and resource-exhaustion attacks. The paper directly studies inter-agent security surfaces and defenses.

### LLM Drift Experiment: A Framework for Quantifying Behavioral Decay in Adversarial Multi-Agent Simulations

* Work key: `doi:10.5281/zenodo.20032071`
* Decision: **KEEP**
* Rationale: author adjudication retains this framework as MAS-security evaluation evidence. It subjects LLM agents to prolonged adversarial multi-agent interaction and quantifies interaction-driven behavioral decay across longitudinal trajectories. Its role in the corpus is evaluation evidence about adversarial social influence and trajectory drift, not a claim that behavioral drift alone defines every security violation.
* Source status: Zenodo software release public 21 May 2026, before the literature cutoff.

## Remaining unresolved item

### Collaborative-adversarial jailbreaking: A propagation-aware attack framework for multi-agent code generation systems

* Work key: `doi:10.1016/j.neunet.2026.109280`
* Scope status: **DIRECT MAS SECURITY**.
* Remaining question: cutoff only. Retain if a public version dated on or before 1 July 2026 can be established; otherwise exclude solely for cutoff compliance.

## Current audit status

Twelve formerly disputed works are now confirmed KEEP. Only one item remains unresolved from the original 13-work discussion queue: `Collaborative-adversarial jailbreaking: A propagation-aware attack framework for multi-agent code generation systems`, and the only unresolved issue is whether a public version existed on or before the 1 July 2026 literature cutoff.
