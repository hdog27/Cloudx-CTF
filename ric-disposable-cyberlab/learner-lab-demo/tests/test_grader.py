"""Offline tests for the instructor-controlled Linux demo grader."""
import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "grader.py"
spec = importlib.util.spec_from_file_location("cloudx_grader", MODULE_PATH)
grader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grader)


class AssessmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.backup = Path(self.tmp.name) / "backup"
        self.backup.write_text("FAKE_VALUE=demo\n", encoding="utf-8")
        self.reflection = Path(self.tmp.name) / "reflection.txt"

    def score(self, owner=True, outsider=True):
        def readable(user, path):
            return owner if user == "learner" else outsider
        with patch.object(grader, "can_read_as", side_effect=readable):
            return grader.assess(self.backup, self.reflection)

    def test_initial_exposed_file_scores_only_owner_access(self):
        self.backup.chmod(0o644)
        result = self.score(owner=True, outsider=True)
        self.assertEqual(result["score"], 20)
        self.assertFalse(result["complete"])

    def test_secure_file_with_reflection_scores_100(self):
        self.backup.chmod(0o600)
        self.reflection.write_text(
            "The backup was world-readable. I restricted it to the owner "
            "and verified that other users cannot read it.",
            encoding="utf-8")
        result = self.score(owner=True, outsider=False)
        self.assertEqual(result["score"], 100)
        self.assertTrue(result["complete"])

    def test_remediation_must_preserve_legitimate_access(self):
        self.backup.chmod(0o600)
        self.reflection.write_text(
            "I changed the permissions and verified the effect on users.",
            encoding="utf-8")
        result = self.score(owner=False, outsider=False)
        self.assertEqual(result["score"], 80)
        self.assertFalse(result["complete"])

    def test_reflection_is_required_but_not_graded_for_truth(self):
        self.backup.chmod(0o600)
        result = self.score(owner=True, outsider=False)
        self.assertEqual(result["score"], 85)
        self.assertFalse(result["complete"])
        self.assertIn("instructor", " ".join(result["notes"]).lower())

    def test_absent_backup_is_error(self):
        self.backup.unlink()
        with self.assertRaises(RuntimeError):
            self.score()


if __name__ == "__main__":
    unittest.main()
