"""
Rule Engine Package

Deterministic, repeatable business logic for insurance claim auditing.
NO AI. NO ML. NO guessing.

Same input → same output. Always.
"""

from .engine import run_audit_rules

__all__ = ["run_audit_rules"]
