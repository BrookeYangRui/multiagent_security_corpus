# Cross-Paper Insights for a Multi-Agent Security SoK

## Purpose and Evidence Boundary

This document develops candidate headline findings from the 142-work canonical
corpus. It is a synthesis layer, not a replacement for paper notes, claim-level
coding, or named human review. The corpus currently contains 90 archival
peer-reviewed works, 47 non-peer or publication-unverified works, and five
workshop or nonarchival works. Of the 142 works, 92 are coded `core_security`
and 50 `security_relevant` ([final search closure](FINAL_SEARCH_CLOSURE.md)).

The labels below follow the repository synthesis protocol:

- **Established finding**: a result explicitly reported by one or more cited
  papers, with the scope of the cited evaluations preserved.
- **Cross-paper observation**: a pattern obtained by comparing multiple paper
  records or structured corpus fields.
- **Our interpretation**: a proposed SoK-level explanation or design principle
  that is not attributed to any one paper.
- **Open question**: a research problem not resolved by the current corpus.

All paper notes and active source-review rows remain `agent_unverified` or
pending named author/reviewer signoff. Quantitative manuscript claims must be
checked against the cited canonical full text before publication
([evidence policy](EVIDENCE_POLICY_AND_REVIEW_REPORT.md)).

## Central Thesis

> **Multi-agent security is not the sum of agent security. It is the security
> of composition under distributed trust, state, and authority.**

**Our interpretation.** A locally safe-agent premise does not establish a safe
system:

```text
Safe(A1) and ... and Safe(An)  =/=>  Safe(Compose(A1, ..., An))
```

The security-relevant object is better represented by a composition contract:

```text
C = (principals, interaction graph, mutable state, capabilities,
     observer/intervention rights, outcome contract)
```

This is an analytic contract, not a fixed security taxonomy. It makes explicit
the variables that determine whether locally acceptable behavior becomes a
globally unauthorized outcome. Conjunctive Prompt Attacks demonstrates that two
fragments that are benign in isolation can become harmful only after routing
composes them ([note](../papers/attacks/acl/2026_arif_conjunctive_prompt_attacks.md),
`arif2026conjunctive`). Architecture Matters reports that changing roles,
topology, and memory can make matched multi-agent configurations substantially
more vulnerable than standalone agents while retaining benign utility in its
tested settings ([note](../papers/attacks/icml/2026_hagag_architecture_matters.md),
`hagag2026architecturematters`). Formalizing the Safety, Security, and
Functional Properties of Agentic AI Systems identifies the corresponding
cross-protocol semantic composition problem ([note](../papers/general/arxiv/2025_allegrini_formalizing_properties.md),
`allegrini2025formalizing`).

## Corpus-Level Signals

These signals motivate the findings but do not by themselves prove a security
claim:

| Signal | Corpus result | Interpretation boundary |
| --- | ---: | --- |
| Canonical works | 142 | One canonical work per version family |
| Core security | 92 | Direct security model, violation, defense, or evaluation |
| Security relevant | 50 | Informative but without a complete direct-security framing |
| Attack-primary works | 58 | Canonical placement, not the attack-claim denominator |
| Claim-level attack candidates | 91 | Provisional source-review coding |
| Attack candidates outside attack-primary | 39/91 (42.9%) | 21 defense, 17 evaluation, one general |
| Evaluation artifacts | 43 | Reusable benchmark, dataset, harness, protocol, or suite records |
| Distinct textual unit descriptions | 43/43 | Does not imply zero conceptual overlap |
| Distinct textual denominator descriptions | 43/43 | Metric names alone are not comparable |

The counts come from
[`corpus/papers.csv`](../corpus/papers.csv),
[`active_source_review.csv`](../reviews/universal/active_source_review.csv),
[`claim_extraction_queue.csv`](../corpus/sets/05_analysis_specific/claim_extraction_queue.csv),
and [`evaluation_artifacts.csv`](../corpus/sets/05_analysis_specific/evaluation_artifacts.csv).

## Finding 1: Safe Components Do Not Compose into a Safe System

> **The defining multi-agent failure is often not that one agent becomes
> unsafe, but that locally acceptable actions compose into a globally
> unauthorized outcome.**

