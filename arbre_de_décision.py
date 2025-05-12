import streamlit as st

st.set_page_config(
    page_title="UBCI – Assistant de Classification Comptable",
    page_icon="🏷️",
    layout="centered"
)

st.title("🏦 UBCI – Arbre de Décision Comptable Logique")

if "reponses" not in st.session_state:
    st.session_state.reponses = {}
r = st.session_state.reponses

# Réinitialisation
if st.button("🔄 Réinitialiser l'analyse"):
    st.session_state.reponses.clear()
    st.experimental_rerun()

st.markdown("---")

# Arbre de décision complet
def arbre_decision():
    if "Q1" not in r:
        r["Q1"] = st.radio("1. La dépense est-elle supérieure à 500 DT ?", ["Oui", "Non"])
        st.stop()
    if r["Q1"] == "Non":
        st.success("✅ Charge")
        return

    if "Q2" not in r:
        r["Q2"] = st.radio("2. La dépense concerne-t-elle un bien physique et tangible ?", ["Oui", "Non"])
        st.stop()
    if r["Q2"] == "Oui":
        branche_corporelle()
    else:
        branche_incorporelle()

def branche_corporelle():
    q = [
        ("Q3", "3. Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?"),
        ("Q4", "4. L'entreprise bénéficie-t-elle des avantages économiques futurs du bien ?"),
        ("Q5", "5. Le cout du bien peut-il être mesuré de manière fiable ?"),
        ("Q6", "6. Les risques et les produits sont-ils transférés à l'entreprise ?")
    ]
    for key, question in q:
        if key not in r:
            r[key] = st.radio(question, ["Oui", "Non"])
            st.stop()
        if r[key] == "Non":
            st.success("✅ Charge")
            return

    if "Q7" not in r:
        r["Q7"] = st.radio("7. La dépense correspond-elle à des frais d’étude ?", ["Oui", "Non"])
        st.stop()

    if r["Q7"] == "Oui":
        if "Q8" not in r:
            r["Q8"] = st.radio("8. Les frais d’étude engagés à l'origine sont-ils directement liés à un actif durable ?", ["Oui", "Non"])
            st.stop()
        if r["Q8"] == "Oui":
            st.success("✅ Immobilisation corporelle")
        else:
            st.success("✅ Charge")
        return

    if "Q9" not in r:
        r["Q9"] = st.radio("9. S'agit-il d'une nouvelle acquisition ?", ["Oui", "Non"])
        st.stop()

    if r["Q9"] == "Oui":
        st.success("✅ Immobilisation corporelle")
        return

    # Grosse réparation
    q_repa = [
        ("Q10", "10. La valeur vénale de la composante >= 1/4 de la valeur de l'actif ?"),
        ("Q11", "11. L'actif initial est-il identifié dans SAP en tant qu'investissement ?"),
        ("Q12", "12. Prolonge-t-il la durée de vie de l'élément ou augmente sa performance ?")
    ]
    for key, question in q_repa:
        if key not in r:
            r[key] = st.radio(question, ["Oui", "Non"])
            st.stop()
        if r[key] == "Non":
            st.success("✅ Charge")
            return

    if "Q13" not in r:
        r["Q13"] = st.radio("13. S'agit-il d’une réparation ou réhabilitation majeure d'infrastructures ?", ["Réparation", "Réhabilitation"])
        st.stop()

    if r["Q13"] == "Réhabilitation":
        st.success("✅ Immobilisation corporelle")
        return

    if "Q14" not in r:
        r["Q14"] = st.radio("14. La réparation présente-t-elle un caractère cyclique ?", ["Oui", "Non"])
        st.stop()
    if r["Q14"] == "Oui":
        st.success("✅ Immobilisation corporelle")
    else:
        st.success("✅ Charge")

