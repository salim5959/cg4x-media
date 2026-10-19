"""Bibliothèque éditoriale CarteGrise4x : 83 concepts vidéo (octobre-novembre 2026).

Règles : faits vérifiés uniquement (data/tarifs.json du site, tarifs 2026 ; délais légaux), aucune promesse
d'acceptation de crédit, mention crédit dès que le paiement en 4 fois est évoqué, service privé non affilié à l'ANTS.
Catégories : acquisition (A), pedagogie (P), conversion (V).
"""
import json

def H(big, icon=None, voice="", kicker=None): return {"type": "hook", "big": big, "icon": icon, "voice": voice, "kicker": kicker}
def P(title, text=None, icon=None, voice="", n=None): return {"type": "point", "title": title, "text": text, "icon": icon, "voice": voice, "n": n}
def L(title, items, voice=""): return {"type": "list", "title": title, "items": items, "voice": voice}
def S(value, label, icon=None, voice=""): return {"type": "stat", "value": value, "label": label, "icon": icon, "voice": voice}
def V(title, left, right, voice=""): return {"type": "versus", "title": title, "left": left, "right": right, "voice": voice}
def ST(title, items, voice=""): return {"type": "steps", "title": title, "items": items, "voice": voice}
def CTA(big="Calculez le prix de votre *carte grise*", sub="Tarif de votre département, tout compris", voice="Calculez votre prix sur cartegrise4x.fr."):
    return {"type": "cta", "big": big, "sub": sub, "voice": voice}
CREDIT_CTA = lambda: CTA("Payez en *1 ou 4 fois*", "PayPal ou Klarna, selon éligibilité", "Calculez votre prix sur cartegrise4x.fr. Paiement en quatre fois selon éligibilité. Un crédit vous engage et doit être remboursé.")

C = []
def add(cid, cat, title, desc, tags, scenes, credit=False):
    C.append({"id": cid, "category": cat, "title": title, "desc": desc, "tags": tags, "credit": credit, "scenes": scenes})

# ======================= ACQUISITION ==========================================================
add("C001", "acquisition", "Voiture d'occasion : 1 mois pour faire la carte grise",
    "Vous venez d'acheter une voiture d'occasion ? Vous avez 1 mois à partir de la date de vente pour mettre la carte grise à votre nom. Préparez la carte grise barrée, le certificat de cession, un justificatif de domicile et votre permis.",
    ["voitureoccasion", "changementdetitulaire", "achatvoiture"],
    [H("Vous avez *1 mois*, pas un jour de plus", "calendar", "Vous venez d'acheter une voiture d'occasion ? Vous avez un mois, pas un jour de plus.", "Voiture d'occasion"),
     P("Le délai démarre à la *vente*", "Un mois à compter de la date inscrite sur le certificat de cession.", "doc", "Le délai démarre à la date de la vente, inscrite sur le certificat de cession.", "1"),
     L("Préparez *4 documents*", ["Carte grise barrée et signée", "Certificat de cession", "Justificatif de domicile", "Permis de conduire"], "Préparez la carte grise barrée, le certificat de cession, un justificatif de domicile et votre permis."),
     CTA("Faites-la *en ligne* aujourd'hui", "Prix calculé selon votre département", "Calculez votre prix et faites la démarche sur cartegrise4x.fr.")])

add("C002", "acquisition", "Même voiture, prix différent selon la région",
    "Même voiture, même puissance, et pourtant pas le même prix de carte grise. Pour une 5 CV en 2026 : 344,75 € de taxe régionale en Île-de-France contre 215 € en Hauts-de-France (hors taxes fixes). Le tarif dépend du prix du cheval fiscal dans votre région.",
    ["prixcartegrise", "chevalfiscal", "iledefrance", "hautsdefrance"],
    [H("Même voiture, *130 € d'écart*", "map", "Même voiture, même puissance. Pourtant, cent trente euros d'écart sur la carte grise.", "5 CV en 2026"),
     S("344,75 €", "Taxe régionale d'une *5 CV* en Île-de-France", "euro", "En Île-de-France, la taxe régionale d'une cinq chevaux coûte trois cent quarante-quatre euros soixante-quinze."),
     S("215 €", "La même *5 CV* en Hauts-de-France", "euro", "En Hauts-de-France, la même voiture coûte deux cent quinze euros."),
     P("Pourquoi ?", "Chaque région fixe le prix du cheval fiscal : de 30 € à 68,95 € en 2026.", "map", "Chaque région fixe son prix du cheval fiscal, de trente à soixante-huit euros quatre-vingt-quinze."),
     CTA("Votre prix *exact* en 30 secondes", "Selon votre département et votre véhicule", "Calculez votre prix exact sur cartegrise4x.fr.")])

add("C003", "acquisition", "Comment est calculé le prix d'une carte grise",
    "Le prix d'une carte grise, c'est une formule simple : chevaux fiscaux × prix du cheval dans votre région, plus la taxe fixe Y.4 (11 €) et la redevance d'acheminement Y.5 (2,76 €). Un malus peut s'ajouter selon le véhicule.",
    ["prixcartegrise", "chevalfiscal", "taxe"],
    [H("Le prix de la carte grise, *décodé*", "euro", "Le prix d'une carte grise, ce n'est pas un mystère. Voici la formule."),
     P("*Chevaux fiscaux* × prix régional", "La puissance fiscale (case P.6) multipliée par le tarif du cheval de votre région.", "car", "D'abord, vos chevaux fiscaux, multipliés par le prix du cheval dans votre région.", "1"),
     P("+ *11 €* de taxe fixe", "La taxe Y.4, identique partout en France.", "doc", "Ensuite, onze euros de taxe fixe.", "2"),
     P("+ *2,76 €* d'acheminement", "La redevance Y.5 pour l'envoi sécurisé du titre.", "house", "Et deux euros soixante-seize pour l'envoi du titre.", "3"),
     CTA()])

add("C004", "acquisition", "Voiture de plus de 10 ans : la taxe régionale divisée par 2",
    "Votre voiture a plus de 10 ans ? La taxe régionale de la carte grise est réduite de 50 %. Exemple en 2026 : une 6 CV en Bretagne passe de 360 € à 180 € de taxe régionale (hors taxes fixes).",
    ["voitureoccasion", "prixcartegrise", "astuce"],
    [H("Plus de 10 ans ? *-50 %*", "car", "Votre voiture a plus de dix ans ? Bonne nouvelle pour la carte grise.", "Bon à savoir"),
     S("-50 %", "Sur la *taxe régionale* au-delà de 10 ans", "euro", "La taxe régionale est réduite de moitié."),
     V("Exemple : 6 CV en Bretagne", ("Moins de 10 ans", "6 × 60 € = 360 € de taxe régionale"), ("Plus de 10 ans", "180 € de taxe régionale"), "Une six chevaux en Bretagne passe de trois cent soixante à cent quatre-vingts euros."),
     CTA("Vérifiez *votre* réduction", "Calcul automatique selon la date de 1re immatriculation", "Vérifiez votre prix sur cartegrise4x.fr.")])

add("C005", "acquisition", "Avant de payer le vendeur : les 5 documents à récupérer",
    "Avant de payer une voiture d'occasion, récupérez : la carte grise barrée et signée, le certificat de cession, le code de cession, le contrôle technique de moins de 6 mois (véhicule de plus de 4 ans) et le certificat de situation administrative.",
    ["voitureoccasion", "achatvoiture", "checklist"],
    [H("N'achetez *pas* avant d'avoir ces 5 papiers", "warn", "Ne payez jamais une voiture d'occasion avant d'avoir ces cinq papiers.", "Achat d'occasion"),
     L("La *checklist* acheteur", ["Carte grise barrée et signée", "Certificat de cession", "Code de cession", "Contrôle technique de moins de 6 mois", "Certificat de situation administrative"], "La carte grise barrée, le certificat de cession, le code de cession, un contrôle technique de moins de six mois, et le certificat de situation administrative."),
     P("Sans eux, *dossier bloqué*", "Un document manquant et la carte grise ne peut pas être faite à votre nom.", "cross", "Sans eux, impossible de mettre la carte grise à votre nom."),
     CTA("On vérifie *votre dossier*", "Avant la saisie de la demande", "Calculez votre prix sur cartegrise4x.fr.")])

