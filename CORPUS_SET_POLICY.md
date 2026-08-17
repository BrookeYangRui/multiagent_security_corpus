# Three-Set Corpus Policy

This repository uses three evidence sets and one screened-out pool. The sets have different jobs in the SoK and must not be merged into one denominator.

## Shared scope gate

A work can enter Set 1 or Set 2 only when source review establishes all of the following:

1. At least two separately addressable LLM-backed agents or principals.
2. An explicit inter-agent relation, such as communication, shared state, delegation, aggregation, topology, membership, or a shared environment.
3. A concrete security property, adversary, attack, defense, guarantee, or security evaluation.
4. The interaction relation creates, amplifies, composes, propagates, obscures, or otherwise changes the security effect.
5. A retrievable source supports the decision. Title-only guesses cannot enter either corpus set.

The literature cutoff remains 2026-07-01. A later publication may qualify only when a version available by the cutoff supports the reviewed claim.

## Set 1: Core synthesis corpus

Set 1 supplies the paper's architecture, taxonomy, attack and defense landscape, quantitative counts, representative tables, and headline findings.

A work enters Set 1 when it passes the shared scope gate and satisfies at least one maturity condition:

* it is an archival peer-reviewed publication; or
* its frozen citation count is greater than 10.

These conditions form a union, not an intersection. An influential preprint may therefore enter Set 1, while a newly published peer-reviewed paper may enter with few citations. Full-text evidence is required for claims used to build the paper's systematization.

## Set 2: Emerging directions corpus

Set 2 contains in-scope work that introduces a credible new attack, defense, benchmark, mechanism, or system direction but has not yet met the Set 1 maturity rule. Typical cases are unaccepted preprints and low-citation early papers.

Set 2 may motivate open problems, emerging trends, and future research directions. It must not determine the taxonomy, prevalence estimates, headline counts, or mature field-wide conclusions.

## Set 3: Contextual citation set

Set 3 is not part of the MAS security corpus. It contains citation-worthy work used for background, comparison, terminology, classical foundations, standards, single-agent baselines, agentic-system context, measurement practice, or deployment examples.

Every Set 3 row must carry a citation role, such as:

* related_work
* classical_foundation
* single_agent_baseline
* agentic_security_context
* protocol_or_standard
* measurement_context
* deployment_evidence
* defense_analogy

Set 3 cannot support a claim that an attack or defense is multi-agent-specific.

## Screened out

Works that fail the shared scope gate and do not have a concrete citation role remain screened out. They are retained only in the review ledger needed to account for the search process. They do not appear in Set 1, Set 2, Set 3, corpus figures, or paper evidence counts.

## Citation count rule

Citation counts are frozen with a date and source. OpenAlex is the primary count source; Semantic Scholar is used only when OpenAlex has no record. The threshold is strictly greater than 10. Each row records the count, source, and snapshot date so later citation growth does not silently move a paper between sets.

## Required tags

Set 1 and Set 2 rows must record:

* publication status and venue
* peer-review status
* citation count, source, and snapshot date
* dominant contribution: attack, defense, evaluation, survey, or general
* interaction interface
* security risk or protected property
* interaction dependence class
* evidence basis and locator
* reviewer and review date

Set 3 rows must record its citation role and the paper section or claim it supports.

## Paper use

1. Build and revise the paper from Set 1.
2. Use Set 2 only to identify emerging directions and open challenges.
3. Insert Set 3 where background, comparison, or external support is needed.
4. Report the three denominators separately and never describe Set 3 as corpus evidence.
