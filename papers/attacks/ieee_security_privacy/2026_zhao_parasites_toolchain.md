# Parasites in the Toolchain: A Large-Scale Analysis of Attacks on the MCP Ecosystem

> **Source-review correction:** The Source Review section at the end supersedes inconsistent automated coding in this note. It still requires author signoff.

## Citation

- Authors: Shuli Zhao, Qinsheng Hou, Zihan Zhan, Yanhao Wang, Yuchong Xie, Yu Guo, Libo Chen, Shenghong Li, Zhi Xue
- Year: 2026
- Venue: IEEE Symposium on Security and Privacy
- DOI: 10.1109/SP63933.2026.00154
- Primary URL: https://doi.org/10.1109/SP63933.2026.00154
- Open access URL: https://arxiv.org/pdf/2509.06572
- BibTeX key: `zhao2026parasites`
- Pages: 138-155

## Paper Type

Attack; Measurement; Ecosystem evaluation

- Primary category: `attack`
- Scope relation: `security_relevant`

## Scope

### System Studied

LLM hosts that orchestrate multiple Model Context Protocol clients, servers, and
tools during autonomous task execution.

### Multi-Agent Dependency

The attack composes individually legitimate services into a cross-tool execution
chain for private-data collection and exfiltration. This is a protocol/toolchain
composition boundary; it does not require every MCP endpoint to contain its own
LLM agent core.

### Application Domain

General-purpose MCP hosts, local data tools, external content services, and
network-capable tools.

## Security Model

- Protected assets: private host data, tool authority, and execution integrity.
- Threat actor: an external adversary able to plant content in a data source that
  a victim workflow may later retrieve.
- Trusted components: the victim's installed MCP servers and tools may each be
  benign in isolation.
- Attacker capabilities: publish an indirect prompt; no direct victim interaction
  or malicious installed server is required.
- Security assumptions: the host lets retrieved instructions influence later
  privileged tool calls and does not enforce least privilege across the chain.

## Main Contribution

The paper formalizes Parasitic Toolchain Attacks and instantiates MCP Unintended
Privacy Disclosure (MCP-UPD). It also introduces MCP-SEC and uses it for a
large-scale census of public MCP servers and tools.

## Attack or Failure

- Attack surface: external content ingested through MCP and subsequently shared
  with privileged tool orchestration.
- Attack mechanism: parasitic ingestion, privacy collection, and privacy
  disclosure across a composed toolchain.
- System-level failure: cross-tool contextual integrity, least privilege, and
  confidentiality failure.
- Security consequence: legitimate tools combine to read private data and send it
  to an attacker-controlled endpoint.

## Defense

- Defense mechanism: context-tool isolation, least-privilege controls, and
  sequence-aware monitoring are discussed.
- Intervention point: tool authorization and cross-tool execution flow.
- Required observability: content provenance, requested permissions, and the full
  ordered tool chain.
- Assumptions: the host can enforce capabilities and distinguish untrusted data
  from executable instructions.
- Limitations: the census identifies capability gadgets; their presence is not
  identical to successful exploitation in every deployment.

## Evaluation

- Evaluated systems: 1,360 public MCP servers containing 12,230 tools, plus
  end-to-end toolchain demonstrations across multiple LLMs.
- Agent configuration: one LLM host orchestrating multiple MCP clients and tools.
- Dataset or environment: public MCP registries and constructed exploit chains.
- Baselines: component-level security analysis and traditional prompt-injection
  framing.
- Metrics: prevalence of exploitable capability gadgets and end-to-end attack
  success.
- Main results: MCP-SEC identifies 1,062 tools and 370 servers with capabilities
  relevant to the modeled attacks.

## Relation to Existing Work

- Papers compared by the authors: indirect prompt injection, tool poisoning, MCP
  scanning, and supply-chain security.
- Claimed research gap: component-wise analysis misses malicious behavior that
  emerges only from a legitimate cross-server tool composition.
- Closest related work: prompt injection in tool-integrated agents and MCP tool
  poisoning.
- Difference from prior work: the adversary can use benign installed services and
  an external-data prompt rather than deploying a malicious MCP server.

## Relevance to Our SoK

- Included concepts: MCP, distributed capabilities, tool composition, provenance,
  and execution-aware information flow.
- Taxonomy implications: the mechanism is indirect prompt injection; the violated
  properties are compositional authority and confidentiality.
- Supported research questions: which global toolchain facts must be visible to
  enforce least privilege.
