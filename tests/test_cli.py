import shutil
import unittest
from pathlib import Path

from repocheck.core import audit_source
from repocheck.core import write_html_report
from repocheck.core import write_json_report

FIXTURE = Path(__file__).parent / "fixtures" / "sample_project"


class AuditTests(unittest.TestCase):
    def test_static_audit_finds_expected_rules(self):
        report = audit_source(str(FIXTURE))
        rule_ids = {item.rule_id for item in report.findings}
        self.assertIn("ENV001", rule_ids)
        self.assertIn("DATA001", rule_ids)
        self.assertIn("CFG001", rule_ids)
        self.assertIsNotNone(report.recipe)
        self.assertIn("train.py", report.recipe.command)

    def test_report_writers_and_smoke(self):
        report = audit_source(str(FIXTURE), mode="smoke")
        self.assertIsNotNone(report.smoke)
        output_dir = Path(__file__).parent / "_tmp_output"
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path = output_dir / "report.json"
        html_path = output_dir / "report.html"
        write_json_report(report, json_path)
        write_html_report(report, html_path)
        self.assertTrue(json_path.exists())
        self.assertTrue(html_path.exists())


if __name__ == "__main__":
    unittest.main()
