import streamlit as st

st.set_page_config(page_title="UBCI - Arbre Comptable", layout="centered")
st.title("🏦 UBCI – Arbre de Décision Comptable Logique")

# SERVICES SIMPLIFIÉS
services = [
    "Demandeur",
    "Comptabilité des immobilisations",
    "Fournisseurs / Comptabilité",
    "Achats",
    "Contrôle de gestion",
    "IT / Juridique",
    "RH"
]
service_connecte = st.selectbox("👤 Connecté en tant que :", services)

# SESSION STATE
if "reponses" not in st.session_state:
    st.session_state.reponses = {}
if "details_depense" not in st.session_state:
    st.session_state.details_depense = {}
if "description_remplie" not in st.session_state:
    st.session_state.description_remplie = False

r = st.session_state.reponses

# SAISIE DÉPENSE PAR SCI
st.markdown("### 📝 Description de la dépense")
if service_connecte == "Comptabilité des immobilisations" and not st.session_state.description_remplie:
    libelle = st.text_input("📌 Intitulé de la dépense :", key="libelle")
    description = st.text_area("🧾 Description :", key="description")
    if st.button("✅ Enregistrer"):
        if libelle.strip():
            st.session_state.details_depense = {
                "libelle": libelle,
                "description": description
            }
            st.session_state.description_remplie = True
            st.success("✅ Dépense enregistrée.")
        else:
            st.warning("⚠️ Intitulé requis.")
elif st.session_state.description_remplie:
    st.info(f"📌 **Dépense** : {st.session_state.details_depense['libelle']}")
    st.markdown(f"🧾 **Description** : {st.session_state.details_depense['description']}")
else:
    st.warning("⏳ En attente de saisie par la Comptabilité des immobilisations.")

