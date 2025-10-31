
import json
import shutil
from pathlib import Path

paths = ['secure_work', 'secure_input']
for path in paths:
    target = Path(path)
    if target.exists():
        shutil.rmtree(target)

artifacts = Path('artifacts')
artifacts.mkdir(exist_ok=True)
artifacts.joinpath('destruction_attestation.json').write_text(json.dumps({
    'destroyed_paths': paths
}, indent=2))
