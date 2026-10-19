import json,sys
cid,day,hhmm=sys.argv[1],sys.argv[2],sys.argv[3]
P={p['network']:p['info'] for p in json.load(open('posts.json')) if p['concept']==cid}
C={c['id']:c for c in json.load(open('concepts.json'))}[cid]
nets=sys.argv[4].split(',') if len(sys.argv)>4 else ['tiktok','instagram','facebook','youtube']
base=dict(P['tiktok']); base['providers']=[{'network':n} for n in nets]
base['publicationDate']={'dateTime':f'{day}T{hhmm}:00','timezone':'Europe/Paris'}
ments="Service privé, non affilié à l'ANTS."+(" Paiement en 4 fois avec PayPal ou Klarna, selon éligibilité et sous réserve d'acceptation. Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager." if C['credit'] else "")
tags=" ".join("#"+t for t in (C['tags']+['cartegrise','voiture'])[:6])
base['text']=f"{C['desc']}\n\n👉 Calculez votre prix sur cartegrise4x.fr (lien en bio)\n\n{ments}\n\n{tags}"
for k in ['tiktokData','instagramData','facebookData','youtubeData']: base.pop(k,None)
for n in nets: base[n+'Data']=P[n][n+'Data']
if 'youtube' in nets: base.pop('videoCoverMilliseconds',None)
print(json.dumps(base,ensure_ascii=False))