add("C006", "acquisition", "Le code de cession, c'est quoi ?",
    "Le code de cession est remis par le vendeur une fois sa déclaration de cession faite. Il permet à l'acheteur de faire la carte grise à son nom. Pensez à le demander le jour de la vente.",
    ["codedecession", "voitureoccasion", "changementdetitulaire"],
    [H("Le *code de cession*, vous l'avez ?", "key", "Vous achetez une voiture d'occasion. Avez-vous pensé au code de cession ?", "Question piège"),
     P("Un code donné par le *vendeur*", "Il l'obtient en déclarant la vente de son véhicule.", "swap", "C'est le vendeur qui l'obtient, en déclarant la vente."),
     P("Indispensable pour *l'acheteur*", "Il permet de mettre la carte grise à votre nom.", "doc", "Sans lui, impossible de faire la carte grise à votre nom."),
     P("Réflexe : le demander *le jour J*", None, "check", "Le bon réflexe : le demander le jour de la vente."),
     CTA()])

add("C007", "acquisition", "Contrôle technique : moins de 6 mois pour vendre",
    "Pour vendre une voiture de plus de 4 ans, le contrôle technique doit dater de moins de 6 mois au moment de la vente. Sans lui, la carte grise ne peut pas être faite au nom de l'acheteur.",
    ["controletechnique", "voitureoccasion", "vendresavoiture"],
    [H("Contrôle technique *de plus de 6 mois* ?", "clock", "Votre contrôle technique a plus de six mois ? Attention si vous achetez ou vendez.", "Achat ou vente"),
     S("6 mois", "Durée de validité du CT *pour une vente*", "calendar", "Pour une vente, il doit dater de moins de six mois."),
     P("Pour les véhicules de *plus de 4 ans*", "Le procès-verbal est obligatoire dans le dossier de carte grise.", "car", "C'est obligatoire pour les véhicules de plus de quatre ans."),
     CTA()])

add("C008", "acquisition", "Certificat de situation administrative : à vérifier avant d'acheter",
    "Avant d'acheter une voiture d'occasion, demandez le certificat de situation administrative. Il indique si le véhicule est gagé ou fait l'objet d'une opposition, ce qui peut bloquer la carte grise.",
    ["nongage", "voitureoccasion", "achatvoiture"],
    [H("Voiture *gagée* = carte grise bloquée", "warn", "Une voiture gagée, et votre carte grise peut être bloquée.", "Achat d'occasion"),
     P("Demandez le *certificat de situation administrative*", "L'ancien « certificat de non-gage ».", "doc", "Demandez le certificat de situation administrative, l'ancien certificat de non-gage."),
     L("Il vous dit si", ["Le véhicule est gagé", "Une opposition existe", "Le véhicule est déclaré volé"], "Il indique si la voiture est gagée, si une opposition existe, ou si elle est déclarée volée."),
     CTA()])

add("C009", "acquisition", "Les régions où la carte grise coûte le moins cher en 2026",
    "Prix du cheval fiscal en 2026 : 30 € à Mayotte, 41 € en Guadeloupe, 43 € en Auvergne-Rhône-Alpes et en Hauts-de-France. Plusieurs régions appliquent le plafond légal de 60 €.",
    ["prixcartegrise", "chevalfiscal", "regions"],
    [H("Où la carte grise coûte *le moins cher* ?", "map", "Où la carte grise coûte-t-elle le moins cher en 2026 ?", "Tarifs 2026"),
     L("Le cheval fiscal *le moins cher*", ["Mayotte : 30 €", "Guadeloupe : 41 €", "Auvergne-Rhône-Alpes : 43 €", "Hauts-de-France : 43 €"], "Mayotte à trente euros, la Guadeloupe à quarante et un, l'Auvergne-Rhône-Alpes et les Hauts-de-France à quarante-trois."),
     P("Le plafond : *60 €*", "Bretagne, Grand Est, Normandie, PACA et d'autres y sont.", "euro", "Plusieurs régions sont au plafond de soixante euros."),
     CTA("Le prix de *votre* département", "Tarifs 2026 mis à jour", "Calculez le prix dans votre département sur cartegrise4x.fr.")])

add("C010", "acquisition", "Île-de-France : 68,95 € le cheval fiscal en 2026",
    "En Île-de-France, depuis 2026, une majoration de 14 € par cheval s'ajoute au tarif régional de 54,95 €, soit 68,95 € par cheval fiscal. Pour une 5 CV : 344,75 € de taxe régionale.",
    ["iledefrance", "paris", "prixcartegrise", "chevalfiscal"],
    [H("Île-de-France : la carte grise *la plus chère*", "map", "En Île-de-France, la carte grise a augmenté en 2026.", "Tarifs 2026"),
     S("68,95 €", "Le cheval fiscal en *Île-de-France*", "euro", "Le cheval fiscal y coûte soixante-huit euros quatre-vingt-quinze."),
     P("54,95 € + *14 €* de majoration", "Une majoration s'ajoute depuis 2026.", "doc", "Cinquante-quatre euros quatre-vingt-quinze, plus quatorze euros de majoration."),
     S("344,75 €", "Taxe régionale d'une *5 CV*", "car", "Pour une cinq chevaux, cela fait trois cent quarante-quatre euros soixante-quinze."),
     CTA()])

add("C011", "acquisition", "Corse : le cheval fiscal passe de 43 à 53 €",
    "Plus forte hausse de France en 2026 : en Corse, le cheval fiscal est passé de 43 € à 53 € au 1er mars 2026.",
    ["corse", "prixcartegrise", "chevalfiscal"],
    [H("Corse : *+10 €* par cheval", "map", "En Corse, la carte grise a pris dix euros par cheval.", "Tarifs 2026"),
     V("Prix du cheval fiscal", ("Avant mars 2026", "43 €"), ("Depuis le 1er mars 2026", "53 €"), "Quarante-trois euros avant mars deux mille vingt-six, cinquante-trois euros depuis."),
     S("+50 €", "Sur la taxe régionale d'une *5 CV*", "euro", "Pour une cinq chevaux, cinquante euros de plus."),
     CTA()])

add("C012", "acquisition", "Où trouver la puissance fiscale sur la carte grise",
    "La puissance fiscale (en chevaux) est indiquée case P.6 de la carte grise. C'est elle qui sert au calcul du prix.",
    ["chevalfiscal", "cartegrise", "astuce"],
    [H("Vos *chevaux fiscaux*, où les trouver ?", "doc", "Combien de chevaux fiscaux a votre voiture ? La réponse est sur la carte grise.", "Astuce"),
     S("P.6", "La case de la *puissance fiscale*", "doc", "Regardez la case P point six."),
     P("C'est elle qui fixe *le prix*", "Puissance fiscale × prix du cheval de votre région.", "euro", "C'est elle qui sert à calculer le prix."),
     CTA()])

add("C013", "acquisition", "Acheter à un particulier : 4 réflexes",
    "Achat d'une voiture à un particulier : vérifiez l'identité du vendeur sur la carte grise, le numéro VIN (case E), le certificat de situation administrative et le contrôle technique.",
    ["voitureoccasion", "achatvoiture", "leboncoin"],
    [H("Achat entre particuliers : *4 réflexes*", "car", "Vous achetez une voiture à un particulier ? Quatre réflexes.", "Avant de signer"),
     ST("Avant de signer", ["Le nom du vendeur = celui de la carte grise", "Le VIN (case E) = celui du véhicule", "Pas de gage ni d'opposition", "Contrôle technique de moins de 6 mois"], "Le vendeur est bien le titulaire. Le numéro de série correspond. Pas de gage. Et un contrôle technique récent."),
     CTA()])

add("C014", "acquisition", "Utilitaire : la taxe Y.2 de 34 €",
    "Vous achetez une camionnette (CTTE) de 3,5 t maximum ? Une taxe Y.2 de 34 € (formation professionnelle) s'ajoute au prix de la carte grise.",
    ["utilitaire", "artisan", "prixcartegrise"],
    [H("Utilitaire ? Une taxe *en plus*", "car", "Vous achetez un utilitaire ? Une taxe s'ajoute à la carte grise.", "Pros et artisans"),
     S("34 €", "Taxe *Y.2* pour une camionnette jusqu'à 3,5 t", "euro", "Trente-quatre euros de taxe Y deux, pour une camionnette jusqu'à trois tonnes et demie."),
     P("Elle s'ajoute *au reste*", "Taxe régionale + Y.4 + Y.5 + Y.2.", "doc", "Elle s'ajoute à la taxe régionale et aux taxes fixes."),
     CTA()])

add("C015", "acquisition", "Ce qui fait varier le prix de votre carte grise",
    "5 éléments font varier le prix d'une carte grise : la région, la puissance fiscale, l'âge du véhicule, son type et un éventuel malus.",
    ["prixcartegrise", "chevalfiscal"],
    [H("Pourquoi *votre* carte grise coûte ce prix ?", "question", "Pourquoi votre carte grise coûte ce prix-là ?", None),
     L("*5 critères*", ["Votre région", "La puissance fiscale", "L'âge du véhicule", "Le type de véhicule", "Un éventuel malus"], "La région. La puissance fiscale. L'âge du véhicule. Son type. Et un éventuel malus."),
     CTA()])

