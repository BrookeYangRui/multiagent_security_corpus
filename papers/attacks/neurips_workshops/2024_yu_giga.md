# Infecting LLM Agents via Generalizable Adversarial Attack

## Citation

- Authors: Weichen Yu, Kai Hu, Tianyu Pang, Chao Du, Min Lin, Matt Fredrikson
- Year: 2024
- Venue: NeurIPS 2024 Workshop on Red Teaming GenAI
- DOI: Not reported
- Primary URL: https://neurips.cc/virtual/2024/106765
- Open access URL: https://openreview.net/pdf?id=udsmFGMwlp
- BibTeX key: `yu2024giga`

## Paper Type

Attack; Evaluation; Empirical study

## Scope

### System Studied

Multi-agent, multi-round LLM systems in which agents repeatedly exchange
messages and retain conversation context while completing a task.

### Multi-Agent Dependency

One seeded adversarial suffix compromises additional agents only when recipients
repeat and transmit it through later messages; population compromise is therefore
defined over an interaction sequence rather than one model invocation.

### Application Domain

General-purpose conversational LLM agents.

## Security Model

- Protected assets: agent instruction integrity and population-wide safety.
- Threat actor: an external adversary that seeds one agent.
- Trusted components: other agents begin uncompromised; system prompts and model
  weights are not described as attacker-controlled.
- Attacker capabilities: optimize a discrete adversarial suffix with model
  gradient access and inject it into an initial agent message.
- Security assumptions: agents exchange text over multiple rounds and retain
  enough peer content for the suffix to be reproduced.

## Main Contribution

The paper introduces Generalizable Infectious Gradient Attack (GIGA), which
optimizes a suffix to reproduce across changing agent contexts. It evaluates both
multi-agent propagation and evasion of a prompt-rewriting safeguard.

## Attack or Failure

- Attack surface: inter-agent text messages and retained conversation memory.
- Attack mechanism: a gradient-optimized suffix induces each exposed agent to
  repeat the suffix, enabling subsequent transmission.
- System-level failure: behavioral contagion across an initially benign agent
  population.
- Security consequence: one injected string can compromise multiple agents and
  bypass an evaluated rewriting defense.

## Defense

- Defense mechanism: the paper evaluates a safeguard model that rewrites prompts
  before an answer model processes them.
- Intervention point: message preprocessing.
- Required observability: the current message presented for rewriting.
- Assumptions: rewriting removes or neutralizes adversarial strings without
  destroying the task request.
- Limitations: the evaluated attack can optimize against the rewriting pipeline;
  the paper does not establish a general defense.

## Evaluation

- Evaluated systems: multi-round agent conversations and a two-model
  safeguard-plus-answer pipeline.
- Agent configuration: multiple agents exposed sequentially through exchanged
  messages; exact configurations vary by experiment.
- Dataset or environment: harmful request sets and conversational contexts
  described in the paper.
- Baselines: existing adversarial suffix methods and unoptimized attacks.
- Metrics: suffix repetition or propagation success, attack success rate, answer
  success, optimization time, and loss.
- Main results: GIGA propagates across varied agent/model contexts; Table 4
  reports 90-100% answer ASR for three safeguard/answer configurations.

## Relation to Existing Work

- Claimed research gap: prior jailbreak attacks did not establish a textual
  suffix that self-propagates through a multi-LLM agent population.
- Closest related work: Agent Smith, The Wolf Within, prompt injection, and
  gradient-based adversarial suffix attacks.
- Difference from prior work: GIGA targets discrete text that generalizes across
  agent personalities, models, and changing conversation memory.

## Relevance to Our SoK

- Included concepts: single-seed infection, multi-round propagation, shared
  context, message-only intervention, and adaptive defense evasion.
- Taxonomy implications: the mechanism is adversarial-suffix optimization; the
  system-level failure is propagation and containment failure.
- Supported research questions: what conditions make an adversarial input
  reproducible across agents, and whether local rewriting prevents contagion.
- Important limitations: initialization instability requires reruns; evaluation
  covers a limited defense and does not provide a standardized population-level
  infection contract.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The setting seeds one agent and studies compromise of the population through later messages. | Explicit author claim | Paper | Abstract; 1 | PDF 1-2 | Not applicable | The authors define multi-agent, multi-round transmission as the attack setting. |
| GIGA searches for a suffix that agents repeat despite changing memory context. | Explicit author claim | Paper | Abstract; method | PDF 1 onward | Not applicable | Generalization across contexts is the stated condition for self-propagation. |
| The evaluation includes propagation and bypass of prompt rewriting. | Explicit author claim | Paper | Abstract; experiments | PDF 1; 5-8 | Tables 1-4 | These are the two evaluation objectives stated by the authors. |
| Three safeguard/answer configurations retain 90-100% answer ASR. | Explicit author claim | Paper | Experiments | PDF 8 | Table 4 | Table 4 reports answer ASR of 100%, 96%, and 90%. |
| Optimization is initialization-sensitive. | Explicit author claim | Paper | 6, Limitations | PDF 9 | Not applicable | The authors state that some starting points require rerunning the attack. |

## Provenance

- Discovery source: NeurIPS official workshop program; prior systematic corpus
- Discovery query: `site:neurips.cc GIGA infecting LLM agents workshop`
- Accessed version: NeurIPS 2024 workshop paper from OpenReview
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

