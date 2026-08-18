# SoK: Attack and Defense Landscape of Agentic AI Systems

## Citation

Title: SoK: Attack and Defense Landscape of Agentic AI Systems

Authors: Juhee Kim; Wenbo Guo; Dawn Song

Year: 2026

Venue: 35th USENIX Security Symposium

DOI: Not reported

Primary URL: https://www.usenix.org/conference/usenixsecurity26/presentation/kim-juhee-agentic

Open access URL: https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_kim-juhee-agentic.pdf

BibTeX key: `kim2026agenticai`

## Paper Type

SoK; Survey; Security taxonomy

- Primary category: `survey`
- Scope relation: `security_relevant`
- Recommended corpus placement: `set3_context`
- Recommended citation role: `agentic_security_context`

## Scope

### System Studied

Agentic AI systems that combine one or more LLM components with conventional software components such as memory, tools, user interfaces, workflows, and external environments. Figure 1 explicitly places “Other Agents” in the external environment and notes that multi-agent systems contain multiple agent cores, each with its own memory, system prompts, and tool sets.

### Multi-Agent Dependency

Multi-agent systems are within the paper's broad agentic-system model, but MAS interaction is not the paper's primary unit of systematization. The main architecture, risk taxonomy, and defense taxonomy are organized around an agentic system's components, design dimensions, and AI-software data/control flows. Multi-agent interaction appears as one environment/interface case and in several representative defenses or monitoring examples.

### Application Domain

General agentic AI, including software-development agents, browser agents, tool-using agents, RAG systems, and agentic applications connected to real-world services.

## Methodology

The final USENIX version includes an explicit literature-review methodology in Section 2.

- Time window: 2023 through October 2025.
- Search dimensions: general agent-security terminology; OWASP-defined risks; component-centric terms; traditional-security adaptations.
- Prioritized venues: top security venues and major ML conferences, supplemented with high-impact preprints, industry whitepapers, and CVEs.
- Standalone-model work is manually excluded from the agent-focused corpus.
- The final review reports 128 papers, including 51 attack methods and 60 defense methods; the remainder cover both sides or case studies without a new method.
- OWASP Top 10 for LLM Applications and MITRE ATLAS are used as external reference taxonomies.

This methodology is useful as a comparator but is not a reproducible systematic-search ledger at the level of our corpus: the final paper reports search dimensions and selection principles rather than a released query-by-query screening ledger with per-paper inclusion decisions.

## System Model

The paper characterizes seven design dimensions that increase agent flexibility and, in its analysis, often expand security exposure:

1. input trust;
2. access sensitivity;
3. workflow;
4. action;
5. memory;
6. tool;
7. user interface.

The core distinction is between conventional software with mostly predetermined logic and agentic systems whose LLM-backed workflow can dynamically select data, tools, and actions.

## Security Model

### Threat Actors

Section 4.1 defines three adversary positions:

- external adversary: manipulates external resources that an agent may retrieve or process;
- user-level adversary: directly supplies malicious inputs to the agent;
- internal adversary: controls or compromises an agent component or its provider.

### Attack Vectors

The final taxonomy contains six attack vectors:

- V1 indirect prompt injection;
- V2 malicious data injection;
- V3 tool poisoning;
- V4 direct prompt injection;
- V5 model poisoning;
- V6 memory poisoning.

### Risks

The final paper consolidates the system-level security discussion into seven risks:

- R1 heterogeneous untrusted interfaces;
- R2 wrong instruction following;
- R3 unconstrained / unsafe data flow;
- R4 hallucination and model mistakes;
- R5 private data leakage;
- R6 unintended / unauthorized action and data corruption;
- R7 resource drain and denial of service.

Section 4.3 then maps design dimensions to these risks and explicitly analyzes cascading risk interactions. In particular, R1 expands attacker-controlled entry points; R2-R4 capture model-mediated failures; and these can propagate into confidentiality, integrity, and availability consequences R5-R7.

### Security Goals

The defense section uses confidentiality, integrity, and availability and additionally discusses contextual security: whether runtime context elements are admissible and correctly prioritized for the intended user task.

## Defense Landscape

The final paper groups defenses as follows.

### Runtime Protection

- input guardrails;
- output guardrails;
- information-flow control and taint tracking;
- monitoring;
- human-in-the-loop validation.

### Secure by Design

- privilege separation;
- formal verification / provable security.

### Identity and Access Management

- identity management;
- access control;
- credential management.

### Component Hardening

- model hardening;
- tool hardening.

Section 5.6 discusses defense-in-depth, least privilege, and complete mediation as design principles.

## Main Contribution

