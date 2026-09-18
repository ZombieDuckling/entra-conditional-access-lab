# Change control checklist

Use this checklist when adapting the lab pattern to a real tenant.

## Before submission

- Policy has a clear owner and business reason.
- Emergency access exclusions have been checked.
- Included groups and applications are named.
- Named locations are current and approved.
- Report-only impact has been reviewed.
- Helpdesk and service owners know the planned change window.
- Rollback owner and action are recorded.
- Validation report is attached to the change ticket.

## Evidence to attach

- Policy JSON export or portal screenshot from the approved tenant evidence store.
- Sign-in log sample showing report-only impact.
- Register row with expected user impact.
- Rollback instruction.
- Approval from the application or service owner when a single app is affected.

## Enforcement gate

Do not enforce a policy if any of these are unresolved:

- emergency access path not tested
- unknown affected users in report-only logs
- named location ownership unclear
- device compliance dependency not ready
- no rollback owner
- no service owner approval for app-specific controls
