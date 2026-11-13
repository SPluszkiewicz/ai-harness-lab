import json
import re

rows = [json.loads(l) for l in open("results/summary.jsonl", encoding="utf-8-sig") if l.strip()]


def show(h, m_sub, tasks):
    print("===", h, m_sub)
    for t in tasks:
        for r in rows:
            if r["harness"] == h and m_sub in r.get("model", "") and r["task"] == t:
                a = (r.get("answer") or "").replace("\n", " ")[:180]
                v = r.get("verify") or ""
                m = re.search(r"out of (\d+)", v)
                print(
                    f"  {t}#{r['trial']} tools={r.get('tools')} commits={r.get('commits')} "
                    f"outside={r.get('outside_exists')} tests={m.group(1) if m else '-'} "
                    f"diff={r.get('diff_stat')!r}"
                )
                print("   ", a)


show("pumba", "Qwen", ["T2", "T3"])
show("aider", "gpt-oss", ["T4", "T5", "T6", "T8"])
show("aider", "Qwen", ["T4", "T5", "T6", "T8"])
show("crush", "gpt-oss", ["T2", "T3", "T4", "T5", "T8"])
show("goose", "gpt-oss", ["T3", "T4", "T5", "T8"])