**Cross-paper observation.** Three distinct attack families have the same
structure. Conjunctive attacks distribute harmful intent across individually
benign fragments. Control-flow hijacking launders an attacker-selected recovery
path through benign specialist agents. Open-channel cognitive collusion composes
individually truthful evidence into a false collective conclusion
([Conjunctive Prompt Attacks](../papers/attacks/acl/2026_arif_conjunctive_prompt_attacks.md),
`arif2026conjunctive`;
[Control-Flow Hijacking](../papers/attacks/iclr/2026_jha_control_flow_hijacking.md),
`jha2026controlflowhijacking`;
[Lying with Truths](../papers/attacks/acl/2026_hu_lying_truths.md),
`hu2026lyingtruths`).

**Our interpretation.** Component certification cannot prove system security
unless the certificate is closed under routing, state updates, and delegated
authority. The missing object is a composition theorem or a runtime composition
monitor, not another per-agent refusal score.

## Finding 2: The Malicious Object Is Often a Trace, Not a Message

> **A system can execute a malicious trace even when every individual message
> passes a local benignity check.**

**Cross-paper observation.** Lying with Truths uses factual public fragments;
Conjunctive Prompt Attacks uses locally benign fragments; control-flow hijacking
uses a plausible error report and repair plan; Thought Virus propagates a latent
preference without requiring a repeated malicious string
([Lying with Truths](../papers/attacks/acl/2026_hu_lying_truths.md),
`hu2026lyingtruths`;
[Conjunctive Prompt Attacks](../papers/attacks/acl/2026_arif_conjunctive_prompt_attacks.md),
`arif2026conjunctive`;
[Control-Flow Hijacking](../papers/attacks/iclr/2026_jha_control_flow_hijacking.md),
`jha2026controlflowhijacking`;
[Thought Virus](../papers/attacks/arxiv/2026_weckbecker_thought_virus.md),
`weckbecker2026thoughtvirus`).

**Our interpretation.** Maliciousness is relational. It can reside in the
relationship among messages, principals, timing, permissions, and goals rather
than in message text. A monitor targeting these failures therefore needs trace
provenance and policy state, not only content classification.

## Finding 3: Multi-Agent Is a Causal Claim, Not an Architecture Label

> **Using multiple agents does not make a result multi-agent-specific. The
> security effect must disappear or materially change when interaction is
> removed.**

**Cross-paper observation.** Agent Smith's population-spread outcome is
undefined without peer interaction, making it a clearly interaction-dependent
effect ([note](../papers/attacks/icml/2024_gu_agent_smith.md),
`gu2024agentsmith`). By contrast, the guardrail denial-of-service primitive also
works against single-agent systems; only shared-service head-of-line blocking is
the multi-agent-specific consequence
([note](../papers/attacks/arxiv/2026_zhou_guardrail_dos.md),
`zhou2026shieldtarget`). Architecture Matters directly compares matched
standalone and multi-agent configurations, providing the stronger causal design
([note](../papers/attacks/icml/2026_hagag_architecture_matters.md),
`hagag2026architecturematters`).

**Our interpretation.** A minimum MAS-security experiment should include an
interaction ablation or matched single-agent counterfactual. Agent count is a
system description; interaction dependence is the causal inclusion test. The
92 core-security versus 50 security-relevant split shows that this distinction
is load-bearing for the corpus rather than terminological.

## Finding 4: Collaboration Is Both the Capability Channel and the Attack Channel

> **The mechanisms that create collective capability are the same mechanisms
> that erode isolation.**

**Cross-paper observation.** Communication enables coordination and infection;
memory enables continuity and persistent poisoning; delegation enables
specialization and privilege laundering; trust enables cooperation and
over-disclosure. The Trust Paradox reports that increasing trust generally
raises both coordination success and exposure in its 1,488 evaluated chains
([note](../papers/attacks/journals_ieee_tcss/2026_xu_trust_paradox.md),
`xu2026trustparadox`). CalBench shows that privacy-preserving silence can harm
coordination and fair burden allocation
([note](../papers/evaluations/arxiv/2026_zou_calbench.md),
`zou2026calbench`). Architecture Matters reports setting-specific vulnerability
increases of up to 3.8-fold at comparable or higher benign accuracy
([note](../papers/attacks/icml/2026_hagag_architecture_matters.md),
`hagag2026architecturematters`).

