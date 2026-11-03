"""Command-line interface for Tool Input Fuzzer."""
import argparse
from .fuzzer import ToolFuzzer

def main():
    parser = argparse.ArgumentParser(description="Tool Input Fuzzer CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate fuzzing on sample tool handler")
    args = parser.parse_args()

    schema = {
        "properties": {
            "filename": {"type": "string"},
            "lines": {"type": "integer"}
        }
    }

    # Fragile handler that crashes on null bytes
    def fragile_handler(args):
        fname = args.get("filename", "")
        if chr(0) in fname:
            raise ValueError("Null byte detected in filename!")
        return "OK"

    results = ToolFuzzer.fuzz(fragile_handler, schema)
    print("Fuzzing finished.")
    print("Resilience Score:", results["resilience_score"], "%")
    print(f"Crashes caught: {len(results['crashes'])}")
    for c in results["crashes"]:
        print(f"  Trigger: {c['input']} -> {c['error']}: {c['message']}")

if __name__ == "__main__":
    main()
