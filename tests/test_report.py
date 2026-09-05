import copy,unittest
from ga_lab_verify.models import CheckResult,CheckStatus,VerificationReport,Verdict
from ga_lab_verify.report import attach_evidence_hash,evidence_hash

class ReportTests(unittest.TestCase):
    def make(self):
        return VerificationReport(1,'1.0.0','2026-09-05T00:00:00+00:00','/repo','a'*40,None,'b'*64,Verdict.SAFE_TO_MERGE,['ok'],[CheckResult('x',CheckStatus.PASS,True,'ok')])
    def test_hash_stable(self):
        r=self.make(); attach_evidence_hash(r); self.assertEqual(r.evidence_sha256,evidence_hash(r.to_dict()))
    def test_tamper_changes_hash(self):
        r=self.make(); attach_evidence_hash(r); d=copy.deepcopy(r.to_dict()); d['verdict']='BLOCKED'; self.assertNotEqual(r.evidence_sha256,evidence_hash(d))
