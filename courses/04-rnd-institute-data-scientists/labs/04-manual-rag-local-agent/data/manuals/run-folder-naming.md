# Run-folder naming (synthetic)

Teaching convention for a fictional sequencing core. Not a real institute document. No instrument recipes.

## Pattern

`YYYYMMDD_SYNTHCORE_<instrument-id>_<run-id>`

Example: `20260817_SYNTHCORE_NS500_RUN0041`

## Rules

- Date is the day the run *folder* was created, not the day samples arrived.
- `instrument-id` is a short token from the door label (letters and digits only).
- Never put a collaborator name or a disease word in the folder name.
- Downstream Nextflow `-resume` points at this folder; renaming after start is a human change, not an agent change.
