# logique.py

def get_next_question_id(r):
    """
    Fonction pilotée par graphe logique complet.
    """
    if 0 not in r:
        return 0  # Montant
    if r[0] < 500:
        return None

    if 1 not in r:
        return 1  # Bien physique ?

    if r[1] == "Oui":  # Branche corporelle
        for q in [2, 3, 4, 5]:
            if q not in r:
                return q
            if r[q] == "Non":
                return None

        if 6 not in r:
            return 6

        if r[6] == "Oui":
            return None

        if 7 not in r:
            return 7

        if r[7] == "Oui":
            if 8 not in r:
                return 8
            if r[8] == "Oui":  # Frais d'étude
                if 9 not in r:
                    return 9
                return None
            elif r[8] == "Non":
                if 10 not in r:
                    return 10
                if r[10] == "Oui":
                    return None
                if 11 not in r:
                    return 11
                if r[11] == "Oui":
                    return None
                for q in [12, 13]:
                    if q not in r:
                        return q
                return None
        elif r[7] == "Non":
            if 10 not in r:
                return 10
            if r[10] == "Non":
                return None
            if 11 not in r:
                return 11
            if r[11] == "Non":
                return None
            if 12 not in r:
                return 12
            if r[12] == "Non":
                return None
            if 13 not in r:
                return 13
            return None

    else:  # Branche incorporelle
        for q in [15, 16, 17, 18]:
            if q not in r:
                return q
            if r[q] == "Non":
                return None

        if 19 not in r:
            return 19

        if r[19] == "Acquisition":
            if 20 not in r:
                return 20
            if r[20] == "Non":
                return None
            for q in [21, 22, 23, 24]:
                if q not in r:
                    return q
                if q != 24 and r[q] == "Non":
                    return None
            return None

        elif r[19] == "Création en interne":
            if 25 not in r:
                return 25
            if r[25] == "Recherche":
                return None
            for q in [26, 27, 28, 29, 30, 31]:
                if q not in r:
                    return q
            return None

        elif r[19] == "Dépense liée à un actif":
            if 32 not in r:
                return 32
            if r[32] == "Dépense":
                if 33 not in r:
                    return 33
                return None
            if r[32] == "Maintenance":
                if 34 not in r:
                    return 34
                if r[34] == "Après":
                    if 35 not in r:
                        return 35
                elif r[34] == "Avant":
                    if 36 not in r:
                        return 36
            return None

    return None


def evaluate_final_result(r):
    justif = []
    if r.get(0) is not None and r.get(0) < 500:
        return "Charge", ["Montant < 500 DT"]

    if r.get(1) == "Oui":
        if any(r.get(x) == "Non" for x in [2, 3, 4, 5]):
            return "Charge", ["Critères de base non remplis"]

        if r.get(6) == "Oui":
            return "Immobilisation corporelle", ["Nouvelle acquisition"]

        if r.get(7) == "Oui":
            if r.get(8) == "Oui":
                if r.get(9) == "Oui":
                    return "Immobilisation corporelle", ["Frais d'étude liés à actif durable"]
                else:
                    return "Charge", ["Frais d'étude non liés à actif"]

        if any(r.get(x) == "Non" for x in [10, 11]):
            return "Charge", ["Réparation non éligible"]

        if r.get(12) == "Réhabilitation majeure d'infrastructures":
            return "Immobilisation corporelle", ["Réhabilitation majeure"]
        elif r.get(12) == "Réparation":
            if r.get(13) == "Oui":
                return "Immobilisation corporelle", ["Réparation cyclique"]
            else:
                return "Charge", ["Réparation ponctuelle"]

    elif r.get(1) == "Non":
        if any(r.get(x) == "Non" for x in [15, 16, 17, 18]):
            return "Charge", ["Critères incorporels non remplis"]

        if r.get(19) == "Acquisition":
            if r.get(20) == "Non":
                return "Immobilisation incorporelle", ["Acquisition non liée à une licence"]
            if any(r.get(x) == "Non" for x in [21, 22, 23]):
                return "Charge", ["Licence ne remplit pas les critères"]
            if r.get(24) == "Oui":
                return "Charge", ["Paiement récurrent"]
            return "Immobilisation incorporelle", ["Licence durable"]

        if r.get(19) == "Création en interne":
            if r.get(25) == "Recherche":
                return "Charge", ["Recherche non capitalisable"]
            checks = [26, 27, 28, 29, 30, 31]
            if all(r.get(x) for x in checks):
                return "Immobilisation incorporelle", ["Conditions IAS 38 remplies"]
            else:
                return "Charge", ["Conditions IAS 38 non remplies"]

        if r.get(19) == "Dépense liée à un actif":
            if r.get(32) == "Dépense" and r.get(33):
                return "Immobilisation corporelle", ["Dépense directement attribuable"]
            if r.get(32) == "Maintenance":
                if r.get(34) == "Après" and r.get(35) == "Évolutive":
                    return "Immobilisation corporelle", ["Maintenance évolutive"]
                elif r.get(34) == "Après" and r.get(35) == "Corrective":
                    return "Charge", ["Maintenance corrective"]
                elif r.get(34) == "Avant" and r.get(36):
                    return "Immobilisation corporelle", ["Mise en état opérationnel"]
                else:
                    return "Charge", ["Maintenance ponctuelle"]

    return None, []
