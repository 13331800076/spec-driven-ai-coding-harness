# Spec-Driven AI Coding Harness

A lightweight harness for turning product requirements into user stories, acceptance criteria, tests, and implementation tasks for AI-assisted software delivery.

中文定位：构建一个轻量级 AI Coding 工程化 Harness，将原始需求文档自动转化为 User Story、Acceptance Criteria、API Spec、Test Cases、Task Breakdown 和 AI Coding Task，帮助团队把“模糊需求”变成“可开发、可测试、可追踪、可交付”的工程资产。

## 1. 项目要解决的问题

很多团队使用 Claude Code、Codex、Cursor、Cline 做 AI 编程时，最大问题不是模型不会写代码，而是：

- 原始需求太模糊，AI 不知道业务边界。
- 没有 User Story，开发任务不可控。
- 没有 Acceptance Criteria，无法判断 AI 写得对不对。
- 没有测试骨架，AI 代码容易变成“看起来能跑”的一次性代码。
- 需求、设计、测试、代码任务之间断裂。
- AI Coding 过程缺少工程约束，随机性太强。
- 每个人 prompt 不同，交付质量不稳定。

本项目的目标是构建一个轻量 Harness，把 AI Coding 从“聊天式写代码”升级为“规格驱动的工程化交付”。

## 2. 核心理念

普通 AI Coding 流程：

```
需求描述 → 直接让 AI 写代码 → 人工试错 → 修 bug
```

本项目的目标流程：

```
原始需求
  ↓
需求解析
  ↓
User Story
  ↓
Acceptance Criteria
  ↓
Domain Model / API Spec
  ↓
Test Cases
  ↓
Task Breakdown
  ↓
AI Coding Tasks
  ↓
pytest / Playwright 测试骨架
  ↓
实现与验收
```

核心思想：**不要直接让 AI 从需求写代码，而是先让 AI 生成可验证的规格，再基于规格写代码。**

## 3. 适合展示的能力

这个项目用于证明：

- 你理解 AI Coding 的工程化问题。
- 你不是单纯使用 Claude Code，而是能设计 AI Coding Workflow。
- 你能把 DDD、BDD、TDD、SDD 思路融入 AI 编程流程。
- 你能构建结构化输出，包括 Markdown、YAML、测试骨架。
- 你能把需求拆成可执行的开发任务。
- 你能让 AI 生成代码前先生成验收标准和测试。
- 你能设计适合企业软件交付的 AI Coding Harness。

## 4. 目标岗位匹配

这个项目适合投递：

- AI Application Engineer
- AI Agent Engineer
- Developer Productivity Engineer
- AI Coding Engineer
- Applied AI Engineer
- Enterprise AI Engineer
- Software Engineer, AI Tools
- GenAI Engineer
- AI Platform Engineer
- SDLC Automation Engineer

## 5. MVP 功能范围

第一版不要做成复杂平台，先做一个 CLI + 文件输出型 Harness。

MVP 输入：一个需求文档 `requirements.md`

MVP 输出：

```
outputs/
  user_stories.md
  acceptance_criteria.md
  domain_model.yaml
  api_spec.yaml
  test_cases.md
  task_breakdown.yaml
  ai_coding_tasks.md
  pytest_skeleton/
  playwright_skeleton/
```

## 6. 输入示例

输入文件：`examples/requirements/attachment_management.md`

```markdown
# Requirement: Unified Attachment Management

The system should provide a unified attachment management feature across procurement, sales, and inventory modules.

Users should be able to upload, preview, download, print, and delete attachments.

The system should support permission control. Only users with proper permissions can delete or print attachments.

The system should record audit logs for each attachment operation.

The attachment service should expose APIs for upload, download, preview, delete, and list operations.
```

## 7. 输出示例

### 7.1 User Story 输出

