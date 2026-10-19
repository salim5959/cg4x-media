#!/usr/bin/env python3
"""Construit le calendrier (20/10 -> 18/11/2026) et les 332 charges utiles Metricool (posts.json).

Créneaux issus de getBestTimeToPostByNetwork (audience Metricool, Europe/Paris) :
  TikTok 10:00 / 12:00 / 18:00 · Instagram 10:00 / 12:30 / 18:00 · Facebook 10:00 / 12:00 / 17:00 · YouTube 10:00 / 14:00 / 16:00
La catégorie placée sur chaque créneau tourne chaque jour, pour comparer les horaires à contenu égal.
"""
import json, datetime as dt
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Paris")
MEDIA = "https://raw.githubusercontent.com/salim5959/cg4x-media/main/"
SLOTS = {"tiktok": ["10:00", "12:00", "18:00"], "instagram": ["10:00", "12:30", "18:00"],
         "facebook": ["10:00", "12:00", "17:00"], "youtube": ["10:00", "14:00", "16:00"]}
# Créneaux déjà occupés par les publications programmées existantes (audit du 19/10)
EXISTING = {}
for d in range(20, 25): EXISTING[f"2026-10-{d}"] = {"tiktok": "18:00", "instagram": "10:00", "facebook": "12:00", "youtube": "16:00"}
for d in (25, 26): EXISTING[f"2026-10-{d}"] = {"tiktok": "10:00", "instagram": "10:00", "facebook": "10:00", "youtube": "16:00"}

TAGS_BASE = {"tiktok": ["cartegrise", "voiture", "astuceauto", "pourtoi"], "instagram": ["cartegrise", "cartegriseenligne", "voiture", "conseilauto"],
             "facebook": ["cartegrise", "voiture"], "youtube": ["cartegrise", "voiture", "shorts"]}
ANTS = "Service privé, non affilié à l'ANTS."
CREDIT = "Paiement en 4 fois avec PayPal ou Klarna, selon éligibilité et sous réserve d'acceptation. Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager."

def utm(net, cid): return f"https://www.cartegrise4x.fr/?utm_source={net}&utm_medium=social&utm_campaign=organic_video_2026&utm_content={cid}"

def hashtags(net, c, n):
    seen, out = set(), []
    for t in c["tags"] + TAGS_BASE[net]:
        if t not in seen: seen.add(t); out.append("#" + t)
    return " ".join(out[:n])

def caption(net, c):
    body = c["desc"]; mention = ANTS + (" " + CREDIT if c["credit"] else "")
    if net == "tiktok": return f"{body}\n\n👉 Calculez votre prix : lien en bio, cartegrise4x.fr\n\n{mention}\n\n{hashtags(net, c, 6)}"
    if net == "instagram": return f"{body}\n\n👉 Calculez votre prix : lien en bio, cartegrise4x.fr\n\n{mention}\n\n{hashtags(net, c, 7)}"
    if net == "facebook": return f"{body}\n\n👉 Calculez votre prix : {utm(net, c['id'])}\n\n{mention}\n\n{hashtags(net, c, 4)}"
    return f"{body}\n\n👉 Calculez le prix de votre carte grise : {utm(net, c['id'])}\n\n{mention}\n\n{hashtags(net, c, 5)}"

def yt_title(c):
    t = c["title"]; suffix = " #shorts"
    return (t if len(t) + len(suffix) <= 100 else t[:100 - len(suffix) - 1] + "…") + suffix

