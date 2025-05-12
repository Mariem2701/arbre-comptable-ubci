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

# === QUESTIONS (Exemple partiel pour démarrer) ===
questions = {
    1: ("La dépense est-elle supérieure à 500 DT ?", "radio", ["Oui", "Non"], "Demandeur"),
    2: ("La dépense concerne-t-elle un bien physique et tangible ?", "radio", ["Oui", "Non"], "Demandeur"),
    3: ("Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?", "radio", ["Oui", "Non"], "Demandeur"),
    4: ("L'entreprise bénéficie-t-elle des avantages économiques futurs du bien ?", "radio", ["Oui", "Non"], "Contrôle de gestion"),
    5: ("Le cout du bien peut-il être mesuré de manière fiable ?", "radio", ["Oui", "Non"], "Fournisseurs / Comptabilité"),
    6: ("Les risques et les produits sont-ils transférés à l'entreprise ?", "radio", ["Oui", "Non"], "Achats"),
    7: ("La dépense correspond-elle à des frais d’étude ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),
    8: ("Les frais d’étude sont-ils directement liés à un actif durable ?", "radio", ["Oui", "Non"], "Contrôle de gestion"),
    9: ("S'agit-il d'une nouvelle acquisition ?", "radio", ["Oui", "Non"], "Achats"),
    10: ("La valeur vénale de la composante >= 1/4 de l'actif ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),
    11: ("L'actif est-il identifié dans SAP comme investissement ?", "radio", ["Oui", "Non"], "IT / Juridique"),
    12: ("Prolonge-t-il la durée de vie ou augmente sa performance ?", "radio", ["Oui", "Non"], "Contrôle de gestion"),
    13: ("S'agit-il d’une réparation ou réhabilitation majeure ?", "radio", ["Réhabilitation", "Réparation"], "Comptabilité des immobilisations"),
    14: ("La réparation est-elle cyclique ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),
    # INCORPORELLES à partir de 15... jusqu'à 64 (à insérer ensuite)
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

