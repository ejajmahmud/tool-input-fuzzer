"""Automated property-based fuzzing engine for agent tool parameters."""
from typing import Dict, Any, List, Callable


class ToolFuzzer:
    MUTATIONS_STRING = [
        "",
        "A" * 10000,
        "\x00nullbyte",
        "../../etc/passwd",
        "<script>alert(1)</script>",
        "🔥🚀✨🤖",
        "\n\r\t\b",
        "'" + " OR 1=1 --",
    ]
    MUTATIONS_INT = [0, -1, 2147483647, -2147483648, 999999999999999999]
    MUTATIONS_BOOL = [True, False, None, "true"]

    @classmethod
    def generate_inputs(cls, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        props = schema.get("properties", {})
        cases: List[Dict[str, Any]] = []

        # Generate base case with empty
        cases.append({k: "" for k in props})

        for prop_name, prop_def in props.items():
            p_type = prop_def.get("type", "string")
            if p_type == "string":
                for val in cls.MUTATIONS_STRING:
                    cases.append({prop_name: val})
            elif p_type in ("integer", "number"):
                for val in cls.MUTATIONS_INT:
                    cases.append({prop_name: val})
            elif p_type == "boolean":
                for val in cls.MUTATIONS_BOOL:
                    cases.append({prop_name: val})

        return cases

    @classmethod
    def fuzz(cls, handler: Callable[[Dict[str, Any]], Any], schema: Dict[str, Any]) -> Dict[str, Any]:
        cases = cls.generate_inputs(schema)
        crashes = []
        passed = 0

        for case in cases:
            try:
                handler(case)
                passed += 1
            except Exception as e:
                crashes.append({
                    "input": case,
                    "error": type(e).__name__,
                    "message": str(e)
                })

        return {
            "total_cases": len(cases),
            "passed": passed,
            "crashes": crashes,
            "resilience_score": round((passed / len(cases)) * 100, 2) if cases else 100.0
        }
