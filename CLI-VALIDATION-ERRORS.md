# CLI Documentation Errors: YAML vs Actual CLI

**Generated**: 2026-04-27  
**Source**: `scripts/validate_yaml_vs_clidoc.py`

## Summary

The current YAML-based command documentation (`config/commands/*.yaml`) contains **20 options that do not exist in the actual CLI** (as reported by cli-doc from Cobra).

These are **real documentation errors** where the docs describe CLI options that users cannot actually use.

---

## The 20 Errors

### connector commands (4 errors)

1. **`connector create`** - Option `name` documented but doesn't exist in CLI
2. **`connector create`** - Option `port` documented but doesn't exist in CLI  
3. **`connector update`** - Option `name` documented but doesn't exist in CLI
4. **`connector update`** - Option `port` documented but doesn't exist in CLI

### debug commands (1 error)

5. **`debug dump`** - Option `file` documented but doesn't exist in CLI

### link commands (1 error)

6. **`link status`** - Option `name` documented but doesn't exist in CLI

### listener commands (5 errors)

7. **`listener create`** - Option `name` documented but doesn't exist in CLI
8. **`listener create`** - Option `port` documented but doesn't exist in CLI
9. **`listener update`** - Option `name` documented but doesn't exist in CLI
10. **`listener status`** - Option `name` documented but doesn't exist in CLI
11. **`listener status`** - Option `port` documented but doesn't exist in CLI

### site commands (4 errors)

12. **`site create`** - Option `name` documented but doesn't exist in CLI
13. **`site update`** - Option `name` documented but doesn't exist in CLI
14. **`site status`** - Option `name` documented but doesn't exist in CLI
15. **`site delete`** - Option `name` documented but doesn't exist in CLI

### system commands (1 error)

16. **`system dump`** - Option `bundle-file` documented but doesn't exist in CLI

### token commands (4 errors)

17. **`token create`** - Option `grant` documented but doesn't exist in CLI
18. **`token create`** - Option `file` documented but doesn't exist in CLI
19. **`token issue`** - Option `file` documented but doesn't exist in CLI
20. **`token issue`** - Option `link-cost` documented but doesn't exist in CLI

---

## Impact

**User Impact**: HIGH  
Users reading the documentation will see options that don't work when they try to use them.

**Maintenance**: This proves the current YAML-based approach is out of sync with the actual CLI code.

---

## Root Cause

The YAML files (`config/commands/*.yaml`) are **manually maintained** and separate from the actual CLI code. When CLI options are:
- Removed from the CLI code
- Renamed in the CLI code  
- Never implemented despite being planned

...the YAML documentation doesn't automatically update, leading to these errors.

---

## Solution

The proposed **cli-doc + metadata merge approach** would eliminate these errors automatically because:

1. **cli-doc** is generated directly from the Cobra CLI code (source of truth)
2. The merge logic would only use options that **actually exist** in cli-doc
3. Phantom options in metadata would be caught by validation
4. When CLI changes, cli-doc updates automatically → docs update automatically

---

## To Run Validation Yourself

```bash
cd /home/paulwright/repos/sk/refdog
source venv/bin/activate
python scripts/validate_yaml_vs_clidoc.py
```

**Full output**: 136 total issues (20 warnings + 116 info items about inherited options)

---

## Related Files

- **Validation script**: `scripts/validate_yaml_vs_clidoc.py`
- **Validation summary**: `VALIDATION-SUMMARY.md`
- **Implementation plan**: `COMMAND-MERGE-IMPLEMENTATION.md`
- **Current YAML files**: `config/commands/*.yaml` (old system, has these errors)
- **CLI-doc files**: `cli-doc/*.md` (authoritative, from actual CLI)
