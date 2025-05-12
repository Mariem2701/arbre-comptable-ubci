import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

@st.cache_resource
def connect_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = st.secrets["google_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1oLsgO9f-4-b8-VAX_fvX3QVdqjIV0c9yfH-KK4kkmtI").sheet1
    return sheet

sheet = connect_sheet()

def enregistrer_reponse(question_id, libelle, reponse, service):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([str(question_id), libelle, str(reponse), service, timestamp])

st.set_page_config(page_title="UBCI - Arbre Comptable", layout="centered")
st.title("🏦 UBCI – Arbre de Décision Comptable Logique")

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

if "reponses" not in st.session_state:
    st.session_state.reponses = {}
if "details_depense" not in st.session_state:
    st.session_state.details_depense = {}
if "description_remplie" not in st.session_state:
    st.session_state.description_remplie = False

r = st.session_state.reponses

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
# Définition des questions (extrait de la version complète pour la clarté)
questions = {
    0: ("La dépense est-elle supérieure à 500 DT ?", "radio", ["Oui", "Non"], "Demandeur"),
    1: ("La dépense concerne-t-elle un bien physique et tangible ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),
    # Ajoutez ici toutes les autres questions selon le modèle précédemment fourni
}

# Fonction logique pour déterminer la prochaine question à poser
def get_next_question_id():
    r = st.session_state.reponses
    if 0 not in r:
        return 0
    if r[0] == "Non":
        return None
    if 1 not in r:
        return 1
    # Suivre l'arbre logique ici en ajoutant les vérifications dans l'ordre correct
    # Voir la logique précédente détaillée
    return None

# Affichage de la question suivante
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
            enregistrer_reponse(next_q, label, val, service_connecte)
            st.rerun()
    else:
        st.info(f"🕒 En attente de réponse du service **{service_resp}**")

# Suivi global
if service_connecte == "Comptabilité des immobilisations":
    st.markdown("### 📋 Suivi en temps réel")
    for qid in r:
        label, _, _, who = questions[qid]
        st.markdown(f"✅ **{label}** — *{who}* : {r[qid]}")

# Résultat final (à adapter selon toutes les nouvelles branches ajoutées)
if service_connecte == "Comptabilité des immobilisations":
    st.markdown("### ✅ Résultat final automatique")
    result = None
    justif = []

    # Exemple : logique partielle à compléter selon toutes les branches définies
    if r.get(0) == "Non":
        result = "Charge"
        justif.append("Montant < 500 DT")

    if result:
        st.success(f"🏷️ **Résultat** : {result}")
        if justif:
            st.markdown("**Justification :**")
            for j in justif:
                st.markdown(f"- {j}")
    else:
        st.info("⏳ Résultat en attente – toutes les réponses nécessaires ne sont pas encore remplies.")


