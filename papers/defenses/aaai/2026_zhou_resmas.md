# ResMAS: Resilience Optimization in LLM-based Multi-agent Systems

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `defense` · venue `AAAI` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation
Title: ResMAS: Resilience Optimization in LLM-based Multi-agent Systems
Authors: Zhilun Zhou; Zihan Liu; Jiahe Liu; Qingyu Shao; Yihan Wang; Kun Shao; Depeng Jin; Fengli Xu
Year: 2026
Venue: AAAI
DOI: 10.1609/aaai.v40i41.40824
Primary URL: https://ojs.aaai.org/index.php/AAAI/article/view/40824
Open access URL: https://ojs.aaai.org/index.php/AAAI/article/download/40824/44785
BibTeX key: zhou2026resmas

## Paper Type
Defense; Evaluation; Empirical study

## Scope
### System Studied
LLM-based MAS whose communication topology and agent prompts can be optimized.
### Multi-Agent Dependency
Resilience is treated as a system property determined jointly by topology and distributed agent behavior.
### Application Domain
Collaborative problem solving under perturbations.

## Security Model
### Protected Assets
Collective task performance under faulty or adversarial influence.
### Threat Actor
Perturbed or faulty member agents.
### Trusted Components
The topology generator and prompt optimizer.
### Attacker Capabilities
Corrupt selected agent behavior or communication.
### Security Assumptions
Deployment topology and prompts can be optimized before use.

## Main Contribution
ResMAS jointly searches for resilient graph structures and topology-aware agent prompts to improve system performance under perturbations.

## Attack or Failure
### Attack Surface
Member-agent outputs and influence paths.
### Attack Mechanism
Faulty contributions are amplified by vulnerable topology.
### System-Level Failure
Collective decisions become brittle under perturbation.
### Security Consequence
Loss of robustness and availability of correct collaboration.

## Defense
### Defense Mechanism
Topology generation plus topology-aware prompt optimization.
### Intervention Point
System design, topology, and agent instructions.
### Required Observability
Training-time system outcomes and topology; no privileged runtime message monitor is central.
### Assumptions
The defender can redesign the graph and prompts.
### Limitations
Optimization is tied to modeled perturbations and evaluated task distributions.

## Evaluation
### Evaluated Systems
LLM multi-agent collaboration configurations.
### Agent Configuration
Generated topologies with specialized prompts.
### Dataset or Environment
Reasoning tasks under multiple perturbation settings.
### Baselines
Fixed common topologies and non-resilience-aware optimization.
### Metrics
Task accuracy and resilience under perturbation.
### Main Results
The authors report improved robustness relative to fixed-topology baselines.

## Relation to Existing Work
### Papers Compared by the Authors
MAS topology optimization and robustness methods.
### Claimed Research Gap
Prior work optimizes nominal performance rather than adversarial resilience.
### Closest Related Work
Topology-aware MAS design.
### Difference From Prior Work
ResMAS co-optimizes graph structure and role prompts for perturbed operation.

## Relevance to Our SoK
### Included Concepts
Topology defense, design-time prevention, and interaction evidence.
### Taxonomy Implications
This is a prevention-oriented topology defense rather than a runtime detector.
### Supported Research Questions
Which defenses modify the interaction structure before deployment?
### Important Limitations
Evidence does not establish robustness to unmodeled adaptive attacks.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| ResMAS jointly optimizes topology and prompts. | Explicit author claim | Paper | Abstract; Method | 1; 3-5 | Framework figure | Core design. |
| Evaluation tests resilience under perturbations. | Explicit author claim | Paper | Experiments | 5-8 | Results tables | Evaluation contract. |
| The primary function is design-time prevention. | Corpus interpretation | Paper | Method | 3-5 | Framework figure | Placement in defense model. |

## Provenance
### Discovery Source
AAAI proceedings; DOI registry; prior corpus defense scan.
### Discovery Query
ResMAS AAAI 2026 resilience optimization
### Accessed Version
Published AAAI 2026 version.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
