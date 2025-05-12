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

# Dictionnaire des questions
questions = {
    # [Question ID]: (Label, Type, Options, Service)
    # COMMUNES
    1: ("La dépense est-elle supérieure à 500 DT ?", "radio", ["Oui", "Non"], "Demandeur"),
    2: ("La dépense concerne-t-elle un bien physique et tangible ?", "radio", ["Oui", "Non"], "Demandeur"),
    # ... Les autres questions sont déjà définies dans le dictionnaire (voir structure précédente)
}

# Logique de navigation

def get_next_question_id():
    r = st.session_state.reponses

    if 1 not in r:
        return 1
    if r[1] == "Non":
        return None  # Montant inférieur à 500 DT => Charge

    if 2 not in r:
        return 2

    if r[2] == "Oui":
        for q in range(10, 15):
            if q not in r:
                return q
        if r.get(14) == "Oui":
            return 15
        if r.get(14) == "Non":
            if 16 not in r:
                return 16
            if r[16] == "Non":
                for q in range(17, 22):
                    if q not in r:
                        return q
    elif r[2] == "Non":
        for q in range(30, 35):
            if q not in r:
                return q
        if r[34] == "Acquisition":
            for q in range(40, 45):
                if q not in r:
                    return q
        elif r[34] == "Création en interne":
            if 50 not in r:
                return 50
            if r[50] == "Développement":
                for q in range(51, 57):
                    if q not in r:
                        return q
        elif r[34] == "Dépense liée à un actif":
            for q in range(60, 65):
                if q not in r:
                    return q

    return None

# AFFICHAGE QUESTION
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

# SUIVI GLOBAL
if service_connecte == "Comptabilité des immobilisations":
    st.markdown("### 📋 Suivi en temps réel")
    for qid in r:
        label, _, _, who = questions[qid]
        st.markdown(f"✅ **{label}** — *{who}* : `{r[qid]}`")

# CALCUL AUTOMATIQUE DU RÉSULTAT
if service_connecte == "Comptabilité des immobilisations":
    st.markdown("### ✅ Résultat final automatique")
    result = None
    justif = []

    # Exemple partiel de logique (à étendre selon le nouvel arbre)
    if r.get(1) == "Non":
        result = "Charge"
        justif.append("Montant < 500 DT")
    elif r.get(2) == "Oui":
        if any(r.get(x) == "Non" for x in [10, 11, 12, 13]):
            result = "Charge"
            justif.append("Critères corporels non remplis")
        else:
            result = "Immobilisation corporelle"
    elif r.get(2) == "Non":
        if any(r.get(x) == "Non" for x in [30, 31, 32, 33]):
            result = "Charge"
            justif.append("Critères incorporels non remplis")
        elif r.get(34) == "Création en interne":
            if r.get(50) == "Recherche":
                result = "Charge"
                justif.append("Phase de recherche non immobilisable")
            else:
                checks = [51, 52, 53, 54, 55, 56]
                if all(r.get(x) for x in checks):
                    result = "Immobilisation incorporelle"
                else:
                    result = "Charge"
                    justif.append("Critères IAS 38 non remplis")

    if result:
        st.success(f"🏷️ **Résultat** : {result}")
        if justif:
            st.markdown("**Justification :**")
            for j in justif:
                st.markdown(f"- {j}")
    else:
        st.info("⏳ Résultat en attente – toutes les réponses nécessaires ne sont pas encore remplies.")