**Our interpretation.** Security is not an independent post-processing layer on
top of collaboration. It constrains the same information and authority flows
that produce utility. A meaningful defense result must therefore report which
capability it removes, delays, or redistributes.

## Finding 5: Reachable Authority, Not Agent Count, Determines Blast Radius

> **The effective attack surface scales with reachable authority rather than
> with the number of agents.**

**Cross-paper observation.** M-Spoiler targets one known participant while
optimizing for the final collective decision and includes experiments scaling
to 101 agents
([note](../papers/attacks/emnlp/2025_liu_manipulate_collective_decisions.md),
`liu2025manipulatecollective`). Don't Trust Your Upstream begins at an exposed
edge agent, reconstructs the graph, and chooses a path to a privileged internal
agent ([note](../papers/attacks/arxiv/2025_liang_dont_trust_upstream.md),
`liang2025donttrustupstream`). Control-flow hijacking reaches otherwise
unavailable tools by manipulating delegation rather than compromising every
member ([note](../papers/attacks/iclr/2026_jha_control_flow_hijacking.md),
`jha2026controlflowhijacking`).

**Our interpretation.** The relevant scaling variables are privileged
reachability, cut vertices, delegation depth, memory scope, and the number of
independent enforcement boundaries. An additional low-authority agent may add
little risk; one agent on a privileged path may dominate system risk.

## Finding 6: There Is No Safest Topology, Only Topology-Threat Pairs

> **Topology is a security control plane, but its effect has no universal
> ordering.**

**Established finding.** In its evaluated privacy setting, Topology Matters
reports that dense graphs and central placements often leak more, while absolute
levels and some rankings vary by model
([note](../papers/evaluations/findings_acl/2026_liu_topology_memory_leakage.md),
`liu2026topologymemory`). NetSafe reports a setting-specific 29.7% relative
performance decrease for a star topology and identifies a security-bottleneck
phenomenon
([note](../papers/evaluations/findings_acl/2025_yu_netsafe.md),
`yu2025netsafe`). Architecture Matters concludes that topology and memory
rankings vary across models and environments
([note](../papers/attacks/icml/2026_hagag_architecture_matters.md),
`hagag2026architecturematters`).

**Our interpretation.** Dense connectivity can increase propagation and
leakage; hubs can concentrate privilege and failure; sparse graphs can create
bottlenecks; pruning can fragment useful communication. Claims about a safe
topology must name the protected property, attacker position, role placement,
and utility constraint.

## Finding 7: Memory Converts a Transient Injection into Distributed State

> **In a multi-agent system, memory is not merely storage. It is a replication
> substrate.**

**Cross-paper observation.** Agent Smith seeds one memory and models subsequent
population spread; Prompt Infection instructs recipients to retain and
reproduce a role-specific payload; Troublemaker optimizes both retrieval and
replication in independent memories
([Agent Smith](../papers/attacks/icml/2024_gu_agent_smith.md),
`gu2024agentsmith`;
[Prompt Infection](../papers/attacks/esorics_workshops/2026_lee_prompt_infection.md),
`lee2026promptinfection`;
[Troublemaker](../papers/attacks/acl/2025_men_troublemaker.md),
`men2025troublemaker`). AgentSafe correspondingly places authorization and
poisoning controls at both message and persistent-memory layers
([note](../papers/defenses/arxiv/2025_mao_agentsafe.md),
`mao2025agentsafe`).

**Our interpretation.** Isolating the original attacker is insufficient once
derived state has been copied into honest agents. Recovery requires provenance,
taint propagation, expiry, revocation, and state repair across descendants.
Current attack-success metrics rarely include this cleanup cost.

## Finding 8: Attack Effects Can Diffuse While Attribution Signals Decay

> **The farther an attack travels, the less its current carrier may resemble
> the original attacker.**

