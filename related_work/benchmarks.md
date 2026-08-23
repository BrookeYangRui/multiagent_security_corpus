# Benchmarks and Evaluations

This synthesis is anchored to the final signed **201 work** manuscript corpus. The active corpus contains **44 evaluation primary works**, all indexed in `papers/index.csv` and materialized under `papers/evaluations/`.

## Evaluation landscape

The final evaluation set spans attack benchmarks, security auditing frameworks, privacy measurements, topology studies, collusion and deception evaluations, and system level robustness studies. The complete list and publication venue placement are maintained in `papers/evaluations/README.md`.

Representative benchmark oriented works include TAMAS, ACIARena, A2ASecBench, AgentLeak, MAGPIE, PEAR, GAMBIT, GAMMAF, HARP, CalBench, Colosseum, and MAC Bench.

## Measurement contracts

Evaluation units differ substantially across the corpus. Depending on the work, the denominator may be a task, attack instance, agent, message, sensitive item, trace, graph, game, or population. Results should therefore not be compared as if they share a common success rate unless the underlying measurement contract is compatible.

Several evaluations also require system level observability. Examples include internal channel instrumentation, attributed communication graphs, full execution traces, topology observations, or procedural action histories. This distinction is important for both benchmark interpretation and defense design because a method that assumes global traces has a different observation model from a local output guardrail.

## Evidence strength

The evaluation corpus should distinguish three questions:

1. Does the study compare a multi agent system with a standalone or alternative system baseline?
2. Does it demonstrate a concrete interaction mechanism through communication, shared state, delegation, aggregation, topology, or another relational path?
3. Does it establish a structural multi agent property that cannot be represented as a property of one isolated agent?

A paper may be valuable security evidence without satisfying all three. These distinctions should be recorded as evidence characterization rather than used to silently change membership in the final 201 corpus.

## Use in the SoK

Use `papers/evaluations/README.md` for the complete 44 work evaluation primary list. Use individual paper notes for benchmark units, baselines, metrics, and evidence locations. Do not use removed analysis tables or historical corpus denominators as active benchmark counts.
