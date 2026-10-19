#!/usr/bin/env python3
"""Aide à la programmation Metricool, idempotente.

  python3 sched_helper.py next <network> [n]     -> prochaines charges utiles à programmer (vidéo publique, pas encore dans ledger.jsonl)
  python3 sched_helper.py record '<json>'        -> enregistre le retour Metricool (id, uuid, media, statut) dans ledger.jsonl
  python3 sched_helper.py status                 -> compte par réseau
"""
import json, sys, os
D = os.path.dirname(os.path.abspath(__file__))
posts = json.load(open(os.path.join(D, "posts.json"), encoding="utf-8"))
def ledger():
    p = os.path.join(D, "ledger.jsonl")
    return {json.loads(l)["key"]: json.loads(l) for l in open(p, encoding="utf-8") if l.strip()} if os.path.exists(p) else {}
def public():
    p = os.path.join(D, "public_ok.txt")
    return set(open(p).read().split()) if os.path.exists(p) else set()

cmd = sys.argv[1]
if cmd == "next":
    net = sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    led, pub = ledger(), public()
    todo = sorted([p for p in posts if p["network"] == net and p["key"] not in led and p["concept"] in pub], key=lambda p: p["date"])
    for p in todo[:n]:
        print(json.dumps({"key": p["key"], "date": p["date"], "info": json.dumps(p["info"], ensure_ascii=False)}, ensure_ascii=False))
    print(f"# restant pour {net}: {len([p for p in posts if p['network'] == net and p['key'] not in led])} (dont {len(todo)} prêts)")
elif cmd == "record":
    r = json.loads(sys.argv[2]); assert "key" in r and "id" in r
    with open(os.path.join(D, "ledger.jsonl"), "a", encoding="utf-8") as f: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("ok", r["key"])
elif cmd == "status":
    from collections import Counter
    led = ledger(); print(len(led), Counter(k.split("|")[1] for k in led))
