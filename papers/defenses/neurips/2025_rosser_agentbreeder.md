# AgentBreeder: Mitigating the AI Safety Risks of Multi-Agent Scaffolds via Self-Improvement

## Citation
Title: AgentBreeder: Mitigating the AI Safety Risks of Multi-Agent Scaffolds via Self-Improvement
Authors: J Rosser; Jakob Foerster
Year: 2025
Venue: NeurIPS
DOI: Not reported
Primary URL: https://proceedings.neurips.cc/paper_files/paper/2025/hash/dc2ccde7ee43e5719e08c68e848bd65a-Abstract-Conference.html
Open access URL: https://proceedings.neurips.cc/paper_files/paper/2025/file/dc2ccde7ee43e5719e08c68e848bd65a-Paper-Conference.pdf
BibTeX key: rosser2025agentbreeder

## Paper Type
Defense; Attack; Evaluation; Empirical study

## Scope
### System Studied
Multi-agent scaffolds composed of generated roles, prompts, and communication patterns.
### Multi-Agent Dependency
Safety changes arise from the composed scaffold and are optimized at the architecture level.
### Application Domain
General reasoning, mathematics, and safety evaluation.

## Security Model
### Protected Assets
Safety behavior while preserving capability.
### Threat Actor
No fixed external attacker; red-mode search exposes unsafe scaffold compositions.
### Trusted Components
The evolutionary evaluator and selected safety benchmark.
### Attacker Capabilities
Search over scaffold designs that jointly optimize capability and unsafe behavior.
### Security Assumptions
Benchmark objectives meaningfully represent deployment safety.

## Main Contribution
AgentBreeder performs multi-objective evolutionary search over agent scaffolds. Blue mode searches for safer capable systems, while red mode demonstrates that unsafe scaffolds can emerge during capability optimization.

## Attack or Failure
### Attack Surface
Role, prompt, and communication composition.
### Attack Mechanism
Architecture search discovers scaffold-level behavior not evident from one component.
### System-Level Failure
Capability optimization selects unsafe interaction structures.
### Security Consequence
Compositional safety degradation.

## Defense
### Defense Mechanism
Multi-objective search that includes explicit safety fitness.
### Intervention Point
System architecture and coordination design.
### Required Observability
End-to-end scaffold outcomes on capability and safety evaluations.
### Assumptions
Fitness tests generalize and reward hacking is controlled.
### Limitations
The authors discuss benchmark reward hacking, finite search budgets, and limited transfer evidence.

## Evaluation
### Evaluated Systems
Evolved LLM multi-agent scaffolds.
### Agent Configuration
Generated scaffold programs compared with hand-designed baselines.
### Dataset or Environment
Reasoning, mathematics, and safety benchmarks implemented in Inspect.
### Baselines
Chain-of-thought, self-consistency, and hand-designed multi-agent scaffolds.
### Metrics
Capability and safety benchmark scores.
### Main Results
The authors report a 79.4% average safety-benchmark uplift in blue mode while retaining capability, and unsafe scaffold discovery in red mode.

## Relation to Existing Work
### Papers Compared by the Authors
Automated agent design and multi-agent scaffold baselines.
### Claimed Research Gap
Scaffold optimization rarely treats safety as an explicit objective.
### Closest Related Work
Automated agent architecture search.
### Difference From Prior Work
The search is explicitly dual-use, exposing and mitigating composition risks.

## Relevance to Our SoK
### Included Concepts
Architecture, coordination, objective structure, and interaction evidence.
### Taxonomy Implications
Defense locus is system design; function is prevention by scaffold selection.
### Supported Research Questions
Can safety be optimized without conflating architecture, compute, and task effects?
### Important Limitations
Safety-benchmark improvements are not security guarantees.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| AgentBreeder searches scaffold designs in blue and red modes. | Explicit author claim | Paper | 4 | 4-6 | Framework figure | Search procedure. |
| Authors report 79.4% average safety uplift in blue mode. | Explicit author claim | Paper | Abstract; 5 | 1; 7-9 | Results | Highlighted benchmark result. |
| The method is design-time prevention rather than runtime enforcement. | Corpus interpretation | Paper | 4 | 4-6 | Framework figure | Defense placement. |

## Provenance
### Discovery Source
NeurIPS proceedings; arXiv version reconciliation.
### Discovery Query
AgentBreeder NeurIPS 2025 official
### Accessed Version
Published NeurIPS 2025 version.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
