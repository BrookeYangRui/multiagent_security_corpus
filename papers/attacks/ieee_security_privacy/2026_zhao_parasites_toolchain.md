# Parasites in the Toolchain: A Large-Scale Analysis of Attacks on the MCP Ecosystem

## Citation

- Authors: Shuli Zhao, Qinsheng Hou, Zihan Zhan, Yanhao Wang, Yuchong Xie, Yu Guo, Libo Chen, Shenghong Li, Zhi Xue
- Year: 2026
- Venue: IEEE Symposium on Security and Privacy
- DOI: Not reported
- Primary URL: https://arxiv.org/abs/2509.06572
- Open access URL: https://arxiv.org/pdf/2509.06572
- BibTeX key: `zhao2026parasites`

## Paper Type

Attack; Defense; Evaluation; Empirical study

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

