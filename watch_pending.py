import subprocess, time, sys

COMP = "ai-agent-security-multi-step-tool-attacks"
WATCH = {
    "55861381": "deputy farm roll 1 (v36)",
    "55861384": "deputy farm roll 2 (v36)",
    "55861386": "deputy farm roll 3 (v36)",
    "55861388": "exfil farm roll 1 (v34)",
    "55861391": "exfil farm roll 2 (v34)",
}
POLL_S = 600
MAX_H = 26

deadline = time.time() + MAX_H * 3600
pending = set(WATCH)

while pending:
    found = {}
    try:
        out = subprocess.run(
            ["kaggle", "competitions", "submissions", "-c", COMP, "--csv"],
            capture_output=True, text=True, timeout=120,
        ).stdout
        for line in out.splitlines()[1:]:
            p = line.split(",")
            if p and p[0] in WATCH:
                found[p[0]] = p
    except Exception as e:
        print(f"[watch] fetch err {e}", flush=True)

    for ref in sorted(pending):
        if ref in found:
            p = found[ref]
            status = p[4] if len(p) > 4 else "?"
            pub = p[5] if len(p) > 5 else ""
            print(f"[{time.strftime('%H:%M')}] {ref} {WATCH[ref]} -> {status} public={pub}", flush=True)
            if "PENDING" not in status and "QUEUED" not in status:
                pending.discard(ref)

    if time.time() > deadline:
        print("TIMEOUT", flush=True); sys.exit(1)
    if pending:
        time.sleep(POLL_S)

print("ALL RESOLVED", flush=True)
