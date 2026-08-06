# Who's the Mole? Modeling and Detecting Intention-Hiding Malicious Agents in LLM-Based Multi-Agent Systems

## Citation

- Authors: Yizhe Xie, Congcong Zhu, Xinyue Zhang, Tianqing Zhu, Dayong Ye, Minghao Wang, Chi Liu
- Year: 2025
- Venue: arXiv preprint
- DOI: 10.48550/arXiv.2507.04724
- Primary URL: https://arxiv.org/abs/2507.04724
- Open access URL: https://arxiv.org/pdf/2507.04724
- BibTeX key: `xie2025whosthemole`

## Paper Type

Attack; Defense; Benchmark; Evaluation; Empirical study

## Scope

### System Studied

Centralized, decentralized, and layered LLM-MAS configurations with role-assigned
agents collaborating on reasoning, coding, and generation tasks.

### Multi-Agent Dependency

A malicious member maintains fluent, role-consistent behavior while subtly
redirecting peer coordination; effectiveness and detection depend on the system's
communication structure.

### Application Domain

Knowledge reasoning, mathematics, code generation, arithmetic, and biography
synthesis.

## Security Model

- Protected assets: task accuracy, completion efficiency, and goal integrity.
- Threat actor: one intention-hiding member agent.
- Trusted components: user task and remaining member roles are benign.
- Attacker capabilities: alter its own protocol-valid messages without overt
  jailbreak strings or access to other agents' internals.
- Security assumptions: peers treat the malicious member as an ordinary
  collaborator and the roster supports centralized, peer, or layered messaging.

## Main Contribution

The paper defines four intention-hiding attacks and evaluates them across three
communication structures and six datasets. It proposes AgentXposed, a detection
framework combining HEXACO-style profiling with progressive questioning and
behavior monitoring.

## Attack or Failure

- Attack surface: role-consistent inter-agent communication and coordination.
- Attack mechanism: suboptimal fixation, reframing misalignment, fake injection,
  or execution delay.
- System-level failure: collective objective and decision integrity degrade
  without obvious local policy violations.
- Security consequence: lower task success or increased completion cost while the
  malicious agent appears cooperative.

## Defense

- Defense mechanism: AgentXposed detection followed by cognitive redirection or
  removal of the flagged agent.
- Intervention point: membership monitoring and post-detection coordination.
- Required observability: agent responses to progressive probes and interaction
  behavior across rounds.
- Assumptions: the defender can question members before harm and remove or
  redirect a detected member.
- Limitations: profiling and interrogation analogies may not transfer to all
  model families, roles, or adaptive adversaries.

## Evaluation

- Evaluated systems: controlled centralized, decentralized, and layered MAS.
- Agent configuration: benign collaborators plus attack agents and two baseline
  threat types.
- Dataset or environment: MMLU, MMLU-Pro, HumanEval, GSM8K, Arithmetic, and
  Biographies.
- Baselines: benign runs, explicit baseline attacks, alternative personality
  models, and standard detection methods.
- Metrics: task accuracy, completion efficiency, detection accuracy, and defense
  recovery.
- Main results: all four attacks degrade at least some tasks across all three
  structures; AgentXposed is reported to outperform alternative profiling and
  detection baselines.

## Relation to Existing Work

- Claimed research gap: existing defenses focus on overt malicious outputs rather
  than agents concealing intent behind role-consistent language.
- Closest related work: faulty-agent robustness, communication attacks, and
  malicious-member detection.
- Difference from prior work: attack stealth and detection are evaluated jointly
  across multiple communication structures.

## Relevance to Our SoK

- Included concepts: malicious membership, covert intent, topology, observer
  scope, progressive probing, redirection, and removal.
- Taxonomy implications: concealed intent is an adversary strategy, whereas
  goal/decision degradation defines the system-level failures.
- Supported research questions: whether topology changes attack effectiveness and
  what observation is required to detect role-consistent malicious members.
- Important limitations: preprint status, synthetic attack prompts, and a bounded
  six-dataset testbed require independent validation.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Four intention-hiding attacks are evaluated. | Explicit author claim | Paper | 4.2 | PDF 4-6 | Not applicable | The method defines fixation, reframing, fake injection, and delay. |
| Evaluation spans three communication structures and six datasets. | Explicit author claim | Paper | 5.1 | PDF 8 | Table 1 | Centralized, decentralized, and layered runs cover the six named datasets. |
| AgentXposed combines personality profiling and progressive probing. | Explicit author claim | Paper | 4.4 | PDF 6-7 | Figures 3-6 | The detector uses HEXACO-inspired profiles and Reid-style questions. |
| The attacks are locally fluent but can violate the collective objective. | Interpretation | Paper | 1; 4.2 | PDF 1-2; 4-6 | Figure 1 | Reframing can preserve role consistency while shifting the group to a different task. |

## Provenance

- Discovery source: arXiv; prior systematic screening corpus
- Discovery query: `Who's the Mole intention-hiding malicious agents publication`
- Accessed version: arXiv v2
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