```markdown
# User Stories

## US-001: Upload Attachment

As a procurement user,
I want to upload attachments to a business document,
so that supporting materials can be stored and reviewed later.

## US-002: Preview Attachment

As a business user,
I want to preview uploaded attachments,
so that I can verify the file content without downloading it.
```

### 7.2 Acceptance Criteria 输出

```markdown
# Acceptance Criteria

## US-001: Upload Attachment

- Given a user has upload permission
- When the user selects a valid file and submits the upload form
- Then the file should be stored successfully
- And the file metadata should be linked to the business object
- And an audit log should be created
```

### 7.3 API Spec 输出

```yaml
apis:
  - name: upload_attachment
    method: POST
    path: /api/attachments/upload
    request:
      business_object_type: string
      business_object_id: string
      file: binary
    response:
      attachment_id: string
      file_name: string
      status: string
```

### 7.4 Test Cases 输出

```markdown
# Test Cases

## TC-001: Upload attachment successfully

Steps:
1. Login as a user with ATTACHMENT_UPLOAD permission.
2. Open a business document.
3. Upload a valid PDF file.
4. Submit the form.

Expected Result:
- The upload succeeds.
- The attachment appears in the attachment list.
- The audit log records the upload operation.
```

### 7.5 Task Breakdown 输出

```yaml
tasks:
  - id: TASK-001
    title: Implement attachment domain model
    type: backend
    related_user_story: US-001
    acceptance_criteria:
      - AC-001
    estimated_effort: medium
```

### 7.6 AI Coding Task 输出

```markdown
# AI Coding Tasks

## TASK-002: Implement upload attachment API

Context:
The system needs a unified attachment upload API for multiple ERP modules.

Goal:
Implement a POST /api/attachments/upload endpoint.

Requirements:
- Validate business_object_type and business_object_id.
- Save uploaded file metadata.
- Return attachment_id, file_name, and status.
- Create audit log after successful upload.

Acceptance Criteria:
- Upload succeeds for authorized users.
- Invalid file type is rejected.
- Audit log is created.

Testing:
- Add pytest cases for successful upload.
- Add pytest cases for invalid file type.
- Add pytest cases for missing permission.

Instructions for AI Coding Agent:
- Do not modify unrelated modules.
- Add tests before implementation.
- Keep API response format consistent with api_spec.yaml.
```

## 8. 系统架构

```
Requirement Document
        ↓
Requirement Parser
        ↓
Domain Analyzer
        ↓
User Story Generator
        ↓
Acceptance Criteria Generator
        ↓
API Spec Generator
        ↓
Test Case Generator
        ↓
Task Breakdown Generator
        ↓
AI Coding Task Generator
        ↓
Test Skeleton Generator
        ↓
Markdown / YAML / pytest / Playwright Output
```

核心设计：

- 输入：非结构化需求
- 输出：结构化工程资产
- 目标：让 AI Coding 有明确上下文、边界、验收标准和测试约束

## 9. 技术栈

**Backend / CLI**
- Python 3.11+
- Typer
- Pydantic
- PyYAML
- Jinja2
- Rich

**LLM Interface**
- 第一版建议支持两种模式：
  - Rule-based mode：不依赖 API key，使用模板和规则生成基础输出。
  - LLM mode：支持 OpenAI-compatible API，根据 prompt 生成更自然的规格文档。

**Testing**
- pytest
- pytest-cov
- Playwright skeleton generation

**Output Format**
- Markdown
- YAML
- JSON
- pytest skeleton
- Playwright skeleton

**Optional Web UI v2**
- FastAPI
- Streamlit
- React

## 10. 核心模块设计

### 10.1 Requirement Parser

职责：读取需求文档，提取标题、背景、功能点、角色、业务对象、约束，输出结构化 RequirementSpec

数据模型：

```python
class RequirementSpec(BaseModel):
    requirement_id: str
    title: str
    background: str | None
    actors: list[str]
    business_objects: list[str]
    features: list[str]
    constraints: list[str]
    raw_text: str
```

