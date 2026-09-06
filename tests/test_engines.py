"""Offline smoke tests for both engines (env=None path — no hosted model needed).

Run either way:
    python -m pytest tests/test_engines.py -v
    python tests/test_engines.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for _p in (str(ROOT), str(ROOT / "official")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from aicomp_sdk.attacks.contracts import AttackRunConfig

import attack
import attack_private


def test_exfil_offline_returns_candidates():
    out = attack.AttackAlgorithm().run(None, AttackRunConfig(time_budget_s=30))
    assert out, "exfil engine returned no offline candidates"
    assert all(c.user_messages for c in out)


def test_exfil_candidates_carry_sentinel():
    out = attack.AttackAlgorithm().run(None, AttackRunConfig(time_budget_s=30))
    for c in out[:50]:
        assert "SECRET_MARKER" in c.user_messages[0]


def test_exfil_candidates_are_cell_distinct():
    out = attack.AttackAlgorithm().run(None, AttackRunConfig(time_budget_s=30))
    msgs = {c.user_messages[0] for c in out}
    assert len(msgs) == len(out) > 1, "candidates are not cell-distinct"


def test_deputy_offline_returns_candidates():
    out = attack_private.AttackAlgorithm().run(None, AttackRunConfig(time_budget_s=30))
    assert out, "deputy engine returned no offline candidates"
    assert all(c.user_messages for c in out)


def test_deputy_targets_whitelist_without_share_intent_words():
    out = attack_private.AttackAlgorithm().run(None, AttackRunConfig(time_budget_s=30))
    for c in out[:50]:
        m = c.user_messages[0]
        assert "corp.invalid" in m, "recipient is not on the whitelisted domain"
        # CONFUSED_DEPUTY is suppressed by send/email/upload — the message must avoid them
        assert not any(w in m.lower() for w in ("send", "email", "upload")), m


if __name__ == "__main__":
    test_exfil_offline_returns_candidates()
    test_exfil_candidates_carry_sentinel()
    test_exfil_candidates_are_cell_distinct()
    test_deputy_offline_returns_candidates()
    test_deputy_targets_whitelist_without_share_intent_words()
    print("all offline engine tests passed")
