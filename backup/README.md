# backup (Module 9)

Automated periodic backup of the graph data that ISN'T already safe in
git — `graphify-out/graph.json` is fine, it's public and already
committed/pushed on every module's own merge. What actually needs a
separate backup is exactly what Module 4 deliberately kept **out** of
git: `graphify-out/private-nodes.enc.json` (the encrypted private-node
store) and `.env` (holds `ULTRON_GRAPH_ENCRYPTION_KEY`, the only thing
that can decrypt it). Losing both together means losing every private
node's content permanently — Module 4's own docs already say there's no
recovery path if the key is lost, which is exactly the scenario this
module exists to prevent.

## What's backed up, and where

`backup/backup_graph_data.py` zips:
- `graphify-out/private-nodes.enc.json`
- `.env`
- `graph-schema/.node_history.json` (already git-tracked, included
  anyway so one restore recovers a fully consistent set in one step)

into `C:\Ultron Project\_backups\graph-data\graph-data-<timestamp>.zip`
— a sibling of the git repo root (`C:\Ultron Project\Ultron Project\`),
same pattern `_archive\` next to it already uses. **Genuinely separate
from GitHub**: this directory is never inside the repo, never staged,
never pushed.

Never reads or prints `.env`'s contents — copies it as a file
(`shutil.copy` semantics via `zipfile`), the same way any real backup
tool handles a file it doesn't need to understand.

Rotated to the most recent 10 backups (`KEEP_LAST_N`) so this doesn't
grow unbounded — a real safeguard, not just a comment, verified in
`test_backup_restore.py`.

## Automated (real, not just documented)

A Windows Scheduled Task, `UltronGraphDataBackup`, runs
`backup_graph_data.py` daily at 3:00 AM. Registered with
`Register-ScheduledTask` (not just written about) and **triggered once
manually to confirm it actually completes successfully end-to-end** —
`Get-ScheduledTaskInfo` showed `LastTaskResult: 0` (success) and a real
new backup zip appeared, proving the whole chain (Task Scheduler →
`python.exe` → this script → a real file on disk), not just that
registration succeeded.

Check/modify/remove it:
```powershell
Get-ScheduledTask -TaskName "UltronGraphDataBackup" | Get-ScheduledTaskInfo
Unregister-ScheduledTask -TaskName "UltronGraphDataBackup" -Confirm:$false   # to remove it
```

## "Confirm restore actually works, don't just assume it" (step 33)

The strong proof, not the weak one. A weak test checks that restored
files exist with the right names. `test_backup_restore.py`'s real
round-trip test:
1. Backs up the **real** project's `private-nodes.enc.json` + `.env`.
2. Restores them into an **isolated temp directory** (never touches the
   real repo).
3. **Decrypts a real private node using ONLY the restored copies** —
   reads the key back out of the restored `.env`, decrypts from the
   restored store, and asserts the result is byte-for-byte identical to
   decrypting the same node from the live files.

If backup or restore had silently truncated or corrupted anything, this
fails. A file-existence check would not have caught that — this is the
actual bar step 33 asks for, not a lower one that happens to pass.

Rotation is verified separately (fill past `keep_last_n`, assert only
the most recent N remain).

## Usage

```
python backup/backup_graph_data.py                    # manual backup (also runs daily via the scheduled task)
python backup/restore_graph_data.py                    # restores the latest backup into this repo (asks before overwriting)
python backup/restore_graph_data.py --zip <path> --to <dir>   # restore a specific backup elsewhere
```

## Known limitations — not solved tonight

- **Single machine, single disk.** `_backups\graph-data\` is still on
  the same physical disk as the repo itself — protects against
  accidental deletion, a bad `git clean`, or this checkout getting
  corrupted, but not against actual disk failure. A real off-machine
  destination (another drive, cloud storage, a second machine) is a
  reasonable next step, not built tonight — scope was "separate from
  GitHub," which this satisfies, not "separate from this computer."
- **No backup of the working `graphify-out/` state beyond what's
  already in git** (graph.json, obsidian/, etc.) — that's already
  protected by being committed on every module's merge, so a second
  backup of it here would be redundant, not missing.
- **The scheduled task runs as whatever user context registered
  it** (this session's) — worth checking `Get-ScheduledTask` after any
  Windows user-account changes on this machine, since a scheduled task
  can silently stop running if the account it's tied to changes state.
