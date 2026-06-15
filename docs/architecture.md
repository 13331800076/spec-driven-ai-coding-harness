# Architecture

## Overview

Spec-Driven AI Coding Harness is a CLI tool that transforms raw requirement documents into structured engineering assets for AI-assisted software delivery.

## System Architecture

```
Requirement Document (.md)
         |
         v
+----------------------------------+
|      Requirement Parser          |
|  - Extract title, actors,        |
|    features, constraints         |
|  - Output: RequirementSpec       |
+----------------------------------+
         |
         v
+----------------------------------+
|      Domain Analyzer             |
|  - Identify operations, objects,   |
|    roles, permissions, modules   |
|  - Output: DomainAnalysis        |
+----------------------------------+
         |
         v
+----------------------------------+
|    Spec Generators (parallel)    |
|  - User Story Generator          |
|  - Acceptance Criteria Generator |
|  - API Spec Generator            |
|  - Test Case Generator           |
+----------------------------------+
         |
         v
+----------------------------------+
|    Task Generators               |
|  - Task Breakdown Generator      |
|  - AI Coding Task Generator      |
+----------------------------------+
         |
         v
+----------------------------------+
|    Test Skeleton Generators      |
|  - pytest Generator              |
|  - Playwright Generator          |
+----------------------------------+
         |
         v
+----------------------------------+
|    Validators                    |
|  - Traceability Validator        |
|  - Quality Gate                  |
+----------------------------------+
         |
         v
+----------------------------------+
|    Renderers                     |
|  - Markdown Renderer (Jinja2)    |
|  - YAML Renderer                 |
+----------------------------------+
         |
         v
    outputs/
```

## Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `parser` | Read and parse markdown requirement files |
| `analyzer` | Extract domain elements (roles, objects, permissions) |
| `generators` | Transform specs into stories, criteria, APIs, tests, tasks |
| `testgen` | Generate pytest and Playwright skeletons |
| `validators` | Check traceability and quality gates |
| `renderers` | Render outputs using Jinja2 templates |
| `cli` | Typer-based CLI interface |

## Data Flow

1. Raw requirement → `RequirementParser` → `RequirementSpec`
2. `RequirementSpec` → `DomainAnalyzer` → `DomainAnalysis`
3. `RequirementSpec` + `DomainAnalysis` → `UserStoryGenerator` → `UserStory[]`
4. `UserStory[]` → `AcceptanceCriteriaGenerator` → `AcceptanceCriteriaGroup[]`
5. `DomainAnalysis` + `UserStory[]` → `ApiSpecGenerator` → `ApiSpec[]`
6. `AcceptanceCriteriaGroup[]` + `ApiSpec[]` → `TestCaseGenerator` → `TestCase[]`
7. `UserStory[]` + `AcceptanceCriteriaGroup[]` + `ApiSpec[]` + `TestCase[]` → `TaskBreakdownGenerator` → `Task[]`
8. `Task[]` → `AgentTaskGenerator` → `AiCodingTask[]`
9. `ApiSpec[]` → `PytestGenerator` → `pytest/` skeleton
10. `UserStory[]` → `PlaywrightGenerator` → `playwright/` skeleton
11. All artifacts → `TraceabilityValidator` + `QualityGate` → `ValidationReport`
