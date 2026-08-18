# General Contribution Adjudication

Review date: 2026-08-18

Scope: all 109 rows currently labeled `general` in Set 1 and Set 2.

This is an adjudication ledger, not a direct rewrite of the generated canonical corpus files. Each row was reviewed for two separate questions:

1. Does the work still pass the shared MAS security scope gate?
2. If it stays in Set 1 or Set 2, what is its dominant contribution?

## Decision rule

A paper should not remain `general` merely because a coarse classifier failed to match an attack, defense, evaluation, or survey keyword. The dominant contribution is assigned from the actual security question and mechanism.

A work moves to Set 3 when multi agent interaction is relevant context but the paper's protected property is primarily task quality, reasoning reliability, efficiency, fairness, application correctness, or another adjacent concern rather than MAS security.

A work is screened out when it should not support the frozen corpus at all, including a withdrawn source or a work for which no pre cutoff public version was established.

## Result

Of the 109 rows currently labeled `general`:

* 62 stay in Set 1 or Set 2.
* 44 move to Set 3 as contextual evidence.
* 3 move to screened out.
* Only 9 remain genuinely `general`.
* The other 53 retained rows are better classified as attack, defense, or evaluation.

The nine retained `general` works are:

* `system_protocol_design`: Cut the Crap: An Economical Communication Pipeline for LLM-based Multi-Agent Systems (Set 1)
* `system_protocol_design`: G-Designer: Architecting Multi-agent Communication Topologies via Graph Neural Networks (Set 1)
* `system_protocol_design`: Free-MAD: Consensus-Free Multi-Agent Debate (Set 1)
* `system_protocol_design`: DAWN: Distributed LLM Multi-Agent Workflow Synthesis (Set 1)
* `system_protocol_design`: MPAS: Breaking Sequential Constraints of Multi-Agent Communication Topologies via Individual-Epistemic Message Propagation (Set 1)
* `formal_security_analysis`: Convergence Dynamics of Agent-to-Agent Interactions with Misaligned Objectives (Set 2)
* `formal_security_analysis`: Formalizing the Safety, Security, and Functional Properties of Agentic AI Systems (Set 2)
* `system_protocol_design`: Distributed General-Purpose Agent Networks (Set 2)
* `security_characterization`: Multi-Agent Orchestration: Coordination, Trust, and Cascading Failures (Set 2)

The retained `general` subtype vocabulary can therefore be reduced to:

* `system_protocol_design`
* `formal_security_analysis`
* `security_characterization`

`trust_governance` is not needed as a residual primary contribution in this adjudication. Papers that introduce concrete governance controls are better classified as defenses; broader ethics, alignment, fairness, and governance papers belong in Set 3 unless they establish a concrete MAS security property.

## Proposed corpus impact

If every adjudication in the ledger is applied:

| Set | Current | Proposed |
| --- | ---: | ---: |
| Set 1 | 121 | 108 |
| Set 2 | 166 | 132 |
| Set 3 | 390 | 434 |
| Screened out | 1540 | 1543 |
| Search universe | 2217 | 2217 |

Proposed Set 1 contribution counts:

| Contribution | Count |
| --- | ---: |
| attack | 33 |
| defense | 39 |
| evaluation | 22 |
| general | 5 |
| survey | 9 |

Proposed Set 2 contribution counts:

| Contribution | Count |
| --- | ---: |
| attack | 38 |
| defense | 61 |
| evaluation | 22 |
| general | 4 |
| survey | 7 |

The resulting MAS security corpus would contain 240 works rather than 287. This reduction is primarily caused by removing generic MAS reliability, reasoning, application, and governance papers that were previously admitted by an over broad `general` bucket.

## Important corrections found during review

Examples of incorrect primary contribution labels include:

* `BlockAgents` to defense
* `CAPRI-DP` to defense
* `Cascading Instruction Influence` to attack
* `RAG-Induced Failures in Multi-Agent Large Language Model Debate` to attack
* `The Achilles Heel of Distributed Multi-Agent Systems` to evaluation
* `EncGPT` to defense
* `Accountable Multi-Agent AI Systems` to defense

Examples that should be contextual rather than corpus evidence include Agent-to-Agent Theory of Mind, Agentic Graph-RAG, EmoDebt, several generic multi agent debate optimization papers, medical and financial applications, and alignment or fairness studies without a concrete MAS security property.

Three exclusions require special attention:

* `A Graph-Theoretic Agreement Framework for Multi-Agent LLM Systems`: source marked withdrawn.
* `LightWDN-Agent`: primary record found after the 2026-07-01 literature cutoff with no pre cutoff public version established in this review.
* `Failure Modes in Production Multi-Agent LLM Systems`: SSRN posting is 2026-07-07, after the cutoff, with no pre cutoff public version established in this review.

## Integration recommendation

Do not manually edit `set1_core.csv` or `set2_emerging.csv`. They are generated outputs. Apply approved decisions through the review ledger or an explicit adjudication override file, rebuild the three sets, then rerun corpus validation and manuscript count checks.
