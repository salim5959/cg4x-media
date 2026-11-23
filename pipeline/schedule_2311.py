#!/usr/bin/env python3
"""Lot du 23/11/2026 : C105-C125 programmés du 29/11 au 05/12/2026 (3 vidéos/jour/réseau).
Mêmes créneaux que le lot du 16/11 : TikTok 10:00/12:00/18:00 · Instagram 11:00/12:30/18:00 ·
Facebook 10:00/12:00/17:00 · YouTube 14:00/15:00/16:00. Rotation quotidienne poursuivie (indice 7 à 13).
Exceptions du 01/12 (créneaux déjà occupés) : YouTube 14:00 (post 400765136) -> 10:00 ; TikTok 10:00 (brouillon 415593523)
-> 11:00 ; Facebook 10:00 (brouillon 415593184) -> 11:00.
Sortie : posts_2311.json, calendar_2311.json."""
import json, datetime as dt
import schedule as S
S.SLOTS = {"tiktok": ["10:00", "12:00", "18:00"], "instagram": ["11:00", "12:30", "18:00"],
           "facebook": ["10:00", "12:00", "17:00"], "youtube": ["14:00", "15:00", "16:00"]}
OVERRIDE = {("2026-12-01", "youtube", "14:00"): "10:00", ("2026-12-01", "tiktok", "10:00"): "11:00",
            ("2026-12-01", "facebook", "10:00"): "11:00"}
START = dt.date(2026, 11, 29)
CAL = [(f"C{105+3*i}", f"C{106+3*i}", f"C{107+3*i}") for i in range(7)]
cmap = {c["id"]: c for c in json.load(open("concepts.json", encoding="utf-8"))}
posts = []
for i, ids in enumerate(CAL):
    day = (START + dt.timedelta(i)).isoformat()
    for net, times in S.SLOTS.items():
        rot = (i + 7) % 3; order = times[rot:] + times[:rot]
        for cid, t in zip(ids, order): posts.append(S.payload(net, cmap[cid], day, OVERRIDE.get((day, net, t), t)))
json.dump(posts, open("posts_2311.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({(START + dt.timedelta(i)).isoformat(): list(ids) for i, ids in enumerate(CAL)}, open("calendar_2311.json", "w"), indent=1)
from collections import Counter; print(len(posts), Counter(p["network"] for p in posts))
