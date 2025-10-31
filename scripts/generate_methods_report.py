
import os, json, yaml, pandas as pd, datetime, hashlib

def load_jsonl(path):
    rows = []
    if not os.path.exists(path): return rows
    with open(path) as f:
        for line in f:
            line=line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def main(audit_path="artifacts/audit.jsonl", metrics_path="artifacts/metrics.csv", codebook_path="config/metrics_codebook.yaml", out="reports/methods_and_limitations.md"):
    audit = load_jsonl(audit_path)
    metrics = pd.read_csv(metrics_path) if os.path.exists(metrics_path) else pd.DataFrame()
    codebook = yaml.safe_load(open(codebook_path))
    ts = datetime.datetime.utcnow().isoformat()+"Z"

    # Simple reproducibility hash (audit + metrics)
    h = hashlib.sha256()
    for e in audit:
        h.update(json.dumps(e, sort_keys=True).encode())
    if not metrics.empty:
        h.update(pd.util.hash_pandas_object(metrics, index=False).values.tobytes())
    run_hash = h.hexdigest()

    lines = []
    lines.append(f"# Methods & Limitations\n")
    lines.append(f"_Generated: {ts}_\n")
    lines.append(f"**Reproducibility hash**: `{run_hash}`\n")
    lines.append(f"## Metric Definitions (from codebook v{codebook['meta']['version']})\n")
    for m in codebook["metrics"]:
        lines.append(f"### {m['title']} (`{m['name']}`)")
        lines.append(f"- **Denominator**: {m['denominator']['population']}")
        lines.append(f"- **Numerator**: {m['numerator']['definition']} (codes: {m['numerator']['code_sets']})")
        lines.append(f"- **Exclusions**: {', '.join(m['exclusions']) if m.get('exclusions') else 'None'}")
        lines.append(f"- **Limitations**: {', '.join(m['limitations']) if m.get('limitations') else 'None'}")
        lines.append(f"- **Population validity**: {m.get('population_validity','N/A')}\n")
    if not metrics.empty:
        lines.append("## Metric Results\n")
        for _, r in metrics.iterrows():
            rate = "NA" if pd.isna(r["rate"]) else f"{float(r['rate']):.1%}"
            lines.append(f"- **{r['metric_name']}**: numerator={int(r['numerator'])}, denominator={int(r['denominator'])}, rate={rate}")
    lines.append("\n## Audit Summary\n")
    by_stage = {}
    for e in audit:
        by_stage.setdefault(e["stage"], 0)
        by_stage[e["stage"]] += 1
    for k,v in by_stage.items():
        lines.append(f"- {k}: {v} events")
    lines.append("\n## Notes\n- Claims reflect insured/observable populations.\n- All SQL templates are versioned; see manifest alerts for changes.\n")

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write("\n".join(lines))
    print("Wrote", out)

if __name__ == "__main__":
    main()
