# Non-Peer Citation Threshold Decision Report

## Decision in one page

This report compares citation thresholds for non-peer-reviewed work in the
peer-first corpus. It does not change the active `>20` rule.

Fixed inputs:

- Literature cutoff: `2026-07-01`
- Citation source: Semantic Scholar Graph API
- Citation snapshot: `2026-08-06`
- Comparison operator: strict greater-than (`>`), not greater-than-or-equal
- Scope frame: 326 works included by the frozen interaction-security screen
- Peer-reviewed backbone: 94 works (85 conference/proceedings and 9 journal)

| Non-peer rule | Eligible non-peer works | Raw peer-first core | Added vs. `>20` |
| --- | ---: | ---: | ---: |
| Citations `>20` | 8 | 102 | -- |
| Citations `>10` | 22 | 116 | 14 |
| Citations `>5` | 52 | 146 | 44 |
| Citations `>0` | 146 | 240 | 138 |

The raw number is not the recommended number. Citation count measures uptake,
not interaction-security relevance. A title can enter the broad screen because
it measures error propagation, robustness, or a named coordination fault while
still being unsuitable for the security taxonomy or headline audits.

## Citation distribution of non-peer work

| Citation band | Works |
| --- | ---: |
| `>20` | 8 |
| `11-20` | 14 |
| `6-10` | 30 |
| `1-5` | 94 |
| `0` | 78 |
| Citation or publication status unresolved | 8 |

The unresolved records are not treated as zero-citation records and are not
silently excluded.

## Current `>20` candidates

The recommendation below is a decision aid based on the frozen full-text
screening evidence. It is not a human evidence verification.

| Citations | Work | Preliminary role | Recommendation | Main reason |
| ---: | --- | --- | --- | --- |
| 42 | AgentSafe | Core security | Retain | Access control, impersonation, memory poisoning, and evaluated defenses depend on inter-agent information flow. |
| 37 | CodeCoR | Adjacent | Do not use in the security denominator | Its primary endpoint is code-generation correctness; pruning propagated faults is reliability rather than an adversarial security contract. |
| 37 | Taming Various Privilege Escalation | Core security | Retain | It formalizes inter-agent privilege escalation and evaluates mandatory access control. |
| 31 | Multi-Agent LLMs for Conversational Task-Solving | Contextual / adjacent | Keep outside the core | This is a thesis-style empirical study; alignment collapse and monopolization are secondary findings rather than a primary security study. |
| 31 | Chasing Moving Targets | Boundary | Full-text scope adjudication | It is directly about adversarial safety, but one model alternates attacker and defender roles; whether this satisfies the separate-core MAS rule needs adjudication. |
| 25 | SAFEFLOW | Core security | Retain | It enforces information-flow and transactional security properties over concurrent agents and shared state. |
| 24 | Debate Only When Necessary | Adjacent | Do not use in the security denominator | The main contribution is efficient reasoning and accuracy; error propagation is primarily a performance fault. |
| 21 | MAGPIE | Core security evaluation | Retain | The benchmark directly measures contextual privacy leakage caused by selective inter-agent communication. |

Preliminary reading of the current eight therefore yields:

- 4 clear core-security works;
- 1 boundary work requiring adjudication;
- 3 contextual or adjacent works.

This means the current raw total of 102 must not be interpreted as 102 already
human-verified security papers.

## Fourteen works added by lowering the threshold to `>10`