def branche_incorporelle():
    q = [
        ("Q15", "15. L’élément est-il identifiable ?"),
        ("Q16", "16. Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?"),
        ("Q17", "17. L'entreprise contrôle-t-elle l'élément et en retire-t-elle des avantages économiques futurs probables ?"),
        ("Q18", "18. Le coût peut-il être mesuré de manière fiable ?")
    ]
    for key, question in q:
        if key not in r:
            r[key] = st.radio(question, ["Oui", "Non"])
            st.stop()
        if r[key] == "Non":
            st.success("✅ Charge")
            return

    if "Q19" not in r:
        r["Q19"] = st.radio("19. Nature de la dépense ?", ["Acquisition", "Création en interne", "Dépense liée à un actif"])
        st.stop()

    if r["Q19"] == "Acquisition":
        sous_branche_acquisition()
    elif r["Q19"] == "Création en interne":
        sous_branche_creation()
    else:
        sous_branche_depense_liee()

def sous_branche_acquisition():
    q = [
        ("Q20", "1. L'acquisition concerne-t-elle une licence ?"),
        ("Q21", "2. L'actif est-il hébergé sur une infrastructure contrôlée par l’entreprise ?"),
        ("Q22", "3. L’entreprise dispose-t-elle d’un droit d’usage distinct et exclusif ?"),
        ("Q23", "4. Le droit d’usage est-il permanent ou longue durée (≥ 3 ans) ?"),
        ("Q24", "5. Le contrat prévoit-il un abonnement/redevance/paiement récurrent ?")
    ]
    for key, question in q:
        if key not in r:
            r[key] = st.radio(question, ["Oui", "Non"])
            st.stop()
        if key == "Q24":
            if r[key] == "Oui":
                st.success("✅ Charge")
            else:
                st.success("✅ Immobilisation incorporelle")
        elif r[key] == "Non":
            st.success("✅ Charge")
            return

def sous_branche_creation():
    if "Q25" not in r:
        r["Q25"] = st.radio("1. Dépenses de recherche ou développement ?", ["Recherche", "Développement"])
        st.stop()
    if r["Q25"] == "Recherche":
        st.success("✅ Charge")
        return

    if "Q26" not in r:
        r["Q26"] = st.radio("2. Toutes les conditions IAS 38.57 sont-elles remplies ?", ["Oui", "Non"])
        st.stop()
    if r["Q26"] == "Oui":
        st.success("✅ Immobilisation incorporelle")
    else:
        st.success("✅ Charge")

def sous_branche_depense_liee():
    if "Q27" not in r:
        r["Q27"] = st.radio("1. S'agit-il d'une dépense ou maintenance ?", ["Dépense", "Maintenance"])
        st.stop()
    if r["Q27"] == "Dépense":
        if "Q28" not in r:
            r["Q28"] = st.radio("2. La dépense est-elle directement attribuable à la préparation de l'actif ?", ["Oui", "Non"])
            st.stop()
        if r["Q28"] == "Oui":
            st.success("✅ Immobilisation corporelle")
        else:
            st.success("✅ Charge")
        return
    else:
        if "Q29" not in r:
            r["Q29"] = st.radio("3. La dépense est-elle réalisée avant ou après mise en service ?", ["Avant", "Après"])
            st.stop()
        if r["Q29"] == "Après":
            if "Q30" not in r:
                r["Q30"] = st.radio("4. Maintenance évolutive ou corrective ?", ["Évolutive", "Corrective"])
                st.stop()
            if r["Q30"] == "Évolutive":
                st.success("✅ Immobilisation corporelle")
            else:
                st.success("✅ Charge")
        else:
            if "Q31" not in r:
                r["Q31"] = st.radio("5. La dépense est-elle directement nécessaire pour rendre l’actif opérationnel ?", ["Oui", "Non"])
                st.stop()
            if r["Q31"] == "Oui":
                st.success("✅ Immobilisation corporelle")
            else:
                st.success("✅ Charge")

arbre_decision()

with st.expander("📋 Suivi des réponses"):
    if r:
        for k, v in r.items():
            st.markdown(f"- **{k}** : `{v}`")
    else:
        st.info("Aucune réponse pour le moment.")