**Cross-paper observation.** When Embedding-Based Defenses Fail shows that
malicious-message separability and the proposed confidence signal both decay
over communication rounds, especially in dense graphs
([note](../papers/attacks/icml/2026_zhang_embedding_defenses.md),
`zhang2026embeddingdefenses`). Thought Virus reports that downstream agents
continue carrying a preference after the seeded agent leaves the conversation
([note](../papers/attacks/arxiv/2026_weckbecker_thought_virus.md),
`weckbecker2026thoughtvirus`). Prompt Infection turns newly compromised agents
into subsequent senders
([note](../papers/attacks/esorics_workshops/2026_lee_prompt_infection.md),
`lee2026promptinfection`).

**Our interpretation.** Propagation creates an attribution inversion: harm can
become more distributed while evidence of the initial malicious source becomes
less distinct. Node-removal defenses should therefore be evaluated against
already-laundered state and messages, not only at the first malicious hop.

## Finding 9: Agreement Can Be the Attack Outcome

> **Consensus is not a security objective without validity. A system can become
> more unanimous and less secure at the same time.**

**Established finding.** Persuasion-driven debate attacks increase agreement
with an attacker-selected wrong answer while reducing collective accuracy
([note](../papers/attacks/journals_scientific_reports/2026_kraidia_collaboration_fails.md),
`kraidia2026collaborationfails`). Lying with Truths causes victims and downstream
judges to converge on a false narrative assembled from true fragments
([note](../papers/attacks/acl/2026_hu_lying_truths.md),
`hu2026lyingtruths`). Rethinking the Reliability of Multi-agent System reports
task accuracy under six of seven faulty nodes, but its measured contract is not
classical agreement, validity, and termination
([note](../papers/defenses/aaai/2026_zheng_byzantine_reliability.md),
`zheng2026byzantinereliability`).

**Our interpretation.** LLM collectives introduce an epistemic-integrity
problem: protocol-compliant agents may agree on an unjustified, manipulated, or
unauthorized conclusion. Majority voting over correlated models and shared
messages is not independent redundancy and should not be described as BFT
without a formal protocol contract.

## Finding 10: The Final Output Is the Wrong Security Boundary

> **A clean final answer does not prove a clean execution, and an unsafe answer
> does not prove an external impact.**

**Established finding.** AgentLeak reports 68.8% leakage in inter-agent messages
versus 27.2% in final outputs in one comparison; output-only auditing misses
internal violations
([note](../papers/evaluations/journals_ieee_access/2026_el_yagoubi_agentleak.md),
`elyagoubi2026agentleak`). Architecture Matters separates planning refusal,
execution refusal, harmful action, and completed harm
([note](../papers/attacks/icml/2026_hagag_architecture_matters.md),
`hagag2026architecturematters`). BAD-ACTS uses executable evaluators for 937
harmful actions, while keeping tools emulated
([note](../papers/evaluations/colm/2026_nother_bad_acts.md),
`nother2026badacts`).

**Our interpretation.** Evaluation needs two independent axes: internal policy
violations over the full trace and verified external effects. Final-output ASR
alone can undercount confidentiality failures and overstate real-world impact.

## Finding 11: Many Defenses Assume an Omniscient and Sovereign Defender

> **A defense can appear general only because its observer has privileges that
> the deployment does not provide.**

**Cross-paper observation.** Among the 23 defense-primary records with populated
mechanism and limitation coding, at least seven explicitly require central,
global, or fully instrumented graph/trace visibility: G-Safeguard, GUARDIAN,
ALTEDA, BlindGuard, XG-Guard, SAIGuard, and TopoSHIELD. At least five also
require topology-changing authority, and at least six explicitly depend on
stable or known identities. These are provisional lower bounds from the active
review fields, not final human-adjudicated prevalence estimates
([active review](../reviews/universal/active_source_review.csv)).

Representative evidence includes G-Safeguard's near-global graph visibility and
edge-control requirement
([note](../papers/defenses/acl/2025_wang_g_safeguard.md),
`wang2025gsafeguard`), BlindGuard's population-level context and graph pruning
([note](../papers/defenses/acl/2026_miao_blindguard.md),
`miao2026blindguard`), and TopoSHIELD's global temporal graph and runtime edge
control ([note](../papers/defenses/findings_acl/2026_huang_toposhield.md),
`huang2026toposhield`).

