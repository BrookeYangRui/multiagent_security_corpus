# Goal-Aware Identification and Rectification of Misinformation in Multi-Agent Systems

## Citation
Title: Goal-Aware Identification and Rectification of Misinformation in Multi-Agent Systems
Authors: Zherui Li; Yan Mi; Zhenhong Zhou; Houcheng Jiang; Guibin Zhang; Kun Wang; Junfeng Fang
Year: 2025
Venue: arXiv
DOI: 10.48550/arXiv.2506.00509
Primary URL: https://arxiv.org/abs/2506.00509
Open access URL: https://arxiv.org/pdf/2506.00509
BibTeX key: li2025argus

## Paper Type
Defense; Benchmark; Evaluation; Empirical study

## Scope
### System Studied
Task-oriented LLM-agent networks exposed to misinformation injection.
### Multi-Agent Dependency
ARGUS evaluates and repairs information as it moves between agents relative to the global task goal.
### Application Domain
Complex collaborative tasks with tools.

## Security Model
### Protected Assets
Collective task and factual integrity.
### Threat Actor
Member or input-level misinformation injector.
### Trusted Components
Goal-aware review and rectification stages.
### Attacker Capabilities
Insert persuasive false claims into agent messages.
### Security Assumptions
The task goal and enough countervailing knowledge are available to the reviewer.

## Main Contribution
The paper introduces MisinfoTask and ARGUS, a training-free two-stage framework that identifies goal-relevant false claims and rectifies downstream information flow.

## Attack or Failure
### Attack Surface
Inter-agent messages.
### Attack Mechanism
False claims enter and propagate through task decomposition.
### System-Level Failure
The group acts on misinformation.
### Security Consequence
Collective decision and action integrity loss.

## Defense
### Defense Mechanism
Goal-aware claim review followed by message rectification.
### Intervention Point
Message protocol.
### Required Observability
Task goal, message content, sender context, and downstream state.
### Assumptions
Reviewer reasoning is more reliable than attacked messages.
### Limitations
LLM-based adjudication can inherit knowledge and judgment errors.

## Evaluation
### Evaluated Systems
Several LLM backbones in multi-agent task workflows.
### Agent Configuration
Task decomposition and message passing under multiple injection attacks.
### Dataset or Environment
MisinfoTask.
### Baselines
Prompt defenses and misinformation-detection variants.
### Metrics
Attack success, identification, rectification, and task performance.
### Main Results
The authors report a large average attack-success reduction across evaluated injection settings.

## Relation to Existing Work
### Papers Compared by the Authors
Misinformation and prompt-injection defenses.
### Claimed Research Gap
Generic filtering ignores the receiving system's current goal.
### Closest Related Work
Message-level MAS safeguards.
### Difference From Prior Work
ARGUS explicitly conditions detection and repair on task intent.

## Relevance to Our SoK
### Included Concepts
Message monitoring, goal context, rectification, and benchmark extraction.
### Taxonomy Implications
Defense locus is message; functions are detection and recovery.
### Supported Research Questions
What global context is required to judge local communication?
### Important Limitations
The work remains a preprint and uses an LLM-based evaluator.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The paper introduces MisinfoTask and two-stage ARGUS. | Explicit author claim | Paper | Abstract; 3-4 | 1; 3-7 | Framework figure | Dataset and method. |
| Evaluation tests multiple misinformation injections. | Explicit author claim | Paper | 5 | 7-10 | Results tables | Evaluation scope. |
| ARGUS needs more than per-message content because it conditions on the system goal. | Corpus interpretation | Paper | 4 | 5-7 | Method | Observer requirement. |

## Provenance
### Discovery Source
arXiv API; prior corpus defense scan.
### Discovery Query
goal-aware misinformation multi-agent ARGUS
### Accessed Version
arXiv v1.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
