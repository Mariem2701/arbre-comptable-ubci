import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

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











import streamlit as st

st.set_page_config(page_title="UBCI - Arbre Comptable", layout="centered")
st.title("🏦 UBCI – Arbre de Décision Comptable Logique")

# SERVICES SIMPLIFIÉS
services = [
    "Demandeur",
    "Comptabilité des immobilisations",  # SCI
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
# --- DÉFINITION DE L’ARBRE LOGIQUE ---
questions = {
    # COMMUNES
    0: ("Montant de la dépense (DT)", "number", None, "Demandeur"),
    1: ("La dépense concerne-t-elle un bien physique et tangible ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),

    # CORPORELLES
    2: ("Utilisation > 1 an ?", "radio", ["Oui", "Non"], "Demandeur"),
    3: ("Avantages économiques futurs ?", "radio", ["Oui", "Non"], "Contrôle de gestion"),
    4: ("Coût mesurable ?", "radio", ["Oui", "Non"], "Fournisseurs / Comptabilité"),
    5: ("Risques/produits transférés ?", "radio", ["Oui", "Non"], "Achats"),
    6: ("Nouvelle acquisition ?", "radio", ["Oui", "Non"], "Achats"),
    7: ("Grosse réparation ≥ 1/4 actif ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),
    8: ("Réhabilitation ou remplacement cyclique ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),
    9: ("Identifié dans SAP comme investissement ?", "radio", ["Oui", "Non"], "IT / Juridique"),
    10: ("Prolonge durée de vie ou augmente performance ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),
    11: ("Paiement récurrent ou échelonné ?", "radio", ["Récurrent", "Échelonné"], "Fournisseurs / Comptabilité"),

    # INCORPORELLES
    100: ("Élément identifiable ?", "radio", ["Oui", "Non"], "Comptabilité des immobilisations"),
    101: ("Utilisation prévue > 1 an ?", "radio", ["Oui", "Non"], "Demandeur"),
    102: ("Contrôle + avantages économiques ?", "radio", ["Oui", "Non"], "Contrôle de gestion"),
    103: ("Coût mesurable de manière fiable ?", "radio", ["Oui", "Non"], "Fournisseurs / Comptabilité"),
    104: ("Acquis ou créé en interne ?", "radio", ["Acquis", "Créé en interne"], "Comptabilité des immobilisations"),

    # CRÉATION INTERNE
    201: ("Recherche ou Développement ?", "radio", ["Recherche", "Développement"], "Comptabilité des immobilisations"),
    202: ("✔ Faisabilité technique", "checkbox", None, "IT / Juridique"),
    203: ("✔ Intention d’achever le projet", "checkbox", None, "IT / Juridique"),
    204: ("✔ Capacité à utiliser ou vendre l’actif", "checkbox", None, "IT / Juridique"),
    205: ("✔ Avantages économiques futurs probables", "checkbox", None, "Contrôle de gestion"),
    206: ("✔ Ressources disponibles", "checkbox", None, "Contrôle de gestion"),
    207: ("✔ Dépenses évaluées de façon fiable", "checkbox", None, "Fournisseurs / Comptabilité"),

    # ACQUISITION
    105: ("L'acquisition concerne-t-elle une licence ?", "radio", ["Oui", "Non"], "IT / Juridique"),
    106: ("La licence est-elle de nature éphémère ?", "radio", ["Oui", "Non"], "IT / Juridique"),
    107: ("Prix d’achat ou dépense ?", "radio", ["Prix d'achat", "Dépense"], "Achats"),
    135: ("✔ Coût du personnel lié à la mise en service", "checkbox", None, "RH"),
    136: ("✔ Honoraires de mise en service", "checkbox", None, "Comptabilité des immobilisations"),
    137: ("✔ Tests de bon fonctionnement", "checkbox", None, "Comptabilité des immobilisations"),
}
# 🔁 LOGIQUE DE L’ARBRE ET AFFICHAGE PAR SERVICE
def get_next_question_id():
    if 0 not in r:
        return 0
    if r[0] < 500:
        return None  # Charge directe, pas d'arbre
    if 1 not in r:
        return 1
    if r[1] == "Oui":
        for q in [2, 3, 4, 5, 6]:
            if q not in r:
                return q
        if r.get(6) == "Oui":
            return 11
        for q in [7, 8, 9, 10, 11]:
            if q not in r:
                return q
    if r[1] == "Non":
        for q in [100, 101, 102, 103, 104]:
            if q not in r:
                return q
        if r.get(104) == "Créé en interne":
            if 201 not in r:
                return 201
            if r.get(201) == "Recherche":
                return None  # Fin : charge
            for q in [202, 203, 204, 205, 206, 207]:
                if q not in r:
                    return q
        elif r.get(104) == "Acquis":
            if 105 not in r:
                return 105
            if r.get(105) == "Oui":
                if 106 not in r:
                    return 106
            elif r.get(105) == "Non":
                if 107 not in r:
                    return 107
                if r.get(107) == "Dépense":
                    for q in [135, 136, 137]:
                        if q not in r:
                            return q
    return None  # Fin du parcours

# 🔍 AFFICHAGE LOGIQUE DE LA QUESTION ACTUELLE
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

# 👁️ SUIVI GLOBAL POUR LE SCI
if service_connecte == "Comptabilité des immobilisations":
    st.markdown("### 📋 Suivi en temps réel")
    for qid in r:
        label, _, _, who = questions[qid]
        st.markdown(f"✅ **{label}** — *{who}* : `{r[qid]}`")
# ✅ CALCUL DU RÉSULTAT FINAL (réservé SCI)
if service_connecte == "Comptabilité des immobilisations":
    st.markdown("### ✅ Résultat final automatique")

    result = None
    justif = []

    if r.get(0) is not None and r.get(0) < 500:
        result = "Charge"
        justif.append("Montant < 500 DT")
    elif r.get(1) == "Oui":
        if any(r.get(x) == "Non" for x in [2, 3, 4, 5, 7, 8, 9, 10]):
            result = "Charge"
            justif.append("Un ou plusieurs critères corporels manquants")
        elif r.get(11) == "Récurrent":
            result = "Charge"
            justif.append("Paiement récurrent")
        elif r.get(11) == "Échelonné":
            result = "Immobilisation corporelle"
    elif r.get(1) == "Non":
        if any(r.get(x) == "Non" for x in [100, 101, 102, 103]):
            result = "Charge"
            justif.append("Critères incorporels manquants")
        elif r.get(104) == "Créé en interne":
            if r.get(201) == "Recherche":
                result = "Charge"
                justif.append("Recherche non immobilisable")
            elif r.get(201) == "Développement":
                checks = [202, 203, 204, 205, 206, 207]
                if all(r.get(x) for x in checks):
                    result = "Immobilisation incorporelle"
                else:
                    result = "Charge"
                    justif.append("Conditions IAS 38 non remplies")
        elif r.get(104) == "Acquis":
            if r.get(105) == "Oui" and r.get(106) == "Oui":
                result = "Charge"
                justif.append("Licence éphémère")
            elif r.get(105) == "Oui" and r.get(106) == "Non":
                result = "Immobilisation incorporelle"
            elif r.get(105) == "Non":
                if r.get(107) == "Prix d'achat":
                    result = "Immobilisation incorporelle"
                elif r.get(107) == "Dépense":
                    if any(r.get(x) for x in [135, 136, 137]):
                        result = "Immobilisation incorporelle"
                    else:
                        result = "Charge"
                        justif.append("Dépense non directement attribuable")

    if result:
        st.success(f"🏷️ **Résultat** : {result}")
        if justif:
            st.markdown("**Justification :**")
            for j in justif:
                st.markdown(f"- {j}")
    else:
        st.info("⏳ Résultat en attente – toutes les réponses nécessaires ne sont pas encore remplies.")
