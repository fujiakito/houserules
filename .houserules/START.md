# Execute a bounded task

Read the project's instructions first. Load only the chosen skill and current task inputs;
do not load the distribution's GUIDE, inventories or research as routine context.

For a small edit, do the work and run its required checks. For repeated verification or a task
that will resume, use the local workflow tool:

1. Define the required outcome and exact input/code files. Preserve the user's selected model.
2. Start once: `python .houserules/workflow.py start <id> --task "<outcome>" --target <file>`.
   Repeat --target for relevant files. Defaults: 3 command runs, 300 total execution seconds;
   pass --max-runs/--max-seconds for the task's agreed budget. Missing future files are allowed.
3. Execute a required check: `python .houserules/workflow.py run <id> -- <executable> <args>`.
   Inspect its log and exit status against the task criterion. Exit zero alone is not task acceptance.
4. Before resuming or claiming a prior pass, run `python .houserules/workflow.py status <id>`.
   Changed tracked inputs or log bytes invalidate the recorded pass. Recheck affected behavior.
5. On repeated blockers or exhausted budget, record what changed and the next owner/action in
   the existing work record. Do not create another task id merely to evade the budget.

workflow.json retains command attempts, target hashes, logs, elapsed time and raw reported usage.
Unknown tokens/cost remain unknown. This tool bounds commands invoked through it; it does not
meter the surrounding chat, prove semantic correctness, or enforce provider spending limits.
Use short-lived checks: a timeout stops the direct child, not necessarily detached descendants.
Do not put credentials in argv or logs. No background worker, hook, MCP or external write is enabled.