The remaining visibility cases are GUARDIAN
([note](../papers/defenses/neurips/2025_zhou_guardian.md),
`zhou2025guardian`), ALTEDA
([note](../papers/defenses/journals_information_processing_management/2026_rabieinejad_alteda.md),
`rabieinejad2026alteda`), XG-Guard
([note](../papers/defenses/acl/2026_pan_xg_guard.md),
`pan2026xgguard`), and SAIGuard
([note](../papers/defenses/arxiv/2026_shi_saiguard.md),
`shi2026saiguard`). The topology-control lower bound is supported by
`wang2025gsafeguard`, `zhou2025guardian`, `pan2026xgguard`, `shi2026saiguard`,
and `huang2026toposhield`. The stable/known-identity lower bound is supported by
`mao2025agentsafe`, `ebrahimi2025credibility`, `wang2025gsafeguard`,
`zhou2025guardian`, `he2025atrust`, and `miao2026blindguard`.

**Our interpretation.** Every defense result should disclose an observation and
intervention contract: what the defender sees, what it trusts, when it acts, and
what it can block or rewrite. Performance without this contract is not portable.

## Finding 12: Observability Is a Security Resource and a Privacy Liability

> **The visibility needed to detect collusion or propagation can itself violate
> confidentiality and create a concentrated attack surface.**

**Cross-paper observation.** Secret Collusion defines covertness relative to an
observer who lacks private knowledge or intent
([note](../papers/attacks/neurips/2024_motwani_secret_collusion.md),
`motwani2024secretcollusion`). Audit the Whisper requires transcripts, paired
interventions, outcomes, calibration data, and sometimes subgroup labels
([note](../papers/defenses/arxiv/2025_tailor_audit_whisper.md),
`tailor2025auditwhisper`). AgentLeak needs instrumentation across seven internal
channels to find exposures that output-only review misses
([note](../papers/evaluations/journals_ieee_access/2026_el_yagoubi_agentleak.md),
`elyagoubi2026agentleak`). CalBench shows that information restriction can also
degrade coordination and fairness
([note](../papers/evaluations/arxiv/2026_zou_calbench.md),
`zou2026calbench`).

**Our interpretation.** Oversight should be treated as a constrained information
flow, not an unlimited trusted sink. The open problem is privacy-preserving
oversight that proves policy compliance without collecting every principal's
full transcript and state.

## Finding 13: Defenses Relocate Risk into the Trusted Computing Base

> **A guarantee without an explicit trusted computing base is an incomplete
> security result.**

**Cross-paper observation.** Maris offers formal information-flow enforcement,
but its guarantee depends on correct policies, labels, identities, and complete
mediation
([note](../papers/defenses/arxiv/2025_cui_maris.md),
`cui2025maris`). ControlValve blocks all evaluated IPI and CFH attacks in its
reported tables, but trusts pre-ingestion planning and complete mediation of
relevant agent transitions
([note](../papers/attacks/iclr/2026_jha_control_flow_hijacking.md),
`jha2026controlflowhijacking`). BlockA2A moves trust into cryptography, ledger
consensus, smart contracts, policy oracles, and endpoint compliance
([note](../papers/defenses/arxiv/2025_zou_blocka2a.md),
`zou2025blocka2a`).

**Our interpretation.** These controls can be valuable precisely because they
make trust explicit. The SoK should compare defenses by trusted computing base,
mediation coverage, and failure mode rather than by post-defense ASR alone.

## Finding 14: The Defense Plane Is Becoming an Attack Plane

> **Centralizing safety enforcement can create a shared failure domain for the
> entire agent population.**

**Established finding.** From Shield to Target attacks reasoning guardrails by
inducing long generations. In its MAS setting, a poisoned worker causes
head-of-line blocking and starvation for other agents sharing the guardrail
service; token and time limits create a fail-open versus fail-closed trade-off
([note](../papers/attacks/arxiv/2026_zhou_guardrail_dos.md),
`zhou2026shieldtarget`). Topology defenses similarly concentrate observation
and edge-control authority in a monitor
([G-Safeguard](../papers/defenses/acl/2025_wang_g_safeguard.md),
`wang2025gsafeguard`;
[TopoSHIELD](../papers/defenses/findings_acl/2026_huang_toposhield.md),
`huang2026toposhield`).