add("C016", "acquisition", "Qui paie la carte grise : l'acheteur ou le vendeur ?",
    "Lors d'une vente entre particuliers, c'est l'acheteur qui fait la carte grise à son nom et qui paie les taxes. Le vendeur, lui, déclare la cession dans les 15 jours.",
    ["voitureoccasion", "changementdetitulaire"],
    [H("Carte grise : *qui paie* ?", "question", "Vente de voiture : qui paie la carte grise ?", None),
     V(None, ("Le vendeur", "Déclare la cession dans les 15 jours"), ("L'acheteur", "Fait et paie la carte grise à son nom"), "Le vendeur déclare la vente. L'acheteur fait et paie la nouvelle carte grise."),
     CTA()])

add("C017", "acquisition", "Le certificat provisoire pour rouler tout de suite",
    "Dès que votre demande est enregistrée, un certificat provisoire vous permet de rouler en France en attendant votre carte grise définitive.",
    ["cartegrise", "voitureoccasion"],
    [H("Rouler *avant* de recevoir la carte grise ?", "car", "Vous pouvez rouler avant de recevoir votre carte grise.", None),
     P("Le *certificat provisoire*", "Remis dès l'enregistrement de votre demande.", "doc", "Grâce au certificat provisoire, remis dès l'enregistrement de votre demande."),
     P("Valable en *France*", "En attendant le titre définitif envoyé chez vous.", "house", "Il est valable en France, en attendant la carte grise envoyée chez vous."),
     CTA()])

add("C018", "acquisition", "Première voiture : la checklist carte grise",
    "Première voiture ? Pour la carte grise, il vous faut : une pièce d'identité, votre permis, un justificatif de domicile de moins de 6 mois, la carte grise barrée, le certificat de cession et le code de cession.",
    ["premierevoiture", "jeuneconducteur", "permis"],
    [H("Première voiture ? *La checklist*", "key", "Première voiture ? Voici la checklist pour la carte grise.", "Jeune conducteur"),
     L("Côté *vous*", ["Pièce d'identité", "Permis de conduire", "Justificatif de domicile de moins de 6 mois"], "De votre côté : une pièce d'identité, le permis, et un justificatif de domicile récent."),
     L("Côté *vendeur*", ["Carte grise barrée et signée", "Certificat de cession", "Code de cession"], "Du côté du vendeur : la carte grise barrée, le certificat de cession, et le code de cession."),
     CTA()])

add("C019", "acquisition", "7 CV en PACA : combien coûte la carte grise ?",
    "Exemple 2026 : une 7 CV de moins de 10 ans en Provence-Alpes-Côte d'Azur = 7 × 60 € = 420 € de taxe régionale, plus 13,76 € de taxes fixes, soit 433,76 € de taxes.",
    ["paca", "marseille", "prixcartegrise"],
    [H("7 CV en PACA : *combien* ?", "car", "Une sept chevaux en Provence-Alpes-Côte d'Azur, combien coûte la carte grise ?", "Exemple 2026"),
     ST("Le calcul", ["7 CV × 60 € = 420 €", "+ 11 € de taxe fixe", "+ 2,76 € d'acheminement"], "Sept fois soixante euros, plus onze euros, plus deux euros soixante-seize."),
     S("433,76 €", "De taxes pour une *7 CV* de moins de 10 ans", "euro", "Soit quatre cent trente-trois euros soixante-seize de taxes."),
     CTA()])

add("C020", "acquisition", "Hauts-de-France : 43 € le cheval fiscal",
    "En Hauts-de-France, le cheval fiscal est passé de 42 € à 43 € au 1er avril 2026 : à égalité avec Auvergne-Rhône-Alpes pour le tarif le plus bas de métropole.",
    ["hautsdefrance", "lille", "prixcartegrise"],
    [H("Hauts-de-France : *parmi les moins chers*", "map", "Vous habitez dans les Hauts-de-France ? Votre carte grise est parmi les moins chères.", "Tarifs 2026"),
     S("43 €", "Le cheval fiscal depuis le *1er avril 2026*", "euro", "Le cheval fiscal y coûte quarante-trois euros depuis avril deux mille vingt-six."),
     S("215 €", "Taxe régionale d'une *5 CV*", "car", "Soit deux cent quinze euros pour une cinq chevaux."),
     CTA()])

add("C021", "acquisition", "Carte grise moto : même démarche qu'une voiture",
    "Vous achetez une moto d'occasion ? La démarche de changement de titulaire est la même que pour une voiture : 1 mois, certificat de cession, carte grise barrée.",
    ["moto", "motooccasion", "changementdetitulaire"],
    [H("Une *moto* d'occasion ?", "moto", "Vous achetez une moto d'occasion ? La carte grise suit les mêmes règles.", "Motards"),
     L("Les *mêmes règles*", ["1 mois pour la faire à votre nom", "Certificat de cession", "Carte grise barrée et signée"], "Un mois pour la faire à votre nom, le certificat de cession, et la carte grise barrée."),
     CTA()])

add("C022", "acquisition", "Achat en fin de mois : calculez bien votre délai",
    "Achetée le 31 octobre ? Le délai d'un mois court à partir de la date de vente indiquée sur le certificat de cession. Ne le laissez pas filer.",
    ["voitureoccasion", "delai"],
    [H("Achetée le *31* ? Attention", "calendar", "Vous avez acheté votre voiture en fin de mois ? Attention au délai.", None),
     P("Le compteur part de la *date de vente*", "Celle inscrite sur le certificat de cession.", "doc", "Le délai d'un mois commence à la date inscrite sur le certificat de cession."),
     P("Faites-la *dès la première semaine*", "Vous gardez de la marge en cas de pièce manquante.", "check", "Le bon réflexe : faites-la dès la première semaine."),
     CTA()])

add("C023", "acquisition", "Le vendeur n'a pas déclaré la cession : que faire ?",
    "Sans déclaration de cession, pas de code de cession. Demandez au vendeur de déclarer la vente : c'est une obligation dans les 15 jours.",
    ["codedecession", "voitureoccasion", "declarationdecession"],
    [H("Pas de *code de cession* ?", "key", "Le vendeur ne vous a pas donné de code de cession ?", "Problème fréquent"),
     P("Le vendeur doit *déclarer la vente*", "C'est obligatoire, dans les 15 jours.", "swap", "Il doit déclarer la vente. C'est obligatoire, dans les quinze jours."),
     P("Le code arrive *ensuite*", "Il vous le transmet pour votre carte grise.", "check", "Le code de cession arrive ensuite, et il vous le transmet."),
     CTA()])

add("C024", "acquisition", "Voiture importée : les pièces en plus",
    "Une voiture achetée à l'étranger demande des pièces supplémentaires pour l'immatriculation en France, notamment le quitus fiscal et un justificatif de conformité.",
    ["import", "voitureimportee", "allemagne"],
    [H("Voiture achetée *à l'étranger* ?", "plate", "Vous avez acheté votre voiture à l'étranger ?", "Import"),
     L("Des pièces *en plus*", ["Quitus fiscal", "Justificatif de conformité", "Carte grise étrangère"], "Il faut des pièces en plus : le quitus fiscal, un justificatif de conformité, et la carte grise étrangère."),
     CTA("Immatriculation *import*", "On vous indique les pièces selon votre cas", "Calculez votre prix sur cartegrise4x.fr.")])

add("C025", "acquisition", "Électrique : le tarif dépend de la région",
    "Carte grise d'une voiture électrique : l'exonération n'est plus automatique partout, chaque région fixe sa règle. Vérifiez le tarif de votre département avant d'acheter.",
    ["voitureelectrique", "electrique", "prixcartegrise"],
    [H("Électrique : carte grise *gratuite* ?", "car", "Une voiture électrique, la carte grise est gratuite ? Plus forcément.", "Électrique"),
     P("Chaque *région* décide", "Exonération totale, partielle, ou tarif plein.", "map", "Aujourd'hui, chaque région décide de sa règle."),
     P("Vérifiez *avant d'acheter*", None, "check", "Vérifiez le tarif avant d'acheter."),
     CTA("Le tarif *électrique* chez vous", "Selon votre département", "Calculez votre prix sur cartegrise4x.fr.")])

