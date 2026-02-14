from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List
import yaml

@dataclass(frozen=True)
class Requirement:
    id: str
    title: str
    severity: str
    check: Dict[str, Any]
    
@dataclass(frozen=True)
class Policy:
    profile_id: str
    profile_version: str
    target: str
    requirements: List[Requirement]
    
    
def load_policy_from_yaml(file_path: str) -> Policy:
    with open(file_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
        
    profile = raw.get("profile", {})
    reqs = raw.get("requirements", [])
    
    
    profile_id = profile.get("id")
    profile_version = profile.get("version")
    profile_target = profile.get("target")
    
    if not profile_id:
        raise ValueError("Profile ID is required in the policy YAML.")
    if not isinstance(reqs, list) or not reqs:
        raise ValueError("Requirements must be a list in the policy YAML.")
    
    requirements: List[Requirement] = []
    
    seen = set()
    for r in reqs:
        rid = r.get("id")
        title = r.get("title", "")
        severity = r.get("severity", "low")
        check = r.get("check")
        
    
        if not rid:
            raise ValueError("Each requirement must have an ID.")
        if rid in seen:
            raise ValueError(f"Duplicate requirement ID found: {rid}")
        if not isinstance(check, dict) or "type" not in check:
            raise ValueError(f"Requirement {rid} missing check.type")
        
        seen.add(rid)
        requirements.append(Requirement(id=rid, title=title, severity=severity, check=check))

    return Policy(
            profile_id=profile_id,
            profile_version=profile_version,
            target=profile_target,
            requirements=requirements,
        )
    
if __name__ == "__main__":
    policy = load_policy_from_yaml("policies/baseline_l1.yaml")
    print(policy.requirements[0].check)
