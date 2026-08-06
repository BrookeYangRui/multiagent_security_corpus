# RiskLab: A Controlled Toolkit for Probing Emergent Risks in LLM-Based Multi-Agent Systems

## Citation

Title: RiskLab: A Controlled Toolkit for Probing Emergent Risks in LLM-Based Multi-Agent Systems

Authors: Yu Jiang; Wenjie Wang; Yue Huang; Yanbo Wang; Zhenhong Zhou; Xiuying Chen; Yang Liu; Pin-Yu Chen; Wei Wang; Xiangliang Zhang

Year: 2026

Venue: ACL System Demonstrations

DOI: 10.18653/v1/2026.acl-demo.17

Primary URL: https://aclanthology.org/2026.acl-demo.17/

Open access URL: https://aclanthology.org/2026.acl-demo.17.pdf

BibTeX key: jiang2026risklab

## Paper Type

Benchmark; Evaluation; System demonstration; Empirical study

## Scope

### System Studied

Configurable LLM multi-agent experiments represented by a topology-environment-protocol-agent-task quintuple.

### Multi-Agent Dependency

The toolkit targets failures caused by communication, incentives, topology, and coordination rather than isolated model errors.

### Application Domain

Controlled studies of general-purpose MAS behavior.

## Security Model

### Protected Assets

Collective task integrity, truthful reporting, bounded resource use, and stable semantics.

### Threat Actor

Malicious, self-interested, or faulty agents and adverse interaction conditions.

### Trusted Components

Experiment controller, trace recorder, scenario oracle, and metric implementation.

### Attacker Capabilities

Configured through roles, incentives, protocols, and environment conditions.

### Security Assumptions

Experiments operate within the toolkit's controlled scenarios.

## Main Contribution

RiskLab is an open-source toolkit for reproducibly varying topology, environment, protocol, agents, and tasks. It includes probes for collusion, resource overreach, semantic drift, and strategic misreporting with trajectory-grounded metrics.

## Attack or Failure

### Attack Surface

Communication graph, protocol, incentives, and task environment.

### Attack Mechanism

Scenario modules induce or expose interaction-dependent risky behavior.

### System-Level Failure

Collusion, drift, overuse, or strategic misreporting at collective level.

### Security Consequence

Loss of collective integrity, reliability, or resource control.

## Defense

### Defense Mechanism

Not a single defense; the toolkit supports controlled evaluation of interventions.

### Intervention Point

Topology, protocol, agent, and environment configuration.

### Required Observability

Global trajectories and configuration metadata.

### Assumptions

Risk metrics depend on known scenario structure or oracle information.

### Limitations

Demonstrated probes are controlled abstractions rather than prevalence estimates for production systems.

## Evaluation

### Evaluated Systems

LLM agents instantiated through the toolkit's supported modules.

### Agent Configuration

User-defined topology and coordination protocol.

### Dataset or Environment

Controlled scenario suites for four emergent risk families.

### Baselines

Clean configurations and alternative structural settings.

### Metrics

Trajectory-grounded, risk-specific measures and task outcomes.

### Main Results

The demonstration shows that structural factors can be varied independently and logged for reproducible risk analysis.

## Relation to Existing Work

### Papers Compared by the Authors

General MAS frameworks and studies of contagion, collusion, drift, and authority effects.

### Claimed Research Gap

Existing frameworks hide interaction graphs or prioritize task completion over controlled risk analysis.

### Closest Related Work

MAS simulation and security evaluation toolkits.

### Difference From Prior Work

RiskLab makes the five-part experiment definition and global trajectory explicit.

## Relevance to Our SoK

### Included Concepts

Topology, protocol, incentive, global trace, and observer scope.

### Taxonomy Implications

Supports separating system design variables from failure outcomes.

### Supported Research Questions

Which structural conditions produce or amplify an emergent risk?

### Important Limitations

The toolkit is extensible, so coverage depends on implemented scenarios and metrics.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Experiments use a topology-environment-protocol-agent-task quintuple. | Explicit author claim | Paper | Abstract; 2 | 1; 2 | Figure 1 | Core experiment model. |
| RiskLab includes collusion, resource overreach, semantic drift, and strategic misreporting probes. | Explicit author claim | Paper | Abstract; 3 | 1; 3-5 | - | Included risk modules. |
| The toolkit records trajectories for system-level analysis. | Explicit author claim | Paper | 2; 4 | 2; 5 | - | Observability and logging design. |

## Provenance

### Discovery Source

ACL Anthology; formal venue scan.

### Discovery Query

ACL 2026 system demo multi-agent risk toolkit

### Accessed Version

Published ACL 2026 system demonstration version.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05
