# SoK: Attack and Defense Landscape of Agentic AI Systems

## Citation
Title: SoK: Attack and Defense Landscape of Agentic AI Systems
Authors: Juhee Kim; Wenbo Guo; Dawn Song
Year: 2026
Venue: USENIX Security
DOI: Not reported
Primary URL: https://www.usenix.org/conference/usenixsecurity26/presentation/kim-juhee-agentic
Open access URL: https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_kim-juhee-agentic.pdf
BibTeX key: kim2026agenticai

## Paper Type
SoK; Survey

## Scope
### System Studied
Agentic AI systems organized around components such as models, prompts, memory, tools, and environment.
### Multi-Agent Dependency
Multi-agent systems appear as a partial case, but the primary organizing boundary is the single agent's component stack.
### Application Domain
General-purpose agentic AI.

## Security Model
### Protected Assets
Agent confidentiality, integrity, availability, and trustworthy execution.
### Threat Actor
Users, external inputs, compromised resources, and other adversarial entities.
### Trusted Components
Varies across surveyed papers.
### Attacker Capabilities
Prompt, memory, tool, model, and environment manipulation.
### Security Assumptions
The SoK normalizes heterogeneous primary-paper assumptions rather than imposing one deployment model.

## Main Contribution
Kim et al. systematize agentic-AI attacks and defenses using seven design dimensions and component-indexed attack surfaces. It is the closest formal SoK comparator for an interaction-centered MAS landscape.

## Attack or Failure
### Attack Surface
Model, prompt, memory, tools, environment, and agent orchestration.
### Attack Mechanism
Varies across the surveyed corpus.
### System-Level Failure
Primarily component compromise; collective failures are not the sole taxonomy axis.
### Security Consequence
Security and privacy loss in agentic systems.

## Defense
### Defense Mechanism
Catalogs preventive, detective, and mitigating techniques across agent components.
### Intervention Point
Multiple component layers.
### Required Observability
Varies by defense.
### Assumptions
Varies by cited work.
### Limitations
Interaction topology, coalition behavior, membership, and distributed authority are not the primary organizing boundary.

## Evaluation
### Evaluated Systems
Not applicable; literature systematization.
### Agent Configuration
Varies across the corpus.
### Dataset or Environment
Not applicable.
### Baselines
Prior surveys and taxonomies.
### Metrics
Corpus and taxonomy coverage rather than a benchmark metric.
### Main Results
The paper identifies recurring attack surfaces and defense gaps across agent designs.

## Relation to Existing Work
### Papers Compared by the Authors
Prior LLM security and agent-security surveys.
### Claimed Research Gap
Earlier work lacks a system-level organization tailored to autonomous agents.
### Closest Related Work
Broad LLM security surveys.
### Difference From Prior Work
The SoK centers agentic design dimensions and attack-defense mapping.

## Relevance to Our SoK
### Included Concepts
Design vocabulary, component boundary, threat actors, and attack-defense mapping.
### Taxonomy Implications
Provides the single-agent boundary against which interaction-native risks are defined.
### Supported Research Questions
What security properties become non-degenerate only when n is at least two?
### Important Limitations
MAS coverage should be measured from the paper rather than inferred from title or venue.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The SoK organizes agentic security around seven design dimensions. | Explicit author claim | Paper | Overview; System model | 2-5 | Taxonomy figures | Organizing framework. |
| It is a component-boundary comparator, not an interaction-centered MAS taxonomy. | Corpus interpretation | Paper | Taxonomy sections | 5-20 | Attack-defense figures | Comparative coding. |

## Provenance
### Discovery Source
USENIX Security official program and paper.
### Discovery Query
site:usenix.org agentic AI SoK Kim
### Accessed Version
Published USENIX Security 2026 version.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
