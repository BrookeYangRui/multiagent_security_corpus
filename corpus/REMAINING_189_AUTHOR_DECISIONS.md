# Author Decisions for the 189-Work Scope Audit

This file records explicit author adjudications that override provisional recommendations in `REMAINING_189_SCOPE_FINAL_REVIEW.md`. These decisions do not change the active denominator because all listed works are already in the 189-work corpus.

## Confirmed KEEP

### From Debate to Decision: Conformal Social Choice for Safe Multi-Agent Deliberation

* Work key: `arxiv:2604.07667`
* Decision: **KEEP**
* Rationale: wrong consensus is converted into a system-level act-versus-escalate decision. The relevant property is collective decision integrity and safe action gating at the aggregation boundary, not generic single-model accuracy. The effect is intrinsically tied to multi-agent deliberation and aggregation.

### LieCraft: A Multi-Agent Framework for Evaluating Deceptive Capabilities in Language Models

* Work key: `olson2026liecraft`
* Decision: **KEEP**
* Rationale: deception, defection, sabotage, accusation, and detection are structurally relational behaviors between separately acting agents. The multi-agent game is not merely incidental; it defines the adversarial interaction and the measured security-relevant capability.

### The Subtle Art of Defection: Understanding Uncooperative Behaviors in LLM based Multi-Agent Systems

* Work key: `supp_the_subtle_art_of_defection_understanding_uncooperative_behaviors_in_llm_based_m`
* Decision: **KEEP**
* Rationale: uncooperative participants cause system-level resource exhaustion and collapse. Availability, resource abuse, and resilience against strategically uncooperative agents are security-relevant properties of the interacting system, not merely local accuracy or reliability.

### Multi-Agent Orchestration: Coordination, Trust, and Cascading Failures

* Work key: `doi:10.2139/ssrn.6734798`
* Decision: **KEEP**
* Rationale: although the survey discusses broader agentic-AI architecture, coordination, trust, and cascading failures are substantive analysis targets rather than incidental mentions. It remains useful evidence for the MAS-security synthesis and corpus-level survey coverage.

## Source corrections supplied during adjudication

The following earlier source-gap flags are no longer valid and should not be used as removal reasons:

* `doi:10.1109/icaic67076.2026.11395749` — **Architectural Resilience in AI-Driven Decision Systems under Adversarial Conditions**. IEEE full text is available at `https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11395749`.
* `doi:10.2139/ssrn.7127218` — **Nexus Protocol: A Cryptographically Secure, Zero-Latency Semantic Routing Engine for Multi-Agent Systems**. A primary SSRN PDF was supplied directly during adjudication, so the previous claim that the paper record could not be recovered is superseded.
* `doi:10.5281/zenodo.19244877` — **Memetic Cascade Detection and Symbolic Immunity in Multi-Agent LLM Systems**. Zenodo confirms the all-versions DOI `10.5281/zenodo.19244877`; version 2 is `10.5281/zenodo.19245513`, published 26 March 2026, with `paper_04.pdf` available. The preprint explicitly presents detection, quarantine, provenance auditing, and integrity verification for symbolic payload propagation across multi-agent LLM systems.

## Audit status after these decisions

The four works above are removed from the discussion queue and remain active corpus members. Architectural Resilience, Nexus Protocol, and Memetic Cascade now require scope/content adjudication only where still relevant; source non-existence is no longer a valid objection.
