# Graph Representation-Based Model Poisoning on the Heterogeneous Internet of Agents

## Citation

- Authors: Hanlin Cai, Haofan Dong, Houtianfu Wang, Kai Li, Sai Zou, Ozgur B. Akan
- Year: 2026
- Venue: IWCMC
- DOI: 10.1109/IWCMC69287.2026.11579822
- Primary URL: https://doi.org/10.1109/IWCMC69287.2026.11579822
- Open access URL: https://arxiv.org/abs/2511.07176
- BibTeX key: `cai2026grmp`

## Paper Type

Attack; Evaluation; Empirical study

## Scope

### System Studied

A heterogeneous Internet of Agents in which distributed LLM agents participate
in federated fine-tuning of a shared global model.

### Multi-Agent Dependency

The adversary observes benign participant updates and submits a malicious local
update to a shared aggregation process. The attack and its system-wide accuracy
effect are defined over multiple training participants.

### Application Domain

Federated fine-tuning for heterogeneous interconnected LLM agents.

## Security Model

- Protected assets: global-model integrity and aggregate task accuracy.
- Threat actor: a malicious federated participant.
- Trusted components: the aggregation server follows the protocol and existing
  defenses inspect submitted updates.
- Attacker capabilities: overhear benign updates and upload a crafted local model
  update.
- Security assumptions: attackers can estimate structural correlations among
  benign parameters while remaining inside accepted statistical ranges.

## Main Contribution

The paper proposes graph representation-based model poisoning (GRMP). It builds a
feature-correlation graph from benign updates, uses a variational graph
autoencoder to model dependencies, and optimizes malicious updates that degrade
the global model while resembling benign submissions.

## Attack or Failure

- Attack surface: federated update exchange and server-side aggregation.
- Attack mechanism: graph-modeled, statistically camouflaged poisoning updates.
- System-level failure: distributed training and aggregate model-integrity
  failure.
- Security consequence: global accuracy decreases while prevailing
  distance/similarity defenses fail to flag the update.

## Defense

- Defense mechanism: existing statistical defenses are evaluated, not proposed.
- Intervention point: aggregation-time update screening.
- Required observability: submitted model updates and their distance or
  similarity statistics.
- Assumptions: anomalous updates are separable from benign clients under the
  defense metric.
- Limitations: GRMP targets that assumption; results concern the tested federated
  models and data distributions.

## Evaluation

- Evaluated systems: federated fine-tuning with heterogeneous client data and
  multiple LLM configurations.
- Agent configuration: benign clients plus one or more poisoning participants and
  a central aggregator.
- Dataset or environment: federated text-task configurations described in the
  paper.
- Baselines: conventional poisoning attacks and distance/similarity defenses.
- Metrics: global-model accuracy degradation and attack detectability.
- Main results: crafted updates reduce global accuracy while retaining benign-like
  statistics under the evaluated defenses.

## Relation to Existing Work

- Papers compared by the authors: model poisoning, federated LLM training, and
  robust aggregation.
- Claimed research gap: prevailing defenses rely on first-order distance or
  similarity signals that weaken for heterogeneous billion-parameter models.
- Closest related work: graph-based poisoning of federated models.
- Difference from prior work: GRMP captures higher-order feature correlations for
  heterogeneous LLM-agent participants.

## Relevance to Our SoK

- Included concepts: malicious member, shared model state, distributed authority,
  and aggregation integrity.
- Taxonomy implications: the mechanism is training-time poisoning; the violated
  property is collective model integrity.
- Supported research questions: whether federated-agent defenses remain valid
  under heterogeneous updates and adaptive statistical mimicry.
- Important limitations: federated fine-tuning is a narrower interaction form
  than message-passing inference-time MAS.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| GRMP constructs a feature-correlation graph from overheard benign updates. | Explicit author claim | Paper | Abstract; method | PDF 1 onward | Not applicable | The graph and variational autoencoder model higher-order dependencies. |
| The malicious update aims to retain benign-like statistics while degrading accuracy. | Explicit author claim | Paper | Abstract; optimization | PDF 1 onward | Not applicable | Statistical camouflage and adversarial degradation are joint objectives. |
| The formal paper has six authors, including Sai Zou. | Verified metadata | Crossref/IEEE metadata | Bibliographic record | Not applicable | Not applicable | DOI metadata supplies the formal-version author list and pages 956-961. |
| The paper was accepted at IWCMC 2026. | Verified metadata | IEEE DOI; arXiv version comment | Bibliographic record | Not applicable | Not applicable | Both records identify the 2026 IWCMC proceedings. |

## Provenance

- Discovery source: IEEE DOI metadata; Crossref; arXiv; prior systematic corpus
- Discovery query: `IWCMC 2026 Graph Representation-based Model Poisoning Internet of Agents`
- Accessed version: published IWCMC metadata with arXiv v3 full text
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

