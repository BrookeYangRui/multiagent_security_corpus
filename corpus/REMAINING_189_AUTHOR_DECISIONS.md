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

## Source corrections without final scope decision

### Nexus Protocol: A Cryptographically Secure, Zero-Latency Semantic Routing Engine for Multi-Agent Systems

* Work key: `doi:10.2139/ssrn.7127218`
* Source status: **PRIMARY SOURCE EXISTS**. A primary SSRN PDF was supplied directly during adjudication, so the previous source-nonexistence objection is superseded.
* Remaining question: confirm from the full PDF that the separately addressable principals are LLM-backed agents and that the cryptographic routing guarantee protects an inter-agent security property rather than a generic distributed-routing system.

### Security of LLM Agents: A Case Study Approach

* Work key: `doi:10.1109/trustcom66490.2025.00226`
* Source status: **PUBLICATION EXISTS; FULL-TEXT MAS BOUNDARY STILL TO VERIFY**. The TrustCom 2025 publication and authorship are verified, and an IEEE stamp link was supplied. The remaining question is whether the case study contains multiple separately addressable LLM-backed agents with a material inter-agent security relation.

### Collaborative-adversarial jailbreaking: A propagation-aware attack framework for multi-agent code generation systems

* Work key: `doi:10.1016/j.neunet.2026.109280`
* Scope status: **DIRECT MAS SECURITY**.
* Remaining question: cutoff only. Retain if a public version dated on or before 1 July 2026 can be established; otherwise exclude solely for cutoff compliance.

### LLM Drift Experiment: A Framework for Quantifying Behavioral Decay in Adversarial Multi-Agent Simulations

* Work key: `doi:10.5281/zenodo.20032071`
* Source status: **SOURCE CONFIRMED**, software release public 21 May 2026.
* Remaining question: scope. The framework measures behavioral/personality/affective/cognitive/social drift under adversarial multi-agent pressure. The current description does not yet state a concrete protected security/privacy property beyond behavioral decay, so under the manuscript's rule that behavioral drift alone is insufficient this remains a genuine boundary case rather than a source-gap case.

## Current audit status

Nine formerly disputed works are now author/source-confirmed KEEP: From Debate to Decision, LieCraft, The Subtle Art of Defection, Multi-Agent Orchestration, Architectural Resilience, Memetic Cascade Detection, Pratyahara, Semantic Taint Propagation, and the Privacy-Preserving Multi-Agent RAG survey.

Only four discussion items remain from the original 13-work queue: Nexus Protocol, Security of LLM Agents, Collaborative-adversarial jailbreaking (cutoff only), and LLM Drift Experiment.
