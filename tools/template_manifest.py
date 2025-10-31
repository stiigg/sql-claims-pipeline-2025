import hashlib
from pathlib import Path


def compute_manifest(root):
    out = []
    for path in sorted(Path(root).rglob('*.sql')):
        out.append({
            'file': str(path),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()
        })
    return out
