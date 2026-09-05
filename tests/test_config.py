import tempfile, unittest
from pathlib import Path
from ga_lab_verify.config import ConfigError, load_config

class ConfigTests(unittest.TestCase):
    def test_valid_config(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'c.toml'; p.write_text('schema_version=1\n[[checks]]\nid="x"\ncommand=["python","-V"]\n')
            c,raw=load_config(p); self.assertEqual(c.checks[0].check_id,'x'); self.assertTrue(raw)
    def test_unknown_schema_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'c.toml'; p.write_text('schema_version=2\n[[checks]]\nid="x"\ncommand=["python","-V"]\n')
            with self.assertRaises(ConfigError): load_config(p)
    def test_duplicate_id_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'c.toml'; p.write_text('schema_version=1\n[[checks]]\nid="x"\ncommand=["a"]\n[[checks]]\nid="x"\ncommand=["b"]\n')
            with self.assertRaises(ConfigError): load_config(p)
