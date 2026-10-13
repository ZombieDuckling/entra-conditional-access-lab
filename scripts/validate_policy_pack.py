#!/usr/bin/env python3
"""Validate the synthetic Conditional Access policy pack."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALID_STATES = {"enabled", "disabled", "reportOnly"}
VALID_GRANT_CONTROLS = {"mfa", "compliantDevice", "approvedClientApp", "block"}
VALID_CLIENT_TYPES = {"browser", "mobileAppsAndDesktopClients", "exchangeActiveSync", "other"}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_ids(path: Path) -> set[str]:
    data = load_json(path)
    return {item["id"] for item in data}


def validate(pack: dict | None = None) -> list[str]:
    errors: list[str] = []
    if pack is None:
        pack = load_json(ROOT / "policies" / "conditional-access-pack.json")
    policies = pack.get("policies", [])
    users = load_ids(ROOT / "sample-data" / "users.json")
    groups = load_ids(ROOT / "sample-data" / "groups.json")
    apps = load_ids(ROOT / "sample-data" / "apps.json")
    locations = load_ids(ROOT / "sample-data" / "named-locations.json")

    if not pack.get("metadata", {}).get("schemaVersion"):
        errors.append("metadata.schemaVersion is required")

    seen_ids: set[str] = set()
    for policy in policies:
        policy_id = policy.get("id", "<missing>")
        if policy_id in seen_ids:
            errors.append(f"{policy_id}: duplicate policy id")
        seen_ids.add(policy_id)

        for field in ["id", "displayName", "state", "owner", "intent", "rollback", "reviewCadence"]:
            if not policy.get(field):
                errors.append(f"{policy_id}: missing {field}")

        if policy.get("state") not in VALID_STATES:
            errors.append(f"{policy_id}: invalid state {policy.get('state')}")

        if policy.get("state") == "enabled":
            errors.append(f"{policy_id}: sample policies must not be enabled")

        if "grp-break-glass" not in policy.get("excludedGroups", []):
            errors.append(f"{policy_id}: emergency access group must be excluded")

        for user_id in policy.get("includedUsers", []) + policy.get("excludedUsers", []):
            if user_id not in users and user_id != "all":
                errors.append(f"{policy_id}: unknown user {user_id}")

        for group_id in policy.get("includedGroups", []) + policy.get("excludedGroups", []):
            if group_id not in groups and group_id != "all":
                errors.append(f"{policy_id}: unknown group {group_id}")

        for app_id in policy.get("includedApplications", []) + policy.get("excludedApplications", []):
            if app_id not in apps and app_id != "all":
                errors.append(f"{policy_id}: unknown application {app_id}")

        controls = set(policy.get("grantControls", []))
        if not controls:
            errors.append(f"{policy_id}: grantControls must not be empty")
        unknown_controls = controls - VALID_GRANT_CONTROLS
        if unknown_controls:
            errors.append(f"{policy_id}: unknown grant controls {sorted(unknown_controls)}")
        if "block" in controls and len(controls) > 1:
            errors.append(f"{policy_id}: block cannot be combined with other grant controls")

        conditions = policy.get("conditions", {})
        unknown_client_types = set(conditions.get("clientAppTypes", [])) - VALID_CLIENT_TYPES
        if unknown_client_types:
            errors.append(f"{policy_id}: unknown client app types {sorted(unknown_client_types)}")

        policy_locations = conditions.get("locations", {})
        for location_id in policy_locations.get("include", []) + policy_locations.get("exclude", []):
            if location_id not in locations and location_id != "all":
                errors.append(f"{policy_id}: unknown named location {location_id}")

    register_path = ROOT / "policies" / "policy-register.csv"
    with register_path.open("r", encoding="utf-8", newline="") as handle:
        register_rows = list(csv.DictReader(handle))
    register_ids = {row["policy_id"] for row in register_rows}
    policy_ids = {policy["id"] for policy in policies}
    if register_ids != policy_ids:
        errors.append(f"policy register mismatch: json={sorted(policy_ids)} csv={sorted(register_ids)}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Validation failed")
        for error in errors:
            print(f"- {error}")
        return 1
    count = len(load_json(ROOT / "policies" / "conditional-access-pack.json").get("policies", []))
    print(f"Validation passed: {count} policies checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
