---
name: speckit-plan
description: Execute the implementation planning workflow using the plan template to generate design artifacts. Use after spec is clarified to create technical implementation plan.
---

# Speckit Plan


## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/setup-plan.ps1 -Json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType copilot`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications


---

## Bundled Resources

### Scripts Directory (`scripts/`)

This skill includes complete PowerShell scripts for speckit operations:

- **common.ps1**: Common functions (Get-RepoRoot, Get-CurrentBranch, etc.)
- **check-prerequisites.ps1**: Validate prerequisites and return feature paths
- **create-new-feature.ps1**: Create new feature branch and directory
- **setup-plan.ps1**: Setup implementation plan
- **update-agent-context.ps1**: Update agent context files

**Usage**: These scripts are self-contained and can be run directly from the skill directory.

```powershell
# Run with JSON output (recommended for programmatic use)
./scripts/check-prerequisites.ps1 -Json

# Run interactively
./scripts/create-new-feature.ps1 "Feature description"
```

### References Directory (`references/`)

Template files used by speckit commands:

- **spec-template.md**: Feature specification structure
- **plan-template.md**: Implementation plan structure  
- **tasks-template.md**: Task list format
- **checklist-template.md**: Quality checklist structure
- **agent-file-template.md**: Agent context file template

- **constitution-example.md**: Example project constitution
- **constitution-template.md**: Constitution template structure


## Recommended Next Steps

After completing this command, consider:
- `speckit-tasks`: Follow-up workflow step
- `speckit-checklist`: Follow-up workflow step


## Self-Contained Design

This skill is **fully self-contained**:
- All required scripts are in `scripts/` directory
- All templates are in `references/` directory
- No external file dependencies
- Can be shared across projects
- Works in projects without `.github/` or `.specify/` directories

The scripts will create necessary directory structures (`specs/`, etc.) if they don't exist.
