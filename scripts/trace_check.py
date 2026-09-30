#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", required=True)
    parser.add_argument("--tests", required=True)
    parser.add_argument("--results", required=True)
    args = parser.parse_args()

    trace = load_json(args.trace)
    tests = load_json(args.tests)["tests"]
    results = load_json(args.results)["results"]

    design_version = trace["design_version"]
    commit = trace["commit"]
    test_ids = {t["test_id"] for t in tests}
    result_by_test = {r["test_id"]: r for r in results}
    linked_tests = set()
    findings = []

    for item in trace["items"]:
        design_id = item["design_id"]
        vcs = item.get("verification_conditions", [])
        if not vcs:
            findings.append({
                "severity": "error",
                "code": "NO_VERIFICATION_CONDITION",
                "design_id": design_id,
                "message": "design item has no verification condition"
            })
            continue
        for vc in vcs:
            if not vc.get("test_ids"):
                findings.append({
                    "severity": "error",
                    "code": "NO_TEST_LINK",
                    "design_id": design_id,
                    "condition_id": vc["condition_id"],
                    "message": "verification condition has no linked test"
                })
            for test_id in vc.get("test_ids", []):
                linked_tests.add(test_id)
                if test_id not in test_ids:
                    findings.append({
                        "severity": "error",
                        "code": "MISSING_TEST",
                        "design_id": design_id,
                        "condition_id": vc["condition_id"],
                        "test_id": test_id,
                        "message": "linked test is not in test inventory"
                    })
                    continue
                result = result_by_test.get(test_id)
                if result is None:
                    findings.append({
                        "severity": "error",
                        "code": "NO_RESULT",
                        "design_id": design_id,
                        "condition_id": vc["condition_id"],
                        "test_id": test_id,
                        "message": "linked test has no execution result"
                    })
                    continue
                if result["commit"] != commit:
                    findings.append({
                        "severity": "error",
                        "code": "STALE_COMMIT",
                        "design_id": design_id,
                        "test_id": test_id,
                        "expected": commit,
                        "actual": result["commit"]
                    })
                if result["design_version"] != design_version:
                    findings.append({
                        "severity": "error",
                        "code": "STALE_DESIGN_VERSION",
                        "design_id": design_id,
                        "test_id": test_id,
                        "expected": design_version,
                        "actual": result["design_version"]
                    })
                if result["status"] != "passed":
                    findings.append({
                        "severity": "error",
                        "code": "RESULT_NOT_PASSED",
                        "design_id": design_id,
                        "test_id": test_id,
                        "status": result["status"]
                    })
            if vc.get("status") == "candidate":
                findings.append({
                    "severity": "warning",
                    "code": "CANDIDATE_LINK",
                    "design_id": design_id,
                    "condition_id": vc["condition_id"],
                    "message": "link requires human approval"
                })

    for test_id in sorted(test_ids - linked_tests):
        findings.append({
            "severity": "warning",
            "code": "ORPHAN_TEST",
            "test_id": test_id,
            "message": "test exists but is not linked from trace table"
        })

    print(json.dumps({"findings": findings}, ensure_ascii=False, indent=2))
    return 1 if any(f["severity"] == "error" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
