# System Models

Cross-paper synthesis of multi-agent system models, interaction structures,
trust assumptions, and security boundaries.

## Entries

Use BibTeX keys or paper-note paths and label every statement by evidence type.

### System and Property Boundaries

- **Author-claimed gap:** `bellay2025safesystems` argues that a system should be
  able to remain safe without assuming every member agent is safe.
- **Established finding:** `allegrini2025formalizing` models host-agent and
  interaction semantics across MCP and A2A and specifies safety, security, and
  functional properties over their composition.
- **Our interpretation:** A useful MAS model therefore needs explicit shared
  state, capability or authority distribution, system properties, and observer
  scope in addition to agents, graph, and protocol.

### Protocol and Trust Boundaries

- **Established finding:** `anbiaee2026protocols` compares MCP, A2A, Agora, and
  ANP across discovery, identity, session, message, delegation, and lifecycle
  threats.
- **Cross-paper observation:** MCP is primarily an agent-to-tool substrate,
  whereas A2A, Agora, and ANP include peer communication. Protocol inclusion
  must therefore depend on the protected multi-agent system, not the presence of
  a protocol acronym.
- **Established finding:** `hu2025responsibility` frames agreement, uncertainty,
  and security as lifecycle-wide collective properties rather than local
  alignment checks.
- **Open question:** Which trace variables are necessary and sufficient to
  decide collective goal, authorization, confidentiality, and agreement
  properties?
