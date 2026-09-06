"""Guarantee the submission notebook embeds the exact medal-winning engine.

The #1 reproducibility invariant: `submission_notebook.ipynb` must write a
`/kaggle/working/attack.py` that is byte-identical to `attack_private.py` (the
CONFUSED_DEPUTY email.send engine that scored private 26.52 → #42/4186 Silver).

Run either way:
    python -m pytest tests/test_notebook_consistency.py -v
    python tests/test_notebook_consistency.py
"""
import base64
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _embedded_bytes() -> bytes:
    nb = json.loads((ROOT / "submission_notebook.ipynb").read_text(encoding="utf-8"))
    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        m = re.search(r'ATTACK_B64\s*=\s*"([A-Za-z0-9+/=]+)"', src)
        if m:
            return base64.b64decode(m.group(1))
    raise AssertionError("no ATTACK_B64 code cell found in the notebook")


def test_notebook_embeds_medal_engine_byte_for_byte():
    embedded = _embedded_bytes()
    on_disk = (ROOT / "attack_private.py").read_bytes()
    assert embedded == on_disk, (
        "submission_notebook.ipynb does not embed attack_private.py byte-for-byte; "
        "the medal result is not reproducible from the notebook."
    )


def test_embedded_source_compiles():
    src = _embedded_bytes().decode("utf-8")
    compile(src, "attack.py", "exec")


if __name__ == "__main__":
    test_notebook_embeds_medal_engine_byte_for_byte()
    test_embedded_source_compiles()
    print("notebook consistency tests passed")
