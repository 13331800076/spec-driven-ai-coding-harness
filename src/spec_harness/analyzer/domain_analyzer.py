"""Domain analyzer module."""

import re
from typing import List, Set

from spec_harness.models import RequirementSpec, DomainAnalysis


class DomainAnalyzer:
    """Analyze requirements to extract domain elements."""

    # Common operation keywords mapped to standardized operations
    OPERATION_KEYWORDS = {
        "upload": "upload",
        "download": "download",
        "preview": "preview",
        "view": "view",
        "print": "print",
        "delete": "delete",
        "create": "create",
        "update": "update",
        "edit": "update",
        "modify": "update",
        "list": "list",
        "search": "search",
        "find": "search",
        "approve": "approve",
        "reject": "reject",
        "submit": "submit",
        "save": "save",
        "validate": "validate",
        "check": "check",
        "notify": "notify",
        "record": "record",
        "log": "log",
        "delegate": "delegate",
    }

    # Permission patterns
    PERMISSION_PREFIXES = [
        "ATTACHMENT", "CUSTOMER", "ORDER", "USER", "SALES", "INVENTORY",
        "PURCHASE", "PRODUCT", "WORKFLOW", "APPROVAL", "INVOICE", "PAYMENT",
    ]

    def analyze(self, spec: RequirementSpec) -> DomainAnalysis:
        """Analyze a requirement spec and return domain analysis."""
        text = spec.raw_text
        operations = self._extract_operations(text)
        permissions = self._extract_permissions(text, operations, spec.business_objects)
        roles = self._extract_roles(text, spec.actors)
        modules = self._extract_modules(text)
        objects = self._extract_business_objects(text, spec.business_objects)
        constraints = self._extract_constraints(text, spec.constraints)

        return DomainAnalysis(
            modules=modules,
            business_objects=objects,
            roles=roles,
            permissions=permissions,
            operations=operations,
            constraints=constraints,
        )

    def _extract_operations(self, text: str) -> List[str]:
        operations: Set[str] = set()
        for keyword, standard in self.OPERATION_KEYWORDS.items():
            if re.search(rf"\b{keyword}\b", text, re.IGNORECASE):
                operations.add(standard)
        return sorted(operations)

    def _extract_permissions(self, text: str, operations: List[str], objects: List[str]) -> List[str]:
        permissions: Set[str] = set()
        # Look for explicit permission mentions
        for match in re.finditer(r"([A-Z_]+_PERMISSION|[A-Z_]+_DELETE|[A-Z_]+_UPLOAD|[A-Z_]+_VIEW)", text):
            permissions.add(match.group(1))
        # Generate inferred permissions from operations + objects
        for obj in objects:
            obj_upper = obj.upper().replace(" ", "_")
            for op in operations:
                op_upper = op.upper()
                permissions.add(f"{obj_upper}_{op_upper}")
        return sorted(permissions)

    def _extract_roles(self, text: str, actors: List[str]) -> List[str]:
        roles: Set[str] = set(actors)
        # Common role patterns
        role_patterns = [
            r"\b(sales\s+manager|sales\s+representative|regional\s+director|vp\s+of\s+sales|system\s+admin|business\s+user|procurement\s+user|authorized\s+user)\b",
            r"\b([a-z]+\s+manager|[a-z]+\s+admin|[a-z]+\s+user)\b",
        ]
        for pattern in role_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                role = match.group(1).strip().lower().replace(" ", "_")
                if role:
                    roles.add(role)
        # Map generic actors to roles
        if "user" in roles and len(roles) == 1:
            roles.add("business_user")
        return sorted(roles)

    def _extract_modules(self, text: str) -> List[str]:
        modules: Set[str] = set()
        module_keywords = [
            "procurement", "sales", "inventory", "customer", "order",
            "purchase", "warehouse", "finance", "hr", "support",
        ]
        for keyword in module_keywords:
            if re.search(rf"\b{keyword}\b", text, re.IGNORECASE):
                modules.add(keyword)
        return sorted(modules)

    def _extract_business_objects(self, text: str, spec_objects: List[str]) -> List[str]:
        objects: Set[str] = set(spec_objects)
        # Look for noun phrases
        for match in re.finditer(r"\b([a-z]+\s+(?:log|record|document|object|item|entry|history))\b", text, re.IGNORECASE):
            objects.add(match.group(1).lower().replace(" ", "_"))
        return sorted(objects)

    def _extract_constraints(self, text: str, spec_constraints: List[str]) -> List[str]:
        constraints: Set[str] = set(spec_constraints)
        # Extract constraint patterns
        for match in re.finditer(r"(?:only|must|should|if|when)\s+.+?(?:\.\n|\.\s+|$)", text, re.IGNORECASE):
            sentence = match.group(0).strip()
            if len(sentence) > 20 and len(sentence) < 200:
                constraints.add(sentence.rstrip("."))
        return sorted(constraints)