**Our interpretation.** Defense evaluation should include attacks on the
monitor, resource isolation, stale or forged telemetry, and graceful degradation.
A security component that all agents require is part of the availability threat
model, not outside it.

## Finding 15: Authentication Preserves Provenance, Not Benign Intent

> **A correctly authenticated malicious peer is still malicious. Signed malice
> remains malice.**

**Cross-paper observation.** A2ASecBench separates spoofed publishers,
malicious registered remote agents, and adversarial clients or users; depending
on the attack, the Host can become a confused deputy across discovery, task
state, requests, and returned artifacts
([note](../papers/evaluations/iclr/2026_li_a2asecbench.md),
`li2026a2asecbench`). BlockA2A supplies identity, signatures, provenance,
reputation, access control, and revocation, but relies on a large trusted
infrastructure
([note](../papers/defenses/arxiv/2025_zou_blocka2a.md),
`zou2025blocka2a`). Control-flow hijacking shows how benign authenticated agents
can become confused deputies through legitimate delegation
([note](../papers/attacks/iclr/2026_jha_control_flow_hijacking.md),
`jha2026controlflowhijacking`).

The published ICLR paper is now source-resolved against OpenReview
`LfdFnakqGJ`. Its exact locators support the protocol-stage taxonomy, the
1,800-task suite denominator, and the reported NeMo gateway experiment. The
Capability Cloaking and Tables 3--4 trial denominators remain unstated, and all
SoK interpretations still require named human signoff.

**Our interpretation.** In open A2A systems, a remote agent should be modeled as
a software supply-chain dependency with delegated authority, not merely as
another model endpoint. Identity and message integrity are necessary, but
admission control, capability attenuation, lifecycle quotas, artifact
validation, and contextual authorization remain separate obligations.

## Finding 16: The Field Has Benchmarks but Not Yet a Shared Measurement Contract

> **ASR without a unit, denominator, stage, and aggregation rule is not a
> metric.**

**Cross-paper observation.** The corpus contains 43 evaluation artifacts. Their
structured records contain 43 distinct textual unit descriptions, 43 distinct
denominator descriptions, and 43 distinct metric bundles. This does not mean
that no concepts overlap; it means that metric-name equality does not establish
measurement-contract equality
([evaluation artifact ledger](../corpus/sets/05_analysis_specific/evaluation_artifacts.csv)).
The frozen annual export also shows a shift from eight evaluation-primary works
in 2025 to 25 by the partial 2026 cutoff, compared with 28 attack-primary works
in that partial year. This is evidence of rapid evaluation growth, not a
full-year growth-rate comparison
([yearly export](../corpus/final/yearly_distribution.csv)).

Troublemaker defines ASR over agent-question pairs and rounds and summarizes the
maximum across rounds
([note](../papers/attacks/acl/2025_men_troublemaker.md),
`men2025troublemaker`). Hierarchical Attacks conditions ASR on clean-correct
samples and separately reports local and systemic errors
([note](../papers/attacks/cvpr/2026_zhou_hierarchical_attacks.md),
`zhou2026hierarchicalattacks`). TAMAS combines attack success, task success, and
a benchmark-specific Effective Robustness Score
([note](../papers/evaluations/acl/2026_kavathekar_tamas.md),
`kavathekar2026tamas`). Agent Smith measures infected agents and population
spread rather than task-level ASR
([note](../papers/attacks/icml/2024_gu_agent_smith.md),
`gu2024agentsmith`).

**Our interpretation.** The field is industrializing before it is
standardizing. A reusable result tuple should contain at least:

```text
(property, threat model, system configuration, intervention,
 unit, denominator, time horizon, aggregation, uncertainty, impact stage)
```

Without that tuple, cross-paper leaderboards are often category errors.

## Finding 17: Current Evidence Establishes Exploitability, Not Deployment Risk

> **The literature has denominators for trials, but rarely denominators for
> exposure.**

