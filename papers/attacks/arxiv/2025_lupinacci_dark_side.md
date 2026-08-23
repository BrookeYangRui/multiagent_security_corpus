# The Dark Side of LLMs: Agent-based Attack Vectors for System-level Compromise

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set2_emerging` · `attack` · venue `arXiv` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

- Authors: Matteo Lupinacci, Francesco Aurelio Pironti, Francesco Blefari, Francesco Romeo, Luigi Arena, Angelo Furfaro
- Year: 2025
- Venue: arXiv
- DOI: 10.48550/arXiv.2507.06850
- Primary URL: https://arxiv.org/abs/2507.06850
- Open access URL: https://arxiv.org/pdf/2507.06850
- BibTeX key: `lupinacci2025darkside`

## Paper Type

Attack; Evaluation; Empirical study

## Scope

### System Studied

Tool-capable LLM agents exposed through direct prompts, poisoned retrieval, or
requests from peer agents across an inter-agent trust boundary.

### Multi-Agent Dependency

The MAS-specific attack succeeds when a victim treats a peer agent as more
trusted than an equivalent user or retrieved instruction. The security failure
depends on who sends the same payload, not only on payload content.

### Application Domain

Autonomous computer-use agents and system administration.

## Security Model

- Protected assets: host integrity, execution authority, and trust-boundary
  enforcement.
- Threat actor: an external user, a retrieval-data attacker, or a malicious peer
  agent.
- Trusted components: the host exposes tools to the victim agent and relies on
  model refusal behavior.
- Attacker capabilities: submit instructions directly, poison RAG context, or
  send a request through another agent.
- Security assumptions: the victim can install or execute software when it accepts
  a request.

## Main Contribution

The paper compares three paths from natural-language influence to host-level
compromise: direct prompt injection, RAG backdoors, and Inter-Agent Trust
Exploitation. It tests whether peer-agent requests bypass refusals observed at
other trust boundaries.

## Attack or Failure

- Attack surface: natural-language instructions crossing user, RAG, and peer-agent
  trust boundaries.
- Attack mechanism: an adversarial peer relays a malware-installation request to a
  tool-capable victim.
- System-level failure: cross-agent authorization and action-integrity failure.
- Security consequence: the victim executes system-compromise steps that it may
  refuse when the same request comes directly from a user.

## Defense

- Defense mechanism: no complete MAS-specific defense is established.
- Intervention point: request provenance, authorization, and tool execution.
- Required observability: sender identity, request lineage, and resulting host
  actions.
- Assumptions: provenance can distinguish peer requests from authorized operator
  instructions.
- Limitations: the experiment evaluates a controlled execution setup and does not
  estimate prevalence in deployed agent ecosystems.

## Evaluation

- Evaluated systems: 18 LLMs used as reasoning engines for tool-capable agents.
- Agent configuration: attacker-to-victim peer interaction plus direct and RAG
  comparison conditions.
- Dataset or environment: controlled system-compromise tasks and injected
  requests.
- Baselines: direct prompt injection and RAG backdoor attack.
- Metrics: fraction of tested models that execute the requested compromise.
- Main results: the paper reports 100% compromise in the inter-agent condition,
  compared with 94.4% for direct injection and 83.3% for RAG backdoors.

## Relation to Existing Work

- Papers compared by the authors: prompt injection, RAG poisoning, and agent tool
  attacks.
- Claimed research gap: model safety changes across request provenance and agent
  trust boundaries.
- Closest related work: indirect prompt injection and cross-agent communication
  attacks.
- Difference from prior work: the same harmful objective is evaluated across
  direct, retrieved, and peer-agent origins.

## Relevance to Our SoK

- Included concepts: malicious peer, provenance, tool authority, and confused
  deputy behavior.
- Taxonomy implications: the mechanism is peer influence; the system property
  violated is compositional authorization.
- Supported research questions: whether local refusal behavior composes across
  sender identities and delegated trust.
- Important limitations: the inter-agent result measures the paper's controlled
  tasks and models and is not a general guarantee of universal compromise.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The paper compares direct, RAG, and inter-agent attack boundaries. | Explicit author claim | Paper | Abstract; threat surfaces | PDF 1; 5-6 | Not applicable | The three access paths are evaluated as distinct attack conditions. |
| A peer request compromises models that resist other request origins. | Explicit author claim | Paper | Inter-Agent Trust Exploitation | PDF 5-6 | Not applicable | The authors attribute the difference to context-dependent trust behavior. |
| The inter-agent condition compromises all tested models. | Explicit author claim | Paper | Evaluation | PDF 5-6 | Not applicable | The paper reports 100.0% for Inter-Agent Trust Exploitation. |
| The current record is arXiv v6. | Verified metadata | arXiv API | Version record | Not applicable | Not applicable | arXiv reports v6 updated 2026-05-09. |

## Provenance

- Discovery source: arXiv; Semantic Scholar; prior systematic full-text screening
- Discovery query: `The Dark Side LLM inter-agent trust exploitation publication`
- Accessed version: arXiv v6
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05
