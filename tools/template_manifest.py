
import os, json, hashlib, datetime

SQL_DIRS = ["sql", "sql/tests"]
MANIFEST = "artifacts/sql_manifest.json"
ALERTS = "artifacts/template_alerts.jsonl"

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def build_manifest():
    entries = {}
    for d in SQL_DIRS:
        if not os.path.isdir(d):
            continue
        for root,_,files in os.walk(d):
            for name in files:
                if name.endswith(".sql"):
                    p = os.path.join(root, name)
                    entries[os.path.relpath(p)] = hash_file(p)
    meta = {"ts": datetime.datetime.utcnow().isoformat()+"Z", "entries": entries}
    with open(MANIFEST, "w") as f:
        json.dump(meta, f, indent=2)
    print("Manifest written:", MANIFEST)

def compare_manifest():
    if not os.path.exists(MANIFEST):
        print("No previous manifest to compare.")
        build_manifest()
        return
    with open(MANIFEST) as f:
        prev = json.load(f)["entries"]
    current = {}
    changed = []
    for d in SQL_DIRS:
        for root,_,files in os.walk(d):
            for name in files:
                if name.endswith(".sql"):
                    p = os.path.join(root, name)
                    rel = os.path.relpath(p)
                    h = hash_file(p)
                    current[rel] = h
                    if rel not in prev or prev[rel] != h:
                        changed.append(rel)
    alert = {"ts": datetime.datetime.utcnow().isoformat()+"Z", "changed_sql": changed}
    os.makedirs("artifacts", exist_ok=True)
    with open(ALERTS, "a") as f:
        f.write(json.dumps(alert)+"\n")
    with open(MANIFEST, "w") as f:
        json.dump({"ts": alert["ts"], "entries": current}, f, indent=2)
    print("Compared. Changed:", changed)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--compare", action="store_true")
    args = p.parse_args()
    if args.compare:
        compare_manifest()
    else:
        build_manifest()
