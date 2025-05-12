# main.py
import streamlit as st
from questions import QUESTIONS
from logique import get_next_question_id, evaluate_final_result
import pandas as pd
from io import BytesIO

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

# Description Dépense
st.markdown("### 📝 Description de la dépense")
if service_connecte == "Comptabilité des immobilisations" and not st.session_state.description_remplie:
    libelle = st.text_input("📌 Intitulé de la dépense :", key="libelle")
    description = st.text_area("🧾 Description :", key="description")
    if st.button("✅ Enregistrer"):
        if libelle.strip():
            st.session_state.details_depense = {"libelle": libelle, "description": description}
            st.session_state.description_remplie = True
            st.success("✅ Dépense enregistrée.")
        else:
            st.warning("⚠️ Intitulé requis.")
elif st.session_state.description_remplie:
    st.info(f"📌 **Dépense** : {st.session_state.details_depense['libelle']}")
    st.markdown(f"🧾 **Description** : {st.session_state.details_depense['description']}")
else:
    st.warning("⏳ En attente de saisie par la Comptabilité des immobilisations.")

# Logique
next_q = get_next_question_id(r)
if next_q is not None:
    label, qtype, options, service_resp, help_text = QUESTIONS[next_q]

    st.markdown("### 📌 Question actuelle")
    st.markdown(f"**➡️ {label}**")
    st.markdown(f"👤 Destinée à : **{service_resp}**")
    if help_text:
        with st.expander("📘 Aide contextuelle"):
            st.markdown(help_text)

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

# Suivi SCI
if service_connecte == "Comptabilité des immobilisations":
    st.markdown("### 📋 Suivi en temps réel")
    for qid in r:
        label, _, _, who, _ = QUESTIONS[qid]
        st.markdown(f"✅ **{label}** — *{who}* : {r[qid]}")

# Résultat Final
if service_connecte == "Comptabilité des immobilisations":
    st.markdown("### ✅ Résultat final automatique")
    result, justifications = evaluate_final_result(r)
    if result:
        st.success(f"🏷️ **Résultat** : {result}")
        if justifications:
            st.markdown("**Justification :**")
            for j in justifications:
                st.markdown(f"- {j}")

        if st.button("⬇️ Télécharger le rapport Excel"):
            output = BytesIO()
            df = pd.DataFrame.from_dict(r, orient='index', columns=['Réponse'])
            df.to_excel(output, index_label='Question')
            st.download_button(
                label="📄 Télécharger",
                data=output.getvalue(),
                file_name="rapport_classification.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.info("⏳ Résultat en attente – toutes les réponses nécessaires ne sont pas encore remplies.")

