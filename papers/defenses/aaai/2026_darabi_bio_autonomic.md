# Resilience in Ambient Multi-Agent LLMs via Decentralized Bio-Autonomic Control and Immune-Inspired Anomaly Detection

## Citation
Title: Resilience in Ambient Multi-Agent LLMs via Decentralized Bio-Autonomic Control and Immune-Inspired Anomaly Detection
Authors: Nastaran Darabi; Devashri Naik; Sina Tayebati; Dinithi Jayasuriya; Amit R. Trivedi
Year: 2026
Venue: AAAI
DOI: 10.1609/aaai.v40i44.41065
Primary URL: https://ojs.aaai.org/index.php/AAAI/article/view/41065
Open access URL: https://ojs.aaai.org/index.php/AAAI/article/download/41065/45026
BibTeX key: darabi2026bioautonomic

## Paper Type
Defense; Evaluation; Empirical study

## Scope
### System Studied
Decentralized ambient LLM agents that communicate and adapt without a central security controller.
### Multi-Agent Dependency
Agents exchange trust evidence through gossip and collectively contain compromised peers.
### Application Domain
Ambient and collaborative agent systems.

## Security Model
### Protected Assets
Collective task integrity, control flow, and continued operation.
### Threat Actor
Compromised member agents.
### Trusted Components
Local MAPE-K loops, immune-inspired detectors, and cryptographic aggregation components.
### Attacker Capabilities
Manipulate local behavior and inter-agent control flow.
### Security Assumptions
Enough honest agents can exchange trustworthy local evidence.

## Main Contribution
The framework equips each agent with a MAPE-K autonomic loop, a Dendritic Cell Algorithm detector, trust scoring, gossip, federated learning, and encrypted aggregation.

## Attack or Failure
### Attack Surface
Agent behavior and decentralized communication.
### Attack Mechanism
Compromised agents send anomalous outputs or hijack control flow.
### System-Level Failure
Distributed collaboration accepts or propagates malicious behavior.
### Security Consequence
Integrity and resilience loss.

## Defense
### Defense Mechanism
Local anomaly signals are fused into decentralized trust and response decisions.
### Intervention Point
Agent-local monitors plus peer trust protocol.
### Required Observability
Local behavior features and exchanged trust summaries.
### Assumptions
Gossip and federated updates remain sufficiently available and honest-majority signals dominate.
### Limitations
Bio-inspired modules and simulated attack settings may not transfer unchanged to open deployments.

## Evaluation
### Evaluated Systems
Ambient multi-agent LLM task configurations.
### Agent Configuration
Decentralized peers using gossip and local control loops.
### Dataset or Environment
Collaborative tasks with injected malicious behavior and control-flow hijacking.
### Baselines
Centralized and component-ablated resilience methods.
### Metrics
Malicious-agent identification, control-flow hijack rate, and collaborative performance.
### Main Results
The authors report improved malicious-agent identification and task retention across tested attacks.

## Relation to Existing Work
### Papers Compared by the Authors
Autonomic computing, immune-inspired anomaly detection, and MAS trust methods.
### Claimed Research Gap
Centralized safeguards create bottlenecks and single points of failure.
### Closest Related Work
Decentralized trust and anomaly monitoring.
### Difference From Prior Work
The paper combines local autonomic control with distributed immune-style evidence exchange.

## Relevance to Our SoK
### Included Concepts
Decentralized monitoring, trust propagation, containment, and recovery.
### Taxonomy Implications
Defense spans agent-local and protocol loci and includes recovery-oriented control.
### Supported Research Questions
Can distributed observation replace a trusted global monitor?
### Important Limitations
The trust assumptions need explicit normalization against colluding coalitions.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The architecture combines MAPE-K, DCA, gossip, federated learning, and encrypted aggregation. | Explicit author claim | Paper | Method | 2-5 | Architecture figure | Component design. |
| Evaluation reports MAI and control-flow hijack rate. | Explicit author claim | Paper | Evaluation | 6-7 | Metrics subsection | Metric definitions. |
| The defense distributes rather than centralizes observer scope. | Corpus interpretation | Paper | Method | 2-5 | Architecture figure | Placement of monitors. |

## Provenance
### Discovery Source
AAAI proceedings; DOI registry; prior corpus defense scan.
### Discovery Query
AAAI bio-autonomic multi-agent LLM resilience
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
