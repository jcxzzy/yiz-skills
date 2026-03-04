---
name: speckit-taskstoissues
description: Convert existing tasks into actionable, dependency-ordered GitHub issues for the feature. Use after tasks are created to create GitHub issues. Requires GitHub repository.
---

# Speckit Taskstoissues


## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").
1. From the executed script, extract the path to **tasks**.
1. Get the Git remote by running:

```bash
git config --get remote.origin.url
```

**ONLY PROCEED TO NEXT STEPS IF THE REMOTE IS A GITHUB URL**

1. For each task in the list, use the GitHub MCP server to create a new issue in the repository that is representative of the Git remote.

**UNDER NO CIRCUMSTANCES EVER CREATE ISSUES IN REPOSITORIES THAT DO NOT MATCH THE REMOTE URL**


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


## Self-Contained Design

This skill is **fully self-contained**:
- All required scripts are in `scripts/` directory
- All templates are in `references/` directory
- No external file dependencies
- Can be shared across projects
- Works in projects without `.github/` or `.specify/` directories

The scripts will create necessary directory structures (`specs/`, etc.) if they don't exist.
