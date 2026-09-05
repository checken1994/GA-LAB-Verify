import json,subprocess,sys,tempfile,unittest
from pathlib import Path
from ga_lab_verify.config import VerifyConfig,PolicyConfig,CommandCheckConfig
from ga_lab_verify.report import attach_evidence_hash,write_report
from ga_lab_verify.verifier import verify

def git(repo,*args): return subprocess.check_output(['git','-C',str(repo),*args],text=True).strip()

class ShaBindingTests(unittest.TestCase):
    def test_report_binds_exact_head(self):
        with tempfile.TemporaryDirectory() as td:
            repo=Path(td); subprocess.check_call(['git','init','-q','-b','main',str(repo)])
            git(repo,'config','user.email','test@example.invalid'); git(repo,'config','user.name','GA LAB Test')
            (repo/'a.txt').write_text('one\n'); git(repo,'add','a.txt'); git(repo,'commit','-q','-m','one'); x=git(repo,'rev-parse','HEAD')
            c=VerifyConfig(1,PolicyConfig(),(CommandCheckConfig('noop',(sys.executable,'-c','pass')),))
            r=verify(repo,c,b'config'); attach_evidence_hash(r); self.assertEqual(r.tested_sha,x)
            jp,_=write_report(r,repo/'.ga-lab-test'); d=json.loads(jp.read_text()); self.assertEqual(d['tested_sha'],x)
            (repo/'a.txt').write_text('two\n'); git(repo,'add','a.txt'); git(repo,'commit','-q','-m','two'); y=git(repo,'rev-parse','HEAD')
            self.assertNotEqual(d['tested_sha'],y)
