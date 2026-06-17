"""Requirement parser module."""

import re
from pathlib import Path

from spec_harness.models import RequirementSpec


class RequirementParser:
    """Parse markdown requirement files into structured RequirementSpec."""

    # Common ERP/business roles
    KNOWN_ROLES = {
        "user",
        "admin",
        "manager",
        "sales",
        "procurement",
        "inventory",
        "business_user",
        "authorized_user",
        "system_admin",
        "customer",
        "vendor",
        "supplier",
        "buyer",
        "seller",
        "approver",
        "reviewer",
        "operator",
        "analyst",
        "developer",
        "tester",
        "product_manager",
        "project_manager",
        "team_lead",
        "engineer",
        "consultant",
        "account_manager",
        "support",
        "helpdesk",
        "auditor",
    }

    # Common non-business words that should NOT be objects
    STOP_WORDS = {
        "system",
        "feature",
        "function",
        "functionality",
        "service",
        "application",
        "app",
        "platform",
        "tool",
        "module",
        "component",
        "capability",
        "ability",
        "option",
        "setting",
        "configuration",
        "process",
        "workflow",
        "operation",
        "action",
        "activity",
        "task",
        "data",
        "information",
        "record",
        "entry",
        "item",
        "object",
        "should",
        "must",
        "can",
        "will",
        "would",
        "could",
        "may",
        "only",
        "also",
        "even",
        "just",
        "all",
        "each",
        "every",
        "proper",
        "valid",
        "invalid",
        "correct",
        "incorrect",
        "unified",
        "comprehensive",
        "integrated",
        "advanced",
        "basic",
        "new",
        "existing",
        "current",
        "previous",
        "next",
        "first",
        "last",
        "one",
        "two",
        "multiple",
        "various",
        "different",
        "same",
        "other",
        "supporting",
        "relevant",
        "necessary",
        "required",
        "optional",
    }

    def parse(self, file_path: str) -> RequirementSpec:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Requirement file not found: {file_path}")
        raw_text = path.read_text(encoding="utf-8").strip()
        if not raw_text:
            raise ValueError(f"Requirement file is empty: {file_path}")
        return self._extract(raw_text, path.stem)

    def _extract(self, raw_text: str, filename: str) -> RequirementSpec:
        title = self._extract_title(raw_text) or filename.replace("_", " ").title()
        background = self._extract_background(raw_text)
        actors = self._extract_actors(raw_text)
        features = self._extract_features(raw_text)
        constraints = self._extract_constraints(raw_text)
        business_objects = self._extract_business_objects(raw_text, features)

        return RequirementSpec(
            requirement_id=f"REQ-{filename.upper()}",
            title=title,
            background=background,
            actors=actors,
            business_objects=business_objects,
            features=features,
            constraints=constraints,
            raw_text=raw_text,
        )

    def _extract_title(self, text: str) -> str | None:
        match = re.search(r"^#\s+(.+)", text, re.MULTILINE)
        return match.group(1).strip() if match else None

    def _extract_background(self, text: str) -> str | None:
        paragraphs = re.split(r"\n\s*\n", text)
        for para in paragraphs[1:]:
            para = para.strip()
            if para and not para.startswith("#") and not para.startswith("-"):
                return para
        return None

    def _extract_actors(self, text: str) -> list[str]:
        roles: set[str] = set()

        # Pattern 1: "As a [role]" or "As an [role]"
        for match in re.finditer(
            r"As\s+a[n]?\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+){0,2})", text, re.IGNORECASE
        ):
            role = match.group(1).strip().lower().replace(" ", "_")
            if role and len(role) > 2 and role not in self.STOP_WORDS:
                roles.add(role)

        # Pattern 2: "[Role] should be able to..." or "Users should..."
        for match in re.finditer(
            r"^([A-Z][a-zA-Z]+(?:\s+[a-zA-Z][a-zA-Z]+){0,2})\s+should\s+(?:be\s+)?able\s+to",
            text,
            re.MULTILINE | re.IGNORECASE,
        ):
            role = match.group(1).strip().lower().replace(" ", "_")
            if role and role not in self.STOP_WORDS and len(role) > 2:
                roles.add(role)

        # Pattern 3: "users with [role] permission" or "[role] users"
        for match in re.finditer(r"(\b[a-z]+(?:\s+[a-z]+){0,2})\s+users?\b", text, re.IGNORECASE):
            role = match.group(1).strip().lower().replace(" ", "_")
            if role and role not in self.STOP_WORDS and len(role) > 2:
                roles.add(role)

        # Pattern 4: "Only [role] can..."
        for match in re.finditer(
            r"Only\s+([a-z]+(?:\s+[a-z]+){0,2})\s+(?:can|may|should)", text, re.IGNORECASE
        ):
            role = match.group(1).strip().lower().replace(" ", "_")
            if role and role not in self.STOP_WORDS and len(role) > 2:
                roles.add(role)

        # Fallback: if no roles found, look for known roles in text
        if not roles:
            for known in self.KNOWN_ROLES:
                if re.search(rf"\b{known.replace('_', ' ')}\b", text, re.IGNORECASE) or re.search(
                    rf"\b{known}\b", text, re.IGNORECASE
                ):
                    roles.add(known)

        # Final fallback
        if not roles:
            roles.add("business_user")

        # Normalize and deduplicate
        normalized = set()
        for role in roles:
            # Singularize common plurals
            if role.endswith("s") and role[:-1] in self.KNOWN_ROLES:
                role = role[:-1]
            normalized.add(role)

        return sorted(normalized)

    def _extract_features(self, text: str) -> list[str]:
        features: list[str] = []
        lines = text.splitlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Pattern 1: "Users should be able to [action]"
            match = re.search(r"should\s+be\s+able\s+to\s+(.+)", line, re.IGNORECASE)
            if match:
                actions = match.group(1).strip().rstrip(".")
                # Split compound actions: "upload, preview, download, print, and delete"
                split_actions = self._split_compound_actions(actions)
                for action in split_actions:
                    if action and len(action) > 3:
                        features.append(action)
                continue

            # Pattern 2: "The system should [provide/support/expose/record/enforce] ..."
            match2 = re.search(
                r"should\s+(provide|support|expose|record|enforce|maintain|generate|send|validate|check)\s+(.+)",
                line,
                re.IGNORECASE,
            )
            if match2:
                feature = f"{match2.group(1).strip()} {match2.group(2).strip()}".rstrip(".")
                if feature and len(feature) > 10 and not feature.lower().startswith("provide a"):
                    features.append(feature)

        # Deduplicate and clean - filter out overly long features
        cleaned: list[str] = []
        seen: set[str] = set()
        for f in features:
            f = f.strip()
            if len(f) > 60:  # Too long, probably captured a whole sentence
                continue
            f_lower = f.lower()
            if f_lower not in seen and not any(sw in f_lower for sw in ["should be able to"]):
                seen.add(f_lower)
                cleaned.append(f)

        return cleaned

    def _split_compound_actions(self, text: str) -> list[str]:
        """Split compound actions like 'upload, preview, and delete' into separate items."""
        text = text.rstrip(".")

        # Handle both "and" and ", and" patterns
        parts = re.split(r",\s*and\s*|,\s*|\s+and\s+", text)
        parts = [p.strip() for p in parts if p.strip()]

        # Remove leading "and" from any remaining parts
        parts = [p[4:].strip() if p.lower().startswith("and ") else p for p in parts]

        if len(parts) <= 1:
            return [text]

        # Try to find the common object at the end
        last_part = parts[-1]
        words = last_part.split()
        first_part = parts[0]
        first_words = first_part.split()

        if len(words) > len(first_words):
            obj = " ".join(words[len(first_words) :])
            actions = []
            for part in parts:
                pw = part.split()
                if len(pw) >= len(first_words):
                    action_words = pw[: len(first_words)]
                    action = " ".join(action_words)
                    if obj:
                        action = f"{action} {obj}"
                    actions.append(action)
                else:
                    actions.append(f"{part} {obj}")
            return actions

        return parts

    def _extract_constraints(self, text: str) -> list[str]:
        constraints: list[str] = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            # Look for constraint patterns
            patterns = [
                r"Only\s+.+\s+(?:can|may|should)",
                r"(?:must|should)\s+(?:be|not|go|have|record|support|enforce|validate|check|verify|ensure)",
                r"(?:if|when)\s+.+\s+(?:then|should|must)",
                r"(?:permission|access|authorization|authentication)",
                r"(?:audit|log|track|trace|history)",
                r"(?:validation|validate|verify|check|format|unique|required|mandatory|optional)",
                r"(?:threshold|limit|maximum|minimum|range|size|length)",
                r"(?:not exceed|not less|not more|at least|at most|no more than)",
            ]
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE) and len(line) > 15:
                    constraint = line.lstrip("- ").rstrip(".")
                    if constraint and constraint not in constraints:
                        constraints.append(constraint)
                    break
        return constraints

    def _extract_business_objects(self, text: str, features: list[str]) -> list[str]:
        objects: set[str] = set()

        # Extract from features - find nouns at the end of action phrases
        for feature in features:
            words = feature.split()
            if len(words) >= 2:
                # Try last 1-2 words as potential objects
                for n in (2, 1):
                    if len(words) >= n:
                        candidate = " ".join(words[-n:]).lower().rstrip("s")
                        if (
                            candidate
                            and len(candidate) > 3
                            and candidate not in self.STOP_WORDS
                            and not candidate.endswith(("ing", "ed", "ly"))
                        ):
                            objects.add(candidate.replace(" ", "_"))
                            break

        # Known ERP objects from text
        erp_objects = [
            "attachment",
            "document",
            "file",
            "customer",
            "order",
            "sales_order",
            "purchase_order",
            "invoice",
            "payment",
            "product",
            "inventory",
            "warehouse",
            "user",
            "role",
            "permission",
            "workflow",
            "approval",
            "notification",
            "audit_log",
            "log",
            "quote",
            "contract",
            "supplier",
            "vendor",
            "account",
            "contact",
            "lead",
            "opportunity",
            "ticket",
            "issue",
            "project",
            "task",
            "employee",
            "department",
            "company",
            "organization",
            "team",
            "report",
            "dashboard",
            "metric",
            "kpi",
            "event",
            "calendar",
            "meeting",
            "email",
            "message",
            "comment",
            "note",
            "tag",
            "category",
            "label",
        ]
        for obj in erp_objects:
            if obj.lower() in text.lower() or obj.replace("_", " ").lower() in text.lower():
                objects.add(obj)

        # Remove stop words and invalid objects
        cleaned = {o for o in objects if o not in self.STOP_WORDS and len(o) > 3}
        return sorted(cleaned)
