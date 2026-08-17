# Three-Set Corpus Policy

This repository uses three evidence sets and one screened-out pool. The sets have different jobs in the SoK and must not be merged into one denominator.

## Shared scope gate

A work can enter Set 1 or Set 2 only when source review establishes all of the following:

1. At least two separately addressable LLM-backed agents or principals.
2. An explicit inter-agent relation, such as communication, shared state, delegation, aggregation, topology, membership, or a shared environment.
3. A concrete security property, adversary, attack, defense, guarantee, or security evaluation.
4. The inter-agent relation is a material part of the attack, defense, evaluation, or security-relevant execution path rather than incidental background.
5. A retrievable source supports the decision. Title-only guesses cannot establish corpus membership.

The scope gate answers whether a paper studies security in an LLM multi-agent system. It does **not** require the paper to isolate the causal effect of interaction. Interaction dependence and evidence strength are coded separately. A paper may therefore be in scope even when it demonstrates a plausible propagation, delegation, shared-state, or aggregation mechanism without a matched single-agent or rewired-system comparison.

The literature cutoff remains 2026-07-01. A later publication may qualify only when a version available by the cutoff supports the reviewed claim.

## Set 1: Mature corpus

Set 1 is the mature in-scope MAS-security corpus. A work enters Set 1 when it passes the shared scope gate and satisfies at least one maturity condition:

* it is peer reviewed; or
* its frozen citation count is at least 10.

These conditions form a union, not an intersection. An influential preprint may therefore enter Set 1, while a newly published peer-reviewed paper may enter with few citations.

Full-text taxonomy readiness is **not** a Set 1 membership condition. It is recorded separately in the `taxonomy_ready` field. Papers lacking complete taxonomy mapping remain in Set 1 but cannot silently carry taxonomy-specific or causal claims that their available evidence does not support.

## Set 2: Emerging directions corpus

Set 2 contains work that passes exactly the same MAS-security scope gate but has not yet met the Set 1 maturity rule. Typical cases are unaccepted preprints and low-citation early papers.

Set 2 may motivate emerging attacks, defenses, benchmarks, mechanisms, and open research directions. It must not be silently counted as mature evidence.

## Set 3: Contextual citation set

Set 3 is not part of the MAS-security corpus. It contains citation-worthy work used for background, comparison, terminology, classical foundations, standards, single-agent baselines, agentic-system context, measurement practice, deployment examples, or defense analogies.

Every Set 3 row must carry a citation role. Set 3 cannot support a claim that an attack or defense is multi-agent-specific unless the manuscript explicitly uses it only as adjacent context.

## Screened out

Works that fail the shared scope gate and do not have a concrete citation role remain screened out. They are retained in the review ledger to account for the search process but do not enter MAS-security evidence counts.

## Citation count rule

Citation counts are frozen with a date and source. OpenAlex is the primary count source; Semantic Scholar is used when needed. The Set 1 threshold is **greater than or equal to 10**. Each row records the count, source, and snapshot date so later citation growth does not silently move a paper between sets.

## Evidence strength and taxonomy readiness

Corpus membership and claim strength are separate judgments.

For interaction claims, the manuscript distinguishes evidence such as mechanism evidence, matched comparative evidence, and structural evidence. A paper can be in Set 1 or Set 2 without proving a numerical causal interaction effect. The interaction-dependence field records what type of system-level effect is claimed; the strength of the supporting comparison is assessed separately in the manuscript evidence audit.

`taxonomy_ready=yes` means the current source package contains sufficient full-text evidence and mapped interaction/risk tags for detailed taxonomy use. `taxonomy_ready=no` means more extraction or author review is needed. This field never changes Set 1 versus Set 2 membership.

## Required tags

Set 1 and Set 2 rows record publication status, peer-review status, frozen citation count, contribution type, interaction interface, security risk or protected property, interaction-dependence class, evidence basis and locator, taxonomy readiness, reviewer, and review date.

Set 3 rows record a citation role and the paper section or claim it supports.

## Paper use

1. Use Set 1 as the mature corpus denominator.
2. Use Set 2 to identify emerging directions and open challenges.
3. Use `taxonomy_ready` and the separate evidence audit to decide which Set 1 papers can support detailed taxonomy or causal claims.
4. Use Set 3 only for background, comparison, or external support.
5. Report Set 1, Set 2, and Set 3 denominators separately.
