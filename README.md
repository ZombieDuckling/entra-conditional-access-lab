# Entra Conditional Access Lab

A tenant-safe lab for designing and reviewing Microsoft Entra Conditional Access policies before they are copied into a real environment.

The repository uses synthetic users, groups, apps, named locations, and policy exports. It shows the workflow a security engineer would use when preparing access controls for a Microsoft 365 estate:

- map access requirements to policy intent
- stage policies in report-only mode
- check break-glass exclusions
- review named location and device compliance dependencies
- validate JSON policy exports before change control
- produce a short evidence report for reviewers

No directory-specific identifiers, user principal names, client data, tokens, or live exports are included.

## What this demonstrates

This lab maps to the VAT IT Security Engineer role areas around Microsoft 365 security, identity controls, endpoint posture, scripting, documentation, and risk-led operations.

| Role area | Evidence in this repo |
| --- | --- |
| Entra ID and Microsoft 365 security administration | Conditional Access policy pack with staged controls for admins, users, guests, legacy authentication, risky sign-ins, and unmanaged devices |
| Security operations and incident readiness | Runbook for emergency access review, report-only rollout, and incident-driven tightening |
| PowerShell and automation | Export and comparison scripts for Graph PowerShell, written to avoid secrets and tenant-specific values |
| Governance and change control | Policy register, risk notes, validation report, and explicit assumptions |
| Endpoint and compliance awareness | Device-compliance and unmanaged-device controls with clear dependency checks |

## Repository layout

```text
.
├── docs/
│   ├── change-control-checklist.md
│   ├── design-notes.md
│   └── operations-runbook.md
├── policies/
│   ├── conditional-access-pack.json
│   └── policy-register.csv
├── sample-data/
│   ├── apps.json
│   ├── groups.json
│   ├── named-locations.json
│   └── users.json
├── scripts/
│   ├── Compare-ConditionalAccessExport.ps1
│   ├── Export-ConditionalAccessPolicies.ps1
│   └── validate_policy_pack.py
└── tests/
    └── test_policy_pack.py
```

## Quick start

Run the validation from the repository root:

```bash
python3 scripts/validate_policy_pack.py
python3 -m unittest discover -s tests
```

Expected result:

```text
Validation passed: 7 policies checked
```

The validator checks that:

- every policy has a stable ID, owner, intent, state, and rollback note
- production-impacting policies start in `reportOnly`
- emergency access accounts are excluded from every policy
- referenced users, groups, applications, and named locations exist in sample data
- grant controls are explicit
- the policy register matches the JSON pack

## Policy set

The sample pack includes seven policies:

1. Admin MFA and compliant device requirement
2. Block legacy authentication
3. Require MFA for risky sign-ins
4. Guest access session controls
5. Unmanaged device browser restriction
6. Finance application location guardrail
7. Baseline user MFA rollout

The names are deliberately plain. A policy reviewer should be able to understand the purpose without reading a paragraph of marketing copy.

## How to use this safely

Use the files as a review pattern, not as a drop-in tenant configuration.

1. Replace sample groups, users, app IDs, and named locations with values from the target tenant.
2. Keep policies in report-only mode until sign-in logs show the expected impact.
3. Confirm emergency access accounts are cloud-only, monitored, and excluded where needed.
4. Record expected user impact in the policy register.
5. Run validation before raising a change request.
6. Attach the generated report and register to the change ticket.

## Graph PowerShell notes

The PowerShell scripts are examples for controlled export and comparison work. They do not contain credentials and they do not write to a tenant. The export script uses read scopes only.

```powershell
Connect-MgGraph -Scopes "Policy.Read.All","Directory.Read.All"
./scripts/Export-ConditionalAccessPolicies.ps1 -OutputPath ./exports/current-ca-policies.json
./scripts/Compare-ConditionalAccessExport.ps1 -BaselinePath ./policies/conditional-access-pack.json -CurrentPath ./exports/current-ca-policies.json
```

## Design choices

- JSON policy data is kept separate from the CSV register so reviewers can check both machine-readable and human-readable views.
- Policy state is explicit. Anything with user impact is staged as report-only in the sample pack.
- Synthetic objects use stable IDs so tests can catch broken references.
- The validation script uses the Python standard library only, which keeps CI simple.

## Safety statement

This repository uses synthetic data only. It contains no live directory exports, no credentials, no directory-specific identifiers, and no customer information.
