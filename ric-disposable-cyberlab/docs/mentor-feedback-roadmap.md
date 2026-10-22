# Cloudx-CTF Mentor Feedback and Roadmap

**Mentor:** Wayne Schmidt  
**Status:** Planning notes and proposed features; not an implementation claim  
**Project:** Cloudx-CTF / RIC disposable cyberlab

## North star

Build a low-cost, isolated, temporary cybersecurity learning environment where an instructor can assign a scenario and a learner can practice, submit evidence, receive actionable feedback, and retry. The long-term learning loop Wayne proposed:

**Attempt → Observe → Assess → Explain → Adapt → Retry**

First validate a single exercise with a real instructor. RIC and CCRI contacts have expressed preliminary interest; production adoption, pilot requirements, and funding are not confirmed.

## Priority 1 — This semester: smallest credible AWS capstone

- [ ] **Define one learning objective and challenge with an instructor.** Specify scenario, task, starting environment, acceptable success evidence, feedback, and possible next exercise. Keep the challenge versioned.
- [ ] **Provision one isolated Linux lab on AWS with Terraform.** Minimize IAM privileges, restrict network connectivity, cap runtime and resource use. Do not assume an intentionally vulnerable VM is safe merely because it is in a VPC.
- [ ] **Demonstrate lifecycle operations:** launch, status/readiness, expire, destroy, and independent cleanup verification. Start with a manual/CLI workflow; add a small authorized API only if time permits.
- [ ] **Test failure and teardown.** Check the effect of repeated launches, partial failures, expiration, and orphaned disks or other resources. Record a recovery procedure.
- [ ] **Connect to the existing CTFd interface** at least enough to demonstrate the student challenge/flag or evidence flow. The CTFd frontend is already self-hosted; AWS infrastructure is not yet implemented.
- [ ] **Add lightweight learner feedback if feasible:** an attempt ID and outcome, short explanation of what was learned, and a suggested retry. Minimal telemetry (e.g., a limited set of lab events) is a stretch goal, not a prerequisite for initial provisioning.
- [ ] **Measure:** deployment time, cleanup success, approximate cost per attempt, idle cost, and the effort required to run a session.

**Definition of done:** one repeatably deployable, demonstrably isolated exercise; a documented learner outcome; controlled teardown; reproducible demonstration and clearly stated limits. Do not claim full automation, forensic-grade evidence, or multi-cloud portability until verified.

## Priority 2 — Future development / pilot

- **Learning records:** associate learner ID, attempt ID, challenge/version, backend, timestamps, outcomes, hints, feedback, retries, and platform errors. Keep raw telemetry separate from learner profiles.
- **Telemetry and evidence preservation:** forward a small, purpose-limited set of command/session and system events; preserve relevant results before ephemeral labs are destroyed. Define consent, access, redaction, retention, encryption, integrity and deletion rules; avoid collecting secrets.
- **Rule-based recommendations:** distinguish learner misunderstandings from infrastructure failures, offer a prerequisite or next exercise, and measure improvement on later attempts. Speed is context, not a primary score.
- **Instructor pilot:** small versioned library, instructor reporting, completion records, support/runbooks, and a realistic operational cost model.
- **Framework mapping:** map specific learning objectives to named versions of NIST/COBIT or other applicable frameworks, explaining the rationale. Finishing a lab does **not** prove organizational compliance.
- **Team scenarios:** carefully isolated red-team, blue-team, incident-response and forensic exercises, including remediation with verification that normal services still work.
- **API and CLI:** common authorized operations for launch, status, reset, expire, destroy and cleanup verification; durable status and idempotent requests.
- **Assessment claims:** separate participation, completion, and proficiency; do not make proficiency claims without validated assessment criteria.

## Priority 3 — Research / possible platform expansion

- **Portability:** separate challenge definitions and lifecycle contracts from deployment adapters. Prove AWS first; then evaluate an on-premises/Proxmox or second-cloud backend. Record cloud-specific dependencies rather than claiming universal compatibility.
- **Low-resource and OS support:** investigate Linux/Windows and low-cost on-premises execution; mobile-friendly learner interface where useful (not necessarily mobile VM execution).
- **Storage tiers:** assess short-lived state/caching separately from durable results; consider S3 lifecycle/Glacier archival only when retrieval time, minimum storage duration, retention, and costs suit the workload.
- **Threat-informed content:** use public CVE/advisory or MITRE ATT&CK material when appropriately licensed and safely reproduced in isolated labs.
- **Scale and economics:** benchmark first at one user, then limited concurrency; explore regional pricing, quotas, cleanup enforcement, unit costs, and later large-scale architecture only when demand exists.
- **Adoption and business model:** interview instructors, identify purchasing and support requirements, and explore possible licensing or curriculum partnerships. No sales or institutional commitments are assumed.
- **AI/ML assessment:** only evaluate after collecting sufficient consented, well-characterized evidence and defining measurable benefits over explicit rules.

## Wayne's specific design principles

1. Design exercises around an observable learning outcome, not just flags.
2. Preserve useful evidence and feedback independently of short-lived lab instances.
3. Keep learner-facing permissions separate from control-plane and infrastructure permissions.
4. Test isolation assuming the learner compromises the intended target.
5. Distinguish learner performance from provisioning delays and broken challenges.
6. Start simple; validate with an instructor before broadening architecture.
7. Think about long-term portability, but avoid implementing multiple backends in the first capstone.
8. Seek professional and educational feedback on what would make a practical pilot.

## Questions to revisit with Wayne

- For our first instructor-approved Linux challenge, what evidence proves the learning objective?
- What is the smallest safe telemetry/attempt record worth retaining?
- How should we balance controlled access, cost ceilings, and automated cleanup?
- Who in cybersecurity education, cloud infrastructure, or cyber range operations could give useful pilot feedback?

## Project constraints

This is a semester capstone being developed alongside coursework and professional commitments. **Prioritize a completed, well-tested AWS proof of concept over speculative product features.** This roadmap records mentor advice for future evaluation; it does not commit the team to delivering every item.
