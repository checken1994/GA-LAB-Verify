import unittest
from ga_lab_verify.models import CheckResult,CheckStatus,Verdict
from ga_lab_verify.verifier import derive_verdict

class VerdictTests(unittest.TestCase):
    def test_pass(self): self.assertEqual(derive_verdict([CheckResult('a',CheckStatus.PASS,True,'ok')])[0],Verdict.SAFE_TO_MERGE)
    def test_fail_precedes_unknown(self):
        v,_=derive_verdict([CheckResult('a',CheckStatus.UNKNOWN,True,'u'),CheckResult('b',CheckStatus.FAIL,True,'f')]); self.assertEqual(v,Verdict.BLOCKED)
    def test_unknown(self): self.assertEqual(derive_verdict([CheckResult('a',CheckStatus.UNKNOWN,True,'u')])[0],Verdict.UNKNOWN)
    def test_optional_fail_does_not_block(self):
        v,_=derive_verdict([CheckResult('a',CheckStatus.PASS,True,'ok'),CheckResult('b',CheckStatus.FAIL,False,'bad')]); self.assertEqual(v,Verdict.SAFE_TO_MERGE)
