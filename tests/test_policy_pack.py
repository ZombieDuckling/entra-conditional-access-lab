import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_policy_pack.py"

spec = importlib.util.spec_from_file_location("validate_policy_pack", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class PolicyPackTests(unittest.TestCase):
    def test_policy_pack_validates(self):
        self.assertEqual([], validator.validate())

    def test_sample_pack_contains_expected_policy_count(self):
        pack = validator.load_json(ROOT / "policies" / "conditional-access-pack.json")
        self.assertEqual(7, len(pack["policies"]))

    def test_all_policies_exclude_emergency_access(self):
        pack = validator.load_json(ROOT / "policies" / "conditional-access-pack.json")
        for policy in pack["policies"]:
            with self.subTest(policy=policy["id"]):
                self.assertIn("grp-break-glass", policy["excludedGroups"])

    def test_no_sample_policy_is_enabled(self):
        pack = validator.load_json(ROOT / "policies" / "conditional-access-pack.json")
        states = {policy["state"] for policy in pack["policies"]}
        self.assertEqual({"reportOnly"}, states)


if __name__ == "__main__":
    unittest.main()
