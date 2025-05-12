import streamlit as st
import json
import os
from datetime import datetime

# Constants
DATA_FILE = "responses.json"
SERVICES = [
    "Demandeur",
    "Comptabilité des immobilisations",
    "Comptabilité des fournisseurs",
    "Achats",
    "Contrôle de gestion",
    "IT",
    "Juridique",
    "RH"
]

# Load or initialize data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# Select user/service
st.sidebar.title("Identification")
user = st.sidebar.text_input("Nom de l'utilisateur")
service = st.sidebar.selectbox("Votre service", SERVICES)

if not user:
    st.warning("Veuillez entrer votre nom dans la barre latérale pour commencer.")
    st.stop()

# User key
user_key = f"{user} - {service}"
if user_key not in data:
    data[user_key] = {"service": service, "responses": {}, "timestamp": str(datetime.now())}

st.title("Arbre de Décision - Classification des Dépenses")

# Helper to show question and save response
def ask_question(q_id, question, options):
    response = st.radio(question, options, key=q_id)
    data[user_key]["responses"][q_id] = response
    save_data(data)
    return response

# Start decision tree
q1 = ask_question("q1", "1- La dépense est-elle supérieure à 500 DT ?", ["Oui", "Non"])
if q1 == "Non":
    st.success("=> Charge")
    st.stop()

q2 = ask_question("q2", "2- La dépense concerne-t-elle un bien physique et tangible ?", ["Oui", "Non"])
if q2 == "Oui":
    st.subheader("Branche Immobilisation Corporelle")
    q3 = ask_question("q3", "3- Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?", ["Oui", "Non"])
    if q3 == "Non": st.success("=> Charge"); st.stop()
    q4 = ask_question("q4", "4- L'entreprise bénéficie-t-elle des avantages économiques futurs ?", ["Oui", "Non"])
    if q4 == "Non": st.success("=> Charge"); st.stop()
    q5 = ask_question("q5", "5- Le cout peut-il être mesuré de manière fiable ?", ["Oui", "Non"])
    if q5 == "Non": st.success("=> Charge"); st.stop()
    q6 = ask_question("q6", "6- Les risques et produits sont-ils transférés ?", ["Oui", "Non"])
    if q6 == "Non": st.success("=> Charge"); st.stop()
    q7 = ask_question("q7", "7- La dépense correspond-elle à des frais d'étude ?", ["Oui", "Non"])
    if q7 == "Oui":
        q8 = ask_question("q8", "8- Les frais d'étude sont-ils liés à un actif durable ?", ["Oui", "Non"])
        if q8 == "Oui": st.success("=> Immobilisation corporelle")
        else: st.success("=> Charge")
        st.stop()
    else:
        q9 = ask_question("q9", "9- S'agit-il d'une nouvelle acquisition ?", ["Oui", "Non"])
        if q9 == "Oui":
            st.success("=> Immobilisation corporelle")
            st.stop()
        else:
            st.subheader("Sous-branche Grosse Réparation")
            q10 = ask_question("q10", "10- Valeur vénale composante >= 1/4 actif ?", ["Oui", "Non"])
            if q10 == "Non": st.success("=> Charge"); st.stop()
            q11 = ask_question("q11", "11- Actif identifié dans SAP comme investissement ?", ["Oui", "Non"])
            if q11 == "Non": st.success("=> Charge"); st.stop()
            q12 = ask_question("q12", "12- Prolonge la durée de vie ou améliore la performance ?", ["Oui", "Non"])
            if q12 == "Non": st.success("=> Charge"); st.stop()
            q13 = ask_question("q13", "13- Réparation ou réhabilitation majeure ?", ["Réparation", "Réhabilitation majeure"])
            if q13 == "Réhabilitation majeure":
                st.success("=> Immobilisation corporelle")
                st.stop()
            q14 = ask_question("q14", "14- Réparation cyclique ?", ["Oui", "Non"])
            if q14 == "Oui": st.success("=> Immobilisation corporelle")
            else: st.success("=> Charge")
            st.stop()
else:
    st.subheader("Branche Immobilisation Incorporelle")
    q15 = ask_question("q15", "15- L'élément est-il identifiable ?", ["Oui", "Non"])
    if q15 == "Non": st.success("=> Charge"); st.stop()
    q16 = ask_question("q16", "16- Utilisé pour plus d'un exercice ?", ["Oui", "Non"])
    if q16 == "Non": st.success("=> Charge"); st.stop()
    q17 = ask_question("q17", "17- Contrôle et avantages futurs ?", ["Oui", "Non"])
    if q17 == "Non": st.success("=> Charge"); st.stop()
    q18 = ask_question("q18", "18- Coût mesurable ?", ["Oui", "Non"])
    if q18 == "Non": st.success("=> Charge"); st.stop()
    q19 = ask_question("q19", "19- Nature de la dépense ?", ["Acquisition", "Création en interne", "Dépense liée à un actif"])
    st.success("La suite des branches internes n'est pas encore déployée dans ce prototype.")
    st.stop()

# Admin view
if service == "Comptabilité des immobilisations":
    st.sidebar.markdown("---")
    st.sidebar.subheader("Vue Comptabilité Immobilisations")
    if st.sidebar.button("Afficher les réponses de tous les services"):
        st.header("Toutes les réponses enregistrées")
        for user, record in data.items():
            st.subheader(user)
            for qid, ans in record["responses"].items():
                st.write(f"**{qid}**: {ans}")


