# Rethinking the Reliability of Multi-agent Systems: A Perspective from Byzantine Fault Tolerance

## Citation

Title: Rethinking the Reliability of Multi-agent Systems: A Perspective from Byzantine Fault Tolerance

Authors: Lifan Zheng; Jiawei Chen; Qinghong Yin; Jingyuan Zhang; Xinyi Zeng; Yu Tian

Year: 2026

Venue: AAAI

DOI: 10.1609/aaai.v40i41.40806

Primary URL: https://ojs.aaai.org/index.php/AAAI/article/view/40806

Open access URL: https://ojs.aaai.org/index.php/AAAI/article/download/40806/44767

BibTeX key: zheng2026byzantinereliability

## Paper Type

- Attack
- Defense
- Evaluation
- Empirical study

## Scope

### System Studied

Seven-node LLM-based multi-agent systems performing mathematical reasoning and safety classification under multiple communication topologies.

### Multi-Agent Dependency

Faulty nodes inject wrong answers into message flows, while honest agents update from neighbors and a collective mechanism aggregates their outputs. Reliability depends on the fraction and placement of Byzantine nodes and on topology.

### Application Domain

Collaborative reasoning and safety classification.

## Security Model

### Protected Assets

Correctness and stability of collective task decisions.

### Threat Actor

Byzantine member agents that repeatedly provide an incorrect candidate answer.

### Trusted Components

The experiment controller, confidence probing model, and non-Byzantine agents.

### Attacker Capabilities

Faulty nodes send the prescribed incorrect answer through their normal graph edges; the number and topology position of faulty nodes are varied.

### Security Assumptions

The setting is an oracle-scored task protocol, not a proof of asynchronous Byzantine agreement with classical validity and termination guarantees.

## Main Contribution

The paper measures LLM-agent task robustness under faulty neighbors and proposes CP-WBFT, which probes confidence and weights candidate answers before aggregation. It evaluates prompt-level and hidden-state confidence probes across six network topologies.

## Attack or Failure

### Attack Surface

Protocol-valid messages from faulty member nodes.

### Attack Mechanism

Byzantine nodes repeatedly introduce an incorrect answer that can be adopted by honest neighbors or dominate unweighted aggregation.

### System-Level Failure

The collective outputs the wrong mathematical answer or unsafe classification.

### Security Consequence

Collective decision-integrity failure under malicious or faulty membership.

## Defense

### Defense Mechanism

CP-WBFT estimates each answer's confidence using a prompt-level or hidden-state probe and performs confidence-weighted voting.

### Intervention Point

Collective aggregation and coordination.

### Required Observability

The coordinator sees all candidate answers and can query or access confidence representations.

### Assumptions

Candidate correctness correlates with the chosen confidence probe, and the aggregation component remains trusted.

### Limitations

The evaluation studies task accuracy and answer confidence, not a classical BFT protocol guarantee; two datasets and fixed seven-node graphs limit generalization.

## Evaluation

### Evaluated Systems

Traditional deterministic nodes and multiple LLM agents, with prompt-level and hidden-state confidence variants.

### Agent Configuration

Seven nodes in six representative topologies, with the Byzantine count varied up to six.

### Dataset or Environment

GSM8K mathematical reasoning and XSTest safety classification.

### Baselines

Traditional-agent propagation, unweighted aggregation, and alternative confidence-probe layers.

### Metrics

Task accuracy and reported reliability accuracy under Byzantine-node configurations.

### Main Results

The paper reports that LLM agents resist erroneous message flows better than traditional deterministic nodes and that CP-WBFT retains high task accuracy in its tested extreme-fault configurations.

## Relation to Existing Work

### Papers Compared by the Authors

Classical Byzantine fault tolerance, LLM confidence estimation, multi-agent debate, and graph reliability work.

### Claimed Research Gap

The effect of replacing traditional agents with LLM-based agents on fault tolerance had not been quantified across topologies.

### Closest Related Work

Byzantine-robust LLM coordination and weighted collective reasoning.

### Difference From Prior Work

The paper exploits LLM skepticism and semantic confidence rather than enforcing a classical authenticated consensus protocol.

## Relevance to Our SoK

### Included Concepts

Fault fraction, topology, malicious membership, answer propagation, trusted aggregation, confidence weighting, and validity definition.

### Taxonomy Implications

This is collective decision integrity under faulty members. Its reported high fault tolerance must be coded as oracle-graded task accuracy, not as exceeding the classical asynchronous agreement ceiling.

### Supported Research Questions

Which assumptions and outcome definitions underlie claims of Byzantine robustness in LLM-MAS?

### Important Limitations

The paper does not establish agreement, validity, and termination under the classical model; confidence probes and a central aggregation procedure add trusted structure.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The pilot uses seven nodes and varies Byzantine nodes across topologies. | Explicit author claim | Paper | Pilot Experiment | 2-3 | Table 1; Figure 2 | Experimental design. |
| Evaluation uses GSM8K and XSTest. | Explicit author claim | Paper | Dataset and Metrics | 2; 5 | - | Dataset definitions. |
| CP-WBFT weights answers using prompt-level or hidden-state confidence probes. | Explicit author claim | Paper | Method | 3-5 | Figure 3 | Framework definition. |
| Six network topologies are evaluated under extreme Byzantine configurations. | Explicit author claim | Paper | Experimental Setting | 5 | Figure 2; Table 2 | Defense evaluation. |
| The claimed robustness outcome is task accuracy rather than a formal classical agreement theorem. | Interpretation | Paper | Dataset and Metrics; Results | 5-7 | Tables 2-3 | The reported quantities are oracle-scored answer accuracy and reliability accuracy. |

## Provenance

### Discovery Source

AAAI proceedings; Crossref; prior corpus completeness scan.

### Discovery Query

`site:ojs.aaai.org LLM multi-agent Byzantine`

### Accessed Version

Published AAAI version.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05

