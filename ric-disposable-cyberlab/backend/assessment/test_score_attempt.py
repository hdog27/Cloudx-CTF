import unittest
from score_attempt import score_attempt, safe_context

class AssessmentTests(unittest.TestCase):
    def attempt(self, checks):
        return {"attempt_id":"a1","challenge_id":"linux-file-permissions-01","challenge_version":"0.1","checks":checks,"learner_id":"SECRET_LEARNER","command_events":[{"command":"password=SECRET"}]}

    def test_all_passed(self):
        names=("exposure_identified","remediation_applied","unauthorized_access_blocked","legitimate_access_preserved")
        result=score_attempt(self.attempt([{"name":n,"passed":True} for n in names]))
        self.assertEqual(result["score"],100)
        self.assertTrue(result["passed"])

    def test_partial(self):
        result=score_attempt(self.attempt([{"name":"exposure_identified","passed":True}]))
        self.assertEqual(result["score"],20)
        self.assertFalse(result["passed"])

    def test_required_check_gates_passing_score(self):
        names=("exposure_identified","remediation_applied","unauthorized_access_blocked")
        result=score_attempt(self.attempt([{"name":n,"passed":True} for n in names]))
        self.assertEqual(result["score"],85)
        self.assertFalse(result["passed"])

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            score_attempt(self.attempt([{"name":"exposure_identified","passed":True},{"name":"exposure_identified","passed":True}]))

    def test_non_boolean_rejected(self):
        with self.assertRaises(ValueError):
            score_attempt(self.attempt([{"name":"exposure_identified","passed":"true"}]))

    def test_ai_context_excludes_identity_and_command_text(self):
        attempt=self.attempt([])
        context=str(safe_context(attempt,score_attempt(attempt)))
        self.assertNotIn("SECRET",context)
        self.assertNotIn("password",context)
        self.assertNotIn("learner_id",context)

if __name__=="__main__":
    unittest.main()