def payload(net, c, day, hhmm):
    local = dt.datetime.fromisoformat(f"{day}T{hhmm}:00").replace(tzinfo=TZ)
    info = {"autoPublish": True, "draft": False, "descendants": [], "firstCommentText": "", "hasNotReadNotes": False,
            "media": [MEDIA + c["id"] + ".mp4"], "mediaAltText": [], "providers": [{"network": net}],
            "publicationDate": {"dateTime": local.strftime("%Y-%m-%dT%H:%M:%S"), "timezone": "Europe/Paris"},
            "shortener": False, "smartLinkData": {"ids": []}, "text": caption(net, c)}
    if net == "tiktok":
        info["tiktokData"] = {"privacyOption": "PUBLIC_TO_EVERYONE", "commercialContentOwnBrand": True, "title": c["title"][:90], "isAigc": True,
                              "disableComment": False, "disableDuet": False, "disableStitch": False, "autoAddMusic": False}
        info["videoCoverMilliseconds"] = 1200
    elif net == "instagram":
        info["instagramData"] = {"type": "REEL", "showReelOnFeed": True, "isAiGenerated": False}
        info["videoCoverMilliseconds"] = 1200
    elif net == "facebook":
        info["facebookData"] = {"type": "REEL", "title": c["title"][:250]}
        info["videoCoverMilliseconds"] = 1200
    else:
        info["youtubeData"] = {"title": yt_title(c), "type": "short", "privacy": "public", "category": "AUTOS_VEHICLES", "madeForKids": False,
                               "isAiGeneratedContent": False, "tags": list(dict.fromkeys(["carte grise", "carte grise en ligne", "cartegrise4x"] + [t for t in c["tags"]]))[:12]}
    return {"key": f"{c['id']}|{net}", "concept": c["id"], "network": net, "day": day, "time": hhmm,
            "date": local.isoformat(), "info": info}

def plan(concepts):
    by = {k: [c for c in concepts if c["category"] == k] for k in ("acquisition", "pedagogie", "conversion")}
    # ordre éditorial : sujets proches des posts existants (1 mois occasion, 4 fois) repoussés plus tard
    late = {"C001", "C058", "C057"}
    for k in by: by[k] = [c for c in by[k] if c["id"] not in late] + [c for c in by[k] if c["id"] in late]
    days = [(dt.date(2026, 10, 20) + dt.timedelta(d)).isoformat() for d in range(30)]
    cal = {}
    for i, day in enumerate(days):
        if day in EXISTING: cats = ["acquisition", "pedagogie"]
        else:
            cats = ["acquisition", "pedagogie", "conversion"]
            # 27 conversions pour 23 jours : 2 conversions sur 4 jours (en remplacement d'un sujet A/P en surplus inexistant)
        picks = []
        for k in cats:
            if by[k]: picks.append(by[k].pop(0))
        cal[day] = picks
    # placer les conversions restantes sur des jours qui en manquent
    rest = by["acquisition"] + by["pedagogie"] + by["conversion"]
    for day in days:
        while len(cal[day]) < (2 if day in EXISTING else 3) and rest: cal[day].append(rest.pop(0))
    assert not rest, rest
    return days, cal

def main():
    concepts = json.load(open("concepts.json", encoding="utf-8")); cmap = {c["id"]: c for c in concepts}
    days, cal = plan(concepts); posts = []
    for i, day in enumerate(days):
        picks = cal[day]
        for net, times in SLOTS.items():
            free = [t for t in times if EXISTING.get(day, {}).get(net) != t]
            # rotation : le créneau de chaque catégorie change d'un jour à l'autre
            rot = i % len(free); order = free[rot:] + free[:rot]
            for c, t in zip(picks, order): posts.append(payload(net, c, day, t))
    json.dump(posts, open("posts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({d: [c["id"] for c in cal[d]] for d in days}, open("calendar.json", "w"), indent=1)
    from collections import Counter
    print(len(posts), Counter(p["network"] for p in posts))
    per = Counter((p["day"], p["network"]) for p in posts)
    for d in days:
        line = " ".join(f"{n[:2]}={per[(d, n)] + (1 if n in EXISTING.get(d, {}) else 0)}" for n in SLOTS)
        print(d, cal[d] and [c["id"] for c in cal[d]], line)

if __name__ == "__main__": main()
