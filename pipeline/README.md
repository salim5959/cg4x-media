# Chaîne vidéo CarteGrise4x

Production automatique de vidéos verticales 1080 × 1920 pour TikTok, Instagram Reels, Facebook Reels et YouTube Shorts, puis programmation dans Metricool (marque `7404281`).

Outils gratuits et open source : Python, Pillow, NumPy, FFmpeg, Piper (voix française SIWIS, licence CC BY 4.0). La musique est générée par le code : aucun droit tiers. Les illustrations (voiture, carte grise, plaque, calendrier…) sont dessinées par le code, sans visuel trompeur.

## Fichiers

| Fichier | Rôle |
|---|---|
| `setup.sh` | Installe Piper, la voix FR et les dépendances Python |
| `concepts_src.py` | Bibliothèque éditoriale (scripts, légendes, catégories). Génère `concepts.json` |
| `render.py` | Rend chaque concept : voix off, sous-titres karaoké, charte du site, musique, couverture |
| `schedule.py` | Calendrier 3 vidéos/jour/réseau et charges utiles Metricool (`posts.json`) |
| `push_media.sh` | Publie les MP4 dans ce dépôt et vérifie l'URL publique (Metricool les copie ensuite chez lui) |
| `sched_helper.py` | Programmation idempotente : file d'attente et journal `ledger.jsonl` (id Metricool de chaque post) |

## Utilisation

```bash
bash setup.sh
python3 concepts_src.py           # -> concepts.json
python3 render.py concepts.json   # -> out/Cxxx.mp4 + out/Cxxx_cover.jpg
python3 schedule.py               # -> posts.json, calendar.json
bash push_media.sh                # -> URLs publiques
python3 sched_helper.py next tiktok 5   # charges utiles à envoyer à createScheduledPost
```

Sous Windows : installer Python 3.11+, FFmpeg (`winget install ffmpeg`) et le binaire Piper Windows (github.com/rhasspy/piper/releases), puis adapter `PIPER` dans `render.py`.

## Créneaux (Metricool « meilleurs horaires », Europe/Paris)

TikTok 10:00 / 12:00 / 18:00 · Instagram 10:00 / 12:30 / 18:00 · Facebook 10:00 / 12:00 / 17:00 · YouTube 10:00 / 14:00 / 16:00. La catégorie de chaque créneau tourne chaque jour pour comparer les horaires.

## Règles éditoriales

- Faits vérifiés uniquement. Tarifs 2026 (source `data/tarifs.json` du site) : taxe Y.4 11 €, Y.5 2,76 €, Y.2 utilitaire 34 €, abattement 50 % au-delà de 10 ans. Cheval fiscal : Mayotte 30 €, Guadeloupe 41 €, Guyane 42,50 €, ARA et HDF 43 €, PDL 51 €, Corse et Martinique 53 €, IDF 54,95 € + 14 € = 68,95 €, NA 58 €, OCC 59,50 €, BFC, Bretagne, CVL, Grand Est, Normandie, PACA, Réunion 60 €.
- Délais : changement de titulaire 1 mois, déclaration de cession 15 jours, changement d'adresse 1 mois, contrôle technique de moins de 6 mois pour une vente (contre-visite : moins de 2 mois).
- Paiement en 4 fois : toujours « PayPal ou Klarna, selon éligibilité », `credit=True` (mention « Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager. »). Jamais d'acceptation garantie ni de « sans frais » non vérifié.
- Toujours « Service privé, non affilié à l'ANTS ». Jamais d'avis clients ni de chiffres non étayés.
- Promesse de délai autorisée, mot pour mot : « Dossier complet traité sous 12 h ouvrées ».

## Mesure

Liens Facebook et YouTube : `https://www.cartegrise4x.fr/?utm_source=<réseau>&utm_medium=social&utm_campaign=organic_video_2026&utm_content=<Cxxx>`. Pour TikTok et Instagram (lien en bio), utiliser `?utm_source=tiktok&utm_medium=social&utm_campaign=organic_video_2026&utm_content=bio` (et `instagram`).
