# Evaluation Measurement Coding

This codebook defines a provisional measurement view over the 43 artifacts in
`evaluation_artifacts.csv`.  The coding is an assistant-derived synthesis of
canonical notes and indexed availability URLs.  It is pending named-author
signoff and must not be reported as independently reproduced artifact behavior.

## Evaluation Categories

`primary_eval_category` uses exactly one analysis lens.  Optional
`secondary_eval_categories` are semicolon-separated and use the same vocabulary.
These labels organize measurement contracts; they do not replace the corpus's
paper-level attack, defense, and evaluation roles.

- `propagation_topology`: spread, graph structure, node placement, or
  interaction architecture is the main measurement object.
- `collective_decision_deception`: collective decisions, deception, collusion,
  or belief manipulation is the main endpoint.
- `privacy_information_flow`: disclosure, contextual privacy, memory leakage,
  or information-flow boundaries are central.
- `delegation_protocol_action`: delegated authority, protocol behavior, tool
  invocation, or harmful action is central.
- `trace_procedural_compliance`: a full trace, procedure, rule, or local-to-global
  measurement contract is central.
- `adaptive_defense_detection`: detection, attribution, adaptation, mitigation,
  or defense comparison is central.

## Impact Evidence Ladder

`impact_stage_max` records the strongest endpoint directly supported by the
canonical note.  A higher stage cannot be inferred merely from a more severe
claimed risk.

- `S1_observable`: an output, score, vote, judgment, or behavioral endpoint is
  observed without a trace or executed-effect contract.
- `S2_trace`: messages, rounds, state transitions, trajectories, propagation, or
  cross-layer telemetry are directly measured.
- `S3_executed_or_persistent`: a controlled action or side effect is executed,
  or state/payload persistence is directly measured.
- `S4_deployment`: a field-deployed system has explicit exposure, control,
  incident, and recovery denominators.  The frozen 43-artifact view contains no
  S4 evidence; platform cases and sandbox executions remain S3 or lower.
- `pending`: the available canonical evidence cannot safely determine a stage.

## Interaction Counterfactual

- `matched_single_agent`: the task and relevant local primitive are compared
  with a matched single-agent system.
- `matched_architecture`: comparable tasks and components are evaluated under a
  matched architecture or topology change.
- `edge_state_authority_ablation`: an interaction edge, shared state, role, or
  authority variable is removed or changed while retaining the local primitive.
- `component_or_attack_controls`: clean, attacked, defended, or component
  controls exist but do not isolate the interaction structure.
- `none_reported`: the note reports no usable counterfactual.
- `pending`: the source evidence is insufficient to select a class.

## Availability

- `code_and_data`: the indexed release is explicitly evidenced as containing
  executable code or a harness and evaluation data.
- `code_or_harness`: a direct repository is indexed but a joint code-and-data
  release is not established by the note.
- `data_only`: a direct data release is established without an executable
  harness.
- `project_page`: an artifact project page is available but release contents are
  not established.
- `paper_only`: the indexed URL resolves to a paper, proceedings, or publication
  record rather than a separately evidenced artifact.
- `unverified`: the indexed artifact-like URL or its contents were not verified.

Availability is separate from reproduction and evidence verification.  In
particular, `code_and_data` records evidence about release contents; it does not
mean that the corpus maintainers executed the release or verified its reported
results.  A2ASecBench and CalBench are `code_and_data`; their primary sources
support `S3_executed_or_persistent` effects and component or attack controls,
but neither reports a matched structural interaction ablation.  These codes
remain provisional pending named human signoff.

## Status And Provenance

`coding_basis` states the local reason for each classification.
`evidence_locator` begins with the canonical note path and identifies the note
sections used.  `coding_status` remains
`assistant_derived_pending_author_signoff` until a named reviewer records an
adjudication; this ledger does not modify paper-note verification status.
