"""API spec generator module."""

from spec_harness.models import ApiSpec, DomainAnalysis, RequirementSpec, UserStory


class ApiSpecGenerator:
    """Generate API specifications from domain analysis and user stories."""

    # HTTP method mapping for operations
    METHOD_MAP = {
        "create": "POST",
        "upload": "POST",
        "submit": "POST",
        "save": "POST",
        "update": "PUT",
        "edit": "PUT",
        "delete": "DELETE",
        "approve": "POST",
        "reject": "POST",
        "delegate": "POST",
        "view": "GET",
        "preview": "GET",
        "download": "GET",
        "list": "GET",
        "search": "GET",
        "find": "GET",
        "check": "GET",
        "validate": "POST",
        "notify": "POST",
        "record": "POST",
        "log": "POST",
    }

    def generate(
        self, spec: RequirementSpec, domain: DomainAnalysis, stories: list[UserStory]
    ) -> list[ApiSpec]:
        apis: list[ApiSpec] = []
        objects = domain.business_objects if domain.business_objects else ["resource"]
        operations = (
            domain.operations
            if domain.operations
            else ["list", "create", "view", "update", "delete"]
        )

        for _idx, operation in enumerate(operations, start=1):
            for obj in objects[:3]:  # Limit to avoid explosion
                obj_slug = obj.replace(" ", "_").lower()
                obj_path = obj.replace(" ", "-").lower()
                method = self.METHOD_MAP.get(operation, "POST")
                path = self._build_path(method, obj_path, operation)
                permission = f"{obj_slug.upper()}_{operation.upper()}"
                request_schema = self._build_request_schema(method, obj)
                response_schema = self._build_response_schema(method, obj)
                error_codes = self._build_error_codes(method)

                apis.append(
                    ApiSpec(
                        name=f"{operation}_{obj_slug}",
                        method=method,
                        path=path,
                        permission_required=permission,
                        request_schema=request_schema,
                        response_schema=response_schema,
                        error_codes=error_codes,
                    )
                )

        return apis

    def _build_path(self, method: str, obj: str, operation: str) -> str:
        if method in ("GET", "DELETE") and operation not in ("list", "search"):
            return f"/api/{obj}s/{{{obj}_id}}"
        if operation in ("list", "search"):
            return f"/api/{obj}s"
        return f"/api/{obj}s/{operation}"

    def _build_request_schema(self, method: str, obj: str) -> dict:
        if method == "GET":
            return {"page": "integer", "page_size": "integer"}
        if "delete" in obj.lower():
            return {}
        return {
            f"{obj}_id": "string",
            "data": "object",
            "file": "binary",
        }

    def _build_response_schema(self, method: str, obj: str) -> dict:
        schema = {"status": "string", "message": "string"}
        if method == "GET":
            schema[f"{obj}"] = "object"
            schema["items"] = "list"
        return schema

    def _build_error_codes(self, method: str) -> list[str]:
        codes = ["400", "401", "403", "500"]
        if method == "GET":
            codes.append("404")
        return codes