| Citations | Work | Preliminary role | Recommendation | Main reason |
| ---: | --- | --- | --- | --- |
| 19 | Revisiting Multi-Agent Debate as Test-Time Scaling | Core claim candidate | Retain after claim-level review | It reports harmfulness propagation and ASR under multi-agent debate, although much of the paper concerns general reasoning effectiveness. |
| 19 | SentinelAgent | Core defense candidate | Retain | It detects interaction-level attacks using a communication graph and reports detection cases. |
| 18 | Agent Drift | Security-relevant | Retain as contextual evidence or audit candidate | It quantifies interaction-derived coordination drift, but the evidence is simulated and not necessarily adversarial. |
| 16 | 1-2-3 Check | Core privacy candidate | Retain | The extractor-checker-executor information flow has an evaluated privacy-leakage endpoint. |
| 15 | The Sum Leaks More Than Its Parts | Core privacy candidate | Retain | It studies compositional privacy leakage and collaborative mitigations against an LLM attacker. |
| 15 | Maestro | Adjacent | Exclude from the security denominator | It optimizes collaboration and benchmark accuracy; the named collaboration faults do not establish a security violation. |
| 14 | VeriMoA | Adjacent | Exclude from the security denominator | It controls noise propagation for HDL-generation correctness, not a security property or adversary. |
| 13 | Cohesive Conversations | Adjacent | Exclude from the security denominator | Dialogue authenticity and conversational coherence are quality properties. |
| 13 | Towards Collaborative Intelligence | Adjacent | Exclude from the security denominator | Intention propagation mitigates task miscoordination, primarily a capability/reliability problem. |
| 12 | MedSentry | Core attack/defense candidate | Retain | A malicious member attacks communication across multiple topologies and the paper reports attack and defense safety scores. |
| 12 | WOLF | Core evaluation candidate | Retain | Multiple role-grounded agents deceive and detect one another with explicit deception endpoints. |
| 12 | Institutional AI | Core collusion candidate | Retain | Repeated LLM-agent markets produce collusion and evaluate a runtime governance defense. |
| 11 | CoopetitiveV | Adjacent | Exclude from the security denominator | Its propagated errors and pass@k endpoint concern Verilog-generation correctness. |
| 11 | When Persuasion Overrides Truth | Core integrity candidate | Retain | It measures adversarial persuasion of a collective judge using explicit override metrics. |

Preliminary disposition of the 14 additions:

- 8 clear interaction-security candidates;
- 1 security-relevant boundary candidate (`Agent Drift`);
- 5 adjacent performance/reliability papers.

Therefore lowering the threshold does not automatically add 14 defensible core
papers. It appears to add 8 clear candidates and one boundary candidate before
human source review.

## Decision options

### Option A: Keep `>20`

Raw peer-first core: 102.

Advantages:

- Closest to a high-impact-preprint exception policy.
- Minimizes preprint-heavy findings.
- Simple to explain.

Risks:

- Misses several directly relevant privacy, collusion, drift, and monitoring
  papers with 11-20 citations.
- Citation age strongly favors older work.
- The eight qualifying records still contain adjacent papers, so the higher
  threshold does not remove the need for scope review.

### Option B: Lower to `>10` without another scope gate

Raw peer-first core: 116.

Advantages:

- Similar in size to comparable agent-security SoKs.
- Adds recent security work that has not had enough time to exceed 20 citations.

Risks:

- Five of the 14 additions appear primarily about performance or reliability.
- Reviewers can reasonably challenge a citation-only inclusion rule.
- The nominal increase overstates the increase in security evidence.

This option is not recommended.

### Option C: Use `>10` as a retrieval gate plus a security-scope gate

Recommended policy:

1. Include every identified peer-reviewed work satisfying the frozen scope.
2. Retrieve every non-peer work with citations `>10`.
3. Admit it to the taxonomy-eligible corpus only after full-text confirmation
   of a direct interaction-security property, adversary, violation, defense, or
   security evaluation.
4. Retain performance, reliability, and social-behavior papers as adjacent
   literature rather than counting them in security denominators.
5. Select every audit denominator independently from the taxonomy-eligible set.

Under the preliminary dispositions in this report, Option C would produce:

| Component | Preliminary count |
| --- | ---: |
| Peer-reviewed backbone | 94 |
| Clear non-peer core candidates (`>10`) | 12 |
| Boundary non-peer candidates | 2 |
| Adjacent high-citation non-peer works | 8 |
| Preliminary strict core | 106 |
| Preliminary core plus boundary | 108 |

These are planning numbers, not final corpus counts. The 94 peer-reviewed works
also require the same scope-quality review; peer review establishes publication
maturity, not relevance to this SoK.

## Recommendation

Adopt Option C. Set `>10` as the non-peer discovery threshold, not as automatic
evidence eligibility. This captures newer influential work without allowing
general multi-agent performance papers to inflate the security corpus.

Keep three separate numbers in the paper and artifact:

```text
Included corpus: all works that pass the broad interaction-security screen
Taxonomy-eligible corpus: peer-first works that pass full-text security scope
Analysis-specific eligible set: works satisfying each audit's frozen contract
```

Do not choose a threshold to reach a target paper count. The defensible corpus
size is the result of the scope rule, not an optimization objective.

## Required review before changing the active rule

1. Review the 22 non-peer works above from canonical full text.
2. Resolve the two boundary cases explicitly.
3. Record claim-level security evidence for each retained work.
4. Apply the same scope test to all 94 peer-reviewed works.
5. Regenerate the peer-first ledger only after adjudication.

Until those steps are complete, `corpus/peer_first_eligibility.csv` correctly
retains the active strict `>20` rule.
