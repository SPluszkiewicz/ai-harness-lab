import json
from pathlib import Path

p = Path("results/summary.jsonl")
text = p.read_text(encoding="utf-8-sig")
rows = [json.loads(l) for l in text.splitlines() if l.strip()]
keep = []
drop = 0
for r in rows:
    if r.get("harness") == "pumba" and r.get("task") in ("T2", "T3"):
        drop += 1
        continue
    if r.get("harness") == "aider" and r.get("task") == "T1" and str(r.get("model", "")).startswith("Qwen"):
        drop += 1
        continue
    keep.append(r)
p.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in keep) + ("\n" if keep else ""), encoding="utf-8")
print(f"kept {len(keep)}, dropped {drop}")
