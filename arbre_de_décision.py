import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

st.set_page_config(page_title="UBCI - Arbre Comptable", layout="centered")
st.title("🏦 UBCI – Arbre de Décision Comptable Logique")

# Connexion à Google Sheets via secrets
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

# Fonction pour enregistrer chaque réponse
def enregistrer_reponse(question_id, libelle, reponse, service):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([str(question_id), libelle, str(reponse), service, timestamp])

# SERVICES SIMPLIFIÉS
services = [
    "Demandeur",
    "Comptabilité des immobilisations",
    "Comptabilité des fournisseurs",
    "Achats",
    "Contrôle de gestion",
    "IT",
    "Juridique",
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

# --- DÉFINITION DE L’ARBRE LOGIQUE SIMPLIFIÉ (extrait) ---
questions = {
    0: ("Montant de la dépense (DT)", "number", None, "Demandeur"),
    1: ("La dépense concerne-t-elle un bien physique et tangible ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),
    2: ("Utilisation > 1 an ?", "radio", ["Oui", "Non"], "Demandeur"),
    3: ("Avantages économiques futurs ?", "radio", ["Oui", "Non"], "Contrôle de gestion")
    # À compléter avec le reste des questions...
}

# 🔁 LOGIQUE DE L’ARBRE

def get_next_question_id():
    if 0 not in r:
        return 0
    if r[0] < 500:
        return None
    if 1 not in r:
        return 1
    if r[1] == "Oui":
        for q in [2, 3]:
            if q not in r:
                return q
    return None

# 🔍 AFFICHAGE DE LA QUESTION ACTUELLE
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

        if st.button("✅ Valider la réponse"):
            r[next_q] = val
            enregistrer_reponse(next_q, label, val, service_connecte)
            st.rerun()
    else:
        st.info(f"🕒 En attente de réponse du service **{service_resp}**")

# 👁️ SUIVI GLOBAL POUR LE SCI
if service_connecte == "Comptabilité des immobilisations":
    st.markdown("### 📋 Suivi en temps réel")
    for qid in r:
        label, _, _, who = questions[qid]
        st.markdown(f"✅ **{label}** — *{who}* : `{r[qid]}`")


