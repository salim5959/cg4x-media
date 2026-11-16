#!/usr/bin/env python3
"""Lot du 16/11/2026 : C084-C104 programmés du 22 au 28/11/2026 (3 vidéos/jour/réseau).
Créneaux identiques au dernier lot programmé (08/11) : TikTok 10:00/12:00/18:00 · Instagram 11:00/12:30/18:00 ·
Facebook 10:00/12:00/17:00 · YouTube 14:00/15:00/16:00. Rotation quotidienne des catégories sur les créneaux.
Sortie : posts_2611.json (mêmes champs que posts.json)."""
import json, datetime as dt
import schedule as S
S.SLOTS = {"tiktok": ["10:00", "12:00", "18:00"], "instagram": ["11:00", "12:30", "18:00"],
           "facebook": ["10:00", "12:00", "17:00"], "youtube": ["14:00", "15:00", "16:00"]}
CAL = [("C084", "C085", "C086"), ("C087", "C088", "C089"), ("C090", "C091", "C092"), ("C102", "C094", "C095"),
       ("C096", "C097", "C098"), ("C099", "C100", "C104"), ("C093", "C103", "C101")]
cmap = {c["id"]: c for c in json.load(open("concepts.json", encoding="utf-8"))}
posts = []
for i, ids in enumerate(CAL):
    day = (dt.date(2026, 11, 22) + dt.timedelta(i)).isoformat()
    for net, times in S.SLOTS.items():
        rot = i % 3; order = times[rot:] + times[:rot]
        for cid, t in zip(ids, order): posts.append(S.payload(net, cmap[cid], day, t))
json.dump(posts, open("posts_2611.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({(dt.date(2026, 11, 22) + dt.timedelta(i)).isoformat(): list(ids) for i, ids in enumerate(CAL)}, open("calendar_2611.json", "w"), indent=1)
from collections import Counter; print(len(posts), Counter(p["network"] for p in posts))
