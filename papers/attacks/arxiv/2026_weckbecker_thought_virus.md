# Thought Virus: Viral Misalignment via Subliminal Prompting in Multi-Agent Systems

## Citation

- Authors: Moritz Weckbecker, Jonas Müller, Ben Hagag, Michael Mulet
- Year: 2026
- Venue: arXiv preprint
- DOI: 10.48550/arXiv.2603.00131
- Primary URL: https://arxiv.org/abs/2603.00131
- Open access URL: https://arxiv.org/pdf/2603.00131
- BibTeX key: `weckbecker2026thoughtvirus`

## Paper Type

Attack; Evaluation; Empirical study

## Scope

### System Studied

Six-agent conversational systems arranged as a forward chain or bidirectional
chain, with one initially biased member.

### Multi-Agent Dependency

A semantically unrelated token preference introduced in one agent changes later
agents through ordinary paraphrased conversation, including after the seeded
agent no longer participates.

### Application Domain

General conversational agents and truthfulness evaluation.

## Security Model

- Protected assets: collective truthfulness and behavioral alignment.
- Threat actor: an operator or prompt attacker able to modify one agent's system
  prompt.
- Trusted components: downstream agents begin without the subliminal preference.
- Attacker capabilities: seed a three-digit token preference in one member; no
  model-weight access or verbatim suffix forwarding is required.
- Security assumptions: agents relay semantic summaries or responses through the
  chosen topology.

## Main Contribution

The paper shows that subliminal prompting can transfer through ordinary
inter-agent conversation and persist across multiple hops. It evaluates both
concept preference and downstream TruthfulQA degradation.

## Attack or Failure

- Attack surface: system prompt of one member and semantic inter-agent messages.
- Attack mechanism: a subliminal token induces a latent concept preference that
  survives paraphrasing and is acquired by downstream agents.
- System-level failure: covert propagation of bias and collective truthfulness
  degradation.
- Security consequence: later agents favor the targeted concept or answer
  TruthfulQA less accurately without an overt malicious string.

## Defense

- Defense mechanism: no complete defense is proposed; the paper contrasts the
  attack with exact-string and semantic-content monitoring.
- Intervention point: potential defenses would require behavior or provenance
  monitoring across messages.
- Required observability: multi-hop response distributions rather than only
  explicit content.
- Assumptions: ordinary content monitors do not flag semantically unrelated
  preference signals.
- Limitations: the effect weakens over hops and is evaluated on two small open
  models, two chain topologies, and controlled token concepts.

## Evaluation

- Evaluated systems: Qwen2.5-7B-Instruct and Llama-3.1-8B-Instruct.
- Agent configuration: six agents in chain and bidirectional-chain settings;
  TruthfulQA uses a three-agent chain.
- Dataset or environment: ten animal-concept preferences and multiple-choice
  TruthfulQA.
- Baselines: random tokens, neutral prompting, and non-conversational preference
  baselines.
- Metrics: target response rate, target log probability, fold increase, and
  TruthfulQA accuracy/log probability.
- Main results: target preferences remain elevated through the six-agent network;
  selected deceitful tokens significantly reduce downstream TruthfulQA results.

## Relation to Existing Work

- Claimed research gap: subliminal learning had not been tested as a multi-agent
  prompt-to-prompt propagation mechanism.
- Closest related work: Agent Smith, GIGA, prompt infection, and subliminal
  learning through training data.
- Difference from prior work: the signal need not be reproduced verbatim or state
  its harmful semantic objective.

## Relevance to Our SoK

- Included concepts: covert seed, semantic propagation, topology, multi-hop
  persistence, observer blind spot, and truthfulness impact.
- Taxonomy implications: subliminal preference transfer is a propagation
  mechanism; collective truthfulness loss is the violated property.
- Supported research questions: which monitoring contracts can detect bias that
  is neither exact-string nor semantically explicit.
- Important limitations: preprint status, small model/topology set, controlled
  concepts, and decaying effects limit prevalence claims.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Bias is measured across six agents and two topologies. | Explicit author claim | Paper | Abstract; 3 | PDF 1; 5 | Figure 3 | The study uses chain and bidirectional-chain communication. |
| The effect persists after the initially biased agent leaves the conversation. | Explicit author claim | Paper | 3 | PDF 4-5 | Figure 2 | Downstream agents become intermediate hosts for the preference. |
| Evaluation uses Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct, and TruthfulQA. | Explicit author claim | Paper | 4 | PDF 5-8 | Tables 1-2 | The experiments report concept and truthfulness outcomes. |
| The attack's covert character challenges content-only monitors. | Interpretation | Paper | 1; 5 | PDF 1-3; 8-9 | Figure 1 | Messages need not repeat a fixed suffix or mention the target behavior explicitly. |

## Provenance

- Discovery source: arXiv; prior propagation audit
- Discovery query: `Thought Virus viral misalignment multi-agent publication`
- Accessed version: arXiv v1
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05
