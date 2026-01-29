"""
Rule Engine Orchestrator

Runs all rule families against bill and policy.
Pure function: same inputs → same outputs.
"""

from typing import List

from app.models.audit import AuditFlag
from app.models.bill import HospitalBill
from app.models.policy import PolicyData

from . import ped
from . import waiting_period
from . import room_rent
from . import consumables
from . import sub_limits
from . import copay


def run_audit_rules(bill: HospitalBill, policy: PolicyData) -> List[AuditFlag]:
    """
    Execute all audit rules against bill and policy.
    
    This is the only public function of the rule engine.
    It orchestrates all rule families and returns combined flags.
    
    Args:
        bill: Structured hospital bill data
        policy: Structured policy data
    
    Returns:
        List of audit flags (may be empty if no issues found)
    
    Note:
        This function is deterministic. Same inputs will always
        produce the same outputs.
    """
    flags: List[AuditFlag] = []
    
    # Run each rule family
    # Each returns List[AuditFlag], we extend our master list
    
    flags.extend(ped.check_ped(bill, policy))
    flags.extend(waiting_period.check_waiting_period(bill, policy))
    flags.extend(room_rent.check_room_rent(bill, policy))
    flags.extend(consumables.check_consumables(bill, policy))
    flags.extend(sub_limits.check_sub_limits(bill, policy))
    flags.extend(copay.check_copay(bill, policy))
    
    return flags