The paper systematizes security of agentic AI as a composition of LLM reasoning with conventional software components. Its distinctive organizing axis is **agent design flexibility and component/data-flow structure**, followed by a threat-model-aware attack taxonomy and a defense-in-depth taxonomy.

The final version also adds a system-level risk-interaction analysis rather than treating R1-R7 as independent point failures.

## Relation to Our SoK

### Why It Is Closest Related Work

Kim et al. is the strongest direct comparator for our paper because it asks a similar systems-security question at a broader agentic-system boundary. It shows why component-local LLM security is insufficient once an LLM can dynamically retrieve data, invoke tools, mutate state, and act on external resources.

### Boundary From Our MAS SoK

The two systematizations use different primary units of analysis.

**Kim et al.**

- system boundary: an agentic application combining LLMs and conventional software;
- primary structure: model, memory, tools, workflow, UI, environment;
- central delta: flexible AI-generated control/data flow across AI-software components;
- attacks/defenses: organized mainly by agent component, adversary position, and defense mechanism.

**Our MAS SoK**

- system boundary: an execution involving multiple separately addressable LLM-backed principals;
- primary structure: communication/routing, shared state, delegation/authority, aggregation, membership/admission, and observation/defense across principals;
- central delta: security properties that are inherited but amplified by interaction, composition-induced, or structurally multi-agent;
- attacks/defenses: organized around the inter-agent relation and the observer/control point required to detect or stop the system-level effect.

This makes Kim et al. a Set 3 agentic-security comparator rather than Set 1/2 MAS-security evidence. The paper contains MAS examples, but its security claims do not generally require a material inter-agent relation.

### Concepts We Reuse as Context

- component security is necessary but insufficient for agentic systems;
- dynamic data/control flow expands downstream consequences of LLM failures;
- adversary position should be separated from the consequence/risk taxonomy;
- inherited defenses should be distinguished from agent-specific adaptations;
- system-level risk interactions matter more than a flat list of vulnerabilities;
- defense coverage should be linked to attack/risk coverage.

### Concepts We Should Not Import Unchanged

- the seven agent design dimensions are not a substitute for MAS topology/authority/state dimensions;
- “other agents” as part of the external environment is too coarse for our unit of analysis;
- agent-level IAM, access control, credential management, model hardening, and generic prompt guardrails should enter our core only when an inter-agent relation materially changes the security mechanism or consequence;
- its component-oriented risk labels should not be treated as our MAS risk taxonomy.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure / table | Evidence |
| --- | --- | --- | --- | ---: | --- | --- |
| The final paper scopes to risks unique to or significantly amplified in agentic systems. | Explicit author claim | Final USENIX paper | 2 | 3 | - | Scope paragraph. |
| The literature review covers 2023 through October 2025 and reports 128 papers, 51 attack methods, and 60 defense methods. | Explicit author claim | Final USENIX paper | 2 | 3 | - | Methodology paragraph. |
| The agent model includes other agents, while MAS have multiple cores with their own memory, prompts, and tools. | Explicit author claim | Final USENIX paper | 3.1 | 4 | Figure 1 | Figure caption and system description. |
| Seven design dimensions are input trust, access sensitivity, workflow, action, memory, tool, and user interface. | Explicit author claim | Final USENIX paper | 3.2 | 4-5 | Table 1 | Design-space taxonomy. |
| Three adversary classes and six attack vectors structure the attack model. | Explicit author claim | Final USENIX paper | 4.1 | 5-6 | Figure 2 | External, user-level, internal; V1-V6. |
| The final risk taxonomy contains R1-R7 and Section 4.3 analyzes risk interactions/amplification. | Explicit author claim | Final USENIX paper | 4.2-4.3 | 6-8 | Figures 2-3 | Risk taxonomy and cascading analysis. |
| The defense landscape maps mechanisms to covered risks. | Explicit author claim | Final USENIX paper | 5 | 8-15 | Table 2; Figure 4 | Runtime, secure-by-design, IAM, and component-hardening defenses. |
| The paper is a broad agentic-security comparator rather than MAS-primary evidence. | Corpus interpretation | Final USENIX paper | 3-5 | 4-15 | Figures 1-4 | Main taxonomy is component/design-dimension centered; MAS is one supported system form rather than the main analytical unit. |

## Provenance

### Discovery Source

USENIX Security 2026 official proceedings.

### Accessed Version

Final proceedings version, 35th USENIX Security Symposium, August 12-14, 2026.

### Access Date

2026-08-18

### Prepared By

OpenAI GPT-5.6 Sol, source-level review of the final proceedings PDF.

### Verification Status

`assistant_source_reviewed_pending_author_signoff`

### Last Updated

2026-08-18
