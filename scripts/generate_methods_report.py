
import os
from pathlib import Path

import yaml

TGT = Path('artifacts/Methods.md')

TEMPLATE = """# Methods Appendix

**Window:** {start} to {end}

## Metrics
{metrics}
"""

ITEM = """### {name}
- Type: {type}
- Denominator: {denom}
- Lookback: {lookback_days} days
- Dx include: {icd10}
- Px include: {cpt}
"""


def main():
    start, end = os.environ.get('START'), os.environ.get('END')
    cfg = yaml.safe_load(Path('config/metrics_codebook.yaml').read_text())
    parts = []
    for name, spec in cfg['metrics'].items():
        parts.append(ITEM.format(
            name=name,
            type=spec.get('type'),
            denom=spec.get('denom', 'n/a'),
            lookback_days=spec.get('lookback_days', 'n/a'),
            icd10=','.join(spec.get('icd10_include', [])),
            cpt=','.join(map(str, spec.get('cpt_include', [])))
        ))
    TGT.parent.mkdir(exist_ok=True)
    TGT.write_text(TEMPLATE.format(start=start, end=end, metrics='
'.join(parts)))


if __name__ == '__main__':
    main()
