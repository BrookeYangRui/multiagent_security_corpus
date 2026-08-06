# Model Context Protocol Threat Modeling and Analysis of Vulnerabilities to Prompt Injection with Tool Poisoning

## Citation

- Authors: Charoes Huang, Xin Huang, Ngoc Phu Tran, Amin Milani Fard
- Year: 2026
- Venue: Journal of Cybersecurity and Privacy
- DOI: 10.3390/jcp6030084
- Primary URL: https://www.mdpi.com/2624-800X/6/3/84
- Open access URL: https://www.mdpi.com/2624-800X/6/3/84/pdf
- BibTeX key: `huang2026mcpthreatmodel`

## Paper Type

Attack; Defense; Evaluation; Threat modeling; Empirical study

## Scope

### System Studied

MCP hosts, clients, LLMs, servers, external stores, and authorization services,
with an empirical focus on client handling of server-provided tool metadata.

### Multi-Agent Dependency

The security consequence crosses a standardized client-server protocol boundary:
untrusted metadata from one endpoint shapes an LLM host's later tool selection.
This is a protocol substrate study and does not require two LLM-backed agent
cores.

### Application Domain

General-purpose AI assistants connected to external services through MCP.

## Security Model

- Protected assets: tool-selection integrity, user authorization, data
  confidentiality, and client transparency.
- Threat actor: a malicious or compromised MCP server or tool publisher.
- Trusted components: the client and host are expected to enforce the boundary
  before metadata reaches the LLM.
- Attacker capabilities: embed instructions or misleading behavior descriptions
  in tool metadata.
- Security assumptions: clients retrieve and expose server metadata when building
  the model context.

## Main Contribution

The paper applies STRIDE and DREAD to the MCP architecture and empirically
compares seven MCP clients under tool-poisoning attacks. It proposes layered
mitigations spanning static validation, model-decision tracing, behavioral
monitoring, and user-facing transparency.

## Attack or Failure

- Attack surface: tool names, descriptions, parameters, and other server-supplied
  metadata incorporated into the model context.
- Attack mechanism: hidden or misleading instructions steer tool choice and
  parameter use.
- System-level failure: client-server contextual integrity and delegated action
  integrity failure.
- Security consequence: the host selects an attacker-influenced tool or performs
  actions the user cannot adequately inspect.

## Defense

- Defense mechanism: static metadata analysis, decision-path tracking, behavioral
  anomaly detection, and improved parameter visibility.
- Intervention point: MCP client ingestion, model decision, and tool invocation.
- Required observability: raw metadata, model-selected tool and parameters, and
  runtime behavior.
- Assumptions: clients can validate metadata before context construction and show
  meaningful details to users.
- Limitations: empirical attacks emphasize two client-side trust boundaries and
  do not implement every proposed mitigation end to end.

## Evaluation

- Evaluated systems: seven major MCP clients.
- Agent configuration: an MCP host/LLM connected to benign and maliciously
  described server tools.
- Dataset or environment: controlled tool-poisoning scenarios and client feature
  analysis.
- Baselines: each client's existing validation and approval behavior.
- Metrics: attack handling, static validation, parameter visibility, and client
  security-feature coverage.
- Main results: most evaluated clients expose material weaknesses due to limited
  metadata validation or inadequate visibility into invocation parameters.

## Relation to Existing Work

- Papers compared by the authors: MCP server vulnerabilities, prompt injection,
  tool poisoning, and agent-security benchmarks.
- Claimed research gap: earlier MCP work emphasizes server-side flaws or the model
  boundary while leaving client behavior underexamined.
- Closest related work: invariant tool-poisoning demonstrations and MCP security
  taxonomies.
- Difference from prior work: the paper combines architecture-wide threat
  modeling with a seven-client empirical comparison.

## Relevance to Our SoK

- Included concepts: MCP protocol, trust boundaries, tool metadata, authority, and
  client-side enforcement.
- Taxonomy implications: tool poisoning is the mechanism; delegated action and
  contextual integrity are the violated properties.
- Supported research questions: where protocol defenses must observe and validate
  inter-component information.
- Important limitations: this is adjacent protocol evidence rather than a study
  of interaction among multiple LLM-backed agents.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The threat model covers six MCP architecture components. | Explicit author claim | Paper | 3 | HTML section 3 | Figure 1; Tables 1-6 | Host, client, LLM, server, stores, and authorization are modeled. |
| The empirical study focuses on client-LLM and client-server boundaries. | Explicit author claim | Paper | 3 | HTML section 3 | Figure 1 | Tool metadata enters model context without independent validation in the attack model. |
| Seven MCP clients are compared under tool poisoning. | Explicit author claim | Paper | 4-6 | HTML sections 4-6 | Evaluation tables | The paper systematically compares validation and visibility behavior. |
| The journal record is volume 6, issue 3, article 84. | Verified metadata | Publisher; Crossref | Article metadata | Not applicable | Not applicable | MDPI and DOI metadata agree on the publication record. |

## Provenance

- Discovery source: journal publisher; Crossref; arXiv; prior systematic corpus
- Discovery query: `MCP Threat Modeling tool poisoning journal DOI`
- Accessed version: published Journal of Cybersecurity and Privacy version
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