### 10.2 Domain Analyzer

职责：识别业务领域对象、模块、权限、操作、潜在 API

### 10.3 User Story Generator

职责：将需求转成标准 User Story。格式：`As a [role], I want to [action], so that [business value].`

### 10.4 Acceptance Criteria Generator

职责：为每个 User Story 生成 Given/When/Then 验收标准

### 10.5 API Spec Generator

职责：生成初版 API 规格，包含 endpoint、method、request schema、response schema、permission、error codes

### 10.6 Test Case Generator

职责：从 Acceptance Criteria 生成测试用例，覆盖 unit test、API integration test、UI E2E test、permission test、negative test

### 10.7 Test Skeleton Generator

职责：自动生成 pytest / Playwright 测试骨架

### 10.8 AI Coding Task Generator

职责：把任务拆成适合 Codex / Claude Code 执行的小任务，每个任务包含：Context、Goal、Scope、Files to modify、Acceptance Criteria、Test Requirements、Out of scope、Coding Agent Instructions

## 11. CLI 设计

- `spec-harness init`：初始化项目，生成目录结构和配置文件
- `spec-harness generate <requirements.md>`：从需求生成规格文档
- `spec-harness generate-tests <api_spec.yaml>`：生成测试骨架
- `spec-harness validate <outputs/>`：校验规格完整性
- `spec-harness export-agent-tasks <task_breakdown.yaml>`：生成 Codex / Claude Code 任务包

## 12. 配置文件设计

`harness.yaml`：

```yaml
project:
  name: spec-driven-ai-coding-harness
  output_dir: outputs

generation:
  mode: rule_based
  language: en
  output_formats:
    - markdown
    - yaml

llm:
  provider: openai_compatible
  model: gpt-4.1
  base_url: ${OPENAI_BASE_URL}
  api_key: ${OPENAI_API_KEY}

testing:
  generate_pytest: true
  generate_playwright: true

quality_gates:
  require_acceptance_criteria: true
  require_test_cases: true
  require_task_traceability: true
```

## 13. 质量门禁设计

### 13.1 Traceability Check

检查链路：Requirement → User Story → Acceptance Criteria → Test Case → Task → AI Coding Task

### 13.2 Completeness Check

检查：是否缺失角色、业务对象、异常场景、权限规则、测试用例、API response、错误码

### 13.3 AI Coding Safety Check

检查：任务是否过大、是否要求 AI 修改过多无关文件、是否缺少测试、是否缺少验收标准、是否存在模糊描述、是否有明确 out of scope

## 14. Vibe Coding 工程化流程

本项目本身也要按照 Vibe Coding 工程方式开发：

```
Idea → SPEC.md → User Story → Acceptance Criteria → Task Breakdown → Codex / Claude Code → pytest → Manual Review → README Demo
```

开发原则：
- 每个功能先写 User Story
- 每个 User Story 先写 Acceptance Criteria
- 每个模块先写测试
- 每次只让 AI Coding Agent 做一个小任务
- 所有输出必须可追踪
- 所有生成结果必须可校验
- 不追求一开始全自动，先追求稳定闭环

## 15. User Story 拆解

### Epic 1：Requirement Parsing
- US-1.1：读取需求文档
- US-1.2：提取业务元素

### Epic 2：Spec Generation
- US-2.1：生成 User Story
- US-2.2：生成 Acceptance Criteria
- US-2.3：生成 API Spec

### Epic 3：Test Generation
- US-3.1：生成测试用例
- US-3.2：生成 pytest 骨架
- US-3.3：生成 Playwright 骨架

### Epic 4：Task Breakdown
- US-4.1：生成开发任务
- US-4.2：生成 AI Coding Task

### Epic 5：Validation & Quality Gate
- US-5.1：规格链路校验
- US-5.2：AI Coding 任务质量检查
