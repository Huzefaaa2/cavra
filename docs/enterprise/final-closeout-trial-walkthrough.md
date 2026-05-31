# Final Closeout Trial Walkthrough

This walkthrough gives customer evaluators a structured way to review CAVRA final closeout workflows with synthetic evidence. It is designed for Community Edition demos, private trial artifacts, and future SaaS trial onboarding without exposing Enterprise source code.

## Audience

- Customer security architect
- Platform engineering lead
- Release manager
- Audit or compliance stakeholder
- Sales engineer or solution architect

## Trial Setup

Use non-production evidence and a non-production connector route. The sample evidence package lives in `examples/demos/final-closeout-trial/sample-evidence-package.json`.

Recommended session length: 45 to 60 minutes.

## Walkthrough Flow

1. Establish the operating model.
   - Explain that Community records public-safe metadata and evidence.
   - Explain that Enterprise or SaaS is responsible for license validation, authenticated connector delivery, SSO/RBAC enforcement, private archive operations, and paid policy packs.

2. Open the Evidence Console or review the sample package.
   - Identify the final readiness bundle.
   - Confirm the release closeout summary is closed.
   - Confirm the signed archive manifest uses external signature metadata only.

3. Review retention approval.
   - Confirm retention review state is `approved`.
   - Confirm retention date and legal hold metadata are present.
   - Verify there are no private archive credentials or deletion controls in the public evidence.

4. Review the downloadable artifact bundle.
   - Confirm the bundle references closeout, readiness, manifest, and file hashes.
   - Confirm the sample contains synthetic identifiers and no customer material.

5. Run or explain retention health.
   - Review approval posture, expiry window, delivery failures, and severity.
   - Explain how a warning or critical finding becomes an owner-tracked release decision.

6. Review alert routing.
   - Show a redacted alert delivery record.
   - Explain that live connector credentials belong in operator-owned systems, Enterprise, or SaaS.

7. Review failed delivery retry planning.
   - Show a retry plan for a simulated failed closeout delivery.
   - Show dry-run worker output before live redelivery.
   - Explain that live redelivery must use an approved connector path.

8. Apply release criteria.
   - Walk through `docs/release-governance-final-closeout-release-criteria.md`.
   - Classify the sample as `ready_for_release`, `ready_with_accepted_risk`, or `blocked`.

9. Close with the upgrade path.
   - Community proves the evidence chain and open plugin model.
   - Trial artifacts prove the private packaging path.
   - Enterprise or SaaS adds organization controls, license validation, authenticated connectors, dashboards, private policy packs, and managed support.

## Trial Success Checklist

- [ ] Customer can explain what evidence CAVRA records before release closeout.
- [ ] Customer can identify which closeout artifacts are public-safe.
- [ ] Customer can identify which controls require Enterprise or SaaS.
- [ ] Customer can review retention health and retry evidence.
- [ ] Customer can map the closeout package to their release governance or audit process.
- [ ] Customer understands that production connectors, license validation, archive mutation, and customer templates are not in the public repository.

## Customer Questions To Capture

- Which release governance system should receive closeout decisions?
- Which SIEM, ITSM, ChatOps, GRC, or webhook providers are required?
- What retention windows apply to AI-agent release evidence?
- What SSO/RBAC groups approve live retries and closeout exceptions?
- Which compliance reports or policy packs are required for production?
- Does the customer need self-hosted Enterprise, hosted SaaS, or both?

## Follow-Up Artifacts

- Final closeout sample evidence package
- Release criteria decision
- Open-core boundary summary
- Integration discovery notes
- Production pilot recommendation

