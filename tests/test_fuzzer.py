"""Unit tests for ToolFuzzer."""
import unittest
from tool_input_fuzzer.fuzzer import ToolFuzzer

class TestToolFuzzer(unittest.TestCase):
    def test_fuzzer_catches_crashes(self):
        schema = {"properties": {"msg": {"type": "string"}}}
        def buggy(args):
            if "alert" in str(args.get("msg")):
                raise RuntimeError("XSS triggered")
        res = ToolFuzzer.fuzz(buggy, schema)
        self.assertGreater(len(res["crashes"]), 0)
        self.assertTrue(any("XSS triggered" in c["message"] for c in res["crashes"]))

    def test_resilient_handler(self):
        schema = {"properties": {"count": {"type": "integer"}}}
        def safe(args):
            return int(args.get("count") or 0)
        res = ToolFuzzer.fuzz(safe, schema)
        self.assertEqual(len(res["crashes"]), 0)
        self.assertEqual(res["resilience_score"], 100.0)

if __name__ == "__main__":
    unittest.main()