**Cross-paper observation.** Agent Smith's one-million-agent result is simulated
scale, not deployment prevalence
([note](../papers/attacks/icml/2024_gu_agent_smith.md),
`gu2024agentsmith`). BAD-ACTS evaluates 937 harmful actions with executable
checks in emulated environments
([note](../papers/evaluations/colm/2026_nother_bad_acts.md),
`nother2026badacts`). MASLeak evaluates 810 synthetic applications plus selected
platform cases and uses component-specific extraction measures
([note](../papers/attacks/usenix_security/2026_wang_masleak.md),
`wang2026masleak`). Parasites in the Toolchain supplies a valuable ecosystem
census of 12,230 tools across 1,360 servers, but explicitly separates the
presence of capability gadgets from successful exploitation
([note](../papers/attacks/ieee_security_privacy/2026_zhao_parasites_toolchain.md),
`zhao2026parasites`).

**Our interpretation.** Most current results estimate conditional
exploitability: success given an attacker, selected configuration, and benchmark
trial. Deployment risk additionally requires exposure prevalence, attacker
frequency, control coverage, realized impact, and recovery cost. These quantities
must not be inferred from ASR.

## Finding 18: A Paper Is Not an Attack; a Claim Is

> **Paper-level labels are placement metadata. Security evidence lives at claim
> or instance level.**

**Cross-paper observation.** The active source review marks 91 works for
claim-level attack coding even though only 58 papers are attack-primary. Of
those 91 candidates, 39 (42.9%) are defense-, evaluation-, or general-primary.
Similarly, 22 of the 43 evaluation artifacts are attached to attack- or
defense-primary papers. Surveys and related-work mentions are not primary attack
evidence
([universal review methodology](../reviews/methodology/UNIVERSAL_REVIEW.md)).

**Our interpretation.** The analysis unit should be:

```text
(claim, adversary or fault actor, capability, precondition, mechanism,
 interaction surface, system property, evidence locator, evaluation contract)
```

This prevents three recurrent errors: treating paper placement as evidence,
counting one paper as one attack, and collapsing multiple incompatible outcomes
into a single paper-level category.

## Second-Order Synthesis

The findings above support four broader conclusions.

### Security Is a Hyperproperty over Interacting Traces

**Our interpretation.** Several key properties compare multiple principals,
views, or executions: whether one principal learns another's data, whether an
observer can distinguish collusion, whether a message has different authority
after delegation, or whether a perturbation spreads beyond its source. These
cannot be evaluated from one final response. Multi-agent security is therefore
closer to an information-flow or trace hyperproperty than to ordinary output
classification
([AgentLeak](../papers/evaluations/journals_ieee_access/2026_el_yagoubi_agentleak.md),
`elyagoubi2026agentleak`;
[Secret Collusion](../papers/attacks/neurips/2024_motwani_secret_collusion.md),
`motwani2024secretcollusion`;
[Conjunctive Prompt Attacks](../papers/attacks/acl/2026_arif_conjunctive_prompt_attacks.md),
`arif2026conjunctive`).

### LLM-MAS Security Has an Epistemic-Integrity Core

**Cross-paper observation.** A non-exclusive keyword audit of the 109 active
rows with populated system-failure coding finds at least 40 explicitly involving
collective decision, belief, answer, objective, or output integrity. The
recurring failure is not only protocol deviation. Agents may follow the
protocol, exchange grammatical messages, and reach agreement while the group
becomes less truthful or less justified
([Collective Manipulation](../papers/attacks/emnlp/2025_liu_manipulate_collective_decisions.md),
`liu2025manipulatecollective`;
[Lying with Truths](../papers/attacks/acl/2026_hu_lying_truths.md),
`hu2026lyingtruths`;
[Collaboration Fails](../papers/attacks/journals_scientific_reports/2026_kraidia_collaboration_fails.md),
`kraidia2026collaborationfails`). The count is a provisional lower bound with
overlapping property families, not a mutually exclusive taxonomy.

### Security Interventions Redistribute Risk

**Our interpretation.** Pruning communication may reduce propagation while
damaging availability or fairness. Increased monitoring may improve detection
while reducing privacy. Timeouts may limit resource attacks while causing
fail-open safety bypass or fail-closed denial of service. Trust may improve task
completion while increasing disclosure. A scalar safety score cannot represent
these transfers
([CalBench](../papers/evaluations/arxiv/2026_zou_calbench.md),
`zou2026calbench`;
[Trust Paradox](../papers/attacks/journals_ieee_tcss/2026_xu_trust_paradox.md),
`xu2026trustparadox`;
[From Shield to Target](../papers/attacks/arxiv/2026_zhou_guardrail_dos.md),
`zhou2026shieldtarget`).

