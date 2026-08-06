# Whispering Agents: An Event-Driven Covert Communication Protocol for the Internet of Agents

## Citation

Title: Whispering Agents: An Event-Driven Covert Communication Protocol for the Internet of Agents

Authors: Kaibo Huang; Yukun Wei; WanshengWu; Tianhua Zhang; Zhongliang Yang; Linna Zhou

Year: 2026

Venue: AAAI

DOI: 10.1609/aaai.v40i37.40380

Primary URL: https://ojs.aaai.org/index.php/AAAI/article/view/40380

Open access URL: https://ojs.aaai.org/index.php/AAAI/article/download/40380/44341

BibTeX key: huang2026whisperingagents

## Paper Type

- Attack
- Evaluation
- Empirical study
- Theoretical analysis

## Scope

### System Studied

Internet-of-Agents conversations in which communicating LLM agents coordinate through event timing, message content, and behavior.

### Multi-Agent Dependency

The channel encodes a secret dialogue in observable interaction events between agents. It requires communicating endpoints and a monitoring adversary, so neither the covert protocol nor its detectability question exists for an isolated agent.

### Application Domain

Agent-to-agent communication privacy and covert coordination.

## Security Model

### Protected Assets

From the protocol designer's view, the existence and payload of agent communication; from a defender's view, oversight and communication-policy integrity.

### Threat Actor

Cooperating sender and receiver agents facing a passive traffic observer or warden.

### Trusted Components

The endpoints share protocol state and keys; the warden does not compromise endpoint internals.

### Attacker Capabilities

Endpoints choose storage, timing, and behavioral events within an otherwise benign dialogue.

### Security Assumptions

Agents can coordinate protocol parameters, the channel remains available, and the observer relies on transcripts or event statistics rather than endpoint state.

## Main Contribution

The paper formalizes a Covert Event Channel with storage, timing, and behavioral dimensions and instantiates it as Pi-CCAP. It evaluates capacity, robustness, and imperceptibility against statistical and LLM-based wardens.

## Attack or Failure

### Attack Surface

The timing, structure, and behavioral choices of agent-to-agent dialogue events.

### Attack Mechanism

Pi-CCAP maps encrypted payload bits into combinations of message form, event timing, and agent behavior while preserving a benign cover conversation.

### System-Level Failure

A monitor cannot reliably distinguish payload-bearing coordination from ordinary agent traffic.

### Security Consequence

Covert coordination and oversight failure; the same construction can protect legitimate communication privacy or conceal collusion.

## Defense

### Defense Mechanism

No new defense is proposed; statistical steganalysis and LLM-as-a-judge wardens are evaluated as detectors.

### Intervention Point

Global communication trace.

### Required Observability

The warden sees dialogue snippets or event distributions but not shared endpoint secrets.

### Assumptions

Detection baselines model normal traffic adequately and have access to comparable benign samples.

### Limitations

Experiments assume shared keys and a passive adversary; broader adaptive wardens, agent models, topics, and real deployments remain untested.

## Evaluation

### Evaluated Systems

Publicly available LLMs used as communicating agents, with GPT-4o used for one warden evaluation.

### Agent Configuration

Paired communicating endpoints running Pi-CCAP under multiple channel combinations.

### Dataset or Environment

Benign dialogue topics spanning domains such as general question answering and technical conversations.

### Baselines

Single-dimension covert or steganographic methods and benign conversations.

### Metrics

Effective bits per round, total capacity, bit error or robustness measures, statistical AUC, and LLM-judge detection outcomes.

### Main Results

The authors report that combined event channels improve usable capacity while statistical and LLM-based wardens remain close to chance in the tested settings.

## Relation to Existing Work

### Papers Compared by the Authors

Text steganography, timing channels, covert-channel theory, LLM collusion, and A2A communication protocols.

### Claimed Research Gap

Prior work did not provide a unified formal model for interactive, event-driven covert channels among agents.

### Closest Related Work

Secret Collusion among AI Agents and language-model steganography.

### Difference From Prior Work

Pi-CCAP jointly uses storage, timing, and behavioral events rather than hiding information only in text tokens.

## Relevance to Our SoK

### Included Concepts

Covert channel, communicating coalition, observer scope, restricted trace, timing and behavioral metadata, and dual-use protocol.

### Taxonomy Implications

The mechanism belongs under covert coordination; the violated property depends on viewpoint: communication privacy for legitimate users or monitorability for a defender.

### Supported Research Questions

What event metadata must an observer collect to detect multi-agent covert coordination beyond message content?

### Important Limitations

The work demonstrates a protocol rather than prevalence of spontaneous collusion, and tested wardens do not establish general undetectability.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The channel has storage, timing, and behavioral dimensions. | Explicit author claim | Paper | Covert Event Channel | 3-4 | Figure 2 | Formal channel model. |
| Pi-CCAP combines the event dimensions to encode an encrypted payload. | Explicit author claim | Paper | Protocol Design | 4-5 | Algorithm 1 | Protocol construction. |
| Capacity and robustness are compared with single-channel baselines. | Explicit author claim | Paper | Experimental Analysis | 6-7 | Tables 1-2 | Evaluation setup and results. |
| Statistical and GPT-4o wardens test imperceptibility. | Explicit author claim | Paper | Evaluation of Invisibility | 7-8 | Figure 3; Table 3 | Detection evaluations. |
| The paper assumes shared keys and a passive adversary. | Explicit author claim | Paper | Discussion and Limitations | 8 | - | Stated limitations. |

## Provenance

### Discovery Source

AAAI proceedings; Crossref; prior corpus completeness scan.

### Discovery Query

`site:ojs.aaai.org multi-agent covert communication`

### Accessed Version

Published AAAI version; the PDF is authoritative for the title, which uses `An Event-Driven` while the OJS display metadata uses `A Event-Driven`.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05

