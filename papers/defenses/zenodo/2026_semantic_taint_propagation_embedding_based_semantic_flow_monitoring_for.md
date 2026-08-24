# Semantic Taint Propagation: Embedding-Based Semantic Flow Monitoring for Multi-Agent Large Language Model Systems

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set2_emerging` · `defense` · venue `Zenodo (CERN European Organization for Nuclear Research)` · signoff `2026-08-21`.
> **Source-review correction (2026-08-24):** the primary violated property is confidentiality / private-data leakage (`R5`), not propagation persistence (`R1`).
<!-- FINAL_CORPUS_STATUS_END -->

## Citation metadata

* Year: 2026
* Venue: Zenodo (CERN European Organization for Nuclear Research)
* DOI (all versions): 10.5281/zenodo.20834834
* Version DOI: 10.5281/zenodo.20834835
* Published: 2026-06-24
* arXiv: N/A
* Primary URL: https://zenodo.org/records/20834835
* Full text: https://zenodo.org/records/20834835/files/Semantic%20Taint%20Propagation.pdf?download=1

## Final corpus classification

* Work key: `doi:10.5281/zenodo.20834834`
* Evidence set: `set2_emerging`
* Dominant contribution: `defense`
* Interaction interfaces: `I2_communication_routing;I4_delegation_action;I6_observation_defense`
* Risk or property: `R5_private_data_leakage`
* Interaction dependence: `interaction_amplified`

## Source-review rationale

The paper's motivating failure is disclosure of sensitive records when adversarial text reaches data-access agents through retrieved documents or inter-agent messages. STP monitors semantic information flow against sensitive and authorized concept anchors and evaluates indirect-injection scenarios, including keyword-free attacks. Propagation is the mechanism by which adversarial influence reaches downstream agents, but the protected property and measured security consequence are confidentiality and unauthorized private-data disclosure. Therefore `R5_private_data_leakage` is the primary risk mapping.