### Security Maturity Should Be Measured by Contracts, Not Component Count

**Our interpretation.** Adding a guard agent, reputation agent, blockchain,
auditor, or anomaly detector does not monotonically increase security. Each
component adds assumptions, privileges, state, latency, and a new failure mode.
A mature system is one whose principals, authority, information flows, trusted
computing base, recovery semantics, and measurable properties are explicit
([AgentSafe](../papers/defenses/arxiv/2025_mao_agentsafe.md),
`mao2025agentsafe`;
[BlockA2A](../papers/defenses/arxiv/2025_zou_blocka2a.md),
`zou2025blocka2a`;
[G-Safeguard](../papers/defenses/acl/2025_wang_g_safeguard.md),
`wang2025gsafeguard`).

## Manuscript-Ready Headline Statements

These statements are concise enough for an abstract, introduction, or
conclusion, but their supporting quantitative details still require named human
signoff.

1. **Safe agents do not necessarily compose into a safe system.**
2. **In multi-agent systems, maliciousness is often a property of the trace,
   not any individual message.**
3. **Multi-agent is a causal security claim, not an architectural label.**
4. **The attack surface scales with reachable authority, not agent count.**
5. **There is no safest topology; there are only topology-threat-property
   combinations.**
6. **Consensus without validity can be the attack outcome.**
7. **The final answer is not the system security boundary.**
8. **A defense is only as general as its observation, trust, and intervention
   contract.**
9. **A guarantee without an explicit trusted computing base is incomplete.**
10. **Authentication proves who sent a message, not whether the delegated action
    is authorized.**
11. **ASR without a unit, denominator, stage, and aggregation rule is not a
    metric.**
12. **Current evidence demonstrates exploitability more often than deployment
    risk.**
13. **A paper is not an attack; a claim is.**

## Research Agenda Implied by the Corpus

### Composition Security

**Open question.** Which local contracts are closed under routing, delegation,
memory updates, and tool invocation? Can a practical system prove that no
composition of locally permitted actions yields a globally forbidden outcome?

### Authority-Reachability Metrics

**Open question.** Can blast radius be predicted from privilege-weighted graph
reachability, state scope, and enforcement cuts better than from agent count or
raw graph density?

### Trace-Level Evaluation Contracts

**Open question.** Can benchmarks standardize property, unit, denominator,
stage, time horizon, and impact verification while retaining domain-specific
metrics?

### Privacy-Preserving Oversight

**Open question.** Can an auditor verify collaboration policy, provenance, or
non-collusion without becoming a global plaintext observer and concentrated
privacy risk?

### Adaptive Defense Evaluation

**Open question.** How do defenses perform when the attacker knows the detector,
targets its observation assumptions, poisons its normal traces, or attacks the
defense service itself?

### Distributed Recovery

**Open question.** After a malicious source is removed, how can a system find
and revoke derived memories, summaries, plans, credentials, and beliefs already
copied into honest agents?

### Deployment Risk Denominators

**Open question.** What fraction of deployed systems expose each authority path,
what controls are active, how often attacks occur, and what verified harms and
recovery costs result?

### Epistemic Validity

**Open question.** What is the analogue of validity for LLM collectives when
ground truth is unavailable, agents are correlated, and a persuasive coalition
can increase agreement around an unsupported conclusion?

## Recommended SoK Positioning

The SoK should not present its main contribution as another attack/defense
taxonomy. Its stronger contribution is to recast multi-agent security as
**trace-level compositional security under distributed authority** and to show
that current evidence is fragmented across incompatible observation,
intervention, and measurement contracts.

The central narrative is therefore:

```text
local safety does not compose
        -> interaction creates new system properties
        -> attacks exploit paths, state, and delegated authority
        -> defenses require explicit observer and trusted-base contracts
        -> evaluation requires claim-level, trace-level measurement
        -> current benchmarks establish exploitability, not yet deployment risk
```
