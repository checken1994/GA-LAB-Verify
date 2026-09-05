import unittest
from ga_lab_verify.config import PolicyConfig
from ga_lab_verify.models import CheckStatus
from ga_lab_verify.policy import evaluate_repository_policy

class PolicyTests(unittest.TestCase):
    def test_dirty_blocks(self):
        r=evaluate_repository_policy(PolicyConfig(),clean=False,changed=[],diff_text=''); d={x.check_id:x for x in r}
        self.assertEqual(d['policy.clean_worktree'].status,CheckStatus.FAIL)
    def test_protected_blocks(self):
        r=evaluate_repository_policy(PolicyConfig(protected_paths=('.github/workflows/',)),clean=True,changed=['.github/workflows/ci.yml'],diff_text=''); d={x.check_id:x for x in r}
        self.assertEqual(d['policy.protected_paths'].status,CheckStatus.FAIL)
    def test_weakening_detected(self):
        r=evaluate_repository_policy(PolicyConfig(),clean=True,changed=[],diff_text='+    assert True\n'); d={x.check_id:x for x in r}
        self.assertEqual(d['policy.test_integrity'].status,CheckStatus.FAIL)
    def test_removed_placeholder_not_new_weakening(self):
        r=evaluate_repository_policy(PolicyConfig(),clean=True,changed=[],diff_text='-    assert True\n'); d={x.check_id:x for x in r}
        self.assertEqual(d['policy.test_integrity'].status,CheckStatus.PASS)