add("C026", "acquisition", "Combien de chevaux fiscaux a votre voiture ?",
    "Citadine, compacte, SUV : la puissance fiscale change tout au prix de la carte grise. Une citadine est souvent autour de 4 à 5 CV, un SUV peut dépasser 7 CV. Vérifiez la case P.6.",
    ["chevalfiscal", "prixcartegrise"],
    [H("Chaque *cheval* se paie", "car", "Sur une carte grise, chaque cheval fiscal se paie.", None),
     V("À 60 € le cheval", ("Citadine 4 CV", "240 € de taxe régionale"), ("SUV 8 CV", "480 € de taxe régionale"), "À soixante euros le cheval, une quatre chevaux paie deux cent quarante euros, une huit chevaux quatre cent quatre-vingts."),
     CTA()])

add("C027", "acquisition", "Déménagement + achat de voiture : une seule démarche",
    "Vous déménagez et achetez une voiture en même temps ? La nouvelle carte grise est faite directement à votre nouvelle adresse.",
    ["demenagement", "voitureoccasion"],
    [H("Nouvelle maison *et* nouvelle voiture ?", "house", "Vous déménagez et vous achetez une voiture en même temps ?", None),
     P("Une seule *carte grise*", "Faite directement à votre nouvelle adresse.", "doc", "Une seule carte grise, faite directement à votre nouvelle adresse."),
     P("Le tarif : celui de votre *nouveau département*", None, "map", "Avec le tarif de votre nouveau département."),
     CTA()])

add("C028", "acquisition", "Acheter une voiture : le budget oublié",
    "Prix de la voiture, assurance, plein... et la carte grise. Pensez à l'intégrer à votre budget dès le départ : selon la région et la puissance, elle peut dépasser 400 €.",
    ["budget", "voitureoccasion", "achatvoiture"],
    [H("Le coût que *tout le monde oublie*", "euro", "Quand on achète une voiture, il y a un coût que tout le monde oublie.", "Budget voiture"),
     L("Votre budget", ["Le prix de la voiture", "L'assurance", "Le plein", "✗ La carte grise"], "Le prix, l'assurance, le plein, et la carte grise."),
     P("Elle peut dépasser *400 €*", "Selon votre région et la puissance du véhicule.", "euro", "Selon la région et la puissance, elle peut dépasser quatre cents euros."),
     CTA("Connaissez le prix *avant d'acheter*", "Simulation gratuite", "Calculez votre prix avant d'acheter sur cartegrise4x.fr.")])

# ======================= PÉDAGOGIE ============================================================
add("C029", "pedagogie", "Déclaration de cession : 15 jours pour le vendeur",
    "Vous vendez votre voiture ? Vous avez 15 jours pour déclarer la cession. Elle vous protège des amendes et des infractions commises après la vente.",
    ["declarationdecession", "vendresavoiture"],
    [H("Vous vendez ? *15 jours* chrono", "clock", "Vous vendez votre voiture ? Vous avez quinze jours.", "Vendeurs"),
     S("15 jours", "Pour *déclarer la cession*", "calendar", "Quinze jours pour déclarer la cession."),
     P("Elle vous *protège*", "Amendes et infractions après la vente ne sont plus pour vous.", "shield", "Elle vous protège des amendes reçues après la vente."),
     CTA("Déclarez *votre cession* en ligne", "Simple et rapide", "Déclarez votre cession sur cartegrise4x.fr.")])

add("C030", "pedagogie", "Certificat de cession : l'heure de la vente compte",
    "Sur le certificat de cession, indiquez la date ET l'heure de la vente. Si un excès de vitesse est flashé le jour même, c'est l'heure qui détermine qui était responsable.",
    ["certificatdecession", "vendresavoiture", "astuce"],
    [H("Le détail qui peut vous *coûter un PV*", "warn", "Sur le certificat de cession, un détail peut vous coûter une amende.", None),
     P("Notez *l'heure* de la vente", "Pas seulement la date.", "clock", "Notez l'heure de la vente, pas seulement la date."),
     P("Flash le jour même ?", "L'heure dit qui conduisait : le vendeur ou l'acheteur.", "car", "En cas de flash le jour même, l'heure indique qui était responsable."),
     CTA()])

add("C031", "pedagogie", "Comment barrer une carte grise",
    "Pour vendre votre voiture, barrez la carte grise d'un trait, inscrivez « Vendu le … à … (heure) » et signez.",
    ["vendresavoiture", "cartegrise", "tuto"],
    [H("Barrer sa carte grise : *la bonne méthode*", "doc", "Vous vendez votre voiture ? Voici comment barrer la carte grise.", "Tuto"),
     ST("Les 3 gestes", ["Un trait en diagonale", "« Vendu le … à … » avec l'heure", "Votre signature"], "Un trait en diagonale. La mention vendu le, à, avec l'heure. Et votre signature."),
     CTA()])

add("C032", "pedagogie", "Changement d'adresse : 1 mois pour mettre à jour",
    "Vous avez déménagé ? Vous avez 1 mois pour mettre à jour l'adresse de votre carte grise.",
    ["demenagement", "changementdadresse"],
    [H("Vous avez *déménagé* ?", "house", "Vous avez déménagé récemment ?", None),
     S("1 mois", "Pour mettre à jour *l'adresse* de la carte grise", "calendar", "Vous avez un mois pour changer l'adresse sur votre carte grise."),
     P("Sinon, *amende* possible", "Et vos courriers officiels partent à l'ancienne adresse.", "warn", "Sinon, une amende est possible, et vos courriers partent à l'ancienne adresse."),
     CTA("Changez *votre adresse* en ligne", None, "Changez votre adresse sur cartegrise4x.fr.")])

add("C033", "pedagogie", "Changement d'adresse : l'étiquette 3 fois maximum",
    "Après un changement d'adresse, vous recevez une étiquette à coller sur la carte grise. Au bout de 3 étiquettes, la 4e adresse donne lieu à une nouvelle carte grise.",
    ["changementdadresse", "demenagement"],
    [H("Changement d'adresse : *une étiquette*", "doc", "Quand vous changez d'adresse, vous recevez une simple étiquette.", "Bon à savoir"),
     S("3", "Étiquettes *maximum* sur une carte grise", "doc", "On peut en coller trois au maximum."),
     P("Au *4e* déménagement", "Une nouvelle carte grise est éditée.", "house", "Au quatrième changement, une nouvelle carte grise est éditée."),
     CTA()])

add("C034", "pedagogie", "Carte grise perdue ou volée : le duplicata",
    "Carte grise perdue ou volée ? Il faut demander un duplicata. En cas de vol, une déclaration de vol est nécessaire.",
    ["duplicata", "cartegrise"],
    [H("Carte grise *perdue* ?", "question", "Vous avez perdu votre carte grise ?", None),
     V("Deux cas", ("Perte", "Déclaration de perte, puis demande de duplicata"), ("Vol", "Déclaration de vol, puis demande de duplicata"), "En cas de perte comme de vol, une déclaration, puis un duplicata."),
     CTA("Demandez *votre duplicata*", None, "Faites votre demande sur cartegrise4x.fr.")])

add("C035", "pedagogie", "Les 3 cerfa à connaître",
    "Les 3 cerfa de la carte grise : 13750 (demande d'immatriculation), 15776 (certificat de cession) et 13757 (mandat d'immatriculation).",
    ["cerfa", "demarches"],
    [H("*3 cerfa* à connaître", "doc", "Carte grise : trois cerfa à connaître.", None),
     L("Les numéros", ["13750 : demande d'immatriculation", "15776 : certificat de cession", "13757 : mandat"], "Le treize sept cent cinquante pour la demande. Le quinze sept cent soixante-seize pour la cession. Le treize sept cent cinquante-sept pour le mandat."),
     P("Bonne nouvelle", "Chez CarteGrise4x, ils sont *pré-remplis*.", "check", "Bonne nouvelle : chez nous, ils sont pré-remplis."),
     CTA()])

add("C036", "pedagogie", "Le mandat cerfa 13757, à quoi sert-il ?",
    "Le mandat (cerfa 13757) autorise un professionnel habilité à faire la démarche de carte grise en votre nom.",
    ["cerfa", "mandat"],
    [H("Pourquoi on vous fait *signer un mandat* ?", "doc", "Pourquoi on vous demande de signer un mandat ?", None),
     P("Le *cerfa 13757*", "Il autorise un professionnel habilité à agir pour vous.", "shield", "Le cerfa treize sept cent cinquante-sept autorise un professionnel habilité à faire la démarche pour vous."),
     P("C'est *obligatoire*", "Pour toute démarche faite par un professionnel.", "check", "Il est obligatoire pour toute démarche faite par un professionnel."),
     CTA()])