# --- NOUVEL ARBRE LOGIQUE ---
questions = {
    0: ("La dépense est-elle supérieure à 500 DT ?", "radio", ["Oui", "Non"], "Demandeur"),
    1: ("La dépense concerne-t-elle un bien physique et tangible ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),

    # Immobilisations corporelles
    2: ("Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?", "radio", ["Oui", "Non"], "Demandeur"),
    3: ("L'entreprise bénéficie-t-elle des avantages économiques futurs du bien ?", "radio", ["Oui", "Non"], "Contrôle de gestion"),
    4: ("Le cout du bien peut-il être mesuré de manière fiable ?", "radio", ["Oui", "Non"], "Fournisseurs / Comptabilité"),
    5: ("Les risques et les produits sont-ils transférés à l'entreprise ?", "radio", ["Oui", "Non"], "Achats"),
    6: ("La dépense correspond-elle à des frais d’étude ?", "radio", ["Oui", "Non"], "Achats"),
    7: ("Les frais d’étude engagés sont-ils directement liés à un actif durable ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),
    8: ("S'agit-il d'une nouvelle acquisition ?", "radio", ["Oui", "Non"], "Achats"),
    9: ("La valeur vénale de la composante >= 1/4 de la valeur de l'actif ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),
    10: ("L'actif initial est-il identifié dans SAP en tant qu'investissement ?", "radio", ["Oui", "Non"], "IT / Juridique"),
    11: ("Prolonge-t-il la durée de vie ou augmente sa performance ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),
    12: ("S'agit-il d’une réparation ou réhabilitation majeure d'infrastructures ?", "radio", ["Réparation", "Réhabilitation majeure"], "Comptabilité des immobilisations"),
    13: ("La réparation présente-t-elle un caractère cyclique ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),

    # Immobilisations incorporelles
    100: ("L’élément est-il identifiable ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),
    101: ("Est-il destiné à être utilisé pour plus d'un exercice ( > 1 an ) ?", "radio", ["Oui", "Non"], "Demandeur"),
    102: ("L'entreprise contrôle-t-elle l'élément et en retire-t-elle des avantages économiques futurs probables ?", "radio", ["Oui", "Non"], "Contrôle de gestion"),
    103: ("Le cout peut-il être mesuré de manière fiable ?", "radio", ["Oui", "Non"], "Fournisseurs / Comptabilité"),
    104: ("S'agit-il d'une acquisition, création en interne ou dépense liée à un actif ?", "radio", ["Acquisition", "Création en interne", "Dépense liée à un actif"], "Comptabilité des immobilisations"),

    # Sous-branche Acquisition
    105: ("L'acquisition concerne-t-elle une licence ?", "radio", ["Oui", "Non"], "IT / Juridique"),
    106: ("L'actif est-il hébergé sur une infrastructure contrôlée par l’entreprise ?", "radio", ["Oui", "Non"], "IT / Juridique"),
    107: ("L’entreprise dispose-t-elle d’un droit d’usage distinct et exclusif de l'actif ?", "radio", ["Oui", "Non"], "IT / Juridique"),
    108: ("Le droit d’usage est-il permanent (licence perpétuelle) ou accordé pour une longue période ?", "radio", ["Oui", "Non"], "IT / Juridique"),
    109: ("Le contrat prévoit-il un abonnement/redevance/paiement récurrent ?", "radio", ["Oui", "Non"], "Fournisseurs / Comptabilité"),

    # Sous-branche Création en interne
    201: ("Dépenses de recherche ou développement ?", "radio", ["Recherche", "Développement"], "Comptabilité des immobilisations"),
    202: ("Faisabilité technique ?", "checkbox", None, "IT / Juridique"),
    203: ("Intention d’achever le projet ?", "checkbox", None, "IT / Juridique"),
    204: ("Capacité à utiliser ou vendre l’actif ?", "checkbox", None, "IT / Juridique"),
    205: ("Avantages économiques futurs probables ?", "checkbox", None, "Contrôle de gestion"),
    206: ("Ressources disponibles ?", "checkbox", None, "Contrôle de gestion"),
    207: ("Dépenses évaluées de façon fiable ?", "checkbox", None, "Fournisseurs / Comptabilité"),

    # Sous-branche Dépenses liées à un actif
    301: ("S'agit-il d'une dépense de maintenance ?", "radio", ["Dépense", "Maintenance"], "Comptabilité des immobilisations"),
    302: ("La dépense est-elle directement attribuables à la préparation de l'actif en vue de son utilisation ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),
    303: ("La dépense concerne-t-elle des opérations de maintenance réalisées avant ou après la mise en service de l’actif ?", "radio", ["Avant", "Après"], "Comptabilité des immobilisations"),
    304: ("La dépense concerne-t-elle une maintenance évolutive ou corrective ?", "radio", ["Évolutive", "Corrective"], "Comptabilité des immobilisations"),
    305: ("La dépense est-elle directement nécessaire pour rendre l’actif opérationnel ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations")
}

# === LOGIQUE DE NAVIGATION ===
def get_next_question_id():
    r = st.session_state.reponses

    if 1 not in r:
        return 1
    if r[1] == "Non":
        return None
    if 2 not in r:
        return 2
    if r[2] == "Oui":
        for q in range(3, 7):
            if q not in r:
                return q
        if r.get(7) == "Oui":
            return 8
        elif r.get(7) == "Non":
            if 9 not in r:
                return 9
            if r[9] == "Non":
                for q in range(10, 15):
                    if q not in r:
                        return q
    elif r[2] == "Non":
        return 15  # début des incorporelles
    return None

# === AFFICHAGE QUESTION ===
next_q = get_next_question_id()
if next_q is not None:
    label, qtype, options, service_resp = questions[next_q]

    st.markdown("### 📌 Question actuelle")
    st.markdown(f"**➡️ {label}**")
    st.markdown(f"👤 Destinée à : **{service_resp}**")

    if service_connecte == service_resp or service_connecte == "Comptabilité des immobilisations":
        key = f"q_{next_q}"
        if qtype == "number":
            val = st.number_input("Réponse :", min_value=0.0, format="%.2f", key=key)
        elif qtype == "radio":
            val = st.radio("Réponse :", options, key=key, index=None)
        elif qtype == "checkbox":
            val = st.checkbox("Cocher si applicable", key=key)
        if st.button("✅ Valider la réponse"):
            r[next_q] = val
            st.rerun()
    else:
        st.info(f"🕒 En attente de réponse du service **{service_resp}**")

# === SUIVI GLOBAL ===
if service_connecte == "Comptabilité des immobilisations":
    st.markdown("### 📋 Suivi en temps réel")
    for qid in sorted(r):
        label, _, _, who = questions.get(qid, ("(Question inconnue)", "", "", ""))
        st.markdown(f"✅ **{label}** — *{who}* : `{r[qid]}`")

# === CALCUL AUTOMATIQUE DU RÉSULTAT FINAL (extrait simplifié) ===
def calculer_resultat_final():
    result = None
    justif = []
    r = st.session_state.reponses

    if r.get(1) == "Non":
        result = "Charge"
        justif.append("Montant < 500 DT")
    elif r.get(2) == "Oui":
        if any(r.get(x) == "Non" for x in [3, 4, 5, 6]):
            result = "Charge"
            justif.append("Critères non remplis pour immobilisation corporelle")
        elif r.get(7) == "Oui" and r.get(8) == "Non":
            result = "Charge"
            justif.append("Frais d’étude non liés à un actif durable")
        elif r.get(9) == "Oui":
            result = "Immobilisation corporelle"
        elif r.get(13) == "Réhabilitation":
            result = "Immobilisation corporelle"
        elif r.get(14) == "Oui":
            result = "Immobilisation corporelle"
        elif r.get(14) == "Non":
            result = "Charge"
            justif.append("Réparation ponctuelle")
    # Ajout des cas pour incorporelles à venir ici…
    return result, justif

# === AFFICHAGE RÉSULTAT ===
if service_connecte == "Comptabilité des immobilisations":
    st.markdown("### ✅ Résultat final automatique")
    result, justif = calculer_resultat_final()
    if result:
        st.success(f"🏷️ **Résultat** : {result}")
        if justif:
            st.markdown("**Justification :**")
            for j in justif:
                st.markdown(f"- {j}")
    else:
        st.info("⏳ Résultat en attente – toutes les réponses nécessaires ne sont pas encore remplies.")

