import json
import sys
from pathlib import Path

harness, model, tasks = sys.argv[1], sys.argv[2], set(sys.argv[3].split(","))
p = Path("results/summary.jsonl")
rows = [json.loads(l) for l in p.read_text(encoding="utf-8-sig").splitlines() if l.strip()]
keep = [r for r in rows if not (r.get("harness") == harness and r.get("model") == model and r.get("task") in tasks)]
p.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in keep) + ("\n" if keep else ""), encoding="utf-8")
print(f"kept {len(keep)}, dropped {len(rows) - len(keep)}")