add("C037", "pedagogie", "Justificatif de domicile : moins de 6 mois",
    "Pour votre carte grise, le justificatif de domicile doit dater de moins de 6 mois : facture d'énergie, d'internet, avis d'imposition, quittance de loyer d'un professionnel...",
    ["justificatif", "demarches"],
    [H("Votre justificatif est *trop vieux* ?", "house", "Votre justificatif de domicile est peut-être trop ancien.", None),
     S("6 mois", "Âge maximum du *justificatif de domicile*", "calendar", "Il doit dater de moins de six mois."),
     L("Exemples acceptés", ["Facture d'énergie", "Facture internet ou téléphone", "Avis d'imposition"], "Une facture d'énergie, d'internet, ou un avis d'imposition."),
     CTA()])

add("C038", "pedagogie", "Mythe : « On a 3 mois pour faire la carte grise »",
    "Faux ! Après l'achat d'un véhicule d'occasion, vous avez 1 mois, pas 3, pour faire la carte grise à votre nom.",
    ["mythe", "voitureoccasion"],
    [H("« On a *3 mois* » ?", "question", "On a trois mois pour faire sa carte grise ? Vrai ou faux ?", "Vrai ou faux"),
     V(None, ("Mythe", "3 mois après l'achat"), ("Réalité", "1 mois après la date de vente"), "Faux. Vous avez un mois après la date de vente."),
     CTA()])

add("C039", "pedagogie", "Mythe : « C'est au vendeur de faire la carte grise »",
    "Faux ! Le vendeur déclare la cession. C'est l'acheteur qui fait la nouvelle carte grise à son nom.",
    ["mythe", "voitureoccasion"],
    [H("« C'est au *vendeur* de la faire » ?", "question", "C'est au vendeur de faire la carte grise ? Vrai ou faux ?", "Vrai ou faux"),
     V(None, ("Mythe", "Le vendeur fait la carte grise"), ("Réalité", "L'acheteur la fait à son nom"), "Faux. C'est l'acheteur qui fait la carte grise à son nom."),
     CTA()])

add("C040", "pedagogie", "Site privé ou site officiel : ce qu'il faut savoir",
    "La démarche de carte grise est possible sans frais de service sur le site officiel de France Titres. Un professionnel habilité comme CarteGrise4x propose un accompagnement payant : vérification du dossier et cerfa pré-remplis. Service privé, non affilié à l'ANTS.",
    ["transparence", "ants", "francetitres"],
    [H("Site privé ou officiel : *la vérité*", "shield", "Site privé ou site officiel pour sa carte grise ? On vous dit tout.", "Transparence"),
     V(None, ("Site officiel", "Sans frais de service, vous faites tout vous-même"), ("CarteGrise4x", "Service payant : dossier vérifié, cerfa pré-remplis"), "Sur le site officiel, c'est sans frais de service et vous faites tout vous-même. Chez nous, vous payez un accompagnement."),
     P("Les *taxes* sont les mêmes", "Fixées par l'État et votre région.", "euro", "Les taxes, elles, sont les mêmes partout."),
     CTA("À vous de *choisir*", "Service privé, non affilié à l'ANTS", "À vous de choisir. Calculez votre prix sur cartegrise4x.fr.")])

add("C041", "pedagogie", "Lire sa carte grise : les cases utiles",
    "Les cases à connaître : A (immatriculation), B (date de 1re immatriculation), E (numéro VIN), P.6 (puissance fiscale), V.7 (CO2).",
    ["cartegrise", "tuto"],
    [H("Votre carte grise *décodée*", "doc", "Votre carte grise, décodée en quelques secondes.", None),
     L("Les cases utiles", ["A : immatriculation", "B : 1re immatriculation", "E : numéro VIN", "P.6 : puissance fiscale", "V.7 : émissions de CO2"], "A, l'immatriculation. B, la première mise en circulation. E, le numéro de série. P six, la puissance fiscale. V sept, le CO2."),
     CTA()])

add("C042", "pedagogie", "Le numéro VIN : vérifiez-le avant d'acheter",
    "Le numéro VIN (case E de la carte grise) est l'identifiant unique du véhicule. Il doit correspondre à celui gravé sur la voiture.",
    ["vin", "voitureoccasion", "arnaque"],
    [H("Le contrôle *anti-arnaque* en 30 s", "shield", "Un contrôle anti-arnaque en trente secondes avant d'acheter.", None),
     P("Le *VIN* case E", "17 caractères, uniques à chaque véhicule.", "doc", "Le numéro de série, case E, dix-sept caractères uniques."),
     P("Comparez-le à *la voiture*", "Souvent visible au pare-brise ou sur le châssis.", "car", "Comparez-le à celui de la voiture, souvent visible au pare-brise."),
     CTA()])

add("C043", "pedagogie", "Retard de carte grise : jusqu'à 750 € d'amende",
    "Ne pas faire la carte grise à son nom dans le mois est une contravention de 4e classe : 135 € d'amende forfaitaire, jusqu'à 750 €.",
    ["amende", "voitureoccasion"],
    [H("Carte grise en retard ? *Jusqu'à 750 €*", "warn", "Carte grise pas faite dans le mois ? Attention à l'amende.", "Amende"),
     S("135 €", "Amende *forfaitaire* (4e classe)", "euro", "L'amende forfaitaire est de cent trente-cinq euros."),
     S("750 €", "Montant *maximum*", "warn", "Elle peut monter jusqu'à sept cent cinquante euros."),
     CTA("Évitez l'amende : *faites-la maintenant*", None, "Faites votre carte grise sur cartegrise4x.fr.")])

add("C044", "pedagogie", "Les erreurs qui bloquent un dossier",
    "Les erreurs qui bloquent une carte grise : photo illisible, signature manquante, justificatif trop ancien, contrôle technique expiré, nom différent entre les documents.",
    ["erreurs", "demarches"],
    [H("*5 erreurs* qui bloquent votre dossier", "cross", "Cinq erreurs qui bloquent votre dossier de carte grise.", None),
     L("À éviter", ["✗ Photo de document illisible", "✗ Signature manquante", "✗ Justificatif de plus de 6 mois", "✗ Contrôle technique expiré", "✗ Nom différent selon les pièces"], "Une photo illisible. Une signature manquante. Un justificatif trop ancien. Un contrôle technique expiré. Un nom différent selon les pièces."),
     P("Notre équipe *vérifie avant*", None, "check", "Notre équipe vérifie votre dossier avant la saisie."),
     CTA()])

add("C045", "pedagogie", "Carte grise à deux noms : le cotitulaire",
    "Une carte grise peut être faite à deux noms : un titulaire et un cotitulaire. Les deux doivent signer la demande.",
    ["couple", "cartegrise"],
    [H("Carte grise *à deux noms* ?", "doc", "On peut mettre une carte grise à deux noms ?", None),
     P("Oui : *titulaire + cotitulaire*", "Pratique pour un couple ou une famille.", "check", "Oui : un titulaire et un cotitulaire."),
     P("Les deux *signent*", "Chacun fournit sa pièce d'identité.", "doc", "Les deux signent et fournissent leur pièce d'identité."),
     CTA()])

add("C046", "pedagogie", "Vignette Crit'Air : liée à la carte grise",
    "La vignette Crit'Air est attribuée selon les informations de la carte grise. Elle est obligatoire pour circuler dans les zones à faibles émissions (ZFE) concernées.",
    ["critair", "zfe"],
    [H("Crit'Air : *vous l'avez* ?", "shield", "Avez-vous votre vignette Crit'Air ?", "ZFE"),
     P("Calculée d'après *la carte grise*", "Énergie et date de 1re immatriculation.", "doc", "Elle dépend des informations de votre carte grise."),
     P("Obligatoire en *ZFE*", "Dans les zones concernées.", "warn", "Elle est obligatoire dans les zones à faibles émissions concernées."),
     CTA("Commandez *votre Crit'Air*", None, "Commandez-la avec votre démarche sur cartegrise4x.fr.")])

add("C047", "pedagogie", "La plaque suit la voiture à vie",
    "Depuis 2009, le numéro d'immatriculation est attribué au véhicule à vie. Il ne change pas quand vous achetez la voiture ou déménagez.",
    ["plaque", "immatriculation"],
    [H("Nouvelle voiture = *nouvelles plaques* ?", "plate", "Vous achetez une voiture : faut-il changer les plaques ?", None),
     P("Non : le numéro suit *le véhicule*", "Depuis 2009, à vie.", "plate", "Non. Depuis deux mille neuf, le numéro suit le véhicule à vie."),
     P("Même si vous *déménagez*", None, "house", "Même si vous déménagez."),
     CTA()])

