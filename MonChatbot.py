import streamlit as st
import json
import pandas as pd

# =============================
# CONFIGURATION PAGE
# =============================
st.set_page_config(
    page_title="Chatbot - Reconversion 2026",
    layout="wide"
)

st.title("🤖 Chatbot - Reconversion professionnelle 2026")

st.markdown("""
### 📌 Instructions
1. Sélectionnez une question
2. Cliquez sur **Générer la réponse**
3. Consultez l’historique
4. Téléchargez les résultats si besoin
""")

# =============================
# CHARGEMENT DU DATASET JSON
# =============================

@st.cache_data
def load_dataset():
    with open("dataset_chatbot_reconversion_2026_complet.json", "r", encoding="utf-8") as f:
        return json.load(f)

dataset = load_dataset()

questions = [item["question"] for item in dataset]

# =============================
# FONCTION CHATBOT
# =============================

def ask_chatbot(question):
    for item in dataset:
        if item["question"] == question:
            return item["answer"]
    return "Réponse non trouvée."

# =============================
# INTERFACE UTILISATEUR
# =============================

selected_question = st.selectbox("📌 Choisissez une question :", questions)

if st.button("🚀 Générer la réponse"):
    response = ask_chatbot(selected_question)

    st.markdown("### 💬 Réponse :")
    st.success(response)

    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append({
        "Question": selected_question,
        "Réponse": response
    })

# =============================
# HISTORIQUE
# =============================

if "history" in st.session_state and st.session_state.history:

    st.markdown("---")
    st.markdown("## 📊 Historique des échanges")

    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Télécharger l'historique (CSV)",
        data=csv,
        file_name="historique_chatbot.csv",
        mime="text/csv"
    )