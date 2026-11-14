def rejection_log_md(log: dict) -> str:
    L = [f"# Rejection log - {log['topic']}", "",
         f"- **Run:** `{log['run_id']}`",
         f"- **Final status:** **{log['status']}** (attempt {log['final_attempt']} of max {log['max_retries'] + 1})",
         f"- **Generator:** `{log['generator_model']}`  |  **Judge:** `{log['judge_model']}`  |  LLM calls: {log['llm_calls']}",
         ""]
    if log["learned_rules_used"]:
        L += ["**Rules learned from earlier runs (added to the writer prompt):**", ""]
        L += [f"  {r}" for r in log["learned_rules_used"]] + [""]
    L += ["## Score per attempt", "", "| Check | " + " | ".join(f"Attempt {a['attempt']}" for a in log["attempts"]) + " |",
          "|---|" + "---|" * len(log["attempts"])]
    ids = [r["id"] for r in log["attempts"][0]["results"]]
    for cid in ids:
        row = []
        for a in log["attempts"]:
            r = next(x for x in a["results"] if x["id"] == cid)
            row.append("PASS" if r["passed"] else "**FAIL**")
        L.append(f"| {cid} | " + " | ".join(row) + " |")
    L.append("| **Total** | " + " | ".join(f"**{a['score']}**" for a in log["attempts"]) + " |")
    L.append("")
    for a in log["attempts"]:
        verdict = "PASSED - shipped" if a["passed"] else "REJECTED"
        L += [f"## Attempt {a['attempt']} - {verdict} ({a['score']})", ""]
        if a["injected_error"]:
            L += [f"> **Deliberate error injected for testing:** {a['injected_error']}", ""]
        if a["changes_requested"]:
            L += ["**What changed on this retry (feedback sent to the writer):**", "", "```"] + a["changes_requested"] + ["```", ""]
        if a["regressions"]:
            L += [f"**Regressions** (passed before, failed now): {', '.join(a['regressions'])}", ""]
        failed = [r for r in a["results"] if not r["passed"]]
        if failed:
            L += ["**What failed and why:**", ""]
            for r in failed:
                L.append(f"- **{r['id']}** ({r['dimension']}, {r['kind']} check): {r['reason']}")
                if r["evidence"]:
                    L.append(f"  - Evidence: _{r['evidence'][:400]}_")
                if r["fix"]:
                    L.append(f"  - Fix requested: {r['fix']}")
            L.append("")
        else:
            L += ["All checks passed.", ""]
    return "\n".join(L)