add("C048", "pedagogie", "Vendre sa voiture : les documents à remettre",
    "Vous vendez ? Remettez à l'acheteur : la carte grise barrée et signée, un exemplaire du certificat de cession, le code de cession, le contrôle technique de moins de 6 mois et le certificat de situation administrative.",
    ["vendresavoiture", "checklist"],
    [H("Vous vendez ? *À remettre* à l'acheteur", "swap", "Vous vendez votre voiture ? Voici ce que vous devez remettre.", "Vendeurs"),
     L("La liste", ["Carte grise barrée et signée", "Certificat de cession", "Code de cession", "CT de moins de 6 mois", "Certificat de situation administrative"], "La carte grise barrée, le certificat de cession, le code de cession, le contrôle technique récent, et le certificat de situation administrative."),
     CTA("Déclarez *votre vente*", None, "Déclarez votre vente sur cartegrise4x.fr.")])

add("C049", "pedagogie", "Gardez votre exemplaire du certificat de cession",
    "Vendeur : gardez toujours un exemplaire du certificat de cession signé. C'est votre preuve en cas d'amende ou de litige après la vente.",
    ["certificatdecession", "vendresavoiture"],
    [H("Vendeur : *ne jetez pas* ce papier", "doc", "Vendeur, ne jetez surtout pas ce papier.", None),
     P("Votre exemplaire du *certificat de cession*", "Signé par vous et l'acheteur.", "doc", "Votre exemplaire du certificat de cession, signé par les deux."),
     P("Votre *preuve*", "En cas d'amende ou de litige après la vente.", "shield", "C'est votre preuve en cas d'amende ou de litige."),
     CTA()])

add("C050", "pedagogie", "Que contient le prix d'une carte grise ?",
    "Le prix d'une carte grise comprend : la taxe régionale (chevaux fiscaux), la taxe fixe Y.4 de 11 €, la redevance d'acheminement Y.5 de 2,76 €, et parfois un malus ou la taxe Y.2 des utilitaires.",
    ["prixcartegrise", "taxe"],
    [H("Où va *votre argent* ?", "euro", "Quand vous payez une carte grise, où va votre argent ?", None),
     L("Les taxes", ["Taxe régionale : à la région", "Taxe fixe Y.4 : 11 €", "Acheminement Y.5 : 2,76 €", "Malus éventuel"], "La taxe régionale, la taxe fixe de onze euros, l'acheminement à deux euros soixante-seize, et un éventuel malus."),
     CTA()])

add("C051", "pedagogie", "Contre-visite : le délai change",
    "Si votre contrôle technique a donné lieu à une contre-visite, la vente demande une contre-visite de moins de 2 mois.",
    ["controletechnique", "contrevisite", "vendresavoiture"],
    [H("Contre-visite ? *Autre délai*", "clock", "Votre contrôle technique a donné une contre-visite ? Le délai change.", None),
     V("Pour vendre", ("CT sans contre-visite", "Moins de 6 mois"), ("Avec contre-visite", "Contre-visite de moins de 2 mois"), "Sans contre-visite, moins de six mois. Avec contre-visite, la contre-visite doit dater de moins de deux mois."),
     CTA()])

add("C052", "pedagogie", "Plus de carte grise en préfecture depuis 2017",
    "Depuis 2017, les préfectures ne délivrent plus les cartes grises au guichet. Toutes les démarches se font en ligne.",
    ["prefecture", "demarches"],
    [H("La préfecture ? *Plus de guichet*", "house", "Vous pensiez aller en préfecture pour votre carte grise ?", None),
     S("2017", "Fin des guichets *carte grise* en préfecture", "calendar", "Depuis deux mille dix-sept, il n'y a plus de guichet carte grise en préfecture."),
     P("Tout se fait *en ligne*", "Sur le site officiel ou avec un professionnel habilité.", "phone", "Tout se fait en ligne, sur le site officiel ou avec un professionnel habilité."),
     CTA()])

add("C053", "pedagogie", "Décès du titulaire : que faire de la voiture ?",
    "Après le décès du titulaire, les héritiers doivent mettre la carte grise à leur nom ou déclarer la vente du véhicule s'ils le vendent.",
    ["succession", "demarches"],
    [H("Voiture d'un *proche décédé*", "doc", "Que faire de la voiture d'un proche décédé ?", None),
     V("Deux options", ("La garder", "Carte grise au nom de l'héritier"), ("La vendre", "Vente et déclaration de cession"), "Soit vous la gardez, avec une carte grise à votre nom. Soit vous la vendez, avec une déclaration de cession."),
     CTA("On vous *accompagne*", "Pièces indiquées selon votre situation", "Calculez votre prix sur cartegrise4x.fr.")])

add("C054", "pedagogie", "Rouler sans carte grise à jour : les risques",
    "Rouler sans carte grise à son nom au-delà d'un mois, c'est risquer une amende et des complications avec votre assurance en cas de sinistre.",
    ["amende", "assurance"],
    [H("Carte grise pas à jour : *les risques*", "warn", "Vous roulez avec une carte grise qui n'est pas à votre nom ?", None),
     L("Ce que vous risquez", ["Amende de 4e classe", "Courriers et PV au mauvais nom", "Complications avec l'assurance"], "Une amende. Des courriers au mauvais nom. Et des complications avec l'assurance."),
     CTA()])

add("C055", "pedagogie", "Véhicule neuf : qui fait la carte grise ?",
    "Pour un véhicule neuf, le concessionnaire fait souvent la carte grise. Si ce n'est pas le cas, vous pouvez la faire avec un professionnel habilité.",
    ["voitureneuve", "concession"],
    [H("Voiture *neuve* : qui fait la carte grise ?", "car", "Vous achetez une voiture neuve. Qui fait la carte grise ?", None),
     P("Souvent le *concessionnaire*", "C'est inclus dans la vente dans la plupart des cas.", "check", "Le plus souvent, c'est le concessionnaire."),
     P("Sinon, *vous*", "Avec le certificat de conformité et la facture.", "doc", "Sinon, c'est vous, avec le certificat de conformité et la facture."),
     CTA()])

add("C056", "pedagogie", "Ce qu'on ne vous dit pas sur le certificat provisoire",
    "Le certificat provisoire vous permet de circuler en France pendant 1 mois, le temps de recevoir votre carte grise définitive. Gardez-le dans la voiture.",
    ["cartegrise", "astuce"],
    [H("Le papier à garder *dans la boîte à gants*", "doc", "Le papier à garder dans la boîte à gants.", None),
     S("1 mois", "De validité pour le *certificat provisoire*", "calendar", "Le certificat provisoire est valable un mois."),
     P("Uniquement en *France*", "En attendant votre carte grise définitive.", "map", "Uniquement en France, en attendant la carte grise définitive."),
     CTA()])

# ======================= CONVERSION ===========================================================
add("C057", "conversion", "Votre carte grise en 4 étapes",
    "Votre carte grise en 4 étapes : 1. calculez votre prix, 2. remplissez un seul formulaire, 3. payez en 1 ou 4 fois selon éligibilité, 4. envoyez vos pièces : nous saisissons votre dossier.",
    ["tuto", "cartegriseenligne"],
    [H("Carte grise : *4 étapes*, c'est tout", "phone", "Votre carte grise, en quatre étapes seulement.", None),
     ST("Comment ça marche", ["Calculez votre prix", "Remplissez un seul formulaire", "Payez en 1 ou 4 fois", "Envoyez vos pièces"], "Calculez votre prix. Remplissez un seul formulaire. Payez en une ou quatre fois. Envoyez vos pièces."),
     CREDIT_CTA()], credit=True)

add("C058", "conversion", "Payer sa carte grise en 4 fois",
    "Votre carte grise payable en 4 fois avec PayPal ou Klarna sur la page de paiement, selon éligibilité. Seule la 1re échéance est prélevée le jour de la commande.",
    ["paiementen4fois", "budget"],
    [H("La carte grise *en 4 fois*", "cards", "Et si vous payiez votre carte grise en quatre fois ?", None),
     P("Avec *PayPal ou Klarna*", "Sur la page de paiement, selon éligibilité.", "cards", "Avec PayPal ou Klarna, selon éligibilité."),
     P("*1re échéance* le jour de la commande", "Les suivantes tous les 30 jours.", "calendar", "Seule la première échéance est prélevée le jour de la commande."),
     CREDIT_CTA()], credit=True)

