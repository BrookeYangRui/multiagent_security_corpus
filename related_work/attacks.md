# Attacks

This synthesis is anchored to the final signed **201 work** manuscript corpus. The active corpus contains **44 attack primary works**, all indexed in `papers/index.csv` and materialized under `papers/attacks/`.

The attack directory is the authoritative paper placement view. A work can still provide attack evidence when its dominant contribution is defense, evaluation, general, or survey, so the count of 44 must not be interpreted as the total number of papers containing any attack result.

## Main interaction dependent patterns

### Propagation and contagion

Several works study malicious influence that moves across agent communication rather than remaining local to one model. Examples include Agent Smith, Troublemaker, Prompt Infection, Flooding Spread of Manipulated Knowledge, CORBA, and topology guided adversarial propagation. These papers motivate analyzing who can influence whom, how quickly influence spreads, and whether topology or role changes alter the outcome.

### Communication manipulation

Attack papers also target the message path itself through tampering, prompt injection, semantic fragmentation, covert communication, and belief manipulation. Examples include Attack the Messages, Conjunctive Prompt Attacks, Lying with Truths, CoMet, and Secret Collusion. The relevant security object is often a sequence or relation among messages rather than a single prohibited string.

### Consensus and collective decision manipulation

A separate cluster studies how one or more adversarial participants can distort group decisions, debate outcomes, or collective beliefs. Examples include Can an Individual Manipulate the Collective Decisions of Multi Agents?, insider attacks on consensus systems, persuasion driven attacks, and many to one adversarial consensus.

### Shared state, tools, and execution

Other attacks exploit shared memory, RAG, tool use, workflow planning, latent state, or code execution. These mechanisms matter because compromise can cross agent boundaries through state or authority even when direct agent to agent messages are not the only carrier.

### Confidentiality and structural inference

The final attack set also contains work on intellectual property leakage, topology inference, latent communication exposure, and other confidentiality failures. MASLeak and CIA are representative examples in which the protected object is a system level relation or shared resource rather than only one agent response.

## Use in the SoK

Use `papers/attacks/README.md` for the complete 44 work attack primary list and venue placement. Use the individual paper notes for technical claims and evidence locations. Do not reuse counts, queues, or denominators from earlier corpus versions.
