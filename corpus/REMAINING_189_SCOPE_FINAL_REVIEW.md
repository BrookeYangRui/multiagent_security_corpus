# Final Source Pass: 189 Active Works

Row-level verdict coverage: **189/189**.
Clear keep after this pass: **176**.
Needs author discussion before any membership change: **13**.

No active Set 1/Set 2 membership is changed by this audit branch.

## Discussion queue

### From Debate to Decision: Conformal Social Choice for Safe Multi-Agent Deliberation

* Work key: `arxiv:2604.07667`
* Current: `set2_emerging` / `defense`
* Recommendation: `lean_remove_scope`
* Reason: The paper studies calibrated act-versus-escalate decisions for wrong consensus in multi-agent debate. The primary source establishes interacting LLM agents and a safety mechanism, but not a concrete adversary or security/privacy boundary beyond incorrect collective answers. Under the strict gate, this looks closer to reliability/safety than MAS security.

### Architectural Resilience in AI-Driven Decision Systems under Adversarial Conditions

* Work key: `doi:10.1109/icaic67076.2026.11395749`
* Current: `set1_core` / `defense`
* Recommendation: `lean_remove_scope`
* Reason: The conference abstract studies self-healing resilience across 20 cooperative agents under adversarial/failure conditions, but the available source does not clearly establish that the evaluated principals are LLM-backed or that a concrete MAS security property, rather than general resilience, is the paper-level object.

### Nexus Protocol: A Cryptographically Secure, Zero-Latency Semantic Routing Engine for Multi-Agent Systems

* Work key: `doi:10.2139/ssrn.7127218`
* Current: `set2_emerging` / `defense`
* Recommendation: `lean_remove_source`
* Reason: Repeated exact-title and DOI searches did not recover a verifiable primary SSRN record for the claimed Nexus Protocol paper. The title is in scope if genuine, but the source-evidence gate is not currently satisfied.

### Memetic Cascade Detection and Symbolic Immunity in Multi-Agent LLM Systems

* Work key: `doi:10.5281/zenodo.19244877`
* Current: `set2_emerging` / `defense`
* Recommendation: `lean_remove_source`
* Reason: A related author blog describing Memetic Cascade Detection is public, but repeated exact-title/DOI searches did not independently recover the claimed Zenodo record. Scope appears plausible; primary-source verification is the blocker.

### Pratyahara: A Neural Tissue Defense Model for Detecting Compromised Agents in Multi-Agent Networks

* Work key: `doi:10.5281/zenodo.19628588`
* Current: `set2_emerging` / `defense`
* Recommendation: `lean_remove_source`
* Reason: Repeated exact-title and DOI searches did not recover a verifiable primary source for Pratyahara. The claimed topic is direct MAS security, but source evidence is insufficient for active-corpus membership.

### Semantic Taint Propagation: Embedding-Based Semantic Flow Monitoring for Multi-Agent Large Language Model Systems

* Work key: `doi:10.5281/zenodo.20834834`
* Current: `set2_emerging` / `defense`
* Recommendation: `lean_remove_source`
* Reason: Repeated exact-title and DOI searches did not recover a verifiable primary source for Semantic Taint Propagation. The claimed topic is direct MAS information-flow security, but source evidence is insufficient for active-corpus membership.

### LieCraft: A Multi-Agent Framework for Evaluating Deceptive Capabilities in Language Models

* Work key: `olson2026liecraft`
* Current: `set1_core` / `evaluation`
* Recommendation: `lean_remove_scope`
* Reason: AAAI confirms a multiplayer hidden-role environment with deception, sabotage, and detection, but the paper's stated objective is measuring LLM deception propensity and skill. The MAS game may function primarily as an evaluation instrument rather than the protected system, so this sits on the scope boundary.

### The Subtle Art of Defection: Understanding Uncooperative Behaviors in LLM based Multi-Agent Systems

* Work key: `supp_the_subtle_art_of_defection_understanding_uncooperative_behaviors_in_llm_based_m`
* Current: `set1_core` / `evaluation`
* Recommendation: `lean_remove_scope`
* Reason: The EACL paper studies uncooperative behaviors causing resource-management collapse, but the primary source frames the outcome as system stability/survival rather than a concrete adversary, security property, authorization boundary, or privacy violation. It is closer to MAS robustness/reliability under the strict gate.

### Security of LLM Agents: A Case Study Approach

* Work key: `doi:10.1109/trustcom66490.2025.00226`
* Current: `set1_core` / `evaluation`
* Recommendation: `lean_remove_scope`
* Reason: The TrustCom paper itself is verifiable, but accessible metadata provides no abstract/full text establishing multiple separately addressable LLM agents. Its broad title, Security of LLM Agents: A Case Study Approach, is not enough to pass the MAS gate without paper-level evidence.

### Collaborative-adversarial jailbreaking: A propagation-aware attack framework for multi-agent code generation systems.

* Work key: `doi:10.1016/j.neunet.2026.109280`
* Current: `set1_core` / `evaluation`
* Recommendation: `lean_remove_cutoff`
* Reason: The paper is unquestionably direct MAS security and isolates a collaborative amplification effect, but the earliest verifiable public record found in this pass is after the 2026-07-01 cutoff (publisher/DBLP metadata appears in July 2026). Keep only if a pre-cutoff public version can be produced.

### LLM Drift Experiment: A Framework for Quantifying Behavioral Decay in Adversarial Multi-Agent Simulations

* Work key: `doi:10.5281/zenodo.20032071`
* Current: `set2_emerging` / `evaluation`
* Recommendation: `lean_remove_source`
* Reason: Repeated exact-title and DOI searches did not recover a verifiable primary source for LLM Drift Experiment. The current record therefore fails the source-evidence gate even if its claimed experiment would otherwise be relevant.

### A Literature Survey on Privacy-Preserving Multi-Agent RAG Systems with an Intelligent Tag-Inference Routing System

* Work key: `doi:10.56726/irjmets98584`
* Current: `set1_core` / `survey`
* Recommendation: `lean_keep_if_source_confirmed`
* Reason: The claimed survey topic is squarely privacy-preserving multi-agent RAG and author/public project pages corroborate the DOI and May 2026 publication, but an authoritative journal landing page or full survey text was not recovered in this pass. Scope is not the concern; source verification is.

### Multi-Agent Orchestration: Coordination, Trust, and Cascading Failures

* Work key: `doi:10.2139/ssrn.6734798`
* Current: `set2_emerging` / `survey`
* Recommendation: `lean_move_related_work`
* Reason: The SSRN primary source is verifiable, but its abstract explicitly synthesizes broad agentic-AI architectures, autonomy, tool invocation, memory, and multi-step trajectories. Multi-agent orchestration is a keyword/theme rather than the paper's exclusive unit of analysis, so it fits Related Work better than the strict MAS-security evidence corpus.

## Clear-keep policy used in this pass

Rows outside the discussion queue were retained only when the available paper-level evidence supports both the MAS boundary and a substantive security/privacy/adversarial relation. A paper may have a non-security dominant contribution and still remain if it contains a substantive interaction-dependent security experiment; dominant contribution is not the membership gate.
