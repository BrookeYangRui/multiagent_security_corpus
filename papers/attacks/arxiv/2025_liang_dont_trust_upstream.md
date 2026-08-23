# Don't Trust Your Upstream: Exploiting LLM Multi-Agent System via Topology-Guided Adversarial Propagation

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set2_emerging` · `attack` · venue `arXiv` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

- Authors: Ruichao Liang, Le Yin, Jing Chen, Yebo Feng, Cong Wu, Xiaoyu Zhang, Huangpeng Gu, Zijian Zhang, Yang Liu
- Year: 2025
- Venue: arXiv preprint
- DOI: 10.48550/arXiv.2512.04129
- Primary URL: https://arxiv.org/abs/2512.04129
- Open access URL: https://arxiv.org/pdf/2512.04129
- BibTeX key: `liang2025donttrustupstream`

## Paper Type

Attack; Defense; Benchmark; Evaluation; Empirical study

## Scope

### System Studied

Tool-using MAS deployed as tree, chain, star, ring, or mesh topologies in
Magentic-One, LangManus, and OWL, plus two end-to-end applications.

### Multi-Agent Dependency

The attacker starts at an externally exposed edge agent, reconstructs the hidden
communication graph, and plans a multi-hop path to a privileged internal agent.

### Application Domain

Web understanding, repository analysis, deep research, and trading workflows.

## Security Model

- Protected assets: privileged tool execution, filesystem integrity, and system
  output integrity.
- Threat actor: a black-box external adversary controlling content seen by an
  edge agent.
- Trusted components: the internal roster and framework are not directly
  compromised.
- Attacker capabilities: query the system, infer roles and edges, contaminate an
  edge observation, and adapt payloads using observed outcomes.
- Security assumptions: upstream outputs are reinterpreted downstream and at
  least one path reaches a higher-privilege agent.

## Main Contribution

The paper proposes TOMA, a four-stage topology-aware multi-hop attack combining
graph reconnaissance, contamination modeling, path selection, and hierarchical
payload optimization. It also evaluates T-Guard, a topology-trust mitigation.

## Attack or Failure

- Attack surface: exposed tools, hidden communication edges, delegated tasks,
  and downstream trust.
- Attack mechanism: infer topology, select an entry-to-target path, and adapt
  payloads that survive relay to a privileged agent.
- System-level failure: propagation containment and compositional authority fail.
- Security consequence: irrelevant or destructive actions, including privileged
  filesystem or command operations.

## Defense

- Defense mechanism: T-Guard combines edge-environment validation with a
  topology trust evaluator and dynamic permissions.
- Intervention point: edge content, communication edges, and access control.
- Required observability: topology, trust signals, and downstream action context.
- Assumptions: a trusted enforcement component can reduce permissions or block
  suspicious paths.
- Limitations: the defense is presented as a concept and evaluated in the same
  benchmark family as the attack.

## Evaluation

- Evaluated systems: Magentic-One, LangManus, OWL, GPT-Researcher, and a trading
  agent application.
- Agent configuration: three frameworks, five topologies, three model families,
  two workloads, and two attack objectives.
- Dataset or environment: browser and filesystem MCP tasks plus 20 application
  scenarios.
- Baselines: topology-unaware flooding, shortest-path variants, and attack-stage
  ablations.
- Metrics: topology-reconstruction F1, ASR, infection-integrity score,
  generalization consistency, blocking rate, latency, and resource overhead.
- Main results: benchmark ASR ranges from 40% to 78%; the real applications are
  compromised in 17 of 20 scenarios; T-Guard blocks 94.8% on average.

## Relation to Existing Work

- Claimed research gap: earlier MAS attacks either cause narrow effects or assume
  intrusive control of internal agents and channels.
- Closest related work: communication attacks, prompt infection, topology safety,
  and tool-output injection.
- Difference from prior work: black-box reconnaissance and path planning are
  integrated with high-impact multi-hop payload propagation.

## Relevance to Our SoK

- Included concepts: topology confidentiality, edge exposure, privilege
  distribution, path planning, tool boundaries, and dynamic permissioning.
- Taxonomy implications: topology inference and payload relay are mechanisms;
  privileged unauthorized action is the impact-bearing failure.
- Supported research questions: how graph structure shapes attack reachability
  and where graph-aware defenses should intervene.
- Important limitations: preprint status, locally instantiated frameworks, and
  attack-selected scenarios may overstate deployment generality.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| TOMA combines reconnaissance, propagation modeling, path selection, and payload optimization. | Explicit author claim | Paper | V | PDF 5-10 | Figure 3 | The framework is presented as four attack phases. |
| Evaluation factorizes three frameworks, five topologies, three models, two workloads, and two objectives. | Explicit author claim | Paper | VII-D | PDF 12-14 | Table III | The benchmark matrix enumerates these factors. |
| TOMA succeeds in 17 of 20 application scenarios. | Explicit author claim | Paper | VII-E | PDF 15 | Table VII | The two locally deployed applications each contribute ten scenarios. |
| T-Guard reports 94.8% average blocking. | Explicit author claim | Paper | VII-F | PDF 15-16 | Tables VIII-X | The defense evaluation reports blocking and overhead. |

## Provenance

- Discovery source: arXiv; prior systematic screening corpus
- Discovery query: `Don't Trust Your Upstream topology guided adversarial propagation publication`
- Accessed version: arXiv v2
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05
