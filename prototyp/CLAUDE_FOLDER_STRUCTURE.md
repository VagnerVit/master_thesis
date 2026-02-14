# .claude Folder Structure

**Location**: `.claude/` (in project root)
**Status**: **Gitignored** (local only, not in repository)

---

## Purpose

The `.claude/` folder contains local Claude Code settings and session data specific to your machine. These files are **not committed to Git** to keep the repository clean and avoid conflicts between different machines/users.

---

## Contents

### Session Data
```
.claude/
├── SESSION_SUMMARY.md          # Quick summary of last session
├── plans/                      # Plan mode files (auto-generated)
│   └── tingly-toasting-pearl.md  # Original implementation plan
├── settings.local.json         # Local Claude Code settings
└── logs/                       # Log files (if enabled)
```

### Key Files

#### `SESSION_SUMMARY.md`
- **Purpose**: Quick reference for last session
- **Created**: Manually by Claude at end of session
- **Content**: What was done, what's next, quick commands
- **Regenerate**: Create manually when needed

#### `plans/*.md`
- **Purpose**: Plan mode files from EnterPlanMode tool
- **Created**: Automatically by Claude Code during planning
- **Content**: Implementation plans, research notes
- **Note**: One plan per planning session

#### `settings.local.json`
- **Purpose**: Local Claude Code configuration
- **Created**: Automatically by Claude Code CLI
- **Content**: CLI preferences, hooks, etc.
- **Don't edit**: Managed by Claude Code itself

#### `logs/` (optional)
- **Purpose**: Application logs for debugging
- **Created**: By src/utils/logging_config.py
- **Location**: `~/.swimath/logs/` (user home, not .claude/)
- **Files**: `swimath.log`, `download.log`, `prepare.log`, `verify.log`

---

## What IS Committed to Git

Even though `.claude/` is gitignored, these related files ARE in the repository:

```
✅ CLAUDE.md                    # Project instructions for Claude
✅ SESSION_HANDOFF.md           # Technical handoff document
✅ TODO.md                      # Task list
✅ PHASE0_DATASET_SETUP.md      # Dataset instructions
✅ .claude/CLAUDE.md (global)   # User's global Claude instructions
```

---

## Setup on New Machine

When you clone the repository on a new machine:

1. **`.claude/` folder will be empty** (gitignored)
2. **Claude Code will auto-create** `settings.local.json`
3. **You can manually create** `SESSION_SUMMARY.md` if needed
4. **Plans will regenerate** when you use plan mode

**No manual setup required** - Claude Code handles it automatically.

---

## Syncing Across Machines

### What Syncs (via Git)
- ✅ Project code and documentation
- ✅ CLAUDE.md (project instructions)
- ✅ SESSION_HANDOFF.md (context for new sessions)
- ✅ TODO.md (task list)

### What Does NOT Sync (local only)
- ❌ `.claude/SESSION_SUMMARY.md` (machine-specific)
- ❌ `.claude/settings.local.json` (personal preferences)
- ❌ `.claude/plans/` (session-specific plans)
- ❌ Logs in `~/.swimath/logs/`

**Recommendation**: Read `SESSION_HANDOFF.md` on new machine to get full context. It contains everything the local `.claude/SESSION_SUMMARY.md` had, but in the repository.

---

## User's Global Instructions

**Location**: `C:\Users\vvagner\.claude\CLAUDE.md` (global, outside project)

This file contains your **global preferences** for all Claude Code projects:
- Coding style (never use `var`, use primary constructors, etc.)
- Git preferences (no co-author tags, no update-database)
- Communication (always Czech, no Claude Code mentions in commits)

**Note**: This is separate from the project-specific `CLAUDE.md` in the repository.

---

## Troubleshooting

### "Where did my SESSION_SUMMARY.md go?"
- It's local only (gitignored)
- When you clone on new machine, it won't be there
- **Solution**: Read `SESSION_HANDOFF.md` instead (in Git)

### "I want to backup my .claude folder"
```bash
# Create backup
cp -r .claude .claude_backup

# Or zip it
zip -r claude_backup.zip .claude
```

### "Can I commit .claude folder?"
- **Not recommended** - it's personal/local
- If you really need to: `git add -f .claude/SESSION_SUMMARY.md`
- **Better**: Put important info in `SESSION_HANDOFF.md` (already in Git)

---

## Summary

```
.claude/              ← LOCAL ONLY (gitignored)
  ├── SESSION_SUMMARY.md    ← Your notes (optional)
  ├── plans/               ← Plan mode files
  └── settings.local.json  ← Claude Code config

Root level:          ← IN GIT (committed)
  ├── CLAUDE.md            ← Project instructions for Claude
  ├── SESSION_HANDOFF.md   ← Technical handoff
  ├── TODO.md              ← Task list
  └── This file            ← Documentation of .claude folder
```

**Key Insight**: `.claude/` is local scratch space. Important info goes in root-level docs (which ARE in Git).

---

_This file is committed to Git to document the gitignored .claude folder_
