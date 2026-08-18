# Evaluation Scope Adjudication

Review date: `2026-08-18`

This audit reviews all 44 works currently labeled `evaluation` in Set 1 and Set 2. The rule is the same substantive-scope rule used for the survey audit: a work remains in the MAS-security corpus only when it substantively evaluates a security property of the multi-agent system itself. Generic reliability, reasoning quality, social behavior, application correctness, or use of MAS as an evaluation tool is contextual rather than MAS-security evidence.

This is an audit-only branch. Canonical frozen corpus files are unchanged.

## Result

- 44 evaluation works reviewed.
- 27 recommended to remain in the MAS-security corpus.
  - Set 1: 14 of 22.
  - Set 2: 13 of 22.
- 17 recommended to move to Set 3.
  - Set 1: 8.
  - Set 2: 9.
- No duplicate identity corrections were identified in this evaluation-only pass.

If applied, the manuscript-facing partition would become:

| Partition | Current | Proposed |
| --- | ---: | ---: |
| Set 1 | 104 | 96 |
| Set 2 | 128 | 119 |
| Set 3 | 441 | 458 |
| Screened out | 1,543 | 1,543 |
| Review universe | 2,216 | 2,216 |
| MAS-security corpus | 232 | 215 |

The proposed contribution distribution would be:

| Contribution | Set 1 | Set 2 | Total |
| --- | ---: | ---: | ---: |
| Attack | 33 | 38 | 71 |
| Defense | 39 | 61 | 100 |
| Evaluation | 14 | 13 | 27 |
| General | 5 | 4 | 9 |
| Survey | 5 | 3 | 8 |
| Total | 96 | 119 | 215 |

## Recommended moves from Set 1

1. `Debate, Deliberate, Decide (D3)` -> `measurement_context`: adversarial debate is an evaluation mechanism for reliability and interpretability, not an attack on the MAS.
2. `Reproducibility Study of Cooperation, Competition, and Maliciousness` -> `measurement_context`: reproduction and negotiation measurement are primary.
3. `Revisiting Multi-Agent Debate as Test-Time Scaling` -> `measurement_context`: studies conditional task effectiveness and test-time scaling rather than security of the MAS.
4. `TCLMA` -> `deployment_evidence`: MAS is used to evaluate scientific novelty.
5. `Autonomous Evaluation Architectures` -> `measurement_context`: generic production-pipeline evaluation and alignment dominate the contribution.
6. `Trustworthy Causal Reasoning in ... Smart Building Systems` -> `deployment_evidence`: evaluates causal reasoning accuracy in an application domain.
7. `Persuade Me if You Can` -> `measurement_context`: measures persuasion capability and susceptibility rather than a concrete MAS security property.
8. `Multi-AI Agent Oriented Privacy Policy Compliance Checking ... Mobile IoT Systems` -> `deployment_evidence`: MAS is the checker; the protected object is the external IoT privacy policy/application.

## Recommended moves from Set 2

1. `Adversarial Consensus Verification ... PAVE Interchange Benchmark` -> `deployment_evidence`: the adversarial verifier is a cooperative evaluation role for financial-forensics correctness, not a threat actor.
2. `Behavioral Drift in Multi-Agent LLM Systems` -> `measurement_context`: longitudinal stability and behavioral decay are the measured properties.
3. `Beyond Individual Agent Monitoring` -> `measurement_context`: relational failure modes are not tied to a concrete security property in the available evidence.
4. `Chain-Centric Multi-Agent Framework` -> `related_work`: generic collaboration architecture and confidence evaluation.
5. `Containing the Cascade` -> `measurement_context`: generic failure-propagation benchmark without a concrete adversarial/security threat in the available evidence.
6. `Multi-Paradigm Agent Interaction in Practice` -> `measurement_context`: analyzes interaction paradigms rather than MAS security.
7. `SycoEval-EM` -> `deployment_evidence`: clinical sycophancy behavior evaluation, not security of the MAS.
8. `Algorithmic Cowardice` -> `measurement_context`: moral conformity and cognitive dissonance are behavioral properties, not concrete security properties.
9. `Is Lying an Emergent Behaviour in LLMs?` -> `measurement_context`: studies emergent lying in a sustainability game without an explicit security threat model.

## Borderline retained works

Four retained works deserve named-author signoff because their security framing is broader than conventional cybersecurity:

- `WOLF`: retained because adversarial deception production/detection is a collective-integrity evaluation.
- `Deception and Communication in Autonomous Multi-Agent Systems`: retained because misaligned deceptive principals are material to the interaction outcome.
- `Infodeme`: retained because misinformation propagation is treated as a collective-integrity failure, but source-level security framing should be rechecked by an author.
- `Security of LLM Agents: A Case Study Approach`: retained because security is the primary subject and the repository source review supports an inter-agent security path, but the externally accessible abstract is limited.

`Cooperation, Competition, and Maliciousness` is also broader than a pure security benchmark, but adversarial/greedy agents and manipulation are substantive parts of its evaluation rather than an incidental challenge section.

See `corpus/adjudication/evaluation_scope_2026-08-18.csv` for all 44 row-level decisions.
