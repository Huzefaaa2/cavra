# AISPM Trial Access And Operator Approval

This public-safe lab explains the Enterprise Trial access flow at a product
and operator level. It describes what a trial evaluator should experience and
what the private operator workflow must verify before package access and a
trial license are issued.

The live approval dashboard, license issuance, GHCR/package access grants,
email delivery, private audit events, and evaluator records remain private
Enterprise responsibilities.

## Evaluator Flow

1. Open the CAVRA Enterprise Trial portal.
2. Submit a trial request with business contact and intended evaluation scope.
3. Receive a request-submitted email from the trial service.
4. Wait for operator approval.
5. After approval, receive public-safe setup instructions and private package
   access guidance through the approved channel.
6. Run the trial package with the provided license key in a controlled
   evaluation environment.

## Operator Review Flow

| Step | Operator Responsibility | Evidence |
| --- | --- | --- |
| Intake | Review request completeness and organization fit. | Request record ref. |
| Risk review | Confirm the request is appropriate for a limited Enterprise Trial. | Review decision ref. |
| Approval | Approve, deny, or request more information. | Approval event ref. |
| Handoff | Trigger evaluator setup instructions and package access. | Handoff packet ref. |
| Closeout | Track expiry, revocation, and follow-up state. | Closeout evidence ref. |

## Operator Readiness Gates

Before announcing or promoting an Enterprise Trial package, the private
operator dashboard should show these release gates as ready:

| Gate | Operator Expectation |
| --- | --- |
| Runtime Binding | Deployment references are present for providers, scheduler, evidence sink, alerts, screenshots, and audit storage. |
| Alert Transport | Synthetic readiness alerts have evidence for email, ChatOps, SIEM, and ITSM destinations. |
| Release Dashboard Publication | Staging release evidence is published to the configured dashboard reference. |
| Trial Field Guide | Screenshots, diagrams, flow charts, and walkthrough references are ready for evaluator onboarding. |
| Operator Audit Archive | Mutation audit export and immutable archive retention validation are ready. |
| Trial Package Readiness Validator | Private package workflow blocks image build or publication when current AISPM readiness evidence is missing. |

The public repository stores only this summary and the related public-safe
readiness packet. The live dashboard output, operator session, approval
records, and archive records remain private.

## Required Controls

- Operator login must be authenticated.
- Approval actions must be audit logged.
- Package access must be gated.
- License keys must never appear in public docs.
- Evaluator identities and request details must be redacted from public
  examples.
- Support handoff should be tracked without exposing private contact details.

## Public Safety Rules

Do not publish license keys, private package URLs, package tokens, evaluator
identity, operator identity, request payloads, IP addresses, private support
records, SMTP credentials, provider responses, or Enterprise source code.

## Public-Safe Screenshots

Use only redacted screenshots for:

- Trial landing page.
- Request submitted state.
- Operator dashboard summary with no evaluator identity.
- Approved handoff status with license and package details removed.

## Verification Checkpoints

| Checkpoint | Expected Result |
| --- | --- |
| Trial request | Request reaches pending or approved state. |
| Operator approval | Approval action creates an audit reference. |
| Evaluator handoff | Handoff packet is ready without exposing secrets. |

## Related Contracts

- `src/cavra/schemas/aispm-report-center-trial-validation-packet.schema.json`
- `src/cavra/schemas/aispm-report-center-trial-operator-dashboard-readiness.schema.json`
- `src/cavra/schemas/aispm-report-center-trial-operator-api-view-model.schema.json`
- `src/cavra/schemas/aispm-report-center-trial-evaluator-handoff-packet.schema.json`

## Related Pages

- [CAVRA Trial Field Guide](CAVRA-Trial-Field-Guide.md)
- [Trial Revocation, Expiry, And Closeout](AISPM-Trial-Revocation-Expiry-And-Closeout.md)
- [Enterprise Trial Self-Service Access](Enterprise-Trial-Self-Service-Access.md)
