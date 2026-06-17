"""User story generator module."""

from spec_harness.models import DomainAnalysis, RequirementSpec, UserStory


class UserStoryGenerator:
    """Generate user stories from requirement spec and domain analysis."""

    # Action words that indicate a user-facing feature
    ACTION_VERBS = {
        "upload",
        "download",
        "preview",
        "view",
        "print",
        "delete",
        "create",
        "update",
        "edit",
        "modify",
        "list",
        "search",
        "find",
        "approve",
        "reject",
        "submit",
        "save",
        "validate",
        "check",
        "notify",
        "record",
        "log",
        "delegate",
        "assign",
        "track",
        "monitor",
        "filter",
        "sort",
        "export",
        "import",
        "share",
        "send",
        "receive",
        "archive",
        "restore",
        "cancel",
        "suspend",
        "resume",
        "activate",
        "deactivate",
        "enable",
        "disable",
        "grant",
        "revoke",
        "add",
        "remove",
        "attach",
        "detach",
        "link",
        "unlink",
        "merge",
        "split",
        "compare",
        "analyze",
        "calculate",
        "generate",
        "schedule",
        "book",
        "reserve",
        "release",
        "transfer",
        "move",
        "copy",
        "clone",
        "duplicate",
    }

    # Words that should NOT be used as roles
    STOP_ROLES = {
        "only",
        "also",
        "even",
        "just",
        "all",
        "each",
        "every",
        "some",
        "any",
        "the",
        "a",
        "an",
        "this",
        "that",
        "these",
        "those",
        "my",
        "your",
        "our",
        "be",
        "have",
        "do",
        "get",
        "make",
        "take",
        "go",
        "come",
        "see",
        "know",
        "think",
        "say",
        "look",
        "want",
        "need",
        "use",
        "work",
        "give",
        "tell",
        "ask",
        "try",
        "feel",
        "become",
        "leave",
        "put",
        "mean",
        "keep",
        "let",
        "begin",
        "seem",
        "help",
        "show",
        "hear",
        "play",
        "run",
        "move",
        "live",
        "believe",
        "bring",
        "happen",
        "write",
        "provide",
        "sit",
        "stand",
        "lose",
        "pay",
        "meet",
        "include",
        "continue",
        "set",
        "learn",
        "change",
        "lead",
        "understand",
        "watch",
        "follow",
        "stop",
        "create",
        "speak",
        "read",
        "allow",
        "add",
        "spend",
        "grow",
        "open",
        "walk",
        "offer",
        "remember",
        "love",
        "consider",
        "appear",
        "buy",
        "wait",
        "serve",
        "die",
        "send",
        "expect",
        "build",
        "stay",
        "fall",
        "cut",
        "reach",
        "kill",
        "remain",
        "suggest",
        "raise",
        "pass",
        "sell",
        "require",
        "report",
        "decide",
        "pull",
        "upload",
        "download",
        "preview",
        "print",
        "delete",
        "edit",
        "update",
        "list",
        "search",
        "find",
        "approve",
        "reject",
        "submit",
        "save",
        "validate",
        "check",
        "notify",
        "record",
        "log",
        "delegate",
    }

    def generate(self, spec: RequirementSpec, domain: DomainAnalysis) -> list[UserStory]:
        stories: list[UserStory] = []
        features = spec.features if spec.features else self._infer_features(domain)

        for idx, feature in enumerate(features, start=1):
            role = self._pick_role(domain, feature, spec)
            action = self._extract_action(feature)
            value = self._infer_value(action, domain)
            title = self._make_title(action)

            stories.append(
                UserStory(
                    id=f"US-{idx:03d}",
                    title=title,
                    role=role,
                    action=action,
                    value=value,
                )
            )

        return stories

    def _infer_features(self, domain: DomainAnalysis) -> list[str]:
        """Infer features from domain operations and objects when no explicit features exist."""
        features = []
        for op in domain.operations[:6]:  # Limit to avoid explosion
            for obj in domain.business_objects[:2]:
                if obj not in self.STOP_ROLES and len(obj) > 3:
                    features.append(f"{op} {obj.replace('_', ' ')}")
        return features if features else ["manage records"]

    def _pick_role(self, domain: DomainAnalysis, feature: str, spec: RequirementSpec) -> str:
        """Select the most appropriate role for a feature."""
        # Try to find role from explicit mentions in requirement
        feature_lower = feature.lower()

        # Look for known roles in the requirement text that relate to this feature
        best_role = None
        for role in domain.roles:
            role_clean = role.replace("_", " ")
            if role in self.STOP_ROLES or len(role) < 3:
                continue
            # Check if role keywords appear near the feature in the raw text
            if any(word in feature_lower for word in role_clean.split()):
                best_role = role_clean
                break

        if best_role:
            return best_role

        # Use a reasonable default role based on feature type
        if any(op in feature_lower for op in ("approve", "reject", "delegate", "authorize")):
            return "authorized user"
        if any(op in feature_lower for op in ("audit", "log", "monitor", "track")):
            return "system administrator"
        if any(op in feature_lower for op in ("create", "update", "delete", "manage")):
            return "business user"
        if any(op in feature_lower for op in ("view", "list", "search", "preview", "download")):
            return "user"

        # Return first valid role from domain
        for role in domain.roles:
            if role not in self.STOP_ROLES and len(role) > 3:
                return role.replace("_", " ")

        return "business user"

    def _extract_action(self, feature: str) -> str:
        """Extract a clean action phrase from a feature description."""
        feature = feature.lower().strip()

        # Remove leading filler phrases
        prefixes = (
            "be able to ",
            "provide ",
            "support ",
            "expose ",
            "record ",
            "enforce ",
            "maintain ",
            "generate ",
            "send ",
            "validate ",
            "check ",
            "have ",
            "use ",
            "get ",
            "make ",
            "take ",
        )
        for prefix in prefixes:
            if feature.startswith(prefix):
                feature = feature[len(prefix) :]

        # Remove trailing filler phrases
        suffixes = (
            " in the system",
            " from the system",
            " to the system",
            " on the system",
            " via the system",
            " through the system",
            " as needed",
            " if needed",
            " when needed",
            " as required",
            " for the business",
            " for business",
            " for the organization",
        )
        for suffix in suffixes:
            if feature.endswith(suffix):
                feature = feature[: -len(suffix)]

        # Clean up the action: ensure it starts with a verb
        words = feature.split()
        if len(words) > 0 and words[0] not in self.ACTION_VERBS:
            # Try to find a verb in the first few words
            for i, word in enumerate(words[:4]):
                if word in self.ACTION_VERBS:
                    words = words[i:]
                    break

        # Remove leading articles
        if words and words[0] in ("a", "an", "the"):
            words = words[1:]

        # Capitalize first letter
        action = " ".join(words).strip()
        if action:
            action = action[0].upper() + action[1:]

        return action

    def _make_title(self, action: str) -> str:
        """Create a concise title from the action."""
        # Limit to first 5-6 words for readability
        words = action.split()
        if len(words) > 6:
            title_words = words[:6]
            title = " ".join(title_words)
        else:
            title = action
        return title

    def _infer_value(self, action: str, domain: DomainAnalysis) -> str:
        """Infer the business value from an action phrase."""
        action_lower = action.lower()

        # Check for specific action patterns
        value_patterns = [
            ("upload", "supporting materials can be stored and reviewed later"),
            ("download", "I can access files offline or share them externally"),
            (
                "preview",
                "I can verify content without downloading or opening in another application",
            ),
            ("delete", "outdated or incorrect files can be removed to keep the system clean"),
            ("print", "physical copies can be produced for signing, filing, or distribution"),
            ("create", "new records can be added to the system and made available to the team"),
            ("update", "information remains accurate and up-to-date for all stakeholders"),
            ("view", "I can access the information I need to make informed decisions"),
            ("list", "I can see all relevant records in one place for overview and management"),
            ("search", "I can quickly find specific records without manual browsing"),
            ("filter", "I can narrow down large datasets to focus on relevant items"),
            ("sort", "I can organize records in a meaningful order for easier analysis"),
            ("approve", "decisions are properly authorized and tracked for accountability"),
            (
                "reject",
                "invalid requests are blocked and returned for correction with clear feedback",
            ),
            ("submit", "requests or documents can be formally sent for processing or review"),
            ("save", "work in progress is preserved and can be resumed later"),
            ("validate", "data integrity is maintained and errors are caught early"),
            (
                "check",
                "conditions or status can be verified before proceeding with dependent actions",
            ),
            (
                "notify",
                "stakeholders are informed of important events without manual communication",
            ),
            (
                "record",
                "a complete history is maintained for compliance, audit, and troubleshooting",
            ),
            ("log", "audit trail is available for accountability and security investigation"),
            (
                "delegate",
                "workflows continue even when primary approvers are unavailable or on leave",
            ),
            ("assign", "work is clearly distributed and ownership is transparent"),
            ("track", "progress and status can be monitored without requesting status updates"),
            ("monitor", "anomalies or issues can be detected early for proactive resolution"),
            ("export", "data can be used in external tools or shared with partners"),
            ("import", "existing data can be migrated or integrated from other systems"),
            ("share", "collaboration is enabled without creating duplicate copies"),
            (
                "archive",
                "old records are preserved but removed from active workflows to reduce clutter",
            ),
            ("restore", "accidentally deleted or modified data can be recovered"),
            ("cancel", "mistaken actions can be undone before they take effect"),
            ("schedule", "tasks or events are planned and reminders are automatic"),
            ("book", "resources or time slots are reserved and conflicts are prevented"),
            ("transfer", "ownership or responsibility can be moved to the right person"),
            ("merge", "related records can be combined to eliminate duplication"),
            ("split", "complex records can be broken down for granular management"),
            ("compare", "differences can be identified for decision-making or reconciliation"),
            ("analyze", "trends and insights can be discovered from accumulated data"),
            ("calculate", "values are computed accurately and consistently"),
            ("generate", "reports, documents, or outputs are produced automatically"),
        ]

        for keyword, value in value_patterns:
            if keyword in action_lower:
                return value

        # Default value based on domain objects
        if domain.business_objects:
            obj = domain.business_objects[0].replace("_", " ")
            return f"the {obj} management process is supported effectively"

        return "the business process is supported effectively"