- Important limitations: this paper represents the protocol/toolchain edge of the
  corpus rather than a population of multiple LLM-backed cores.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| MCP-UPD composes benign tools into a three-stage exfiltration chain. | Explicit author claim | Paper | 2-3 | PDF 2 onward | Attack workflow | The stages are parasitic ingestion, privacy collection, and disclosure. |
| The census covers 12,230 tools across 1,360 servers. | Explicit author claim | Paper | Abstract; census | PDF 1 onward | Census tables | These are the stated MCP-SEC corpus sizes. |
| The analysis identifies 1,062 relevant tools and 370 relevant servers. | Explicit author claim | Paper | Results | PDF results section | Census tables | The paper reports 8.7% of tools and 27.2% of servers. |
| The paper was accepted by IEEE S&P 2026. | Verified metadata | Paper; arXiv | Header; version comment | PDF 1 | Meta-review appendix | The paper includes the S&P meta-review and arXiv records the acceptance. |

## Provenance

- Discovery source: IEEE S&P paper metadata; arXiv; prior systematic corpus
- Discovery query: `Parasites in the Toolchain IEEE Security Privacy 2026`
- Accessed version: IEEE S&P 2026 accepted paper, arXiv v5 full text
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

<!-- SOURCE_REVIEW_START -->
## Source Review

**Status:** `source_reviewed_pending_author_signoff`

**Outcome:** Ready after major patch

**Review source:** `reviews/load_bearing/load_bearing_source_review.csv`

This section supersedes inconsistent automated coding elsewhere in this note.
It is a source-level review, not human verification. Manuscript-facing claims
still require author or designated-reviewer signoff.

### Identity and Scope

- Identity: Accepted and published at IEEE S&P 2026. Replace the arXiv-only venue record with final IEEE proceedings metadata while keeping the accepted arXiv version linked.
- Recommended scope: `security_relevant`
- Multi-agent dependency: The system is one LLM host composing multiple MCP servers and tools. It is directly relevant to distributed capability composition but does not necessarily contain multiple independently stateful LLM agent cores.
- Recommended roles: attack; measurement; ecosystem evaluation
- Maturity: Archival peer-reviewed systems-security evidence, adjacent to strict LLM-MAS scope.

### Threat and Failure Coding

- Attacker or fault actor: External adversary who plants content in a source later retrieved by a victim workflow.
- Capabilities: Publishes indirect prompts and relies on installed benign tools to ingest content, collect private data, and disclose it.
- Preconditions: The host lets untrusted retrieved instructions influence later privileged calls and does not enforce least privilege across the tool chain.
- Surfaces: External content; MCP servers and tools; cross-tool execution flow; host authorization.
- Mechanism: Parasitic ingestion, private-data collection, and disclosure through composition of legitimate tools.
- Primary system-level failure: F6 least-privilege and authority integrity failure.
- Impact: F2 confidentiality loss through exfiltration.

### Evaluation Contract

- Configuration: 1,360 public MCP servers containing 12,230 tools, plus end-to-end demonstrations across selected LLM hosts.
- Topology: Host-tool and server composition graph rather than a multi-agent population graph.
- Baseline or ablation: Component-level security analysis, traditional prompt-injection framing, and end-to-end attack variants.
- Metric: Capability-gadget prevalence and separately measured end-to-end attack success.
- Unit: Tool, server, or end-to-end exploit chain.
- Denominator: 12,230 tools and 1,360 servers for the census; separate trial denominators for demonstrations.
- Result boundary: The census identifies 1,062 tools and 370 servers with capabilities relevant to the modeled attack. This is not the same as successful exploitation of all those tools or servers.

### Evidence and Boundaries

- Evidence locations: Abstract and attack workflow, PDF p. 1 onward; attack stages in Secs. 2 to 3; census methods and tables; result tables for 1,062 tools and 370 servers; final IEEE metadata record.
- Author claim versus corpus interpretation: Tool and server census and demonstrated attack chains are author claims. Scope downgrade and F6/F2 mapping are corpus interpretations.
- Limitations: Host-tool rather than strict multi-agent boundary; public registry sampling; inaccessible servers and token barriers; LLM-assisted classification plus manual checks; capability presence is not exploit prevalence.

### Required Corrections

- **CRITICAL - Publication metadata:** Record final IEEE S&P venue, DOI, and page range; retain arXiv as linked version.
- **CRITICAL - Scope relation:** Downgrade from core_security to security_relevant under the independent-agent-core definition.
- **HIGH - Result interpretation:** Separate capability-gadget prevalence from successful exploitation.
<!-- SOURCE_REVIEW_END -->
