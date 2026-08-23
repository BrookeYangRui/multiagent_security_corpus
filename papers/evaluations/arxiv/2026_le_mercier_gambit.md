# GAMBIT: A Three-Mode Benchmark for Adversarial Robustness in Multi-Agent LLM Collectives

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set2_emerging` · `evaluation` · venue `arXiv` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

Title: GAMBIT: A Three-Mode Benchmark for Adversarial Robustness in Multi-Agent LLM Collectives

Authors: Alexandre Le Mercier; Chris Develder; Thomas Demeester

Year: 2026

Venue: arXiv

DOI: 10.48550/arXiv.2605.09027

Primary URL: https://arxiv.org/abs/2605.09027

Open access URL: https://arxiv.org/pdf/2605.09027

BibTeX key: lemercier2026gambit

## Paper Type

Benchmark; Evaluation; Attack; Defense; Empirical study

## Scope

### System Studied
Chess-solving LLM collectives containing an adaptive imposter and external detector.

### Multi-Agent Dependency
The imposter influences group deliberation while adapting its messages to evade a detector trained on earlier strategies.

### Application Domain
Strategic collaborative reasoning.

## Security Model

### Protected Assets
Collective task performance and detector robustness.

### Threat Actor
An adaptive imposter agent.

### Trusted Components
Chess environment, cost function, labels, and held-out evaluation harness.

### Attacker Capabilities
Co-evolve messaging strategies against surface-level detectors.

### Security Assumptions
Chess provides deterministic correctness and difficulty control.

## Main Contribution

GAMBIT introduces 27,804 labeled instances covering 240 co-evolved imposter strategies. Its three modes measure zero-shot detection under distribution shift and few-shot recalibration from twenty labeled examples using two independent scores.

## Attack or Failure

### Attack Surface
Inter-agent deliberation.

### Attack Mechanism
An imposter supplies strategically deceptive reasoning and adapts to the detector.

### System-Level Failure
The collective answer degrades while malicious participation remains undetected.

### Security Consequence
Collective integrity and monitoring failure.

## Defense

### Defense Mechanism
Model-independent discussion detectors and meta-learned recalibration.

### Intervention Point
Conversation monitoring.

### Required Observability
Collective discussion and imposter labels during calibration.

### Assumptions
Twenty labeled post-shift examples are available for recalibration mode.

### Limitations
Chess and one adaptive-attack generator may not represent all collaborative tasks.

## Evaluation

### Evaluated Systems
Gemini-based collectives and multiple detector variants.

### Agent Configuration
Benign solvers plus one adaptive imposter.

### Dataset or Environment
22,104 training and 5,700 held-out instances.

### Baselines
Surface detectors and meta-learned variants across three modes.

### Metrics
Zero-shot detection score and recalibration/adaptation score, including F1.

### Main Results
Near-identical zero-shot detectors differ by 8x in few-shot adaptation; the meta-learned variant converges 20x faster in the reported setup.

## Relation to Existing Work

### Papers Compared by the Authors
Static malicious-agent and imposter-detection studies.

### Claimed Research Gap
Static evaluation does not measure robustness to an adversary that adapts to the detector.

### Closest Related Work
Who’s the Mole and topology-aware malicious-agent detection.

### Difference From Prior Work
Attacks and defenses co-evolve and recalibration is a separate evaluation mode.

## Relevance to Our SoK

### Included Concepts
Adaptive adversary, observer, detection, distribution shift, and recalibration.

### Taxonomy Implications
Shows that a defense contract includes adaptation data and post-deployment update assumptions.

### Supported Research Questions
Does a detector adapt after the attack distribution shifts?

### Important Limitations
Current evidence is preprint-only.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The dataset has 27,804 instances and 240 imposter strategies. | Explicit author claim | Paper | Abstract; 3 | 1; 4-7 | - | Dataset scale. |
| Three modes separate zero-shot shift from twenty-example recalibration. | Explicit author claim | Paper | Abstract; 3 | 1; 4-7 | Figure 1 | Evaluation design. |
| Zero-shot similarity can conceal large adaptation differences. | Explicit author claim | Paper | Abstract; 5 | 1; 9-12 | Results figures | Main finding. |

## Provenance

### Discovery Source
arXiv; benchmark keyword search.

### Discovery Query
multi-agent LLM adaptive imposter benchmark

### Accessed Version
arXiv v2.

### Access Date
2026-08-05
### Prepared By
Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status
agent_unverified

### Last Updated
2026-08-05