add("C059", "conversion", "Prix affiché tout compris, selon votre département",
    "Sur CarteGrise4x, le prix est calculé selon le tarif de votre département et affiché tout compris avant le paiement : taxes et frais de service.",
    ["prixcartegrise", "transparence"],
    [H("Le prix *final*, avant de payer", "euro", "Vous voyez le prix final avant de payer.", None),
     L("Le prix inclut", ["Les taxes de votre région", "Les taxes fixes", "Nos frais de service"], "Le prix inclut les taxes de votre région, les taxes fixes, et nos frais de service."),
     P("*Aucune surprise*", "Tout est affiché avant la validation.", "check", "Tout est affiché avant la validation."),
     CTA()])

add("C060", "conversion", "Dossier complet traité sous 12 h ouvrées",
    "Chez CarteGrise4x, un dossier complet est traité sous 12 h ouvrées.",
    ["rapide", "cartegriseenligne"],
    [H("Dossier traité *sous 12 h ouvrées*", "clock", "Votre dossier complet, traité sous douze heures ouvrées.", None),
     S("12 h", "Dossier complet traité *sous 12 h ouvrées*", "clock", "Dossier complet traité sous douze heures ouvrées."),
     P("Puis le *certificat provisoire*", "Dès l'enregistrement de votre demande.", "doc", "Puis vous recevez le certificat provisoire dès l'enregistrement."),
     CTA()])

add("C061", "conversion", "Professionnel habilité SIV",
    "CarteGrise4x est un professionnel habilité SIV : nous saisissons directement votre demande dans le système d'immatriculation des véhicules. Service privé, non affilié à l'ANTS.",
    ["habilite", "siv"],
    [H("Qui saisit *votre dossier* ?", "shield", "Qui saisit votre demande de carte grise ?", None),
     P("Un professionnel *habilité SIV*", "Autorisé à saisir dans le système d'immatriculation.", "shield", "Un professionnel habilité S I V, autorisé à saisir votre demande."),
     P("Service *privé*", "Non affilié à l'ANTS.", "check", "Nous sommes un service privé, non affilié à l'A N T S."),
     CTA()])

add("C062", "conversion", "Les cerfa pré-remplis pour vous",
    "Plus besoin de chercher le bon cerfa : chez CarteGrise4x, vous remplissez un seul formulaire et les cerfa sont pré-remplis.",
    ["cerfa", "simplicite"],
    [H("Les cerfa ? *On s'en occupe*", "doc", "Les cerfa, c'est compliqué ? On s'en occupe.", None),
     V(None, ("Seul", "Trouver le bon cerfa, le remplir, le scanner"), ("Avec nous", "Un formulaire, cerfa pré-remplis"), "Seul, il faut trouver le bon cerfa et le remplir. Avec nous, un seul formulaire, et les cerfa sont pré-remplis."),
     CTA()])

add("C063", "conversion", "Une équipe vérifie votre dossier",
    "Avant la saisie, notre équipe vérifie vos pièces pour éviter un refus ou un blocage.",
    ["accompagnement", "cartegriseenligne"],
    [H("Votre dossier *vérifié* avant envoi", "check", "Votre dossier est vérifié avant d'être saisi.", None),
     L("On vérifie", ["La lisibilité des pièces", "Les signatures", "La validité du contrôle technique", "Le justificatif de domicile"], "On vérifie la lisibilité, les signatures, le contrôle technique, et le justificatif de domicile."),
     CTA()])

add("C064", "conversion", "Sans vous déplacer, depuis votre téléphone",
    "Votre carte grise sans vous déplacer : formulaire, paiement et envoi des pièces se font en ligne, depuis votre téléphone.",
    ["cartegriseenligne", "mobile"],
    [H("Votre carte grise *depuis le canapé*", "phone", "Votre carte grise depuis votre canapé.", None),
     L("Tout en ligne", ["Le formulaire", "Le paiement", "L'envoi des pièces"], "Le formulaire, le paiement, l'envoi des pièces : tout se fait en ligne."),
     P("La carte grise arrive *chez vous*", None, "house", "Et la carte grise arrive chez vous."),
     CTA()])

add("C065", "conversion", "Une carte grise à 400 € ? Étalez le paiement",
    "Une carte grise à 400 € ? Avec le paiement en 4 fois (PayPal ou Klarna, selon éligibilité), cela fait 4 échéances de 100 €. Seule la 1re est prélevée le jour de la commande.",
    ["paiementen4fois", "budget"],
    [H("400 € d'un coup ? *Ou 4 × 100 €*", "cards", "Quatre cents euros d'un coup ? Ou quatre fois cent euros.", "Exemple"),
     S("4 × 100 €", "Pour une carte grise à *400 €*", "cards", "Pour une carte grise à quatre cents euros, quatre échéances de cent euros."),
     P("Selon *éligibilité*", "PayPal ou Klarna décident de l'acceptation.", "shield", "Sous réserve d'acceptation par PayPal ou Klarna."),
     CREDIT_CTA()], credit=True)

add("C066", "conversion", "Déclaration de cession en ligne",
    "Vous vendez votre voiture ? Faites votre déclaration de cession en ligne avec CarteGrise4x et récupérez le code de cession pour l'acheteur.",
    ["declarationdecession", "vendresavoiture"],
    [H("Déclarer *la vente* de sa voiture", "swap", "Vous avez vendu votre voiture ? Déclarez la vente en ligne.", "Vendeurs"),
     ST("Avec nous", ["Remplissez le formulaire", "Joignez le certificat de cession", "Recevez le code de cession"], "Remplissez le formulaire. Joignez le certificat de cession. Recevez le code de cession."),
     CTA("Déclarez *votre cession*", None, "Déclarez votre cession sur cartegrise4x.fr.")])

add("C067", "conversion", "Changement d'adresse en ligne",
    "Vous avez déménagé ? Mettez à jour l'adresse de votre carte grise en ligne, sans vous déplacer.",
    ["changementdadresse", "demenagement"],
    [H("Déménagé ? *Mettez à jour* en 3 min", "house", "Vous avez déménagé ? Mettez à jour votre carte grise.", None),
     ST("En ligne", ["Votre nouvelle adresse", "Un justificatif de domicile", "Votre carte grise actuelle"], "Votre nouvelle adresse, un justificatif de domicile, et votre carte grise actuelle."),
     CTA("Changez *d'adresse*", None, "Changez votre adresse sur cartegrise4x.fr.")])

add("C068", "conversion", "Calculer le prix de sa carte grise en 30 secondes",
    "Calculez le prix de votre carte grise en 30 secondes : département, puissance fiscale, date de 1re immatriculation et type de démarche.",
    ["prixcartegrise", "simulateur"],
    [H("Votre prix en *30 secondes*", "clock", "Le prix de votre carte grise en trente secondes.", None),
     ST("Il vous faut", ["Votre département", "La puissance fiscale (P.6)", "La date de 1re immatriculation (B)", "Le type de démarche"], "Votre département, la puissance fiscale, la date de première immatriculation, et le type de démarche."),
     CTA("Faites *le calcul*", "Gratuit et sans engagement", "Faites le calcul sur cartegrise4x.fr.")])

add("C069", "conversion", "CarteGrise4x, c'est l'ANTS ?",
    "Non. CarteGrise4x est un service privé, non affilié à l'ANTS. Nous sommes un professionnel habilité qui fait la démarche pour vous, contre des frais de service affichés avant paiement.",
    ["faq", "transparence"],
    [H("CarteGrise4x, *c'est l'ANTS* ?", "question", "On nous demande souvent : CarteGrise4x, c'est l'ANTS ?", "FAQ"),
     P("*Non*, service privé", "Non affilié à l'ANTS.", "shield", "Non. Nous sommes un service privé, non affilié à l'A N T S."),
     P("Un professionnel *habilité*", "Frais de service affichés avant paiement.", "check", "Un professionnel habilité, avec des frais affichés avant le paiement."),
     CTA()])

add("C070", "conversion", "Toutes les démarches de carte grise",
    "Changement de titulaire, déclaration de cession, changement d'adresse, duplicata, véhicule neuf, import, W garage : toutes vos démarches de carte grise en ligne.",
    ["demarches", "cartegriseenligne"],
    [H("*Toutes* vos démarches au même endroit", "doc", "Toutes vos démarches de carte grise au même endroit.", None),
     L("Démarches", ["Changement de titulaire", "Déclaration de cession", "Changement d'adresse", "Duplicata", "Véhicule neuf ou importé"], "Changement de titulaire, cession, adresse, duplicata, véhicule neuf ou importé."),
     CTA()])

