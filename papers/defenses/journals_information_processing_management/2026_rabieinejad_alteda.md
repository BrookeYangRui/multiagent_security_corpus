# ALTEDA: An Adaptive Layered Threat Detection Architecture for Multi-Agent Systems

## Citation
Title: ALTEDA: An Adaptive Layered Threat Detection Architecture for Multi-Agent Systems
Authors: Elnaz Rabieinejad; Fattane Zarrinkalam; Ali Dehghantanha
Year: 2026
Venue: Information Processing & Management
DOI: 10.1016/j.ipm.2026.104768
Primary URL: https://doi.org/10.1016/j.ipm.2026.104768
Open access URL: https://www.sciencedirect.com/science/article/pii/S030645732600129X
BibTeX key: rabieinejad2026alteda

## Paper Type
Defense; Evaluation; Empirical study

## Scope
### System Studied
Multi-agent applications observed through synchronized application, network, and system logs.
### Multi-Agent Dependency
The detector correlates events across agents and infrastructure to identify distributed attack traces.
### Application Domain
Operational multi-agent deployments.

## Security Model
### Protected Assets
System integrity, availability, and auditability.
### Threat Actor
External or compromised-agent attackers producing cross-layer traces.
### Trusted Components
Log collection, synchronization, graph construction, and detector.
### Attacker Capabilities
Trigger attacks visible across application, network, or host telemetry.
### Security Assumptions
Telemetry is trustworthy and sufficiently complete.

## Main Contribution
ALTEDA builds graph representations from synchronized multi-layer logs and performs early threat detection without storing prompt or response content.

## Attack or Failure
### Attack Surface
Agent application, network, and system layers.
### Attack Mechanism
Distributed malicious actions create correlated cross-layer events.
### System-Level Failure
Local log inspection misses the combined attack path.
### Security Consequence
Delayed detection and reduced attribution.

## Defense
### Defense Mechanism
Cross-layer temporal graph construction and adaptive threat classification.
### Intervention Point
Global telemetry and trace analysis.
### Required Observability
Synchronized application, network, and operating-system events.
### Assumptions
Stable clocks, agent attribution, and intact log pipelines.
### Limitations
Evaluation uses generated traces; encrypted or missing telemetry can reduce visibility.

## Evaluation
### Evaluated Systems
A multi-agent test environment instrumented at three telemetry layers.
### Agent Configuration
Interacting agents producing benign and attacked execution traces.
### Dataset or Environment
800 traces; the paper reports 31.4% attack traces.
### Baselines
Single-layer and non-adaptive detection variants.
### Metrics
Detection performance, false alarms, and earliest detection point.
### Main Results
The authors report early detection at roughly 40% of an attack trace while avoiding prompt-content collection.

## Relation to Existing Work
### Papers Compared by the Authors
Log-based intrusion detection and agent anomaly monitoring.
### Claimed Research Gap
Single-layer monitoring misses distributed agent attack context.
### Closest Related Work
Graph-based cross-layer threat detection.
### Difference From Prior Work
ALTEDA correlates three telemetry planes while excluding message content.

## Relevance to Our SoK
### Included Concepts
Global trace, provenance, attribution, privacy-preserving observability, and detection.
### Taxonomy Implications
Defense locus is global trace; function is detection and attribution.
### Supported Research Questions
Which global properties can be detected without reading message content?
### Important Limitations
The trace generator and deployment instrumentation constrain external validity.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| ALTEDA correlates application, network, and system logs without prompt content. | Explicit author claim | Paper | Architecture | HTML full text | Architecture figure | Telemetry contract. |
| Evaluation contains 800 traces and reports 31.4% attack success. | Explicit author claim | Paper | Evaluation | HTML full text | Dataset table | Evaluation population. |
| Required observer scope is global but content-minimizing. | Corpus interpretation | Paper | Architecture | HTML full text | Architecture figure | Observed variables. |

## Provenance
### Discovery Source
ScienceDirect; Crossref DOI; prior corpus defense scan.
### Discovery Query
ALTEDA multi-agent threat detection 104768
### Accessed Version
Published journal HTML version.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
