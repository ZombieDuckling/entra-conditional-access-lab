# Design notes

## Scope

This lab covers the review workflow around Microsoft Entra Conditional Access policy design. It does not create or enforce tenant policies.

## Assumptions

- Emergency access accounts exist, are cloud-only, and are monitored separately.
- Device compliance signals are already available through endpoint management.
- Named locations are maintained by the identity or network team.
- Report-only mode is available for staged rollout.
- Security operations can review sign-in logs before enforcement.

## Review questions

Use these questions before moving a policy from report-only to on:

1. Does the policy have a named owner?
2. Does it exclude emergency access accounts where appropriate?
3. Are included users and groups scoped as narrowly as the risk allows?
4. Are applications named rather than hidden under vague descriptions?
5. Are location exclusions justified and documented?
6. Is the expected user impact recorded in the register?
7. Is the rollback owner clear?

## Rollout pattern

1. Draft policy and register entry.
2. Run local validation.
3. Peer review the policy JSON and register.
4. Import into a test or staging tenant if available.
5. Run in report-only mode.
6. Review sign-in impact with service owners.
7. Enforce after the change record is approved.

## Data handling

Do not place live exports in this repository. Store live exports in the approved internal evidence location for the tenant, with access limited to the change team.
