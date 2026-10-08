#!/usr/bin/env python3
"""PROOF-01: public, independent teaching replay, NOT private LOCAL_AGENTS code.

The historical case is described publicly, but the implementations below were
written specifically for this showcase. Passing these tests only verifies the
behaviour of this miniature reproduction.
"""

from __future__ import annotations

import ast
import json
import unittest
from dataclasses import dataclass


@dataclass(frozen=True)
class Case:
    request_expression: str
    tool_expression: str | None
    tool_result: int | None
    final_answer: int


CASE_FALSE_ACCEPT = Case(
    request_expression="5 + 6",
    tool_expression="6 * 7",
    tool_result=42,
    final_answer=42,
)


def illustrative_legacy_approval(case: Case) -> bool:
    """Deliberately flawed: checks tool/answer agreement, not task alignment."""
    return case.tool_expression is not None and case.final_answer == case.tool_result


def _calculate(node: ast.AST) -> int:
    """Evaluate only integer constants and +, -, *; never evaluate Python code."""
    if isinstance(node, ast.Expression):
        return _calculate(node.body)
    if isinstance(node, ast.Constant) and type(node.value) is int:
        return node.value
    if isinstance(node, ast.BinOp):
        left, right = _calculate(node.left), _calculate(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
    raise ValueError("Unsupported arithmetic expression")


def illustrative_guarded_approval(case: Case) -> bool:
    """Require correct operation, authentic arithmetic result, and matching answer.

    This is a toy rule for one arithmetic scenario, not a general LLM verifier.
    """
    if case.tool_expression is None or case.tool_result is None:
        return False
    try:
        requested = ast.parse(case.request_expression, mode="eval")
        executed = ast.parse(case.tool_expression, mode="eval")
        expected = _calculate(requested)
        observed = _calculate(executed)
    except (SyntaxError, ValueError, RecursionError):
        return False
    return (
        ast.dump(requested, include_attributes=False)
        == ast.dump(executed, include_attributes=False)
        and expected == observed == case.tool_result == case.final_answer
    )


class Proof01Tests(unittest.TestCase):
    def test_historical_pattern_is_accepted_by_illustrative_old_rule(self):
        self.assertTrue(illustrative_legacy_approval(CASE_FALSE_ACCEPT))

    def test_wrong_operation_is_rejected_by_guarded_rule(self):
        self.assertFalse(illustrative_guarded_approval(CASE_FALSE_ACCEPT))

    def test_correct_operation_is_accepted(self):
        self.assertTrue(
            illustrative_guarded_approval(Case("5 + 6", "5+6", 11, 11))
        )

    def test_correct_answer_from_wrong_operation_is_rejected(self):
        self.assertFalse(
            illustrative_guarded_approval(Case("5 + 6", "12 - 1", 11, 11))
        )

    def test_forged_tool_result_is_rejected(self):
        self.assertFalse(
            illustrative_guarded_approval(Case("5 + 6", "5 + 6", 42, 42))
        )

    def test_answer_does_not_match_tool_result(self):
        self.assertFalse(
            illustrative_guarded_approval(Case("5 + 6", "5 + 6", 11, 42))
        )

    def test_missing_tool_is_rejected(self):
        self.assertFalse(
            illustrative_guarded_approval(Case("5 + 6", None, None, 11))
        )

    def test_non_arithmetic_expression_is_rejected_without_execution(self):
        self.assertFalse(
            illustrative_guarded_approval(Case("5 + 6", "sum([5, 6])", 11, 11))
        )

    def test_malformed_expression_is_rejected(self):
        self.assertFalse(
            illustrative_guarded_approval(Case("5 + 6", "5 +", 11, 11))
        )


def main() -> int:
    old = illustrative_legacy_approval(CASE_FALSE_ACCEPT)
    guarded = illustrative_guarded_approval(CASE_FALSE_ACCEPT)
    print(
        json.dumps(
            {
                "proof": "PROOF-01",
                "kind": "independent_illustrative_reproduction",
                "actual_private_verifier_executed": False,
                "requested_expression": CASE_FALSE_ACCEPT.request_expression,
                "tool_executed_expression": CASE_FALSE_ACCEPT.tool_expression,
                "tool_result": CASE_FALSE_ACCEPT.tool_result,
                "reported_answer": CASE_FALSE_ACCEPT.final_answer,
                "illustrative_legacy_approved": old,
                "illustrative_guarded_approved": guarded,
                "expected": {"legacy": True, "guarded": False},
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if old is True and guarded is False else 1


if __name__ == "__main__":
    raise SystemExit(main())
