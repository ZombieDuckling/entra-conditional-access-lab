# Operations runbook

## Daily checks

- Review risky sign-ins and user risk events.
- Check Conditional Access report-only impact for staged policies.
- Confirm no emergency access account is using normal daily workflows.
- Review failures for admin portals and finance systems.

## Weekly checks

- Compare current tenant policies to the approved baseline.
- Check for policies changed outside the change process.
- Review named location changes.
- Confirm guest access sessions still match collaboration requirements.

## Emergency access review

1. Confirm whether the incident blocks normal administrator sign-in.
2. Use the approved emergency access account only for recovery work.
3. Record the time, reason, actions, and approver in the incident ticket.
4. Rotate credentials if the procedure requires it.
5. Review Conditional Access policies that affected the incident.

## Incident-driven tightening

When a credential incident involves a specific group or app:

1. Identify affected users and applications.
2. Add a report-only policy scoped to that set.
3. Validate emergency access exclusions.
4. Review sign-in log impact.
5. Enforce after incident lead approval.
6. Remove or fold the temporary policy into the baseline after closure.