add("C071", "conversion", "Paiement sécurisé",
    "Le paiement se fait sur des pages sécurisées : carte bancaire, PayPal ou Klarna. Le paiement en 4 fois est soumis à éligibilité.",
    ["paiement", "securite"],
    [H("Payer en ligne, *en sécurité*", "shield", "Payer sa carte grise en ligne, en toute sécurité.", None),
     L("Moyens de paiement", ["Carte bancaire", "PayPal", "Klarna"], "Carte bancaire, PayPal ou Klarna."),
     P("Pages de paiement *sécurisées*", "Gérées par nos prestataires de paiement.", "shield", "Sur des pages de paiement sécurisées."),
     CREDIT_CTA()], credit=True)

add("C072", "conversion", "1re échéance seulement le jour de la commande",
    "En paiement en 4 fois (PayPal ou Klarna, selon éligibilité), seule la 1re échéance est prélevée le jour de la commande, puis une échéance tous les 30 jours.",
    ["paiementen4fois", "budget"],
    [H("Aujourd'hui, vous payez *1/4*", "cards", "Aujourd'hui, vous ne payez qu'un quart.", None),
     ST("Les échéances", ["Jour de la commande : 1re échéance", "+30 jours : 2e échéance", "+60 jours : 3e échéance", "+90 jours : 4e échéance"], "La première le jour de la commande, puis une tous les trente jours."),
     CREDIT_CTA()], credit=True)

add("C073", "conversion", "Le changement de titulaire avec CarteGrise4x",
    "Changement de titulaire avec CarteGrise4x : un seul formulaire, cerfa pré-remplis, dossier vérifié, certificat provisoire dès l'enregistrement.",
    ["changementdetitulaire", "voitureoccasion"],
    [H("Changement de titulaire, *simplifié*", "swap", "Le changement de titulaire, en version simple.", None),
     L("Ce que vous avez", ["Un seul formulaire", "Des cerfa pré-remplis", "Un dossier vérifié", "Le certificat provisoire"], "Un seul formulaire, des cerfa pré-remplis, un dossier vérifié, et le certificat provisoire."),
     CTA()])

add("C074", "conversion", "Duplicata de carte grise en ligne",
    "Carte grise perdue, volée ou abîmée ? Demandez votre duplicata en ligne avec CarteGrise4x.",
    ["duplicata"],
    [H("Carte grise *abîmée* ou perdue ?", "doc", "Votre carte grise est perdue, volée ou abîmée ?", None),
     P("Demandez un *duplicata*", "En ligne, sans vous déplacer.", "phone", "Demandez un duplicata, en ligne."),
     P("Gardez le *certificat provisoire*", "En attendant le nouveau titre.", "doc", "En attendant, vous avez un certificat provisoire."),
     CTA("Votre *duplicata*", None, "Faites votre demande sur cartegrise4x.fr.")])

add("C075", "conversion", "Pourquoi « 4x » dans CarteGrise4x ?",
    "Le 4x de CarteGrise4x, c'est le paiement en 4 fois avec PayPal ou Klarna, selon éligibilité.",
    ["cartegrise4x", "paiementen4fois"],
    [H("Pourquoi *« 4x »* ?", "question", "Pourquoi carte grise quatre x ?", None),
     S("4x", "Comme payable *en 4 fois*", "cards", "Quatre x, comme payable en quatre fois."),
     P("PayPal ou Klarna", "Selon éligibilité.", "cards", "Avec PayPal ou Klarna, selon éligibilité."),
     CREDIT_CTA()], credit=True)

add("C076", "conversion", "Vous achetez ce week-end ? Préparez la carte grise",
    "Vous achetez une voiture ce week-end ? Calculez dès maintenant le prix de la carte grise et préparez les pièces.",
    ["voitureoccasion", "weekend"],
    [H("Achat *ce week-end* ?", "car", "Vous achetez une voiture ce week-end ?", None),
     ST("Avant le rendez-vous", ["Calculez le prix de la carte grise", "Vérifiez la checklist des pièces", "Demandez le code de cession"], "Calculez le prix, vérifiez la checklist, et demandez le code de cession."),
     CTA()])

add("C077", "conversion", "Carte grise étudiante : étaler le coût",
    "Étudiant et première voiture ? Le paiement en 4 fois avec PayPal ou Klarna (selon éligibilité) permet d'étaler le coût de la carte grise. Un crédit vous engage et doit être remboursé.",
    ["etudiant", "premierevoiture", "paiementen4fois"],
    [H("Étudiant, *première voiture* ?", "key", "Étudiant, première voiture ? Pensez au coût de la carte grise.", None),
     P("Étalez en *4 fois*", "PayPal ou Klarna, selon éligibilité.", "cards", "Vous pouvez étaler le paiement en quatre fois, selon éligibilité."),
     P("Vérifiez votre *budget*", "Chaque échéance doit rester supportable.", "check", "Vérifiez que chaque échéance reste dans votre budget."),
     CREDIT_CTA()], credit=True)

add("C078", "conversion", "W garage : immatriculation provisoire",
    "Professionnels de l'automobile : faites vos démarches W garage en ligne avec CarteGrise4x.",
    ["wgarage", "professionnel", "garage"],
    [H("Garages : le *W garage* en ligne", "plate", "Vous êtes garagiste ? Le W garage se fait aussi en ligne.", "Pros"),
     P("Pour les *professionnels*", "Essais, livraisons et transferts de véhicules.", "car", "Pour les professionnels de l'automobile."),
     CTA("Démarches *pros*", None, "Faites vos démarches sur cartegrise4x.fr.")])

add("C079", "conversion", "Combien de temps pour faire la démarche ?",
    "Avec CarteGrise4x : quelques minutes pour remplir le formulaire, et un dossier complet traité sous 12 h ouvrées.",
    ["rapide", "cartegriseenligne"],
    [H("Ça prend *combien de temps* ?", "clock", "Faire sa carte grise en ligne, ça prend combien de temps ?", None),
     V(None, ("Vous", "Quelques minutes de formulaire"), ("Nous", "Dossier complet traité sous 12 h ouvrées"), "De votre côté, quelques minutes. De notre côté, un dossier complet traité sous douze heures ouvrées."),
     CTA()])

add("C080", "conversion", "Une question sur votre démarche ?",
    "Un doute sur votre démarche de carte grise ? Posez votre question en commentaire, on vous répond.",
    ["faq", "question"],
    [H("Une *question* sur votre carte grise ?", "question", "Vous avez une question sur votre carte grise ?", None),
     P("Posez-la *en commentaire*", "On vous répond.", "phone", "Posez-la en commentaire, on vous répond."),
     L("Les plus fréquentes", ["Quel délai ?", "Quels documents ?", "Quel prix ?"], "Délai, documents, prix : on vous explique tout."),
     CTA()])

add("C081", "conversion", "Vendeur pro ou particulier : on s'adapte",
    "Achat chez un particulier, vente, déménagement ou import : CarteGrise4x vous indique les pièces selon votre situation.",
    ["accompagnement"],
    [H("Votre situation est *particulière* ?", "question", "Votre situation est particulière ?", None),
     L("On vous guide", ["Achat entre particuliers", "Vente de votre voiture", "Déménagement", "Véhicule importé"], "Achat, vente, déménagement ou import : on vous guide."),
     CTA()])

add("C082", "conversion", "Récap : votre carte grise sans stress",
    "Le récap : 1 mois pour la faire, prix selon votre région, un seul formulaire, dossier vérifié, paiement en 1 ou 4 fois selon éligibilité.",
    ["recap", "cartegriseenligne"],
    [H("Carte grise *sans stress* : le récap", "check", "La carte grise sans stress, le récap.", None),
     L("À retenir", ["1 mois après l'achat", "Prix selon votre région", "Un seul formulaire", "Dossier vérifié", "Paiement en 1 ou 4 fois"], "Un mois après l'achat. Prix selon votre région. Un seul formulaire. Dossier vérifié. Paiement en une ou quatre fois."),
     CREDIT_CTA()], credit=True)

add("C083", "conversion", "Changement de titulaire : votre prix maintenant",
    "Vous venez d'acheter ? Calculez maintenant le prix de votre changement de titulaire, selon votre département et votre véhicule.",
    ["changementdetitulaire", "prixcartegrise"],
    [H("Vous venez *d'acheter* ?", "car", "Vous venez d'acheter une voiture ? Félicitations.", None),
     P("Calculez votre *prix exact*", "Département, chevaux fiscaux, âge du véhicule.", "euro", "Calculez maintenant votre prix exact."),
     P("Faites-la *dans le mois*", None, "calendar", "Et faites la carte grise dans le mois."),
     CTA()])

if __name__ == "__main__":
    assert len(C) == 83, len(C)
    assert len({c["id"] for c in C}) == 83
    json.dump(C, open("concepts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from collections import Counter; print(len(C), Counter(c["category"] for c in C))
