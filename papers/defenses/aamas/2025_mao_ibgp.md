# IBGP: Imperfect Byzantine Generals Problem for Zero-Shot Robustness in Communicative Multi-Agent Systems

## Citation
Title: IBGP: Imperfect Byzantine Generals Problem for Zero-Shot Robustness in Communicative Multi-Agent Systems
Authors: Yihuan Mao; Yipeng Kang; Peilun Li; Lichao Sun; Wei Wang; Mingsong Chen; Yang Liu
Year: 2025
Venue: AAMAS
DOI: Not reported
Primary URL: https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p2654.pdf
Open access URL: https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p2654.pdf
BibTeX key: mao2025ibgp

## Paper Type
Defense; Theoretical analysis; Evaluation

## Scope
### System Studied
Communicative agents that require local coordination rather than global byte-identical consensus.
### Multi-Agent Dependency
The protocol explicitly reasons about malicious population fractions and local k-of-n agreement.
### Application Domain
Collaborative reasoning and sensor-network coordination.

## Security Model
### Protected Assets
Local coordination consistency under faulty members.
### Threat Actor
Byzantine member agents with unknown identities.
### Trusted Components
Protocol execution and honest local neighborhoods.
### Attacker Capabilities
Send arbitrary conflicting messages.
### Security Assumptions
Correctness uses the paper's imperfect/local agreement predicate rather than classical global agreement.

## Main Contribution
IBGP reformulates Byzantine coordination around local practical agreement and proposes a zero-shot LLM-agent protocol with analytical and empirical resilience evidence.

## Attack or Failure
### Attack Surface
Coordination messages.
### Attack Mechanism
Byzantine members send inconsistent or false proposals.
### System-Level Failure
Agents fail to coordinate on locally compatible actions.
### Security Consequence
Decision-integrity and coordination failure.

## Defense
### Defense Mechanism
Local consensus rules tailored to imperfect agreement.
### Intervention Point
Coordination protocol.
### Required Observability
Messages from the relevant local participant set.
### Assumptions
Local k-of-n coordination suffices for the application.
### Limitations
The guarantee is not classical global Byzantine agreement and should not be compared directly with the f<n/3 ceiling.

## Evaluation
### Evaluated Systems
Communicative LLM agents and a sensor-network case study.
### Agent Configuration
Variable malicious fractions and local coordination groups.
### Dataset or Environment
Reasoning tasks plus sensor coordination.
### Baselines
Standard communication and voting approaches.
### Metrics
Task success and coordination under malicious fractions.
### Main Results
The authors report empirical robustness under the relaxed local-agreement definition.

## Relation to Existing Work
### Papers Compared by the Authors
Classical BGP and LLM-agent consensus methods.
### Claimed Research Gap
Global consensus is unnecessarily strict for many MAS tasks.
### Closest Related Work
Byzantine agreement and robust voting.
### Difference From Prior Work
IBGP changes the correctness predicate to local coordination.

## Relevance to Our SoK
### Included Concepts
Byzantine capability, agreement definitions, denominator, and assumption normalization.
### Taxonomy Implications
Defense locus is protocol; protected property is local coordination integrity.
### Supported Research Questions
Which classical assumptions are relaxed by apparent super-ceiling claims?
### Important Limitations
This is an AAMAS extended abstract and provides less detail than a full paper.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| IBGP replaces global agreement with local coordination properties. | Explicit author claim | Paper | 1-2 | 1-2 | Definitions | Correctness predicate. |
| The paper evaluates a sensor-network case study. | Explicit author claim | Paper | 4 | 3 | Case study | Evaluation setting. |
| Super-ceiling comparison requires assumption normalization. | Corpus interpretation | Paper | 2 | 2 | Definitions | Strict agreement is relaxed. |

## Provenance
### Discovery Source
AAMAS official proceedings; prior Byzantine audit.
### Discovery Query
site:ifaamas.org IBGP AAMAS 2025
### Accessed Version
Published AAMAS 2025 extended abstract.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
