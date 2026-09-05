import sys,tempfile,unittest
from pathlib import Path
from ga_lab_verify.config import CommandCheckConfig
from ga_lab_verify.models import CheckStatus
from ga_lab_verify.runner import run_check

class RunnerTests(unittest.TestCase):
    def test_pass_hashes_output(self):
        with tempfile.TemporaryDirectory() as td:
            r=run_check(CommandCheckConfig('ok',(sys.executable,'-c',"print('hello')")),Path(td))
            self.assertEqual(r.status,CheckStatus.PASS); self.assertIsNotNone(r.stdout_sha256); self.assertIsNone(r.stdout)
    def test_failure(self):
        with tempfile.TemporaryDirectory() as td:
            r=run_check(CommandCheckConfig('bad',(sys.executable,'-c','raise SystemExit(7)')),Path(td))
            self.assertEqual(r.status,CheckStatus.FAIL); self.assertEqual(r.return_code,7)
    def test_missing_executable_unknown(self):
        with tempfile.TemporaryDirectory() as td:
            r=run_check(CommandCheckConfig('missing',('definitely-not-real-ga-lab-command',)),Path(td))
            self.assertEqual(r.status,CheckStatus.UNKNOWN)
